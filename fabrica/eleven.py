"""Gera a narração com o ElevenLabs e salva em projetos/<nome>/audio/ (parte1…, short1…, tiktok1…).

Só gera o que ainda não existe, então rodar de novo não gasta crédito.
O resto da fábrica trata esses arquivos como áudio gravado (alinhamento, legenda karaokê etc.).

  ELEVENLABS_KEY=... python -m fabrica.eleven <projeto>

projeto.json → "voz": {"motor": "eleven", "eleven_voz": "Will", "modelo": "<id opcional>"}
"""
import json, os, sys
import requests

from .alinhar import achar_audio

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.elevenlabs.io"


def nota(t, m):
    print(f"::notice title={t}::{m}", flush=True)


def aviso(t, m):
    print(f"::warning title={t}::{m}", flush=True)


# como a voz deve falar siglas que ela lê errado (o texto da legenda continua igual)
# como a voz deve FALAR (a legenda continua com a grafia certa); cada projeto pode somar mais em "pronuncia"
PRONUNCIA = {"pt": [(r"\bQAs\b", "kiuêis"), (r"\bQA\b", "kiuêi"), (r"\bQ&A\b", "perguntas e respostas"),
                    (r"\bKolynos\b", "Colínos"), (r"\bNestlé\b", "Nestlê"), (r"\b(CADE|Cade)\b", "Cádi"), (r"\bChokito\b", "Chokíto")]}


def falado(p, t):
    import re
    for a, b in PRONUNCIA.get(idioma_de(p), []) + [tuple(x) for x in (p.get("pronuncia") or [])]:
        t = re.sub(a, b, t)
    return t


def textos(p):
    out = []
    for k, g in enumerate(p["script"]["long"]["parts"]):
        out.append((f"parte{k + 1}", g))
    for i, g in enumerate(p["script"].get("shorts", [])):
        out.append((f"short{i + 1}", g))
    for i, g in enumerate(p["script"].get("tiktoks", [])):
        out.append((f"tiktok{i + 1}", g))
    # frases marcadas "abertura" não vão para o TTS: o áudio delas é a intro do canal (canal/intro.mp3, ou intro_en.mp3…), colado na frente.
    # Se o idioma ainda não tem intro gravada, a abertura é narrada junto com o resto.
    pula = os.path.exists(intro_de(p))
    # "pausa": N segundos de silêncio depois da frase (ex.: desafio "pausa o vídeo e tenta"). Vira a marca ⟨pausa:N⟩: o áudio é gerado
    # em pedaços cortados nela e o silêncio exato é colado entre eles (a tag [silence] do v4 dá ~2 s, e várias seguidas não somam)
    def com_pausa(s):
        return s["text"].strip() + (f" ⟨pausa:{s['pausa']}⟩" if s.get("pausa") else "")
    return [(n, falado(p, " ".join(com_pausa(s) for s in g["sentences"] if s.get("text", "").strip() and not (pula and s.get("abertura"))))) for n, g in out]


def idioma_de(p):
    return (p.get("idioma") or "pt").lower()[:2]


def intro_de(p):
    i = idioma_de(p)
    return os.path.join(RAIZ, "canal", "intro.mp3" if i == "pt" else f"intro_{i}.mp3")


def com_abertura(p, nome):
    for g, n in [(g, f"parte{k + 1}") for k, g in enumerate(p["script"]["long"]["parts"])]:
        if n == nome:
            return any(s.get("abertura") for s in g["sentences"])
    return False



# ---------- remendo: troca só as frases que mudaram, sem refazer o áudio inteiro ----------
def frases_faladas(p, nome):
    """as frases de uma parte, do jeito que a voz fala (na ordem, sem as vazias)"""
    for k, g in enumerate(p["script"]["long"]["parts"]):
        if f"parte{k + 1}" == nome:
            return [falado(p, s["text"].strip()) for s in g["sentences"] if s.get("text", "").strip()]
    return None


def plano_remendo(p, nome, t_novo, pasta_audio):
    """quais frases mudaram desde o áudio gravado: [(índice, texto antigo, texto novo)], ou None se precisa refazer tudo"""
    import difflib, re
    ft = os.path.join(pasta_audio, f"{nome}.txt")
    if not os.path.exists(ft) or com_abertura(p, nome):
        return None
    velho = open(ft, encoding="utf8").read()
    marca = r"\s*⟨pausa:[\d.]+⟩\s*"
    if re.findall(marca, velho) != re.findall(marca, t_novo):
        return None  # as pausas mudaram: refaz tudo
    velho, t_novo = re.sub(marca, " ", velho), re.sub(marca, " ", t_novo)  # o silêncio da pausa fica onde está no áudio
    novas = frases_faladas(p, nome)
    if not novas or " ".join(novas).split() != t_novo.split():
        return None
    tv, tn = velho.split(), t_novo.split()
    lim = [0]
    for f in novas:
        lim.append(lim[-1] + len(f.split()))
    ops = difflib.SequenceMatcher(None, tv, tn, autojunk=False).get_opcodes()

    def no_velho(j):  # a fronteira j (entre palavras do texto novo) no texto velho
        for tag, i1, i2, j1, j2 in ops:
            if j1 <= j <= j2:
                if tag == "equal":
                    return i1 + (j - j1)
                if j == j1:
                    return i1
                if j == j2:
                    return i2
                return None  # a troca atravessa a fronteira da frase: não dá pra remendar
        return None
    pos = [no_velho(j) for j in lim]
    if any(x is None for x in pos) or pos[-1] != len(tv):
        return None
    velhas = [" ".join(tv[pos[i]:pos[i + 1]]) for i in range(len(novas))]
    mud = [(i, velhas[i], novas[i]) for i in range(len(novas)) if velhas[i].split() != novas[i].split()]
    if not mud or sum(len(x[2]) for x in mud) > 0.7 * len(t_novo):
        return None  # mudou quase tudo: sai melhor refazendo a parte inteira
    return {"velhas": velhas, "novas": novas, "mudou": mud}


def aplicar_remendo(plano, audio, gerar_frase, log=print):
    """corta cada frase que mudou do áudio antigo e cola a nova no lugar (do fim pro começo, pros tempos não andarem)"""
    import subprocess as sp, tempfile, shutil
    from .alinhar import _palavras, _tempos
    dur = float(sp.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio], capture_output=True, text=True).stdout.strip())
    tempos, taxa, _ = _tempos(plano["velhas"], _palavras(audio), dur)
    log(f"    remendo: {taxa:.0%} das palavras achadas no áudio antigo")
    if taxa < 0.8:
        raise RuntimeError(f"alinhamento fraco ({taxa:.0%})")
    N = len(tempos)
    with tempfile.TemporaryDirectory() as tmp:
        atual = os.path.join(tmp, "atual.wav")
        sp.run(["ffmpeg", "-loglevel", "error", "-y", "-i", audio, "-ac", "1", "-ar", "44100", atual], check=True)
        for i, _, nova in sorted(plano["mudou"], reverse=True):
            c0 = (tempos[i - 1][1] + tempos[i][0]) / 2 if i > 0 else max(0.0, tempos[i][0] - 0.05)
            c1 = (tempos[i][1] + tempos[i + 1][0]) / 2 if i < N - 1 else dur
            gl, gr = max(0.05, tempos[i][0] - c0), max(0.05, c1 - tempos[i][1]) if i < N - 1 else 0.3
            bruto = os.path.join(tmp, f"f{i}.mp3"); open(bruto, "wb").write(gerar_frase(nova))
            limpo = os.path.join(tmp, f"f{i}.wav")  # tira o silêncio do começo e do fim da frase nova
            sp.run(["ffmpeg", "-loglevel", "error", "-y", "-i", bruto, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                    "-ac", "1", "-ar", "44100", limpo], check=True)
            saida = os.path.join(tmp, f"r{i}.wav")
            sp.run(["ffmpeg", "-loglevel", "error", "-y", "-i", atual, "-i", limpo, "-filter_complex",
                    f"[0:a]atrim=0:{c0:.3f},asetpts=PTS-STARTPTS[a];[0:a]atrim={c1:.3f},asetpts=PTS-STARTPTS[c];"
                    f"[1:a]adelay={int(gl * 1000)},apad=pad_dur={gr:.3f}[b];[a][b][c]concat=n=3:v=0:a=1", saida], check=True)
            shutil.move(saida, atual)
            log(f"    remendo: frase {i + 1} trocada ({c0:.2f}s a {c1:.2f}s)")
        sp.run(["ffmpeg", "-loglevel", "error", "-y", "-i", atual, "-b:a", "128k", audio], check=True)


def main(nome):
    key = os.environ.get("ELEVENLABS_KEY", "").strip()
    pasta = os.path.join(RAIZ, "projetos", nome)
    p = json.load(open(os.path.join(pasta, "projeto.json"), encoding="utf8"))
    voz = p.get("voz") or {}
    if voz.get("motor") != "eleven":
        return
    if not key:
        aviso("ElevenLabs", "falta o secret ELEVENLABS_KEY no GitHub"); return
    H = {"xi-api-key": key}
    pasta_audio = os.path.join(pasta, "audio"); os.makedirs(pasta_audio, exist_ok=True)
    # o texto de cada áudio fica salvo ao lado (<nome>.txt): se o roteiro mudou, o áudio é gerado de novo
    def mudou(n, t):
        ft = os.path.join(pasta_audio, f"{n}.txt")
        return os.path.exists(ft) and open(ft, encoding="utf8").read() != t
    faltam = [(n, t) for n, t in textos(p) if not achar_audio(pasta_audio, n) or mudou(n, t)]
    if any(mudou(n, t) for n, t in faltam):
        nota("ElevenLabs", "roteiro mudou: regerando " + ", ".join(n for n, t in faltam if mudou(n, t)))
    if not faltam:
        nota("ElevenLabs", "todos os áudios já existem, nada gerado"); return

    # voz: pelo id ou pelo nome
    vid = voz.get("voice_id")
    if not vid:
        alvo = (voz.get("eleven_voz") or "Vinícius Torales").lower()
        r = requests.get(f"{API}/v1/voices", headers=H, timeout=60); r.raise_for_status()
        vs = r.json().get("voices", [])
        achou = [v for v in vs if v["name"].lower().startswith(alvo)] or [v for v in vs if alvo in v["name"].lower()]
        if not achou:
            aviso("ElevenLabs", f"não achei a voz '{alvo}'. Vozes na conta: " + ", ".join(v["name"] for v in vs)[:800]); sys.exit(2)
        vid = achou[0]["voice_id"]
        nota("ElevenLabs voz", f"{achou[0]['name']} ({vid})")

    # modelo: o pedido no projeto, senão o mais novo que fala o idioma do vídeo
    r = requests.get(f"{API}/v1/models", headers=H, timeout=60); r.raise_for_status()
    modelos = [m for m in r.json() if m.get("can_do_text_to_speech")]
    lingua = idioma_de(p)
    def fala_pt(m):
        return any((l.get("language_id") or "").startswith(lingua) for l in m.get("languages") or [])
    mid = voz.get("modelo")
    if not mid:
        pref = [m for m in modelos if m["model_id"] == "eleven_v4_turbo"] or [m for m in modelos if fala_pt(m) and "v4" in m["model_id"]] or [m for m in modelos if m["model_id"] == "eleven_multilingual_v2"] or [m for m in modelos if fala_pt(m)]
        mid = pref[0]["model_id"]
    mod = next((m for m in modelos if m["model_id"] == mid), {})
    mult = float(((mod.get("model_rates") or {}).get("character_cost_multiplier")) or 1.0)
    nota("ElevenLabs modelos", " · ".join(f"{m['model_id']} x{(m.get('model_rates') or {}).get('character_cost_multiplier', '?')}" for m in modelos)[:900])

    # partes em que só algumas frases mudaram: troca só essas frases (gasta muito menos crédito)
    remendos = {}
    for n, t in faltam:
        if mudou(n, t) and achar_audio(pasta_audio, n):
            pl = plano_remendo(p, n, t, pasta_audio)
            if pl:
                remendos[n] = pl
                nota("ElevenLabs remendo", f"{n}: só {len(pl['mudou'])} frase(s) mudaram: " + " | ".join(x[2] for x in pl["mudou"])[:600])

    # saldo antes de gastar
    chars = sum(len(t) for n, t in faltam if n not in remendos) + sum(len(x[2]) for pl in remendos.values() for x in pl["mudou"]); custo = int(chars * mult)
    r = requests.get(f"{API}/v1/user/subscription", headers=H, timeout=60)
    if r.ok:
        s = r.json(); resta = s.get("character_limit", 0) - s.get("character_count", 0)
        nota("ElevenLabs saldo", f"vai usar ~{custo} de {resta} créditos restantes (modelo {mid}, {chars} caracteres)")
        if custo > resta:
            aviso("ElevenLabs", f"créditos insuficientes: precisa de ~{custo}, restam {resta}. Nada foi gerado."); sys.exit(2)

    def gerar_frase(txt):
        r = requests.post(f"{API}/v1/text-to-speech/{vid}?output_format=mp3_44100_128", headers=H, timeout=600,
                          json={"text": txt, "model_id": mid, **({"voice_settings": voz["ajustes"]} if voz.get("ajustes") else {})})
        if r.status_code != 200:
            raise RuntimeError(f"erro {r.status_code} {r.text[:300]}")
        return r.content

    feitos = []
    for n, t in faltam:
        if n in remendos:
            try:
                aplicar_remendo(remendos[n], achar_audio(pasta_audio, n), gerar_frase)
                open(os.path.join(pasta_audio, f"{n}.txt"), "w", encoding="utf8").write(t)
                feitos.append(n + " (remendo)"); print(f"  {n}.mp3 remendado", flush=True)
                continue
            except Exception as e:
                aviso("ElevenLabs remendo", f"{n}: não deu pra remendar ({str(e)[:200]}); refazendo a parte inteira")
        import re as _re, subprocess as _sp, tempfile as _tf
        pedacos = _re.split(r"\s*⟨pausa:([\d.]+)⟩\s*", t)  # [texto, pausa, texto, pausa, ..., texto]
        destino = os.path.join(pasta_audio, f"{n}.mp3")
        with _tf.TemporaryDirectory() as tmp:
            lista = []
            for k in range(0, len(pedacos), 2):
                txt_k = pedacos[k].strip()
                if txt_k:
                    r = requests.post(f"{API}/v1/text-to-speech/{vid}?output_format=mp3_44100_128", headers=H, timeout=600,
                                      json={"text": txt_k, "model_id": mid, **({"voice_settings": voz["ajustes"]} if voz.get("ajustes") else {})})
                    if r.status_code != 200:
                        aviso("ElevenLabs", f"{n}: erro {r.status_code} {r.text[:300]}"); sys.exit(2)
                    a = os.path.join(tmp, f"p{k}.mp3"); open(a, "wb").write(r.content); lista.append(a)
                if k + 1 < len(pedacos):
                    sil = os.path.join(tmp, f"s{k}.mp3")
                    _sp.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-t", pedacos[k + 1], "-i", "anullsrc=r=44100:cl=mono", "-b:a", "128k", sil], check=True); lista.append(sil)
            if len(lista) == 1:
                import shutil as _sh; _sh.copy(lista[0], destino)
            else:
                ent = sum([["-i", a] for a in lista], [])
                filt = "".join(f"[{i}:a]aresample=44100,aformat=channel_layouts=mono[a{i}];" for i in range(len(lista))) + "".join(f"[a{i}]" for i in range(len(lista))) + f"concat=n={len(lista)}:v=0:a=1"
                _sp.run(["ffmpeg", "-loglevel", "error", "-y", *ent, "-filter_complex", filt, "-b:a", "128k", destino], check=True)
        intro = intro_de(p)
        if com_abertura(p, n) and os.path.exists(intro):  # abertura do canal + 0,3 s de pausa + narração
            import subprocess, shutil
            tmp = destino + ".tmp.mp3"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", intro, "-f", "lavfi", "-t", "0.3", "-i", "anullsrc=r=44100:cl=mono", "-i", destino,
                            "-filter_complex", "[0:a]aresample=44100,aformat=channel_layouts=mono[a0];[2:a]aresample=44100,aformat=channel_layouts=mono[a2];[a0][1:a][a2]concat=n=3:v=0:a=1",
                            "-b:a", "128k", tmp], check=True)
            shutil.move(tmp, destino)
        open(os.path.join(pasta_audio, f"{n}.txt"), "w", encoding="utf8").write(t)
        feitos.append(n); print(f"  {n}.mp3 ({len(t)} caracteres)", flush=True)
    nota("ElevenLabs", f"gerados: {', '.join(feitos)}")


if __name__ == "__main__":
    main(sys.argv[1])

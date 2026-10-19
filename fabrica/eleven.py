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
                    (r"\bKolynos\b", "Colínos"), (r"\bNestlé\b", "Néslê"), (r"\b(CADE|Cade)\b", "Cádi"), (r"\bChokito\b", "Chokíto")]}


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
    return [(n, falado(p, " ".join(s["text"].strip() for s in g["sentences"] if s.get("text", "").strip() and not (pula and s.get("abertura"))))) for n, g in out]


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
    faltam = [(n, t) for n, t in textos(p) if not achar_audio(pasta_audio, n)]
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

    # saldo antes de gastar
    chars = sum(len(t) for _, t in faltam); custo = int(chars * mult)
    r = requests.get(f"{API}/v1/user/subscription", headers=H, timeout=60)
    if r.ok:
        s = r.json(); resta = s.get("character_limit", 0) - s.get("character_count", 0)
        nota("ElevenLabs saldo", f"vai usar ~{custo} de {resta} créditos restantes (modelo {mid}, {chars} caracteres)")
        if custo > resta:
            aviso("ElevenLabs", f"créditos insuficientes: precisa de ~{custo}, restam {resta}. Nada foi gerado."); sys.exit(2)

    feitos = []
    for n, t in faltam:
        r = requests.post(f"{API}/v1/text-to-speech/{vid}?output_format=mp3_44100_128", headers=H, timeout=600,
                          json={"text": t, "model_id": mid, **({"voice_settings": voz["ajustes"]} if voz.get("ajustes") else {})})
        if r.status_code != 200:
            aviso("ElevenLabs", f"{n}: erro {r.status_code} {r.text[:300]}"); sys.exit(2)
        destino = os.path.join(pasta_audio, f"{n}.mp3")
        with open(destino, "wb") as f:
            f.write(r.content)
        intro = intro_de(p)
        if com_abertura(p, n) and os.path.exists(intro):  # abertura do canal + 0,3 s de pausa + narração
            import subprocess, shutil
            tmp = destino + ".tmp.mp3"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", intro, "-f", "lavfi", "-t", "0.3", "-i", "anullsrc=r=44100:cl=mono", "-i", destino,
                            "-filter_complex", "[0:a]aresample=44100,aformat=channel_layouts=mono[a0];[2:a]aresample=44100,aformat=channel_layouts=mono[a2];[a0][1:a][a2]concat=n=3:v=0:a=1",
                            "-b:a", "128k", tmp], check=True)
            shutil.move(tmp, destino)
        feitos.append(n); print(f"  {n}.mp3 ({len(t)} caracteres)", flush=True)
    nota("ElevenLabs", f"gerados: {', '.join(feitos)}")


if __name__ == "__main__":
    main(sys.argv[1])

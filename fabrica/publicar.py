"""Publicação automática no YouTube.

  python -m fabrica.publicar enfileirar saida   → põe os vídeos gerados na fila (release "fila" do GitHub)
  python -m fabrica.publicar enviar             → sobe o que estiver na fila e agenda

Agenda: longo às 12h (Brasília), um Short por dia às 18h, sempre depois do último já agendado.
Os vídeos sobem privados com data de publicação. A cota grátis da API dá uns 5 vídeos por dia;
o que não couber fica na fila e sobe na execução diária seguinte (workflow "Publicar").

Secrets: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (Custo Oculto) e YT_REFRESH_TOKEN_EN (Hidden Cost).
Cada vídeo vai para o canal do idioma do projeto ("idioma" no projeto.json); cada canal tem a própria agenda.
"""
import datetime as dt, glob, json, os, shutil, subprocess, sys, tempfile, time
import requests

from .canais import CANAIS, canal

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(RAIZ, "publicados.json")
TAG = "fila"
BRT = dt.timezone(dt.timedelta(hours=-3))
HORA = {"longo": 12, "short": 18, "serie": 8}


class Cota(Exception):
    pass


def gh(*args, check=True):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check).stdout


def nota(titulo, msg, nivel="notice"):
    print(f"::{nivel} title={titulo}::{msg}"[:1000], flush=True)


# ---------- fila ----------
def enfileirar(pasta_saida):
    if subprocess.run(["gh", "release", "view", TAG], capture_output=True).returncode != 0:
        gh("release", "create", TAG, "--title", "Fila de publicação", "--notes", "Vídeos esperando envio ao YouTube. Gerenciado pela fábrica.", "--prerelease")
    agora = time.time(); n = 0; ja = {r["nome"] for r in registro()}; pulados = []
    for mf in sorted(glob.glob(os.path.join(pasta_saida, "**", "youtube_*.json"), recursive=True)):
        d = os.path.dirname(mf); meta = json.load(open(mf, encoding="utf8"))
        nome = os.path.basename(mf)[len("youtube_"):-5]
        if not meta.get("video"):
            continue
        if nome in ja:  # já foi para o YouTube: regerar não duplica
            pulados.append(nome); continue
        meta["enfileirado"] = agora; meta["ordem"] = 0 if meta["tipo"] == "longo" else int("".join(c for c in nome.split("_")[-1] if c.isdigit()) or 1)
        with tempfile.TemporaryDirectory() as t:
            arqs = []
            def cp(src, suf):
                if src and os.path.exists(os.path.join(d, src)):
                    dst = os.path.join(t, f"{nome}__{suf}"); shutil.copy(os.path.join(d, src), dst); arqs.append(dst)
            cp(meta.get("video"), "video.mp4"); cp(meta.get("miniatura"), "miniatura.jpg"); cp(meta.get("legenda"), "legenda.srt")
            mj = os.path.join(t, f"{nome}__meta.json"); json.dump(meta, open(mj, "w", encoding="utf8"), ensure_ascii=False); arqs.append(mj)
            gh("release", "upload", TAG, *arqs, "--clobber"); n += 1
    nota("Fila de publicação", f"{n} vídeo(s) na fila do YouTube" + (f" · já publicados, não reenviados: {', '.join(pulados)}" if pulados else ""))


def fila():
    if subprocess.run(["gh", "release", "view", TAG], capture_output=True).returncode != 0:
        return {}
    itens = {}
    for a in json.loads(gh("release", "view", TAG, "--json", "assets"))["assets"]:
        if "__" in a["name"]:
            nome, suf = a["name"].split("__", 1); itens.setdefault(nome, []).append(a["name"])
    return itens


# ---------- agenda ----------
def registro():
    try:
        return json.load(open(REG, encoding="utf8"))
    except Exception:
        return []


def proximo_horario(tipo, reg, caso=None, idioma="pt"):
    reg = [r for r in reg if idioma_de(r) == idioma]  # cada canal tem a própria agenda
    agora = dt.datetime.now(BRT)
    dia = agora.date()
    if agora.hour >= HORA[tipo] - 2:  # precisa de folga para o YouTube processar
        dia += dt.timedelta(days=1)
    ultimos = [dt.datetime.fromisoformat(r["publishAt"]).astimezone(BRT).date() for r in reg if r["tipo"] == tipo]
    if tipo == "longo":
        if ultimos and max(ultimos) >= dia:
            dia = max(ultimos) + dt.timedelta(days=1)
    longos = [dt.datetime.fromisoformat(r["publishAt"]).astimezone(BRT).date() for r in reg
              if r["tipo"] == "longo" and r.get("publishAt") and (not caso or r["nome"].startswith(caso + "_"))]
    if tipo == "longo" and ultimos:  # um longo por semana
        dia = max(dia, max(ultimos) + dt.timedelta(days=7))
    if tipo != "longo" and longos:  # Short nunca sai antes do longo que ele anuncia
        dia = max(dia, max(longos))
        if dia == max(longos) and HORA[tipo] <= HORA["longo"]:
            dia += dt.timedelta(days=1)
    if tipo != "longo":  # preenche o primeiro dia livre (um de cada tipo por dia)
        ocupados = set(ultimos)
        while dia in ocupados:
            dia += dt.timedelta(days=1)
    return dt.datetime(dia.year, dia.month, dia.day, HORA[tipo], tzinfo=BRT)


# ---------- YouTube ----------
def idioma_de(x):
    return ((x or {}).get("idioma") or "pt").lower()[:2]


def tem_canal(idioma="pt"):
    return bool(os.environ.get(canal(idioma)["token_env"], "").strip())


def idiomas_ativos():
    return [i for i in CANAIS if tem_canal(i)]


_TOKENS = {}


def token(idioma="pt"):
    if idioma in _TOKENS:
        return _TOKENS[idioma]
    env = canal(idioma)["token_env"]
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ[env], "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"Não consegui entrar no YouTube ({r.status_code}): {r.text[:300]}. Confira os secrets YT_CLIENT_ID, YT_CLIENT_SECRET e {env}.")
    _TOKENS[idioma] = r.json()["access_token"]
    return _TOKENS[idioma]


def checar(r, oque):
    if r.status_code in (200, 201):
        return r
    txt = r.text[:600]
    if r.status_code == 403 and any(k in txt for k in ("quotaExceeded", "uploadLimitExceeded", "dailyLimitExceeded")):
        raise Cota(txt)
    raise RuntimeError(f"{oque}: erro {r.status_code}: {txt}")


def voz_sintetica(caso):
    """True se o caso foi narrado por voz de IA que NÃO é a voz clonada do Vinícius (aí o YouTube pede o aviso)."""
    for pasta in (caso or "", (caso or "").replace("_", "-")):
        f = os.path.join(RAIZ, "projetos", pasta, "projeto.json")
        if pasta and os.path.exists(f):
            voz = json.load(open(f, encoding="utf8")).get("voz") or {}
            return not str(voz.get("eleven_voz", "")).startswith("Vinícius")
    return True


_TITULOS = {}


def ja_no_canal(idioma, titulo):
    """Trava contra vídeo duplicado: confere os últimos uploads do canal (quando o publicados.json não foi salvo)."""
    if idioma not in _TITULOS:
        H = {"Authorization": f"Bearer {token(idioma)}"}; Y = "https://www.googleapis.com/youtube/v3"
        try:
            up = checar(requests.get(f"{Y}/channels?part=contentDetails&mine=true", headers=H, timeout=30), "canal").json()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            j = checar(requests.get(f"{Y}/playlistItems?part=snippet&maxResults=50&playlistId={up}", headers=H, timeout=30), "uploads").json()
            _TITULOS[idioma] = {it["snippet"]["title"]: it["snippet"]["resourceId"]["videoId"] for it in j.get("items", [])}
        except Exception as e:
            nota("Checagem de duplicado falhou", str(e)[:200], "warning"); _TITULOS[idioma] = {}
    return _TITULOS[idioma].get(titulo)


def subir_video(tk, path, meta, quando):
    corpo = {"snippet": {"title": meta["titulo"], "description": meta["descricao"], "tags": meta.get("tags", [])[:30],
                         "categoryId": "27", "defaultLanguage": canal(idioma_de(meta))["yt_lang"], "defaultAudioLanguage": canal(idioma_de(meta))["yt_lang"]},
             "status": {"privacyStatus": "private", "publishAt": quando.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "selfDeclaredMadeForKids": False, "containsSyntheticMedia": voz_sintetica(meta.get("caso"))}}
    tam = os.path.getsize(path)
    r = checar(requests.post("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                             headers={"Authorization": f"Bearer {tk}", "Content-Type": "application/json; charset=UTF-8",
                                      "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)},
                             data=json.dumps(corpo), timeout=60), "iniciar envio")
    url = r.headers["Location"]
    with open(path, "rb") as f:
        r = checar(requests.put(url, headers={"Authorization": f"Bearer {tk}", "Content-Type": "video/mp4", "Content-Length": str(tam)},
                                data=f, timeout=3600), "enviar vídeo")
    return r.json()


def subir_miniatura(tk, vid, path):
    with open(path, "rb") as f:
        checar(requests.post(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                             headers={"Authorization": f"Bearer {tk}", "Content-Type": "image/jpeg"}, data=f.read(), timeout=120), "miniatura")


def subir_legenda(tk, vid, path, idioma="pt"):
    c = canal(idioma)
    snip = json.dumps({"snippet": {"videoId": vid, "language": c["yt_lang"], "name": c["legenda_nome"], "isDraft": False}})
    srt = open(path, "rb").read(); b = "fronteira_custo_oculto"
    corpo = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{snip}\r\n--{b}\r\nContent-Type: application/x-subrip\r\n\r\n").encode() + srt + f"\r\n--{b}--".encode()
    checar(requests.post("https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
                         headers={"Authorization": f"Bearer {tk}", "Content-Type": f"multipart/related; boundary={b}"}, data=corpo, timeout=120), "legenda")


def enviar():
    itens = fila()
    if not itens:
        nota("Publicar", "fila vazia"); return
    with tempfile.TemporaryDirectory() as t:
        metas = {}
        for nome in itens:
            gh("release", "download", TAG, "-p", f"{nome}__meta.json", "-D", t, "--clobber")
            metas[nome] = json.load(open(os.path.join(t, f"{nome}__meta.json"), encoding="utf8"))
        ordem = sorted(metas, key=lambda n: (metas[n]["enfileirado"], metas[n]["ordem"]))
        reg = registro(); feitos = []; sem_canal = set()
        try:
            for nome in ordem:
                meta = metas[nome]; idi = idioma_de(meta)
                if f"{nome}__video.mp4" not in itens[nome]:
                    continue
                if not tem_canal(idi):  # canal ainda não autorizado: o vídeo espera na fila
                    sem_canal.add(canal(idi)["token_env"]); continue
                tk = token(idi)
                dup = ja_no_canal(idi, meta["titulo"])
                if dup:  # já está no canal: só registra e tira da fila
                    reg.append({"nome": nome, "tipo": meta["tipo"], "idioma": idi, "titulo": meta["titulo"], "video_id": dup, "caso": meta.get("caso"),
                                "caso_titulo": meta.get("caso_titulo"), "publishAt": proximo_horario(meta["tipo"], reg, meta.get("caso"), idi).isoformat(), "status": "private"})
                    feitos.append(f"{meta['titulo']} já estava no canal (youtu.be/{dup}), não subi de novo")
                    for a in itens[nome]:
                        gh("release", "delete-asset", TAG, a, "-y", check=False)
                    json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
                    continue
                gh("release", "download", TAG, "-p", f"{nome}__*", "-D", t, "--clobber")
                quando = proximo_horario(meta["tipo"], reg, meta.get("caso"), idi)
                lg = next((x for x in reg if meta.get("caso") and x["nome"] == f"{meta['caso']}_longo" and x.get("video_id")), None)
                if lg and meta["tipo"] != "longo" and "youtu.be/" not in meta["descricao"]:
                    meta["descricao"] = f"{canal(idi)['caso_completo']} https://youtu.be/{lg['video_id']}\n\n" + meta["descricao"]
                v = subir_video(tk, os.path.join(t, f"{nome}__video.mp4"), meta, quando)
                vid = v["id"]; extra = []
                for suf, fn in (("miniatura.jpg", subir_miniatura), ("legenda.srt", lambda tk, vid, path: subir_legenda(tk, vid, path, idi))):
                    if f"{nome}__{suf}" in itens[nome]:
                        try:
                            fn(tk, vid, os.path.join(t, f"{nome}__{suf}"))
                        except Cota:
                            raise
                        except Exception as e:
                            extra.append(f"{suf.split('.')[0]} falhou: {str(e)[:150]}")
                reg.append({"nome": nome, "tipo": meta["tipo"], "idioma": idi, "titulo": meta["titulo"], "video_id": vid, "caso": meta.get("caso"), "caso_titulo": meta.get("caso_titulo"),
                            "publishAt": quando.isoformat(), "status": v.get("status", {}).get("privacyStatus")})
                feitos.append(f"{meta['titulo']} → {quando:%d/%m %Hh} (youtu.be/{vid})" + (f" [{'; '.join(extra)}]" if extra else ""))
                for a in itens[nome]:
                    gh("release", "delete-asset", TAG, a, "-y", check=False)
                json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        except Cota:
            nota("Cota do dia acabou", "o resto da fila sobe na próxima execução diária", "warning")
        if sem_canal:
            nota("Canal sem autorização", f"vídeos esperando na fila: falta o secret {', '.join(sorted(sem_canal))}", "warning")
        if feitos:
            nota("Agendados no YouTube", " | ".join(feitos))
        restam = len(fila())
        if restam:
            nota("Ainda na fila", f"{restam} vídeo(s)")


def miniaturas(pasta_saida):
    """Põe a capa em vídeos que já estão no YouTube (ex.: Shorts agendados antes de existir a capa)."""
    reg = registro(); por_nome = {r["nome"]: r for r in reg if r.get("video_id")}; tk = None; feitos = []
    for mf in glob.glob(os.path.join(pasta_saida, "**", "youtube_*.json"), recursive=True):
        nome = os.path.basename(mf)[len("youtube_"):-5]; meta = json.load(open(mf, encoding="utf8"))
        r = por_nome.get(nome); arq = meta.get("miniatura") and os.path.join(os.path.dirname(mf), meta["miniatura"])
        import hashlib
        h = hashlib.sha1(open(arq, "rb").read()).hexdigest()[:12] if arq and os.path.exists(arq) else None
        if not r or not h or r.get("miniatura_ok") == h:
            continue
        if not tem_canal(idioma_de(r)):
            continue
        try:
            subir_miniatura(token(idioma_de(r)), r["video_id"], arq); r["miniatura_ok"] = h; feitos.append(nome)
        except Exception as e:
            nota("Miniatura falhou", f"{nome}: {str(e)[:300]}", "warning")
    if feitos:
        json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        nota("Miniaturas aplicadas", ", ".join(feitos))


TODOS = "Todos os casos | Custo Oculto"
COM = os.path.join(RAIZ, "comentarios.json")


def comentar():
    """Posta pelo canal os comentários aprovados (comentarios.json) quando o vídeo já está público. Fixar é manual no Studio."""
    try:
        fila_c = json.load(open(COM, encoding="utf8"))
    except Exception:
        return
    reg = {r["nome"]: r for r in registro()}; tk = None; feitos = []
    # Shorts e partes da série (canal em português) ganham o link do caso completo — texto aprovado pelo Vinícius em 15/10/2026
    longos = {r.get("caso"): r for r in reg.values() if r.get("tipo") == "longo" and r.get("video_id")}
    ja = {c.get("nome") for c in fila_c}
    for r in reg.values():
        lg = longos.get(r.get("caso"))
        if r.get("tipo") in ("short", "serie") and r.get("video_id") and lg and idioma_de(r) == "pt" and r["nome"] not in ja:
            fila_c.append({"nome": r["nome"], "texto": f"📌 O caso completo está aqui: https://youtu.be/{lg['video_id']}", "depois_de": lg["nome"]})
    for c in fila_c:
        if c.get("feito"):
            continue
        vid = c.get("video_id") or (reg.get(c.get("nome")) or {}).get("video_id")
        if not vid:
            continue
        idi = c.get("idioma") or idioma_de(reg.get(c.get("nome")))
        if not tem_canal(idi):
            continue
        H = {"Authorization": f"Bearer {token(idi)}"}
        v = requests.get("https://www.googleapis.com/youtube/v3/videos", headers=H, params={"part": "status", "id": vid}, timeout=30).json().get("items") or []
        if not v or v[0]["status"]["privacyStatus"] != "public":
            continue
        if c.get("depois_de"):  # o link só vai quando o longo também já está no ar
            lv = (reg.get(c["depois_de"]) or {}).get("video_id")
            lj = requests.get("https://www.googleapis.com/youtube/v3/videos", headers=H, params={"part": "status", "id": lv}, timeout=30).json().get("items") or []
            if not lj or lj[0]["status"]["privacyStatus"] != "public":
                continue
        q = requests.post("https://www.googleapis.com/youtube/v3/commentThreads?part=snippet", headers=H, timeout=30,
                          json={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": c["texto"]}}}})
        if q.status_code in (200, 201):
            c["feito"] = q.json()["id"]; feitos.append(c.get("nome") or vid)
        else:
            nota("Comentário falhou", f"{c.get('nome')}: {q.status_code} " + " ".join(q.text.split())[:300], "warning")
    json.dump(fila_c, open(COM, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    if feitos:
        nota("Comentários postados (fixe no Studio)", ", ".join(feitos))


def playlists():
    """Playlists que tocam em sequência, em cada canal: uma com todos os longos e uma por caso (longo + série)."""
    reg = registro()
    for idi in idiomas_ativos():
        _playlists(reg, idi)


def _playlists(reg_todo, idi):
    reg = [r for r in reg_todo if idioma_de(r) == idi]; C = canal(idi)
    tk = token(idi); H = {"Authorization": f"Bearer {tk}"}; Y = "https://www.googleapis.com/youtube/v3"
    titulos = {}
    for r in reg:  # nome do caso vem do longo
        if r.get("tipo") == "longo" and r.get("caso_titulo"):
            titulos[r["caso"]] = r["caso_titulo"]
    ex = {}; tok = None
    while True:
        q = requests.get(f"{Y}/playlists?part=snippet&mine=true&maxResults=50" + (f"&pageToken={tok}" if tok else ""), headers=H, timeout=30)
        checar(q, "listar playlists"); j = q.json()
        for it in j.get("items", []):
            ex[it["snippet"]["title"]] = it["id"]
        tok = j.get("nextPageToken")
        if not tok:
            break
    def pl(titulo, desc):
        if titulo not in ex:
            q = checar(requests.post(f"{Y}/playlists?part=snippet,status", headers=H, timeout=30,
                                     json={"snippet": {"title": titulo, "description": desc, "defaultLanguage": C["yt_lang"]}, "status": {"privacyStatus": "public"}}), "criar playlist")
            ex[titulo] = q.json()["id"]
        return ex[titulo]
    feitos = []
    try:
        for r in reg:
            if not r.get("video_id"):
                continue
            alvos = []
            if r.get("tipo") == "longo":
                alvos.append(C["pl_todos"])
            if r.get("caso") in titulos and r.get("tipo") in ("longo", "serie"):
                alvos.append((C["pl_caso"][0].format(t=titulos[r["caso"]]), C["pl_caso"][1].format(t=titulos[r["caso"]])))
            for t, d in alvos:
                if t in (r.get("playlists") or []):
                    continue
                pid = pl(t, d)
                q = requests.post(f"{Y}/playlistItems?part=snippet", headers=H, timeout=30,
                                  json={"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": r["video_id"]}}})
                if q.status_code == 403 and "quota" in q.text.lower():
                    raise Cota(q.text)
                if q.status_code not in (200, 201):
                    nota("Playlist falhou", f"{r['nome']} → {t}: {q.status_code} " + " ".join(q.text.split())[:300], "warning"); continue
                r.setdefault("playlists", []).append(t); feitos.append(f"{r['nome']} → {t}")
    except Cota:
        nota("Cota do dia acabou", "playlists continuam na próxima execução", "warning")
    except Exception as e:
        nota("Playlist falhou", str(e)[:400], "warning")
    if feitos:
        json.dump(reg_todo, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        nota(f"Playlists {C['nome']}", f"{len(feitos)} adicionados: " + "; ".join(feitos)[:800])


def conferir():
    for idi in idiomas_ativos():
        _conferir(idi)


def _conferir(idi):
    tk = token(idi)
    r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true", headers={"Authorization": f"Bearer {tk}"}, timeout=30)
    if r.status_code != 200:
        nota("YouTube: falhou", f"{r.status_code}: {r.text[:500]}", "error"); raise SystemExit(1)
    it = r.json().get("items") or []
    if not it:
        nota("YouTube: nenhum canal", f"a conta autorizada não tem canal. Autorize com o canal {canal(idi)['nome']}.", "error"); raise SystemExit(1)
    c = it[0]
    nota("YouTube conectado", f"canal: {c['snippet']['title']} · inscritos: {c['statistics'].get('subscriberCount')} · vídeos: {c['statistics'].get('videoCount')}")


def reconstruir():
    """Recupera entradas do publicados.json a partir do YouTube (quando o commit do registro falhou). Usa reparo.json: título → dados."""
    mapa = json.load(open(os.path.join(RAIZ, "reparo.json"), encoding="utf8"))
    reg = registro(); ja = {r.get("video_id") for r in reg} | {r["nome"] for r in reg}
    tk = token(); H = {"Authorization": f"Bearer {tk}"}; Y = "https://www.googleapis.com/youtube/v3"
    up = checar(requests.get(f"{Y}/channels?part=contentDetails&mine=true", headers=H, timeout=30), "canal").json()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = []; tok = None
    for _ in range(4):
        j = checar(requests.get(f"{Y}/playlistItems?part=contentDetails&maxResults=50&playlistId={up}" + (f"&pageToken={tok}" if tok else ""), headers=H, timeout=30), "uploads").json()
        ids += [it["contentDetails"]["videoId"] for it in j.get("items", [])]; tok = j.get("nextPageToken")
        if not tok:
            break
    novos = []
    for k in range(0, len(ids), 50):
        j = checar(requests.get(f"{Y}/videos?part=snippet,status&id={','.join(ids[k:k + 50])}", headers=H, timeout=30), "vídeos").json()
        for v in j.get("items", []):
            d = mapa.get(v["snippet"]["title"]); st = v["status"]
            if not d or v["id"] in ja or d["nome"] in ja or not st.get("publishAt"):
                continue
            quando = dt.datetime.fromisoformat(st["publishAt"].replace("Z", "+00:00")).astimezone(BRT).isoformat()
            reg.append(dict(d, titulo=v["snippet"]["title"], video_id=v["id"], publishAt=quando, status=st["privacyStatus"], miniatura_ok=True))
            novos.append(f"{d['nome']} → {quando[:16]} ({v['id']})"); ja.add(d["nome"])
    json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    nota("Registro reconstruído", f"{len(novos)} recuperados: " + "; ".join(novos))


def ia(marcar=None):
    """Lista o aviso de 'conteúdo alterado ou sintético' de todos os vídeos do canal; com ids, marca esses como sintéticos."""
    tk = token(); H = {"Authorization": f"Bearer {tk}"}; Y = "https://www.googleapis.com/youtube/v3"
    up = checar(requests.get(f"{Y}/channels?part=contentDetails&mine=true", headers=H, timeout=30), "canal").json()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = []; tok = None
    for _ in range(6):
        j = checar(requests.get(f"{Y}/playlistItems?part=contentDetails&maxResults=50&playlistId={up}" + (f"&pageToken={tok}" if tok else ""), headers=H, timeout=30), "uploads").json()
        ids += [it["contentDetails"]["videoId"] for it in j.get("items", [])]; tok = j.get("nextPageToken")
        if not tok:
            break
    linhas = []; feitos = []
    for k in range(0, len(ids), 50):
        j = checar(requests.get(f"{Y}/videos?part=snippet,status&id={','.join(ids[k:k + 50])}", headers=H, timeout=30), "vídeos").json()
        for v in j.get("items", []):
            st = v["status"]; sint = st.get("containsSyntheticMedia")
            alvo = (v["id"] not in marcar["exceto"]) if isinstance(marcar, dict) else (marcar and v["id"] in marcar)
            if alvo and not sint:
                st2 = {kk: st[kk] for kk in ("privacyStatus", "publishAt", "license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids") if kk in st}
                st2["containsSyntheticMedia"] = True
                checar(requests.put(f"{Y}/videos?part=status", headers=H, timeout=30, json={"id": v["id"], "status": st2}), "marcar IA")
                feitos.append(v["id"]); sint = True
            linhas.append(f"{v['id']} {'IA' if sint else 'sem aviso'} · {v['snippet']['title'][:50]}")
    for i in range(0, len(linhas), 12):
        nota(f"Aviso de IA ({i // 12 + 1})", " | ".join(linhas[i:i + 12]))
    if feitos:
        nota("Marcados como IA", ", ".join(feitos))


def liberar(nomes):
    """Publica agora (público) vídeos que já subiram agendados. nomes: 'caso_longo,caso_short1'."""
    reg = registro(); feitos = []
    for nome in [n.strip() for n in nomes.split(",") if n.strip()]:
        r = next((x for x in reg if x["nome"] == nome and x.get("video_id")), None)
        if not r:
            nota("Liberar", f"{nome}: não está no publicados.json (ainda não subiu?)", "warning"); continue
        H = {"Authorization": f"Bearer {token(idioma_de(r))}"}; Y = "https://www.googleapis.com/youtube/v3"
        v = checar(requests.get(f"{Y}/videos", headers=H, params={"part": "status", "id": r["video_id"]}, timeout=30), "status").json()["items"][0]["status"]
        st = {k: v[k] for k in ("license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia") if k in v}
        st["privacyStatus"] = "public"
        checar(requests.put(f"{Y}/videos?part=status", headers=H, timeout=30, json={"id": r["video_id"], "status": st}), "liberar")
        r["publishAt"] = dt.datetime.now(BRT).isoformat(); r["status"] = "public"; feitos.append(f"{nome} (youtu.be/{r['video_id']})")
    if feitos:
        json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        nota("Publicado agora", " | ".join(feitos))


def ajustar(arq="ajustes.json"):
    """Troca título e/ou data de vídeos já agendados (ajustes.json: {nome: {"titulo"?, "publishAt"?}}) e atualiza o registro."""
    aj = json.load(open(os.path.join(RAIZ, arq), encoding="utf8")); reg = registro(); por = {r["nome"]: r for r in reg}; feitos = []
    for nome, a in aj.items():
        r = por.get(nome) or ({"nome": nome, "video_id": a["video_id"], "idioma": a.get("idioma", "pt")} if a.get("video_id") else None)
        if not r or not r.get("video_id"):
            nota("Ajuste ignorado", f"{nome}: não está no registro", "warning"); continue
        H = {"Authorization": f"Bearer {token(idioma_de(r))}"}; Y = "https://www.googleapis.com/youtube/v3"
        v = checar(requests.get(f"{Y}/videos?part=snippet,status&id={r['video_id']}", headers=H, timeout=30), "ler vídeo").json().get("items") or []
        if not v:
            nota("Ajuste ignorado", f"{nome}: vídeo não encontrado", "warning"); continue
        v = v[0]; parts = []; corpo = {"id": r["video_id"]}
        if a.get("titulo"):
            sn = {k: v["snippet"][k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage") if k in v["snippet"]}
            sn["title"] = a["titulo"][:100]; corpo["snippet"] = sn; parts.append("snippet")
        if a.get("publishAt"):
            if v["status"]["privacyStatus"] != "private":
                nota("Data não trocada", f"{nome}: já está público", "warning")
            else:
                st = {k: v["status"][k] for k in ("privacyStatus", "license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia") if k in v["status"]}
                st["publishAt"] = dt.datetime.fromisoformat(a["publishAt"]).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                corpo["status"] = st; parts.append("status")
        if not parts:
            continue
        checar(requests.put(f"{Y}/videos?part={','.join(parts)}", headers=H, timeout=30, json=corpo), f"ajustar {nome}")
        if "snippet" in parts:
            r["titulo"] = a["titulo"][:100]
        if "status" in parts:
            r["publishAt"] = a["publishAt"]
        feitos.append(f"{nome}: " + " / ".join(x for x in (a.get("titulo"), a.get("publishAt", "")[:16]) if x))
    json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    nota("Ajustes aplicados", " | ".join(feitos) or "nada")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "enviar"
    if cmd == "miniaturas":
        miniaturas(sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "saida"))
    elif cmd == "conferir":
        conferir()
    elif cmd == "comentar":
        comentar()
    elif cmd == "ia":
        arg = sys.argv[2] if len(sys.argv) > 2 else ""
        ia({"exceto": set(arg[len("todos-exceto:"):].split(","))} if arg.startswith("todos-exceto:") else (set(arg.split(",")) if arg else None))
    elif cmd == "ajustar":
        ajustar(sys.argv[2] if len(sys.argv) > 2 else "ajustes.json")
    elif cmd == "reconstruir":
        reconstruir()
    elif cmd == "playlists":
        playlists()
    elif cmd == "liberar":
        liberar(sys.argv[2] if len(sys.argv) > 2 else "")
    elif cmd == "enfileirar":
        enfileirar(sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "saida"))
    else:
        enviar()

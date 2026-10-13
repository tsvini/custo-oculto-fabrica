"""Publicação automática no YouTube.

  python -m fabrica.publicar enfileirar saida   → põe os vídeos gerados na fila (release "fila" do GitHub)
  python -m fabrica.publicar enviar             → sobe o que estiver na fila e agenda

Agenda: longo às 12h (Brasília), um Short por dia às 18h, sempre depois do último já agendado.
Os vídeos sobem privados com data de publicação. A cota grátis da API dá uns 5 vídeos por dia;
o que não couber fica na fila e sobe na execução diária seguinte (workflow "Publicar").

Secrets: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
"""
import datetime as dt, glob, json, os, shutil, subprocess, sys, tempfile, time
import requests

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


def proximo_horario(tipo, reg, caso=None):
    agora = dt.datetime.now(BRT)
    dia = agora.date()
    if agora.hour >= HORA[tipo] - 2:  # precisa de folga para o YouTube processar
        dia += dt.timedelta(days=1)
    ultimos = [dt.datetime.fromisoformat(r["publishAt"]).astimezone(BRT).date() for r in reg if r["tipo"] == tipo]
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
    return dt.datetime(dia.year, dia.month, dia.day, HORA[tipo], tzinfo=BRT)


# ---------- YouTube ----------
def token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"Não consegui entrar no YouTube ({r.status_code}): {r.text[:300]}. Confira os secrets YT_CLIENT_ID, YT_CLIENT_SECRET e YT_REFRESH_TOKEN.")
    return r.json()["access_token"]


def checar(r, oque):
    if r.status_code in (200, 201):
        return r
    txt = r.text[:600]
    if r.status_code == 403 and any(k in txt for k in ("quotaExceeded", "uploadLimitExceeded", "dailyLimitExceeded")):
        raise Cota(txt)
    raise RuntimeError(f"{oque}: erro {r.status_code}: {txt}")


def subir_video(tk, path, meta, quando):
    corpo = {"snippet": {"title": meta["titulo"], "description": meta["descricao"], "tags": meta.get("tags", [])[:30],
                         "categoryId": "27", "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"},
             "status": {"privacyStatus": "private", "publishAt": quando.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "selfDeclaredMadeForKids": False, "containsSyntheticMedia": False}}
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


def subir_legenda(tk, vid, path):
    snip = json.dumps({"snippet": {"videoId": vid, "language": "pt-BR", "name": "Português", "isDraft": False}})
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
        tk = token(); reg = registro(); feitos = []
        try:
            for nome in ordem:
                meta = metas[nome]
                if f"{nome}__video.mp4" not in itens[nome]:
                    continue
                gh("release", "download", TAG, "-p", f"{nome}__*", "-D", t, "--clobber")
                quando = proximo_horario(meta["tipo"], reg, meta.get("caso"))
                lg = next((x for x in reg if meta.get("caso") and x["nome"] == f"{meta['caso']}_longo" and x.get("video_id")), None)
                if lg and meta["tipo"] != "longo" and "youtu.be/" not in meta["descricao"]:
                    meta["descricao"] = f"▶ Caso completo: https://youtu.be/{lg['video_id']}\n\n" + meta["descricao"]
                v = subir_video(tk, os.path.join(t, f"{nome}__video.mp4"), meta, quando)
                vid = v["id"]; extra = []
                for suf, fn in (("miniatura.jpg", subir_miniatura), ("legenda.srt", subir_legenda)):
                    if f"{nome}__{suf}" in itens[nome]:
                        try:
                            fn(tk, vid, os.path.join(t, f"{nome}__{suf}"))
                        except Cota:
                            raise
                        except Exception as e:
                            extra.append(f"{suf.split('.')[0]} falhou: {str(e)[:150]}")
                reg.append({"nome": nome, "tipo": meta["tipo"], "titulo": meta["titulo"], "video_id": vid, "caso": meta.get("caso"), "caso_titulo": meta.get("caso_titulo"),
                            "publishAt": quando.isoformat(), "status": v.get("status", {}).get("privacyStatus")})
                feitos.append(f"{meta['titulo']} → {quando:%d/%m %Hh} (youtu.be/{vid})" + (f" [{'; '.join(extra)}]" if extra else ""))
                for a in itens[nome]:
                    gh("release", "delete-asset", TAG, a, "-y", check=False)
                json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        except Cota:
            nota("Cota do dia acabou", "o resto da fila sobe na próxima execução diária", "warning")
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
        tk = tk or token()
        try:
            subir_miniatura(tk, r["video_id"], arq); r["miniatura_ok"] = h; feitos.append(nome)
        except Exception as e:
            nota("Miniatura falhou", f"{nome}: {str(e)[:300]}", "warning")
    if feitos:
        json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        nota("Miniaturas aplicadas", ", ".join(feitos))


TODOS = "Todos os casos | Custo Oculto"


def playlists():
    """Playlists que tocam em sequência: uma com todos os longos e uma por caso (longo + série)."""
    reg = registro(); tk = token(); H = {"Authorization": f"Bearer {tk}"}; Y = "https://www.googleapis.com/youtube/v3"
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
                                     json={"snippet": {"title": titulo, "description": desc, "defaultLanguage": "pt-BR"}, "status": {"privacyStatus": "public"}}), "criar playlist")
            ex[titulo] = q.json()["id"]
        return ex[titulo]
    feitos = []
    try:
        for r in reg:
            if not r.get("video_id"):
                continue
            alvos = []
            if r.get("tipo") == "longo":
                alvos.append((TODOS, "Todos os casos do Custo Oculto, um atrás do outro: fraudes, quedas e quem pagou a conta."))
            if r.get("caso") in titulos and r.get("tipo") in ("longo", "serie"):
                alvos.append((f"Caso {titulos[r['caso']]} | Custo Oculto", f"O caso {titulos[r['caso']]} completo e em partes."))
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
        json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        nota("Playlists", f"{len(feitos)} adicionados: " + "; ".join(feitos)[:800])


def conferir():
    tk = token()
    r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true", headers={"Authorization": f"Bearer {tk}"}, timeout=30)
    if r.status_code != 200:
        nota("YouTube: falhou", f"{r.status_code}: {r.text[:500]}", "error"); raise SystemExit(1)
    it = r.json().get("items") or []
    if not it:
        nota("YouTube: nenhum canal", "a conta autorizada não tem canal. Autorize com a conta/canal Custo Oculto.", "error"); raise SystemExit(1)
    c = it[0]
    nota("YouTube conectado", f"canal: {c['snippet']['title']} · inscritos: {c['statistics'].get('subscriberCount')} · vídeos: {c['statistics'].get('videoCount')}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "enviar"
    if cmd == "miniaturas":
        miniaturas(sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "saida"))
    elif cmd == "conferir":
        conferir()
    elif cmd == "playlists":
        playlists()
    elif cmd == "enfileirar":
        enfileirar(sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "saida"))
    else:
        enviar()

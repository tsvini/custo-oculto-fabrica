"""Agenda do canal Vini QA no YouTube (@viniqaoficial).

  python -m fabrica.viniqa            → sobe os vídeos da agenda que ainda não estão no canal, já agendados

Lê projetos/*/agenda.json ({"link_curso", "videos": [{"short", "data", "hora", "titulo", "legenda"}]}),
baixa o MP4 do release "videos" e sobe privado com data de publicação. Registro em publicados_viniqa.json.
Secret: YT_REFRESH_TOKEN_QA (mais YT_CLIENT_ID e YT_CLIENT_SECRET, os mesmos dos outros canais).
A cota da API é a mesma dos outros canais: o que não couber sobe na execução diária seguinte.
"""
import datetime as dt, glob, json, os, subprocess, tempfile

from .publicar import BRT, Cota, checar, nota
import requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(RAIZ, "publicados_viniqa.json")
CFG = os.path.join(RAIZ, "projetos", "viniqa.json")  # {"link_professor": "...", "comentario": "texto com {link}"}
ENV = "YT_REFRESH_TOKEN_QA"


def token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ[ENV], "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"Não consegui entrar no canal Vini QA ({r.status_code}): {r.text[:300]}. Confira o secret {ENV}.")
    return r.json()["access_token"]


def descricao(item, link, cupom=None):
    leg = item["legenda"]
    corpo, _, tags = leg.partition(" #")
    corpo = corpo.replace("Curso completo de Cypress do zero: link na bio.", "").strip()
    promo = f"{cupom['texto']}\n" if cupom and dt.date.today().isoformat() < cupom["ate"] else ""
    return (f"{corpo}\n\n🎓 Curso completo de Cypress pra quem tá começando do zero:\n{promo}{link}\n\n"
            f"Sou o Vinícius Torales, QA, e ensino testes automatizados do zero.\n\n#" + tags).strip()


def subir(tk, path, titulo, desc, quando):
    corpo = {"snippet": {"title": titulo[:100], "description": desc, "categoryId": "27", "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR",
                         "tags": ["cypress", "qa", "testes automatizados", "automação de testes", "curso de cypress"]},
             "status": {"privacyStatus": "private", "publishAt": quando.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "selfDeclaredMadeForKids": False, "containsSyntheticMedia": False}}
    tam = os.path.getsize(path)
    r = checar(requests.post("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                             headers={"Authorization": f"Bearer {tk}", "Content-Type": "application/json; charset=UTF-8",
                                      "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)},
                             data=json.dumps(corpo), timeout=60), "iniciar envio")
    with open(path, "rb") as f:
        r = checar(requests.put(r.headers["Location"], headers={"Authorization": f"Bearer {tk}", "Content-Type": "video/mp4",
                                                                "Content-Length": str(tam)}, data=f, timeout=3600), "enviar vídeo")
    return r.json()["id"]


def atualizar_descricoes(tk_fn, reg):
    """vídeo já no canal com a descrição antiga (link ou cupom mudou na agenda): troca só a descrição"""
    agendas = {}
    for ag in glob.glob(os.path.join(RAIZ, "projetos", "*", "agenda.json")):
        a = json.load(open(ag, encoding="utf8")); slug = os.path.basename(os.path.dirname(ag)).replace("-", "_")
        for it in a["videos"]:
            agendas[f"{slug}_short{it['short']}.mp4"] = descricao(it, a["link_curso"], a.get("cupom"))
    feitos = []; tk = None
    for r in reg:
        nova = agendas.get(r["arquivo"])
        if not nova or r.get("desc") == nova:
            continue
        tk = tk or tk_fn()
        h = {"Authorization": f"Bearer {tk}"}
        v = checar(requests.get("https://www.googleapis.com/youtube/v3/videos", params={"part": "snippet", "id": r["video_id"]}, headers=h, timeout=30), "ler vídeo").json()
        if not v.get("items"):
            continue
        sn = v["items"][0]["snippet"]; sn["description"] = nova
        checar(requests.put("https://www.googleapis.com/youtube/v3/videos?part=snippet", headers={**h, "Content-Type": "application/json"},
                            data=json.dumps({"id": r["video_id"], "snippet": {k: sn[k] for k in ("title", "description", "categoryId", "tags", "defaultLanguage", "defaultAudioLanguage") if k in sn}}), timeout=30), "atualizar descrição")
        r["desc"] = nova; feitos.append(r["titulo"])
        json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    return feitos


def comentar(tk_fn, reg):
    """Comenta em cada vídeo do canal, assim que ele fica público, o link da página de professor (texto aprovado pelo Vinícius em 10/11/2026)."""
    try:
        cfg = json.load(open(CFG, encoding="utf8"))
    except Exception:
        return []
    link = (cfg.get("link_professor") or "").strip()
    if not link:
        return []
    texto = cfg.get("comentario", "📌 Todos os meus cursos estão aqui: {link}").replace("{link}", link)
    agora = dt.datetime.now(BRT); feitos = []; tk = None
    for r in reg:
        if r.get("comentario") or dt.datetime.fromisoformat(r["publishAt"]) > agora:
            continue
        tk = tk or tk_fn(); H = {"Authorization": f"Bearer {tk}"}
        v = requests.get("https://www.googleapis.com/youtube/v3/videos", headers=H, params={"part": "status", "id": r["video_id"]}, timeout=30).json().get("items") or []
        if not v or v[0]["status"]["privacyStatus"] != "public":
            continue
        q = requests.post("https://www.googleapis.com/youtube/v3/commentThreads?part=snippet", headers=H, timeout=30,
                          json={"snippet": {"videoId": r["video_id"], "topLevelComment": {"snippet": {"textOriginal": texto}}}})
        if q.status_code in (200, 201):
            r["comentario"] = q.json()["id"]; feitos.append(r["titulo"])
            json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        else:
            nota("Vini QA: comentário falhou", f"{r['titulo']}: {q.status_code} " + " ".join(q.text.split())[:300], "warning"); break
    return feitos


def main():
    if not os.environ.get(ENV, "").strip():
        nota("Vini QA", f"falta o secret {ENV}: nada subiu", "warning"); return
    try:
        reg = json.load(open(REG, encoding="utf8"))
    except Exception:
        reg = []
    feitos = {r["arquivo"] for r in reg}
    agora = dt.datetime.now(BRT); tk = None; ok = []
    try:
        for ag in sorted(glob.glob(os.path.join(RAIZ, "projetos", "*", "agenda.json"))):
            a = json.load(open(ag, encoding="utf8")); slug = os.path.basename(os.path.dirname(ag)).replace("-", "_")
            for it in a["videos"]:
                arq = f"{slug}_short{it['short']}.mp4"
                h, m = map(int, it.get("hora", "12:00").split(":"))
                quando = dt.datetime.fromisoformat(it["data"]).replace(hour=h, minute=m, tzinfo=BRT)
                if arq in feitos:
                    continue
                if quando < agora + dt.timedelta(hours=2):
                    nota("Vini QA", f"{arq} passou da data ({it['data']}) e não subiu", "warning"); continue
                tk = tk or token()
                with tempfile.TemporaryDirectory() as t:
                    if subprocess.run(["gh", "release", "download", "outros-videos", "-p", arq, "-D", t, "--clobber"]).returncode:  # vídeo do canal fica em outros-videos
                        subprocess.run(["gh", "release", "download", "videos", "-p", arq, "-D", t, "--clobber"], check=True)
                    desc = descricao(it, a["link_curso"], a.get("cupom"))
                    vid = subir(tk, os.path.join(t, arq), it["titulo"], desc, quando)
                reg.append({"arquivo": arq, "titulo": it["titulo"], "video_id": vid, "publishAt": quando.isoformat(), "desc": desc})
                json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
                ok.append(f"{it['titulo']} → {quando:%d/%m %Hh} (youtu.be/{vid})")
        cm = comentar(lambda: tk or token(), reg)
        if cm:
            ok.append(f"comentário com o link em {len(cm)} vídeo(s) (fixe no Studio)")
        at = atualizar_descricoes(lambda: tk or token(), reg)
        if at:
            ok.append(f"descrição nova em {len(at)} vídeo(s)")
    except Cota as e:
        ok.append(f"limite do YouTube: o resto sobe amanhã ({str(e)[:200]})")
    except Exception as e:
        ok.append(f"ERRO: {str(e)[:300]}")
    nota("Vini QA agendados", " | ".join(ok) if ok else "nada novo")
    open(os.path.join(RAIZ, "viniqa_status.txt"), "w", encoding="utf8").write(
        f"{dt.datetime.now(BRT):%d/%m %H:%M} · {len(reg)} no canal · " + (" | ".join(ok) if ok else "nada novo") + "\n")


if __name__ == "__main__":
    main()

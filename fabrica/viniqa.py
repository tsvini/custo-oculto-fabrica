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
ENV = "YT_REFRESH_TOKEN_QA"


def token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ[ENV], "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"Não consegui entrar no canal Vini QA ({r.status_code}): {r.text[:300]}. Confira o secret {ENV}.")
    return r.json()["access_token"]


def descricao(item, link):
    leg = item["legenda"]
    corpo, _, tags = leg.partition(" #")
    corpo = corpo.replace("Curso completo de Cypress do zero: link na bio.", "").strip()
    return (f"{corpo}\n\n🎓 Curso completo de Cypress pra quem tá começando do zero:\n{link}\n\n"
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
                    subprocess.run(["gh", "release", "download", "videos", "-p", arq, "-D", t, "--clobber"], check=True)
                    vid = subir(tk, os.path.join(t, arq), it["titulo"], descricao(it, a["link_curso"]), quando)
                reg.append({"arquivo": arq, "titulo": it["titulo"], "video_id": vid, "publishAt": quando.isoformat()})
                json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
                ok.append(f"{it['titulo']} → {quando:%d/%m %Hh} (youtu.be/{vid})")
    except Cota:
        nota("Vini QA", "cota do dia acabou: o resto sobe amanhã", "warning")
    nota("Vini QA agendados", " | ".join(ok) if ok else "nada novo")


if __name__ == "__main__":
    main()

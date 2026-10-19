"""Painel único: junta YouTube (Custo Oculto, Hidden Cost, Vini QA), TikTok, Instagram, Facebook e Udemy
em docs/painel/dados.json (lido pela página docs/painel/index.html, no GitHub Pages).

Roda todo dia pelo workflow "Painel". Cada fonte é independente: se uma falhar, as outras continuam.
Udemy não tem API aberta para instrutor: os números vêm de painel_manual.json (atualizado à mão).
"""
import datetime as dt
import json
import os

import requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "docs", "painel", "dados.json")
HIST = os.path.join(RAIZ, "docs", "painel", "historico.json")
YT = "https://www.googleapis.com/youtube/v3"
YA = "https://youtubeanalytics.googleapis.com/v2/reports"
GV = os.environ.get("META_GRAPH_VERSION", "v24.0")
CANAIS_YT = [("custo_oculto", "Custo Oculto (YouTube)", "YT_REFRESH_TOKEN"),
             ("hidden_cost", "Hidden Cost (YouTube EN)", "YT_REFRESH_TOKEN_EN"),
             ("vini_qa", "Vini QA (YouTube)", "YT_REFRESH_TOKEN_QA")]


def env(k):
    return os.environ.get(k, "").strip()


def yt_token(var):
    r = requests.post("https://oauth2.googleapis.com/token", timeout=30, data={
        "client_id": env("YT_CLIENT_ID"), "client_secret": env("YT_CLIENT_SECRET"), "refresh_token": env(var), "grant_type": "refresh_token"})
    r.raise_for_status()
    return r.json()["access_token"]


def youtube(var):
    H = {"Authorization": f"Bearer {yt_token(var)}"}
    ch = requests.get(f"{YT}/channels", headers=H, params={"part": "statistics,snippet", "mine": "true"}, timeout=30).json()["items"][0]
    st = ch["statistics"]
    hoje = dt.date.today(); ini = (hoje - dt.timedelta(days=28)).isoformat()
    dia = requests.get(YA, headers=H, timeout=60, params={"ids": "channel==MINE", "startDate": ini, "endDate": hoje.isoformat(),
                                                           "metrics": "views,subscribersGained", "dimensions": "day", "sort": "day"}).json().get("rows", [])
    top = requests.get(YA, headers=H, timeout=60, params={"ids": "channel==MINE", "startDate": ini, "endDate": hoje.isoformat(),
                                                           "metrics": "views,averageViewPercentage,likes", "dimensions": "video", "sort": "-views", "maxResults": "5"}).json().get("rows", [])
    titulos = {}
    if top:
        v = requests.get(f"{YT}/videos", headers=H, params={"part": "snippet", "id": ",".join(r[0] for r in top)}, timeout=30).json()
        titulos = {i["id"]: i["snippet"]["title"] for i in v.get("items", [])}
    return {"seguidores": int(st.get("subscriberCount", 0)), "views_total": int(st.get("viewCount", 0)), "videos": int(st.get("videoCount", 0)),
            "views_28d": sum(r[1] for r in dia), "views_7d": sum(r[1] for r in dia[-7:]), "seguidores_28d": sum(r[2] for r in dia),
            "dia": [[r[0], r[1]] for r in dia],
            "top": [{"titulo": titulos.get(r[0], r[0]), "url": f"https://youtu.be/{r[0]}", "views": r[1], "retencao": round(r[2]), "likes": r[3]} for r in top]}


def instagram():
    tok, ig = env("META_PAGE_TOKEN"), env("META_IG_ID")
    G = f"https://graph.facebook.com/{GV}"
    p = requests.get(f"{G}/{ig}", params={"fields": "username,followers_count,media_count", "access_token": tok}, timeout=30).json()
    m = requests.get(f"{G}/{ig}/media", params={"fields": "caption,permalink,like_count,comments_count,timestamp", "limit": 5, "access_token": tok}, timeout=30).json()
    return {"seguidores": p.get("followers_count", 0), "videos": p.get("media_count", 0), "usuario": p.get("username"),
            "top": [{"titulo": (x.get("caption") or "").split("\n")[0][:90], "url": x.get("permalink"), "likes": x.get("like_count", 0),
                     "comentarios": x.get("comments_count", 0)} for x in m.get("data", [])]}


def facebook():
    tok, pg = env("META_PAGE_TOKEN"), env("META_PAGE_ID")
    p = requests.get(f"https://graph.facebook.com/{GV}/{pg}", params={"fields": "name,followers_count,fan_count", "access_token": tok}, timeout=30).json()
    return {"seguidores": p.get("followers_count") or p.get("fan_count") or 0}


def tiktok():
    from .redes import tiktok_token
    t = tiktok_token(); H = {"Authorization": f"Bearer {t}"}
    u = requests.get("https://open.tiktokapis.com/v2/user/info/", headers=H, timeout=30,
                     params={"fields": "display_name,follower_count,likes_count,video_count"}).json()
    d = (u.get("data") or {}).get("user") or {}
    out = {"usuario": d.get("display_name"), "seguidores": d.get("follower_count"), "curtidas": d.get("likes_count"), "videos": d.get("video_count")}
    if out["seguidores"] is None:
        out["aviso"] = "TikTok não devolveu os números: " + str(u.get("error"))[:200]
    try:  # vídeos mais recentes com views e curtidas (permissão video.list)
        vl = requests.post("https://open.tiktokapis.com/v2/video/list/", headers=dict(H, **{"Content-Type": "application/json"}), timeout=30,
                           params={"fields": "id,title,view_count,like_count,comment_count,share_url,create_time"}, json={"max_count": 20}).json()
        vids = (vl.get("data") or {}).get("videos") or []
        out["views_total"] = sum(v.get("view_count") or 0 for v in vids)
        out["top"] = [{"titulo": (v.get("title") or "").split("#")[0].strip()[:90] or "(sem título)", "url": v.get("share_url"), "views": v.get("view_count"),
                       "likes": v.get("like_count")} for v in sorted(vids, key=lambda v: v.get("create_time") or 0, reverse=True)[:6]]
    except Exception as e:
        out["aviso"] = f"lista de vídeos: {str(e)[:120]}"
    return out


def udemy():
    H = {"Authorization": f"bearer {env('UDEMY_TOKEN')}", "Accept": "application/json"}
    B = "https://www.udemy.com/instructor-api/v1/taught-courses"
    cs = requests.get(f"{B}/courses/", headers=H, params={"fields[course]": "@all", "page_size": 20}, timeout=30)
    cs.raise_for_status(); cursos = cs.json().get("results", [])
    rv = requests.get(f"{B}/reviews/", headers=H, params={"page_size": 5}, timeout=30).json()
    qs = requests.get(f"{B}/questions/", headers=H, params={"page_size": 10, "status": "unresponded"}, timeout=30).json()
    alunos = sum(int(c.get("num_subscribers") or 0) for c in cursos)
    return {"alunos": alunos or None, "cursos": [{"titulo": c.get("title"), "url": "https://www.udemy.com" + (c.get("url") or ""), "alunos": c.get("num_subscribers"),
                                                  "nota": c.get("rating"), "avaliacoes": c.get("num_reviews")} for c in cursos],
            "avaliacoes": rv.get("count"), "perguntas_sem_resposta": qs.get("count")}


def agenda():
    """Tudo que está para ser lançado, de todas as plataformas, em ordem de data."""
    agora = dt.datetime.now(dt.timezone.utc); itens = []
    def futuro(q):
        try:
            return dt.datetime.fromisoformat(q.replace("Z", "+00:00")) > agora
        except Exception:
            return False
    try:
        for r in json.load(open(os.path.join(RAIZ, "publicados.json"), encoding="utf8")):
            if r.get("publishAt") and futuro(r["publishAt"]) and r.get("status") != "public":
                en = (r.get("idioma") or "pt").startswith("en")
                itens.append({"quando": r["publishAt"], "plataforma": "Hidden Cost (YouTube EN)" if en else "Custo Oculto (YouTube)",
                              "chave": "hidden_cost" if en else "custo_oculto", "titulo": r.get("titulo"), "tipo": r.get("tipo"),
                              "id": r["nome"], "url": f"https://studio.youtube.com/video/{r['video_id']}/edit"})
    except Exception as e:
        print(f"::warning title=Agenda YouTube::{e}")
    try:
        for r in json.load(open(os.path.join(RAIZ, "publicados_viniqa.json"), encoding="utf8")):
            if r.get("publishAt") and futuro(r["publishAt"]):
                itens.append({"quando": r["publishAt"], "plataforma": "Vini QA (YouTube)", "chave": "vini_qa", "titulo": r.get("titulo"), "tipo": "short",
                              "id": r["video_id"], "url": f"https://studio.youtube.com/video/{r['video_id']}/edit"})
    except Exception as e:
        print(f"::warning title=Agenda Vini QA::{e}")
    try:
        for it in json.load(open(os.path.join(RAIZ, "agenda_redes.json"), encoding="utf8")):
            if it.get("cancelado") or not futuro(it["quando"]) or it["quando"].startswith("2099"):
                continue
            for rede in it.get("redes", []):
                if str((it.get("status") or {}).get(rede, "")).startswith("ok"):
                    continue
                itens.append({"quando": it["quando"], "plataforma": {"instagram": "Instagram", "facebook": "Facebook", "tiktok": "TikTok"}.get(rede, rede),
                              "chave": rede, "titulo": it.get("titulo"), "tipo": "short", "id": it["id"], "url": it.get("video")})
    except Exception as e:
        print(f"::warning title=Agenda redes::{e}")
    try:  # TikToks antigos agendados no Metricool (lista copiada à mão em painel_manual.json)
        man = json.load(open(os.path.join(RAIZ, "painel_manual.json"), encoding="utf8"))
        for it in man.get("metricool", []):
            if futuro(it["quando"]):
                rede = it.get("plataforma_rede", "tiktok")
                itens.append(dict(it, chave=rede, plataforma=("Instagram" if rede == "instagram" else "TikTok") + " (Metricool)", sem_cancelar=True))
    except Exception:
        pass
    return sorted(itens, key=lambda x: x["quando"])


def esperando():
    """Vídeos já prontos no YouTube, privados e sem data: esperando aprovação."""
    try:
        reg = json.load(open(os.path.join(RAIZ, "publicados.json"), encoding="utf8"))
    except Exception:
        return []
    return [{"titulo": r.get("titulo"), "id": r["nome"], "plataforma": "Hidden Cost (YouTube EN)" if (r.get("idioma") or "pt").startswith("en") else "Custo Oculto (YouTube)",
             "url": f"https://studio.youtube.com/video/{r['video_id']}/edit", "cancelado": bool(r.get("cancelado"))}
            for r in reg if r.get("video_id") and r.get("status") == "private" and not r.get("publishAt")]


def main():
    dados = {"atualizado": dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M"), "fontes": {}}
    fontes = [(k, nome, (lambda v=var: youtube(v)), var) for k, nome, var in CANAIS_YT]
    fontes += [("tiktok", "TikTok @custooculto", tiktok, "TIKTOK_CLIENT_KEY"),
               ("instagram", "Instagram @custooculto.oficial", instagram, "META_PAGE_TOKEN"),
               ("facebook", "Facebook · Custo Oculto", facebook, "META_PAGE_TOKEN")]
    for k, nome, fn, var in fontes:
        if not env(var):
            dados["fontes"][k] = {"nome": nome, "erro": "não conectado"}; continue
        try:
            dados["fontes"][k] = dict(fn(), nome=nome)
        except Exception as e:
            dados["fontes"][k] = {"nome": nome, "erro": str(e)[:200]}
            print(f"::warning title=Painel {k}::{str(e)[:300]}", flush=True)
    try:
        man = json.load(open(os.path.join(RAIZ, "painel_manual.json"), encoding="utf8"))
    except Exception:
        man = {}
    dados["fontes"]["udemy"] = dict({"nome": "Udemy · Cypress para leigos"}, **man.get("udemy", {}))
    if env("UDEMY_TOKEN"):
        try:
            dados["fontes"]["udemy"].update({k: v for k, v in udemy().items() if v is not None}); dados["fontes"]["udemy"].pop("obs", None)
        except Exception as e:
            dados["fontes"]["udemy"]["aviso"] = f"API da Udemy: {str(e)[:150]}"
    dados["agenda"] = agenda()
    dados["esperando"] = esperando()
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    json.dump(dados, open(SAIDA, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    # histórico de seguidores por dia (para o gráfico de evolução)
    try:
        hist = json.load(open(HIST, encoding="utf8"))
    except Exception:
        hist = {}
    dia = dt.date.today().isoformat()
    hist[dia] = {k: v.get("seguidores") for k, v in dados["fontes"].items() if isinstance(v.get("seguidores"), (int, float))}
    json.dump(dict(sorted(hist.items())[-180:]), open(HIST, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("::notice title=Painel::" + " · ".join(f"{v['nome']}: {v.get('seguidores', v.get('erro', '-'))}" for v in dados["fontes"].values()), flush=True)


if __name__ == "__main__":
    main()

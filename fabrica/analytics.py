"""Relatório do canal pelo YouTube Analytics: salva relatorios/AAAA-MM-DD.json e relatorios/ultimo.json.

Mede o que importa para a monetização: horas de vídeo longo (12 meses), inscritos,
retenção e origem do tráfego de cada vídeo.
"""
import datetime as dt, json, os
import requests

from .publicar import token, registro, nota, RAIZ

A = "https://youtubeanalytics.googleapis.com/v2/reports"


def rep(H, ini, fim, **kw):
    q = {"ids": "channel==MINE", "startDate": ini, "endDate": fim, **kw}
    r = requests.get(A, headers=H, params=q, timeout=60)
    if r.status_code != 200:
        return {"erro": f"{r.status_code} {' '.join(r.text.split())[:300]}"}
    j = r.json(); cols = [c["name"] for c in j.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in j.get("rows", [])]


def main():
    H = {"Authorization": f"Bearer {token()}"}
    hoje = dt.date.today(); fim = hoje.isoformat()
    ano = (hoje - dt.timedelta(days=365)).isoformat(); d28 = (hoje - dt.timedelta(days=28)).isoformat(); d7 = (hoje - dt.timedelta(days=7)).isoformat()
    out = {"data": fim}
    out["por_formato_12m"] = rep(H, ano, fim, metrics="views,estimatedMinutesWatched,subscribersGained", dimensions="creatorContentType")
    out["por_formato_7d"] = rep(H, d7, fim, metrics="views,estimatedMinutesWatched,subscribersGained", dimensions="creatorContentType")
    out["dia_a_dia_28d"] = rep(H, d28, fim, metrics="views,estimatedMinutesWatched,subscribersGained", dimensions="day", sort="day")
    out["origem_28d"] = rep(H, d28, fim, metrics="views,estimatedMinutesWatched", dimensions="insightTrafficSourceType", sort="-views")
    out["buscas_28d"] = rep(H, d28, fim, metrics="views", dimensions="insightTrafficSourceDetail", filters="insightTrafficSourceType==YT_SEARCH", sort="-views", maxResults="25")
    out["videos_28d"] = rep(H, d28, fim, metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares",
                            dimensions="video", sort="-views", maxResults="50")
    nomes = {r["video_id"]: r["nome"] for r in registro() if r.get("video_id")}
    out["retencao"] = {}
    for r in registro():
        if r.get("tipo") == "longo" and r.get("video_id"):
            out["retencao"][r["nome"]] = rep(H, ano, fim, metrics="audienceWatchRatio,relativeRetentionPerformance", dimensions="elapsedVideoTimeRatio",
                                             filters=f"video=={r['video_id']}")
    out["nomes"] = nomes
    # contagem atual (Data API, quase em tempo real; o Analytics atrasa 2-3 dias)
    ids = [r["video_id"] for r in registro() if r.get("video_id")]; atual = {}
    for i in range(0, len(ids), 50):
        q = requests.get("https://www.googleapis.com/youtube/v3/videos", headers=H, timeout=60,
                         params={"part": "statistics,status", "id": ",".join(ids[i:i + 50])})
        for it in (q.json().get("items", []) if q.ok else []):
            st = it.get("statistics", {})
            atual[nomes.get(it["id"], it["id"])] = {"views": int(st.get("viewCount", 0)), "likes": int(st.get("likeCount", 0)),
                                                    "comentarios": int(st.get("commentCount", 0)), "status": it.get("status", {}).get("privacyStatus")}
    out["contagem_atual"] = atual
    q = requests.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true", headers=H, timeout=30)
    out["canal"] = (q.json().get("items") or [{}])[0].get("statistics") if q.ok else None
    os.makedirs(os.path.join(RAIZ, "relatorios"), exist_ok=True)
    for fn in (f"{fim}.json", "ultimo.json"):
        json.dump(out, open(os.path.join(RAIZ, "relatorios", fn), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    f12 = out["por_formato_12m"]
    if isinstance(f12, list):
        horas = sum(x.get("estimatedMinutesWatched", 0) for x in f12 if x.get("creatorContentType") not in ("SHORTS", "shorts")) / 60
        nota("Rumo às 4.000 horas", f"horas de vídeo longo nos últimos 12 meses: {horas:.1f} · formatos: " + "; ".join(f"{x.get('creatorContentType')}: {x.get('views')} views" for x in f12))
    else:
        nota("Analytics", str(f12), "warning")


if __name__ == "__main__":
    main()

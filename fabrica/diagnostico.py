"""Diagnóstico de entrega de um vídeo do YouTube (só leitura).
python -m fabrica.diagnostico <video_id> [outros ids...]"""
import datetime as dt, json, sys
import requests
from .publicar import token

Y = "https://www.googleapis.com/youtube/v3"


def nota(t, m):
    print(f"::notice title={t}::{m}", flush=True)


def main(ids):
    H = {"Authorization": f"Bearer {token()}"}
    v = requests.get(f"{Y}/videos", headers=H, timeout=30, params={"part": "snippet,status,contentDetails,statistics,processingDetails,suggestions,fileDetails", "id": ",".join(ids)}).json()
    for it in v.get("items", []):
        sn, st, cd = it["snippet"], it["status"], it["contentDetails"]
        nota(f"Vídeo {it['id']}", json.dumps({
            "titulo": sn["title"], "publicado": sn.get("publishedAt"), "stats": it.get("statistics"),
            "status": st, "duracao": cd.get("duration"), "licensed": cd.get("licensedContent"), "restricao": cd.get("regionRestriction"),
            "rating": cd.get("contentRating"), "processamento": it.get("processingDetails", {}).get("processingStatus"),
            "arquivo": {k: it.get("fileDetails", {}).get(k) for k in ("videoStreams",)}, "sugestoes": it.get("suggestions"),
            "tags": sn.get("tags"), "categoria": sn.get("categoryId"), "idioma": sn.get("defaultAudioLanguage")}, ensure_ascii=False)[:3800])
    # últimos uploads do canal p/ comparar
    ch = requests.get(f"{Y}/channels", headers=H, params={"part": "contentDetails", "mine": "true"}, timeout=30).json()["items"][0]
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    pl = requests.get(f"{Y}/playlistItems", headers=H, params={"part": "contentDetails", "playlistId": up, "maxResults": 25}, timeout=30).json()
    vid = [x["contentDetails"]["videoId"] for x in pl.get("items", [])]
    vv = requests.get(f"{Y}/videos", headers=H, params={"part": "snippet,statistics,status", "id": ",".join(vid)}, timeout=30).json()
    linhas = [f"{x['snippet'].get('publishedAt','')[:16]} {x['status']['privacyStatus'][:4]} {x['statistics'].get('viewCount','?'):>6} {x['snippet']['title'][:50]}" for x in vv.get("items", [])]
    nota("Últimos uploads", " | ".join(linhas)[:3900])
    # tráfego por origem (Analytics, pode ter atraso)
    hoje = dt.date.today().isoformat(); ini = (dt.date.today() - dt.timedelta(days=3)).isoformat()
    for i in ids:
        r = requests.get("https://youtubeanalytics.googleapis.com/v2/reports", headers=H, timeout=60, params={"ids": "channel==MINE", "startDate": ini, "endDate": hoje,
            "metrics": "views,averageViewPercentage", "dimensions": "insightTrafficSourceType", "filters": f"video=={i}"})
        nota(f"Origem {i}", r.text[:1500])


if __name__ == "__main__":
    main(sys.argv[1:])

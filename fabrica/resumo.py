"""Resumo rápido de todos os canais (inscritos, views e os últimos vídeos com views/likes), em anotações do Actions."""
import os
import requests
from .publicar import checar, nota

Y = "https://www.googleapis.com/youtube/v3"
CANAIS = [("Custo Oculto", "YT_REFRESH_TOKEN"), ("Hidden Cost", "YT_REFRESH_TOKEN_EN"), ("Vini QA", "YT_REFRESH_TOKEN_QA")]


def tk(env):
    r = requests.post("https://oauth2.googleapis.com/token", data={"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                                                   "refresh_token": os.environ[env], "grant_type": "refresh_token"}, timeout=30)
    return r.json().get("access_token")


def main():
    for nome, env in CANAIS:
        if not os.environ.get(env):
            nota(nome, "sem token"); continue
        H = {"Authorization": f"Bearer {tk(env)}"}
        ch = checar(requests.get(f"{Y}/channels?part=statistics,contentDetails&mine=true", headers=H, timeout=30), "canal").json()["items"][0]
        up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
        j = checar(requests.get(f"{Y}/playlistItems?part=contentDetails&maxResults=25&playlistId={up}", headers=H, timeout=30), "uploads").json()
        ids = [i["contentDetails"]["videoId"] for i in j.get("items", [])]
        linhas = []
        if ids:
            v = checar(requests.get(f"{Y}/videos?part=snippet,statistics,status&id={','.join(ids)}", headers=H, timeout=30), "vídeos").json()
            for x in v.get("items", []):
                s = x["statistics"]; st = x["status"]
                linhas.append(f"{x['snippet']['publishedAt'][:10] if st['privacyStatus']=='public' else 'agend.'} {s.get('viewCount',0)}v {s.get('likeCount',0)}♥ {x['snippet']['title'][:45]}")
        S = ch["statistics"]
        nota(f"{nome}", f"inscritos {S.get('subscriberCount')} · views {S.get('viewCount')} · vídeos {S.get('videoCount')} || " + " | ".join(linhas[:25]))


if __name__ == "__main__":
    main()

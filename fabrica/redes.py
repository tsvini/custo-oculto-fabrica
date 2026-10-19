"""Publicação direta (sem Metricool) em Instagram, Facebook e TikTok.

A agenda fica em agenda_redes.json:
  [{"id": "kolynos_v3", "quando": "2026-10-20T19:00:00-03:00", "video": "<URL pública do MP4>",
    "legenda": "...", "titulo": "...", "redes": ["instagram", "facebook", "tiktok"], "ia": true,
    "status": {"instagram": "ok:<id>" | "erro:<msg>", ...}}]

python -m fabrica.redes publicar   → publica tudo que já passou do horário e ainda não saiu (roda de hora em hora)
python -m fabrica.redes testar     → só confere tokens e contas, sem publicar

Segredos (GitHub → Settings → Secrets → Actions):
  META_PAGE_TOKEN   token de longa duração da Página do Facebook (dá acesso à Página e ao Instagram ligado a ela)
  META_PAGE_ID      ID da Página "Custo Oculto"
  META_IG_ID        ID da conta profissional do Instagram ligada à Página
  TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN   app do TikTok for Developers
  TIKTOK_MODO       "inbox" (padrão: vai pra caixa de entrada do app, você toca em publicar) ou "direto" (depois da auditoria)
"""
import datetime as dt
import json
import os
import sys
import tempfile
import time

import requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENDA = os.path.join(RAIZ, "agenda_redes.json")
GV = os.environ.get("META_GRAPH_VERSION", "v24.0")
G = f"https://graph.facebook.com/{GV}"
TT = "https://open.tiktokapis.com/v2"


def nota(t, m, nivel="notice"):
    print(f"::{nivel} title={t}::{str(m).replace(chr(10), ' ')[:900]}", flush=True)


def env(k):
    return os.environ.get(k, "").strip()


# ---------------- Instagram (Reels) ----------------
def instagram(item):
    tok, ig = env("META_PAGE_TOKEN"), env("META_IG_ID")
    if not (tok and ig):
        raise RuntimeError("sem META_PAGE_TOKEN/META_IG_ID")
    r = requests.post(f"{G}/{ig}/media", data={"media_type": "REELS", "video_url": item["video"], "caption": item["legenda"][:2200],
                                              "share_to_feed": "true", "access_token": tok}, timeout=120)
    r.raise_for_status(); cid = r.json()["id"]
    for _ in range(60):  # o Instagram baixa e processa o vídeo
        s = requests.get(f"{G}/{cid}", params={"fields": "status_code,status", "access_token": tok}, timeout=60).json()
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") == "ERROR":
            raise RuntimeError(f"processamento: {s.get('status')}")
        time.sleep(10)
    else:
        raise RuntimeError("processamento demorou demais")
    r = requests.post(f"{G}/{ig}/media_publish", data={"creation_id": cid, "access_token": tok}, timeout=120)
    r.raise_for_status()
    return r.json()["id"]


# ---------------- Facebook (Reels da Página) ----------------
def facebook(item):
    tok, pg = env("META_PAGE_TOKEN"), env("META_PAGE_ID")
    if not (tok and pg):
        raise RuntimeError("sem META_PAGE_TOKEN/META_PAGE_ID")
    r = requests.post(f"{G}/{pg}/video_reels", data={"upload_phase": "start", "access_token": tok}, timeout=60)
    r.raise_for_status(); vid = r.json()["video_id"]; up = r.json()["upload_url"]
    r = requests.post(up, headers={"Authorization": f"OAuth {tok}", "file_url": item["video"]}, timeout=600)
    r.raise_for_status()
    r = requests.post(f"{G}/{pg}/video_reels", data={"upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED",
                                                     "description": item["legenda"][:5000], "title": item.get("titulo", "")[:255],
                                                     "access_token": tok}, timeout=120)
    r.raise_for_status()
    if not r.json().get("success", True):
        raise RuntimeError(r.text[:300])
    return vid


# ---------------- TikTok ----------------
def tiktok_token():
    r = requests.post(f"{TT}/oauth/token/", data={"client_key": env("TIKTOK_CLIENT_KEY"), "client_secret": env("TIKTOK_CLIENT_SECRET"),
                                                  "grant_type": "refresh_token", "refresh_token": env("TIKTOK_REFRESH_TOKEN")},
                      headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=60)
    j = r.json()
    if "access_token" not in j:
        raise RuntimeError(f"token TikTok: {j}")
    if j.get("refresh_token") and j["refresh_token"] != env("TIKTOK_REFRESH_TOKEN"):
        nota("TikTok", "o TikTok devolveu um refresh token novo; atualize o segredo TIKTOK_REFRESH_TOKEN quando o atual vencer", "warning")
    return j["access_token"]


def tiktok(item):
    if not (env("TIKTOK_CLIENT_KEY") and env("TIKTOK_REFRESH_TOKEN")):
        raise RuntimeError("sem app do TikTok configurado")
    tok = tiktok_token(); H = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8"}
    with tempfile.TemporaryDirectory() as d:  # baixa o MP4 e envia por partes (FILE_UPLOAD não exige domínio verificado)
        arq = os.path.join(d, "v.mp4")
        with requests.get(item["video"], stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(arq, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
        tam = os.path.getsize(arq); parte = min(tam, 10_000_000); n = max(1, tam // parte)
        fonte = {"source": "FILE_UPLOAD", "video_size": tam, "chunk_size": parte, "total_chunk_count": n}
        if env("TIKTOK_MODO") == "direto":
            info = requests.post(f"{TT}/post/publish/creator_info/query/", headers=H, timeout=60).json().get("data", {})
            priv = "PUBLIC_TO_EVERYONE" if "PUBLIC_TO_EVERYONE" in info.get("privacy_level_options", []) else "SELF_ONLY"
            corpo = {"post_info": {"title": item["legenda"][:2200], "privacy_level": priv, "is_aigc": bool(item.get("ia", True)),
                                   "disable_comment": False, "disable_duet": False, "disable_stitch": False}, "source_info": fonte}
            url = f"{TT}/post/publish/video/init/"
        else:
            corpo = {"source_info": fonte}; url = f"{TT}/post/publish/inbox/video/init/"
        r = requests.post(url, headers=H, json=corpo, timeout=60).json()
        if r.get("error", {}).get("code") not in (None, "ok"):
            raise RuntimeError(f"init: {r['error']}")
        pid, up = r["data"]["publish_id"], r["data"]["upload_url"]
        with open(arq, "rb") as f:
            for i in range(n):
                ini = i * parte; fim = tam - 1 if i == n - 1 else ini + parte - 1
                f.seek(ini); b = f.read(fim - ini + 1)
                rr = requests.put(up, data=b, headers={"Content-Type": "video/mp4", "Content-Length": str(len(b)),
                                                       "Content-Range": f"bytes {ini}-{fim}/{tam}"}, timeout=600)
                if rr.status_code not in (200, 201, 206):
                    raise RuntimeError(f"upload parte {i + 1}: {rr.status_code} {rr.text[:200]}")
    return pid + (" (na caixa de entrada do app: toque em publicar)" if env("TIKTOK_MODO") != "direto" else "")


REDES = {"instagram": instagram, "facebook": facebook, "tiktok": tiktok}


def publicar():
    agenda = json.load(open(AGENDA, encoding="utf8")) if os.path.exists(AGENDA) else []
    agora = dt.datetime.now(dt.timezone.utc); feitos = []
    for item in agenda:
        if dt.datetime.fromisoformat(item["quando"]) > agora:
            continue
        st = item.setdefault("status", {})
        for rede in item.get("redes", []):
            if str(st.get(rede, "")).startswith("ok"):
                continue
            if str(st.get(rede, "")).count("erro") >= 3:  # tentou 3 vezes: para de insistir e avisa
                continue
            try:
                st[rede] = "ok:" + str(REDES[rede](item)); feitos.append(f"{item['id']} → {rede}")
            except Exception as e:
                st[rede] = (st.get(rede, "") + " erro: " + str(e)[:200]).strip()
                nota(f"Falha {rede}", f"{item['id']}: {str(e)[:400]}", "warning")
    json.dump(agenda, open(AGENDA, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    nota("Redes", ("publicados: " + "; ".join(feitos)) if feitos else "nada na hora de publicar")


def testar():
    tok = env("META_PAGE_TOKEN")
    if tok:
        for alvo, campos in ((env("META_PAGE_ID"), "name,followers_count"), (env("META_IG_ID"), "username,followers_count,media_count")):
            if alvo:
                nota("Meta", requests.get(f"{G}/{alvo}", params={"fields": campos, "access_token": tok}, timeout=60).json())
        nota("Meta token", requests.get(f"{G}/debug_token", params={"input_token": tok, "access_token": tok}, timeout=60).json().get("data", {}))
    else:
        nota("Meta", "sem META_PAGE_TOKEN", "warning")
    if env("TIKTOK_REFRESH_TOKEN"):
        try:
            t = tiktok_token()
            nota("TikTok", requests.post(f"{TT}/post/publish/creator_info/query/", headers={"Authorization": f"Bearer {t}"}, timeout=60).json())
        except Exception as e:
            nota("TikTok", str(e), "warning")
    else:
        nota("TikTok", "sem TIKTOK_REFRESH_TOKEN", "warning")


if __name__ == "__main__":
    {"publicar": publicar, "testar": testar}[sys.argv[1] if len(sys.argv) > 1 else "publicar"]()

"""Tira um vídeo do lançamento (chamado pelo botão "Tirar do lançamento" do painel, via issue do GitHub).

python -m fabrica.cancelar <id>
  <id> = nome na fábrica (ex.: garoto_short1, americanas_serie2), id de vídeo do YouTube, ou id da agenda das redes.

- YouTube (Custo Oculto, Hidden Cost, Vini QA): vídeo fica PRIVADO e sem data (nada é apagado).
- Instagram/Facebook/TikTok (agenda_redes.json): sai da agenda (status "cancelado").
Para voltar, é só reagendar depois (nada se perde).
"""
import json
import os
import sys

import requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Y = "https://www.googleapis.com/youtube/v3"


def token(var):
    r = requests.post("https://oauth2.googleapis.com/token", timeout=30, data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ[var], "grant_type": "refresh_token"})
    r.raise_for_status()
    return r.json()["access_token"]


def privado(video_id, var):
    H = {"Authorization": f"Bearer {token(var)}"}
    v = requests.get(f"{Y}/videos", headers=H, params={"part": "status", "id": video_id}, timeout=30).json().get("items") or []
    if not v:
        return "vídeo não encontrado no YouTube"
    st = v[0]["status"]
    if st.get("privacyStatus") == "public":
        return "já está PÚBLICO: não mexi (tire manualmente no Studio se quiser)"
    novo = {k: st[k] for k in ("license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia") if k in st}
    novo.update({"privacyStatus": "private", "publishAt": None})
    r = requests.put(f"{Y}/videos?part=status", headers=H, json={"id": video_id, "status": novo}, timeout=30)
    return "YouTube: privado e sem data" if r.status_code == 200 else f"YouTube falhou: {r.status_code} {r.text[:200]}"


def main(alvo):
    alvo = alvo.strip(); feitos = []
    # Custo Oculto / Hidden Cost
    reg_p = os.path.join(RAIZ, "publicados.json"); reg = json.load(open(reg_p, encoding="utf8"))
    for r in reg:
        if alvo in (r.get("nome"), r.get("video_id")) and r.get("video_id"):
            var = "YT_REFRESH_TOKEN_EN" if (r.get("idioma") or "pt").startswith("en") else "YT_REFRESH_TOKEN"
            msg = privado(r["video_id"], var); feitos.append(f"{r['nome']}: {msg}")
            if "privado e sem data" in msg:
                r.pop("publishAt", None); r["status"] = "private"; r["cancelado"] = True
    json.dump(reg, open(reg_p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    # Vini QA
    vq_p = os.path.join(RAIZ, "publicados_viniqa.json")
    if os.path.exists(vq_p):
        vq = json.load(open(vq_p, encoding="utf8"))
        for r in vq:
            if alvo in (r.get("video_id"), os.path.splitext(r.get("arquivo", ""))[0]):
                msg = privado(r["video_id"], "YT_REFRESH_TOKEN_QA"); feitos.append(f"Vini QA {r['titulo'][:50]}: {msg}")
                if "privado e sem data" in msg:
                    r["publishAt"] = None; r["cancelado"] = True
        json.dump(vq, open(vq_p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    # Instagram / Facebook / TikTok
    ag_p = os.path.join(RAIZ, "agenda_redes.json")
    if os.path.exists(ag_p):
        ag = json.load(open(ag_p, encoding="utf8"))
        for it in ag:
            if it.get("id") == alvo:
                it["cancelado"] = True; it["quando"] = "2099-01-01T00:00:00-03:00"
                feitos.append(f"{alvo}: fora da agenda de {', '.join(it.get('redes', []))}")
        json.dump(ag, open(ag_p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    msg = " | ".join(feitos) or f"não achei '{alvo}' em nenhuma agenda"
    print(f"::notice title=Tirar do lançamento::{msg}", flush=True)
    open(os.path.join(RAIZ, ".resultado_cancelar.txt"), "w", encoding="utf8").write(msg)


if __name__ == "__main__":
    main(sys.argv[1])

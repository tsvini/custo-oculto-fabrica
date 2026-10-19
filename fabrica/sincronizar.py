"""Confere no YouTube quais vídeos do registro ainda existem (só leitura no YouTube).
Os que não existem mais (excluídos pelo Vinícius no Studio) ficam marcados como "excluido" no publicados.json,
saem da agenda do painel e nunca são reenviados."""
import json, os
import requests
from .publicar import token, REG, nota

Y = "https://www.googleapis.com/youtube/v3"


def existentes(ids, idioma):
    H = {"Authorization": f"Bearer {token(idioma)}"}; ok = {}
    for i in range(0, len(ids), 50):
        r = requests.get(f"{Y}/videos", headers=H, timeout=30, params={"part": "status", "id": ",".join(ids[i:i + 50])})
        r.raise_for_status()
        for it in r.json().get("items", []):
            ok[it["id"]] = it["status"]
    return ok


def main():
    reg = json.load(open(REG, encoding="utf8")); excl = []; mud = []
    for idioma in ("pt", "en"):
        rs = [r for r in reg if r.get("video_id") and ((r.get("idioma") or "pt")[:2] == idioma) and not r.get("excluido")]
        ok = existentes([r["video_id"] for r in rs], idioma)
        for r in rs:
            st = ok.get(r["video_id"])
            if st is None:
                r["excluido"] = True; r["status"] = "excluido"; r.pop("publishAt", None); excl.append(r["nome"])
            elif st.get("privacyStatus") == "private" and not st.get("publishAt") and r.get("publishAt"):
                r.pop("publishAt", None); r["status"] = "private"; mud.append(r["nome"])
            elif st.get("publishAt") and st["publishAt"] != r.get("publishAt"):
                r["status"] = st.get("privacyStatus")
    json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    nota("Excluídos no YouTube", f"{len(excl)}: {', '.join(excl)}"[:3900])
    nota("Privados sem data", f"{len(mud)}: {', '.join(mud)}"[:3900])


if __name__ == "__main__":
    main()

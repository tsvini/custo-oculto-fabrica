"""Busca fotos livres no Wikimedia Commons para escolher a dedo.

fotos/busca.txt: uma linha por busca, "rotulo | termo de busca".
Saída: previas/fotos_<rotulo>.jpg (folha de contato numerada) e fotos/<rotulo>.json (títulos exatos, licença, autor).
"""
import json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fabrica.midia import _commons_busca, LIVRE, UA_BOT
from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(RAIZ, "previas"), exist_ok=True)
for linha in open(os.path.join(RAIZ, "fotos", "busca.txt"), encoding="utf8"):
    if "|" not in linha:
        continue
    rot, termo = [x.strip() for x in linha.split("|", 1)]
    try:
        res = [r for r in _commons_busca(termo, 480) if r["mime"] == "image/jpeg" and LIVRE.match(r["lic"] or "")][:12]
    except Exception as e:
        print(f"::warning title={rot}::{e}"); continue
    json.dump(res, open(os.path.join(RAIZ, "fotos", rot + ".json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    W, H = 360, 240; folha = Image.new("RGB", (W * 4, (H + 46) * 3), (18, 18, 18)); d = ImageDraw.Draw(folha)
    for i, r in enumerate(res):
        x, y = (i % 4) * W, (i // 4) * (H + 46)
        try:
            req = urllib.request.Request(r["url"], headers={"User-Agent": UA_BOT}); tmp = "/tmp/_f.jpg"
            open(tmp, "wb").write(urllib.request.urlopen(req, timeout=30).read())
            im = Image.open(tmp).convert("RGB"); im.thumbnail((W, H)); folha.paste(im, (x, y))
        except Exception:
            pass
        d.text((x + 4, y + H + 2), f"#{i} {r['w']}x{r['h']} {r['lic'][:18]}", fill=(255, 210, 60))
        d.text((x + 4, y + H + 20), r["title"].replace("File:", "")[:52], fill=(230, 230, 230))
    folha.save(os.path.join(RAIZ, "previas", f"fotos_{rot}.jpg"), quality=82)
    print(f"::notice title=Fotos {rot}::{len(res)} livres para '{termo}'")

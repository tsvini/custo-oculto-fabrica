"""Baixa os logos de um projeto (projeto.json → "logos") para projetos/<nome>/midia/ e registra o resultado em logos.log.
Uso: python ferramentas/baixar_logos.py <projeto>. Arquivo em midia/ tem prioridade na geração, então o vídeo não depende do Commons."""
import json, os, sys, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fabrica import midia as M

nome = sys.argv[1]
pasta = os.path.join(M.RAIZ if hasattr(M, "RAIZ") else os.getcwd(), "projetos", nome)
pasta = pasta if os.path.isdir(pasta) else os.path.join(os.getcwd(), "projetos", nome)
p = json.load(open(os.path.join(pasta, "projeto.json"), encoding="utf8"))
dest_dir = os.path.join(pasta, "midia"); os.makedirs(dest_dir, exist_ok=True)
log = []


def api(params):
    url = M.COMMONS + "?" + urllib.parse.urlencode(dict(params, format="json"))
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": M.UA_BOT}), timeout=30) as r:
        return json.load(r)


for k, arq in M.coletar_logos(p).items():
    candidatos = [arq] if isinstance(arq, str) else list(arq)
    feito = False
    for c in candidatos:
        t = c if c.lower().startswith("file:") else "File:" + c
        j = api({"action": "query", "titles": t, "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": 1400, "iiextmetadatafilter": "LicenseShortName"})
        pg = next(iter((j.get("query") or {}).get("pages", {}).values()), {})
        ii = (pg.get("imageinfo") or [{}])[0]
        lic = M._limpa_html(((ii.get("extmetadata") or {}).get("LicenseShortName") or {}).get("value", ""))
        if "missing" in pg or not ii.get("url"):
            log.append(f"{k}: {t} não existe"); continue
        if not M.LIVRE.match(lic or ""):
            log.append(f"{k}: {t} licença não livre ({lic})"); continue
        d = os.path.join(dest_dir, k + ".png")
        M._baixa(ii.get("thumburl") or ii["url"], d, headers={"User-Agent": M.UA_BOT})
        from PIL import Image
        im = Image.open(d).convert("RGBA"); bb = im.getchannel("A").getbbox()
        (im.crop(bb) if bb else im).save(d)
        log.append(f"{k}: OK {pg.get('title')} · {lic}"); feito = True; break
    if not feito:  # procura pelo nome
        q = os.path.splitext(candidatos[0].split(":", 1)[-1])[0]
        j = api({"action": "query", "list": "search", "srnamespace": 6, "srlimit": 8, "srsearch": q})
        log.append(f"{k}: sugestões no Commons para '{q}': " + " | ".join(x["title"] for x in (j.get("query") or {}).get("search", [])))
open(os.path.join(dest_dir, "logos.log"), "w", encoding="utf8").write("\n".join(log) + "\n")
print("\n".join(log))

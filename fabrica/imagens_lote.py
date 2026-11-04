"""python -m fabrica.imagens_lote imagens/<arquivo>.json → imagens/<lote>/<chave>.jpg (Cloudflare FLUX, cota grátis)."""
import json, os, sys
from .midia import ia_imagens
arq = sys.argv[1]; lote = os.path.splitext(os.path.basename(arq))[0]
ia_imagens(json.load(open(arq, encoding="utf8")), os.path.join("imagens", lote), True, print)
print(f"::notice title=Imagens::{len(os.listdir(os.path.join('imagens', lote)))} prontas em imagens/{lote}")

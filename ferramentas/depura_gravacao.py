"""Grava as cenas de teste (gravar) como a fábrica faz e salva quadros pra conferir: dbg/."""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fabrica import midia as M
os.makedirs("dbg", exist_ok=True)
SAUCE = "https://www.saucedemo.com/"
cenas = [{"type": "tela", "media": "rec_teste", "url": SAUCE, "gravar": True, "acoes": [{"fill": ["#user-name", "standard_user"]}, {"click": "#login-button"}]},
         {"type": "editor", "navegador": {"media": "rec_nav", "url": SAUCE, "gravar": True, "acoes": [], "espera_inicio": 1800}}]
log = lambda m: print(m, flush=True)
M.gravacoes(cenas, "dbg", log)
with open("dbg/relatorio.txt", "w") as f:
    for k in ("rec_teste", "rec_nav"):
        p = f"dbg/{k}.mp4"
        if not os.path.exists(p):
            f.write(f"{k}: NAO EXISTE\n"); continue
        info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,nb_frames:format=duration", "-of", "json", p], capture_output=True, text=True).stdout
        f.write(f"{k}: {info}\n")
        for t in (0.5, 2, 4):
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", p, "-frames:v", "1", "-vf", "scale=640:-1", f"dbg/{k}_{t}.png"])
print(open("dbg/relatorio.txt").read())

"""Refaz só a sonoplastia de um vídeo já renderizado (sem renderizar a imagem de novo).
python -m fabrica.refazer_som <nome>   (ex.: kolynos_v3_short1)
Precisa de: <nome>_sem_som.mp4 no release "videos" (a fábrica sobe junto) e previas/eventos_<nome>.json.
"""
import json, os, subprocess, sys
from . import sonoplastia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(nome):
    ev = json.load(open(os.path.join(RAIZ, "previas", f"eventos_{nome}.json"), encoding="utf8"))
    src = os.path.join(RAIZ, nome + "_sem_som.mp4")
    subprocess.run(["gh", "release", "download", "videos", "-p", nome + "_sem_som.mp4", "-O", src, "--clobber"], check=True)
    sonoplastia.processar(src, ev["eventos"], ev.get("trilha"), ev.get("roteiro", ""), os.path.join(RAIZ, "previas", f"som_{nome}.json"))
    os.replace(src, os.path.join(RAIZ, nome + ".mp4"))
    subprocess.run(["gh", "release", "upload", "videos", os.path.join(RAIZ, nome + ".mp4"), "--clobber"], check=True)


if __name__ == "__main__":
    main(sys.argv[1])

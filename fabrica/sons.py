"""Biblioteca de efeitos sonoros (gerada uma vez no ElevenLabs Sound Effects e guardada em motor/sons/).

python -m fabrica.sons            → gera só os que faltam
python -m fabrica.sons whoosh,boom → refaz esses
"""
import os
import sys

import requests

PASTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor", "sons")

# nome: (descrição para o gerador, segundos)
SONS = {
    "whoosh": ("fast punchy cinematic whoosh swoosh transition, clean, no music", 1.0),
    "boom": ("viral vine boom sound effect, deep bass boom hit, meme sound", 1.5),
    "impacto": ("huge cinematic trailer impact hit, deep sub bass drop with short reverb tail", 2.0),
    "caixa": ("old cash register ka-ching with coins rattling and bell ring", 1.3),
    "carimbo": ("heavy rubber stamp slammed hard on paper on a wooden desk, single hit", 0.8),
    "subida": ("tension riser building up suspense, rising whoosh and strings, ends abruptly", 2.5),
    "scratch": ("vinyl record scratch stop sound effect, comedic freeze", 1.0),
    "dun": ("dramatic dun dun duuun orchestral sting, suspense reveal", 2.5),
    "clique": ("camera shutter click, single photo snap", 0.6),
    "ding": ("smartphone notification ding, clean bright", 0.8),
    "trilha_trap": ("modern viral TikTok documentary background beat, dark trap, crisp hi-hats, deep 808 bass, mysterious piano melody, 90 BPM, catchy, loopable, no vocals", 22.0),
    "trilha_lofi": ("catchy lo-fi hip hop beat for storytelling shorts, punchy drums, warm bass, nostalgic electric piano, 85 BPM, upbeat but chill, loopable, no vocals", 22.0),
    "trilha_epica": ("energetic cinematic hybrid beat for viral business story videos, driving drums, pulsing synth bass, strings stabs, building tension, 100 BPM, loopable, no vocals", 22.0),
    "trilha_tensao": ("dark suspenseful documentary background music, low pulsing synth bass, soft ticking clock, steady tempo, no melody, loopable", 20.0),
}


def gerar(nome):
    texto, dur = SONS[nome]
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers={"xi-api-key": os.environ["ELEVENLABS_KEY"]},
                      json={"text": texto, "duration_seconds": dur, "prompt_influence": 0.6}, timeout=180)
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code} {r.text[:200]}")
    os.makedirs(PASTA, exist_ok=True)
    with open(os.path.join(PASTA, nome + ".mp3"), "wb") as f:
        f.write(r.content)


def creditos():
    try:
        s = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": os.environ["ELEVENLABS_KEY"]}, timeout=30).json()
        return s["character_limit"] - s["character_count"]
    except Exception:
        return None


def main():
    refazer = set(sys.argv[1].split(",")) if len(sys.argv) > 1 and sys.argv[1] else set()
    antes = creditos(); feitos = []
    for nome in SONS:
        if nome in refazer or not os.path.exists(os.path.join(PASTA, nome + ".mp3")):
            try:
                gerar(nome); feitos.append(nome); print(f"  som {nome}: ok", flush=True)
            except Exception as e:
                print(f"::warning title=Som {nome}::{str(e)[:300]}", flush=True)
    depois = creditos()
    gasto = f", gastou {antes - depois} créditos (restam {depois})" if antes is not None and depois is not None else ""
    print(f"::notice title=Biblioteca de sons::gerados: {', '.join(feitos) or 'nenhum'}{gasto}", flush=True)


if __name__ == "__main__":
    main()

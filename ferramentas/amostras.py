"""Gera amostras das vozes abertas (grátis, rodam no próprio servidor) para comparar."""
import os, subprocess, sys, urllib.request, wave

TXT = ("Durante décadas, mais da metade da pasta de dente vendida no Brasil tinha a mesma marca. "
       "A caixinha verde e amarela estava em quase todo banheiro do país. "
       "E então, em mil novecentos e noventa e sete, ela simplesmente sumiu das prateleiras. "
       "Não faliu. Não teve escândalo. Não perdeu clientes.")
OUT = "amostras"; os.makedirs(OUT, exist_ok=True)
HF = "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR"
ok = []


def mp3(wav, nome):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "160k", f"{OUT}/{nome}.mp3"], check=True)
    os.remove(wav); ok.append(nome)


# Piper
from piper import PiperVoice
for v in ["faber-medium", "cadu-medium", "jeff-medium", "edresson-low"]:
    nome = f"pt_BR-{v}"; spk, q = v.rsplit("-", 1)
    try:
        for ext in (".onnx", ".onnx.json"):
            if not os.path.exists(nome + ext):
                urllib.request.urlretrieve(f"{HF}/{spk}/{q}/{nome}{ext}", nome + ext)
        voz = PiperVoice.load(nome + ".onnx")
        with wave.open("t.wav", "wb") as w:
            if hasattr(voz, "synthesize_wav"):
                voz.synthesize_wav(TXT, w)
            else:
                voz.synthesize(TXT, w)
        mp3("t.wav", "piper_" + spk)
    except Exception as e:
        print(f"::warning title=Piper {v}::{type(e).__name__}: {e}"[:900])

# Kokoro
try:
    from kokoro import KPipeline
    import numpy as np, soundfile as sf
    pipe = KPipeline(lang_code="p")
    for v in ["pm_alex", "pm_santa", "pf_dora"]:
        try:
            audio = np.concatenate([np.asarray(a) for _, _, a in pipe(TXT, voice=v, speed=1.0)])
            sf.write("t.wav", audio, 24000); mp3("t.wav", "kokoro_" + v)
        except Exception as e:
            print(f"::warning title=Kokoro {v}::{type(e).__name__}: {e}"[:900])
except Exception as e:
    print(f"::warning title=Kokoro::{type(e).__name__}: {e}"[:900])

print(f"::notice title=Amostras geradas::{', '.join(ok) or 'nenhuma'}")
sys.exit(0 if ok else 1)

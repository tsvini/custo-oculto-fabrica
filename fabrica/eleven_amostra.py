"""Amostra curta da mesma frase em vários modelos do ElevenLabs (amostras/eleven.txt → amostras/eleven_<modelo>.mp3)."""
import os, requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.elevenlabs.io"


def main():
    H = {"xi-api-key": os.environ["ELEVENLABS_KEY"].strip()}
    linhas = open(os.path.join(RAIZ, "amostras", "eleven.txt"), encoding="utf8").read().strip().split("\n")
    voz, modelos, textos = linhas[0].strip(), linhas[1].split(), [l.strip() for l in linhas[2:] if l.strip()]
    vs = requests.get(f"{API}/v1/voices", headers=H, timeout=60).json().get("voices", [])
    v = next(x for x in vs if x["name"].lower().startswith(voz.lower()))
    print(f"::notice title=Voz::{v['name']}")
    for m, (k, texto) in [(m, kt) for m in modelos for kt in enumerate(textos, 1)]:
        r = requests.post(f"{API}/v1/text-to-speech/{v['voice_id']}?output_format=mp3_44100_128", headers=H, timeout=300, json={"text": texto, "model_id": m})
        if r.status_code != 200:
            print(f"::warning title={m}::{r.status_code} {r.text[:200]}"); continue
        arq = os.path.join(RAIZ, "amostras", f"eleven_{m}_{k}.mp3"); open(arq, "wb").write(r.content)
        print(f"::notice title=Amostra::{m} ok")
        try:  # transcreve: se a tag de emoção ([excited]...) for lida em voz alta, aparece aqui
            from faster_whisper import WhisperModel
            segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(arq, language="pt")
            import subprocess
            dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout.strip()
            print(f"::notice title=Amostra {k} {m} ({dur}s)::" + " | ".join(f"[{x.start:.1f}-{x.end:.1f}] {x.text.strip()}" for x in segs))
        except Exception as e:
            print(f"::warning title=Transcrição::{e}")


if __name__ == "__main__":
    main()

"""Amostra curta da mesma frase em vários modelos do ElevenLabs (amostras/eleven.txt → amostras/eleven_<modelo>.mp3)."""
import os, requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.elevenlabs.io"


def main():
    H = {"xi-api-key": os.environ["ELEVENLABS_KEY"].strip()}
    linhas = open(os.path.join(RAIZ, "amostras", "eleven.txt"), encoding="utf8").read().strip().split("\n")
    voz, modelos, texto = linhas[0].strip(), linhas[1].split(), " ".join(linhas[2:]).strip()
    vs = requests.get(f"{API}/v1/voices", headers=H, timeout=60).json().get("voices", [])
    v = next(x for x in vs if x["name"].lower().startswith(voz.lower()))
    print(f"::notice title=Voz::{v['name']}")
    for m in modelos:
        r = requests.post(f"{API}/v1/text-to-speech/{v['voice_id']}?output_format=mp3_44100_128", headers=H, timeout=300, json={"text": texto, "model_id": m})
        if r.status_code != 200:
            print(f"::warning title={m}::{r.status_code} {r.text[:200]}"); continue
        open(os.path.join(RAIZ, "amostras", f"eleven_{m}.mp3"), "wb").write(r.content)
        print(f"::notice title=Amostra::{m} ok")


if __name__ == "__main__":
    main()

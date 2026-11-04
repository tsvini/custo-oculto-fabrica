"""Gera na ElevenLabs as narrações de narracoes/*.txt que ainda não têm .mp3 (voz do Vinícius, eleven_v4).
Confere o saldo antes: se não der para todas, não gera nenhuma e avisa."""
import glob, os, subprocess, sys, requests

API = "https://api.elevenlabs.io"
VOZ = "DvaR4JBPwbssaWwbSJ47"
AJ = {"stability": 0.5, "similarity_boost": 0.75, "speed": 1.0}


def nota(t, m, n="notice"):
    print(f"::{n} title={t}::{m}", flush=True)


def main():
    H = {"xi-api-key": os.environ["ELEVENLABS_KEY"].strip()}
    modelo = sys.argv[1] if len(sys.argv) > 1 else "eleven_v4"
    fila = [f for f in sorted(glob.glob("narracoes/*.txt")) if not os.path.exists(f[:-4] + ".mp3")]
    total = sum(len(open(f, encoding="utf8").read().strip()) for f in fila)
    s = requests.get(f"{API}/v1/user/subscription", headers=H, timeout=60).json()
    resta = s.get("character_limit", 0) - s.get("character_count", 0)
    nota("Saldo", f"{len(fila)} narrações, {total} caracteres; saldo {resta} créditos (modelo {modelo})")
    if total > resta:
        nota("Sem saldo", f"faltam {total - resta} créditos; nada foi gerado", "warning"); return
    for f in fila:
        txt = open(f, encoding="utf8").read().strip()
        r = requests.post(f"{API}/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128", headers=H, timeout=600,
                          json={"text": txt, "model_id": modelo, "voice_settings": AJ})
        if r.status_code != 200:
            nota("Erro", f"{f}: {r.status_code} {r.text[:200]}", "warning"); continue
        open(f[:-4] + ".mp3", "wb").write(r.content)
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f[:-4] + ".mp3"],
                           capture_output=True, text=True).stdout.strip()
        nota("Narração", f"{os.path.basename(f)[:-4]}: {float(d):.1f} s" if d else os.path.basename(f))


if __name__ == "__main__":
    main()

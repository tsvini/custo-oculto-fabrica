"""python -m fabrica.transcrever <nome> [modelo] → legendas/<nome>.json com [início, fim, palavra]."""
import json, sys, traceback
try:
    from faster_whisper import WhisperModel
    n = sys.argv[1]; mod = sys.argv[2] if len(sys.argv) > 2 else "large-v3"
    m = WhisperModel(mod, device="cpu", compute_type="int8")
    import wave, numpy as np
    w = wave.open(f"legendas/{n}.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language="pt", word_timestamps=True, beam_size=5)
    out = [[round(w.start, 2), round(w.end, 2), w.word.strip()] for s in segs for w in s.words]
    json.dump(out, open(f"legendas/{n}.json", "w"), ensure_ascii=False)
    print("::notice title=Transcrição::" + " ".join(w[2] for w in out)[:3500])
except Exception:
    print("::error title=Transcrição::" + traceback.format_exc().replace("\n", " | ")[-3000:]); sys.exit(1)

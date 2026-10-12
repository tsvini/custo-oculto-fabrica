"""Narração gravada pelo Vinícius: usa os áudios enviados e descobre o tempo de cada frase.

Arquivos em projetos/<nome>/audio/:
  parte1.mp3 … parteN.mp3  → vídeo longo (uma por parte do roteiro)
  short1.mp3, short2.mp3…  → Shorts
Aceita mp3, wav, m4a, ogg, aac, flac, opus.

O tempo de cada frase vem do reconhecimento de fala (faster-whisper) alinhado ao texto
do roteiro. Palavra que não bate (número falado diferente, nome estrangeiro) é interpolada.
"""
import difflib, os, re, subprocess, tempfile, unicodedata
import numpy as np
from .tts import SR, _np_to_wav, _wav_to_np

EXTS = (".mp3", ".wav", ".m4a", ".ogg", ".aac", ".flac", ".opus", ".webm")
_MODELO = None


def achar_audio(pasta, base):
    if not os.path.isdir(pasta):
        return None
    for fn in sorted(os.listdir(pasta)):
        nome, ext = os.path.splitext(fn)
        n = nome.lower().replace(" ", "").replace("_", "").replace("-", "").replace("shorts", "short").replace("parte0", "parte")
        if ext.lower() in EXTS and n == base:
            return os.path.join(pasta, fn)
    return None


def _carregar(path):
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", wav], check=True)
        with open(wav, "rb") as f:
            return _wav_to_np(f.read())


def _norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def _palavras(path):
    global _MODELO
    if _MODELO is None:
        from faster_whisper import WhisperModel
        _MODELO = WhisperModel(os.environ.get("WHISPER_MODELO", "small"), device="cpu", compute_type="int8")
    segs, _ = _MODELO.transcribe(path, language="pt", word_timestamps=True, vad_filter=False, beam_size=5)
    out = []
    for s in segs:
        for w in s.words or []:
            n = _norm(w.word)
            if n:
                out.append((n, float(w.start), float(w.end)))
    return out


def _tempos(frases, ouvidas, dur):
    roteiro = []  # (palavra, índice da frase)
    for i, f in enumerate(frases):
        for w in f.split():
            n = _norm(w)
            if n:
                roteiro.append((n, i))
    N = len(roteiro)
    ini = [None] * N; fim = [None] * N
    sm = difflib.SequenceMatcher(None, [w for w, _ in roteiro], [w for w, _, _ in ouvidas], autojunk=False)
    for a, b, k in sm.get_matching_blocks():
        for j in range(k):
            ini[a + j], fim[a + j] = ouvidas[b + j][1], ouvidas[b + j][2]
    casadas = sum(x is not None for x in ini)
    # interpola as palavras que não casaram entre as âncoras vizinhas
    t0 = ouvidas[0][1] if ouvidas else 0.0
    t1 = ouvidas[-1][2] if ouvidas else dur
    anc = [(-1, t0, t0)] + [(i, ini[i], fim[i]) for i in range(N) if ini[i] is not None] + [(N, t1, t1)]
    for (ia, _, fa), (ib, sb, _) in zip(anc, anc[1:]):
        gap = ib - ia - 1
        for j in range(1, gap + 1):
            t = fa + (sb - fa) * (j - 0.5) / gap
            ini[ia + j] = t; fim[ia + j] = t
    tempos = []
    for i in range(len(frases)):
        idx = [k for k in range(N) if roteiro[k][1] == i]
        a = ini[idx[0]] if idx else (tempos[-1][1] if tempos else t0)
        b = fim[idx[-1]] if idx else a
        tempos.append([a, max(a + 0.3, b)])
    for i in range(1, len(tempos)):  # sem sobreposição, sempre em ordem
        if tempos[i][0] < tempos[i - 1][1]:
            meio = (tempos[i][0] + tempos[i - 1][1]) / 2
            tempos[i - 1][1] = max(tempos[i - 1][0] + 0.2, meio); tempos[i][0] = tempos[i - 1][1]
        tempos[i][1] = max(tempos[i][1], tempos[i][0] + 0.2)
    return tempos, casadas / max(1, N)


def parte(frases, audio, saida_wav, log=print):
    lead = 0.15
    x = _carregar(audio)
    try:
        ouvidas = _palavras(audio)
    except Exception as e:
        log(f"    reconhecimento de fala falhou ({e}); tempos por tamanho de frase")
        ouvidas = []
    dur = len(x) / SR
    if ouvidas:
        tempos, taxa = _tempos(frases, ouvidas, dur)
    else:
        tot = sum(len(f) for f in frases) or 1; t = 0.0; tempos = []; taxa = 0.0
        for f in frases:
            d = dur * len(f) / tot; tempos.append([t, t + d]); t += d
    y = np.concatenate([np.zeros(int(lead * SR), np.float32), x, np.zeros(int(0.25 * SR), np.float32)])
    # volume uniforme, igual à voz sintética
    win = SR // 100; n = len(y) // win
    rms = np.sqrt((y[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    fala = rms[20 * np.log10(rms) > -45]
    if len(fala):
        y = y * (10 ** (-18 / 20) / np.sqrt((fala ** 2).mean()))
        a = np.abs(y); m = a > 0.7
        y[m] = np.sign(y[m]) * (0.7 + 0.2 * np.tanh((a[m] - 0.7) / 0.2))
    _np_to_wav(y.astype(np.float32), saida_wav)
    tempos = [[round(a + lead, 3), round(b + lead, 3)] for a, b in tempos]
    return tempos, len(y) / SR, taxa

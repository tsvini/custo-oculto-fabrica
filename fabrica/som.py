"""Desenho de som dos Shorts: trilha de tensão e efeitos (whoosh, impacto, caixa registradora, carimbo, subida).

Tudo sintetizado aqui com numpy (sem banco de áudio, sem licença, sem custo).
mixar(video, sons, trilha) lê a narração do MP4, põe a trilha por baixo (abaixando quando a voz fala)
e os efeitos nos tempos marcados nas cenas ("sfx"), e troca o áudio do vídeo.
"""
import os
import subprocess
import tempfile

import numpy as np

SR = 48000


def _env(n, a=0.005, r=0.3):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(r, 1e-4))
    return e


def _lp(x, k):  # passa-baixa simples (média móvel exponencial)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += k * (x[i] - acc); y[i] = acc
    return y


def _ruido(n, seed=1):
    return np.random.default_rng(seed).standard_normal(n)


def whoosh(d=0.55):
    n = int(SR * d); t = np.arange(n) / SR
    x = _ruido(n, 3)
    # varredura: filtro abre e fecha
    k = 0.02 + 0.25 * np.sin(np.pi * t / d) ** 2
    y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += k[i] * (x[i] - acc); y[i] = acc
    y = y - _lp(y, 0.01)
    return 0.9 * y / (np.abs(y).max() + 1e-9) * np.sin(np.pi * t / d) ** 1.5


def impacto(d=1.2):
    n = int(SR * d); t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t * 18)  # queda de afinação
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    clique = _lp(_ruido(n, 5), 0.3) * np.exp(-t * 40) * 0.6
    y = sub + clique
    return 0.95 * y / (np.abs(y).max() + 1e-9)


def caixa(d=0.9):  # "ka-ching"
    n = int(SR * d); t = np.arange(n) / SR
    ka = _lp(_ruido(n, 7), 0.5) * np.exp(-t * 60) * 0.7
    sino = np.zeros(n)
    for f, a in ((2093, 1.0), (2637, 0.7), (3136, 0.5), (4186, 0.3)):
        ini = int(0.08 * SR); tt = np.maximum(0, t - 0.08)
        s = a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 5) * (t >= 0.08)
        sino += s
    y = ka + 0.35 * sino
    return 0.9 * y / (np.abs(y).max() + 1e-9)


def carimbo(d=0.6):
    n = int(SR * d); t = np.arange(n) / SR
    baque = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 22)
    tapa = _lp(_ruido(n, 9), 0.6) * np.exp(-t * 55)
    y = baque + 0.8 * tapa
    return 0.95 * y / (np.abs(y).max() + 1e-9)


def subida(d=1.6):  # riser que termina no corte
    n = int(SR * d); t = np.arange(n) / SR
    x = _ruido(n, 11)
    k = 0.01 + 0.4 * (t / d) ** 2
    y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += k[i] * (x[i] - acc); y[i] = acc
    tom = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * 0.25
    y = (y / (np.abs(y).max() + 1e-9) + tom) * (t / d) ** 2
    return 0.8 * y / (np.abs(y).max() + 1e-9)


EFEITOS = {"whoosh": whoosh, "impacto": impacto, "caixa": caixa, "carimbo": carimbo, "subida": subida}


def trilha_tensao(dur, bpm=84):
    """Base escura: drone grave com batida de coração e um pulso agudo discreto."""
    n = int(SR * dur); t = np.arange(n) / SR
    drone = (np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 82.4 * t) + 0.3 * np.sin(2 * np.pi * 110 * t + 0.5 * np.sin(2 * np.pi * 0.2 * t)))
    drone *= 0.55 + 0.45 * np.sin(2 * np.pi * 0.11 * t) ** 2
    ar = _lp(_ruido(n, 13), 0.004) * 6
    y = 0.5 * drone + 0.25 * ar
    batida = 60 / bpm
    for k in range(int(dur / batida) + 1):
        for off, a in ((0, 1.0), (0.22, 0.6)):  # tum-tum
            i = int((k * batida + off) * SR)
            if i >= n:
                continue
            m = min(n - i, int(0.35 * SR)); tt = np.arange(m) / SR
            y[i:i + m] += a * 1.4 * np.sin(2 * np.pi * (45 + 40 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
    pulso = 60 / bpm / 2
    for k in range(int(dur / pulso)):
        i = int(k * pulso * SR); m = min(n - i, int(0.08 * SR)); tt = np.arange(m) / SR
        y[i:i + m] += 0.06 * np.sin(2 * np.pi * 1760 * tt) * np.exp(-tt * 60)
    fade = np.minimum(1, np.minimum(t / 1.5, (dur - t) / 1.2))
    return y * np.clip(fade, 0, 1) / (np.abs(y).max() + 1e-9)


PASTA_SONS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor", "sons")


def _arquivo(nome):
    """Som gravado da biblioteca (motor/sons/<nome>.mp3), se existir."""
    f = os.path.join(PASTA_SONS, nome + ".mp3")
    return _le(f) if os.path.exists(f) else None


def _le(video):
    with tempfile.NamedTemporaryFile(suffix=".f32", delete=False) as f:
        tmp = f.name
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", tmp], check=True)
    x = np.fromfile(tmp, dtype=np.float32).astype(np.float64); os.remove(tmp)
    return x


def mixar(video, sons, trilha=None, vol_trilha=0.16, vol_sfx=0.55):
    """sons: [(segundo, nome_do_efeito)]. Troca o áudio do MP4 pela mistura (voz + trilha com ducking + efeitos)."""
    if not sons and not trilha:
        return
    voz = _le(video); n = len(voz); dur = n / SR
    mix = voz.copy()
    if trilha:
        base = _arquivo("trilha_" + trilha) if isinstance(trilha, str) else None
        if base is not None and len(base) > SR:
            # repete a trilha gravada com cruzamento de 1s até cobrir o vídeo
            xf = SR; tr = base.copy()
            while len(tr) < n:
                rampa = np.linspace(0, 1, xf)
                tr = np.concatenate([tr[:-xf], tr[-xf:] * (1 - rampa) + base[:xf] * rampa, base[xf:]])
            tr = tr[:n] / (np.abs(base).max() + 1e-9)
            t = np.arange(n) / SR; tr *= np.clip(np.minimum(t / 1.0, (dur - t) / 1.2), 0, 1)
        else:
            tr = trilha_tensao(dur)[:n]
        # ducking: trilha abaixa quando a voz está forte
        env = np.sqrt(_lp(voz ** 2, 0.0008))
        env = env / (env.max() + 1e-9)
        duck = 1 - 0.55 * np.clip(env * 3, 0, 1)
        mix += vol_trilha * tr * duck
    for seg, nome in sons or []:
        s = _arquivo(nome)
        if s is None:
            f = EFEITOS.get(nome)
            if not f:
                continue
            s = f()
        else:
            s = 0.9 * s / (np.abs(s).max() + 1e-9)
        i = int(max(0, seg) * SR)
        if nome == "subida":
            i = max(0, i - len(s))  # a subida termina no ponto marcado
        if i >= n:
            continue
        m = min(len(s), n - i); mix[i:i + m] += vol_sfx * s[:m]
    pico = np.abs(mix).max()
    if pico > 0.98:
        mix *= 0.98 / pico
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.f32"); mix.astype(np.float32).tofile(wav)
        out = os.path.join(d, "v.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", wav,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
        os.replace(out, video)

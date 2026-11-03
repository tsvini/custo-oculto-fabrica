"""Legendas .vtt das aulas do Playwright para Leigos, para subir na Udemy.

Ouve o MP4 final (o mesmo que está na Udemy), acha o tempo de cada palavra com o faster-whisper
e escreve o texto EXATO do roteiro (getByRole, npx... com a grafia certa). Palavra que o whisper
ouviu diferente é interpolada entre as vizinhas, igual na fábrica.

Uso: python -m ferramentas.legendas_udemy video.mp4 NN saida.vtt"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fabrica.alinhar import _palavras, _tempos  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX = 84  # duas linhas de 42


def _ts(t):
    t = max(0.0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def _linhas(txt):
    if len(txt) <= 42:
        return txt
    meio = len(txt) // 2
    esp = [i for i, c in enumerate(txt) if c == " "]
    # corta perto do meio, de preferência logo depois de uma pontuação
    i = min(esp, key=lambda k: abs(k - meio) - (14 if txt[k - 1] in ".,:;?!" else 0))
    return txt[:i] + "\n" + txt[i + 1:]


def _blocos(palavras):
    """quebra a frase em blocos de até MAX caracteres, preferindo cortar depois de pontuação"""
    out, cur = [], []
    for w in palavras:
        if cur and len(" ".join(x[0] for x in cur + [w])) > MAX:
            # volta até a última pontuação do bloco, se houver uma razoável
            cut = max((k for k in range(len(cur)) if re.search(r"[.,:;?!]$", cur[k][0]) and k >= len(cur) // 2), default=None)
            if cut is not None and cut < len(cur) - 1:
                out.append(cur[:cut + 1]); cur = cur[cut + 1:]
            else:
                out.append(cur); cur = []
        cur.append(w)
        if re.search(r"[.?!]$", w[0]) and len(" ".join(x[0] for x in cur)) > 30:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def gerar(mp4, n, saida):
    p = json.load(open(os.path.join(RAIZ, "projetos", f"curso-playwright-{n:02d}", "projeto.json"), encoding="utf8"))
    frases = [s["text"] for s in p["script"]["long"]["parts"][0]["sentences"] if s.get("text", "").strip()]
    ouvidas = _palavras(mp4)
    dur = ouvidas[-1][2] if ouvidas else 0
    _, taxa, palavras = _tempos(frases, ouvidas, dur)
    cues = []
    for lst in palavras:
        for b in _blocos(lst):
            cues.append([b[0][1], b[-1][2] + 0.35, " ".join(w[0] for w in b)])
    for i in range(len(cues) - 1):  # sem sobreposição
        cues[i][1] = min(cues[i][1], cues[i + 1][0] - 0.02)
        cues[i][1] = max(cues[i][1], cues[i][0] + 0.6)
        if cues[i + 1][0] < cues[i][1]:
            cues[i + 1][0] = cues[i][1] + 0.02
    with open(saida, "w", encoding="utf8") as f:
        f.write("WEBVTT\n\n")
        for k, (a, b, t) in enumerate(cues, 1):
            f.write(f"{k}\n{_ts(a)} --> {_ts(max(b, a + 0.6))}\n{_linhas(t)}\n\n")
    print(f"aula {n:02d}: {len(cues)} legendas, {taxa:.0%} das palavras casaram com o áudio, fim {_ts(cues[-1][1]) if cues else '-'}", flush=True)
    return taxa


if __name__ == "__main__":
    gerar(sys.argv[1], int(sys.argv[2]), sys.argv[3])

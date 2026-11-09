"""Montagem automática de um vídeo da série, sem escolhas manuais.
python -m fabrica.montar <pasta_trabalho> <serie g|j> <empresa> <roteiro.txt> <palavras.json> <narracao.mp3> <encerramento.mp4> <saida.mp4> [musica.mp3]
A pasta de trabalho precisa ter os clipes (clip_01.mp4, clipe_02.mp4 ... em ordem pelo número).
Faz: legenda karaokê, efeitos escolhidos pelas regras abaixo, clipes distribuídos pela fala,
música abaixando sob a voz, encerramento sem som e volume no padrão das redes."""
import difflib, glob, json, os, re, subprocess, sys, unicodedata
from . import efeitos as fx

GOLD = "&H003DC8FF&"; WHITE = "&H00FFFFFF&"
CARIMBOS = {"falência": "FALÊNCIA", "faliu": "FALIU", "faliram": "FALIRAM", "vendida": "VENDIDA", "vendido": "VENDIDO",
            "recusou": "RECUSOU", "fechou": "FECHOU", "fecharam": "FECHARAM", "desligado": "DESLIGADO", "enterrou": "ENTERRADO",
            "prejuízo": "PREJUÍZO", "aluguel": "ALUGUEL", "cancelaram": "CANCELARAM", "perdeu": "PERDEU", "encalhou": "ENCALHOU",
            "abandonado": "ABANDONADO", "esquecido": "ESQUECIDO", "dívida": "DÍVIDA",
            "encalhe": "ENCALHE", "desabou": "DESABOU", "quebrou": "QUEBROU", "demitiu": "DEMITIU", "cortou": "CORTOU", "desistiu": "NÃO DESISTIU", "lucrou": "LUCROU"}
NUMPAL = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9,
          "dez": 10, "onze": 11, "doze": 12, "quinze": 15, "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60,
          "setenta": 70, "oitenta": 80, "noventa": 90, "cem": 100, "cento": 100, "duzentos": 200, "trezentos": 300, "quatrocentos": 400,
          "quinhentos": 500, "seiscentos": 600, "setecentos": 700, "oitocentos": 800, "novecentos": 900}
MOEDA = {"dólares": "US$ ", "reais": "R$ ", "euros": "€ "}


def num_extenso(ws, i):
    """'mil e trezentos cartuchos' -> (1300, palavras usadas, unidade/rótulo) ou None; exige 'mil' ou mais"""
    tot = cur = 0; j = i; viu_mil = False
    while j < len(ws):
        t = ws[j][2].rstrip(".,?!:;").lower()
        if t in NUMPAL: cur += NUMPAL[t]
        elif t == "mil": cur = (cur or 1) * 1000; tot += cur; cur = 0; viu_mil = True
        elif t in ("milhão", "milhões"): cur = (cur or 1) * 10**6; tot += cur; cur = 0; viu_mil = True
        elif t == "e" and j > i: pass
        else: break
        j += 1
        if re.search(r"[.,?!:;]$", ws[j - 1][2]): break
    while j > i and ws[j - 1][2].rstrip(".,").lower() == "e": j -= 1
    v = tot + cur
    if not viu_mil or v < 1000 or j - i < 2: return None
    prox = ws[j][2].rstrip(".,?!:;").lower() if j < len(ws) and not re.search(r"[.,?!:;]$", ws[j - 1][2]) else ""
    return v, j - i, prox
UNIDADES = {"anos": "ANOS", "mil": "MIL", "milhão": "MILHÃO", "milhões": "MILHÕES", "bilhão": "BILHÃO", "bilhões": "BILHÕES", "%": "%"}
COMUNS = set("A O As Os E Em Num Numa No Na Nos Nas Mas Isso Era Hoje Depois Essa Esse Uma Um Para Por Com De Do Da Quando Você Nós Ele Ela Foi Só Venda Perdeu Inventou Mostrou Voltou Continuou Tinha".split()) | {"Nos","Num","Numa","Em","E"}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def corrige(ws, roteiro):
    """usa a grafia e as palavras do roteiro; trechos que o whisper errou são redistribuídos no tempo"""
    rt = roteiro.split()
    a = [norm(w[2]) for w in ws]; b = [norm(t) for t in rt]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and (i2 - i1) == (j2 - j1)):
            for k in range(i2 - i1):
                out.append([ws[i1 + k][0], ws[i1 + k][1], rt[j1 + k]])
        elif tag == "replace" and (i2 - i1) == 1 and re.search(r"\d", ws[i1][2]):
            out.append(list(ws[i1]))  # número/sigla que o roteiro escreve por extenso (ex.: 3M)
        elif tag == "replace" or (tag == "insert" and out):
            t0 = ws[i1][0] if i1 < len(ws) and tag == "replace" else out[-1][1]
            t1 = ws[i2 - 1][1] if tag == "replace" else (ws[i1][0] if i1 < len(ws) else t0 + 0.3 * (j2 - j1))
            if t1 <= t0: t1 = t0 + 0.25 * (j2 - j1)
            n = j2 - j1; st = (t1 - t0) / n
            for k in range(n):
                out.append([t0 + k * st, t0 + (k + 1) * st, rt[j1 + k]])
        # delete: palavras que só o whisper ouviu são descartadas
    return out


def blocos(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        t = " ".join(x[2] for x in cur)
        if len(cur) == 3 or re.search(r"[.,?!:;]$", w[2]) or (len(cur) == 2 and len(t) > 15):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def ts(x):
    x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


def ass_karaoke(chs, dur, arq):
    ev = [f"Dialogue: 6,{ts(0)},{ts(dur)},Draw,,0,0,0,,{{\\pos(0,0)\\c{GOLD}\\clip(0,0,0,1920)\\t(0,{int(dur*1000)},\\clip(0,0,1080,1920))\\p1}}m 0 0 l 1080 0 l 1080 10 l 0 10{{\\p0}}"]
    for ci, ch in enumerate(chs):
        prox = chs[ci + 1][0][0] if ci + 1 < len(chs) else dur
        fim = min(prox, ch[-1][1] + 0.5)
        for wi, w in enumerate(ch):
            a = w[0] if wi else ch[0][0]; b = ch[wi + 1][0] if wi + 1 < len(ch) else fim
            partes = [(f"{{\\c{GOLD}\\fscx108\\fscy108}}{x[2].upper()}{{\\c{WHITE}\\fscx100\\fscy100}}" if j == wi else x[2].upper()) for j, x in enumerate(ch)]
            pop = "{\\fscx70\\fscy70\\t(0,90,\\fscx100\\fscy100)}" if wi == 0 else ""
            ev.append(f"Dialogue: 5,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\an5\\pos(540,1330)}}{pop}{' '.join(partes)}")
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Black,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,1,0,1,7,4,5,90,90,0,1
Style: Draw,Inter,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    open(arq, "w").write(hdr + "\n".join(ev) + "\n")


def frases(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r"[.?!]$", w[2]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def quebra(txt, n=22):
    linhas, l = [], ""
    for p in txt.split():
        if len(l) + len(p) + 1 > n and l: linhas.append(l); l = p
        else: l = (l + " " + p).strip()
    if l: linhas.append(l)
    return linhas


def escolhe_efeitos(ws, serie, empresa, dur):
    """regras automáticas -> lista (ini, fim, y, fn, modo, grupo)"""
    fr = frases(ws); inicio_frase = sorted(f[0][0] for f in fr)
    def prox_frase(t):
        for s in inicio_frase:
            if s > t + 0.3: return s
        return dur
    E = []
    st = lambda im: (lambda t: im)
    E.append((0.0, min(2.6, prox_frase(0)), 520, st(fx.tag(empresa.upper(), sub="O CUSTO DE SER GIGANTE" if serie == "g" else "A JOGADA QUE MUDOU TUDO")), "slide", 0))
    # fim: frase de assinatura / citação e pergunta
    fim_txt = None
    if serie == "g":
        for f in fr:
            if f[0][2].lower() == "o" and len(f) > 2 and norm(f[1][2]) == "custo":
                fim_txt = f
    else:
        for i, f in enumerate(fr):
            if norm(f[0][2]) == "foi" and i > 0 and "grande" in " ".join(norm(x[2]) for x in fr[i - 1]):
                fim_txt = fr[i - 1] + f
    reservado = fim_txt[0][0] if fim_txt else dur
    # três frases curtas antes do fim
    trio = []
    for i in range(len(fr) - 2):
        g = fr[i:i + 3]
        if all(len(x) <= 5 for x in g) and g[-1][-1][1] <= reservado + 0.5 and g[0][0][0] > dur * 0.5:
            trio = g
    usados = set(); pula = set()
    for i, w in enumerate(ws):
        a = w[0]
        if i in pula: continue
        if a >= reservado - 0.2 or (trio and trio[0][0][0] - 0.2 <= a): break
        t = w[2].rstrip(".,?!:;").strip("“”\"")
        lo = t.lower()
        fim = min(prox_frase(a), a + 2.8)
        if re.fullmatch(r"(18|19|20)\d\d", t):
            lab = None; ini = a
            if i >= 2 and E and E[-1][5] == 1 and E[-1][4] == "slide" and ws[i - 1][2].lower() == "de" \
                    and not re.search(r"[.,?!:;]$", ws[i - 2][2]) and abs(E[-1][0] - ws[i - 2][0]) < 0.05 and a - E[-1][0] < 1.5:
                lab = ws[i - 2][2].rstrip(".,").upper(); ini = E.pop()[0]  # 'Natal de 1982' -> 1982 com rótulo NATAL
            elif a < 2.0 and E and E[0][5] == 0:
                lab = empresa.upper(); E.pop(0); ini = 0.0  # ano logo na abertura: o nome da empresa vira o rótulo
            E.append((ini, max(fim, min(a + 1.8, dur)), 560, st(fx.num(t, 230, label=lab, branco=True)), "pop", 1)); continue
        ne = num_extenso(ws, i) if lo in NUMPAL or lo == "mil" else None
        if ne:
            v, n, prox = ne; pre = MOEDA.get(prox, ""); lab = None if pre or not prox or len(prox) > 10 else prox.upper()
            def cnt2(tt, v=v, pre=pre, lab=lab):
                k = min(1, tt / 0.8); x = round(v * (1 - (1 - k) ** 3))
                return fx.num(pre + f"{x:,}".replace(",", "."), 200, label=lab)
            E.append((a, min(prox_frase(a), a + 3.0), 560, cnt2, "pop", 1)); pula.update(range(i + 1, i + n)); continue
        if re.fullmatch(r"\d+", t) and i + 1 < len(ws) and ws[i + 1][2].rstrip(".,").lower() in MOEDA:
            pre = MOEDA[ws[i + 1][2].rstrip(".,").lower()]; v = int(t)
            def cnt3(tt, v=v, pre=pre):
                k = min(1, tt / 0.7); return fx.num(pre + f"{round(v * (1 - (1 - k) ** 3)):,}".replace(",", "."), 210)
            E.append((a, max(fim, min(a + 1.8, dur)), 560, cnt3, "pop", 1)); continue
        if re.fullmatch(r"\d+([.,]\d+)?", t) and i + 1 < len(ws) and ws[i + 1][2].rstrip(".,").lower() in UNIDADES:
            un = UNIDADES[ws[i + 1][2].rstrip(".,").lower()]; v = t.replace(".", "")
            try:
                alvo = float(v.replace(",", ".")); dec = "," in v
                def cnt(tt, alvo=alvo, un=un, dec=dec):
                    k = min(1, tt / 0.7); x = alvo * (1 - (1 - k) ** 3)
                    s = (f"{x:.1f}".replace(".", ",") if dec else f"{round(x)}")
                    return fx.num(f"{s} {un}" if un != "%" else f"{s}%", 210)
                E.append((a, fim, 560, cnt, "pop", 1))
            except ValueError:
                E.append((a, fim, 560, st(fx.num(f"{t} {un}", 210)), "pop", 1))
            continue
        if lo == "anos" and i + 1 < len(ws) and re.fullmatch(r"\d0", ws[i + 1][2].rstrip(".,")):
            E.append((a, fim, 560, st(fx.num("ANOS " + ws[i + 1][2].rstrip(".,"), 200, branco=True)), "pop", 1)); continue
        if a < 2.4 and not re.fullmatch(r"(18|19|20)\d\d", t): continue  # deixa a abertura limpa para o nome da série
        if lo in CARIMBOS and lo not in usados and not (CARIMBOS[lo].startswith("NÃO ") and (i == 0 or ws[i - 1][2].lower() != "não")):
            usados.add(lo); E.append((a, max(fim, min(a + 1.8, dur)), 560, st(fx.stamp(CARIMBOS[lo], 110)), "slam", 1)); continue
        if i + 1 < len(ws):
            t2 = ws[i + 1][2].rstrip(".,?!:;")
            if t[:1].isupper() and t2[:1].isupper() and not re.search(r"[.,?!:;]$", w[2]) and t not in COMUNS and t2 not in COMUNS and norm(t) != norm(empresa) and len(t) > 2 and len(t2) > 2:
                nome = f"{t} {t2}".upper()
                if nome not in usados:
                    usados.add(nome); pula.add(i + 1); E.append((a, a + 2.8, 520, st(fx.tag(nome)), "slide", 1)); continue
        ant = ws[i - 1][2] if i else "."
        if t[:1].isupper() and len(t) > 3 and t not in COMUNS and norm(t) != norm(empresa) and not re.search(r"[.?!]$", ant) and t.upper() not in usados and not any(t.upper() in u.split() for u in usados) \
                and (not E or a - E[-1][0] > 3.5):
            usados.add(t.upper()); E.append((a, min(prox_frase(a), a + 2.6), 520, st(fx.tag(t.upper())), "slide", 1)); continue
    for k, f in enumerate(trio):
        txt = " ".join(x[2] for x in f).rstrip(".").upper()
        E.append((f[0][0], reservado if fim_txt else trio[-1][-1][1] + 0.6, 400 + k * 125, st(fx.tag(txt)), "slide", 2))
    if fim_txt:
        txt = " ".join(x[2] for x in fim_txt).upper()
        dest = {"CUSTO", "OCULTO"} if serie == "g" else set()
        if serie == "j":
            m = re.search(r"FOI (.*)$", txt.split(". ")[-1]); dest = set(norm(p).upper() for p in (m.group(1).split() if m else []))
            dest = {p for p in txt.split() if norm(p).upper() in dest}
            dest = {p.strip(".,”“") for p in dest}
        perg = [f for f in fr if f[-1][2].endswith("?") and f[0][0] > fim_txt[0][0]]
        qfim = perg[0][0][0] if perg else dur
        if serie == "j":
            depois = [f for f in fr if f[0][0] > fim_txt[-1][0] and len(f) <= 7 and norm(f[0][2]) != "essa" and not f[-1][2].endswith("?")][:3]
            if len(depois) == 3:
                fim3 = qfim
                for k, f in enumerate(depois):
                    E.append((f[0][0], fim3, 400 + k * 125, st(fx.tag(" ".join(x[2] for x in f).rstrip(".").upper())), "slide", 2))
                qfim = depois[0][0][0]
        E.append((fim_txt[0][0], qfim, 520, st(fx.quote(quebra(txt, 24), dest)), "up", 3))
        if perg:
            E.append((perg[0][0][0], dur, 520, st(fx.tag("RESPONDE NOS COMENTÁRIOS", sub="E VOCÊ?")), "up", 4))
    # sem sobreposição entre grupos diferentes
    E.sort(key=lambda e: e[0]); out = []
    for e in E:
        if out and out[-1][1] > e[0] and not (out[-1][5] == e[5] == 2):
            # encurta todos os efeitos ainda visíveis
            out = [(o[0], min(o[1], e[0]), *o[2:]) if o[1] > e[0] else o for o in out]
        out.append(e)
    return [e for e in out if e[1] - e[0] >= 1.0]


def cortes(n, dur, fr):
    ini = [f[0][0] for f in fr]
    c = [0.0]
    for i in range(1, n):
        alvo = dur * i / n
        perto = min(ini, key=lambda s: abs(s - alvo))
        c.append(perto if abs(perto - alvo) < 1.4 and perto - c[-1] > 3 else alvo)
    c.append(dur)
    return c


def main(pasta, serie, empresa, roteiro, palavras, narr, encerr, saida, musica=None):
    tmp = os.path.join(pasta, "_tmp"); os.makedirs(tmp, exist_ok=True)
    run = lambda *a: subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *a], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", narr])) + 0.2
    ws = corrige([list(w) for w in json.load(open(palavras))], open(roteiro, encoding="utf-8").read())
    clipmap = {int(re.search(r"_(\d+)", os.path.basename(p)).group(1)): p for p in glob.glob(os.path.join(pasta, "clip*_*.mp4"))}
    fotos = {int(re.match(r"(\d+)", os.path.basename(p)).group(1)): p for p in glob.glob(os.path.join(pasta, "fotos", "*")) if re.match(r"\d+\.(jpe?g|png)$", os.path.basename(p), re.I)}
    idx = sorted(set(clipmap) | set(fotos))
    mov = {}
    anim = glob.glob(os.path.join(pasta, "*animacao*.txt"))
    if anim:
        for l in open(anim[0], encoding="utf-8-sig"):
            m = re.match(r"\((\d+)\.", l.strip())
            if m: mov[int(m.group(1))] = l.lower()
    fr = frases(ws); c = cortes(len(idx), dur, fr)
    base = os.path.join(tmp, "base.mp4")
    lista = open(os.path.join(tmp, "lista.txt"), "w")
    for i, n in enumerate(idx):
        d = c[i + 1] - c[i]; out = os.path.join(tmp, f"s{i:02d}.mp4")
        if not os.path.exists(base):
            if n in clipmap:
                k = max(1.0, min(1.35, d / 4.9))
                run("-ss", "0.1", "-i", clipmap[n], "-an", "-vf", f"setpts=(PTS-STARTPTS)*{k:.4f},fps=30,scale=1080:1920:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=3",
                    "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out)
            else:
                fr_n = int(d * 30) + 2; t = mov.get(n, ""); z = "1.0+0.12*on/%d" % fr_n; x = "iw/2-(iw/zoom/2)"; y = "ih/2-(ih/zoom/2)"
                if "afastamento" in t or "recua" in t: z = "1.12-0.12*on/%d" % fr_n
                elif "travelling" in t or "desliza" in t: z = "1.12"; x = "(iw-iw/zoom)*on/%d" % fr_n
                elif "desce" in t: z = "1.12"; y = "(ih-ih/zoom)*on/%d" % fr_n
                elif "rápido" in t: z = "1.0+0.20*on/%d" % fr_n
                run("-loop", "1", "-i", fotos[n], "-vf", f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='{z}':x='{x}':y='{y}':d={fr_n}:s=1080x1920:fps=30,setsar=1",
                    "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out)
        lista.write(f"file 's{i:02d}.mp4'\n")
    lista.close()
    ass_karaoke(blocos(ws), dur, os.path.join(tmp, "k.ass"))
    if not os.path.exists(base): run("-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "lista.txt"), "-vf", f"ass={os.path.join(tmp, 'k.ass')}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p", os.path.join(tmp, "base.mp4"))
    E = escolhe_efeitos(ws, serie, empresa, dur)
    ins = ["-i", os.path.join(tmp, "base.mp4")]; fc = []; last = "0:v"
    for i, (a, b, y, fn, modo, _) in enumerate(E):
        p = os.path.join(tmp, f"fx{i:02d}"); W, H = fx.renderiza(p, b - a, fn, modo)
        ins += ["-framerate", "30", "-i", os.path.join(p, "%04d.png")]
        fc.append(f"[{i+1}:v]format=rgba,setpts=PTS+{a:.3f}/TB[e{i}]")
        fc.append(f"[{last}][e{i}]overlay=x={540 - W // 2}:y={y - H // 2}:eof_action=pass:format=auto[v{i}]"); last = f"v{i}"
    run(*ins, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", os.path.join(tmp, "fx.mp4"))
    corpo = os.path.join(tmp, "corpo.mp4")
    if musica:
        run("-i", os.path.join(tmp, "fx.mp4"), "-i", narr, "-stream_loop", "-1", "-i", musica, "-filter_complex",
            f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad=whole_dur={dur:.3f},asplit=2[n][sc];[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.20,atrim=0:{dur:.3f},afade=t=in:d=1,afade=t=out:st={dur-1.8:.3f}:d=1.7[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[d];[n][d]amix=inputs=2:normalize=0[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", corpo)
    else:
        run("-i", os.path.join(tmp, "fx.mp4"), "-i", narr, "-filter_complex", f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad=whole_dur={dur:.3f}[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", corpo)
    fim = os.path.join(tmp, "fim.mp4")
    run("-i", encerr, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", "scale=1080:1920:flags=lanczos,fps=30,setsar=1,delogo=x=30:y=40:w=230:h=80", "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", fim)
    run("-i", corpo, "-i", fim, "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a];[a]loudnorm=I=-14:TP=-1.5:LRA=11[a2]",
        "-map", "[v]", "-map", "[a2]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", saida)
    json.dump([[round(e[0], 2), round(e[1], 2), e[4]] for e in E], open(os.path.join(tmp, "efeitos.json"), "w"))
    return E


if __name__ == "__main__":
    E = main(*sys.argv[1:])
    print("ok", len(E), "efeitos")

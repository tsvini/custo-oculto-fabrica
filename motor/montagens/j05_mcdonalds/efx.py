import json, subprocess, sys
sys.path.insert(0, '.')
import fx
ws = json.load(open('/home/claude/custo-oculto-fabrica/legendas/j05_mcdonalds.json'))
def wt(txt, n=1):
    c = 0
    for w in ws:
        if w[2].rstrip(".,?:").upper().replace("MILKSHAKE","MILK-SHAKE") == txt.upper():
            c += 1
            if c == n: return w[0]
    raise KeyError(txt)
EL = []  # (nome, ini, fim, y, base_fn, modo)
def add(nome, a, b, y, fn, modo): EL.append((nome, a, b, y, fn, modo))
st = lambda im: (lambda t: im)
add("bilhoes", wt("bilhões"), 2.7, 560, st(fx.num("BILHÕES", 190)), "pop")
add("1954", wt("1954"), 8.3, 560, st(fx.num("1954", 230, branco=True)), "pop")
add("ray", wt("Ray"), 11.1, 520, st(fx.tag("RAY KROC", sub="QUEM ERA")), "slide")
add("vend", wt("vendia"), 11.1, 660, st(fx.tag("VENDEDOR DE MILK-SHAKE", claro=True)), "slide")
add("cal", wt("Califórnia"), 14.9, 520, st(fx.tag("CALIFÓRNIA · 1954", sub="ONDE")), "slide")
for i, (p, t) in enumerate((("Cardápio", "CARDÁPIO CURTO"), ("cozinha", "COZINHA EM LINHA"), ("pedido", "PRONTO EM MINUTOS"))):
    add(f"rec{i}", wt(p), 20.7, 400 + i * 125, st(fx.tag(t)), "slide")
add("fran", wt("franquias"), 24.7, 520, st(fx.tag("FRANQUIAS", sub="O NOVO NEGÓCIO")), "slide")
add("conta", wt("conta"), 28.5, 560, st(fx.stamp("A CONTA NÃO FECHAVA", 84)), "slam")
add("harry", wt("Harry"), 34.7, 540, st(fx.tag("HARRY SONNEBORN", sub="O HOMEM DAS FINANÇAS")), "slide")
add("terreno", wt("terreno"), 38.5, 560, st(fx.num("O TERRENO", 170)), "pop")
add("aluguel", wt("aluguel"), 43.3, 520, st(fx.stamp("ALUGUEL", 120)), "slam")
add("mes", wt("todo"), 43.3, 700, st(fx.tag("TODO MÊS", claro=True)), "up")
add("quote", wt("Nós"), 49.1, 470, st(fx.quote(["NÃO ESTAMOS NO RAMO", "DE HAMBÚRGUER.", "ESTAMOS NO RAMO", "IMOBILIÁRIO.”"], {"IMOBILIÁRIO"})), "up")
t40 = wt("40")
def cont(t):
    k = min(1, t / 0.7); v = round(40 * (1 - (1 - k) ** 3)); return fx.num(f"+{v} MIL", 220, label="RESTAURANTES NO MUNDO")
add("40", t40, 52.3, 600, cont, "pop")
add("fq", wt("franqueado", 2), 62.8, 420, st(fx.tag("FRANQUEADO  →  LANCHE", claro=True)), "slide")
add("mc", wt("fica"), 62.8, 575, st(fx.tag("McDONALD'S  →  CHÃO", sub="QUEM FICA COM O QUÊ")), "slide")
add("nunca", wt("nunca"), 62.8, 760, st(fx.stamp("NUNCA ATRASA", 90)), "slam")
add("coment", wt("Você"), 68.5, 520, st(fx.tag("RESPONDE NOS COMENTÁRIOS", sub="E VOCÊ?")), "up")
ins = ["-i", "corpo_v.mp4"]; fc = []; last = "0:v"
for i, (nome, a, b, y, fn, modo) in enumerate(EL):
    W, H = fx.renderiza(f"fx_{nome}", b - a, fn, modo)
    ins += ["-framerate", "30", "-i", f"fx_{nome}/%04d.png"]
    fc.append(f"[{i+1}:v]format=rgba,setpts=PTS+{a:.3f}/TB[e{i}]")
    fc.append(f"[{last}][e{i}]overlay=x={540 - W // 2}:y={y - H // 2}:eof_action=pass:format=auto[v{i}]"); last = f"v{i}"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "corpo_fx.mp4"], check=True)
print("ok", len(EL))

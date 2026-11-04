import json, sys
W = json.load(open('/home/claude/custo-oculto-fabrica/legendas/j05_mcdonalds.json')); OUT = 'm.ass'; DUR = 68.6
ws = [list(w) for w in W]
def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
GOLD = "&H003DC8FF&"; WHITE = "&H00FFFFFF&"
ev = []
def E(st, en, style, txt, layer=1): ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{txt}")
BLOCOS = """O McDONALD'S|VENDE BILHÕES|DE HAMBÚRGUERES.|MAS A JOGADA|QUE FEZ ELE|GIGANTE|NÃO FOI|O HAMBÚRGUER.|EM 1954,|RAY KROC|VENDIA MÁQUINAS|DE MILK-SHAKE.|UMA LANCHONETE|NA CALIFÓRNIA|COMPROU TANTAS|QUE ELE FOI|VER DE PERTO.|ERA DOS|IRMÃOS McDONALD.|CARDÁPIO CURTO,|COZINHA EM LINHA,|PEDIDO PRONTO|EM MINUTOS.|KROC VIROU|O RESPONSÁVEL|PELAS FRANQUIAS.|MAS TINHA|UM PROBLEMA.|CADA FRANQUIA|RENDIA POUCO|PARA A EMPRESA.|A CONTA|NÃO FECHAVA.|A VIRADA VEIO|DE UM HOMEM|DAS FINANÇAS|QUE TRABALHAVA|COM ELE,|HARRY SONNEBORN.|A IDEIA|ERA SIMPLES.|O McDONALD'S|PASSARIA A|CONTROLAR|O TERRENO|DE CADA|RESTAURANTE.|E O FRANQUEADO|PAGARIA ALUGUEL.|VENDA BEM|OU MAL,|O ALUGUEL|CHEGA TODO MÊS.|A FRASE|FICOU FAMOSA:|NÓS NÃO ESTAMOS|NO RAMO|DE HAMBÚRGUER.|ESTAMOS NO RAMO|IMOBILIÁRIO.|HOJE, SÃO|MAIS DE|40 MIL|RESTAURANTES|NO MUNDO.|A GRANDE JOGADA|NÃO FOI|O LANCHE RÁPIDO.|FOI PERCEBER|ONDE ESTAVA|O DINHEIRO|DE VERDADE.|O FRANQUEADO|VENDE O LANCHE.|O McDONALD'S|FICA COM O CHÃO.|E O ALUGUEL|NUNCA ATRASA.|ESSA FOI|A JOGADA|QUE MUDOU TUDO.|VOCÊ SABIA|QUE O McDONALD'S|GANHA DINHEIRO|COM IMÓVEIS?""".split("|")
chunks, k = [], 0
for b in BLOCOS:
    n = len(b.split()); chunks.append(ws[k:k + n]); k += n
assert k == len(ws), (k, len(ws))
for c, b in zip(chunks, BLOCOS):
    for w, t in zip(c, b.split()): w[2] = t
for ci, ch in enumerate(chunks):
    ini = ch[0][0]; prox = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else DUR
    fim_ch = min(prox, ch[-1][1] + 0.5)
    for wi, w in enumerate(ch):
        a = w[0] if wi else ini; b = ch[wi + 1][0] if wi + 1 < len(ch) else fim_ch
        partes = [(f"{{\\c{GOLD}\\fscx108\\fscy108}}{x[2]}{{\\c{WHITE}\\fscx100\\fscy100}}" if wj == wi else x[2]) for wj, x in enumerate(ch)]
        pop = "{\\fscx70\\fscy70\\t(0,90,\\fscx100\\fscy100)}" if wi == 0 else ""
        E(a, b, "Cap", "{\\an5\\pos(540,1330)}" + pop + " ".join(partes), 5)
def wt(txt, n=1):
    c = 0
    for w in ws:
        if w[2].rstrip(".,?:") == txt:
            c += 1
            if c == n: return w[0]
    raise KeyError(txt)
def chip(st, en, txt, y=470, cor="&H3DC8FF&", fg="&H101010&"):
    E(st, en, "Chip", f"{{\\pos(540,{y})\\3c{cor}\\c{fg}\\fad(150,200)\\fscx85\\fscy85\\t(0,150,\\fscx100\\fscy100)}}{txt}", 3)
def big(st, en, txt, y=560, cor=GOLD, size=None, instant=False):
    fs = f"\\fs{size}" if size else ""
    anim = "" if instant else "\\fscx60\\fscy60\\t(0,120,\\fscx108\\fscy108)\\t(120,200,\\fscx100\\fscy100)"
    E(st, en, "Big", f"{{\\pos(540,{y})\\c{cor}{fs}{anim}\\fad(0,180)}}{txt}", 3)
def stamp(st, en, txt, y=560):
    E(st, en, "Stamp", f"{{\\pos(540,{y})\\frz-5\\fscx170\\fscy170\\t(0,130,\\fscx100\\fscy100)\\fad(0,180)}}{txt}", 4)
E(0, DUR, "Draw", f"{{\\pos(0,0)\\c{GOLD}\\clip(0,0,0,1920)\\t(0,{int(DUR*1000)},\\clip(0,0,1080,1920))\\p1}}m 0 0 l 1080 0 l 1080 10 l 0 10{{\\p0}}", 6)
big(wt("BILHÕES"), 2.7, "BILHÕES", y=560)
big(wt("1954"), 8.3, "1954", y=560, cor=WHITE)
chip(wt("RAY"), 11.1, "RAY KROC", y=470)
chip(wt("VENDIA"), 11.1, "VENDEDOR DE MILK-SHAKE", y=585, cor="&HFFFFFF&")
chip(wt("CALIFÓRNIA"), 14.9, "CALIFÓRNIA · 1954", y=470)
for i, (p, t) in enumerate((("CARDÁPIO", "CARDÁPIO CURTO"), ("COZINHA", "COZINHA EM LINHA"), ("PEDIDO", "PRONTO EM MINUTOS"))):
    chip(wt(p), 20.7, t, y=380 + i * 115)
chip(wt("FRANQUIAS"), 24.7, "FRANQUIAS", y=470)
stamp(wt("CONTA"), 28.5, "A CONTA NÃO FECHAVA", y=560)
chip(wt("HARRY"), 34.7, "HARRY SONNEBORN", y=470)
chip(wt("HARRY"), 34.7, "O HOMEM DAS FINANÇAS", y=585, cor="&HFFFFFF&")
big(wt("TERRENO"), 38.5, "O TERRENO", y=560, size=170)
stamp(wt("ALUGUEL"), 43.3, "ALUGUEL", y=520)
chip(wt("TODO"), 43.3, "TODO MÊS", y=680, cor="&HFFFFFF&")
E(wt("NÓS"), 49.1, "Label", f"{{\\pos(540,420)\\fs66\\fad(200,150)}}“NÃO ESTAMOS NO RAMO\\NDE HAMBÚRGUER.”", 3)
big(wt("IMOBILIÁRIO"), 49.1, "IMOBILIÁRIO", y=640, size=150)
t40 = wt("40")
for k2 in range(13):
    v = round(40 * (1 - (1 - k2 / 12) ** 3)); st = t40 + k2 * 0.05
    big(st, st + 0.05 if k2 < 12 else 52.3, f"+{v} MIL", y=560, instant=True)
chip(t40 + 0.5, 52.3, "RESTAURANTES", y=720, cor="&HFFFFFF&")
chip(wt("FRANQUEADO", 2), 59.1, "FRANQUEADO → LANCHE", y=430, cor="&HFFFFFF&")
chip(wt("FICA"), 62.8, "McDONALD'S → CHÃO", y=545)
stamp(wt("NUNCA"), 62.8, "NUNCA ATRASA", y=700)
chip(wt("VOCÊ"), DUR, "RESPONDE NOS COMENTÁRIOS", y=470)
hdr = open('/tmp/claude-0/-home-claude/648429a5-07d0-5da7-a5cd-811b5c8d04e6/scratchpad/k3/e.ass').read().split('[Events]')[0]
open(OUT, "w").write(hdr + "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(ev) + "\n")
print("ok", len(chunks))

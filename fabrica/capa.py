"""Capa 1080x1440 no estilo do Custo Oculto (série, EP, nome e foto dividida).
python -m fabrica.capa <saida.jpg> <serie g|j> <ep> <nome> <foto_esq> <foto_dir> <foto_cartao>"""
import random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W, H = 1080, 1440
FONTE = "/root/.fonts/Anton-Regular.ttf"
VERM = (214, 30, 24)
AMAR = (255, 196, 20)


def f(tam):
    return ImageFont.truetype(FONTE, tam)


def cobrir(img, w, h):
    return ImageOps.fit(img.convert("RGB"), (w, h), Image.LANCZOS)


def pincel(w, h, cor, seed):
    """faixa de pincel com bordas irregulares"""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for x in range(0, w + 1, 18):
        pts.append((x, rnd.randint(0, int(h * 0.14))))
    for x in range(w, -1, -18):
        pts.append((x, h - rnd.randint(0, int(h * 0.14))))
    d.polygon(pts, fill=cor + (255,))
    for _ in range(40):  # fiapos
        y = rnd.randint(int(h * 0.1), int(h * 0.9))
        x0 = rnd.choice([rnd.randint(-40, 30), rnd.randint(w - 30, w + 40)])
        d.line([(x0, y), (x0 + rnd.randint(-60, 60), y + rnd.randint(-3, 3))], fill=cor + (255,), width=rnd.randint(2, 6))
    return im.filter(ImageFilter.GaussianBlur(0.6))


def texto(base, xy, s, tam, cor, contorno=8, ancora="mm", sombra=True):
    d = ImageDraw.Draw(base)
    if sombra:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 8), s, font=f(tam), fill=(0, 0, 0, 200), anchor=ancora)
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d.text(xy, s, font=f(tam), fill=cor, anchor=ancora, stroke_width=contorno, stroke_fill=(10, 10, 10))


def caber(s, tam, larg):
    while f(tam).getlength(s) > larg and tam > 40:
        tam -= 4
    return tam


def capa(saida, serie, ep, nome, esq, dir_, cartao):
    rnd = random.Random(nome)
    gig = serie == "g"
    A = cobrir(Image.open(esq), W, H)
    B = cobrir(Image.open(dir_), W, H)
    if gig:  # auge quente x queda fria
        A = ImageEnhance.Color(A).enhance(1.25)
        B = ImageEnhance.Color(B).enhance(0.35)
        B = Image.blend(B, Image.new("RGB", (W, H), (20, 40, 70)), 0.25)
        B = ImageEnhance.Brightness(B).enhance(0.8)
    else:  # antes frio x depois quente
        A = ImageEnhance.Color(A).enhance(0.6)
        A = Image.blend(A, Image.new("RGB", (W, H), (20, 30, 50)), 0.2)
        B = ImageEnhance.Color(B).enhance(1.3)
        B = ImageEnhance.Brightness(B).enhance(1.08)
    # divisão rasgada em diagonal
    mask = Image.new("L", (W, H), 0)
    pts, x0, x1 = [], 760, 430
    for y in range(0, H + 1, 24):
        x = x0 + (x1 - x0) * y / H + rnd.randint(-16, 16)
        pts.append((x, y))
    ImageDraw.Draw(mask).polygon(pts + [(W, H), (W, 0)], fill=255)
    base = Image.composite(B, A, mask).convert("RGBA")
    brilho = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(brilho).line(pts, fill=(255, 235, 200, 255) if not gig else (210, 230, 255, 255), width=7)
    base.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(5)))
    base.alpha_composite(brilho)
    # escurece topo e base para o texto
    grad = Image.new("L", (1, H))
    for y in range(H):
        a = max(0, 230 - y * 0.55) if y < 420 else (max(0, (y - 980) * 0.5) if y > 980 else 0)
        grad.putpixel((0, y), int(min(230, a)))
    base.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 0)] * 3 + [grad.resize((W, H))]))
    # cartão de foto antiga
    c = cobrir(Image.open(cartao), 380, 300)
    c = ImageEnhance.Color(ImageOps.grayscale(c).convert("RGB")).enhance(1)
    c = Image.blend(c, Image.new("RGB", c.size, (112, 86, 52)), 0.28)
    card = Image.new("RGBA", (412, 332), (236, 226, 204, 255))
    card.paste(c, (16, 16))
    card = card.rotate(rnd.choice([-7, 7]), expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pos = (330, 790)
    sh.paste((0, 0, 0, 170), (pos[0] + 14, pos[1] + 18, pos[0] + card.width + 14, pos[1] + card.height + 18), card)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    base.alpha_composite(card, pos)
    # topo: série
    if gig:
        texto(base, (W // 2, 92), "O CUSTO DE SER", 118, (255, 255, 255))
        base.alpha_composite(pincel(880, 210, VERM, nome + "a").rotate(-2, expand=True), (90, 140))
        texto(base, (W // 2, 248), "GIGANTE", 220, AMAR, 10)
    else:
        texto(base, (W // 2, 92), "A JOGADA QUE", 118, (255, 255, 255))
        base.alpha_composite(pincel(880, 210, VERM, nome + "a").rotate(-2, expand=True), (90, 140))
        texto(base, (W // 2, 248), "MUDOU TUDO", 200, AMAR, 10)
    # selo do EP
    sel = Image.new("RGBA", (330, 130), (0, 0, 0, 0))
    ImageDraw.Draw(sel).rounded_rectangle((4, 4, 326, 126), 22, fill=(14, 14, 14, 255), outline=(240, 240, 240, 255), width=6)
    sel = sel.rotate(-3, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(sel, (W // 2 - sel.width // 2, 382))
    d = ImageDraw.Draw(base)
    d.text((W // 2 - 20, 450), "EP.", font=f(96), fill=(255, 255, 255), anchor="rm")
    d.text((W // 2 + 4, 450), f"{int(ep):02d}", font=f(104), fill=VERM, anchor="lm", stroke_width=3, stroke_fill=(10, 10, 10))
    # nome
    base.alpha_composite(pincel(980, 250, VERM, nome + "b").rotate(-3, expand=True, resample=Image.BICUBIC), (40, 1130))
    t = caber(nome, 230, 900)
    texto(base, (W // 2, 1262), nome, t, (255, 255, 255), 9)
    base.convert("RGB").save(saida, quality=92)


if __name__ == "__main__":
    capa(*sys.argv[1:8])

"""Capa 1080x1440 no estilo da capa do Mappin: série no topo, EP, foto dividida por um rasgo,
cartão de foto antiga, nome grande numa faixa vermelha e a parte de baixo preta.
O canto de cima à esquerda fica livre para a logo do canal.
python -m fabrica.capa <saida.jpg> <serie g|j> <ep> <nome> <foto_esq> <foto_dir> <foto_cartao>"""
import random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

W, H = 1080, 1440
FOTO_H = 1150          # abaixo disso é preto
FONTE = "/root/.fonts/Anton-Regular.ttf"
VERM = (205, 24, 20)


def f(t):
    return ImageFont.truetype(FONTE, t)


def cobrir(img, w, h, foco=0.5):
    return ImageOps.fit(img.convert("RGB"), (w, h), Image.LANCZOS, centering=(0.5, foco))


def ruido(w, h, seed, escala=3, dens=0.10):
    rnd = random.Random(seed)
    m = Image.new("L", (w // escala, h // escala), 255)
    px = m.load()
    for _ in range(int(m.width * m.height * dens)):
        px[rnd.randrange(m.width), rnd.randrange(m.height)] = rnd.randint(0, 120)
    return m.resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(0.8))


def pincel(w, h, cor, seed):
    """faixa de pincel: várias pinceladas horizontais sobrepostas, pontas desfiadas"""
    rnd = random.Random(seed)
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    n = 46
    for i in range(n):
        y = int(h * .1 + (h * .8) * i / (n - 1)) + rnd.randint(-6, 6)
        x0 = rnd.randint(0, int(w * .08)); x1 = w - rnd.randint(0, int(w * .08))
        d.line([(x0, y), (x1, y + rnd.randint(-5, 5))], fill=255, width=rnd.randint(int(h * .05), int(h * .1)))
    for _ in range(26):  # fiapos finos saindo das pontas
        y = rnd.randint(int(h * .12), int(h * .88))
        if rnd.random() < .5:
            d.line([(int(w * .06), y), (rnd.randint(-30, int(w * .03)), y + rnd.randint(-3, 3))], fill=255, width=rnd.randint(2, 5))
        else:
            d.line([(int(w * .94), y), (rnd.randint(int(w * .97), w + 30), y + rnd.randint(-3, 3))], fill=255, width=rnd.randint(2, 5))
    m = m.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(.7))
    im = Image.new("RGBA", (w, h), cor + (0,))
    im.putalpha(m)
    borda = Image.new("RGBA", (w, h), (120, 0, 0, 0))
    borda.putalpha(ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(13))).filter(ImageFilter.GaussianBlur(5)).point(lambda v: v // 2))
    im.alpha_composite(borda)
    return im


def texto_italico(s, tam, cor, contorno, grad=None, seed="x"):
    """texto grande inclinado, com contorno, sombra e textura gasta"""
    fn = f(tam)
    l, t, r, b = fn.getbbox(s, stroke_width=contorno)
    w, h = r - l + 80, b - t + 60
    camada = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(camada).text((40 - l, 30 - t), s, font=fn, fill=(20, 20, 20, 255), stroke_width=contorno, stroke_fill=(15, 15, 15, 255))
    miolo = Image.new("L", (w, h), 0)
    ImageDraw.Draw(miolo).text((40 - l, 30 - t), s, font=fn, fill=255)
    if grad:  # degradê vertical
        g = Image.new("RGB", (1, h))
        for y in range(h):
            k = y / h
            g.putpixel((0, y), tuple(int(grad[0][i] * (1 - k) + grad[1][i] * k) for i in range(3)))
        cheio = g.resize((w, h))
    else:
        cheio = Image.new("RGB", (w, h), cor)
    
    camada.paste(cheio, (0, 0), miolo)
    camada = camada.transform((w + int(h * .12), h), Image.AFFINE, (1, .12, -h * .12, 0, 1, 0), Image.BICUBIC)
    sombra = Image.new("RGBA", camada.size, (0, 0, 0, 0))
    sombra.putalpha(camada.getchannel("A").point(lambda v: int(v * .8)))
    out = Image.new("RGBA", (camada.width + 30, camada.height + 30), (0, 0, 0, 0))
    out.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(8)), (14, 18))
    out.alpha_composite(camada)
    return out


def colar_centro(base, im, cx, cy):
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def capa(saida, serie, ep, nome, esq, dir_, cartao):
    rnd = random.Random(nome)
    gig = serie == "g"
    A = cobrir(Image.open(esq), W, FOTO_H)
    B = cobrir(Image.open(dir_), W, FOTO_H)
    quente = lambda im: ImageEnhance.Brightness(Image.blend(ImageEnhance.Color(im).enhance(1.35), Image.new("RGB", im.size, (255, 170, 60)), .14)).enhance(1.05)
    frio = lambda im: ImageEnhance.Brightness(Image.blend(ImageEnhance.Color(im).enhance(.45), Image.new("RGB", im.size, (20, 60, 80)), .32)).enhance(.78)
    A, B = (quente(A), frio(B)) if gig else (frio(A), quente(B))
    for im in (A, B):
        ImageEnhance.Contrast(im).enhance(1.15)
    # rasgo: do alto à direita até o meio, depois desce
    rasgo = []
    for i in range(26):
        k = i / 25
        x = 1060 + (590 - 1060) * k + rnd.randint(-14, 14)
        y = 70 + (770 - 70) * k + rnd.randint(-8, 8)
        rasgo.append((x, y))
    mask = Image.new("L", (W, FOTO_H), 0)
    ImageDraw.Draw(mask).polygon(rasgo + [(760, FOTO_H), (W, FOTO_H), (W, 0)], fill=255)
    foto = Image.composite(B, A, mask.filter(ImageFilter.GaussianBlur(1.5)))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    base.paste(foto, (0, 0))
    luz = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(luz).line(rasgo, fill=(255, 240, 220, 255), width=9, joint="curve")
    base.alpha_composite(luz.filter(ImageFilter.GaussianBlur(10)))
    base.alpha_composite(luz.filter(ImageFilter.GaussianBlur(3)))
    ImageDraw.Draw(base).line(rasgo, fill=(255, 255, 255, 255), width=3, joint="curve")
    # escurece o topo e funde a foto no preto embaixo
    a = Image.new("L", (1, H))
    for y in range(H):
        v = 200 - y * .7 if y < 280 else 0
        if y > FOTO_H - 330:
            v = max(v, (y - (FOTO_H - 330)) / 330 * 255)
        a.putpixel((0, y), int(max(0, min(255, v))))
    preto = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    preto.putalpha(a.resize((W, H)))
    base.alpha_composite(preto)
    # cartão de foto antiga
    c = cobrir(Image.open(cartao), 470, 330)
    c = Image.blend(ImageOps.grayscale(c).convert("RGB"), Image.new("RGB", c.size, (120, 92, 56)), .3)
    c = ImageEnhance.Contrast(c).enhance(1.1)
    card = Image.new("RGBA", (506, 366), (232, 220, 196, 255))
    card.paste(c, (18, 18))
    gasto = Image.new("RGBA", card.size, (90, 60, 30, 0))
    gasto.putalpha(ruido(*card.size, nome + "c", 3, .04).point(lambda v: (255 - v) // 5))
    card.alpha_composite(gasto)
    card = card.rotate(-6, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px, py = 250, 760
    sh.paste((0, 0, 0, 200), (px + 16, py + 20), card)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    base.alpha_composite(card, (px, py))
    # topo: série (o canto esquerdo fica livre para a logo)
    cx = 600
    faixa = pincel(820, 330, VERM, nome + "t").rotate(-3, expand=True, resample=Image.BICUBIC)
    colar_centro(base, faixa, cx + 20, 190)
    l1, l2 = ("O CUSTO DE SER", "GIGANTE") if gig else ("A JOGADA QUE", "MUDOU TUDO")
    colar_centro(base, texto_italico(l1, 104, (255, 255, 255), 7, seed=nome + "1"), cx, 92)
    t2 = 236 if gig else 196
    colar_centro(base, texto_italico(l2, t2, None, 9, grad=((255, 222, 60), (244, 150, 10)), seed=nome + "2"), cx, 238)
    # selo do EP
    ep_txt = texto_italico("EP.", 100, (255, 255, 255), 3, seed="ep")
    num = texto_italico(f"{int(ep):02d}", 108, (226, 22, 22), 3, seed="n")
    ep_txt = ep_txt.crop(ep_txt.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox())
    num = num.crop(num.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox())
    sw = ep_txt.width + num.width + 90
    sel = Image.new("RGBA", (sw, 150), (0, 0, 0, 0))
    ImageDraw.Draw(sel).rounded_rectangle((5, 5, sw - 5, 145), 26, fill=(12, 12, 12, 255), outline=(235, 235, 235, 255), width=7)
    sel.alpha_composite(ep_txt, (34, 75 - ep_txt.height // 2))
    sel.alpha_composite(num, (34 + ep_txt.width + 22, 75 - num.height // 2))
    colar_centro(base, sel.rotate(-3, expand=True, resample=Image.BICUBIC), cx - 30, 405)
    # nome
    colar_centro(base, pincel(940, 300, VERM, nome + "b").rotate(-4, expand=True, resample=Image.BICUBIC), W / 2 + 10, 1170)
    tam = 270
    while True:
        t = texto_italico(nome, tam, (250, 250, 250), 9, seed=nome + "n")
        if t.width <= 980 or tam < 90:
            break
        tam -= 8
    colar_centro(base, t, W / 2, 1168)
    base.convert("RGB").save(saida, quality=93)


if __name__ == "__main__":
    capa(*sys.argv[1:8])

"""Efeitos de tela renderizados em PNG (cartões, números, carimbos, citação) com animação."""
import math, os, random, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
FPS = 30
FI = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype({"xb": FI + "Inter-ExtraBold.otf", "bk": FI + "Inter-Black.otf", "b": FI + "Inter-Bold.otf", "an": "/root/.fonts/Anton-Regular.ttf"}[n], s)
GOLD = (255, 200, 61); GOLD2 = (245, 140, 20); RED = (214, 36, 36); INK = (14, 14, 16)

def sombra(im, raio=18, alfa=170, dx=0, dy=10):
    a = im.getchannel("A").point(lambda v: v * alfa // 255)
    sh = Image.new("RGBA", (im.width + 4 * raio, im.height + 4 * raio), (0, 0, 0, 0))
    s2 = Image.new("RGBA", im.size, (0, 0, 0, 255)); s2.putalpha(a)
    sh.alpha_composite(s2, (2 * raio + dx, 2 * raio + dy)); sh = sh.filter(ImageFilter.GaussianBlur(raio))
    sh.alpha_composite(im, (2 * raio, 2 * raio)); return sh

def brilho(im, cor, raio=22, forca=1.0):
    a = im.getchannel("A")
    g = Image.new("RGBA", (im.width + 4 * raio, im.height + 4 * raio), cor + (0,))
    m = Image.new("L", g.size, 0); m.paste(a, (2 * raio, 2 * raio))
    m = m.filter(ImageFilter.GaussianBlur(raio)).point(lambda v: min(255, int(v * forca)))
    g.putalpha(m); g.alpha_composite(im, (2 * raio, 2 * raio)); return g

def tag(txt, cor=GOLD, sub=None, claro=False):
    f = F("xb", 56); tw = int(f.getlength(txt)); pad = 34
    fs = F("b", 30); sw = int(fs.getlength(sub)) if sub else 0
    w = max(tw, sw) + 2 * pad + 14; h = 104 + (44 if sub else 0)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bg = (250, 250, 250, 240) if claro else (16, 16, 18, 228)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 24, fill=bg)
    d.rounded_rectangle((0, 0, 14, h - 1), 7, fill=cor + (255,))
    d.rounded_rectangle((1, 1, w - 2, h - 2), 24, outline=(255, 255, 255, 40), width=2)
    y = 20
    if sub:
        d.text((pad + 14, 16), sub, font=fs, fill=cor + (255,)); y = 56
    d.text((pad + 14, y), txt, font=f, fill=(INK if claro else (255, 255, 255)) + (255,))
    return sombra(im)

def grad_text(txt, fonte, c1, c2, stroke=10):
    l, t, r, b = fonte.getbbox(txt, stroke_width=stroke)
    w, h = r - l + 8, b - t + 8
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).text((4 - l, 4 - t), txt, font=fonte, fill=255)
    st = Image.new("L", (w, h), 0); ImageDraw.Draw(st).text((4 - l, 4 - t), txt, font=fonte, fill=255, stroke_width=stroke, stroke_fill=255)
    g = Image.new("RGB", (1, h))
    for y in range(h):
        k = y / h; g.putpixel((0, y), tuple(int(c1[i] * (1 - k) + c2[i] * k) for i in range(3)))
    out = Image.new("RGBA", (w, h), INK + (0,)); out.putalpha(st)
    fill = g.resize((w, h)).convert("RGBA"); fill.putalpha(m); out.alpha_composite(fill)
    # reflexo no topo
    hl = Image.new("RGBA", (w, h), (255, 255, 255, 0)); hm = ImageChops.multiply(m, Image.linear_gradient("L").rotate(180).resize((w, h)).point(lambda v: max(0, v - 150)))
    hl.putalpha(hm); out.alpha_composite(hl)
    return out

def num(txt, tam=210, label=None, branco=False):
    c1, c2 = ((255, 255, 255), (205, 210, 220)) if branco else ((255, 226, 110), GOLD2)
    t = brilho(grad_text(txt, F("an", tam), c1, c2), (255, 170, 30) if not branco else (255, 255, 255), 26, 0.55)
    if not label: return sombra(t, 14, 150)
    lb = tag(label, claro=True)
    w = max(t.width, lb.width); im = Image.new("RGBA", (w, t.height + lb.height - 40), (0, 0, 0, 0))
    im.alpha_composite(t, ((w - t.width) // 2, 0)); im.alpha_composite(lb, ((w - lb.width) // 2, t.height - 40))
    return im

def stamp(txt, tam=92):
    f = F("an", tam); tw = int(f.getlength(txt)); w, h = tw + 80, tam + 70
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=RED + (255,))
    d.rounded_rectangle((10, 10, w - 11, h - 11), 9, outline=(255, 255, 255, 235), width=5)
    d.text((w // 2, h // 2 + 2), txt, font=f, fill=(255, 255, 255, 255), anchor="mm")
    rnd = random.Random(txt); a = im.getchannel("A"); px = a.load()
    for _ in range(int(w * h * 0.03)):
        x, y = rnd.randrange(w), rnd.randrange(h)
        if px[x, y]: px[x, y] = rnd.randint(60, 200)
    im.putalpha(a.filter(ImageFilter.GaussianBlur(0.6)))
    return sombra(im.rotate(-5, expand=True, resample=Image.BICUBIC), 16, 190)

def quote(linhas, destaque):
    f = F("xb", 62); fq = F("an", 190)
    w = max(int(f.getlength(l)) for l in linhas) + 130; h = 80 * len(linhas) + 120
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 28, fill=(16, 16, 18, 225), outline=(255, 255, 255, 40), width=2)
    d.text((26, -36), "“", font=fq, fill=GOLD + (255,))
    y = 62
    for l in linhas:
        x = 60
        for p in l.split(" "):
            c = GOLD if p.strip(".,”“") in destaque else (255, 255, 255)
            d.text((x, y), p, font=f, fill=c + (255,)); x += int(f.getlength(p + " "))
        y += 80
    return sombra(im)

def ease_back(t):
    c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def ease_out(t): return 1 - (1 - t) ** 3

def renderiza(pasta, dur, base_fn, modo="pop", entrada=0.32, saida=0.22):
    """gera frames RGBA; base_fn(t)->imagem. Devolve (w,h)."""
    if os.path.isdir(pasta): shutil.rmtree(pasta)
    os.makedirs(pasta)
    n = int(round(dur * FPS)); b0 = base_fn(0)
    W, H = int(b0.width * 1.25) + 40, int(b0.height * 1.25) + 40
    for i in range(n):
        t = i / FPS; b = base_fn(t)
        k = min(1, t / entrada); ko = min(1, max(0, (dur - t) / saida))
        alpha = min(ease_out(k), ko); s = 1.0; dx = dy = 0; rot = 0
        if modo == "pop": s = 0.55 + 0.45 * ease_back(k)
        elif modo == "slide": dx = int(-90 * (1 - ease_out(k)))
        elif modo == "up": dy = int(60 * (1 - ease_out(k)))
        elif modo == "slam":
            kk = min(1, t / 0.16); s = 1.8 - 0.8 * ease_out(kk); alpha = min(1, kk * 2.5, ko)
            if 0.16 < t < 0.4: dx = int(random.Random(i).randint(-7, 7)); dy = int(random.Random(i + 9).randint(-7, 7))
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        im = b if abs(s - 1) < 1e-3 else b.resize((max(1, int(b.width * s)), max(1, int(b.height * s))), Image.BICUBIC)
        if alpha < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
        fr.alpha_composite(im, (W // 2 - im.width // 2 + dx, H // 2 - im.height // 2 + dy))
        fr.save(f"{pasta}/{i:04d}.png", compress_level=1)
    return W, H

"""Checagem automática das cenas: acha textos que se sobrepõem ou saem da tela.
Uso: python ferramentas/checa_textos.py projetos/curso-playwright-08 [mais pastas...]
Renderiza cada cena em 4 momentos (com print fake no lugar das mídias) e lista os problemas."""
import json, os, sys
from playwright.sync_api import sync_playwright
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = r"""
window.__txt = [];
const P = CanvasRenderingContext2D.prototype;  // acompanha o recorte (clip) de retângulos, pra ignorar texto escondido
const oSave = P.save, oRest = P.restore, oRect = P.rect, oClip = P.clip, oBP = P.beginPath;
P.save = function () { (this.__pilha = this.__pilha || []).push(this.__clip || null); return oSave.apply(this, arguments); };
P.restore = function () { this.__clip = (this.__pilha || []).pop() || null; return oRest.apply(this, arguments); };
P.beginPath = function () { this.__r = null; return oBP.apply(this, arguments); };
P.rect = function (x, y, w, h) { const tr = this.getTransform(); const a = [tr.a * x + tr.c * y + tr.e, tr.b * x + tr.d * y + tr.f], b = [tr.a * (x + w) + tr.c * (y + h) + tr.e, tr.b * (x + w) + tr.d * (y + h) + tr.f];
  this.__r = [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[0], b[0]), Math.max(a[1], b[1])]; return oRect.apply(this, arguments); };
P.clip = function () { if (this.__r) { const r = this.__r, c = this.__clip; this.__clip = c ? [Math.max(r[0], c[0]), Math.max(r[1], c[1]), Math.min(r[2], c[2]), Math.min(r[3], c[3])] : r; } return oClip.apply(this, arguments); };
const F = CanvasRenderingContext2D.prototype.fillText;
CanvasRenderingContext2D.prototype.fillText = function (t, x, y) {
  try { const m = this.measureText(t); const tr = this.getTransform(); const w = m.width;
    let x0 = this.textAlign === "center" ? x - w / 2 : this.textAlign === "right" || this.textAlign === "end" ? x - w : x;
    const h = (m.actualBoundingBoxAscent || 0) + (m.actualBoundingBoxDescent || 0);
    const y0 = y - (m.actualBoundingBoxAscent || 0);
    const p = (X, Y) => [tr.a * X + tr.c * Y + tr.e, tr.b * X + tr.d * Y + tr.f];
    const [ax, ay] = p(x0, y0), [bx, by] = p(x0 + w, y0 + h);
    let bx0 = Math.min(ax, bx), by0 = Math.min(ay, by), bx1 = Math.max(ax, bx), by1 = Math.max(ay, by); const c = this.__clip;
    if (c) { bx0 = Math.max(bx0, c[0]); by0 = Math.max(by0, c[1]); bx1 = Math.min(bx1, c[2]); by1 = Math.min(by1, c[3]); }
    if (String(t).trim() && this.globalAlpha > 0.5 && bx1 - bx0 > 2 && by1 - by0 > 2) window.__txt.push({ t: String(t), x0: bx0, y0: by0, x1: bx1, y1: by1 });
  } catch (e) {}
  return F.apply(this, arguments);
};
window.checar = async (tipo, s, t, dur) => {
  for (const w of [500, 600, 700, 800, 900]) await document.fonts.load(w + " 40px Inter"); await document.fonts.load("700 40px 'JetBrains Mono'");
  const cv = document.getElementById("cv"), ctx = cv.getContext("2d"); const W = 1920, H = 1080; ctx.setTransform(1,0,0,1,0,0); ctx.clearRect(0,0,W,H);
  window.__txt = []; window.CO_MARCA = ["PLAYWRIGHT", "PARA LEIGOS"];
  COEngine.SCENES[tipo](ctx, { W, H, vertical: false, u: 1, cx: W / 2, cy: H * 0.45 }, t, dur, s, {});
  const T = window.__txt; const prob = [];
  T.forEach((a) => { if (a.x0 < -2 || a.x1 > W + 2 || a.y0 < -2 || a.y1 > H + 2) prob.push("fora da tela: " + a.t.slice(0, 40)); });
  for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) { const a = T[i], b = T[j];
    if (a.t === b.t && Math.abs(a.x0 - b.x0) < 3 && Math.abs(a.y0 - b.y0) < 3) continue;  // mesmo texto desenhado 2x (contorno)
    const ix = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0), iy = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
    if (ix > 4 && iy > 4) prob.push("sobreposto: '" + a.t.slice(0, 30) + "' × '" + b.t.slice(0, 30) + "'"); }
  return [...new Set(prob)];
};
true;
"""
alvos = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto("file://" + RAIZ + "/ferramentas/teste_cena.html"); pg.evaluate(JS)
    total = 0
    for pasta in alvos:
        pj = json.load(open(os.path.join(RAIZ, pasta, "projeto.json"), encoding="utf8"))
        for parte in pj["script"]["long"]["parts"]:
            for i, s in enumerate(parte["sentences"], 1):
                sc = s["scene"]; dur = 6.0
                achados = set()
                for t in (1.5, 3.0, 4.5, 5.9):
                    try:
                        for x in pg.evaluate("([a,b,c,d])=>checar(a,b,c,d)", [sc["type"], sc, t, dur]): achados.add(x)
                    except Exception as e:
                        achados.add("erro: " + str(e)[:80])
                if achados:
                    total += len(achados); print(f"{os.path.basename(pasta)} frase {i} [{sc['type']}]:"); [print("   -", x) for x in sorted(achados)]
    print("problemas:", total)
    b.close()

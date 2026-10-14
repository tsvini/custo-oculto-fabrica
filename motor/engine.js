/* Estúdio Custo Oculto — motor de vídeo (canvas + WebAudio + WebCodecs). */
(function (global) {
  "use strict";
  const COL = { gold: [245, 170, 40], red: [230, 52, 52], white: [245, 245, 242], muted: [150, 150, 155],
    green: [70, 190, 110], blue: [70, 140, 235], dark: [20, 20, 24], card: [26, 26, 31] };
  const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
  const MONO = "'JetBrains Mono', 'Courier New', monospace";

  function col(c, fb) {
    if (Array.isArray(c)) return c;
    if (typeof c === "string" && COL[c]) return COL[c];
    if (typeof c === "string" && /^#?[0-9a-f]{6}$/i.test(c)) {
      const h = c.replace("#", "");
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }
    return fb || COL.white;
  }
  const css = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const easeOut = (x) => { x = clamp(x); return 1 - Math.pow(1 - x, 3); };
  const easeInOut = (x) => { x = clamp(x); return 3 * x * x - 2 * x * x * x; };
  const backOut = (x) => { x = clamp(x); const c1 = 1.70158, c3 = 2.70158; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
  const lerp = (a, b, t) => a + (b - a) * t;
  const fmtInt = (n) => Math.round(n).toLocaleString("pt-BR");

  function font(w, size, fam) { return `${w} ${Math.max(1, Math.round(size))}px ${fam || FONT}`; }

  function textW(ctx, txt, f) { ctx.font = f; return ctx.measureText(txt).width; }

  // Texto centralizado com alpha/escala/contorno
  function drawC(ctx, txt, f, x, y, o = {}) {
    const a = o.alpha === undefined ? 1 : o.alpha;
    if (a <= 0.01 || !txt) return;
    ctx.save();
    ctx.globalAlpha *= a;
    ctx.translate(x, y);
    if (o.scale && o.scale !== 1) ctx.scale(o.scale, o.scale);
    ctx.font = f;
    ctx.textAlign = o.align || "center";
    ctx.textBaseline = "middle";
    if (o.stroke) {
      ctx.lineJoin = "round";
      ctx.lineWidth = o.stroke * 2;
      ctx.strokeStyle = css(o.strokeCol || [0, 0, 0]);
      ctx.strokeText(txt, 0, 0);
    }
    if (o.shadow) { ctx.shadowColor = "rgba(0,0,0,.55)"; ctx.shadowBlur = o.shadow; ctx.shadowOffsetY = o.shadow / 3; }
    ctx.fillStyle = css(col(o.fill, COL.white));
    ctx.fillText(txt, 0, 0);
    ctx.restore();
  }
  // Ajusta o tamanho para caber na largura
  function fitSize(ctx, txt, w, size, maxW) { const m = textW(ctx, txt, font(w, size)); return m > maxW ? size * maxW / m : size; }

  function rrect(ctx, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function box(ctx, x, y, w, h, r, fill, alpha = 1, stroke, lw) {
    if (alpha <= 0) return;
    ctx.save(); ctx.globalAlpha *= alpha; rrect(ctx, x, y, w, h, r);
    if (fill) { ctx.fillStyle = css(col(fill)); ctx.fill(); }
    if (stroke) { ctx.lineWidth = lw || 3; ctx.strokeStyle = css(col(stroke)); ctx.stroke(); }
    ctx.restore();
  }
  function wrap(ctx, txt, f, maxW) {
    const words = String(txt).split(/\s+/); const lines = []; let cur = "";
    ctx.font = f;
    for (const w of words) { const t = (cur + " " + w).trim(); if (ctx.measureText(t).width <= maxW || !cur) cur = t; else { lines.push(cur); cur = w; } }
    if (cur) lines.push(cur); return lines;
  }

  // ---------- fundo ----------
  class Background {
    constructor(W, H) {
      this.W = W; this.H = H;
      const b = document.createElement("canvas"); b.width = W; b.height = H; const c = b.getContext("2d");
      const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#141419"); g.addColorStop(1, "#060608");
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      const v = c.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.25, W / 2, H / 2, Math.max(W, H) * 0.75);
      v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(0,0,0,.55)");
      c.fillStyle = v; c.fillRect(0, 0, W, H);
      this.base = b;
      this.grain = [];
      const gw = Math.ceil(W / 2), gh = Math.ceil(H / 2);
      for (let k = 0; k < 6; k++) {
        const gc = document.createElement("canvas"); gc.width = gw; gc.height = gh;
        const x = gc.getContext("2d"); const id = x.createImageData(gw, gh); const d = id.data;
        for (let i = 0; i < d.length; i += 4) { const v2 = Math.random() < 0.5 ? 0 : 255; d[i] = d[i + 1] = d[i + 2] = v2; d[i + 3] = Math.random() * 16; }
        x.putImageData(id, 0, 0); this.grain.push(gc);
      }
    }
    draw(ctx, i, t, glow = COL.gold, strength = 0.10, tint = null) {
      const { W, H } = this;
      ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over";
      ctx.drawImage(this.base, 0, 0);
      const cx = W * (0.5 + 0.25 * Math.sin(t * 0.21)), cy = H * (0.35 + 0.12 * Math.cos(t * 0.17));
      const r = Math.max(W, H) * 0.55;
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
      g.addColorStop(0, css(glow, strength * 2.2)); g.addColorStop(1, css(glow, 0));
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      if (tint) { ctx.fillStyle = css(tint, 0.12); ctx.fillRect(0, 0, W, H); }
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(this.grain[i % 6], 0, 0, W, H);
      ctx.imageSmoothingEnabled = true;
    }
  }

  // ---------- cenas ----------
  function enter(t, d = 0.35) { return [easeOut(t / d), lerp(0.9, 1, backOut(t / d))]; }
  function cue(s, i, def) {
    const cs = s._cues; const k = i + (s.cue_offset || 0);
    if (cs && cs.length > 1 && k < cs.length) return cs[k] + 0.1;
    return def;
  }

  const S = {};
  S.counter = (ctx, c, t, dur, s) => {
    const u = c.u; const [a, sc] = enter(t);
    const p = easeOut((t - 0.1) / Math.max(0.6, Math.min(1.6, dur * 0.5)));
    const val = (s.prefix || "") + fmtInt((s.value || 0) * p) + (s.suffix || "");
    const full = (s.prefix || "") + fmtInt(s.value || 0) + (s.suffix || "");
    const size = fitSize(ctx, full, 900, (s.size || 230) * u, c.W * 0.88);
    drawC(ctx, s.over, font(700, 54 * u), c.cx, c.cy - 210 * u, { fill: "muted", alpha: a });
    drawC(ctx, val, font(900, size), c.cx, c.cy, { fill: col(s.color, COL.gold), alpha: a, scale: sc });
    drawC(ctx, s.label, font(800, fitSize(ctx, s.label || "", 800, 66 * u, c.W * 0.9)), c.cx, c.cy + 190 * u, { alpha: easeOut((t - 0.5) / 0.4) });
    if (s.sub) drawC(ctx, s.sub, font(500, 44 * u), c.cx, c.cy + 270 * u, { fill: "muted", alpha: easeOut((t - 0.8) / 0.4) });
  };
  S.date = (ctx, c, t, dur, s) => {
    const u = c.u * (c.vertical ? 1 : 0.74); const [a, sc] = enter(t);
    const w = 560 * u, h = 620 * u, x0 = c.cx - w / 2, y0 = c.cy - h / 2 - 20 * u, yo = (1 - a) * 60 * u;
    box(ctx, x0, y0 + yo, w, h, 40 * u, "white", a);
    ctx.save(); ctx.globalAlpha = a; rrect(ctx, x0, y0 + yo, w, h, 40 * u); ctx.clip();
    ctx.fillStyle = css(COL.red); ctx.fillRect(x0, y0 + yo, w, 150 * u); ctx.restore();
    drawC(ctx, s.month, font(900, fitSize(ctx, s.month || "", 900, 84 * u, w * 0.88)), c.cx, y0 + 78 * u + yo, { alpha: a });
    drawC(ctx, s.day, font(900, fitSize(ctx, s.day || "", 900, 300 * u, w * 0.85)), c.cx, y0 + 370 * u + yo, { fill: [20, 20, 24], alpha: a, scale: sc });
    drawC(ctx, s.year, font(700, fitSize(ctx, s.year || "", 700, 70 * u, w * 0.85)), c.cx, y0 + 560 * u + yo, { fill: [90, 90, 96], alpha: a });
    if (s.tag) {
      const ta = easeOut((t - 0.6) / 0.35); const f = font(800, 54 * u); const tw = textW(ctx, s.tag, f) + 60 * u; const ty = y0 + h + 90 * u;
      box(ctx, c.cx - tw / 2, ty - 48 * u, tw, 96 * u, 48 * u, "gold", ta);
      drawC(ctx, s.tag, f, c.cx, ty, { fill: [20, 20, 20], alpha: ta });
    }
  };
  S.board = (ctx, c, t, dur, s) => {
    const u = c.u; const [a] = enter(t); const rows = s.rows || [];
    const flip = (s.flip_at === undefined ? 0.35 : s.flip_at) * dur;
    const w = (c.vertical ? 980 : 1300) * u, rh = 112 * u, x0 = c.cx - w / 2, top = c.cy - rows.length * rh / 2 - 40 * u;
    box(ctx, x0 - 20 * u, top - 120 * u, w + 40 * u, rows.length * rh + 150 * u, 28 * u, [12, 12, 14], a, [60, 60, 66], 3 * u);
    ctx.save(); ctx.globalAlpha = a; ctx.textBaseline = "top"; ctx.textAlign = "left";
    ctx.font = font(700, 46 * u, MONO); ctx.fillStyle = css(COL.gold); ctx.fillText(s.header || "PARTIDAS", x0 + 10 * u, top - 95 * u);
    ctx.font = font(700, 34 * u, MONO); ctx.fillStyle = css(COL.muted); ctx.fillText("STATUS", x0 + w - 310 * u, top - 85 * u);
    ctx.restore();
    rows.forEach((r, i) => {
      const y = top + i * rh; const ra = easeOut((t - 0.08 * i) / 0.3) * a; if (ra <= 0) return;
      box(ctx, x0, y + 8 * u, w, rh - 16 * u, 10 * u, [24, 24, 28], ra);
      ctx.save(); ctx.globalAlpha = ra; ctx.textBaseline = "top"; ctx.textAlign = "left";
      ctx.font = font(700, 50 * u, MONO); ctx.fillStyle = css(COL.white); ctx.fillText(r[0], x0 + 22 * u, y + 28 * u);
      const maxd = w - 200 * u - 330 * u; let ds = 50 * u; ctx.font = font(700, ds, MONO);
      const dw = ctx.measureText(r[1]).width; if (dw > maxd) { ds *= maxd / dw; ctx.font = font(700, ds, MONO); }
      ctx.fillText(r[1], x0 + 200 * u, y + 28 * u + (50 * u - ds) * 0.6);
      const ft = flip + 0.12 * i; let st, cl;
      if (t < ft) { st = s.ok_label || "CONFIRMADO"; cl = [90, 200, 120]; }
      else { const k = Math.floor((t - ft) / 0.04); st = k > 4 ? (s.bad_label || "CANCELADO") : Array.from({ length: 9 }, () => "ABCDEFGHIJKLMNOPRSTUVZ"[Math.floor(Math.random() * 22)]).join(""); cl = COL.red; }
      ctx.font = font(700, 50 * u, MONO); ctx.fillStyle = css(cl); ctx.fillText(st, x0 + w - 310 * u, y + 28 * u);
      ctx.restore();
    });
  };
  S.flash = (ctx, c, t, dur, s) => {
    const u = c.u; const sc = lerp(1.6, 1, easeOut(t / 0.25)); const a = clamp(t / 0.12);
    const lines = String(s.text || "").split("\n"); let fs = (s.size || 170) * u;
    for (const ln of lines) fs = Math.min(fs, fitSize(ctx, ln, 900, fs, c.W * 0.9));
    const total = lines.length * fs * 1.05;
    lines.forEach((ln, i) => drawC(ctx, ln, font(900, fs), c.cx, c.cy - total / 2 + fs * 0.55 + i * fs * 1.05, { fill: col(s.color, COL.red), alpha: a, scale: sc }));
  };
  S.stamp = (ctx, c, t, dur, s) => {
    const u = c.u * (c.vertical ? 1 : 0.8); const [a] = enter(t);
    const w = 720 * u, h = 820 * u, x0 = c.cx - w / 2, y0 = c.cy - h / 2 - 40 * u;
    box(ctx, x0, y0, w, h, 24 * u, [236, 233, 224], a);
    drawC(ctx, s.org, font(700, fitSize(ctx, s.org || "", 700, 40 * u, w * 0.85)), c.cx, y0 + 80 * u, { fill: [110, 110, 110], alpha: a });
    const tl = wrap(ctx, s.title || "", font(900, 58 * u), w - 120 * u);
    tl.slice(0, 3).forEach((ln, i) => drawC(ctx, ln, font(900, 58 * u), c.cx, y0 + 170 * u + i * 70 * u, { fill: [30, 30, 30], alpha: a }));
    for (let i = 0; i < 8; i++) { const lw = (w - 140 * u) * (0.6 + 0.4 * ((i * 37) % 10) / 10); box(ctx, x0 + 70 * u, y0 + 360 * u + i * 52 * u, lw, 16 * u, 8 * u, [200, 196, 186], a); }
    const st = s.stamp_at === undefined ? 0.45 : s.stamp_at;
    if (t > st) {
      const k = easeOut((t - st) / 0.18); const sc = lerp(2.2, 1, k); const scol = col(s.stamp_color, COL.red);
      let fs = (s.stamp_size || 120) * u; ctx.font = font(900, fs); let tw = ctx.measureText(s.stamp || "").width;
      if (tw > w * 1.05) { fs *= w * 1.05 / tw; tw = w * 1.05; }
      ctx.save(); ctx.globalAlpha = a * clamp(k * 1.5) * 0.92; ctx.translate(c.cx, c.cy + 150 * u - 40 * u); ctx.rotate(-14 * Math.PI / 180); ctx.scale(sc, sc);
      const pad = 34 * u; rrect(ctx, -tw / 2 - pad, -fs / 2 - pad, tw + pad * 2, fs + pad * 2, 18 * u); ctx.lineWidth = 12 * u; ctx.strokeStyle = css(scol); ctx.stroke();
      ctx.font = font(900, fs); ctx.fillStyle = css(scol); ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(s.stamp || "", 0, 4 * u);
      ctx.restore();
    }
  };
  S.timeline = (ctx, c, t, dur, s) => {
    const u = c.u; const [a] = enter(t); const w = (c.vertical ? 820 : 1300) * u; const x0 = c.cx - w / 2, x1 = c.cx + w / 2, y = c.cy + 120 * u;
    box(ctx, x0, y - 10 * u, w, 20 * u, 10 * u, [55, 55, 60], a);
    const p = easeInOut((t - 0.3) / Math.max(0.8, dur * 0.55));
    box(ctx, x0, y - 10 * u, Math.max(1, w * p), 20 * u, 10 * u, "gold", a);
    [[x0, s.start, s.start_sub, COL.gold], [x1, s.end, s.end_sub, p >= 0.999 ? COL.red : [55, 55, 60]]].forEach(([xx, lab, sub, cl]) => {
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = css(cl); ctx.beginPath(); ctx.arc(xx, y, 26 * u, 0, 7); ctx.fill(); ctx.restore();
      drawC(ctx, lab, font(800, 50 * u), xx, y + 90 * u, { alpha: a });
      if (sub) drawC(ctx, sub, font(500, 38 * u), xx, y + 150 * u, { fill: "muted", alpha: a });
    });
    drawC(ctx, s.big, font(900, fitSize(ctx, s.big || "", 900, (s.size || 180) * u, c.W * 0.85)), c.cx, c.cy - 130 * u, { alpha: easeOut((t - 0.2) / 0.4), scale: lerp(0.9, 1, backOut((t - 0.2) / 0.4)) });
  };
  S.bigtext = (ctx, c, t, dur, s) => {
    const u = c.u; const lines = s.lines || [];
    const sizes = lines.map((l) => fitSize(ctx, l[0], 900, (l[2] || 110) * u, c.W * 0.9));
    const total = sizes.reduce((x, y) => x + y * 1.12, 0); let y = c.cy - total / 2;
    lines.forEach((l, i) => {
      const st = i * (s.stagger === undefined ? 0.25 : s.stagger); const hh = sizes[i] * 1.12;
      drawC(ctx, l[0], font(900, sizes[i]), c.cx, y + hh / 2, { fill: col(l[1]), alpha: easeOut((t - st) / 0.3), scale: lerp(0.9, 1, backOut((t - st) / 0.35)) });
      y += hh;
    });
  };
  S.bullets = (ctx, c, t, dur, s) => {
    const u = c.u; const items = s.items || []; const rh = 130 * u; const top = c.cy - items.length * rh / 2;
    if (s.title) drawC(ctx, s.title, font(700, 50 * u), c.cx, top - 90 * u, { fill: "muted", alpha: easeOut(t / 0.3) });
    const gap = s.stagger || Math.min(1.2, dur / Math.max(items.length, 1) * 0.75);
    items.forEach((it, i) => {
      const st = cue(s, i, 0.25 + i * gap);
      const fs = fitSize(ctx, it, 900, (s.size || 76) * u, c.W * 0.9);
      drawC(ctx, it, font(900, fs), c.cx, top + i * rh + rh / 2, { fill: (i === items.length - 1 && s.last_gold) ? COL.gold : COL.white, alpha: easeOut((t - st) / 0.35), scale: lerp(0.9, 1, backOut((t - st) / 0.4)) });
    });
  };
  S.compare = (ctx, c, t, dur, s) => {
    const u = c.u; const items = s.items || []; const n = items.length;
    if (s.title) drawC(ctx, s.title, font(800, 56 * u), c.cx, c.cy - (c.vertical ? 560 : 330) * u, { alpha: easeOut(t / 0.3) });
    items.forEach((it, i) => {
      const st = i * (s.stagger === undefined ? 0.9 : s.stagger); const a = easeOut((t - st) / 0.35); const sc = lerp(0.85, 1, backOut((t - st) / 0.4));
      let x, y, slot;
      if (c.vertical) { x = c.cx; y = c.cy - 260 * u + i * 520 * u; slot = c.W * 0.88; }
      else { x = n === 1 ? c.W / 2 : c.W * (0.29 + 0.42 * i / (n - 1)); y = c.cy; slot = c.W * (n === 2 ? 0.36 : 0.26); }
      const fs = fitSize(ctx, it[0], 900, (s.size || 150) * u, slot);
      drawC(ctx, it[0], font(900, fs), x, y, { fill: col(it[2]), alpha: a, scale: sc });
      drawC(ctx, it[1], font(700, 48 * u), x, y + 130 * u, { fill: "muted", alpha: a });
    });
    if (s.vs !== false && n === 2) drawC(ctx, "×", font(900, 90 * u), c.cx, c.cy, { fill: [90, 90, 96], alpha: easeOut((t - 0.5) / 0.3) });
  };
  S.events = (ctx, c, t, dur, s) => {
    const u = c.u; const ev = s.events || []; const rh = (s.row || 120) * u; const top = c.cy - ev.length * rh / 2;
    const x0 = c.cx - (c.vertical ? 470 : 720) * u; const gap = s.stagger || dur / Math.max(ev.length, 1) * 0.8;
    box(ctx, x0 + 18 * u, top + rh * 0.5, 6 * u, rh * (ev.length - 1), 2, [60, 60, 66], easeOut(t / 0.3));
    ev.forEach((e, i) => {
      const a = easeOut((t - cue(s, i, 0.2 + i * gap)) / 0.35); if (a <= 0) return; const y = top + i * rh + rh / 2; const cl = col(e[2], COL.gold);
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = css(cl); ctx.beginPath(); ctx.arc(x0 + 21 * u, y, 20 * u, 0, 7); ctx.fill();
      ctx.textBaseline = "middle"; ctx.textAlign = "left"; ctx.font = font(900, 50 * u); ctx.fillText(e[0], x0 + 70 * u + (1 - a) * 30 * u, y);
      const tx = x0 + (c.vertical ? 330 : 400) * u; const lines = wrap(ctx, e[1], font(600, 46 * u), c.W - tx - 120 * u).slice(0, 2);
      ctx.font = font(600, 46 * u); ctx.fillStyle = css(COL.white);
      lines.forEach((ln, k) => ctx.fillText(ln, tx + (1 - a) * 30 * u, y + (k - (lines.length - 1) / 2) * 54 * u));
      ctx.restore();
    });
  };
  S.flow = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.35); const bw = 520 * u, bh = 300 * u;
    const A = c.vertical ? [c.cx, c.cy - 330 * u] : [c.W * 0.27, c.cy]; const B = c.vertical ? [c.cx, c.cy + 330 * u] : [c.W * 0.73, c.cy];
    [[A, s.a, s.a_sub, COL.gold], [B, s.b, s.b_sub, COL.red]].forEach(([[x, y], lab, sub, cl]) => {
      box(ctx, x - bw / 2, y - bh / 2, bw, bh, 30 * u, "card", a, cl, 5 * u);
      drawC(ctx, lab, font(900, fitSize(ctx, lab || "", 900, 70 * u, bw * 0.85)), x, y - 30 * u, { fill: cl, alpha: a });
      drawC(ctx, sub, font(600, fitSize(ctx, sub || "", 600, 40 * u, bw * 0.9)), x, y + 55 * u, { fill: "muted", alpha: a });
    });
    const pa = easeOut((t - 0.3) / 0.5);
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "rgb(120,120,126)";
    if (c.vertical) { const y0 = A[1] + bh / 2 + 20 * u, y1 = B[1] - bh / 2 - 20 * u; ctx.fillRect(c.cx - 5 * u, y0, 10 * u, (y1 - y0) * pa); }
    else { const x0 = A[0] + bw / 2 + 20 * u, x1 = B[0] - bw / 2 - 20 * u; ctx.fillRect(x0, c.cy - 5 * u, (x1 - x0) * pa, 10 * u);
      if (pa > 0.95) { ctx.beginPath(); ctx.moveTo(x1, c.cy); ctx.lineTo(x1 - 30 * u, c.cy - 22 * u); ctx.lineTo(x1 - 30 * u, c.cy + 22 * u); ctx.fill(); } }
    ctx.restore();
    if (t > 0.8) for (let k = 0; k < 6; k++) {
      const ph = ((t - 0.8) * 0.45 + k / 6) % 1; let px, py;
      if (c.vertical) { px = c.cx + 40 * u * Math.sin(k * 2.1); py = lerp(A[1] + bh / 2, B[1] - bh / 2, ph); }
      else { px = lerp(A[0] + bw / 2, B[0] - bw / 2, ph); py = c.cy - 60 * u + 25 * u * Math.sin(k * 2.1); }
      drawC(ctx, s.coin || "R$", font(900, 46 * u), px, py, { fill: "gold", alpha: Math.sin(ph * Math.PI) * a });
    }
    if (s.caption) drawC(ctx, s.caption, font(800, fitSize(ctx, s.caption, 800, 54 * u, c.W * 0.9)), c.cx, c.cy - (c.vertical ? 620 : 300) * u, { alpha: easeOut((t - 0.2) / 0.4) });
  };
  S.endcard = (ctx, c, t, dur, s) => {
    const u = c.u;
    drawC(ctx, "CUSTO", font(900, 170 * u), c.cx, c.cy - 110 * u, { alpha: easeOut(t / 0.4), scale: lerp(0.85, 1, backOut(t / 0.45)) });
    drawC(ctx, "OCULTO", font(900, 170 * u), c.cx, c.cy + 60 * u, { fill: "gold", alpha: easeOut((t - 0.12) / 0.4), scale: lerp(0.85, 1, backOut((t - 0.12) / 0.45)) });
    if (s.sub) { const ta = easeOut((t - 0.5) / 0.4); const f = font(800, 52 * u); const tw = textW(ctx, s.sub, f) + 70 * u; const ty = c.cy + 260 * u;
      box(ctx, c.cx - tw / 2, ty - 52 * u, tw, 104 * u, 52 * u, "red", ta); drawC(ctx, s.sub, f, c.cx, ty, { alpha: ta }); }
  };
  S.chapter = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4);
    drawC(ctx, s.num, font(700, 46 * u), c.cx, c.cy - 120 * u, { fill: "gold", alpha: a });
    drawC(ctx, s.title, font(900, fitSize(ctx, s.title || "", 900, (s.size || 130) * u, c.W * 0.85)), c.cx, c.cy, { alpha: a, scale: lerp(0.92, 1, backOut(t / 0.5)) });
    const lw = 420 * u * easeOut((t - 0.2) / 0.5); box(ctx, c.cx - lw / 2, c.cy + 100 * u, Math.max(1, lw), 8 * u, 2, "gold", a);
  };
  // manchete desenhada (sem print): recorte de jornal com veículo, data e título
  const SERIF = "Merriweather, Georgia, 'Times New Roman', 'Liberation Serif', serif";
  S.manchete = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.35);
    const outlet = String(s.outlet || (s.source || "").split(",")[0] || "").toUpperCase();
    const date = s.date || ((s.source || "").split(",")[1] || "").trim();
    const w = Math.min(c.W * (c.vertical ? 0.9 : 0.62), 1200 * u); const pad = 56 * u;
    let hs = (c.vertical ? 74 : 66) * u; let lines = wrap(ctx, s.headline || "", font(800, hs, SERIF), w - pad * 2);
    while (lines.length > 4 && hs > 30 * u) { hs *= 0.9; lines = wrap(ctx, s.headline || "", font(800, hs, SERIF), w - pad * 2); }
    const lh = hs * 1.18; const h = pad + 64 * u + 30 * u + lines.length * lh + 40 * u + 5 * 34 * u + pad;
    const x0 = c.cx - w / 2; const y0 = c.cy - h / 2 - (c.vertical ? 40 : 20) * u + (1 - a) * 50 * u;
    const z = lerp(1, 1.04, easeInOut(t / Math.max(dur, 0.1)));
    ctx.save(); ctx.globalAlpha = a; ctx.translate(c.cx, c.cy); ctx.rotate((s.rotate === undefined ? -1.2 : s.rotate) * Math.PI / 180); ctx.scale(z, z); ctx.translate(-c.cx, -c.cy);
    ctx.shadowColor = "rgba(0,0,0,.7)"; ctx.shadowBlur = 40 * u; ctx.shadowOffsetY = 12 * u; ctx.fillStyle = "#f3efe6"; ctx.fillRect(x0, y0, w, h); ctx.shadowColor = "transparent";
    ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    let y = y0 + pad + 40 * u;
    ctx.font = font(900, 40 * u, SERIF); ctx.fillStyle = "#1a1a1a"; ctx.fillText(outlet, x0 + pad, y);
    ctx.font = font(600, 28 * u); ctx.fillStyle = "#6b6b6b"; ctx.textAlign = "right"; ctx.fillText(date, x0 + w - pad, y); ctx.textAlign = "left";
    y += 22 * u; ctx.fillStyle = "#1a1a1a"; ctx.fillRect(x0 + pad, y, w - pad * 2, 4 * u); y += 30 * u;
    const hp = easeOut((t - 0.7) / 0.6);
    lines.forEach((ln, i) => {
      const by = y + i * lh; ctx.font = font(800, hs, SERIF); const lw = ctx.measureText(ln).width;
      if (hp > 0) { const k = clamp(hp * lines.length - i); if (k > 0) { ctx.fillStyle = "rgba(255,205,40,.55)"; ctx.fillRect(x0 + pad - 6 * u, by + lh * 0.12, (lw + 12 * u) * k, lh * 0.86); } }
      ctx.fillStyle = "#111"; ctx.fillText(ln, x0 + pad, by + lh * 0.82);
    });
    y += lines.length * lh + 40 * u;
    for (let i = 0; i < 5; i++) { const lw2 = (w - pad * 2) * (0.62 + 0.38 * ((i * 37) % 10) / 10); ctx.fillStyle = "#cfcac0"; ctx.fillRect(x0 + pad, y + i * 34 * u, lw2, 14 * u); }
    ctx.restore();
  };
  function mediaFallback(ctx, c, t, dur, s) {
    if (s.headline) return S.manchete(ctx, c, t, dur, s);
    const fb = s.fallback || { type: "bigtext", lines: [[s.lower || s.label || "", "white", 90]] };
    (S[fb.type] || S.bigtext)(ctx, c, t, dur, fb);
  }
  S.print = (ctx, c, t, dur, s, media) => {
    const m = media && media[s.media]; const img = m && m.img;
    if (!img) return mediaFallback(ctx, c, t, dur, s);
    const u = c.u; const a = easeOut(t / 0.35);
    const maxW = c.W * (c.vertical ? 0.9 : 0.68), maxH = c.H * (c.vertical ? 0.45 : 0.56);
    const r = Math.min(maxW / img.width, maxH / img.height); const z = lerp(0.96, s.zoom || 1.08, easeInOut(t / Math.max(dur, 0.1)));
    const w = img.width * r * z, h = img.height * r * z; const cy = c.cy - (c.vertical ? 60 : 70) * u + (1 - a) * 40 * u;
    ctx.save(); ctx.globalAlpha = a; ctx.translate(c.cx, cy); ctx.rotate((s.rotate === undefined ? -1.0 : s.rotate) * Math.PI / 180);
    ctx.shadowColor = "rgba(0,0,0,.7)"; ctx.shadowBlur = 40 * u; ctx.shadowOffsetY = 12 * u; ctx.fillStyle = "#fff"; ctx.fillRect(-w / 2, -h / 2, w, h);
    ctx.shadowColor = "transparent"; ctx.drawImage(img, -w / 2, -h / 2, w, h);
    if (s.highlight) { const [hx0, hy0, hx1, hy1] = s.highlight; const hp = easeOut((t - 0.8) / 0.5);
      if (hp > 0) { ctx.fillStyle = "rgba(255,200,40,.37)"; ctx.fillRect(-w / 2 + hx0 * w, -h / 2 + hy0 * h, (hx1 - hx0) * w * hp, (hy1 - hy0) * h); } }
    ctx.restore();
    if (s.source) { const f = font(700, 34 * u); const txt = "Fonte: " + s.source; const tw = textW(ctx, txt, f); const y = cy + h / 2 + 30 * u;
      box(ctx, c.cx - tw / 2 - 24 * u, y, tw + 48 * u, 56 * u, 28 * u, [0, 0, 0], 0.7 * a); drawC(ctx, txt, f, c.cx, y + 28 * u, { fill: [220, 220, 220], alpha: a }); }
  };
  S.image = (ctx, c, t, dur, s, media) => {
    const m = media && media[s.media]; const img = m && m.img;
    if (!img) return mediaFallback(ctx, c, t, dur, s);
    const z = lerp(s.z0 || 1.04, s.z1 || 1.16, t / Math.max(dur, 0.1)); const r = Math.max(c.W / img.width, c.H / img.height) * z;
    const w = img.width * r, h = img.height * r; const a = easeOut(t / 0.3);
    ctx.save(); ctx.globalAlpha = a; ctx.drawImage(img, (c.W - w) / 2, (c.H - h) / 2, w, h); ctx.fillStyle = `rgba(0,0,0,${s.dim === undefined ? 0.35 : s.dim})`; ctx.fillRect(0, 0, c.W, c.H); ctx.restore();
    overlayLabels(ctx, c, t, s); credito(ctx, c, m, a);
  };
  S.video = (ctx, c, t, dur, s, media) => {
    const m = media && media[s.media]; const v = m && m.video;
    if (!v || !v.videoWidth) return mediaFallback(ctx, c, t, dur, s);
    const z = lerp(1, s.zoom || 1.06, t / Math.max(dur, 0.1)); const vw = v.videoWidth, vh = v.videoHeight; const a = easeOut(t / 0.25);
    ctx.save(); ctx.globalAlpha = a;
    if (vh > vw && !c.vertical) { // vertical em quadro horizontal: fundo desfocado
      const rb = Math.max(c.W / vw, c.H / vh); ctx.filter = "blur(30px) brightness(.7)"; ctx.drawImage(v, (c.W - vw * rb) / 2, (c.H - vh * rb) / 2, vw * rb, vh * rb); ctx.filter = "none";
      const rf = c.H / vh * z; ctx.drawImage(v, (c.W - vw * rf) / 2, (c.H - vh * rf) / 2, vw * rf, vh * rf);
    } else { const r = Math.max(c.W / vw, c.H / vh) * z; ctx.drawImage(v, (c.W - vw * r) / 2, (c.H - vh * r) / 2, vw * r, vh * r); }
    ctx.fillStyle = `rgba(0,0,0,${s.dim === undefined ? 0.35 : s.dim})`; ctx.fillRect(0, 0, c.W, c.H); ctx.restore();
    overlayLabels(ctx, c, t, s); credito(ctx, c, m, a);
  };
  // ---------- CAPA de impacto (1º segundo do vídeo e miniatura) ----------
  // {type:"capa", foto:"chave_da_foto", recorte:"texto do recorte de jornal", faixa:"TEXTO NA FAIXA VERMELHA",
  //  linhas:[["TEXTO","gold",210], ...], selo:"TEXTO DO SELO", seta:true}
  const DISPLAY = "Anton, 'Bebas Neue', Impact, 'Arial Narrow', sans-serif";
  function credito(ctx, c, m, a) {
    if (!m || !m.credit) return; const u = c.u; ctx.save(); ctx.globalAlpha = 0.75 * (a === undefined ? 1 : a);
    ctx.font = font(500, 22 * u); ctx.textBaseline = "middle"; ctx.fillStyle = "#fff"; ctx.shadowColor = "rgba(0,0,0,.9)"; ctx.shadowBlur = 6 * u;
    const txt = m.credit.length > 90 ? m.credit.slice(0, 89) + "…" : m.credit;
    if (c.vertical) { ctx.textAlign = "left"; ctx.fillText(txt, 40 * u, c.H * 0.115); } else { ctx.textAlign = "right"; ctx.fillText(txt, c.W - 30 * u, c.H - 28 * u); }
    ctx.restore();
  }
  function papel(ctx, x, y, w, h, seed) { // retângulo com bordas rasgadas
    let r = seed || 7; const rnd = () => { r = (r * 9301 + 49297) % 233280; return r / 233280; };
    const n = Math.max(8, Math.round(w / 28)); ctx.beginPath(); ctx.moveTo(x, y + rnd() * 8);
    for (let i = 1; i <= n; i++) ctx.lineTo(x + w * i / n, y + rnd() * 10);
    for (let i = n; i >= 0; i--) ctx.lineTo(x + w * i / n, y + h - rnd() * 10);
    ctx.closePath();
  }
  // ---------- LOGOS (marca famosa: capa, abertura e "X contra Y") ----------
  // cena {type:"logo", logo:"chave", logo2:"chave2" (opcional, vira "A x B"), sub:"TEXTO", placa:true (fundo claro p/ logo escuro)}
  function drawLogo(ctx, c, m, cx, cy, maxW, maxH, a, sc, placa) {
    if (!m || !m.img || a <= 0) return 0; const img = m.img; const u = c.u;
    const r = Math.min(maxW / img.width, maxH / img.height); const w = img.width * r * sc, h = img.height * r * sc;
    ctx.save(); ctx.globalAlpha = a;
    if (placa) { box(ctx, cx - w / 2 - 36 * u, cy - h / 2 - 28 * u, w + 72 * u, h + 56 * u, 22 * u, [245, 242, 235], 0.96 * a); }
    else { ctx.shadowColor = "rgba(0,0,0,.85)"; ctx.shadowBlur = 40 * u; }
    ctx.drawImage(img, cx - w / 2, cy - h / 2, w, h); ctx.restore(); return h;
  }
  S.logo = (ctx, c, t, dur, s, media) => {
    const u = c.u; const V = c.vertical; const z = lerp(1, 1.06, clamp(t / Math.max(dur, 0.1)));
    const k1 = easeOut(clamp(t / 0.35)), sc1 = lerp(1.25, 1, k1) * z;
    if (s.logo2) {
      const k2 = easeOut(clamp((t - 0.45) / 0.35)), sc2 = lerp(1.25, 1, k2) * z;
      const mw = V ? c.W * 0.7 : c.W * 0.34, mh = V ? c.H * 0.16 : c.H * 0.32;
      const p1 = V ? [c.cx, c.H * 0.27] : [c.W * 0.26, c.cy], p2 = V ? [c.cx, c.H * 0.56] : [c.W * 0.74, c.cy];
      drawLogo(ctx, c, media && media[s.logo], p1[0], p1[1], mw, mh, k1, sc1, s.placa);
      drawLogo(ctx, c, media && media[s.logo2], p2[0], p2[1], mw, mh, k2, sc2, s.placa2 === undefined ? s.placa : s.placa2);
      const kx = easeOut(clamp((t - 0.25) / 0.3)); const f = `${Math.round(150 * u)}px ${DISPLAY}`;
      drawC(ctx, "X", f, V ? c.cx : c.W / 2, V ? c.H * 0.415 : c.cy, { stroke: 10 * u, alpha: kx, fill: COL.red });
    } else {
      drawLogo(ctx, c, media && media[s.logo], c.cx, c.cy - (s.sub ? 60 * u : 0), V ? c.W * 0.78 : c.W * 0.5, V ? c.H * 0.2 : c.H * 0.36, k1, sc1, s.placa);
    }
    if (s.sub) { const ks = easeOut(clamp((t - 0.6) / 0.4)); const f = `${Math.round((V ? 80 : 70) * u)}px ${DISPLAY}`;
      drawC(ctx, String(s.sub).toUpperCase(), f, c.cx, s.logo2 ? (V ? c.H * 0.72 : c.H * 0.8) : c.cy + (V ? 230 : 200) * u, { stroke: 8 * u, alpha: ks, fill: COL.gold }); }
  };
  S.capa = (ctx, c, t, dur, s, media) => {
    const u = c.u; const V = c.vertical; const m = media && media[s.foto]; const img = m && m.img;
    if (img) {
      const z = lerp(1.06, 1.14, clamp(t / Math.max(dur, 0.1))); const r = Math.max(c.W / img.width, c.H / img.height) * z;
      const w = img.width * r, h = img.height * r; const ox = V ? (c.W - w) / 2 : c.W - w * 0.92;
      ctx.drawImage(img, ox, (c.H - h) / 2, w, h);
      ctx.fillStyle = "rgba(8,8,12,.28)"; ctx.fillRect(0, 0, c.W, c.H);
    }
    const g = V ? ctx.createLinearGradient(0, 0, 0, c.H) : ctx.createLinearGradient(0, 0, c.W, 0);
    if (V) { g.addColorStop(0, "rgba(0,0,0,.55)"); g.addColorStop(0.22, "rgba(0,0,0,0)"); g.addColorStop(0.42, "rgba(0,0,0,.15)"); g.addColorStop(0.62, "rgba(0,0,0,.8)"); g.addColorStop(1, "rgba(0,0,0,.95)"); }
    else { g.addColorStop(0, "rgba(0,0,0,.95)"); g.addColorStop(0.42, "rgba(0,0,0,.75)"); g.addColorStop(0.7, "rgba(0,0,0,.05)"); g.addColorStop(1, "rgba(0,0,0,0)"); }
    ctx.fillStyle = g; ctx.fillRect(0, 0, c.W, c.H);
    const slam = (d) => { const k = clamp((t - d) / 0.18); return [k, lerp(1.35, 1, easeOut(k))]; };
    // vertical: fora da coluna de botões do TikTok (direita) e do texto do post (embaixo)
    const X0 = V ? c.W * 0.455 : c.W * 0.06; const maxW = V ? c.W * 0.78 : c.W * 0.5;
    // logo da marca (no lugar do recorte de jornal)
    const ml = s.logo && media && media[s.logo];
    if (ml) { const [k, sc] = slam(0);
      if (V) drawLogo(ctx, c, ml, c.W * 0.5, c.H * 0.25, c.W * 0.66, c.H * 0.13, k, sc, s.placa);
      else { const r = Math.min(c.W * 0.32 / ml.img.width, c.H * 0.17 / ml.img.height); drawLogo(ctx, c, ml, X0 + ml.img.width * r / 2, c.H * 0.08 + ml.img.height * r / 2, c.W * 0.32, c.H * 0.17, k, sc, s.placa); }
    }
    // recorte de jornal
    if (s.recorte && !ml) {
      const [k] = slam(0); const fs = (V ? 46 : 40) * u; const f = `italic 800 ${Math.round(fs)}px ${SERIF}`;
      const lines = wrap(ctx, s.recorte, f, (V ? 520 : 560) * u).slice(0, 3); ctx.font = f;
      const w = Math.max(...lines.map((l) => ctx.measureText(l).width)) + 60 * u; const h = lines.length * fs * 1.2 + 50 * u;
      const x = V ? c.W - w - 50 * u : X0; const y = V ? c.H * 0.17 : c.H * 0.08;
      ctx.save(); ctx.globalAlpha = k; ctx.translate(x + w / 2, y + h / 2); ctx.rotate((V ? -4 : -2) * Math.PI / 180); ctx.translate(-w / 2, -h / 2);
      ctx.shadowColor = "rgba(0,0,0,.6)"; ctx.shadowBlur = 24 * u; ctx.shadowOffsetY = 8 * u; ctx.fillStyle = "#efe9dc"; papel(ctx, 0, 0, w, h, 11); ctx.fill();
      ctx.shadowColor = "transparent"; ctx.fillStyle = "#1b1b1b"; ctx.font = f; ctx.textAlign = "left"; ctx.textBaseline = "top";
      lines.forEach((l, i) => ctx.fillText(l, 30 * u, 25 * u + i * fs * 1.2)); ctx.restore();
    }
    // bloco de texto
    const lines = (s.linhas || []).map((l) => Array.isArray(l) ? l : [l, "white"]);
    const sizes = lines.map((l) => { const base = (l[2] || (V ? 200 : 170)) * u; ctx.font = `${Math.round(base)}px ${DISPLAY}`; const w = ctx.measureText(String(l[0]).toUpperCase()).width; return w > maxW ? base * maxW / w : base; });
    const faixaH = s.faixa ? (V ? 112 : 96) * u : 0; const blockH = faixaH + 18 * u + sizes.reduce((a, b) => a + b * 1.0, 0);
    let y = V ? c.H * 0.47 : (c.H - blockH) / 2 + (ml ? 110 * u : s.recorte ? 60 * u : 0);
    const selH = s.selo ? 110 * u : 0;
    if (V && y + blockH + selH > c.H * 0.76) y = Math.max(c.H * 0.3, c.H * 0.76 - blockH - selH);
    if (s.faixa) {
      const [k, sc] = slam(0.08); const fs = (V ? 72 : 60) * u; ctx.font = `${Math.round(fs)}px ${DISPLAY}`; let tw = ctx.measureText(s.faixa.toUpperCase()).width;
      const fsz = tw > maxW - 60 * u ? fs * (maxW - 60 * u) / tw : fs; ctx.font = `${Math.round(fsz)}px ${DISPLAY}`; tw = ctx.measureText(s.faixa.toUpperCase()).width;
      const bw = tw + 70 * u, bx = V ? X0 - bw / 2 : X0 - 10 * u;
      ctx.save(); ctx.globalAlpha = k; ctx.translate(bx + bw / 2, y + faixaH / 2); ctx.rotate(-3 * Math.PI / 180); ctx.scale(sc, sc);
      ctx.fillStyle = "#d61f26"; ctx.beginPath(); ctx.moveTo(-bw / 2 + 18 * u, -faixaH / 2); ctx.lineTo(bw / 2, -faixaH / 2); ctx.lineTo(bw / 2 - 18 * u, faixaH / 2); ctx.lineTo(-bw / 2, faixaH / 2); ctx.closePath(); ctx.fill();
      ctx.fillStyle = "#fff"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(s.faixa.toUpperCase(), 0, 4 * u); ctx.restore();
      y += faixaH + 18 * u;
    }
    lines.forEach((l, i) => {
      const [k, sc] = slam(0.18 + i * 0.1); const fs = sizes[i]; const txt = String(l[0]).toUpperCase();
      ctx.save(); ctx.globalAlpha = k; ctx.font = `${Math.round(fs)}px ${DISPLAY}`; ctx.textBaseline = "middle"; ctx.textAlign = V ? "center" : "left";
      ctx.translate(X0, y + fs * 0.5); ctx.scale(sc, sc);
      ctx.lineJoin = "round"; ctx.lineWidth = 14 * u; ctx.strokeStyle = "rgba(0,0,0,.95)"; ctx.strokeText(txt, 0, 0);
      ctx.shadowColor = "rgba(0,0,0,.7)"; ctx.shadowBlur = 30 * u; ctx.fillStyle = css(col(l[1], COL.white)); ctx.fillText(txt, 0, 0); ctx.restore();
      y += fs * 1.0;
    });
    if (s.selo) {
      const [k] = slam(0.5); const fs = (V ? 64 : 52) * u; ctx.font = `${Math.round(fs)}px ${DISPLAY}`; const txt = s.selo.toUpperCase(); const tw = Math.min(ctx.measureText(txt).width, maxW - 120 * u);
      const bw = tw + (s.seta ? 130 : 60) * u, bh = fs * 1.35, bx = V ? X0 - bw / 2 : X0, by = y + 24 * u;
      box(ctx, bx, by, bw, bh, 14 * u, [12, 12, 14], 0.92 * k, "gold", 4 * u);
      ctx.save(); ctx.globalAlpha = k; ctx.font = `${Math.round(fs)}px ${DISPLAY}`; ctx.fillStyle = css(COL.gold); ctx.textBaseline = "middle"; ctx.textAlign = "left";
      ctx.fillText(txt, bx + 30 * u, by + bh / 2 + 3 * u, tw);
      if (s.seta) { const ax = bx + bw - 70 * u, ay = by + bh / 2; ctx.strokeStyle = css(COL.red); ctx.lineWidth = 12 * u; ctx.lineCap = "round";
        ctx.beginPath(); ctx.moveTo(ax - 20 * u, ay - 28 * u); ctx.lineTo(ax + 20 * u, ay + 22 * u); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(ax + 24 * u, ay - 6 * u); ctx.lineTo(ax + 22 * u, ay + 26 * u); ctx.lineTo(ax - 8 * u, ay + 22 * u); ctx.stroke(); }
      ctx.restore();
    }
    credito(ctx, c, m, 1);
  };
  function overlayLabels(ctx, c, t, s) {
    const u = c.u;
    if (s.label) drawC(ctx, s.label, font(900, fitSize(ctx, s.label, 900, (s.size || 120) * u, c.W * 0.9)), c.cx, c.cy, { stroke: 7 * u, alpha: easeOut((t - 0.3) / 0.4) });
    if (s.lower) { const f = font(800, 44 * u); const tw = textW(ctx, s.lower, f); const y = c.H * (c.vertical ? 0.2 : 0.12); const la = easeOut((t - 0.4) / 0.4);
      box(ctx, 60 * u, y - 40 * u, tw + 70 * u, 80 * u, 10 * u, [0, 0, 0], 0.75 * la);
      ctx.save(); ctx.globalAlpha = la; ctx.fillStyle = css(COL.gold); ctx.fillRect(60 * u, y - 40 * u, 10 * u, 80 * u); ctx.restore();
      drawC(ctx, s.lower, f, 100 * u, y, { alpha: la, align: "left" }); }
  }

  // ---------- legendas ----------
  function buildWords(segs) {
    const words = [];
    segs.forEach((sg, si) => {
      if (!sg.text) return;
      const toks = String(sg.cap || sg.text).split(/\s+/).filter(Boolean);
      if (sg.words && !sg.cap && sg.words.length === toks.length) { sg.words.forEach(([w, a, b]) => words.push({ w, s: Math.max(a, sg.start), e: Math.min(Math.max(b, a + 0.05), sg.end + 0.3), seg: si })); return; }
      const wts = toks.map((w) => w.replace(/[^\p{L}\p{N}]/gu, "").length * (/\d/.test(w) ? 3.2 : 1) + 2);
      const tot = wts.reduce((a, b) => a + b, 0) || 1; let t = sg.start; const span = sg.end - sg.start;
      toks.forEach((w, i) => { const d = span * wts[i] / tot; words.push({ w, s: t, e: t + d, seg: si }); t += d; });
    });
    const chunks = []; let cur = [];
    for (const wd of words) {
      cur.push(wd); const nch = cur.reduce((a, x) => a + x.w.length, 0) + cur.length - 1;
      if (cur.length >= 3 || /[.,!?;:]$/.test(wd.w) || nch >= 15) { chunks.push(cur); cur = []; }
    }
    if (cur.length) chunks.push(cur);
    return chunks;
  }
  function drawCaptions(ctx, c, t, chunks, safe) {
    let lo = 0, hi = chunks.length - 1, ch = null;
    while (lo <= hi) { const m = (lo + hi) >> 1; const k = chunks[m]; if (t < k[0].s - 0.02) hi = m - 1; else if (t >= k[k.length - 1].e + 0.05) lo = m + 1; else { ch = k; break; } }
    if (!ch) return;
    const u = c.u; let fs = (c.vertical ? 84 : 64) * u; const words = ch.map((w) => w.w.toUpperCase());
    ctx.font = font(900, fs); let sp = ctx.measureText(" ").width + (safe ? 16 : 6) * u; let ws = words.map((w) => ctx.measureText(w).width + 16 * u);
    let total = ws.reduce((a, b) => a + b, 0) + sp * (words.length - 1); const maxW = c.W * (safe ? 0.72 : c.vertical ? 0.86 : 0.7);
    if (total > maxW) { const k = maxW / total; fs *= k; sp *= k; ws = ws.map((x) => x * k); total = maxW; }
    let x = c.cx - total / 2; const y = c.H * (safe ? 0.68 : c.vertical ? 0.70 : 0.84); const ka = easeOut((t - ch[0].s) / 0.12);
    ch.forEach((wd, i) => { const act = wd.s <= t && t < wd.e + 0.03;
      drawC(ctx, words[i], font(900, fs), x + ws[i] / 2, y, { fill: act ? COL.gold : COL.white, stroke: 9 * u, alpha: ka, scale: act ? 1.08 : 1 }); x += ws[i] + sp; });
  }

  // ---------- áudio ----------
  const SR = 48000;
  async function decodeAudio(arrayBuffer) {
    const AC = global.OfflineAudioContext || global.webkitOfflineAudioContext;
    const ctx = new AC(1, SR, SR);
    const buf = await ctx.decodeAudioData(arrayBuffer.slice(0));
    const n = buf.length; const out = new Float32Array(n);
    for (let ch = 0; ch < buf.numberOfChannels; ch++) { const d = buf.getChannelData(ch); for (let i = 0; i < n; i++) out[i] += d[i] / buf.numberOfChannels; }
    if (buf.sampleRate !== SR) return resample(out, buf.sampleRate, SR);
    return out;
  }
  function resample(x, from, to) { const n = Math.round(x.length * to / from); const y = new Float32Array(n);
    for (let i = 0; i < n; i++) { const p = i * from / to; const i0 = Math.floor(p); const f = p - i0; y[i] = (x[i0] || 0) * (1 - f) + (x[i0 + 1] || 0) * f; } return y; }
  function frameDb(x, win) { const n = Math.floor(x.length / win); const db = new Float32Array(n);
    for (let k = 0; k < n; k++) { let s = 0; for (let i = k * win; i < (k + 1) * win; i++) s += x[i] * x[i]; db[k] = 10 * Math.log10(s / win + 1e-12); } return db; }
  function silences(x, thr = -36, minDur = 0.09) {
    const win = SR / 100; const db = frameDb(x, win); const out = []; let st = -1;
    for (let k = 0; k <= db.length; k++) { const sil = k < db.length && db[k] < thr;
      if (sil && st < 0) st = k; if (!sil && st >= 0) { if ((k - st) / 100 >= minDur) out.push([st / 100, k / 100]); st = -1; } }
    return out;
  }
  // encurta pausas longas e normaliza o volume
  function prepVoice(x, maxPause = 0.18) {
    const sil = silences(x, -40, maxPause + 0.02); const keep = []; let pos = 0;
    for (const [a, b] of sil) { const cutA = a + maxPause / 2, cutB = b - maxPause / 2; if (cutB > cutA) { keep.push([pos, cutA]); pos = cutB; } }
    keep.push([pos, x.length / SR]);
    const total = keep.reduce((s, [a, b]) => s + Math.max(0, b - a), 0); const y = new Float32Array(Math.round(total * SR)); let o = 0;
    for (const [a, b] of keep) { const i0 = Math.round(a * SR), i1 = Math.min(x.length, Math.round(b * SR)); y.set(x.subarray(i0, i1), o); o += i1 - i0; }
    const win = SR / 100; const db = frameDb(y, win); let s = 0, n = 0;
    for (let k = 0; k < db.length; k++) if (db[k] > -45) { s += Math.pow(10, db[k] / 10); n++; }
    const rmsDb = n ? 10 * Math.log10(s / n) : -20; const gain = Math.pow(10, (-17 - rmsDb) / 20);
    for (let i = 0; i < y.length; i++) { let v = y[i] * gain; if (Math.abs(v) > 0.7) v = Math.sign(v) * (0.7 + 0.2 * Math.tanh((Math.abs(v) - 0.7) / 0.2)); y[i] = v; }
    return y.subarray(0, o);
  }
  function align(segs, x) {
    const total = x.length / SR; let sil = silences(x);
    const lead = sil.length && sil[0][0] < 0.05 ? sil[0][1] : 0; const tail = sil.length && sil[sil.length - 1][1] > total - 0.05 ? sil[sil.length - 1][0] : total;
    sil = sil.filter(([a, b]) => a > lead + 0.05 && b < tail - 0.05);
    const lens = segs.map((s) => s.text.length); const sum = lens.reduce((a, b) => a + b, 0); const cum = []; let acc = 0;
    for (let i = 0; i < lens.length - 1; i++) { acc += lens[i]; cum.push(lead + (tail - lead) * acc / sum); }
    const bounds = []; const used = new Set();
    for (const exp of cum) {
      let best = -1, bd = 1e9;
      sil.forEach(([a, b], i) => { if (used.has(i)) return; const mid = (a + b) / 2; const d = Math.abs(mid - exp) - Math.min(b - a, 0.4) * 1.5;
        if (d < bd && (!bounds.length || mid > bounds[bounds.length - 1][1])) { best = i; bd = d; } });
      if (best >= 0 && Math.abs((sil[best][0] + sil[best][1]) / 2 - exp) < 2.5) { used.add(best); bounds.push(sil[best]); } else bounds.push([exp, exp]);
    }
    let t = lead; bounds.push([tail, total]);
    segs.forEach((sg, i) => { sg.start = t; sg.end = bounds[i][0]; t = bounds[i][1]; });
    return total;
  }
  function synthBed(total, cuts) {
    const n = Math.ceil(total * SR); const m = new Float32Array(n);
    for (const [f0, amp] of [[55, 0.5], [82.4, 0.32], [110, 0.18], [130.8, 0.12]])
      for (let i = 0; i < n; i++) { const tt = i / SR; m[i] += amp * Math.sin(2 * Math.PI * f0 * tt) * (0.6 + 0.4 * Math.sin(2 * Math.PI * 0.07 * tt + f0)); }
    for (let i = 0; i < n; i++) { const tt = i / SR; m[i] *= 0.045 * clamp(Math.min(tt / 1.5, (total - tt) / 1.5)); }
    const L = Math.floor(0.6 * SR); const hit = new Float32Array(L);
    for (let i = 0; i < L; i++) { const k = i / SR; hit[i] = 0.28 * Math.sin(2 * Math.PI * (70 * Math.exp(-k * 6) + 38) * k) * Math.exp(-k * 7) + 0.05 * (Math.random() * 2 - 1) * Math.exp(-Math.pow(k - 0.12, 2) / 0.004); }
    for (const c of cuts) { const i0 = Math.floor(Math.max(0, c - 0.08) * SR); for (let i = 0; i < L && i0 + i < n; i++) m[i0 + i] += hit[i]; }
    return m;
  }

  // ---------- linha do tempo ----------
  // units: [{kind:'speech', sentences:[{text,cap,scene}], voice:Float32Array} | {kind:'card', scene, dur}]
  function buildTimeline(units, opts = {}) {
    const segs = []; let t0 = 0; const voiceParts = [];
    units.forEach((u, ui) => {
      if (u.kind === "card") { segs.push({ text: "", scene: JSON.parse(JSON.stringify(u.scene)), start: t0, end: t0 + u.dur, card: true }); t0 += u.dur; return; }
      const local = u.sentences.map((s) => ({ text: s.text, cap: s.cap, scene: JSON.parse(JSON.stringify(s.scene || { type: "bigtext", lines: [] })) }));
      let dur;
      if (u.voice && u.timings && u.timings.length === local.length) { local.forEach((s, k) => { s.start = u.timings[k][0]; s.end = u.timings[k][1]; if (u.words && u.words[k]) s.words = u.words[k]; }); dur = u.voice.length / SR; voiceParts.push([t0, u.voice]); }
      else if (u.voice) { dur = align(local, u.voice); voiceParts.push([t0, u.voice]); }
      else { let t = 0.3; local.forEach((s) => { const d = s.text.length / 15.5; s.start = t; s.end = t + d; t += d + 0.15; }); dur = t + 0.3; }
      local.forEach((s) => { s.start += t0; s.end += t0; if (s.words) s.words = s.words.map(([w, a, b]) => [w, a + t0, b + t0]); segs.push(s); });
      t0 += dur + (ui === units.length - 1 ? (opts.tail || 1.2) : (opts.gap || 0.5));
    });
    const total = t0;
    // capa não pode ficar parada: segura ~1.3s e corta para a cena seguinte (com movimento e legenda)
    for (let i = segs.length - 1; i >= 0; i--) {
      const sg = segs[i]; const sc = sg.scene;
      if (sg.card || !sc || sc.type !== "capa" || sg.end - sg.start < 2.2) continue;
      const dep = sc.depois || (sc.foto ? { type: "image", media: sc.foto, z0: 1.12, z1: 1.28, dim: 0.3 } : null);
      if (dep) segs.splice(i + 1, 0, { text: "", scene: JSON.parse(JSON.stringify(dep)), start: sg.start + 1.3, end: sg.end, extra: true });
    }
    segs.forEach((sg, i) => { sg.s0 = i === 0 ? 0 : sg.start - 0.05; sg.s1 = i + 1 < segs.length ? segs[i + 1].start - 0.05 : total; if (sg.card) { sg.s0 = sg.start; sg.s1 = sg.end; } });
    // "same" continua a cena anterior
    segs.forEach((sg, k) => {
      if (sg.scene && sg.scene.type === "same") return;
      let j = k; while (j + 1 < segs.length && segs[j + 1].scene && segs[j + 1].scene.type === "same") j++;
      sg.head = k; sg.headEnd = segs[j].s1; sg.scene._cues = []; for (let m = k; m <= j; m++) { segs[m].head = k; sg.scene._cues.push(segs[m].start - sg.s0); }
      for (let m = k + 1; m <= j; m++) segs[m].headEnd = segs[j].s1;
    });
    const chunks = buildWords(segs.filter((s) => !s.card));
    const cuts = segs.filter((s) => !(s.scene && s.scene.type === "same")).map((s) => s.s0);
    const voice = new Float32Array(Math.ceil(total * SR));
    voiceParts.forEach(([off, v]) => voice.set(v.subarray(0, Math.min(v.length, voice.length - Math.round(off * SR))), Math.round(off * SR)));
    const bed = synthBed(total, opts.batida ? cuts : []); /* sem o "bum" nas trocas de cena */ const mix = new Float32Array(voice.length);
    for (let i = 0; i < mix.length; i++) { let v = voice[i] + bed[i]; if (Math.abs(v) > 0.95) v = Math.sign(v) * 0.95; mix[i] = v; }
    return { segs, total, chunks, audio: mix, hook: !!opts.hook };
  }

  function segAt(tl, t) {
    const s = tl.segs; let lo = 0, hi = s.length - 1;
    while (lo < hi) { const m = (lo + hi + 1) >> 1; if (s[m].s0 <= t) lo = m; else hi = m - 1; }
    return lo;
  }

  class Renderer {
    constructor(canvas, vertical) {
      this.canvas = canvas; this.vertical = vertical;
      const W = vertical ? 1080 : 1920, H = vertical ? 1920 : 1080; canvas.width = W; canvas.height = H;
      this.ctx = canvas.getContext("2d"); this.c = { W, H, vertical, u: Math.min(W, H) / 1080, cx: W / 2, cy: H * (vertical ? 0.40 : 0.45) };
      this.bg = new Background(W, H);
    }
    activeScene(tl, t) {
      const i = segAt(tl, t); const sg = tl.segs[i]; const head = tl.segs[sg.head === undefined ? i : sg.head];
      return { sg, head, scene: head.scene || {}, lt: t - head.s0, dur: (sg.headEnd || sg.s1) - head.s0, first: (sg.head === 0) };
    }
    async syncMedia(tl, t, media) { // posiciona clipes de vídeo no tempo certo (render offline)
      const { scene, lt } = this.activeScene(tl, t);
      if (scene.type === "video" && media && media[scene.media] && media[scene.media].video) {
        const v = media[scene.media].video; const d = v.duration || 1; const target = ((scene.start || 0) + lt) % Math.max(0.1, d - 0.05);
        if (Math.abs(v.currentTime - target) > 0.01) await new Promise((res) => { const done = () => { v.removeEventListener("seeked", done); res(); }; v.addEventListener("seeked", done); v.currentTime = target; setTimeout(done, 400); });
      }
    }
    draw(tl, t, i, media) {
      const { ctx, c } = this; const a = this.activeScene(tl, t); const sc = a.scene; let lt = a.lt;
      if (tl.hook && a.first) lt += 0.9;
      const tint = sc.tint === "red" ? COL.red : null;
      this.bg.draw(ctx, i, t, tint ? COL.red : COL.gold, tint ? 0.16 : 0.10, tint);
      (S[sc.type] || S.bigtext)(ctx, c, lt, a.dur, sc, media);
      const endT = a.head.s0 + a.dur;
      if (endT - t < 0.12 && endT < tl.total - 0.1) { ctx.fillStyle = `rgba(0,0,0,${(1 - (endT - t) / 0.12) * 0.8})`; ctx.fillRect(0, 0, c.W, c.H); }
      if (sc.type !== "endcard" && sc.type !== "chapter" && sc.type !== "capa") drawCaptions(ctx, c, t, tl.chunks, tl.safe);
      if (c.vertical) { ctx.fillStyle = css(COL.gold); ctx.fillRect(0, 0, c.W * t / tl.total, 10); }
      drawC(ctx, "CUSTO OCULTO", font(900, 30 * c.u), c.cx, c.H * (tl.safe ? 0.15 : c.vertical ? 0.085 : 0.06), { alpha: 0.45 });
    }
  }

  // ---------- exportação ----------
  async function pickCodecs(W, H) {
    if (!global.VideoEncoder || !global.AudioEncoder || !global.Mp4Muxer) return null;
    const vcands = [["avc", "avc1.640028"], ["avc", "avc1.4d0028"], ["avc", "avc1.42003e"], ["vp9", "vp09.00.40.08"]];
    let video = null;
    for (const [mux, codec] of vcands) {
      try { const r = await VideoEncoder.isConfigSupported({ codec, width: W, height: H, bitrate: 6e6, framerate: 30 }); if (r.supported) { video = { mux, codec }; break; } } catch (e) {}
    }
    let audio = null;
    for (const [mux, codec] of [["aac", "mp4a.40.2"], ["opus", "opus"]]) {
      try { const r = await AudioEncoder.isConfigSupported({ codec, sampleRate: SR, numberOfChannels: 1, bitrate: 128000 }); if (r.supported) { audio = { mux, codec }; break; } } catch (e) {}
    }
    return video && audio ? { video, audio } : null;
  }

  async function exportMp4(tl, vertical, media, onProgress, signal) {
    const canvas = document.createElement("canvas"); const R = new Renderer(canvas, vertical); const { W, H } = R.c; const fps = 30;
    const codecs = await pickCodecs(W, H);
    if (!codecs) return exportRealtime(tl, vertical, media, onProgress, signal);
    const target = new Mp4Muxer.ArrayBufferTarget();
    const muxer = new Mp4Muxer.Muxer({ target, video: { codec: codecs.video.mux, width: W, height: H, frameRate: fps }, audio: { codec: codecs.audio.mux, numberOfChannels: 1, sampleRate: SR }, fastStart: "in-memory", firstTimestampBehavior: "offset" });
    let err = null;
    const venc = new VideoEncoder({ output: (ch, meta) => muxer.addVideoChunk(ch, meta), error: (e) => { err = e; } });
    venc.configure({ codec: codecs.video.codec, width: W, height: H, bitrate: vertical ? 5e6 : 7e6, framerate: fps });
    const aenc = new AudioEncoder({ output: (ch, meta) => muxer.addAudioChunk(ch, meta), error: (e) => { err = e; } });
    aenc.configure({ codec: codecs.audio.codec, sampleRate: SR, numberOfChannels: 1, bitrate: 128000 });
    const step = SR; // 1 s por bloco
    for (let i = 0; i < tl.audio.length; i += step) {
      const chunk = tl.audio.slice(i, Math.min(tl.audio.length, i + step));
      const ad = new AudioData({ format: "f32-planar", sampleRate: SR, numberOfFrames: chunk.length, numberOfChannels: 1, timestamp: Math.round(i / SR * 1e6), data: chunk });
      aenc.encode(ad); ad.close();
    }
    const nfr = Math.floor(tl.total * fps);
    for (let i = 0; i < nfr; i++) {
      if (signal && signal.aborted) throw new DOMException("cancelado", "AbortError");
      if (err) throw err;
      const t = i / fps; await R.syncMedia(tl, t, media); R.draw(tl, t, i, media);
      const fr = new VideoFrame(canvas, { timestamp: Math.round(t * 1e6), duration: Math.round(1e6 / fps) });
      venc.encode(fr, { keyFrame: i % 60 === 0 }); fr.close();
      while (venc.encodeQueueSize > 8) await new Promise((r) => setTimeout(r, 4));
      if (i % 15 === 0) { onProgress && onProgress(i / nfr); await new Promise((r) => setTimeout(r, 0)); }
    }
    await venc.flush(); await aenc.flush(); if (err) throw err; muxer.finalize();
    onProgress && onProgress(1);
    return { blob: new Blob([target.buffer], { type: "video/mp4" }), ext: "mp4", codec: codecs.video.codec };
  }

  // reserva: grava em tempo real (WebM) quando o navegador não tem WebCodecs
  async function exportRealtime(tl, vertical, media, onProgress, signal) {
    const canvas = document.createElement("canvas"); const R = new Renderer(canvas, vertical);
    const ac = new AudioContext({ sampleRate: SR }); const buf = ac.createBuffer(1, tl.audio.length, SR); buf.copyToChannel(tl.audio, 0);
    const src = ac.createBufferSource(); src.buffer = buf; const dest = ac.createMediaStreamDestination(); src.connect(dest);
    const stream = new MediaStream([...canvas.captureStream(30).getVideoTracks(), ...dest.stream.getAudioTracks()]);
    const mime = ["video/webm;codecs=vp9,opus", "video/webm;codecs=vp8,opus", "video/webm"].find((m) => MediaRecorder.isTypeSupported(m));
    const rec = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 6e6 }); const parts = []; rec.ondataavailable = (e) => e.data.size && parts.push(e.data);
    const done = new Promise((r) => (rec.onstop = r)); rec.start(1000); const t0 = ac.currentTime + 0.1; src.start(t0); let i = 0;
    await new Promise((resolve, reject) => {
      const tick = async () => {
        if (signal && signal.aborted) { rec.stop(); src.stop(); reject(new DOMException("cancelado", "AbortError")); return; }
        const t = ac.currentTime - t0; if (t >= tl.total) { resolve(); return; }
        if (t >= 0) { await R.syncMedia(tl, t, media); R.draw(tl, t, i++, media); onProgress && onProgress(t / tl.total); }
        requestAnimationFrame(tick);
      }; tick();
    });
    rec.stop(); await done; ac.close();
    return { blob: new Blob(parts, { type: "video/webm" }), ext: "webm", codec: mime };
  }

  function toSrt(tl) {
    const ts = (x) => { const h = Math.floor(x / 3600), m = Math.floor((x % 3600) / 60), s = Math.floor(x % 60), ms = Math.round((x - Math.floor(x)) * 1000);
      return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")},${String(Math.min(ms, 999)).padStart(3, "0")}`; };
    let n = 1; const out = [];
    tl.segs.filter((s) => s.text).forEach((sg) => {
      const words = String(sg.cap || sg.text).split(/\s+/); const chunks = []; const nCh = Math.ceil(words.length / 12), per = Math.ceil(words.length / nCh); for (let i = 0; i < words.length; i += per) chunks.push(words.slice(i, i + per).join(" "));
      const tot = chunks.reduce((a, c) => a + c.length, 0) || 1; let t = sg.start;
      chunks.forEach((c) => { const d = (sg.end - sg.start) * c.length / tot; out.push(`${n++}\n${ts(t)} --> ${ts(t + d)}\n${c}\n`); t += d; });
    });
    return out.join("\n");
  }
  function chapterMarks(tl) {
    const marks = []; tl.segs.forEach((s, i) => { if (i === 0) marks.push([0, "Introdução"]); else if (s.card && s.scene.type === "chapter") marks.push([s.s0, s.scene.title]); });
    return marks.map(([t, n]) => `${String(Math.floor(t / 60)).padStart(2, "0")}:${String(Math.floor(t % 60)).padStart(2, "0")} ${n.charAt(0) + n.slice(1).toLowerCase()}`).join("\n");
  }

  // miniatura
  function drawThumb(canvas, cfg) {
    canvas.width = 1280; canvas.height = 720; const ctx = canvas.getContext("2d"); const bg = new Background(1280, 720);
    bg.draw(ctx, 0, 1, col(cfg.glow, COL.gold), 0.22);
    const lines = cfg.lines.filter((l) => l.text); const sizes = lines.map((l) => fitSize(ctx, l.text, 900, l.size, 1180));
    const total = sizes.reduce((a, b) => a + b * 1.08, 0); let y = 360 - total / 2;
    lines.forEach((l, i) => { const h = sizes[i] * 1.08;
      if (l.pill) { const f = font(900, sizes[i]); const tw = textW(ctx, l.text, f) + 80; box(ctx, 640 - tw / 2, y + 6, tw, h - 12, (h - 12) / 2, col(l.color), 1); drawC(ctx, l.text, f, 640, y + h / 2, { fill: [15, 15, 15] }); }
      else drawC(ctx, l.text, font(900, sizes[i]), 640, y + h / 2, { fill: col(l.color), shadow: 18 });
      y += h; });
  }

  function drawCapa(canvas, scene, media, vertical) {
    const R = new Renderer(canvas, vertical); R.bg.draw(R.ctx, 0, 1); S.capa(R.ctx, R.c, 3, 5, scene, media); return canvas;
  }
  global.COEngine = { drawCapa, COL, Renderer, buildTimeline, decodeAudio, prepVoice, align, exportMp4, toSrt, chapterMarks, drawThumb, SCENES: S, SR, pickCodecs };
})(window);

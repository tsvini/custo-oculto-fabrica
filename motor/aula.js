/* Cenas didáticas para aulas (curso Cypress para leigos): editor de código, terminal, passo a passo,
   pastas, cards de conceito e gravação de tela emoldurada. Registra em COEngine.SCENES. */
(function (global) {
  "use strict";
  const S = global.COEngine.SCENES;
  const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
  const MONO = "'JetBrains Mono', 'Courier New', monospace";
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const easeOut = (x) => { x = clamp(x); return 1 - Math.pow(1 - x, 3); };
  const backOut = (x) => { x = clamp(x); const c1 = 1.70158, c3 = 2.70158; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
  const lerp = (a, b, t) => a + (b - a) * t;
  const font = (w, s, f) => `${w} ${Math.max(1, Math.round(s))}px ${f || FONT}`;
  // paleta das aulas: verde Cypress + tons de editor escuro
  const C = { ac: "#3fd68a", ac2: "#69a7ff", yel: "#ffd23f", red: "#ff6b6b", txt: "#e8eaf0", mut: "#8b93a7",
    win: "#1b1e27", bar: "#252936", side: "#20232e", line: "#2c3140", term: "#0f1117", folder: "#f5c542" };
  function rr(ctx, x, y, w, h, r) { r = Math.min(r, w / 2, h / 2); ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function txt(ctx, t, f, x, y, fill, align = "left", alpha = 1) { if (!t || alpha <= 0.01) return; ctx.save(); ctx.globalAlpha *= alpha; ctx.font = f; ctx.textAlign = align; ctx.textBaseline = "middle"; ctx.fillStyle = fill; ctx.fillText(t, x, y); ctx.restore(); }
  function tw(ctx, t, f) { ctx.font = f; return ctx.measureText(t).width; }

  // janela com sombra e barra de título (3 bolinhas)
  function janela(ctx, x, y, w, h, u, titulo, a, cor = C.win) {
    ctx.save(); ctx.globalAlpha *= a;
    ctx.shadowColor = "rgba(0,0,0,.6)"; ctx.shadowBlur = 60 * u; ctx.shadowOffsetY = 24 * u;
    rr(ctx, x, y, w, h, 22 * u); ctx.fillStyle = cor; ctx.fill(); ctx.shadowColor = "transparent";
    ctx.save(); rr(ctx, x, y, w, h, 22 * u); ctx.clip(); ctx.fillStyle = C.bar; ctx.fillRect(x, y, w, 64 * u); ctx.restore();
    ["#ff5f57", "#febc2e", "#28c840"].forEach((c, i) => { ctx.beginPath(); ctx.arc(x + (36 + i * 34) * u, y + 32 * u, 10 * u, 0, 7); ctx.fillStyle = c; ctx.fill(); });
    txt(ctx, titulo, font(600, 26 * u), x + w / 2, y + 32 * u, C.mut, "center");
    ctx.strokeStyle = "rgba(255,255,255,.07)"; ctx.lineWidth = 2 * u; rr(ctx, x, y, w, h, 22 * u); ctx.stroke();
    ctx.restore(); return y + 64 * u;
  }
  // cursor do mouse: vem de baixo, para no alvo e "clica" (anel) em t_click
  function cursor(ctx, u, x, y, t, tc) {
    const k = easeOut((t - (tc - 0.9)) / 0.8); if (k <= 0) return;
    const cx = lerp(x + 260 * u, x, k), cy = lerp(y + 200 * u, y, k);
    const p = (t - tc) / 0.45; if (p > 0 && p < 1) { ctx.save(); ctx.globalAlpha = 1 - p; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; ctx.beginPath(); ctx.arc(x, y, (14 + 46 * p) * u, 0, 7); ctx.stroke(); ctx.restore(); }
    const sc = p > 0 && p < 0.25 ? 0.85 : 1; ctx.save(); ctx.translate(cx, cy); ctx.scale(sc * u * 1.6, sc * u * 1.6);
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, 26); ctx.lineTo(7, 20); ctx.lineTo(12, 31); ctx.lineTo(17, 29); ctx.lineTo(12, 18); ctx.lineTo(21, 18); ctx.closePath();
    ctx.fillStyle = "#fff"; ctx.strokeStyle = "#111"; ctx.lineWidth = 1.6; ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 6; ctx.fill(); ctx.stroke(); ctx.restore();
  }
  const topo = (c, H) => (c.vertical ? c.H * 0.2 : c.H * 0.38 - H / 2);  // janelas acima da faixa e da legenda karaokê
  function legenda(ctx, c, t, s) {  // faixa explicativa embaixo da janela
    if (!s.legenda) return; const u = c.u; const a = easeOut((t - (s.legenda_em || 0.6)) / 0.4); if (a <= 0) return;
    const f = font(800, 44 * u); const w = tw(ctx, s.legenda, f) + 80 * u; const y = c.H * (c.vertical ? 0.80 : 0.795);
    ctx.save(); ctx.globalAlpha = a; rr(ctx, c.cx - w / 2, y - 44 * u + (1 - a) * 20 * u, w, 88 * u, 44 * u); ctx.fillStyle = C.ac; ctx.fill(); ctx.restore();
    txt(ctx, s.legenda, f, c.cx, y + (1 - a) * 20 * u, "#0b1a12", "center", a);
  }

  function pastaIcone(ctx, x, y, s, a, cor = C.folder) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = cor;
    rr(ctx, x, y, s * 0.42, s * 0.2, s * 0.05); ctx.fill(); rr(ctx, x, y + s * 0.1, s, s * 0.7, s * 0.07); ctx.fill();
    ctx.fillStyle = "rgba(255,255,255,.25)"; rr(ctx, x, y + s * 0.18, s, s * 0.08, s * 0.03); ctx.fill(); ctx.restore(); }
  // destaque de sintaxe simples (JS)
  const KW = /^(const|let|var|function|return|if|else|describe|it|context|beforeEach|before|after|afterEach|async|await|new|import|from|export|default)$/;
  function tokens(linha) {
    const out = []; const re = /(\/\/.*$)|('[^']*'|"[^"]*"|`[^`]*`)|(\b\d+\b)|([A-Za-z_$][\w$]*)|(\s+)|(.)/g; let m;
    while ((m = re.exec(linha))) {
      if (m[1]) out.push([m[1], C.mut]); else if (m[2]) out.push([m[2], "#f0a868"]); else if (m[3]) out.push([m[3], "#c792ea"]);
      else if (m[4]) { const nx = linha.slice(re.lastIndex).trimStart()[0]; out.push([m[4], KW.test(m[4]) ? "#c792ea" : m[4] === "cy" ? C.ac : nx === "(" ? C.ac2 : C.txt]); }
      else out.push([m[0], C.txt]);
    }
    return out;
  }

  // EDITOR: {type:"editor", arquivo:"login.cy.js", codigo:"linhas\n...", digitar:true, destaque:[3,4], legenda:"...", pastas:["cypress","e2e","login.cy.js"]}
  S.editor = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const sc = lerp(0.96, 1, backOut(t / 0.5));
    const W = (c.vertical ? 1000 : 1500) * u, H = (c.vertical ? 1100 : 700) * u; const x = c.cx - W / 2, y = topo(c, H);
    ctx.save(); ctx.translate(c.cx, y + H / 2); ctx.scale(sc, sc); ctx.translate(-c.cx, -(y + H / 2));
    const top = janela(ctx, x, y, W, H, u, (s.arquivo || "arquivo.js") + " — Visual Studio Code", a);
    const sideW = s.pastas && !c.vertical ? 330 * u : 0;
    if (sideW) {
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.side; ctx.fillRect(x, top, sideW, H - (top - y) - 22 * u); ctx.restore();
      txt(ctx, "EXPLORER", font(700, 20 * u), x + 28 * u, top + 36 * u, C.mut, "left", a);
      s.pastas.forEach((p, i) => {
        const yy = top + (86 + i * 50) * u, ind = Math.min(i, 4) * 22 * u, arq = /\.\w+$/.test(p);
        if (arq) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = C.ac; rr(ctx, x + 32 * u + ind, yy - 13 * u, 20 * u, 26 * u, 4 * u); ctx.fill(); ctx.restore(); }
        else pastaIcone(ctx, x + 28 * u + ind, yy - 14 * u, 30 * u, a);
        txt(ctx, p, font(arq ? 600 : 500, 24 * u), x + 68 * u + ind, yy, arq ? C.ac : C.txt, "left", a);
      });
    }
    // aba
    const tabX = x + sideW; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.win; ctx.fillRect(tabX, top, 300 * u, 56 * u); ctx.fillStyle = C.ac; ctx.fillRect(tabX, top, 300 * u, 4 * u); ctx.restore();
    txt(ctx, s.arquivo || "arquivo.js", font(600, 24 * u), tabX + 28 * u, top + 30 * u, C.txt, "left", a);
    const linhas = String(s.codigo || "").split("\n"); const total = linhas.join("").length || 1;
    const fs = (s.fonte || (linhas.length > 12 ? 30 : 36)) * u; const lh = fs * 1.55; const x0 = tabX + 96 * u; let yy = top + 100 * u;
    const d0 = s.digitar_de || ((s.destaque && s.destaque.length) ? Math.min(...s.destaque) : 1);  // linhas antes disso já estão escritas
    const pronto = linhas.slice(0, d0 - 1).join("").length; const falta = Math.max(1, total - pronto);
    const k = s.digitar === false ? 1 : clamp((t - 0.5) / Math.max(0.8, Math.min(dur * (s.vel || 0.7), falta / 18)));
    const dig = k; let resta = pronto + Math.floor(k * falta);
    linhas.forEach((ln, i) => {
      const hl = (s.destaque || []).includes(i + 1);
      if (hl && dig >= 1) { const ha = easeOut((t - 0.5 - Math.max(0.8, Math.min(dur * (s.vel || 0.7), falta / 18))) / 0.4); ctx.save(); ctx.globalAlpha = 0.18 * ha; ctx.fillStyle = C.ac; ctx.fillRect(tabX, yy - lh / 2, W - sideW, lh); ctx.globalAlpha = ha; ctx.fillRect(tabX, yy - lh / 2, 6 * u, lh); ctx.restore(); }
      txt(ctx, String(i + 1), font(500, fs * 0.8, MONO), x0 - 30 * u, yy, "#4b5263", "right", a);
      let mostra = Math.min(ln.length, resta); resta -= ln.length; let xx = x0;
      for (const [tk, cor] of tokens(ln)) { if (mostra <= 0) break; const parte = tk.slice(0, mostra); mostra -= tk.length; txt(ctx, parte, font(500, fs, MONO), xx, yy, cor, "left", a); xx += tw(ctx, parte, font(500, fs, MONO)); }
      if (dig < 1 && resta < 0 && resta + ln.length >= 0 && Math.floor(t * 2.5) % 2 === 0) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.ac; ctx.fillRect(xx + 2 * u, yy - fs * 0.6, 4 * u, fs * 1.2); ctx.restore(); }
      yy += lh;
    });
    ctx.restore(); legenda(ctx, c, t, s);
  };

  // TERMINAL: {type:"terminal", pasta:"C:\\Users\\voce\\meu-projeto", linhas:[{cmd:"node -v"},{out:"v22.11.0", cor:"ac"}], legenda:"..."}
  S.terminal = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 1000 : 1400) * u, H = (c.vertical ? 900 : 640) * u;
    const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, s.titulo || "Terminal", a, C.term);
    const fs = 34 * u, lh = fs * 1.7; let yy = top + 60 * u; const pr = (s.prompt || "PS " + (s.pasta || "C:\\meu-projeto") + ">") + " ";
    const L = s.linhas || []; const passo = Math.max(0.6, (dur - 1) / Math.max(L.length, 1)); let tt = t - 0.5;
    for (const l of L) {
      if (tt < 0) break;
      if (l.cmd !== undefined) {
        const k = clamp(tt / Math.max(0.4, passo * 0.6)); const cmd = l.cmd.slice(0, Math.ceil(k * l.cmd.length));
        txt(ctx, pr, font(600, fs, MONO), x + 40 * u, yy, C.ac2, "left", a);
        const px = x + 40 * u + tw(ctx, pr, font(600, fs, MONO)); txt(ctx, cmd, font(600, fs, MONO), px, yy, C.txt, "left", a);
        if (k < 1 && Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = C.txt; ctx.fillRect(px + tw(ctx, cmd, font(600, fs, MONO)) + 4 * u, yy - fs * 0.55, fs * 0.55, fs * 1.1); }
      } else {
        txt(ctx, l.out, font(500, fs, MONO), x + 40 * u, yy, C[l.cor] || l.cor || C.mut, "left", a * easeOut(tt / 0.3));
      }
      yy += lh; tt -= l.cmd !== undefined ? passo : passo * 0.35;
    }
    legenda(ctx, c, t, s);
  };

  // PASSO: {type:"passo", n:1, de:4, titulo:"Baixe o VS Code", sub:"code.visualstudio.com", icone:"⬇"}
  S.passo = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.35); const k = backOut(t / 0.5);
    const R = 120 * u * lerp(0.6, 1, k); const cy = c.cy - 120 * u;
    ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(c.cx, cy, R + 18 * u, 0, 7); ctx.fillStyle = "rgba(63,214,138,.15)"; ctx.fill();
    ctx.beginPath(); ctx.arc(c.cx, cy, R, 0, 7); ctx.fillStyle = C.ac; ctx.fill(); ctx.restore();
    txt(ctx, s.icone || String(s.n || 1), font(900, R * 0.95), c.cx, cy + 6 * u, "#0b1a12", "center", a);
    if (s.de) txt(ctx, `PASSO ${s.n} DE ${s.de}`, font(800, 34 * u), c.cx, cy + R + 70 * u, C.ac, "center", easeOut((t - 0.2) / 0.3));
    const f = font(900, Math.min(110, 1700 / Math.max(8, (s.titulo || "").length) * 1.6) * u);
    txt(ctx, (s.titulo || "").toUpperCase(), f, c.cx, cy + R + 160 * u, C.txt, "center", easeOut((t - 0.3) / 0.35));
    if (s.sub) { const fs = font(600, 44 * u, s.mono ? MONO : FONT); const w = tw(ctx, s.sub, fs) + 60 * u; const ya = easeOut((t - 0.55) / 0.35);
      ctx.save(); ctx.globalAlpha = ya; rr(ctx, c.cx - w / 2, cy + R + 225 * u, w, 76 * u, 16 * u); ctx.fillStyle = C.bar; ctx.fill(); ctx.restore();
      txt(ctx, s.sub, fs, c.cx, cy + R + 263 * u, C.yel, "center", ya); }
    if (s.de) { const bw = 600 * u, bx = c.cx - bw / 2, by = c.H - 90 * u; ctx.save(); ctx.globalAlpha = a; rr(ctx, bx, by, bw, 12 * u, 6 * u); ctx.fillStyle = C.line; ctx.fill();
      rr(ctx, bx, by, bw * lerp((s.n - 1) / s.de, s.n / s.de, easeOut((t - 0.3) / 0.8)), 12 * u, 6 * u); ctx.fillStyle = C.ac; ctx.fill(); ctx.restore(); }
  };

  // PASTAS: {type:"pastas", caminho:"Este Computador > Documentos", itens:["Fotos","Trabalho",{"nome":"meu-projeto","novo":true}], legenda:"..."}
  S.pastas = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 1000 : 1500) * u, H = (c.vertical ? 1000 : 660) * u;
    const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "Explorador de Arquivos", a, "#f3f4f7");
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#e4e7ee"; ctx.fillRect(x, top, W, 70 * u); ctx.restore();
    pastaIcone(ctx, x + 34 * u, top + 18 * u, 40 * u, a);
    txt(ctx, s.caminho || "Documentos", font(600, 28 * u), x + 92 * u, top + 35 * u, "#3a3f4b", "left", a);
    const itens = (s.itens || []).map((i) => (typeof i === "string" ? { nome: i } : i)); const cols = c.vertical ? 3 : 5; const cell = (W - 80 * u) / cols;
    itens.forEach((it, i) => {
      const cx = x + 40 * u + (i % cols) * cell + cell / 2, cy = top + 130 * u + Math.floor(i / cols) * 250 * u;
      const st = it.novo ? (s.novo_em || 1.0) : 0.15 + i * 0.08; const k = backOut((t - st) / 0.45); const ka = easeOut((t - st) / 0.3);
      if (ka <= 0) return; const sz = 150 * u * (it.novo ? lerp(0.4, 1, k) : 1);
      if (it.novo && t > st + 0.5) { ctx.save(); ctx.globalAlpha = 0.25 * easeOut((t - st - 0.5) / 0.4); rr(ctx, cx - cell / 2 + 20 * u, cy - 20 * u, cell - 40 * u, 230 * u, 18 * u); ctx.fillStyle = C.ac2; ctx.fill(); ctx.restore(); }
      pastaIcone(ctx, cx - sz / 2, cy + (150 * u - sz) / 2, sz, ka, it.arquivo ? "#9aa3b5" : C.folder);
      const nome = it.novo ? it.nome.slice(0, Math.ceil(clamp((t - st - 0.6) / 0.8) * it.nome.length)) : it.nome;
      txt(ctx, nome, font(it.novo ? 800 : 600, 30 * u), cx, cy + 180 * u, "#2a2f3a", "center", ka);
    });
    legenda(ctx, c, t, s);
  };

  // CARDS: {type:"cards", titulo:"O QUE VAMOS INSTALAR", itens:[["✎","VS Code","onde você escreve o código"],["⬢","Node.js","o motor que roda o Cypress"],["⑂","Git","guarda o histórico"]]}
  S.cards = (ctx, c, t, dur, s) => {
    const u = c.u; const it = s.itens || []; const n = it.length; const V = c.vertical;
    const cw = V ? 860 * u : Math.min(520, 1700 / n - 40) * u, ch = V ? 300 * u : 560 * u, gap = 44 * u;
    if (s.titulo) txt(ctx, s.titulo, font(800, 46 * u), c.cx, V ? c.H * 0.16 : c.cy - ch / 2 - 90 * u, C.mut, "center", easeOut(t / 0.3));
    const passo = Math.min(1.0, (dur - 0.6) / Math.max(n, 1));
    it.forEach(([ic, ti, sub, cor], i) => {
      const st = s.juntos ? 0.2 : 0.2 + i * passo; const ka = easeOut((t - st) / 0.35), k = backOut((t - st) / 0.45); if (ka <= 0) return;
      const x = V ? c.cx - cw / 2 : c.cx - (n * cw + (n - 1) * gap) / 2 + i * (cw + gap), y = V ? c.H * 0.22 + i * (ch + gap) : c.cy - ch / 2;
      ctx.save(); ctx.globalAlpha = ka; ctx.translate(x + cw / 2, y + ch / 2); ctx.scale(lerp(0.9, 1, k), lerp(0.9, 1, k)); ctx.translate(-(x + cw / 2), -(y + ch / 2));
      ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 40 * u; rr(ctx, x, y, cw, ch, 28 * u); ctx.fillStyle = C.win; ctx.fill(); ctx.shadowColor = "transparent";
      ctx.fillStyle = cor || C.ac; rr(ctx, x, y, cw, 10 * u, 5 * u); ctx.fill();
      const icY = V ? y + ch / 2 : y + 170 * u, icX = V ? x + 150 * u : x + cw / 2;
      ctx.beginPath(); ctx.arc(icX, icY, 80 * u, 0, 7); ctx.fillStyle = "rgba(255,255,255,.06)"; ctx.fill(); ctx.restore();
      txt(ctx, ic, font(800, 84 * u), icX, icY + 4 * u, cor || C.ac, "center", ka);
      if (V) { txt(ctx, ti, font(900, 60 * u), x + 280 * u, y + ch / 2 - 36 * u, C.txt, "left", ka); txt(ctx, sub, font(500, 34 * u), x + 280 * u, y + ch / 2 + 34 * u, C.mut, "left", ka); }
      else { txt(ctx, ti, font(900, 58 * u), x + cw / 2, y + 330 * u, C.txt, "center", ka);
        const ws = String(sub || "").split(" "); let l1 = "", l2 = ""; ws.forEach((w) => { if ((l1 + " " + w).length < 22 && !l2) l1 = (l1 + " " + w).trim(); else l2 = (l2 + " " + w).trim(); });
        txt(ctx, l1, font(500, 32 * u), x + cw / 2, y + 410 * u, C.mut, "center", ka); txt(ctx, l2, font(500, 32 * u), x + cw / 2, y + 455 * u, C.mut, "center", ka); }
    });
  };

  // TELA: gravação de tela (clipe em midia/) emoldurada, com zoom e caixa de destaque
  // {type:"tela", media:"instala_vscode", titulo:"code.visualstudio.com", zoom:[x0,y0,x1,y1] (0–1), zoom_em:2, caixa:[x0,y0,x1,y1], legenda:"..."}
  S.tela = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const m = media && media[s.media];
    const W = (c.vertical ? 1000 : 1200) * u, H = W * 9 / 16 + 64 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, s.titulo || "", a);
    const vw = W, vh = H - (top - y); ctx.save(); rr(ctx, x, top, vw, vh, 0); ctx.clip();
    const el = m && (m.video || m.img);
    if (el) {
      const iw = el.videoWidth || el.width, ih = el.videoHeight || el.height; let [zx0, zy0, zx1, zy1] = [0, 0, 1, 1];
      if (s.zoom) { const k = easeOut((t - (s.zoom_em || 1.5)) / 0.8); zx0 = lerp(0, s.zoom[0], k); zy0 = lerp(0, s.zoom[1], k); zx1 = lerp(1, s.zoom[2], k); zy1 = lerp(1, s.zoom[3], k); }
      ctx.globalAlpha = a; ctx.drawImage(el, zx0 * iw, zy0 * ih, (zx1 - zx0) * iw, (zy1 - zy0) * ih, x, top, vw, vh);
      if (s.caixa) { const k = easeOut((t - (s.caixa_em || 1.2)) / 0.4); const [bx0, by0, bx1, by1] = s.caixa; const fx = (v) => x + (v - zx0) / (zx1 - zx0) * vw, fy = (v) => top + (v - zy0) / (zy1 - zy0) * vh;
        ctx.globalAlpha = k; ctx.strokeStyle = C.yel; ctx.lineWidth = 8 * u; rr(ctx, fx(bx0), fy(by0), fx(bx1) - fx(bx0), fy(by1) - fy(by0), 14 * u); ctx.stroke();
        ctx.globalAlpha = 1; cursor(ctx, u, (fx(bx0) + fx(bx1)) / 2, (fy(by0) + fy(by1)) / 2, t, (s.caixa_em || 1.2) + 0.9); }
    } else { ctx.fillStyle = "#11131a"; ctx.fillRect(x, top, vw, vh); txt(ctx, "[ gravação: " + (s.media || "?") + " ]", font(700, 40 * u), c.cx, top + vh / 2, C.mut, "center", a); }
    ctx.restore(); legenda(ctx, c, t, s);
  };
  // INSTALADOR (desenhado): {type:"instalador", app:"Visual Studio Code", titulo:"Select Additional Tasks", texto:"...", caixas:[["Add to PATH",true]], botao:"Next", progresso:false, legenda:"..."}
  S.instalador = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 980 : 1240) * u, H = (c.vertical ? 900 : 680) * u;
    const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "Setup - " + (s.app || "Programa"), a, "#f4f5f8");
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#ffffff"; ctx.fillRect(x, top, W, 130 * u); ctx.fillStyle = "#e3e6ec"; ctx.fillRect(x, top + 130 * u, W, 2 * u); ctx.restore();
    txt(ctx, s.titulo || "", font(800, 40 * u), x + 50 * u, top + 52 * u, "#1d2230", "left", a);
    txt(ctx, s.subtitulo || "", font(500, 28 * u), x + 50 * u, top + 98 * u, "#5d6577", "left", a);
    let yy = top + 200 * u;
    String(s.texto || "").split("\n").forEach((l) => { txt(ctx, l, font(500, 30 * u), x + 50 * u, yy, "#2a2f3a", "left", a); yy += 46 * u; });
    (s.caixas || []).forEach(([rot, on], i) => {
      const cy = yy + 20 * u + i * 64 * u; const st = 0.8 + i * 0.6; const k = on ? easeOut((t - st) / 0.25) : 0;
      ctx.save(); ctx.globalAlpha = a; rr(ctx, x + 50 * u, cy - 18 * u, 36 * u, 36 * u, 6 * u); ctx.fillStyle = k > 0.5 ? "#2f6fe4" : "#fff"; ctx.fill(); ctx.strokeStyle = "#8b93a7"; ctx.lineWidth = 2 * u; ctx.stroke();
      if (k > 0.5) { ctx.strokeStyle = "#fff"; ctx.lineWidth = 5 * u; ctx.beginPath(); ctx.moveTo(x + 58 * u, cy); ctx.lineTo(x + 66 * u, cy + 9 * u); ctx.lineTo(x + 80 * u, cy - 9 * u); ctx.stroke(); }
      if (on && t > st - 0.3 && t < st + 0.6) { ctx.strokeStyle = C.yel; ctx.lineWidth = 6 * u; rr(ctx, x + 40 * u, cy - 28 * u, 56 * u, 56 * u, 10 * u); ctx.stroke(); }
      ctx.restore(); txt(ctx, rot, font(600, 30 * u), x + 110 * u, cy, "#2a2f3a", "left", a);
    });
    if (s.progresso) { const k = clamp((t - 0.5) / Math.max(1, dur - 1)); const bw = W - 100 * u, by = top + 260 * u;
      ctx.save(); ctx.globalAlpha = a; rr(ctx, x + 50 * u, by, bw, 34 * u, 8 * u); ctx.fillStyle = "#e3e6ec"; ctx.fill(); rr(ctx, x + 50 * u, by, bw * k, 34 * u, 8 * u); ctx.fillStyle = "#2fb36a"; ctx.fill(); ctx.restore();
      txt(ctx, k < 1 ? "Instalando... " + Math.round(k * 100) + "%" : "Pronto!", font(700, 30 * u), x + 50 * u, by + 80 * u, "#2a2f3a", "left", a); }
    const bh = 64 * u, bw2 = 190 * u, by2 = y + H - bh - 40 * u;
    [["Cancel", false], [s.botao || "Next", true]].forEach(([rot, pri], i) => { const bx = x + W - (i === 0 ? 2 : 1) * (bw2 + 24 * u);
      ctx.save(); ctx.globalAlpha = a; rr(ctx, bx, by2, bw2, bh, 10 * u); ctx.fillStyle = pri ? "#2f6fe4" : "#fff"; ctx.fill(); ctx.strokeStyle = pri ? "#2f6fe4" : "#b9c0cc"; ctx.lineWidth = 2 * u; ctx.stroke();
      if (pri) { const k = easeOut((t - (s.botao_em || dur * 0.7)) / 0.3); if (k > 0) { ctx.strokeStyle = C.yel; ctx.globalAlpha = a * k; ctx.lineWidth = 7 * u; rr(ctx, bx - 10 * u, by2 - 10 * u, bw2 + 20 * u, bh + 20 * u, 14 * u); ctx.stroke(); } }
      ctx.restore(); txt(ctx, rot, font(700, 30 * u), bx + bw2 / 2, by2 + bh / 2, pri ? "#fff" : "#2a2f3a", "center", a);
      if (pri && !s.progresso) cursor(ctx, u, bx + bw2 * 0.55, by2 + bh * 0.6, t, (s.botao_em || dur * 0.7) + 0.35); });
    legenda(ctx, c, t, s);
  };
  // RUNNER do Cypress (desenhado): lista de comandos à esquerda, site à direita
  // {type:"runner", spec:"login.cy.js", teste:"entra com usuário e senha", passos:[["visit","saucedemo.com"],["get","#user-name"],["type","standard_user"]],
  //  media:"site_sauce", url:"https://www.saucedemo.com", status:"passou"|"falhou", erro:"Timed out retrying...", legenda:"..."}
  S.runner = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 1000 : 1640) * u, H = (c.vertical ? 1100 : 700) * u; const x = c.cx - W / 2, y = topo(c, H);
    const LW = c.vertical ? W : 600 * u; const P = s.passos || []; const falha = s.status === "falhou";
    // foco: "passo" (o passo que falhou/último), "lista" (os comandos), "erro" (a mensagem), "site", "status" (PASSOU/FALHOU)
    const t0 = y + 64 * u, ex0 = x + LW + 30 * u, ew0 = W - LW - 60 * u;
    const R = { lista: [x, t0 + 64 * u, LW, y + H - t0 - 64 * u], passo: [x, t0 + 160 * u + (P.length - 1) * 50 * u - 24 * u, LW, 48 * u],
      erro: [ex0 - 8 * u, y + H - 198 * u, ew0 + 16 * u, 166 * u], site: [x + LW, t0, W - LW, y + H - t0], status: [x + W - 330 * u, t0 + 16 * u, 310 * u, 90 * u] }[s.foco];
    const kf = R ? easeOut((t - (s.foco_em === undefined ? (s.pronto ? 0.5 : dur * 0.8) : s.foco_em)) / 0.6) : 0;
    const zf = R ? lerp(1, s.zoom || ({ passo: 1.12, erro: 1.12, status: 1.15 }[s.foco] || 1.04), kf) : 1;
    ctx.save(); if (R) { const fx = lerp(c.cx, R[0] + R[2] / 2, 0.6), fy = lerp(y + H / 2, R[1] + R[3] / 2, 0.6); ctx.translate(fx, fy); ctx.scale(zf, zf); ctx.translate(-fx, -fy); }
    const top = janela(ctx, x, y, W, H, u, "Cypress — " + (s.spec || "spec.cy.js"), a, "#1b1e27");
    const passo = Math.max(0.35, (dur * 0.75 - 0.6) / Math.max(P.length, 1)); const feitos = s.pronto ? P.length : clamp((t - 0.6) / passo, 0, P.length);
    const tFim = s.pronto ? 0 : 0.6 + P.length * passo;
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#171a22"; ctx.fillRect(x, top, LW, y + H - top - 2 * u); ctx.restore();
    const fim = feitos >= P.length; const ok = fim && !falha;
    txt(ctx, s.spec || "spec.cy.js", font(700, 24 * u, MONO), x + 28 * u, top + 34 * u, C.txt, "left", a);
    txt(ctx, (fim ? (falha ? "✗ 1" : "✓ 1") : "…"), font(800, 26 * u), x + LW - 30 * u, top + 34 * u, fim ? (falha ? C.red : C.ac) : C.mut, "right", a);
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.line; ctx.fillRect(x, top + 64 * u, LW, 2 * u); ctx.restore();
    const cor = fim ? (falha ? C.red : C.ac) : C.yel;
    ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(x + 40 * u, top + 104 * u, 11 * u, 0, 7); ctx.fillStyle = cor; ctx.fill(); ctx.restore();
    txt(ctx, s.teste || "teste", font(700, 28 * u), x + 66 * u, top + 104 * u, C.txt, "left", a);
    let yy = top + 160 * u;
    P.forEach(([cmd, arg], i) => {
      const k = clamp(feitos - i); if (k <= 0) return; const ultimo = falha && i === P.length - 1 && fim;
      if (ultimo) { ctx.save(); ctx.globalAlpha = 0.18; ctx.fillStyle = C.red; ctx.fillRect(x, yy - 22 * u, LW, 44 * u); ctx.restore(); }
      txt(ctx, String(i + 1), font(600, 22 * u, MONO), x + 40 * u, yy, "#4b5263", "center", a * k);
      txt(ctx, cmd, font(700, 25 * u, MONO), x + 70 * u, yy, ultimo ? C.red : "#69a7ff", "left", a * k);
      const cw = tw(ctx, cmd, font(700, 25 * u, MONO)); txt(ctx, String(arg || ""), font(600, 23 * u, MONO), x + 86 * u + cw, yy, C.txt, "left", a * k);
      yy += 50 * u;
    });
    if (!c.vertical) { // site
      const sx = x + LW, sw = W - LW, sh = y + H - top; const m = media && media[s.media]; const el = m && (m.video || m.img);
      ctx.save(); rr(ctx, sx, top, sw, sh - 2 * u, 0); ctx.clip(); ctx.globalAlpha = a; ctx.fillStyle = "#fff"; ctx.fillRect(sx, top, sw, sh);
      if (el) { const iw = el.videoWidth || el.width, ih = el.videoHeight || el.height; const r = Math.max(sw / iw, sh / ih); ctx.drawImage(el, sx, top, iw * r, ih * r); }
      else txt(ctx, s.url || "site", font(700, 34 * u), sx + sw / 2, top + sh / 2, "#8b93a7", "center", a);
      ctx.restore();
      if (fim) { const ka = easeOut((t - tFim) / 0.35); const lab = falha ? "FALHOU" : "PASSOU"; const f = font(900, 40 * u); const w = tw(ctx, lab, f) + 70 * u;
        ctx.save(); ctx.globalAlpha = ka; rr(ctx, sx + sw - w - 30 * u, top + 26 * u, w, 70 * u, 35 * u); ctx.fillStyle = falha ? C.red : C.ac; ctx.fill(); ctx.restore();
        txt(ctx, lab, f, sx + sw - w / 2 - 30 * u, top + 62 * u, "#0b1a12", "center", ka); }
    }
    if (falha && fim && s.erro) { const ka = easeOut((t - tFim) / 0.4); const ex = c.vertical ? x + 20 * u : x + LW + 30 * u, ew = c.vertical ? LW - 40 * u : W - LW - 60 * u, by = c.vertical ? yy + 20 * u : y + H - 190 * u;
      ctx.save(); ctx.globalAlpha = a * ka; rr(ctx, ex, by, ew, 150 * u, 12 * u); ctx.fillStyle = "#2a1517"; ctx.fill(); ctx.fillStyle = "rgba(255,107,107,.15)"; ctx.fill(); ctx.strokeStyle = C.red; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
      txt(ctx, "AssertionError", font(800, 24 * u, MONO), ex + 24 * u, by + 36 * u, C.red, "left", a * ka);
      String(s.erro).match(/.{1,60}(\s|$)/g).slice(0, 3).forEach((l, i) => txt(ctx, l.trim(), font(600, 21 * u, MONO), ex + 24 * u, by + 76 * u + i * 30 * u, C.txt, "left", a * ka)); }
    if (R && kf > 0) {  // holofote: escurece o resto e contorna o que importa
      ctx.save(); ctx.fillStyle = `rgba(0,0,0,${0.62 * kf})`;  // quatro faixas em volta do foco
      const [rx, ry, rw, rh] = R; const BX = -c.W, BY = -c.H, BW = c.W * 3, BH = c.H * 3;
      ctx.fillRect(BX, BY, BW, ry - BY); ctx.fillRect(BX, ry + rh, BW, BY + BH - ry - rh); ctx.fillRect(BX, ry, rx - BX, rh); ctx.fillRect(rx + rw, ry, BX + BW - rx - rw, rh);
      ctx.globalAlpha = kf; ctx.strokeStyle = C.yel; ctx.lineWidth = 6 * u / zf; rr(ctx, R[0], R[1], R[2], R[3], 12 * u); ctx.stroke(); ctx.restore();
    }
    ctx.restore();
    legenda(ctx, c, t, s);
  };
  // seta do mouse em (x,y)
  function seta(ctx, u, x, y, sc = 1) { ctx.save(); ctx.translate(x, y); ctx.scale(sc * u * 1.6, sc * u * 1.6);
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, 26); ctx.lineTo(7, 20); ctx.lineTo(12, 31); ctx.lineTo(17, 29); ctx.lineTo(12, 18); ctx.lineTo(21, 18); ctx.closePath();
    ctx.fillStyle = "#fff"; ctx.strokeStyle = "#111"; ctx.lineWidth = 1.6; ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 6; ctx.fill(); ctx.stroke(); ctx.restore(); }
  // mouse que percorre pontos [[x,y,t_clique,cor?],...]: chega em cada ponto 0.15s antes do clique; anel no clique
  function rota(ctx, u, pts, t) {
    if (!pts.length || t < pts[0][2] - 1.0) return; let px = pts[0][0] + 260 * u, py = pts[0][1] + 200 * u, pt = pts[0][2] - 1.0;
    let x = px, y = py, sc = 1;
    for (const [tx, ty, tc, cor] of pts) {
      const ini = Math.max(pt, tc - 0.95), k = easeOut((t - ini) / Math.max(0.2, tc - 0.15 - ini));
      if (t >= ini) { x = lerp(px, tx, k); y = lerp(py, ty, k); }
      const p = (t - tc) / 0.45; if (p > 0 && p < 1) { ctx.save(); ctx.globalAlpha = 1 - p; ctx.strokeStyle = cor || C.yel; ctx.lineWidth = 5 * u; ctx.beginPath(); ctx.arc(tx, ty, (14 + 46 * p) * u, 0, 7); ctx.stroke(); ctx.restore(); if (p < 0.25) sc = 0.85; }
      px = tx; py = ty; pt = tc;
    }
    seta(ctx, u, x, y, sc);
  }
  // desenha um print (1600x900) ajustado à largura dentro de [sx,sy,sw,sh]; devolve a função que converte coordenadas 0–1 do print
  // z = zoom (1 = largura toda); foco = ponto 0–1 do print que fica perto do centro
  function print(ctx, el, sx, sy, sw, sh, a, fundo = "#fff", foco = [0.5, 0.3], z = 1) {
    ctx.save(); ctx.beginPath(); ctx.rect(sx, sy, sw, sh); ctx.clip(); ctx.globalAlpha *= a; ctx.fillStyle = fundo; ctx.fillRect(sx, sy, sw, sh);
    const iw = el ? (el.videoWidth || el.width) : 1600, ih = el ? (el.videoHeight || el.height) : 900; const r = sw / iw * z;
    const ox = Math.min(sx, Math.max(sx + sw - iw * r, sx + sw / 2 - foco[0] * iw * r));
    const oy = ih * r <= sh ? sy : Math.min(sy, Math.max(sy + sh - ih * r, sy + sh * 0.42 - foco[1] * ih * r));
    if (el) ctx.drawImage(el, ox, oy, iw * r, ih * r);
    ctx.restore(); return (fx, fy) => [ox + fx * iw * r, oy + fy * ih * r];
  }
  function caixaElem(ctx, u, p, e, a, rotulo, cor = "rgba(111,168,220,.55)") {  // realce estilo navegador
    if (!e || a <= 0) return; const [x0, y0] = p(e[0], e[1]), [x1, y1] = p(e[2], e[3]);
    ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = cor; ctx.fillRect(x0, y0, x1 - x0, y1 - y0); ctx.restore();
    if (rotulo) { const f = font(700, 22 * u, MONO); const w = tw(ctx, rotulo, f) + 32 * u; const ty = y1 + 14 * u;
      ctx.save(); ctx.globalAlpha *= a; ctx.shadowColor = "rgba(0,0,0,.35)"; ctx.shadowBlur = 14 * u; rr(ctx, x0, ty, w, 44 * u, 8 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.restore();
      txt(ctx, rotulo, f, x0 + 16 * u, ty + 22 * u, "#8a3ab9", "left", a); }
  }
  function linhasHtml(s) {  // árvore do DevTools a partir do HTML real capturado (ou "html_linhas" à mão)
    if (s.html_linhas) return s.html_linhas;
    const h = s.html || { tag: "input", attrs: [["type", "text"], ["data-test", "username"], ["id", "user-name"]], pai: "div.form_group" };
    const [pt, pc] = String(h.pai || "div").split(".");
    const L = [{ n: 0, p: [["<", "pu"], ["html", "tag"], [">", "pu"]] }, { n: 1, p: [["<", "pu"], ["body", "tag"], [">", "pu"]] },
      { n: 2, p: [["<", "pu"], ["form", "tag"], [">", "pu"]] }, { n: 3, p: [["<", "pu"], [pt, "tag"], ...(pc ? [[" class", "an"], ["=", "pu"], [`"${pc}"`, "av"]] : []), [">", "pu"]] },
      { n: 4, p: [["<", "pu"], [h.tag, "tag"]], sel: true }];
    (h.attrs || []).filter(([k]) => k !== "style").forEach(([k, v]) => (v = String(v).length > 34 ? String(v).slice(0, 32) + "…" : v, L.push({ n: 5, p: [[k, "an"], ...(v !== "" ? [["=", "pu"], [`"${v}"`, "av"]] : [])], sel: true, attr: k })));
    L[L.length - 1].p.push(["> == $0", "pu"]); L.push({ n: 3, p: [["</", "pu"], [pt, "tag"], [">", "pu"]] });
    return L;
  }
  const DT = { tag: "#5db0d7", an: "#9bbbdc", av: "#f29766", pu: "#a8a8a8", tx: "#e8eaed" };

  // DEVTOOLS: botão direito › Inspecionar no site de verdade; abre o painel com o HTML real do elemento e realça atributos
  // {type:"devtools", media:"insp_user", url:"https://www.saucedemo.com", inspecionar:"#user-name", realce:["data-test","id"], realce_em:5, legenda:"..."}
  S.devtools = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1640 * u, H = 720 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, s.titulo || (s.url || "").replace(/^https?:\/\//, "").replace(/\/$/, ""), a, "#fff");
    const m = media && media[s.media]; const el = m && (m.video || m.img); const e = s.elem || [0.37, 0.3, 0.63, 0.36];
    const tc = s.clique_em || 1.6, tMenu = tc, tIn = tc + 1.0, tOpen = tIn + 0.35;
    const ko = s.aberto ? 1 : easeOut((t - tOpen) / 0.6); const PW = (s.painel || 0.5) * W * ko; const sw = W - PW, sh = y + H - top;
    const ex = (e[0] + e[2]) / 2, ey = (e[1] + e[3]) / 2;
    const p = print(ctx, el, x, top, sw, sh, a, "#fff", [ex, ey], lerp(1, s.zoom_site || 1.8, ko));
    if (!el) txt(ctx, s.url || "site", font(700, 34 * u), x + sw / 2, top + sh / 2, C.mut, "center", a);
    const kh = s.aberto ? 1 : easeOut((t - tOpen - 0.3) / 0.4);
    const h = s.html || {}; const idv = (h.attrs || []).find((q) => q[0] === "id"); const cls = (h.attrs || []).find((q) => q[0] === "class");
    void cls; caixaElem(ctx, u, p, e, kh * a, (h.tag || "input") + (idv ? "#" + idv[1] : "") + (s.elem_tam ? `  ${s.elem_tam[0]}×${s.elem_tam[1]}` : ""));
    if (PW > 2) {  // painel do DevTools
      const px = x + sw; ctx.save(); ctx.beginPath(); ctx.rect(px, top, PW, sh - 2 * u); ctx.clip(); ctx.globalAlpha = a;
      ctx.fillStyle = "#202124"; ctx.fillRect(px, top, PW, sh); ctx.fillStyle = "#292a2d"; ctx.fillRect(px, top, PW, 56 * u); ctx.fillStyle = "#3c4043"; ctx.fillRect(px, top + 56 * u, PW, 2 * u);
      ctx.fillStyle = "#3c4043"; ctx.fillRect(px, top, 3 * u, sh); ctx.restore();
      ctx.save(); ctx.beginPath(); ctx.rect(px, top, PW, sh - 2 * u); ctx.clip();
      let tx = px + 30 * u; ["Elements", "Console", "Sources", "Network"].forEach((n, i) => { txt(ctx, n, font(600, 23 * u), tx, top + 28 * u, i ? "#9aa0a6" : "#e8eaed", "left", a);
        const w = tw(ctx, n, font(600, 23 * u)); if (!i) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#8ab4f8"; ctx.fillRect(tx - 6 * u, top + 52 * u, w + 12 * u, 4 * u); ctx.restore(); } tx += w + 40 * u; });
      const L = linhasHtml(s); const fs = (s.fonte || 25) * u, lh = fs * 1.62; let yy = top + 100 * u; const ind = 26 * u;
      const re = s.realce || []; const r0 = s.realce_em || Math.min(dur - 1.5, tOpen + 2.2);
      L.forEach((ln, i) => {
        const kl = easeOut((t - tOpen - 0.15 - i * 0.04) / 0.3) * a; if (kl <= 0) return;
        if (ln.sel) { ctx.save(); ctx.globalAlpha = kl; ctx.fillStyle = "#1d3b5a"; ctx.fillRect(px + 3 * u, yy - lh / 2, PW, lh); ctx.restore(); }
        let xx = px + 30 * u + ln.n * ind; if (i < 4 && !ln.sel) txt(ctx, "▾", font(600, fs * 0.7), xx - 18 * u, yy, "#9aa0a6", "left", kl);
        const ri = ln.attr ? re.indexOf(ln.attr) : -1;
        if (ri >= 0) { const kr = easeOut((t - r0 - ri * 1.2) / 0.35); if (kr > 0) { const w = ln.p.reduce((q, [tk]) => q + tw(ctx, tk, font(600, fs, MONO)), 0);
          ctx.save(); ctx.globalAlpha = kr; ctx.fillStyle = "rgba(255,210,63,.18)"; rr(ctx, xx - 10 * u, yy - lh / 2 + 2 * u, w + 20 * u, lh - 4 * u, 8 * u); ctx.fill(); ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; ctx.stroke(); ctx.restore();
          if (ri === 0) txt(ctx, "← " + (s.realce_rotulo || "use este!"), font(800, 24 * u), xx + w + 26 * u, yy, C.yel, "left", kr); } }
        for (const [tk, k] of ln.p) { txt(ctx, tk, font(600, fs, MONO), xx, yy, DT[k] || DT.tx, "left", kl); xx += tw(ctx, tk, font(600, fs, MONO)); }
        yy += lh;
      });
      ctx.restore();
    }
    if (!s.aberto) {  // botão direito › menu › Inspecionar
      const [ax, ay] = p(ex, ey); const km = t > tMenu && t < tOpen + 0.1 ? easeOut((t - tMenu) / 0.2) : 0;
      const itens = c.idioma === "en" || global.CO_IDIOMA === "en" ? ["Back", "Reload", "Save as...", "Print...", "Inspect"] : ["Voltar", "Recarregar", "Salvar como...", "Imprimir...", "Inspecionar"];
      const mx = ax + 8 * u, my = ay + 8 * u, mw = 300 * u, ih = 50 * u;
      if (km > 0) { ctx.save(); ctx.globalAlpha = km; ctx.shadowColor = "rgba(0,0,0,.4)"; ctx.shadowBlur = 24 * u; rr(ctx, mx, my, mw, ih * itens.length + 16 * u, 10 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.restore();
        itens.forEach((n, i) => { const last = i === itens.length - 1; const hy = my + 8 * u + i * ih;
          if (last) { ctx.save(); ctx.globalAlpha = km * easeOut((t - tMenu - 0.5) / 0.2); ctx.fillStyle = "#e8f0fe"; ctx.fillRect(mx, hy, mw, ih); ctx.restore();
            if (t > tIn - 0.4) { ctx.save(); ctx.globalAlpha = km; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, mx - 4 * u, hy - 2 * u, mw + 8 * u, ih + 4 * u, 8 * u); ctx.stroke(); ctx.restore(); } }
          if (i === itens.length - 2) { ctx.save(); ctx.globalAlpha = km; ctx.fillStyle = "#e3e6ec"; ctx.fillRect(mx, hy + ih - 1 * u, mw, 2 * u); ctx.restore(); }
          txt(ctx, n, font(last ? 700 : 500, 25 * u), mx + 24 * u, hy + ih / 2, "#202124", "left", km); }); }
      const pts = [[ax, ay, tc, "#69a7ff"], [mx + 120 * u, my + 8 * u + 4.5 * ih, tIn]];
      if (t < tOpen + 0.3) rota(ctx, u, pts, t);
    }
    legenda(ctx, c, t, s);
  };

  // PLAYGROUND do Cypress: clica na mira, passa o mouse no elemento, o Cypress sugere o seletor; copia
  // {type:"playground", media:"insp_user", url:"...", inspecionar:"#user-name", spec:"login.cy.js", seletor:"[data-test=\"username\"]", copiar:true, legenda:"..."}
  S.playground = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1640 * u, H = 720 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "Cypress — " + (s.spec || "spec.cy.js"), a, "#1b1e27");
    const LW = 440 * u; const h = s.html || {}; const at = (k) => ((h.attrs || []).find((q) => q[0] === k) || [])[1];
    const sel = s.seletor || (at("data-test") ? `[data-test="${at("data-test")}"]` : at("data-cy") ? `[data-cy="${at("data-cy")}"]` : at("id") ? "#" + at("id") : h.tag || "input");
    const cmd = `cy.get('${sel}')`;
    // reporter (esquerda)
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#171a22"; ctx.fillRect(x, top, LW, y + H - top - 2 * u); ctx.fillStyle = C.line; ctx.fillRect(x, top + 64 * u, LW, 2 * u); ctx.restore();
    txt(ctx, s.spec || "spec.cy.js", font(700, 24 * u, MONO), x + 28 * u, top + 34 * u, C.txt, "left", a);
    (s.passos || [["visit", (s.url || "").replace(/^https?:\/\//, "")]]).forEach(([k, v], i) => { const yy = top + 110 * u + i * 50 * u;
      txt(ctx, String(i + 1), font(600, 22 * u, MONO), x + 40 * u, yy, "#4b5263", "center", a); txt(ctx, k, font(700, 25 * u, MONO), x + 70 * u, yy, C.ac2, "left", a);
      txt(ctx, String(v || ""), font(600, 22 * u, MONO), x + 86 * u + tw(ctx, k, font(700, 25 * u, MONO)), yy, C.txt, "left", a); });
    // barra de endereço com a mira
    const sx = x + LW, sw = W - LW; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#20232e"; ctx.fillRect(sx, top, sw, 64 * u); ctx.restore();
    const mira = [sx + 40 * u, top + 32 * u]; const tc1 = s.clique_em || 1.4; const kb = easeOut((t - tc1 - 0.15) / 0.4);
    ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(mira[0], mira[1], 22 * u, 0, 7); ctx.fillStyle = kb > 0.5 ? C.ac2 : "#2c3140"; ctx.fill();
    ctx.strokeStyle = kb > 0.5 ? "#fff" : C.txt; ctx.lineWidth = 3 * u; ctx.beginPath(); ctx.arc(mira[0], mira[1], 10 * u, 0, 7); ctx.stroke();
    [[0, -1], [0, 1], [-1, 0], [1, 0]].forEach(([dx, dy2]) => { ctx.beginPath(); ctx.moveTo(mira[0] + dx * 6 * u, mira[1] + dy2 * 6 * u); ctx.lineTo(mira[0] + dx * 16 * u, mira[1] + dy2 * 16 * u); ctx.stroke(); }); ctx.restore();
    if (kb < 0.5) { const tip = global.CO_IDIOMA === "en" ? "Open Selector Playground" : "Abrir Selector Playground"; const ka = easeOut((t - 0.6) / 0.3) * (1 - kb * 2);
      const f = font(700, 22 * u); const w = tw(ctx, tip, f) + 30 * u; ctx.save(); ctx.globalAlpha = ka; rr(ctx, mira[0] + 34 * u, mira[1] - 20 * u, w, 40 * u, 8 * u); ctx.fillStyle = "#000"; ctx.fill(); ctx.restore(); txt(ctx, tip, f, mira[0] + 49 * u, mira[1], "#fff", "left", ka); }
    txt(ctx, s.url || "", font(600, 22 * u, MONO), mira[0] + 50 * u, mira[1], C.mut, "left", a * (kb > 0.5 ? 0 : 1 - easeOut((t - 0.6) / 0.3)));
    // barra do playground (desce quando abre)
    const TB = 84 * u * kb; const st = top + 64 * u; const sh = y + H - st;
    const m = media && media[s.media]; const el = m && (m.video || m.img); const e = s.elem || [0.37, 0.3, 0.63, 0.36];
    const ex = (e[0] + e[2]) / 2, ey = (e[1] + e[3]) / 2;
    const p = print(ctx, el, sx, st + TB, sw, sh - TB - 2 * u, a, "#fff", [ex, ey], s.zoom_site || 1.5);
    if (!el) txt(ctx, s.url || "site", font(700, 34 * u), sx + sw / 2, st + sh / 2, C.mut, "center", a);
    const tc2 = tc1 + 1.7, tc3 = tc2 + 2.0; const kh = easeOut((t - tc2 + 0.6) / 0.3);
    if (kb > 0) {
      caixaElem(ctx, u, p, e, kh * a, sel);
      ctx.save(); ctx.beginPath(); ctx.rect(sx, st, sw, TB); ctx.clip(); ctx.globalAlpha = a; ctx.fillStyle = "#f3f4f7"; ctx.fillRect(sx, st, sw, TB); ctx.fillStyle = "#d5d9e2"; ctx.fillRect(sx, st + TB - 2 * u, sw, 2 * u);
      const by = st + TB - 42 * u; const ix = sx + 30 * u, iw = sw - 220 * u; rr(ctx, ix, by - 26 * u, iw, 52 * u, 8 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.strokeStyle = "#b9c0cc"; ctx.lineWidth = 2 * u; ctx.stroke();
      const kt = clamp((t - tc2) / 0.8); const cmdV = kt > 0 ? cmd.slice(0, Math.ceil(kt * cmd.length)) : "cy.get(' ')";
      txt(ctx, cmdV, font(700, 26 * u, MONO), ix + 20 * u, by, kt > 0 ? "#1d2230" : "#9aa0a6", "left", 1);
      const cbx = ix + iw + 20 * u; rr(ctx, cbx, by - 26 * u, 140 * u, 52 * u, 8 * u); ctx.fillStyle = "#e4e7ee"; ctx.fill();
      const kc = s.copiar !== false ? easeOut((t - tc3) / 0.2) : 0; txt(ctx, kc > 0.5 ? (global.CO_IDIOMA === "en" ? "Copied!" : "Copiado!") : (global.CO_IDIOMA === "en" ? "Copy" : "Copiar"), font(800, 22 * u), cbx + 70 * u, by, kc > 0.5 ? "#1f8f55" : "#3a3f4b", "center", 1);
      ctx.restore();
      if (kt >= 1) { const kr = easeOut((t - tc2 - 0.9) / 0.35); ctx.save(); ctx.globalAlpha = kr; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, ix - 6 * u, by - 32 * u, iw + 12 * u, 64 * u, 10 * u); ctx.stroke(); ctx.restore(); }
    }
    const [ax, ay] = p(ex, ey); const pts = [[mira[0], mira[1], tc1], [ax, ay, tc2, "#69a7ff"]];
    if (s.copiar !== false) { const by = st + 84 * u - 42 * u; pts.push([sx + 30 * u + (sw - 220 * u) + 90 * u, by + 6 * u, tc3]); }
    rota(ctx, u, pts, t);
    legenda(ctx, c, t, s);
  };
  // MENU: clicar em menus de verdade (VS Code ou Explorador). 
  // {type:"menu", app:"vscode"|"explorer", barra:["File","Edit",...], abre:0, menus:[["New File","Open Folder..."],["..."]], caminho:[1], ponto:[0.6,0.5] (botão direito),
  //  resultado:"terminal"|"pasta"|"arquivo", novo:"meu-primeiro-teste", pastas:[...], itens:[...], legenda:"..."}
  S.menu = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1500 * u, H = 700 * u; const x = c.cx - W / 2, y = topo(c, H);
    const claro = s.app === "explorer"; const fundo = claro ? "#f3f4f7" : C.win;
    const top = janela(ctx, x, y, W, H, u, s.titulo || (claro ? "Explorador de Arquivos" : "Visual Studio Code"), a, fundo);
    const tc0 = s.clique_em || 1.2, passo = s.passo || 1.15; const M = s.menus || []; const cam = s.caminho || [];
    const tFim = tc0 + M.length * passo; const fechado = t > tFim + 0.25;
    let corpo = top;
    const barra = (s.barra && s.barra.length ? s.barra : null) || (s.barra ? null : claro ? null : ["File", "Edit", "Selection", "View", "Go", "Run", "Terminal", "Help"]); const bx = [];
    if (barra) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = claro ? "#e4e7ee" : "#2a2d3a"; ctx.fillRect(x, top, W, 52 * u); ctx.restore(); let xx = x + 24 * u;
      barra.forEach((b, i) => { const w = tw(ctx, b, font(500, 24 * u)) + 30 * u; const on = s.abre === i && t > tc0 - 0.05 && !fechado;
        if (on) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = claro ? "#cfd6e4" : "#3c4157"; rr(ctx, xx, top + 6 * u, w, 40 * u, 6 * u); ctx.fill(); ctx.restore(); }
        txt(ctx, b, font(500, 24 * u), xx + 15 * u, top + 26 * u, claro ? "#2a2f3a" : (on ? "#fff" : "#c5c9d6"), "left", a); bx.push([xx, w]); xx += w; });
      corpo = top + 52 * u; }
    // corpo do app
    const ch = y + H - corpo; let sideW = 0;
    if (claro) {
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#fff"; ctx.fillRect(x, corpo, W, ch - 2 * u); ctx.fillStyle = "#e4e7ee"; ctx.fillRect(x, corpo, W, 64 * u); ctx.restore();
      pastaIcone(ctx, x + 30 * u, corpo + 16 * u, 38 * u, a); txt(ctx, s.caminho_txt || "Este Computador  ›  Documentos", font(600, 26 * u), x + 84 * u, corpo + 32 * u, "#3a3f4b", "left", a);
      const its = (s.itens || ["Fotos", "Músicas", "Trabalho"]).slice(); const kn = s.resultado === "pasta" ? easeOut((t - tFim - 0.3) / 0.4) : 0; if (kn > 0) its.push({ nome: s.novo || "Nova pasta", novo: true });
      its.forEach((it, i) => { const nome = typeof it === "string" ? it : it.nome; const cx = x + 130 * u + i * 240 * u, cy = corpo + 130 * u; const ka = it.novo ? kn : 1;
        if (it.novo) { ctx.save(); ctx.globalAlpha = a * kn * 0.3; rr(ctx, cx - 95 * u, cy - 16 * u, 190 * u, 210 * u, 14 * u); ctx.fillStyle = C.ac2; ctx.fill(); ctx.restore(); }
        pastaIcone(ctx, cx - 65 * u, cy, 130 * u, a * ka); const nt = it.novo ? nome.slice(0, Math.ceil(clamp((t - tFim - 0.8) / 1.0) * nome.length)) || "Nova pasta" : nome;
        txt(ctx, nt, font(it.novo ? 800 : 600, 26 * u), cx, cy + 150 * u, "#2a2f3a", "center", a * ka); });
    } else {
      sideW = s.pastas ? 330 * u : 0;
      if (sideW) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.side; ctx.fillRect(x, corpo, sideW, ch - 2 * u); ctx.restore(); txt(ctx, "EXPLORER", font(700, 20 * u), x + 28 * u, corpo + 34 * u, C.mut, "left", a);
        const ps = s.pastas.slice(); const kn = s.resultado === "arquivo" ? easeOut((t - tFim - 0.3) / 0.3) : 0;
        ps.forEach((p, i) => { const yy = corpo + (80 + i * 48) * u, ind = Math.min(i, 3) * 22 * u, arq = /\.\w+$/.test(p);
          if (arq) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = C.ac; rr(ctx, x + 32 * u + ind, yy - 13 * u, 20 * u, 26 * u, 4 * u); ctx.fill(); ctx.restore(); } else pastaIcone(ctx, x + 28 * u + ind, yy - 14 * u, 30 * u, a);
          txt(ctx, p, font(500, 24 * u), x + 68 * u + ind, yy, C.txt, "left", a); });
        if (kn > 0) { const i = ps.length, yy = corpo + (80 + i * 48) * u, ind = Math.min(i, 3) * 22 * u; const nm = (s.novo || "novo.js").slice(0, Math.ceil(clamp((t - tFim - 0.6) / 1.0) * (s.novo || "novo.js").length));
          ctx.save(); ctx.globalAlpha = a * kn; ctx.strokeStyle = C.ac2; ctx.lineWidth = 2 * u; ctx.strokeRect(x + 60 * u + ind, yy - 20 * u, sideW - 80 * u - ind, 40 * u); ctx.fillStyle = C.ac; rr(ctx, x + 32 * u + ind, yy - 13 * u, 20 * u, 26 * u, 4 * u); ctx.fill(); ctx.restore();
          txt(ctx, nm, font(600, 24 * u), x + 68 * u + ind, yy, C.txt, "left", a * kn); } }
      txt(ctx, s.fundo_txt || "", font(700, 40 * u), x + sideW + (W - sideW) / 2, corpo + ch * 0.4, "#3a3f50", "center", a);
      if (s.resultado === "terminal") { const k = easeOut((t - tFim - 0.3) / 0.5); if (k > 0) { const th = 250 * u * k, ty = y + H - th - 2 * u;
        ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.term; ctx.fillRect(x + sideW, ty, W - sideW, th); ctx.fillStyle = C.line; ctx.fillRect(x + sideW, ty, W - sideW, 2 * u);
        ctx.beginPath(); ctx.rect(x + sideW, ty, W - sideW, th); ctx.clip();
        ["PROBLEMS", "OUTPUT", "TERMINAL"].forEach((n, i) => txt(ctx, n, font(700, 20 * u), x + sideW + 30 * u + i * 160 * u, ty + 30 * u, i === 2 ? C.txt : C.mut, "left", 1));
        ctx.fillStyle = C.ac2; ctx.fillRect(x + sideW + 30 * u + 320 * u, ty + 46 * u, tw(ctx, "TERMINAL", font(700, 20 * u)), 3 * u);
        const pr = s.prompt || "PS C:\\Users\\voce\\Documents\\meu-primeiro-teste> "; txt(ctx, pr, font(600, 26 * u, MONO), x + sideW + 30 * u, ty + 100 * u, C.ac2, "left", 1);
        if (Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = C.txt; ctx.fillRect(x + sideW + 34 * u + tw(ctx, pr, font(600, 26 * u, MONO)), ty + 86 * u, 14 * u, 28 * u); }
        ctx.restore();
        ctx.save(); ctx.globalAlpha = k; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, x + sideW + 8 * u, ty + 6 * u, W - sideW - 16 * u, th - 12 * u, 12 * u); ctx.stroke(); ctx.restore(); } }
    }
    // menus
    const mf = font(500, 25 * u), ih = 48 * u; const pts = [];
    let mx, my;
    if (barra && s.abre !== undefined) { mx = bx[s.abre][0]; my = corpo; pts.push([bx[s.abre][0] + bx[s.abre][1] / 2, top + 26 * u, tc0]); }
    else { const pp = s.ponto || [0.6, 0.55]; mx = x + sideW + pp[0] * (W - sideW); my = corpo + pp[1] * ch; pts.push([mx, my, tc0, "#69a7ff"]); mx += 6 * u; my += 6 * u; }
    M.forEach((itens, k) => {
      const tk = tc0 + k * passo; if (t < tk) return; const ka = fechado ? 0 : easeOut((t - tk - 0.05) / 0.15);
      const mw = Math.max(300 * u, ...itens.map((n) => tw(ctx, n, mf) + 110 * u)); const mh = itens.reduce((q, n) => q + (n === "—" ? 14 * u : ih), 0) + 16 * u;
      if (my + mh > y + H - 10 * u) my = y + H - 10 * u - mh;
      if (mx + mw > x + W - 10 * u) mx = k ? mx - mw * 2 + 12 * u : x + W - 10 * u - mw;
      ctx.save(); ctx.globalAlpha = a * ka; ctx.shadowColor = "rgba(0,0,0,.45)"; ctx.shadowBlur = 26 * u; rr(ctx, mx, my, mw, mh, 10 * u); ctx.fillStyle = claro ? "#fff" : "#252526"; ctx.fill(); ctx.shadowColor = "transparent";
      ctx.strokeStyle = claro ? "#d5d9e2" : "#454545"; ctx.lineWidth = 1.5 * u; ctx.stroke(); ctx.restore();
      let yy = my + 8 * u; let prox = null;
      itens.forEach((n, i) => {
        if (n === "—") { ctx.save(); ctx.globalAlpha = a * ka; ctx.fillStyle = claro ? "#e3e6ec" : "#454545"; ctx.fillRect(mx + 12 * u, yy + 6 * u, mw - 24 * u, 1.5 * u); ctx.restore(); yy += 14 * u; return; }
        const esc = cam[k] === i; const kh = esc ? easeOut((t - (tk + passo - 0.55)) / 0.15) : 0;
        if (kh > 0) { ctx.save(); ctx.globalAlpha = a * ka * kh; ctx.fillStyle = claro ? "#e5f0ff" : "#04395e"; rr(ctx, mx + 6 * u, yy + 2 * u, mw - 12 * u, ih - 4 * u, 6 * u); ctx.fill();
          ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; ctx.stroke(); ctx.restore(); }
        const sub = / ›$/.test(n); const nome = n.replace(/ ›$/, "");
        txt(ctx, nome, font(esc ? 700 : 500, 25 * u), mx + 26 * u, yy + ih / 2, claro ? "#202124" : (esc && kh > 0 ? "#fff" : "#cccccc"), "left", a * ka);
        if (sub) txt(ctx, "›", font(700, 28 * u), mx + mw - 26 * u, yy + ih / 2, claro ? "#5d6577" : "#cccccc", "right", a * ka);
        if (esc) { pts.push([mx + Math.min(mw * 0.45, tw(ctx, nome, mf) + 40 * u), yy + ih / 2 + 4 * u, tk + passo]); prox = [mx + mw - 6 * u, yy - 8 * u]; }
        yy += ih;
      });
      if (prox) [mx, my] = prox;
    });
    if (t < tFim + 0.9) rota(ctx, u, pts, t);
    legenda(ctx, c, t, s);
  };

  // LAUNCHPAD do Cypress (a janela que abre com "npx cypress open")
  // {type:"launchpad", tela:"tipo"|"navegador"|"specs", specs:["login.cy.js"], escolha:0, legenda:"..."}
  S.launchpad = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1500 * u, H = 720 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "Cypress", a, "#ffffff"); const tc = s.clique_em || Math.min(dur * 0.6, 2.6); const en = global.CO_IDIOMA === "en";
    const IND = "#4956e3", ESC = "#1b1e2e", MUT = "#5a5f7a"; const pts = [];
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#f8f8fa"; ctx.fillRect(x, top, W, 64 * u); ctx.fillStyle = "#e1e3ed"; ctx.fillRect(x, top + 64 * u, W, 2 * u); ctx.restore();
    txt(ctx, "meu-primeiro-teste", font(600, 24 * u), x + 36 * u, top + 32 * u, MUT, "left", a);
    if (s.tela === "tipo") {
      txt(ctx, "Welcome to Cypress!", font(800, 46 * u), c.cx, top + 140 * u, ESC, "center", a);
      txt(ctx, en ? "Review the differences between each testing type →" : "Escolha o tipo de teste", font(500, 26 * u), c.cx, top + 196 * u, MUT, "center", a);
      [["E2E Testing", en ? "Test your whole site like a user" : "testa o site como um usuário", "#1fa971"], ["Component Testing", en ? "Test a single component" : "testa uma peça isolada", "#9aa0b4"]].forEach(([ti, sub, cor], i) => {
        const cw = 520 * u, chh = 300 * u, cx = c.cx - cw - 30 * u + i * (cw + 60 * u), cy = top + 250 * u; const on = i === (s.escolha || 0); const kh = on ? easeOut((t - tc + 0.5) / 0.3) : 0;
        ctx.save(); ctx.globalAlpha = a; rr(ctx, cx, cy, cw, chh, 14 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.strokeStyle = kh > 0 ? IND : "#d0d2e0"; ctx.lineWidth = (2 + 3 * kh) * u; ctx.stroke(); ctx.restore();
        ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(cx + cw / 2, cy + 100 * u, 52 * u, 0, 7); ctx.fillStyle = cor; ctx.globalAlpha = a * 0.18; ctx.fill(); ctx.restore();
        txt(ctx, i ? "⚙" : "◎", font(800, 56 * u), cx + cw / 2, cy + 102 * u, cor, "center", a);
        txt(ctx, ti, font(800, 34 * u), cx + cw / 2, cy + 196 * u, ESC, "center", a); txt(ctx, sub, font(500, 24 * u), cx + cw / 2, cy + 244 * u, MUT, "center", a);
        if (on) pts.push([cx + cw / 2, cy + 196 * u, tc]); });
    } else if (s.tela === "navegador") {
      txt(ctx, en ? "Choose a browser" : "Choose a browser", font(800, 44 * u), c.cx, top + 130 * u, ESC, "center", a);
      txt(ctx, en ? "Choose your preferred browser for E2E testing." : "Escolha o navegador para os testes", font(500, 26 * u), c.cx, top + 182 * u, MUT, "center", a);
      const bs = s.navegadores || [["Chrome", "#4285f4"], ["Edge", "#0f9d8a"], ["Electron", "#47848f"]]; const esc = s.escolha || 0; const tc1 = tc - 1.4;
      bs.forEach(([n, cor], i) => { const bw = 260 * u, bh = 200 * u, bx0 = c.cx - (bs.length * bw + (bs.length - 1) * 30 * u) / 2 + i * (bw + 30 * u), by0 = top + 230 * u;
        const on = i === esc && t > tc1; ctx.save(); ctx.globalAlpha = a; rr(ctx, bx0, by0, bw, bh, 12 * u); ctx.fillStyle = on ? "#eef0ff" : "#fff"; ctx.fill(); ctx.strokeStyle = on ? IND : "#d0d2e0"; ctx.lineWidth = (on ? 4 : 2) * u; ctx.stroke();
        ctx.beginPath(); ctx.arc(bx0 + bw / 2, by0 + 80 * u, 42 * u, 0, 7); ctx.fillStyle = cor; ctx.fill(); ctx.beginPath(); ctx.arc(bx0 + bw / 2, by0 + 80 * u, 17 * u, 0, 7); ctx.fillStyle = "#fff"; ctx.fill(); ctx.restore();
        txt(ctx, n, font(700, 28 * u), bx0 + bw / 2, by0 + 160 * u, ESC, "center", a); if (i === esc) pts.push([bx0 + bw / 2, by0 + 100 * u, tc1]); });
      const btn = (en ? "Start E2E Testing in " : "Start E2E Testing in ") + bs[esc][0]; const f = font(800, 28 * u); const bw2 = tw(ctx, btn, f) + 70 * u, bx2 = c.cx - bw2 / 2, by2 = top + 480 * u;
      const kb = easeOut((t - tc) / 0.2); ctx.save(); ctx.globalAlpha = a; rr(ctx, bx2, by2, bw2, 72 * u, 10 * u); ctx.fillStyle = kb > 0.5 ? "#3a46c9" : IND; ctx.fill(); ctx.restore();
      txt(ctx, btn, f, c.cx, by2 + 36 * u, "#fff", "center", a); pts.push([c.cx + bw2 * 0.25, by2 + 40 * u, tc]);
    } else {  // specs
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#1b1e2e"; ctx.fillRect(x, top + 66 * u, 90 * u, y + H - top - 68 * u); ctx.restore();
      ["▤", "⚙", "▶"].forEach((ic, i) => txt(ctx, ic, font(700, 32 * u), x + 45 * u, top + 130 * u + i * 80 * u, i ? "#9aa0b4" : "#fff", "center", a));
      txt(ctx, "Specs", font(800, 40 * u), x + 140 * u, top + 130 * u, ESC, "left", a);
      ctx.save(); ctx.globalAlpha = a; rr(ctx, x + 140 * u, top + 175 * u, W - 200 * u, 60 * u, 8 * u); ctx.strokeStyle = "#d0d2e0"; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
      txt(ctx, en ? "Search specs" : "Search specs", font(500, 24 * u), x + 170 * u, top + 205 * u, "#9aa0b4", "left", a);
      pastaIcone(ctx, x + 150 * u, top + 268 * u, 34 * u, a, "#9aa0b4"); txt(ctx, "cypress / e2e", font(700, 26 * u), x + 200 * u, top + 286 * u, MUT, "left", a);
      (s.specs || ["login.cy.js"]).forEach((n, i) => { const yy = top + 350 * u + i * 64 * u; const on = i === (s.escolha || 0); const kh = on ? easeOut((t - tc + 0.5) / 0.3) : 0;
        if (kh > 0) { ctx.save(); ctx.globalAlpha = a * kh; ctx.fillStyle = "#eef0ff"; rr(ctx, x + 170 * u, yy - 28 * u, W - 260 * u, 56 * u, 8 * u); ctx.fill(); ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; ctx.stroke(); ctx.restore(); }
        ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#1fa971"; rr(ctx, x + 200 * u, yy - 14 * u, 22 * u, 28 * u, 4 * u); ctx.fill(); ctx.restore();
        txt(ctx, n.replace(/\.cy\.js$/, ""), font(700, 27 * u, MONO), x + 240 * u, yy, kh > 0 ? IND : ESC, "left", a); const nw = tw(ctx, n.replace(/\.cy\.js$/, ""), font(700, 27 * u, MONO));
        txt(ctx, ".cy.js", font(500, 27 * u, MONO), x + 240 * u + nw, yy, "#9aa0b4", "left", a); if (on) pts.push([x + 260 * u + nw / 2, yy + 6 * u, tc]); });
    }
    rota(ctx, u, pts, t);
    legenda(ctx, c, t, s);
  };
})(window);

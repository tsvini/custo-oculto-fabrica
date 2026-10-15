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
  function legenda(ctx, c, t, s) {  // faixa explicativa embaixo da janela
    if (!s.legenda) return; const u = c.u; const a = easeOut((t - (s.legenda_em || 0.6)) / 0.4); if (a <= 0) return;
    const f = font(800, 44 * u); const w = tw(ctx, s.legenda, f) + 80 * u; const y = c.H - 150 * u;
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
    const W = (c.vertical ? 1000 : 1560) * u, H = (c.vertical ? 1100 : 780) * u; const x = c.cx - W / 2, y = (c.vertical ? c.H * 0.2 : c.H * 0.42 - H / 2);
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
    const dig = s.digitar === false ? 1 : clamp((t - 0.5) / Math.max(0.8, dur * (s.vel || 0.7))); let resta = Math.floor(dig * total);
    linhas.forEach((ln, i) => {
      const hl = (s.destaque || []).includes(i + 1);
      if (hl && dig >= 1) { const ha = easeOut((t - 0.5 - dur * (s.vel || 0.7)) / 0.4); ctx.save(); ctx.globalAlpha = 0.18 * ha; ctx.fillStyle = C.ac; ctx.fillRect(tabX, yy - lh / 2, W - sideW, lh); ctx.globalAlpha = ha; ctx.fillRect(tabX, yy - lh / 2, 6 * u, lh); ctx.restore(); }
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
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 1000 : 1400) * u, H = (c.vertical ? 900 : 680) * u;
    const x = c.cx - W / 2, y = c.vertical ? c.H * 0.22 : c.H * 0.42 - H / 2;
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
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 1000 : 1500) * u, H = (c.vertical ? 1000 : 720) * u;
    const x = c.cx - W / 2, y = c.vertical ? c.H * 0.2 : c.H * 0.42 - H / 2;
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
    const W = (c.vertical ? 1000 : 1600) * u, H = W * 9 / 16 + 64 * u; const x = c.cx - W / 2, y = c.vertical ? c.H * 0.25 : c.H * 0.43 - H / 2;
    const top = janela(ctx, x, y, W, H, u, s.titulo || "", a);
    const vw = W, vh = H - (top - y); ctx.save(); rr(ctx, x, top, vw, vh, 0); ctx.clip();
    const el = m && (m.video || m.img);
    if (el) {
      const iw = el.videoWidth || el.width, ih = el.videoHeight || el.height; let [zx0, zy0, zx1, zy1] = [0, 0, 1, 1];
      if (s.zoom) { const k = easeOut((t - (s.zoom_em || 1.5)) / 0.8); zx0 = lerp(0, s.zoom[0], k); zy0 = lerp(0, s.zoom[1], k); zx1 = lerp(1, s.zoom[2], k); zy1 = lerp(1, s.zoom[3], k); }
      ctx.globalAlpha = a; ctx.drawImage(el, zx0 * iw, zy0 * ih, (zx1 - zx0) * iw, (zy1 - zy0) * ih, x, top, vw, vh);
      if (s.caixa) { const k = easeOut((t - (s.caixa_em || 1.2)) / 0.4); const [bx0, by0, bx1, by1] = s.caixa; const fx = (v) => x + (v - zx0) / (zx1 - zx0) * vw, fy = (v) => top + (v - zy0) / (zy1 - zy0) * vh;
        ctx.globalAlpha = k; ctx.strokeStyle = C.yel; ctx.lineWidth = 8 * u; rr(ctx, fx(bx0), fy(by0), fx(bx1) - fx(bx0), fy(by1) - fy(by0), 14 * u); ctx.stroke(); }
    } else { ctx.fillStyle = "#11131a"; ctx.fillRect(x, top, vw, vh); txt(ctx, "[ gravação: " + (s.media || "?") + " ]", font(700, 40 * u), c.cx, top + vh / 2, C.mut, "center", a); }
    ctx.restore(); legenda(ctx, c, t, s);
  };
  // INSTALADOR (desenhado): {type:"instalador", app:"Visual Studio Code", titulo:"Select Additional Tasks", texto:"...", caixas:[["Add to PATH",true]], botao:"Next", progresso:false, legenda:"..."}
  S.instalador = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 980 : 1240) * u, H = (c.vertical ? 900 : 720) * u;
    const x = c.cx - W / 2, y = c.vertical ? c.H * 0.2 : c.H * 0.42 - H / 2;
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
      ctx.restore(); txt(ctx, rot, font(700, 30 * u), bx + bw2 / 2, by2 + bh / 2, pri ? "#fff" : "#2a2f3a", "center", a); });
    legenda(ctx, c, t, s);
  };
})(window);

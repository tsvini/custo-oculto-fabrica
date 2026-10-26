/* Cenas didáticas para aulas (curso Cypress para leigos): editor de código, terminal, passo a passo,
   pastas, cards de conceito e gravação de tela emoldurada. Registra em COEngine.SCENES. */
(function (global) {
  "use strict";
  const S = global.COEngine.SCENES;
  const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
  const MONO = "'JetBrains Mono', 'Courier New', monospace";
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const easeOut = (x) => { x = clamp(x); return 1 - Math.pow(1 - x, 3); };
  const easeInOut = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const backOut = (x) => { x = clamp(x); const c1 = 1.70158, c3 = 2.70158; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
  const lerp = (a, b, t) => a + (b - a) * t;
  const font = (w, s, f) => `${w} ${Math.max(1, Math.round(s))}px ${f || FONT}`;
  // paleta das aulas: verde Cypress + tons de editor escuro
  const C = { ac: "#3fd68a", ac2: "#69a7ff", yel: "#ffd23f", red: "#ff6b6b", txt: "#e8eaf0", mut: "#8b93a7",
    win: "#1b1e27", bar: "#252936", side: "#20232e", line: "#2c3140", term: "#0f1117", folder: "#f5c542" };
  // código sem ligaduras: "=>" tem que aparecer como => (o aluno vai digitar isso), não como uma seta
  function semLig(ctx, f) { ctx.textRendering = /JetBrains/.test(f) ? "optimizeSpeed" : "auto"; }
  function rr(ctx, x, y, w, h, r) { w = Math.max(0, w); h = Math.max(0, h); r = Math.max(0, Math.min(r, w / 2, h / 2)); ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function txt(ctx, t, f, x, y, fill, align = "left", alpha = 1) { if (!t || alpha <= 0.01) return; ctx.save(); ctx.globalAlpha *= alpha; ctx.font = f; semLig(ctx, f); ctx.textAlign = align; ctx.textBaseline = "middle"; ctx.fillStyle = fill; ctx.fillText(t, x, y); ctx.restore(); }
  // árvore do Explorer: se algum item começar com espaços, o nível vem dos espaços (2 por nível); senão, cada item fica um nível abaixo do anterior
  function arvore(lista, max) { const expl = lista.some((p) => /^ /.test(p)); return lista.map((p, i) => { const nm = p.trim(); return { nm, nv: expl ? Math.floor((p.length - p.trimStart().length) / 2) : Math.min(i, max) }; }); }
  // fonte que cabe: diminui o tamanho até o texto caber em maxW (nunca passa do tamanho pedido)
  function caber(ctx, t, peso, tam, maxW, fam) { const w = tw(ctx, String(t || ""), font(peso, tam, fam)); return font(peso, w > maxW ? tam * maxW / w : tam, fam); }
  function tw(ctx, t, f) { ctx.font = f; semLig(ctx, f); const w = ctx.measureText(t).width; ctx.textRendering = "auto"; return w; }

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
  function seloColinha(ctx, c, t, s) {  // "já está na sua colinha": aparece no canto e some
    const t0 = s.colinha_em === undefined ? 1.2 : s.colinha_em; const k = easeOut((t - t0) / 0.35) * (1 - easeOut((t - t0 - (s.colinha_dur || 3.2)) / 0.4)); if (k <= 0) return;
    const u = c.u, f = font(800, 30 * u), tx = global.CO_IDIOMA === "en" ? "It's in your cheat sheet" : "Já está na sua colinha"; const w = tw(ctx, tx, f) + 120 * u, h = 76 * u;
    const x = c.W - w - 40 * u + (1 - k) * 60 * u, y = c.H - h - 36 * u;
    ctx.save(); ctx.globalAlpha = k; ctx.shadowColor = "rgba(0,0,0,.45)"; ctx.shadowBlur = 24 * u; rr(ctx, x, y, w, h, 38 * u); ctx.fillStyle = C.yel; ctx.fill(); ctx.shadowColor = "transparent";
    const ix = x + 26 * u, iy = y + 16 * u; ctx.fillStyle = "#fff"; rr(ctx, ix, iy, 34 * u, 44 * u, 5 * u); ctx.fill(); ctx.fillStyle = "#c9a400"; [0, 1, 2].forEach((i) => ctx.fillRect(ix + 7 * u, iy + (12 + i * 9) * u, 20 * u, 3 * u)); ctx.restore();
    txt(ctx, tx, f, x + 76 * u, y + h / 2, "#1a1400", "left", k);
  }
  function legenda(ctx, c, t, s) {  // faixa explicativa embaixo da janela
    if (s.colinha) seloColinha(ctx, c, t, s);
    if (!s.legenda) return; const u = c.u; const a = easeOut((t - (s.legenda_em || 0.6)) / 0.4); if (a <= 0) return;
    const f = font(800, 44 * u); const w = tw(ctx, s.legenda, f) + 80 * u; const y = c.H * (c.vertical ? 0.80 : 0.795);
    ctx.save(); ctx.globalAlpha = a; rr(ctx, c.cx - w / 2, y - 44 * u + (1 - a) * 20 * u, w, 88 * u, 44 * u); ctx.fillStyle = C.ac; ctx.fill(); ctx.restore();
    txt(ctx, s.legenda, f, c.cx, y + (1 - a) * 20 * u, "#0b1a12", "center", a);
  }

  function pastaIcone(ctx, x, y, s, a, cor = C.folder) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = cor;
    rr(ctx, x, y, s * 0.42, s * 0.2, s * 0.05); ctx.fill(); rr(ctx, x, y + s * 0.1, s, s * 0.7, s * 0.07); ctx.fill();
    ctx.fillStyle = "rgba(255,255,255,.25)"; rr(ctx, x, y + s * 0.18, s, s * 0.08, s * 0.03); ctx.fill(); ctx.restore(); }
  // destaque de sintaxe simples (JS)
  const KW = /^(const|let|var|function|return|if|else|describe|it|context|beforeEach|before|after|afterEach|async|await|new|import|from|export|default|for|of|class|constructor|this|require)$/;
  function tokens(linha) {
    const out = []; const re = /(\/\/.*$)|('[^']*'|"[^"]*"|`[^`]*`)|(\b\d+\b)|([A-Za-z_$][\w$]*)|(\s+)|(.)/g; let m;
    while ((m = re.exec(linha))) {
      if (m[1]) out.push([m[1], C.mut]); else if (m[2]) out.push([m[2], "#f0a868"]); else if (m[3]) out.push([m[3], "#c792ea"]);
      else if (m[4]) { const nx = linha.slice(re.lastIndex).trimStart()[0]; out.push([m[4], KW.test(m[4]) ? "#c792ea" : (m[4] === "cy" || m[4] === "page" || m[4] === "test" || m[4] === "expect" || m[4] === "request") ? C.ac : nx === "(" ? C.ac2 : C.txt]); }
      else out.push([m[0], C.txt]);
    }
    return out;
  }

  // EDITOR: {type:"editor", arquivo:"login.cy.js", codigo:"linhas\n...", digitar:true, destaque:[3,4], legenda:"...", pastas:["cypress","e2e","login.cy.js"]}
  S.editor = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const sc = lerp(0.96, 1, backOut(t / 0.5));
    const W = (c.vertical ? 1000 : 1500) * u, H = (c.vertical ? 1100 : 700) * u; const x = c.cx - W / 2, y = topo(c, H);
    ctx.save(); ctx.translate(c.cx, y + H / 2); ctx.scale(sc, sc); ctx.translate(-c.cx, -(y + H / 2));
    const top = janela(ctx, x, y, W, H, u, (s.arquivo || "arquivo.js") + " — Visual Studio Code", a);
    const sideW = s.pastas && !c.vertical ? 330 * u : 0;
    if (sideW) {
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.side; ctx.fillRect(x, top, sideW, H - (top - y) - 22 * u); ctx.restore();
      txt(ctx, "EXPLORER", font(700, 20 * u), x + 28 * u, top + 36 * u, C.mut, "left", a);
      const arvE = arvore(s.pastas, 4); const passoE = Math.min(50, (H / u - (top - y) / u - 120) / Math.max(1, arvE.length));  // muitos arquivos: as linhas ficam mais juntas pra caber
      arvE.forEach(({ nm: p, nv }, i) => {
        const pasta = /\/$/.test(p); if (pasta) p = p.slice(0, -1); const yy = top + (86 + i * passoE) * u, ind = nv * 22 * u, arq = !pasta && (/\.\w+$/.test(p) || /^\.\w/.test(p));
        if (arq) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = C.ac; rr(ctx, x + 32 * u + ind, yy - 13 * u, 20 * u, 26 * u, 4 * u); ctx.fill(); ctx.restore(); }
        else pastaIcone(ctx, x + 28 * u + ind, yy - 14 * u, 30 * u, a);
        const fsN = Math.min(24 * u, 24 * u * (sideW - 88 * u - ind) / Math.max(1, tw(ctx, p, font(arq ? 600 : 500, 24 * u))));  // nome comprido encolhe pra caber no Explorer
        txt(ctx, p, font(arq ? 600 : 500, fsN), x + 68 * u + ind, yy, arq ? C.ac : C.txt, "left", a);
      });
    }
    // aba
    const tabX = x + sideW; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.win; ctx.fillRect(tabX, top, 300 * u, 56 * u); ctx.fillStyle = C.ac; ctx.fillRect(tabX, top, 300 * u, 4 * u); ctx.restore();
    txt(ctx, s.arquivo || "arquivo.js", font(600, 24 * u), tabX + 28 * u, top + 30 * u, C.txt, "left", a);
    const linhas = String(s.codigo || "").split("\n"); const total = linhas.join("").length || 1;
    // no vertical, a fonte cresce até caber na largura
    const maxCh = Math.max(10, ...linhas.map((l) => l.length));
    // a linha mais comprida sempre cabe inteira (código nunca é cortado na lateral)
    let fs = Math.min(c.vertical ? 46 * u : (s.fonte || (linhas.length > 12 ? 30 : 36)) * u, (W - sideW - 140 * u) / (maxCh * 0.6)); let lh = fs * 1.55; const x0 = tabX + 96 * u; let yy = top + 100 * u;
    // rolar: o arquivo inteiro aparece de cima e a tela desce até o fim antes de começar a digitar
    const PH = s.terminal ? Math.round(H * (s.terminal_altura || 0.4)) : 0;  // painel do terminal integrado (embaixo, como no VS Code); terminal_altura: cenas em que o assunto é o terminal
    if (PH) { fs = Math.min(fs, (y + H - PH - top - 100 * u) / ((linhas.length - 0.4) * 1.55)); lh = fs * 1.55; }  // com o terminal aberto, o código inteiro ainda cabe em cima
    const baseY = y + H - PH - 40 * u, cabem = Math.floor((baseY - yy) / lh) + 1, sobra = s.rolar_ate ? clamp(Math.ceil(s.rolar_ate - cabem + 2) * lh, 0, Math.max(0, linhas.length - cabem) * lh) : Math.max(0, linhas.length - cabem) * lh;
    const rDe = s.rolar_de || 1.6, rDur = s.rolar_dur || 1.5; const rolando = s.rolar && sobra > 0;
    const t0 = rolando ? rDe + rDur + 0.3 : 0.5; if (rolando) yy -= sobra * easeInOut((t - rDe) / rDur);
    ctx.save(); ctx.beginPath(); ctx.rect(tabX, top + 58 * u, W - sideW, y + H - PH - top - 60 * u); ctx.clip();
    const d0 = s.digitar_de || ((s.destaque && s.destaque.length) ? Math.min(...s.destaque) : 1);  // linhas antes disso já estão escritas
    const d1 = s.digitar_ate || linhas.length;  // linhas depois disso já estão escritas também
    const pronto = linhas.slice(0, d0 - 1).join("").length; const falta = Math.max(1, linhas.slice(0, d1).join("").length - pronto);
    const tDig = Math.max(0.8, Math.min(rolando ? Math.max(0.8, dur - t0 - 1.0) : dur * (s.vel || 0.7), falta / 18));
    const k = s.digitar === false ? 1 : clamp((t - t0) / tDig);
    if (s.rolar_depois && !rolando) yy -= Math.max(0, linhas.length - cabem) * lh * easeInOut((t - (s.digitar === false ? (s.rolar_de || 2.0) : t0 + tDig + 0.5)) / (s.rolar_dur || 1.4));  // digita no topo e depois desce até o fim do arquivo
    const dig = k; let resta = pronto + Math.floor(k * falta);
    // apagar: as linhas ficam vermelhas, somem, e o código de baixo sobe (a numeração se ajusta no fim)
    const AP = s.apagar || [], tA = s.apagar_em === undefined ? 1.0 : s.apagar_em, kR = easeOut((t - tA) / 0.4), kC = easeInOut((t - tA - 0.8) / 0.5); let num = 0;
    linhas.forEach((ln, i) => {
      const ap = AP.includes(i + 1), hf = ap ? 1 - kC : 1;
      if (ap && hf <= 0.002) { if (i + 1 <= d1) resta -= ln.length; return; }
      num += 1; const aL = ap ? a * (1 - kC) : a;
      if (ap && kR > 0) { ctx.save(); ctx.globalAlpha = 0.3 * kR * (1 - kC); ctx.fillStyle = "#ff6b6b"; ctx.fillRect(tabX, yy - lh * hf / 2, W - sideW, lh * hf); ctx.globalAlpha = kR * (1 - kC); ctx.fillRect(tabX, yy - lh * hf / 2, 6 * u, lh * hf); ctx.restore(); }
      const hl = (s.destaque || []).includes(i + 1);
      if (rolando && (s.marca_inicio || []).includes(i + 1)) { const hm = easeOut((t - 0.4) / 0.3) * (1 - easeOut((t - rDe - 0.6) / 0.4)); if (hm > 0) { ctx.save(); ctx.globalAlpha = 0.16 * hm; ctx.fillStyle = C.yel; ctx.fillRect(tabX, yy - lh / 2, W - sideW, lh); ctx.globalAlpha = hm; ctx.fillRect(tabX, yy - lh / 2, 6 * u, lh); ctx.restore(); } }
      if (hl && dig >= 1) { const ha = easeOut((t - (s.digitar === false ? (s.destaque_em || 1.2) : t0 + tDig)) / 0.4); ctx.save(); ctx.globalAlpha = 0.18 * ha; ctx.fillStyle = C.ac; ctx.fillRect(tabX, yy - lh / 2, W - sideW, lh); ctx.globalAlpha = ha; ctx.fillRect(tabX, yy - lh / 2, 6 * u, lh); ctx.restore(); }
      txt(ctx, String((kC >= 1 && AP.length ? num - 1 : i) + (s.linha0 || 1)), font(500, fs * 0.8, MONO), x0 - 30 * u, yy, "#4b5263", "right", aL);  // linha0: o trecho visível de um arquivo maior
      let mostra = i + 1 > d1 ? ln.length : Math.min(ln.length, resta); if (i + 1 <= d1) resta -= ln.length; let xx = x0;
      // descomentar: a linha começa com "// " (cinza, comentário) e as barras vão sendo apagadas, uma linha depois da outra
      const iD = (s.descomentar || []).indexOf(i + 1);
      if (iD >= 0) { const tD = (s.descomentar_em === undefined ? 1.2 : s.descomentar_em) + iD * 0.7, sobra = 3 - clamp(Math.floor((t - tD) / 0.16), 0, 3);
        if (sobra > 0) { const pre = "// ".slice(3 - sobra); txt(ctx, pre + ln, font(500, fs, MONO), x0, yy, "#6a737d", "left", aL);
          if (t >= tD - 0.3 && Math.floor(t * 2.5) % 2 === 0) { ctx.save(); ctx.globalAlpha = aL; ctx.fillStyle = C.ac; ctx.fillRect(x0 - 3 * u, yy - fs * 0.6, 4 * u, fs * 1.2); ctx.restore(); }
          mostra = 0; } }
      for (const [tk, cor] of tokens(ln)) { if (mostra <= 0) break; const parte = tk.slice(0, mostra); mostra -= tk.length; txt(ctx, parte, font(500, fs, MONO), xx, yy, cor, "left", aL); xx += tw(ctx, parte, font(500, fs, MONO)); }
      if (dig < 1 && i + 1 <= d1 && resta < 0 && resta + ln.length >= 0 && Math.floor(t * 2.5) % 2 === 0) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.ac; ctx.fillRect(xx + 2 * u, yy - fs * 0.6, 4 * u, fs * 1.2); ctx.restore(); }
      yy += lh * hf;
    });
    ctx.restore();
    if (PH) painelTerminal(ctx, u, tabX, y + H - PH, W - sideW, PH, t, dur, s, a);
    ctx.restore();
    if (s.navegador) navegadorPorCima(ctx, c, t, dur, s.navegador, media);
    legenda(ctx, c, t, s);
  };
  // painel TERMINAL dentro do VS Code: s.terminal = [{cmd, em}, {out, cor, em}] (em = fração da cena; ja:true = já estava lá)
  function painelTerminal(ctx, u, x, y, w, h, t, dur, s, a) {
    ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = C.term; ctx.fillRect(x, y, w, h - 22 * u); ctx.fillStyle = "rgba(255,255,255,.12)"; ctx.fillRect(x, y, w, 2 * u); ctx.restore();
    let tx = x + 36 * u; ["PROBLEMS", "OUTPUT", "DEBUG CONSOLE", "TERMINAL", "PORTS"].forEach((nm) => {
      const on = nm === "TERMINAL"; txt(ctx, nm, font(on ? 700 : 500, 19 * u), tx, y + 34 * u, on ? C.txt : C.mut, "left", a);
      const ww = tw(ctx, nm, font(on ? 700 : 500, 19 * u)); if (on) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = C.ac; ctx.fillRect(tx, y + 50 * u, ww, 3 * u); ctx.restore(); } tx += ww + 34 * u; });
    const pr = "PS " + (s.term_pasta || "...\\meu-primeiro-playwright") + "> "; const L = s.terminal;
    const maxc = Math.max(...L.map((l) => (l.cmd !== undefined ? pr.length + l.cmd.length : (l.out || "").length)));
    const fs = Math.min(28 * u, (w - 72 * u) / (maxc * 0.6)); const lh = fs * 1.6; let yy = y + 92 * u;
    // cada linha começa no seu "em", mas nunca antes de o comando de cima terminar de ser digitado (frase curta não mostra o resultado antes do comando)
    // frase curta: se a última linha não couber na cena, digita mais rápido (o resultado sempre aparece antes de a cena acabar)
    let vd = 1, tempos, durCmd = (l) => Math.max(0.3, Math.max(0.6, l.cmd.length / 22) / vd);
    for (vd of [1, 1.4, 2, 2.8, 4, 6]) { let livre = -1; tempos = L.map((l, i) => { if (l.ja) return -1; let t0 = Math.max(l.em !== undefined ? l.em * dur : 0.6 + i * 0.8, livre);
      if (l.cmd !== undefined) livre = t0 + durCmd(l) + 0.25 / vd; else livre = Math.max(livre, t0 + 0.15); return t0; });
      if (Math.max(...tempos) <= dur - 0.7) break; }
    const vis = L.map((l, i) => [l, tempos[i]]).filter(([, t0]) => t >= t0); const cabe = Math.max(1, Math.floor((h - 22 * u - 92 * u) / lh) + 1);
    if (!vis.length) {  // terminal ainda vazio: o prompt esperando, com o cursor piscando (no meio de um comando não aparece prompt)
      const ult = vis.length ? vis[vis.length - 1][0] : null; const yP = yy + Math.min(vis.length, cabe - 1) * lh;
      if (!ult || ult.cmd === undefined) { txt(ctx, pr, font(600, fs, MONO), x + 36 * u, yP, C.ac2, "left", a); if (Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = C.txt; ctx.fillRect(x + 36 * u + tw(ctx, pr, font(600, fs, MONO)) + 3 * u, yP - fs * 0.55, fs * 0.55, fs * 1.1); } } }
    vis.slice(-cabe).forEach(([l, t0]) => {  // como no terminal de verdade: quando enche, as linhas de cima sobem
      let px = x + 36 * u;
      if (l.cmd !== undefined) {
        const k = l.ja ? 1 : clamp((t - t0) / durCmd(l)); const cmd = l.cmd.slice(0, Math.ceil(k * l.cmd.length));
        txt(ctx, pr, font(600, fs, MONO), px, yy, C.ac2, "left", a); px += tw(ctx, pr, font(600, fs, MONO)); txt(ctx, cmd, font(600, fs, MONO), px, yy, C.txt, "left", a);
        if ((k < 1 || l.cmd === "") && Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = C.txt; ctx.fillRect(px + tw(ctx, cmd, font(600, fs, MONO)) + 3 * u, yy - fs * 0.55, fs * 0.55, fs * 1.1); }  // comando vazio: o cursor esperando
      } else txt(ctx, l.out, font(500, fs, MONO), px, yy, C[l.cor] || l.cor || C.mut, "left", a * (l.ja ? 1 : easeOut((t - t0) / 0.3)));
      yy += lh; });
  }
  // janela do navegador (gravação real) aparecendo por cima entre em e ate (frações da cena) e fechando sozinha
  function navegadorPorCima(ctx, c, t, dur, n, media) {
    const u = c.u, t0 = n.em * dur, t1 = n.ate * dur; if (t < t0 || t > t1) return;
    const kin = easeOut((t - t0) / 0.35), kout = 1 - easeOut((t - (t1 - 0.4)) / 0.4), a = Math.min(kin, kout), sc = lerp(0.88, 1, Math.min(kin, kout));
    const m0 = media && media[n.media]; const e0 = m0 && (m0.video || m0.img); const asp = e0 ? (e0.videoWidth || e0.width) / (e0.videoHeight || e0.height) : 16 / 9;
    const emPe = asp < 1;  // vídeo de celular: janela em pé
    const H = emPe ? 760 * u : 1150 * u * 9 / 16 + 64 * u, W = emPe ? (H - 64 * u) * asp : 1150 * u, x = c.cx - W / 2, y = c.cy - H / 2 - 40 * u;
    ctx.save(); ctx.translate(c.cx, y + H / 2); ctx.scale(sc, sc); ctx.translate(-c.cx, -(y + H / 2));
    const top = janela(ctx, x, y, W, H, u, n.titulo || "Chromium", a); const m = media && media[n.media]; const el = m && (m.video || m.img);
    ctx.save(); ctx.globalAlpha *= a; rr(ctx, x, top, W, H - (top - y), 0); ctx.clip();
    if (el) ctx.drawImage(el, x, top, W, H - (top - y)); else { ctx.fillStyle = "#fff"; ctx.fillRect(x, top, W, H - (top - y)); txt(ctx, "[ gravação: " + n.media + " ]", font(700, 36 * u), c.cx, top + (H - 64 * u) / 2, "#888", "center"); }
    ctx.restore(); ctx.restore();
  }

  // TERMINAL: {type:"terminal", pasta:"C:\\Users\\voce\\meu-projeto", linhas:[{cmd:"node -v"},{out:"v22.11.0", cor:"ac"}], legenda:"..."}
  // BLOCO DE NOTAS × VS CODE: o mesmo código, primeiro tudo preto no Bloco de Notas, depois colorido no VS Code
  // {type:"bloco_vs", codigo:"...", vs_em:2.2, legenda:"..."}
  S.bloco_vs = (ctx, c, t, dur, s) => {
    const u = c.u; const L = (s.codigo || "").split("\n"); const W = 840 * u, H = 470 * u, gap = 70 * u, y = topo(c, H) + 20 * u;
    const x1 = c.cx - W - gap / 2, x2 = c.cx + gap / 2; const fs = Math.min(26 * u, (W - 80 * u) / (Math.max(...L.map((l) => l.length)) * 0.6)); const lh = fs * 1.7;
    const a1 = easeOut(t / 0.4); const LE = s.codigo_esq ? s.codigo_esq.split("\n") : L; const escuro = !!s.codigo_esq;  // codigo_esq: comparação de código (ex.: Cypress × Playwright), as duas janelas escuras e coloridas
    const fsE = Math.min(fs, (W - 80 * u) / (Math.max(...LE.map((l) => l.length)) * 0.6));
    const top1 = janela(ctx, x1, y, W, H, u, s.janela_esq || "Sem título - Bloco de Notas", a1, escuro ? C.term : "#ffffff");
    LE.forEach((l, i) => { if (!escuro) { txt(ctx, l, font(500, fsE, MONO), x1 + 40 * u, top1 + 50 * u + i * fsE * 1.7, "#111111", "left", a1); return; }
      let xx = x1 + 40 * u; for (const [tk, cor] of tokens(l)) { txt(ctx, tk, font(500, fsE, MONO), xx, top1 + 50 * u + i * fsE * 1.7, cor, "left", a1); xx += tw(ctx, tk, font(500, fsE, MONO)); } });
    txt(ctx, s.titulo_esq || "BLOCO DE NOTAS", font(800, 44 * u), x1 + W / 2, y + H + 70 * u, C.txt, "center", a1); txt(ctx, s.sub_esq || "tudo da mesma cor", font(600, 30 * u), x1 + W / 2, y + H + 118 * u, C.mut, "center", a1);
    const t2 = s.vs_em || 2.0; const a2 = easeOut((t - t2) / 0.45); if (a2 <= 0) { legenda(ctx, c, t, s); return; }
    ctx.save(); ctx.translate(0, (1 - a2) * 30 * u); const top2 = janela(ctx, x2, y, W, H, u, s.janela_dir || "login.spec.js — Visual Studio Code", a2, C.term);
    L.forEach((l, i) => { let xx = x2 + 40 * u; for (const [tk, cor] of tokens(l)) { txt(ctx, tk, font(500, fs, MONO), xx, top2 + 50 * u + i * lh, cor, "left", a2); xx += tw(ctx, tk, font(500, fs, MONO)); } });
    txt(ctx, s.titulo_dir || "VS CODE", font(800, 44 * u), x2 + W / 2, y + H + 70 * u, C.yel, "center", a2); txt(ctx, s.sub_dir || "cada coisa de uma cor", font(600, 30 * u), x2 + W / 2, y + H + 118 * u, C.mut, "center", a2);
    ctx.restore(); legenda(ctx, c, t, s);
  };
  // DESAFIO: o enunciado em itens e a contagem regressiva "pausa o vídeo e tenta"
  // {type:"desafio", numero:"1", titulo:"Senha errada", itens:[["✓","usuário certo"],...], contagem:5, contagem_em:1.0}
  S.desafio = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4);
    txt(ctx, s.numero ? "DESAFIO " + s.numero : "DESAFIO", font(800, 40 * u), c.cx, c.H * 0.12, C.ac, "center", a);
    txt(ctx, s.titulo || "", caber(ctx, s.titulo || "", 900, 84 * u, c.W * 0.86), c.cx, c.H * 0.21, C.txt, "center", a);
    const L = s.itens || []; const W = 980 * u, lh = Math.min(92 * u, (c.H * 0.46) / Math.max(1, L.length)), x0 = c.W * 0.08, y0 = c.H * 0.32;
    L.forEach(([ic, tx, cor], i) => { const k = easeOut((t - 0.4 - i * 0.3) / 0.35); if (k <= 0) return; const yy = y0 + i * lh + lh / 2;
      ctx.save(); ctx.globalAlpha = a * k * 0.9; rr(ctx, x0, yy - lh * 0.42, W, lh * 0.84, 18 * u); ctx.fillStyle = C.win; ctx.fill(); ctx.fillStyle = cor || C.ac; ctx.fillRect(x0, yy - lh * 0.42, 8 * u, lh * 0.84); ctx.restore();
      txt(ctx, ic, font(800, 40 * u), x0 + 56 * u, yy, cor || C.ac, "center", a * k); txt(ctx, tx, caber(ctx, tx, 700, 40 * u, W - 140 * u), x0 + 104 * u, yy, C.txt, "left", a * k); });
    // contagem: anel que esvazia e o número no meio
    const n = s.contagem || 5, t0 = s.contagem_em !== undefined ? s.contagem_em : Math.max(0.8, dur - n - 0.5), cx = c.W * 0.79, cy = c.H * 0.5, R = 170 * u; const kc = easeOut((t - t0 + 0.3) / 0.4);
    if (kc > 0) { const el = clamp((t - t0) / n); const resta = Math.max(1, n - Math.floor(Math.max(0, t - t0)));
      ctx.save(); ctx.globalAlpha = a * kc; ctx.lineWidth = 18 * u; ctx.strokeStyle = "rgba(255,255,255,.08)"; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.stroke();
      ctx.strokeStyle = el < 1 ? C.yel : C.ac; ctx.lineCap = "round"; ctx.beginPath(); ctx.arc(cx, cy, R, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (1 - el)); ctx.stroke(); ctx.restore();
      txt(ctx, el < 1 ? String(resta) : "▶", font(900, 150 * u), cx, cy, el < 1 ? C.yel : C.ac, "center", a * kc);
      txt(ctx, "⏸  pausa o vídeo e tenta", font(800, 38 * u), cx, cy + R + 70 * u, C.txt, "center", a * kc); }
    legenda(ctx, c, t, s);
  };
  S.terminal = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 1000 : 1600) * u, H = (c.vertical ? 900 : 660) * u;
    const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, s.titulo || "Terminal", a, C.term);
    // cabe na janela: encurta o caminho do prompt; a fonte fica entre 30 e 40; comando longo quebra de linha (como no terminal de verdade)
    let pasta = s.pasta || "C:\\meu-projeto"; const L0 = s.linhas || [];
    const maxCmd = Math.max(0, ...L0.map((l) => (l.cmd !== undefined ? l.cmd.length : 0)));
    if (("PS " + pasta + "> ").length + maxCmd > 58 && pasta.includes("\\")) pasta = "...\\" + pasta.split("\\").pop();
    const pr = (s.prompt || "PS " + pasta + ">") + " "; const fsMin = (s.fonte_min || (c.vertical ? 26 : 30)) * u;  // fonte_min: saída longa de erro cabe sem quebrar
    const larg = (n) => (W - 90 * u) / (n * 0.6);
    const chars0 = Math.max(10, ...L0.map((l) => (l.cmd !== undefined ? pr.length + l.cmd.length : (l.out || "").length)));
    const fs = Math.max(fsMin, Math.min((s.fonte || 40) * u, larg(chars0 + 1))); const cap = Math.floor((W - 90 * u) / (fs * 0.6));
    const L = []; L0.forEach((l) => {
      if (l.cmd !== undefined && pr.length + l.cmd.length > cap) { let r = l.cmd, first = true; while (r.length) { let n = first ? cap - pr.length : cap; if (r.length > n) { const cut = Math.max(r.lastIndexOf(" ", n - 1), r.lastIndexOf("/", n - 1)); if (cut > n * 0.5) n = cut + 1; } L.push({ cmd: r.slice(0, n), cont: !first, ja: l.ja }); r = r.slice(n); first = false; } }
      else if (l.out !== undefined && l.out.length > cap) { for (let i = 0; i < l.out.length; i += cap) L.push(Object.assign({}, l, { out: l.out.slice(i, i + cap) })); }
      else L.push(l); });
    const lh = s.compacto ? Math.max(fs * 1.4, 32 * u) : Math.max(fs * 1.6, 40 * u); let yy = top + (s.compacto ? 44 : 56) * u;  /* compacto: listas longas (git status) cabem inteiras */
    // linhas com ja:true já estavam na tela na cena anterior: aparecem prontas, sem digitar de novo
    const nPassos = L.filter((l) => !l.ja && l.cmd !== undefined && !l.cont).length + L.filter((l) => !l.ja && l.out !== undefined).length * 0.35 + L.filter((l) => !l.ja && l.cont).length * 0.6;
    const passo = Math.max(0.6, (dur * (s.vel || 0.75) - 0.5) / Math.max(nPassos, 1)); let tt = t - 0.5;
    const hl = s.destaque || []; let jl = -1;
    for (const l of L) {
      jl++; if (hl.includes(jl)) { const kh = easeOut((t - (s.destaque_em || 1.0)) / 0.35); if (kh > 0) { ctx.save(); ctx.globalAlpha = a * kh * 0.2; ctx.fillStyle = C.yel; ctx.fillRect(x + 20 * u, yy - lh / 2, W - 40 * u, lh); ctx.globalAlpha = a * kh; ctx.fillRect(x + 20 * u, yy - lh / 2, 6 * u, lh); ctx.restore(); } }  // destaque: linhas apontadas (índice em s.linhas)
      if (l.ja) { let px = x + 40 * u;
        if (l.cmd !== undefined) { if (!l.cont) { txt(ctx, pr, font(600, fs, MONO), px, yy, C.ac2, "left", a); px += tw(ctx, pr, font(600, fs, MONO)); } txt(ctx, l.cmd, font(600, fs, MONO), px, yy, C.txt, "left", a); }
        else txt(ctx, l.out, font(500, fs, MONO), px, yy, C[l.cor] || l.cor || C.mut, "left", a);
        yy += lh; continue; }
      if (tt < 0) {  // antes de digitar: o prompt já está lá, com o cursor piscando (terminal nunca aparece vazio)
        if (l.cmd !== undefined && !l.cont) { txt(ctx, pr, font(600, fs, MONO), x + 40 * u, yy, C.ac2, "left", a); if (Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = C.txt; ctx.fillRect(x + 40 * u + tw(ctx, pr, font(600, fs, MONO)) + 4 * u, yy - fs * 0.55, fs * 0.55, fs * 1.1); } }
        break; }
      if (l.cmd !== undefined) {
        const pc = l.cont ? passo * 0.6 : passo; const k = clamp(tt / Math.max(0.4, pc * 0.75)); const cmd = l.cmd.slice(0, Math.ceil(k * l.cmd.length));
        let px = x + 40 * u; if (!l.cont) { txt(ctx, pr, font(600, fs, MONO), px, yy, C.ac2, "left", a); px += tw(ctx, pr, font(600, fs, MONO)); }
        txt(ctx, cmd, font(600, fs, MONO), px, yy, C.txt, "left", a);
        if (k < 1 && Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = C.txt; ctx.fillRect(px + tw(ctx, cmd, font(600, fs, MONO)) + 4 * u, yy - fs * 0.55, fs * 0.55, fs * 1.1); }
        tt -= pc;
      } else {
        txt(ctx, l.out, font(500, fs, MONO), x + 40 * u, yy, C[l.cor] || l.cor || C.mut, "left", a * easeOut(tt / 0.3)); tt -= passo * 0.35;
      }
      yy += lh;
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
    if (s.botao) s = Object.assign({}, s, { seleciona_em: Math.min(s.seleciona_em || 1.2, dur * 0.22), botao_em: Math.min(s.botao_em || 2.6, dur * 0.72) });  // a escolha da pasta sempre cabe na cena, por mais curta que seja
    const u = c.u; const a = easeOut(t / 0.4); const W = (c.vertical ? 1000 : 1500) * u, H = (c.vertical ? 1000 : 660) * u;
    const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, s.titulo || "Explorador de Arquivos", a, "#f3f4f7");
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#e4e7ee"; ctx.fillRect(x, top, W, 70 * u); ctx.restore();
    pastaIcone(ctx, x + 34 * u, top + 18 * u, 40 * u, a);
    txt(ctx, s.caminho || "Documentos", font(600, 28 * u), x + 92 * u, top + 35 * u, "#3a3f4b", "left", a);
    const itens = (s.itens || []).map((i) => (typeof i === "string" ? { nome: i } : i)); const cols = c.vertical ? 3 : 5; const cell = (W - 80 * u) / cols;
    itens.forEach((it, i) => {
      const cx = x + 40 * u + (i % cols) * cell + cell / 2, cy = top + 130 * u + Math.floor(i / cols) * 250 * u;
      const st = it.novo ? (s.novo_em || 1.0) : 0.15 + i * 0.08; const k = backOut((t - st) / 0.45); const ka = easeOut((t - st) / 0.3);
      if (ka <= 0) return; const sz = 150 * u * (it.novo ? lerp(0.4, 1, k) : 1);
      if (it.novo && t > st + 0.5) { ctx.save(); ctx.globalAlpha = 0.25 * easeOut((t - st - 0.5) / 0.4); rr(ctx, cx - cell / 2 + 20 * u, cy - 20 * u, cell - 40 * u, 268 * u, 18 * u); ctx.fillStyle = C.ac2; ctx.fill(); ctx.restore(); }
      if (it.arquivo) { const fw = sz * 0.62, fh = sz * 0.8, fx = cx - fw / 2, fy = cy + (150 * u - fh) / 2; ctx.save(); ctx.globalAlpha *= ka;
        ctx.beginPath(); ctx.moveTo(fx, fy); ctx.lineTo(fx + fw * 0.68, fy); ctx.lineTo(fx + fw, fy + fw * 0.32); ctx.lineTo(fx + fw, fy + fh); ctx.lineTo(fx, fy + fh); ctx.closePath();
        ctx.fillStyle = "#fff"; ctx.fill(); ctx.strokeStyle = "#9aa3b5"; ctx.lineWidth = 3 * u; ctx.stroke(); ctx.fillStyle = it.cor || "#2f6fe4"; rr(ctx, fx + fw * 0.18, fy + fh * 0.5, fw * 0.64, fh * 0.28, 6 * u); ctx.fill(); ctx.restore();
        txt(ctx, it.ext || "EXE", font(900, sz * 0.13), cx, fy + fh * 0.64, "#fff", "center", ka); }
      else pastaIcone(ctx, cx - sz / 2, cy + (150 * u - sz) / 2, sz, ka, C.folder);
      const nome = it.novo ? it.nome.slice(0, Math.ceil(clamp((t - st - 0.6) / 0.8) * it.nome.length)) : it.nome;
      // nome comprido quebra em 2 linhas (como no Windows), cortando depois de um traço ou espaço; só encolhe se ainda não couber
      const pesoN = it.novo ? 800 : 600, maxN = cell - 56 * u; let lin = [it.nome];
      if (tw(ctx, it.nome, font(pesoN, 30 * u)) > maxN) { let melhor = -1; for (let j = 1; j < it.nome.length; j++) if (/[-_ ]/.test(it.nome[j - 1]) && Math.abs(j - it.nome.length / 2) < Math.abs(melhor - it.nome.length / 2)) melhor = j; if (melhor > 0) lin = [it.nome.slice(0, melhor), it.nome.slice(melhor)]; }
      const fN = font(pesoN, Math.min(30 * u, ...lin.map((l) => 30 * u * Math.min(1, maxN / tw(ctx, l, font(pesoN, 30 * u))))));
      let resta = nome.length; lin.forEach((l, j) => { const parte = l.slice(0, Math.max(0, resta)); resta -= l.length; txt(ctx, parte, fN, cx, cy + (180 + j * 36) * u, "#2a2f3a", "center", ka); });
      if (s.seleciona === i) { const ks = easeOut((t - (s.seleciona_em || 1.2)) / 0.25); if (ks > 0) { ctx.save(); ctx.globalAlpha = 0.3 * ks; rr(ctx, cx - cell / 2 + 20 * u, cy - 20 * u, cell - 40 * u, 268 * u, 18 * u); ctx.fillStyle = "#2f6fe4"; ctx.fill(); ctx.globalAlpha = ks; ctx.strokeStyle = "#2f6fe4"; ctx.lineWidth = 3 * u; ctx.stroke(); ctx.restore(); } }
    });
    // janela de escolher pasta (Open Folder): o item escolhido fica azul e o cursor clica no botão
    if (s.botao) { const bw = tw(ctx, s.botao, font(700, 26 * u)) + 70 * u, bh = 62 * u, bx = x + W - bw - 40 * u, by = y + H - bh - 30 * u, tb = s.botao_em || 2.6;
      const kb = easeOut((t - tb - 0.1) / 0.2); ctx.save(); ctx.globalAlpha = a; rr(ctx, bx, by, bw, bh, 10 * u); ctx.fillStyle = kb > 0 ? "#1d55c0" : "#2f6fe4"; ctx.fill(); ctx.restore();
      txt(ctx, s.botao, font(700, 26 * u), bx + bw / 2, by + bh / 2, "#fff", "center", a);
      rr(ctx, x + 40 * u, by, W - bw - 120 * u, bh, 10 * u); ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = "#c4c9d4"; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
      txt(ctx, "Pasta:  " + (t > (s.seleciona_em || 1.2) && s.seleciona !== undefined ? ((s.itens[s.seleciona].nome) || s.itens[s.seleciona]) : ""), font(600, 26 * u), x + 64 * u, by + bh / 2, "#2a2f3a", "left", a);
      if (s.seleciona !== undefined) { const i = s.seleciona, cols0 = c.vertical ? 3 : 5, cell0 = (W - 80 * u) / cols0; const ix = x + 40 * u + (i % cols0) * cell0 + cell0 / 2, iy = top + 205 * u + Math.floor(i / cols0) * 250 * u;
        if (t <= tb - 0.9) cursor(ctx, u, ix + 30 * u, iy, t, s.seleciona_em || 1.2); else { const kk = easeOut((t - (tb - 0.9)) / 0.7); cursor(ctx, u, lerp(ix + 30 * u, bx + bw / 2, kk), lerp(iy, by + bh / 2, kk), t, tb); } } }  /* um cursor só: da pasta até o botão */
    legenda(ctx, c, t, s);
  };

  // CARDS: {type:"cards", titulo:"O QUE VAMOS INSTALAR", itens:[["✎","VS Code","onde você escreve o código"],["⬢","Node.js","o motor que roda o Cypress"],["⑂","Git","guarda o histórico"]]}
  S.cards = (ctx, c, t, dur, s) => {
    const u = c.u; const it = s.itens || []; const n = it.length; const V = c.vertical;
    const cw = V ? 860 * u : Math.min(520, 1700 / n - 40) * u, ch = V ? 300 * u : 560 * u, gap = 44 * u;
    if (s.titulo) txt(ctx, s.titulo, caber(ctx, s.titulo, 800, 46 * u, c.W * 0.9), c.cx, V ? c.H * 0.16 : c.cy - ch / 2 - 90 * u, C.mut, "center", easeOut(t / 0.3));
    const passo = Math.min(1.0, (dur - 0.6) / Math.max(n, 1));
    it.forEach(([ic, ti, sub, cor], i) => {
      const st = s.juntos ? 0.2 : 0.2 + i * passo; const ka = easeOut((t - st) / 0.35), k = backOut((t - st) / 0.45); if (ka <= 0) return;
      const x = V ? c.cx - cw / 2 : c.cx - (n * cw + (n - 1) * gap) / 2 + i * (cw + gap), y = V ? c.H * 0.22 + i * (ch + gap) : c.cy - ch / 2;
      ctx.save(); ctx.globalAlpha = ka; ctx.translate(x + cw / 2, y + ch / 2); ctx.scale(lerp(0.9, 1, k), lerp(0.9, 1, k)); ctx.translate(-(x + cw / 2), -(y + ch / 2));
      ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 40 * u; rr(ctx, x, y, cw, ch, 28 * u); ctx.fillStyle = C.win; ctx.fill(); ctx.shadowColor = "transparent";
      ctx.fillStyle = cor || C.ac; rr(ctx, x, y, cw, 10 * u, 5 * u); ctx.fill();
      const icY = V ? y + ch / 2 : y + 170 * u, icX = V ? x + 150 * u : x + cw / 2;
      ctx.beginPath(); ctx.arc(icX, icY, 80 * u, 0, 7); ctx.fillStyle = "rgba(255,255,255,.06)"; ctx.fill(); ctx.restore();
      txt(ctx, ic, caber(ctx, ic, 800, 84 * u, 130 * u), icX, icY + 4 * u, cor || C.ac, "center", ka);
      if (V) { txt(ctx, ti, caber(ctx, ti, 900, 60 * u, cw - 310 * u), x + 280 * u, y + ch / 2 - 36 * u, C.txt, "left", ka); txt(ctx, sub, font(500, 34 * u), x + 280 * u, y + ch / 2 + 34 * u, C.mut, "left", ka); }
      else { txt(ctx, ti, caber(ctx, ti, 900, 58 * u, cw - 50 * u), x + cw / 2, y + 330 * u, C.txt, "center", ka);
        const ws = String(sub || "").split(" "); let l1 = "", l2 = ""; ws.forEach((w) => { if ((l1 + " " + w).length < 22 && !l2) l1 = (l1 + " " + w).trim(); else l2 = (l2 + " " + w).trim(); });
        txt(ctx, l1, font(500, 32 * u), x + cw / 2, y + 410 * u, C.mut, "center", ka); txt(ctx, l2, font(500, 32 * u), x + cw / 2, y + 455 * u, C.mut, "center", ka); }
    });
  };

  // CONHECIDOS: os nomes (seletores) que a gente já achou em aulas anteriores, com a aula de onde vieram
  S.conhecidos = (ctx, c, t, dur, s) => {
    const u = c.u; const L = s.itens || []; const n = L.length; const en = global.CO_IDIOMA === "en";
    txt(ctx, s.titulo || (en ? "YOU ALREADY KNOW THESE" : "VOCÊ JÁ CONHECE ESSES"), font(800, 46 * u), c.cx, c.H * 0.14, C.mut, "center", easeOut(t / 0.3));
    const rh = Math.min(118 * u, (c.H * 0.7) / Math.max(n, 1)), w = 1560 * u, x = c.cx - w / 2, y0 = c.H * 0.22;
    const passo = Math.min(0.9, (dur - 0.8) / Math.max(n, 1));
    L.forEach(([sel, desc, aula, nova], i) => {
      const st = 0.3 + i * passo, ka = easeOut((t - st) / 0.35); if (ka <= 0) return; const y = y0 + i * rh, cor = nova ? C.yel : C.ac;
      ctx.save(); ctx.globalAlpha = ka; rr(ctx, x, y, w, rh - 18 * u, 18 * u); ctx.fillStyle = C.win; ctx.fill(); ctx.fillStyle = cor; rr(ctx, x, y, 10 * u, rh - 18 * u, 5 * u); ctx.fill(); ctx.restore();
      const cy = y + (rh - 18 * u) / 2; let fs = 36 * u; while (fs > 20 * u && tw(ctx, sel, font(700, fs, MONO)) > 820 * u) fs -= 1 * u;
      txt(ctx, sel, font(700, fs, MONO), x + 44 * u, cy, cor, "left", ka);
      txt(ctx, desc, font(600, 32 * u), x + 900 * u, cy, C.txt, "left", ka);
      const etq = nova ? (en ? "NEW" : "NOVO") : (en ? "lesson " : "aula ") + aula, bw = tw(ctx, etq, font(800, 28 * u)) + 44 * u;
      ctx.save(); ctx.globalAlpha = ka; rr(ctx, x + w - bw - 30 * u, cy - 26 * u, bw, 52 * u, 26 * u); ctx.fillStyle = nova ? "rgba(255,210,63,.18)" : "rgba(63,214,138,.16)"; ctx.fill(); ctx.restore();
      txt(ctx, etq, font(800, 28 * u), x + w - bw / 2 - 30 * u, cy, cor, "center", ka);
    });
  };

  // RECORTE: cena horizontal (tela, devtools, runner…) dentro do vídeo vertical — desenha a cena num quadro 1920x1080
  // e mostra só um pedaço dele, ampliado. {type:"recorte", corte:[x,y,w,h], cena:{...}, legenda:"..."}
  S.recorte = (ctx, c, t, dur, s, media) => {
    const inner = s.cena || {}; const F = S[inner.type] || S.bigtext;
    if (!c.vertical) return F(ctx, c, t, dur, inner, media);
    const oc = S.recorte._cv || (S.recorte._cv = document.createElement("canvas")); oc.width = 1920; oc.height = 1080;
    const o = oc.getContext("2d"); o.clearRect(0, 0, 1920, 1080);
    F(o, { W: 1920, H: 1080, vertical: false, u: 1, cx: 960, cy: 486 }, t, dur, Object.assign({}, inner, { legenda: "" }), media);
    const [x, y, w, h] = s.corte || [160, 30, 1600, 880]; const dw = c.W * (s.largura || 0.96), dh = Math.min(dw * h / w, c.H * 0.62), dw2 = dh * w / h;
    const a = easeOut(t / 0.3); ctx.save(); ctx.globalAlpha = a; ctx.drawImage(oc, x, y, w, h, (c.W - dw2) / 2, c.H * 0.42 - dh / 2, dw2, dh); ctx.restore();
    legenda(ctx, c, t, { legenda: s.legenda !== undefined ? s.legenda : inner.legenda, legenda_em: s.legenda_em });
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
  // TELA CHEIA: gravação real da tela inteira (ex.: o codegen gravado no Xvfb), ocupando o quadro todo.
  // {type:"tela_cheia", media:"cg19_usuario", gravar:true, recorte:[x0,y0,x1,y1] (opcional, 0-1), legenda:"..."}  — imagem também serve (sem gravar)
  S.tela_cheia = (ctx, c, t, dur, s, media) => {
    const a = easeOut(t / 0.3); const m = media && media[s.media]; const el = m && (m.video || m.img);
    if (el) { const iw = el.videoWidth || el.width, ih = el.videoHeight || el.height; const [x0, y0, x1, y1] = s.recorte || [0, 0, 1, 1];
      ctx.save(); ctx.globalAlpha = a; ctx.drawImage(el, x0 * iw, y0 * ih, (x1 - x0) * iw, (y1 - y0) * ih, 0, 0, c.W, c.H); ctx.restore(); }
    else { ctx.fillStyle = "#11131a"; ctx.fillRect(0, 0, c.W, c.H); txt(ctx, "[ gravação: " + (s.media || "?") + " ]", font(700, 40 * c.u), c.cx, c.cy, C.mut, "center", a); }
    legenda(ctx, c, t, s);
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
    const bh = 64 * u, bw2 = Math.max(190 * u, tw(ctx, s.botao || "Next", font(700, 30 * u)) + 50 * u), by2 = y + H - bh - 40 * u;
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
    const t0 = y + 64 * u, ex0 = x + LW + 30 * u, ew0 = W - LW - 60 * u; const AN = s.antes || []; const off = AN.length * 50 * u;  // testes anteriores (já verdes)
    const R = { lista: [x, t0 + 64 * u, LW, y + H - t0 - 64 * u], passo: [x, t0 + 160 * u + off + (P.length - 1) * 50 * u - 24 * u, LW, 48 * u],
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
    txt(ctx, (fim ? (falha ? "✗ 1" : "✓ " + (1 + AN.length)) : "…"), font(800, 26 * u), x + LW - 30 * u, top + 34 * u, fim ? (falha ? C.red : C.ac) : C.mut, "right", a);
    AN.forEach((n, i) => { const ay = top + 104 * u + i * 50 * u; ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(x + 40 * u, ay, 11 * u, 0, 7); ctx.fillStyle = C.ac; ctx.fill(); ctx.restore();
      txt(ctx, "✓", font(900, 15 * u), x + 40 * u, ay + 1 * u, "#0b1a12", "center", a); txt(ctx, n, font(600, 26 * u), x + 66 * u, ay, C.mut, "left", a); });
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.line; ctx.fillRect(x, top + 64 * u, LW, 2 * u); ctx.restore();
    const cor = fim ? (falha ? C.red : C.ac) : C.yel;
    ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(x + 40 * u, top + 104 * u + off, 11 * u, 0, 7); ctx.fillStyle = cor; ctx.fill(); ctx.restore();
    txt(ctx, s.teste || "teste", font(700, 28 * u), x + 66 * u, top + 104 * u + off, C.txt, "left", a);
    let yy = top + 160 * u + off;
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
    (h.attrs || []).filter(([k]) => (s.attrs || ["class", "placeholder", "type", "data-test", "data-cy", "id", "name", "value", "href"]).includes(k)).forEach(([k, v]) => (v = String(v).length > 34 ? String(v).slice(0, 32) + "…" : v, L.push({ n: 5, p: [[k, "an"], ...(v !== "" ? [["=", "pu"], [`"${v}"`, "av"]] : [])], sel: true, attr: k })));
    L[L.length - 1].p.push(["> == $0", "pu"]); L.push({ n: 3, p: [["</", "pu"], [pt, "tag"], [">", "pu"]] });
    return L;
  }
  // o "monte de código" de quando o DevTools abre sem apontar pra nada (fe = recolhido)
  const BAGUNCA = [[0, "html", " lang", "\"en\"", 1], [1, "head", 0], [1, "body", 0, 0, 1], [2, "noscript", 0], [2, "div", " id", "\"root\"", 1], [3, "div", " class", "\"login_container\"", 1], [4, "div", " class", "\"login_logo\""], [4, "div", " class", "\"login_wrapper\"", 1],
    [5, "div", " class", "\"login_wrapper-inner\"", 1], [6, "div", " id", "\"login_button_container\"", 1], [7, "div", " class", "\"login-box\"", 1], [8, "form", 0, 0, 1], [9, "div", " class", "\"form_group\""], [9, "div", " class", "\"form_group\""], [5, "div", " class", "\"login_credentials_wrap\""], [2, "script", " src", "\"/static/js/main.js\""]]
    .map(([n, tg, an, av, aberto]) => ({ n, fe: aberto ? 0 : 1, p: [["<", "pu"], [tg, "tag"], ...(an ? [[an, "an"], ["=", "pu"], [av, "av"]] : []), [aberto ? ">" : ">…</" + tg + ">", "pu"]] }));
  const DT = { tag: "#5db0d7", an: "#9bbbdc", av: "#f29766", pu: "#a8a8a8", tx: "#e8eaed" };

  // DEVTOOLS: botão direito › Inspecionar no site de verdade; abre o painel com o HTML real do elemento e realça atributos
  // {type:"devtools", media:"insp_user", url:"https://www.saucedemo.com", inspecionar:"#user-name", realce:["data-test","id"], realce_em:5, legenda:"..."}
  S.devtools = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1640 * u, H = 720 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, s.titulo || (s.url || "").replace(/^https?:\/\//, "").replace(/\/$/, ""), a, "#fff");
    const m = media && media[s.media]; const el = m && (m.video || m.img); const e = s.elem || [0.37, 0.3, 0.63, 0.36];
    const seta = !!s.seta; if (seta) s = Object.assign({}, s, { aberto: true });  // modo "setinha": painel já aberto com o código todo, e a setinha leva até o campo
    const tPick = s.seta_em || 1.6, tEl = tPick + 1.9;
    const tc = s.clique_em || 1.6, tMenu = tc, tIn = tc + 1.0, tOpen = s.aberto ? -2 : tIn + 0.35;
    const ko = s.aberto ? 1 : easeOut((t - tOpen) / 0.6); const PW = (s.painel || 0.5) * W * ko; const sw = W - PW, sh = y + H - top;
    const ex = (e[0] + e[2]) / 2, ey = (e[1] + e[3]) / 2;
    const p = print(ctx, el, x, top, sw, sh, a, "#fff", [ex, ey], lerp(1, s.zoom_site || 1.8, ko));
    if (!el) txt(ctx, s.url || "site", font(700, 34 * u), x + sw / 2, top + sh / 2, C.mut, "center", a);
    const kh = seta ? easeOut((t - tEl + 0.55) / 0.2) : s.aberto ? 1 : easeOut((t - tOpen - 0.3) / 0.4);
    const h = s.html || {}; const idv = (h.attrs || []).find((q) => q[0] === "id"); const cls = (h.attrs || []).find((q) => q[0] === "class");
    void cls; caixaElem(ctx, u, p, e, kh * a, (h.tag || "input") + (idv ? "#" + idv[1] : "") + (s.elem_tam ? `  ${s.elem_tam[0]}×${s.elem_tam[1]}` : ""));
    if (PW > 2) {  // painel do DevTools
      const px = x + sw; ctx.save(); ctx.beginPath(); ctx.rect(px, top, PW, sh - 2 * u); ctx.clip(); ctx.globalAlpha = a;
      ctx.fillStyle = "#202124"; ctx.fillRect(px, top, PW, sh); ctx.fillStyle = "#292a2d"; ctx.fillRect(px, top, PW, 56 * u); ctx.fillStyle = "#3c4043"; ctx.fillRect(px, top + 56 * u, PW, 2 * u);
      ctx.fillStyle = "#3c4043"; ctx.fillRect(px, top, 3 * u, sh); ctx.restore();
      ctx.save(); ctx.beginPath(); ctx.rect(px, top, PW, sh - 2 * u); ctx.clip();
      const ic = [px + 34 * u, top + 28 * u]; const kAt = seta && t > tPick && t < tEl + 0.1 ? 1 : 0;
      ctx.save(); ctx.globalAlpha = a; if (kAt) { ctx.fillStyle = "rgba(138,180,248,.18)"; rr(ctx, ic[0] - 20 * u, ic[1] - 20 * u, 40 * u, 40 * u, 6 * u); ctx.fill(); }
      ctx.strokeStyle = kAt ? "#8ab4f8" : "#c4c7c5"; ctx.lineWidth = 2.4 * u; ctx.setLineDash([4 * u, 3 * u]); ctx.strokeRect(ic[0] - 12 * u, ic[1] - 12 * u, 18 * u, 18 * u); ctx.setLineDash([]);
      ctx.fillStyle = kAt ? "#8ab4f8" : "#c4c7c5"; ctx.beginPath(); ctx.moveTo(ic[0] - 2 * u, ic[1] - 2 * u); ctx.lineTo(ic[0] + 13 * u, ic[1] + 4 * u); ctx.lineTo(ic[0] + 6 * u, ic[1] + 6 * u); ctx.lineTo(ic[0] + 4 * u, ic[1] + 13 * u); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = "#c4c7c5"; ctx.lineWidth = 2.4 * u; rr(ctx, ic[0] + 30 * u, ic[1] - 13 * u, 16 * u, 26 * u, 3 * u); ctx.stroke(); rr(ctx, ic[0] + 48 * u, ic[1] - 6 * u, 12 * u, 19 * u, 3 * u); ctx.stroke(); ctx.restore();
      if (seta && t > tPick - 0.6) { const kp = t < tEl ? easeOut((t - tPick + 0.6) / 0.25) : 0; ctx.save(); ctx.globalAlpha = kp; ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; rr(ctx, ic[0] - 22 * u, ic[1] - 22 * u, 44 * u, 44 * u, 8 * u); ctx.stroke(); ctx.restore(); }
      let tx = px + 120 * u; ["Elements", "Console", "Sources", "Network"].forEach((n, i) => { txt(ctx, n, font(600, 23 * u), tx, top + 28 * u, i ? "#9aa0a6" : "#e8eaed", "left", a);
        const w = tw(ctx, n, font(600, 23 * u)); if (!i) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#8ab4f8"; ctx.fillRect(tx - 6 * u, top + 52 * u, w + 12 * u, 4 * u); ctx.restore(); } tx += w + 40 * u; });
      const bag = seta && t < tEl + 0.05; const tL = seta ? tEl : tOpen;
      const L = bag ? BAGUNCA : linhasHtml(s); const fs = (s.fonte || 25) * u, lh = fs * 1.62; let yy = top + 100 * u; const ind = 26 * u;
      const re = s.realce || []; const r0 = s.realce_em || Math.min(dur - 1.5, tL + 2.2);
      L.forEach((ln, i) => {
        const kl = bag ? a : easeOut((t - tL - 0.15 - i * 0.04) / 0.3) * a; if (kl <= 0) return;
        if (ln.sel) { ctx.save(); ctx.globalAlpha = kl; ctx.fillStyle = "#1d3b5a"; ctx.fillRect(px + 3 * u, yy - lh / 2, PW, lh); ctx.restore(); }
        let xx = px + 30 * u + ln.n * ind; if ((bag ? ln.fe !== undefined : i < 4) && !ln.sel) txt(ctx, bag && ln.fe ? "▸" : "▾", font(600, fs * 0.7), xx - 18 * u, yy, "#9aa0a6", "left", kl);
        const ri = ln.attr ? re.indexOf(ln.attr) : -1;
        if (ri >= 0) { const kr = easeOut((t - r0 - ri * 1.2) / 0.35); if (kr > 0) { const w = ln.p.reduce((q, [tk]) => q + tw(ctx, tk, font(600, fs, MONO)), 0);
          ctx.save(); ctx.globalAlpha = kr; ctx.fillStyle = "rgba(255,210,63,.18)"; rr(ctx, xx - 10 * u, yy - lh / 2 + 2 * u, w + 20 * u, lh - 4 * u, 8 * u); ctx.fill(); ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; ctx.stroke(); ctx.restore();
          if (ri === 0) txt(ctx, "← " + (s.realce_rotulo || "use este!"), font(800, 24 * u), xx + w + 26 * u, yy, C.yel, "left", kr); } }
        for (const [tk, k] of ln.p) { txt(ctx, tk, font(600, fs, MONO), xx, yy, DT[k] || DT.tx, "left", kl); xx += tw(ctx, tk, font(600, fs, MONO)); }
        yy += lh;
      });
      ctx.restore();
    }
    if (seta) {  // dica + mouse: setinha › campo
      const px = x + sw, ic = [px + 34 * u, top + 28 * u]; const kt = t > tPick - 1.0 && t < tPick + 0.7 ? easeOut((t - tPick + 1.0) / 0.25) : 0;
      if (kt > 0) { const l1 = global.CO_IDIOMA === "en" ? "Select an element in the page to inspect it" : "Selecionar um elemento da página", l2 = "Ctrl + Shift + C";
        const f = font(600, 21 * u), w = Math.max(tw(ctx, l1, f), tw(ctx, l2, f)) + 32 * u; ctx.save(); ctx.globalAlpha = kt; rr(ctx, ic[0] - 10 * u, ic[1] + 34 * u, w, 72 * u, 8 * u); ctx.fillStyle = "#3c4043"; ctx.fill(); ctx.restore();
        txt(ctx, l1, f, ic[0] + 6 * u, ic[1] + 56 * u, "#e8eaed", "left", kt); txt(ctx, l2, font(800, 21 * u, MONO), ic[0] + 6 * u, ic[1] + 86 * u, C.yel, "left", kt); }
      const [ax, ay] = p(ex, ey); rota(ctx, u, [[ic[0], ic[1], tPick, "#8ab4f8"], [ax, ay, tEl, "#8ab4f8"]], t);
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
    const tc2 = tc1 + (s.campo_em || 1.7), tc3 = tc2 + (s.copiar_em || 2.0); const kh = easeOut((t - tc2) / 0.25);  // só destaca depois do clique no campo
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
    const M = s.menus || []; const tc0 = s.clique_em || 1.2, passo = s.passo || Math.max(1.15, (dur * 0.62 - tc0) / Math.max(M.length, 1));; const cam = s.caminho || [];  // o menu fica aberto boa parte da frase
    const tFim = tc0 + M.length * passo; const fechado = t > tFim + 0.25;
    let corpo = top;
    const barra = (s.barra && s.barra.length ? s.barra : null) || (s.barra ? null : claro ? null : ["File", "Edit", "Selection", "View", "Go", "Run", "Terminal", "Help"]); const bx = [];
    if (barra) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = claro ? "#e4e7ee" : "#2a2d3a"; ctx.fillRect(x, top, W, 52 * u); ctx.restore(); let xx = x + 24 * u;
      barra.forEach((b, i) => { const w = tw(ctx, b, font(500, 24 * u)) + 30 * u; const on = s.abre === i && t > tc0 - 0.05 && !fechado;
        if (on) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = claro ? "#cfd6e4" : "#3c4157"; rr(ctx, xx, top + 6 * u, w, 40 * u, 6 * u); ctx.fill(); ctx.restore(); }
        txt(ctx, b, font(500, 24 * u), xx + 15 * u, top + 26 * u, claro ? "#2a2f3a" : (on ? "#fff" : "#c5c9d6"), "left", a); bx.push([xx, w]); xx += w; });
      corpo = top + 52 * u; }
    // corpo do app
    const ch = y + H - corpo; let sideW = 0; let alvoPos = null;
    if (claro) {
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#fff"; ctx.fillRect(x, corpo, W, ch - 2 * u); ctx.fillStyle = "#e4e7ee"; ctx.fillRect(x, corpo, W, 64 * u); ctx.restore();
      pastaIcone(ctx, x + 30 * u, corpo + 16 * u, 38 * u, a); txt(ctx, s.caminho_txt || "Este Computador  ›  Documentos", font(600, 26 * u), x + 84 * u, corpo + 32 * u, "#3a3f4b", "left", a);
      const its = (s.itens || ["Fotos", "Músicas", "Trabalho"]).slice(); const kn = s.resultado === "pasta" ? easeOut((t - tFim - 0.3) / 0.4) : 0; if (kn > 0) its.push({ nome: s.novo || "Nova pasta", novo: true });
      its.forEach((it, i) => { const nome = typeof it === "string" ? it : it.nome; const cx = x + 130 * u + i * 240 * u, cy = corpo + 130 * u; const ka = it.novo ? kn : 1;
        if (it.novo) { ctx.save(); ctx.globalAlpha = a * kn * 0.3; rr(ctx, cx - 95 * u, cy - 16 * u, 190 * u, 210 * u, 14 * u); ctx.fillStyle = C.ac2; ctx.fill(); ctx.restore(); }
        pastaIcone(ctx, cx - 65 * u, cy, 130 * u, a * ka); const nt = it.novo ? nome.slice(0, Math.ceil(clamp((t - tFim - 0.8) / 1.0) * nome.length)) || "Nova pasta" : nome;
        txt(ctx, nt, caber(ctx, nome, it.novo ? 800 : 600, 26 * u, 220 * u), cx, cy + 150 * u, "#2a2f3a", "center", a * ka); });
    } else {
      sideW = s.pastas ? 330 * u : 0;
      if (sideW) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.side; ctx.fillRect(x, corpo, sideW, ch - 2 * u); ctx.restore(); txt(ctx, "EXPLORER", font(700, 20 * u), x + 28 * u, corpo + 34 * u, C.mut, "left", a);
        const ps = s.pastas.slice(); const kn = s.resultado === "arquivo" ? easeOut((t - tFim - 0.3) / 0.3) : 0;
        // novo_pos: onde o arquivo novo entra (os de baixo descem); apaga: nome do item que some depois do clique (os de baixo sobem)
        const arv = arvore(ps, 3); const passoM = Math.min(48, (ch / u - 120) / Math.max(1, arv.length + (s.resultado === "arquivo" ? 1 : 0)));  /* muitos arquivos: linhas mais juntas */ const iNovo = s.novo_pos !== undefined ? s.novo_pos : ps.length; const iApaga = s.apaga ? arv.findIndex((q) => q.nm === s.apaga) : -1; const ka2 = iApaga >= 0 ? easeOut((t - tFim - 0.2) / 0.35) : 0;
        const alvoNm = s.alvo_item || s.apaga;  // botão direito em cima deste item do Explorer (o menu abre ali e o item fica selecionado)
        arv.forEach(({ nm: p, nv }, i) => { const pasta = /\/$/.test(p); if (pasta) p = p.slice(0, -1); const desl = (i >= iNovo ? kn : 0) - (iApaga >= 0 && i > iApaga ? ka2 : 0); const al = a * (i === iApaga ? 1 - ka2 : 1);
          const yy = corpo + (80 + (i + desl) * passoM) * u, ind = nv * 22 * u, arq = !pasta && (/\.\w+$/.test(p) || /^\.\w/.test(p));
          if (al <= 0.01) return;
          if (alvoNm && (p === alvoNm.replace(/\/$/, "") || p.trim() === alvoNm.replace(/\/$/, ""))) { alvoPos = [x + 68 * u + ind + Math.min(tw(ctx, p, font(500, 24 * u)), sideW - 120 * u) * 0.6, yy];
            const ks = easeOut((t - tc0 + 0.1) / 0.2); if (ks > 0) { ctx.save(); ctx.globalAlpha = al * ks; ctx.fillStyle = "#04395e"; ctx.fillRect(x, yy - 22 * u, sideW, 44 * u); ctx.strokeStyle = "#007fd4"; ctx.lineWidth = 2 * u; ctx.strokeRect(x + 1 * u, yy - 22 * u, sideW - 2 * u, 44 * u); ctx.restore(); } }
          if (arq) { ctx.save(); ctx.globalAlpha *= al; ctx.fillStyle = C.ac; rr(ctx, x + 32 * u + ind, yy - 13 * u, 20 * u, 26 * u, 4 * u); ctx.fill(); ctx.restore(); } else pastaIcone(ctx, x + 28 * u + ind, yy - 14 * u, 30 * u, al);
          txt(ctx, p, caber(ctx, p, 500, 24 * u, sideW - 88 * u - ind), x + 68 * u + ind, yy, C.txt, "left", al); });
        if (kn > 0) { const i = iNovo, yy = corpo + (80 + i * passoM) * u, ind = (s.novo_nivel !== undefined ? s.novo_nivel : arv.some((q) => q.nv !== Math.min(arv.indexOf(q), 3)) ? arv[arv.length - 1].nv : Math.min(i, 3)) * 22 * u; const nm = (s.novo || "novo.js").slice(0, Math.ceil(clamp((t - tFim - 0.6) / 1.0) * (s.novo || "novo.js").length));
          ctx.save(); ctx.globalAlpha = a * kn; ctx.strokeStyle = C.ac2; ctx.lineWidth = 2 * u; ctx.strokeRect(x + 60 * u + ind, yy - 20 * u, sideW - 80 * u - ind, 40 * u); if (!s.novo_pasta) { ctx.fillStyle = C.ac; rr(ctx, x + 32 * u + ind, yy - 13 * u, 20 * u, 26 * u, 4 * u); ctx.fill(); } ctx.restore(); if (s.novo_pasta) pastaIcone(ctx, x + 28 * u + ind, yy - 14 * u, 30 * u, a * kn);
          txt(ctx, nm, caber(ctx, s.novo || "novo.js", 600, 24 * u, sideW - 88 * u - ind), x + 68 * u + ind, yy, C.txt, "left", a * kn); } }
      txt(ctx, s.fundo_txt || "", font(700, 40 * u), x + sideW + (W - sideW) / 2, corpo + ch * 0.4, "#3a3f50", "center", a);
      if (s.resultado === "terminal") { const k = easeOut((t - tFim - 0.3) / 0.5); if (k > 0) { const th = 250 * u * k, ty = y + H - th - 2 * u;
        ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = C.term; ctx.fillRect(x + sideW, ty, W - sideW, th); ctx.fillStyle = C.line; ctx.fillRect(x + sideW, ty, W - sideW, 2 * u);
        ctx.beginPath(); ctx.rect(x + sideW, ty, W - sideW, th); ctx.clip();
        ["PROBLEMS", "OUTPUT", "TERMINAL"].forEach((n, i) => txt(ctx, n, font(700, 20 * u), x + sideW + 30 * u + i * 160 * u, ty + 30 * u, i === 2 ? C.txt : C.mut, "left", 1));
        ctx.fillStyle = C.ac2; ctx.fillRect(x + sideW + 30 * u + 320 * u, ty + 46 * u, tw(ctx, "TERMINAL", font(700, 20 * u)), 3 * u);
        const pr = s.prompt || "PS C:\\Users\\voce\\Documents\\" + ((s.pastas && s.pastas[0]) || "meu-primeiro-teste").trim() + "> "; txt(ctx, pr, font(600, 26 * u, MONO), x + sideW + 30 * u, ty + 100 * u, C.ac2, "left", 1);
        if (Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = C.txt; ctx.fillRect(x + sideW + 34 * u + tw(ctx, pr, font(600, 26 * u, MONO)), ty + 86 * u, 14 * u, 28 * u); }
        ctx.restore();
        ctx.save(); ctx.globalAlpha = k; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, x + sideW + 8 * u, ty + 6 * u, W - sideW - 16 * u, th - 12 * u, 12 * u); ctx.stroke(); ctx.restore(); } }
    }
    // menus
    const mf = font(500, 25 * u), ih = 48 * u; const pts = [];
    let mx, my, pmx = 0;
    if (barra && s.abre !== undefined) { mx = bx[s.abre][0]; my = corpo; pts.push([bx[s.abre][0] + bx[s.abre][1] / 2, top + 26 * u, tc0]); }
    else if (alvoPos) { [mx, my] = alvoPos; pts.push([mx, my, tc0, "#69a7ff"]); mx = x + sideW + 12 * u; my -= 20 * u; }  // o menu abre ao lado do Explorer, sem tampar os nomes
    else { const pp = s.ponto || [0.6, 0.55]; mx = x + sideW + pp[0] * (W - sideW); my = corpo + pp[1] * ch; pts.push([mx, my, tc0, "#69a7ff"]); mx += 6 * u; my += 6 * u; }
    M.forEach((itens, k) => {
      const tk = tc0 + k * passo; if (t < tk) return; const ka = fechado ? 0 : easeOut((t - tk - 0.05) / 0.15);
      const mw = Math.max(300 * u, ...itens.map((n) => tw(ctx, n, mf) + 110 * u)); const mh = itens.reduce((q, n) => q + (n === "—" ? 14 * u : ih), 0) + 16 * u;
      if (my + mh > y + H - 10 * u) my = y + H - 10 * u - mh;
      if (mx + mw > x + W - 10 * u) mx = k ? pmx - mw + 6 * u : x + W - 10 * u - mw;
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
      if (prox) { pmx = mx; [mx, my] = prox; }
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
  // GITHUB (desenhado, tema escuro): tela:"novo" (criar repositório) ou "repo" (projeto publicado)
  // {type:"github", tela:"novo"|"repo", usuario:"voce", repo:"meu-primeiro-teste", arquivos:[...], legenda:"..."}
  S.github = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1500 * u, H = 720 * u; const x = c.cx - W / 2, y = topo(c, H);
    const G = { bg: "#0d1117", hd: "#010409", bd: "#30363d", tx: "#e6edf3", mu: "#7d8590", ok: "#238636", ln: "#4493f8", inp: "#0d1117" };
    const us = s.usuario || "voce", rp = s.repo || "meu-primeiro-teste"; const novo = s.tela === "novo";
    const modo = s.tela || "repo"; const url = novo ? "github.com/new" : modo === "signup" ? "github.com/signup" : `github.com/${us}/${rp}`;
    const top = janela(ctx, x, y, W, H, u, "", a, G.bg);
    // barra de endereço
    const ab = [x + 160 * u, y + 14 * u, W - 320 * u, 38 * u]; ctx.save(); ctx.globalAlpha = a; rr(ctx, ...ab, 19 * u); ctx.fillStyle = "#1b1f27"; ctx.fill(); ctx.restore();
    const kU = modo === "repo" ? easeOut((t - (s.url_em || dur * 0.62)) / 0.35) : 0;
    txt(ctx, "🔒 " + url, font(600, 22 * u), ab[0] + 24 * u, ab[1] + 19 * u, kU > 0 ? C.yel : C.mut, "left", a);
    if (kU > 0) { ctx.save(); ctx.globalAlpha = kU; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, ab[0] - 6 * u, ab[1] - 6 * u, tw(ctx, "🔒 " + url, font(600, 22 * u)) + 60 * u, ab[3] + 12 * u, 22 * u); ctx.stroke(); ctx.restore(); }
    // cabeçalho do GitHub
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = G.hd; ctx.fillRect(x, top, W, 70 * u); ctx.fillStyle = G.bd; ctx.fillRect(x, top + 70 * u, W, 1.5 * u); ctx.restore();
    ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(x + 50 * u, top + 35 * u, 18 * u, 0, 7); ctx.fillStyle = G.tx; ctx.fill(); ctx.restore();
    txt(ctx, novo ? "New repository" : modo === "signup" ? "Sign up" : `${us} / ${rp}`, font(700, 24 * u), x + 84 * u, top + 35 * u, G.tx, "left", a);
    const plus = [x + W - 150 * u, top + 35 * u]; ctx.save(); ctx.globalAlpha = a; rr(ctx, plus[0] - 26 * u, plus[1] - 18 * u, 52 * u, 36 * u, 8 * u); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
    txt(ctx, "+ ▾", font(700, 22 * u), plus[0], plus[1], G.tx, "center", a);
    ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(x + W - 70 * u, top + 35 * u, 18 * u, 0, 7); ctx.fillStyle = "#6e40c9"; ctx.fill(); ctx.restore();
    const body = top + 72 * u; const pts = [];
    if (novo) {
      const dir = !!s.direto; const tc0 = dir ? -9 : (s.clique_em || 1.0); const tcN = dir ? -8 : tc0 + 1.1; const tCr = s.criar_em || Math.min(dur - 0.8, (dir ? 1 : tcN) + 4.2); const kF = dir ? 1 : easeOut((t - tcN - 0.2) / 0.35);
      if (!dir) pts.push([plus[0], plus[1], tc0]);
      if (dir) {} else if (t > tc0 && t < tcN + 0.25) { const mx = plus[0] - 240 * u, my = plus[1] + 26 * u; const its = ["New repository", "Import repository", "New codespace", "New gist"];
        ctx.save(); ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 20 * u; rr(ctx, mx, my, 270 * u, its.length * 46 * u + 12 * u, 10 * u); ctx.fillStyle = "#161b22"; ctx.fill(); ctx.shadowColor = "transparent"; ctx.strokeStyle = G.bd; ctx.lineWidth = 1.5 * u; ctx.stroke(); ctx.restore();
        its.forEach((n, i) => { const yy = my + 6 * u + i * 46 * u; if (!i && t > tcN - 0.5) { ctx.save(); ctx.fillStyle = "#1f6feb"; rr(ctx, mx + 6 * u, yy + 2 * u, 258 * u, 42 * u, 6 * u); ctx.fill(); ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; ctx.stroke(); ctx.restore(); }
          txt(ctx, n, font(i ? 500 : 700, 23 * u), mx + 22 * u, yy + 23 * u, G.tx, "left", 1); });
        pts.push([mx + 120 * u, my + 30 * u, tcN]); }
      else pts.push([plus[0] - 120 * u, plus[1] + 56 * u, tcN]);
      if (kF > 0) {
        const fx = x + 200 * u; let yy = body + 46 * u;
        txt(ctx, "Create a new repository", font(800, 34 * u), fx, yy, G.tx, "left", a * kF); yy += 36 * u;
        txt(ctx, "A repository contains all project files, including the revision history.", font(500, 20 * u), fx, yy, G.mu, "left", a * kF); yy += 26 * u;
        ctx.save(); ctx.globalAlpha = a * kF; ctx.fillStyle = G.bd; ctx.fillRect(fx, yy, W - 400 * u, 1.5 * u); ctx.restore(); yy += 36 * u;
        txt(ctx, "Owner *", font(700, 22 * u), fx, yy, G.tx, "left", a * kF); txt(ctx, "Repository name *", font(700, 22 * u), fx + 250 * u, yy, G.tx, "left", a * kF); yy += 44 * u;
        ctx.save(); ctx.globalAlpha = a * kF; rr(ctx, fx, yy - 24 * u, 200 * u, 48 * u, 8 * u); ctx.fillStyle = "#161b22"; ctx.fill(); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke();
        const tN = dir ? (s.nome_em || 0.8) : tcN + 0.9; const kN = clamp((t - tN) / 1.4); const foco = t > tN - 0.3;
        rr(ctx, fx + 250 * u, yy - 24 * u, 460 * u, 48 * u, 8 * u); ctx.fillStyle = G.inp; ctx.fill(); ctx.strokeStyle = foco ? "#1f6feb" : G.bd; ctx.lineWidth = (foco ? 3 : 2) * u; ctx.stroke(); ctx.restore();
        txt(ctx, "👤 " + us + " ▾", font(600, 22 * u), fx + 18 * u, yy, G.tx, "left", a * kF); txt(ctx, "/", font(700, 30 * u), fx + 225 * u, yy, G.mu, "center", a * kF);
        const nm = rp.slice(0, Math.ceil(kN * rp.length)); txt(ctx, nm, font(600, 24 * u), fx + 268 * u, yy, G.tx, "left", a * kF);
        if (kN > 0 && kN < 1 && Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = G.tx; ctx.fillRect(fx + 270 * u + tw(ctx, nm, font(600, 24 * u)), yy - 14 * u, 3 * u, 28 * u); }
        if (kN >= 1) txt(ctx, `✓ ${rp} is available.`, font(700, 21 * u), fx + 730 * u, yy, "#3fb950", "left", a * easeOut((t - tN - 1.5) / 0.3));
        pts.push([fx + 470 * u, yy + 4 * u, tN - 0.2]); yy += 56 * u;
        // descrição (opcional)
        const yDesc = yy; txt(ctx, "Description (optional)", font(700, 21 * u), fx, yy, G.tx, "left", a * kF); yy += 42 * u;
        ctx.save(); ctx.globalAlpha = a * kF; rr(ctx, fx, yy - 20 * u, 710 * u, 40 * u, 8 * u); ctx.fillStyle = G.inp; ctx.fill(); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
        const kD = s.desc_em ? easeOut((t - s.desc_em) / 0.3) : 0; if (kD > 0) { ctx.save(); ctx.globalAlpha = kD; ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; rr(ctx, fx - 7 * u, yy - 27 * u, 724 * u, 54 * u, 10 * u); ctx.stroke(); ctx.restore(); txt(ctx, global.CO_IDIOMA === "en" ? "optional: you can leave it empty" : "opcional: pode deixar vazio", font(800, 20 * u), fx + 18 * u, yy, C.yel, "left", kD); }
        yy += 64 * u;
        [["Public", "Anyone on the internet can see this repository.", true], ["Private", "You choose who can see and commit.", false]].forEach(([n, d, on]) => {
          ctx.save(); ctx.globalAlpha = a * kF; ctx.beginPath(); ctx.arc(fx + 14 * u, yy, 12 * u, 0, 7); ctx.strokeStyle = on ? "#1f6feb" : G.mu; ctx.lineWidth = (on ? 7 : 2) * u; ctx.stroke(); ctx.restore();
          txt(ctx, n, font(700, 23 * u), fx + 44 * u, yy - 10 * u, G.tx, "left", a * kF); txt(ctx, d, font(500, 19 * u), fx + 44 * u, yy + 16 * u, G.mu, "left", a * kF); yy += 58 * u; });
        // opções de baixo: README, .gitignore e licença (deixar tudo desmarcado)
        { const ox = fx + 800 * u, oy = yDesc + 4 * u, ow = 470 * u, oh = 150 * u; const kO = s.opcoes_em ? easeOut((t - s.opcoes_em) / 0.3) : 0;
          txt(ctx, "Initialize this repository with:", font(700, 20 * u), ox, oy, G.tx, "left", a * kF);
          ctx.save(); ctx.globalAlpha = a * kF; rr(ctx, ox, oy + 22 * u, 22 * u, 22 * u, 4 * u); ctx.strokeStyle = G.mu; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
          txt(ctx, "Add a README file", font(600, 20 * u), ox + 34 * u, oy + 33 * u, G.tx, "left", a * kF);
          [["Add .gitignore", ".gitignore template: None"], ["Choose a license", "License: None"]].forEach(([r, v], i) => { const ry = oy + 74 * u + i * 44 * u;
            txt(ctx, r, font(700, 19 * u), ox, ry, G.tx, "left", a * kF); ctx.save(); ctx.globalAlpha = a * kF; rr(ctx, ox + 170 * u, ry - 17 * u, 280 * u, 34 * u, 6 * u); ctx.fillStyle = "#21262d"; ctx.fill(); ctx.restore();
            txt(ctx, v + " ▾", font(600, 18 * u), ox + 182 * u, ry, G.tx, "left", a * kF); });
          if (kO > 0) { ctx.save(); ctx.globalAlpha = kO; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, ox - 14 * u, oy - 22 * u, ow + 10 * u, oh + 18 * u, 12 * u); ctx.stroke(); ctx.restore();
            txt(ctx, global.CO_IDIOMA === "en" ? "leave everything unchecked" : "deixe tudo desmarcado", font(800, 21 * u), ox, oy + oh + 14 * u, C.yel, "left", kO); } }
        const bw = 250 * u, bx = fx, by = yy - 10 * u; const kb = easeOut((t - tCr) / 0.2);
        ctx.save(); ctx.globalAlpha = a * kF; rr(ctx, bx, by, bw, 54 * u, 8 * u); ctx.fillStyle = kb > 0.5 ? "#2ea043" : G.ok; ctx.fill(); ctx.restore();
        txt(ctx, "Create repository", font(700, 23 * u), bx + bw / 2, by + 27 * u, "#fff", "center", a * kF);
        if (t > tCr - 0.6) { ctx.save(); ctx.globalAlpha = easeOut((t - tCr + 0.6) / 0.3); ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, bx - 8 * u, by - 8 * u, bw + 16 * u, 70 * u, 12 * u); ctx.stroke(); ctx.restore(); }
        pts.push([bx + bw * 0.55, by + 30 * u, tCr]);
      }
    } else if (modo === "secrets") {  // Settings › Secrets and variables › Actions: os segredos do repositório
      let yy = body + 28 * u; const fx = x + 60 * u;
      let tx0 = fx; ["<> Code", "Issues", "Pull requests", "Actions", "Settings"].forEach((n, i) => { const on = n === "Settings"; txt(ctx, n, font(on ? 700 : 500, 22 * u), tx0, yy, on ? G.tx : G.mu, "left", a); const w = tw(ctx, n, font(700, 22 * u));
        if (on) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#f78166"; ctx.fillRect(tx0 - 6 * u, yy + 22 * u, w + 12 * u, 3 * u); ctx.restore(); pts.push([tx0 + w / 2, yy, s.clique_em || 0.8]); } tx0 += w + 50 * u; });
      yy += 60 * u; const sw = 330 * u; const kS = easeOut((t - (s.menu_em || 1.6)) / 0.3);
      ["General", "Collaborators", "Branches", "Actions", "Secrets and variables", "    Actions", "    Codespaces", "Pages"].forEach((n, i) => { const sel = i === 5; const yi = yy + i * 46 * u;
        if (sel && kS > 0) { ctx.save(); ctx.globalAlpha = a * kS; ctx.fillStyle = "#1f2937"; rr(ctx, fx - 10 * u, yi - 20 * u, sw, 40 * u, 6 * u); ctx.fill(); ctx.fillStyle = "#1f6feb"; ctx.fillRect(fx - 10 * u, yi - 20 * u, 4 * u, 40 * u); ctx.restore(); pts.push([fx + 120 * u, yi, (s.menu_em || 1.6) - 0.1]); }
        txt(ctx, n.trim(), font(sel || i === 4 ? 700 : 500, 21 * u), fx + (n.startsWith(" ") ? 30 * u : 0), yi, G.tx, "left", a); });
      const mx = fx + sw + 40 * u, mw = x + W - 60 * u - mx; let my = yy - 6 * u;
      txt(ctx, "Actions secrets and variables", font(800, 30 * u), mx, my, G.tx, "left", a * kS); my += 50 * u;
      txt(ctx, "Secrets are encrypted and are used for sensitive data.", font(500, 20 * u), mx, my, G.mu, "left", a * kS); my += 54 * u;
      const tB = s.botao_em || 2.6; const bw = 290 * u; ctx.save(); ctx.globalAlpha = a * kS; rr(ctx, mx + mw - bw, my - 26 * u, bw, 50 * u, 8 * u); ctx.fillStyle = G.ok; ctx.fill();
      if (t > tB - 0.5 && t < tB + 1.0) { ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; ctx.stroke(); } ctx.restore(); txt(ctx, "New repository secret", font(700, 21 * u), mx + mw - bw / 2, my, "#fff", "center", a * kS);
      pts.push([mx + mw - bw / 2, my + 4 * u, tB]);
      txt(ctx, "Repository secrets", font(800, 24 * u), mx, my, G.tx, "left", a * kS); my += 50 * u;
      const sec = s.segredos || ["SAUCE_USER", "SAUCE_PASSWORD"]; const t0 = tB + 1.0; const passoS = Math.max(1.0, (dur * 0.85 - t0) / Math.max(1, sec.length));
      ctx.save(); ctx.globalAlpha = a * kS; rr(ctx, mx, my - 24 * u, mw, 50 * u * (sec.length + 0.2), 8 * u); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
      sec.forEach((nm, i) => { const k = easeOut((t - t0 - i * passoS) / 0.35); if (k <= 0) return; const yi = my + i * 50 * u;
        txt(ctx, "🔒  " + nm, font(700, 22 * u, MONO), mx + 20 * u, yi, G.tx, "left", a * k); txt(ctx, "Updated now", font(500, 19 * u), mx + mw - 120 * u, yi, G.mu, "right", a * k); txt(ctx, "✎  🗑", font(500, 20 * u), mx + mw - 20 * u, yi, G.mu, "right", a * k);
        if (i < sec.length - 1) { ctx.save(); ctx.globalAlpha = a * k; ctx.fillStyle = G.bd; ctx.fillRect(mx, yi + 25 * u, mw, 1.5 * u); ctx.restore(); } });
      if (s.aviso) txt(ctx, s.aviso, font(800, 22 * u), mx, my + sec.length * 50 * u + 30 * u, C.yel, "left", a * easeOut((t - t0 - sec.length * passoS) / 0.4));
    } else if (modo === "signup") {
      const fx = c.cx - 330 * u; let yy = body + 70 * u;
      txt(ctx, "Welcome to GitHub!", font(800, 38 * u), fx, yy, G.tx, "left", a); yy += 40 * u;
      txt(ctx, "Let's begin the adventure", font(500, 22 * u), fx, yy, "#3fb950", "left", a); yy += 60 * u;
      const campos = s.campos || [["Email", "voce@email.com"], ["Password", "••••••••••"], ["Username", us]]; const t0 = s.digita_em || 1.0;
      campos.forEach(([rot, val], i) => { const ti = t0 + i * 1.5; const k = clamp((t - ti) / 1.0); const v = val.slice(0, Math.ceil(k * val.length));
        txt(ctx, rot + " *", font(700, 22 * u), fx, yy, G.tx, "left", a); yy += 36 * u;
        ctx.save(); ctx.globalAlpha = a; rr(ctx, fx, yy - 22 * u, 660 * u, 46 * u, 8 * u); ctx.fillStyle = G.inp; ctx.fill(); ctx.strokeStyle = t > ti - 0.2 && t < ti + 1.3 ? "#1f6feb" : G.bd; ctx.lineWidth = 2.5 * u; ctx.stroke(); ctx.restore();
        txt(ctx, v, font(600, 22 * u), fx + 16 * u, yy, G.tx, "left", a); if (k > 0 && k < 1) pts.push([fx + 330 * u, yy + 6 * u, ti - 0.1]);
        if (rot === "Username" && k >= 1) txt(ctx, "← " + (global.CO_IDIOMA === "en" ? "goes in your link" : "vai no seu link"), font(800, 22 * u), fx + 680 * u, yy, C.yel, "left", a * easeOut((t - ti - 1.1) / 0.3));
        yy += 62 * u; });
      const tB = t0 + campos.length * 1.5 + 0.6; const bw = 660 * u, by = yy - 6 * u; const kb = easeOut((t - tB) / 0.2);
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx, by, bw, 52 * u, 8 * u); ctx.fillStyle = kb > 0.5 ? "#2ea043" : G.ok; ctx.fill(); if (t > tB - 0.6) { ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; ctx.stroke(); } ctx.restore();
      txt(ctx, "Continue ›", font(700, 23 * u), fx + bw / 2, by + 26 * u, "#fff", "center", a); pts.push([fx + bw * 0.55, by + 30 * u, tB]);
    } else if (modo === "setup") {
      const fx = x + 70 * u, fw = W - 140 * u; let yy = body + 50 * u; const gitUrl = `https://github.com/${us}/${rp}.git`;
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx, yy - 20 * u, fw, 150 * u, 10 * u); ctx.fillStyle = "#0d2a4a"; ctx.fill(); ctx.strokeStyle = "#1f6feb"; ctx.lineWidth = 1.5 * u; ctx.stroke(); ctx.restore();
      txt(ctx, "Quick setup — if you've done this kind of thing before", font(700, 23 * u), fx + 24 * u, yy + 12 * u, G.tx, "left", a);
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx + 24 * u, yy + 44 * u, 110 * u, 44 * u, 6 * u); ctx.fillStyle = "#21262d"; ctx.fill(); ctx.restore(); txt(ctx, "HTTPS", font(700, 20 * u), fx + 79 * u, yy + 66 * u, G.tx, "center", a);
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx + 146 * u, yy + 44 * u, fw - 240 * u, 44 * u, 6 * u); ctx.fillStyle = G.bg; ctx.fill(); ctx.strokeStyle = G.bd; ctx.stroke(); ctx.restore();
      txt(ctx, gitUrl, font(600, 21 * u, MONO), fx + 162 * u, yy + 66 * u, G.tx, "left", a); txt(ctx, "⧉", font(700, 26 * u), fx + fw - 60 * u, yy + 66 * u, G.mu, "center", a);
      const k1 = easeOut((t - (s.url_em || 1.2)) / 0.3); if (k1 > 0) { ctx.save(); ctx.globalAlpha = k1; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, fx + 138 * u, yy + 36 * u, fw - 224 * u, 60 * u, 10 * u); ctx.stroke(); ctx.restore();
        txt(ctx, global.CO_IDIOMA === "en" ? "your repository's address" : "o endereço do seu repositório", font(800, 22 * u), fx + 146 * u, yy + 116 * u, C.yel, "left", k1); }
      yy += 190 * u;
      txt(ctx, "…or push an existing repository from the command line", font(800, 26 * u), fx, yy, G.tx, "left", a); yy += 30 * u;
      const cmds = [`git remote add origin ${gitUrl}`, "git branch -M main", "git push -u origin main"];
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx, yy, fw, 150 * u, 10 * u); ctx.fillStyle = "#161b22"; ctx.fill(); ctx.strokeStyle = G.bd; ctx.lineWidth = 1.5 * u; ctx.stroke(); ctx.restore();
      cmds.forEach((cm, i) => txt(ctx, cm, font(600, 23 * u, MONO), fx + 26 * u, yy + 36 * u + i * 40 * u, G.tx, "left", a));
      const cpx = fx + fw - 50 * u, cpy = yy + 36 * u; ctx.save(); ctx.globalAlpha = a; rr(ctx, cpx - 24 * u, cpy - 20 * u, 48 * u, 40 * u, 6 * u); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore(); txt(ctx, "⧉", font(700, 26 * u), cpx, cpy, G.tx, "center", a);
      const k2 = easeOut((t - (s.cmd_em || dur * 0.55)) / 0.3); if (k2 > 0) { ctx.save(); ctx.globalAlpha = k2; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, fx - 8 * u, yy - 8 * u, fw + 16 * u, 166 * u, 12 * u); ctx.stroke(); ctx.restore(); pts.push([cpx, cpy, (s.cmd_em || dur * 0.55) + 0.9]); }
      const kc = easeOut((t - (s.cmd_em || dur * 0.55) - 1.0) / 0.2); if (kc > 0) txt(ctx, global.CO_IDIOMA === "en" ? "Copied!" : "Copiado!", font(800, 22 * u), cpx - 40 * u, cpy, "#3fb950", "right", kc);
    } else if (modo === "readme") {  // o README renderizado na página do repositório, com o selo do GitHub Actions
      let yy = body + 40 * u; const fx = x + 60 * u, fw = W - 120 * u;
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx, yy, fw, y + H - yy - 30 * u, 10 * u); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.fillStyle = "#161b22"; rr(ctx, fx, yy, fw, 52 * u, 10 * u); ctx.fill(); ctx.restore();
      txt(ctx, "📖 README", font(700, 21 * u), fx + 24 * u, yy + 26 * u, G.tx, "left", a); yy += 100 * u;
      const tit = s.titulo_readme || rp; txt(ctx, tit, font(800, 44 * u), fx + 40 * u, yy, G.tx, "left", a);
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = G.bd; ctx.fillRect(fx + 40 * u, yy + 36 * u, fw - 80 * u, 2 * u); ctx.restore(); yy += 80 * u;
      // o selo: "Playwright Tests | passing" (cinza + verde), como o GitHub gera
      const kb = easeOut((t - (s.selo_em !== undefined ? s.selo_em : 0.6)) / 0.4); const e1 = s.selo_nome || "Playwright Tests", e2 = s.selo_status || "passing";
      const fb = font(600, 22 * u), w1 = tw(ctx, e1, fb) + 28 * u, w2 = tw(ctx, e2, fb) + 28 * u, bh = 38 * u, bx = fx + 40 * u, by = yy - bh / 2;
      ctx.save(); ctx.globalAlpha = a * kb; rr(ctx, bx, by, w1 + w2, bh, 6 * u); ctx.clip(); ctx.fillStyle = "#555"; ctx.fillRect(bx, by, w1, bh); ctx.fillStyle = "#3fb950"; ctx.fillRect(bx + w1, by, w2, bh); ctx.restore();
      txt(ctx, e1, fb, bx + w1 / 2, yy, "#fff", "center", a * kb); txt(ctx, e2, fb, bx + w1 + w2 / 2, yy, "#fff", "center", a * kb);
      const kf = easeOut((t - (s.foco_em || dur * 0.45)) / 0.35);
      if (kf > 0) { ctx.save(); ctx.globalAlpha = kf; ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; rr(ctx, bx - 12 * u, by - 12 * u, w1 + w2 + 24 * u, bh + 24 * u, 10 * u); ctx.stroke(); ctx.restore();
        txt(ctx, s.foco_rotulo || "← verde: os testes estão passando", font(800, 26 * u), bx + w1 + w2 + 36 * u, yy, C.yel, "left", kf); }
      yy += 70 * u;
      (s.linhas_readme || []).forEach(([tp, tx], i) => { const kl = easeOut((t - 0.9 - i * 0.18) / 0.3) * a; if (yy > y + H - 60 * u) return;
        if (tp === "h") { yy += 10 * u; txt(ctx, tx, font(800, 30 * u), fx + 40 * u, yy, G.tx, "left", kl); yy += 46 * u; }
        else if (tp === "c") { ctx.save(); ctx.globalAlpha = kl; rr(ctx, fx + 40 * u, yy - 22 * u, fw - 80 * u, 44 * u, 8 * u); ctx.fillStyle = "#0d1117"; ctx.fill(); ctx.restore(); txt(ctx, tx, font(600, 22 * u, MONO), fx + 60 * u, yy, G.tx, "left", kl); yy += 54 * u; }
        else { txt(ctx, tx, font(500, 24 * u), fx + 40 * u, yy, G.mu, "left", kl); yy += 40 * u; } });
    } else {
      let yy = body + 50 * u; const fx = x + 60 * u, fw = W - 120 * u;
      let tx0 = fx; ["<> Code", "Issues", "Pull requests", "Actions", "Settings"].forEach((n, i) => { txt(ctx, n, font(i ? 500 : 700, 22 * u), tx0, yy - 22 * u, i ? G.mu : G.tx, "left", a); tx0 += tw(ctx, n, font(700, 22 * u)) + 50 * u;
        if (!i) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#f78166"; ctx.fillRect(fx - 6 * u, yy, 110 * u, 3 * u); ctx.restore(); } });
      yy += 50 * u;
      txt(ctx, rp, font(800, 32 * u), fx, yy, G.tx, "left", a); const rw = tw(ctx, rp, font(800, 32 * u));
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx + rw + 18 * u, yy - 16 * u, 90 * u, 32 * u, 16 * u); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore(); txt(ctx, "Public", font(600, 18 * u), fx + rw + 63 * u, yy, G.mu, "center", a);
      yy += 50 * u;
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx, yy - 22 * u, 140 * u, 44 * u, 8 * u); ctx.fillStyle = "#21262d"; ctx.fill(); rr(ctx, fx + fw - 150 * u, yy - 22 * u, 150 * u, 44 * u, 8 * u); ctx.fillStyle = G.ok; ctx.fill(); ctx.restore();
      txt(ctx, "⑂ main ▾", font(600, 21 * u), fx + 70 * u, yy, G.tx, "center", a); txt(ctx, "<> Code ▾", font(700, 21 * u), fx + fw - 75 * u, yy, "#fff", "center", a);
      yy += 44 * u; const arqs = s.arquivos || [["cypress", true, "meu primeiro teste automatizado"], [".gitignore", false, "meu primeiro teste automatizado"], ["cypress.config.js", false, "meu primeiro teste automatizado"], ["package-lock.json", false, "meu primeiro teste automatizado"], ["package.json", false, "meu primeiro teste automatizado"]];
      const rh = Math.min(50 * u, (y + H - yy - 20 * u) / (arqs.length + 1)); const th = rh * (arqs.length + 1);  /* muitos arquivos: linhas mais baixas, a tabela cabe na janela */
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx, yy, fw, th, 10 * u); ctx.strokeStyle = G.bd; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.fillStyle = "#161b22"; rr(ctx, fx, yy, fw, rh, 10 * u); ctx.fill(); ctx.restore();
      ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); ctx.arc(fx + 34 * u, yy + rh / 2, 13 * u, 0, 7); ctx.fillStyle = "#6e40c9"; ctx.fill(); ctx.restore();
      txt(ctx, us, font(700, 21 * u), fx + 60 * u, yy + rh / 2, G.tx, "left", a); txt(ctx, s.commit || "meu primeiro teste automatizado", font(500, 21 * u), fx + 70 * u + tw(ctx, us, font(700, 21 * u)), yy + rh / 2, G.mu, "left", a);
      txt(ctx, "🕓 1 Commit", font(600, 20 * u), fx + fw - 24 * u, yy + rh / 2, G.tx, "right", a);
      const kfoc = easeOut((t - (s.foco_em || dur * 0.35)) / 0.35);
      arqs.forEach(([n, dir, msg], i) => { const ry = yy + rh * (i + 1); const ka = easeOut((t - 0.5 - i * 0.12) / 0.3) * a;
        ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = G.bd; ctx.fillRect(fx, ry, fw, 1.5 * u); ctx.restore();
        if (dir) pastaIcone(ctx, fx + 22 * u, ry + 12 * u, 30 * u, ka, "#7d8590"); else { ctx.save(); ctx.globalAlpha = ka; ctx.strokeStyle = G.mu; ctx.lineWidth = 2 * u; rr(ctx, fx + 27 * u, ry + 13 * u, 20 * u, 25 * u, 3 * u); ctx.stroke(); ctx.restore(); }
        txt(ctx, n, font(500, 22 * u), fx + 70 * u, ry + rh / 2, G.tx, "left", ka); txt(ctx, msg, font(500, 20 * u), fx + fw * 0.42, ry + rh / 2, G.mu, "left", ka);
        txt(ctx, "now", font(500, 20 * u), fx + fw - 24 * u, ry + rh / 2, G.mu, "right", ka);
        if ((s.foco_item !== undefined ? i === s.foco_item : dir) && kfoc > 0) { ctx.save(); ctx.globalAlpha = kfoc * (1 - kU); ctx.strokeStyle = C.yel; ctx.lineWidth = 4 * u; rr(ctx, fx + 6 * u, ry + 4 * u, fw - 12 * u, rh - 8 * u, 8 * u); ctx.stroke(); ctx.restore();
          txt(ctx, s.foco_rotulo || "← seus testes", font(800, 22 * u), fx + 90 * u + tw(ctx, n, font(500, 22 * u)), ry + rh / 2, C.yel, "left", kfoc * (1 - kU)); } });
    }
    rota(ctx, u, pts, t);
    legenda(ctx, c, t, s);
  };
  // INICIAR (menu Iniciar do Windows): aperta a tecla Windows, digita o nome do app e abre
  // {type:"iniciar", busca:"PowerShell", app:"Windows PowerShell", tipo:"Aplicativo", legenda:"..."}
  S.iniciar = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1500 * u, H = 720 * u; const x = c.cx - W / 2, y = topo(c, H);
    // "área de trabalho"
    ctx.save(); ctx.globalAlpha = a; rr(ctx, x, y, W, H, 22 * u); ctx.clip();
    const g = ctx.createLinearGradient(x, y, x + W, y + H); g.addColorStop(0, "#0b3a6e"); g.addColorStop(1, "#1d6fb8"); ctx.fillStyle = g; ctx.fillRect(x, y, W, H);
    const tbH = 64 * u; ctx.fillStyle = "rgba(20,24,32,.92)"; ctx.fillRect(x, y + H - tbH, W, tbH);
    const tk = s.tecla_em || 0.8; const ko = easeOut((t - tk - 0.15) / 0.35); const tb = c.cx;
    // botão Iniciar (logo genérico de 4 quadrados)
    const bx = tb - 160 * u, by = y + H - tbH / 2; const pres = t > tk && t < tk + 0.35;
    if (pres || ko > 0) { ctx.fillStyle = "rgba(255,255,255,.12)"; rr(ctx, bx - 26 * u, by - 26 * u, 52 * u, 52 * u, 8 * u); ctx.fill(); }
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([dx, dy]) => { ctx.fillStyle = "#4cc2ff"; ctx.fillRect(bx + (dx < 0 ? -15 : 2) * u, by + (dy < 0 ? -15 : 2) * u, 13 * u, 13 * u); });
    ["#ffd23f", "#3fd68a", "#ff8c42"].forEach((cor, i) => { ctx.fillStyle = cor; rr(ctx, tb - 80 * u + i * 70 * u, by - 18 * u, 36 * u, 36 * u, 8 * u); ctx.fill(); });
    ctx.restore();
    // tecla do teclado aparecendo (dica visual)
    const kk = t > tk - 0.5 && t < tk + 0.9 ? easeOut((t - tk + 0.5) / 0.25) : 0;
    if (kk > 0) { const kx = x + 80 * u, ky = y + 80 * u, ks = 120 * u * (pres ? 0.92 : 1);
      ctx.save(); ctx.globalAlpha = a * kk; ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 20 * u; rr(ctx, kx, ky, ks, ks, 18 * u); ctx.fillStyle = "#f4f5f8"; ctx.fill(); ctx.shadowColor = "transparent";
      ctx.strokeStyle = pres ? C.yel : "#c9ced8"; ctx.lineWidth = 5 * u; ctx.stroke();
      const cx2 = kx + ks / 2, cy2 = ky + ks / 2; [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([dx, dy]) => { ctx.fillStyle = "#1d6fb8"; ctx.fillRect(cx2 + (dx < 0 ? -26 : 3) * u, cy2 + (dy < 0 ? -26 : 3) * u, 23 * u, 23 * u); }); ctx.restore();
      txt(ctx, global.CO_IDIOMA === "en" ? "Windows key" : "tecla Windows", font(800, 30 * u), kx + ks + 24 * u, ky + ks / 2, "#fff", "left", a * kk); }
    // menu Iniciar
    if (ko > 0) {
      const mw = 760 * u, mh = 520 * u, mx = c.cx - mw / 2, my = y + H - tbH - 16 * u - mh * ko;
      ctx.save(); ctx.globalAlpha = a * ko; ctx.beginPath(); ctx.rect(x, y, W, H - tbH); ctx.clip(); ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 40 * u; rr(ctx, mx, my, mw, mh, 16 * u); ctx.fillStyle = "#202634"; ctx.fill(); ctx.shadowColor = "transparent";
      // caixa de busca
      const ty0 = tk + 0.7; const busca = s.busca || "PowerShell"; const kt = clamp((t - ty0) / Math.max(0.6, busca.length * 0.08)); const tx2 = busca.slice(0, Math.ceil(kt * busca.length));
      rr(ctx, mx + 30 * u, my + 30 * u, mw - 60 * u, 64 * u, 32 * u); ctx.fillStyle = "#2c3446"; ctx.fill(); ctx.strokeStyle = kt > 0 ? "#4cc2ff" : "#3a4458"; ctx.lineWidth = 3 * u; ctx.stroke();
      txt(ctx, "⌕", font(700, 30 * u), mx + 62 * u, my + 62 * u, "#aab3c5", "center", 1);
      txt(ctx, tx2 || (global.CO_IDIOMA === "en" ? "Search for apps, settings and documents" : "Pesquisar aplicativos, configurações e documentos"), font(kt > 0 ? 700 : 500, 26 * u), mx + 90 * u, my + 62 * u, kt > 0 ? "#fff" : "#8a93a6", "left", 1);
      if (kt > 0 && kt < 1 && Math.floor(t * 2.5) % 2 === 0) { ctx.fillStyle = "#fff"; ctx.fillRect(mx + 92 * u + tw(ctx, tx2, font(700, 26 * u)), my + 46 * u, 3 * u, 32 * u); }
      // resultado
      const kr = easeOut((t - ty0 - Math.max(0.6, busca.length * 0.08) - 0.1) / 0.3);
      if (kr > 0) {
        txt(ctx, global.CO_IDIOMA === "en" ? "Best match" : "Melhor correspondência", font(700, 22 * u), mx + 40 * u, my + 136 * u, "#aab3c5", "left", kr);
        const ry = my + 160 * u, rh = 120 * u; const tc = s.clique_em || Math.min(dur - 0.8, ty0 + 2.6);
        ctx.globalAlpha = a * ko * kr; rr(ctx, mx + 30 * u, ry, mw - 60 * u, rh, 12 * u); ctx.fillStyle = "#2f3a52"; ctx.fill();
        if (t > tc - 0.6) { ctx.strokeStyle = C.yel; ctx.lineWidth = 5 * u; ctx.stroke(); }
        rr(ctx, mx + 52 * u, ry + 22 * u, 76 * u, 76 * u, 12 * u); ctx.fillStyle = "#012456"; ctx.fill(); txt(ctx, ">_", font(800, 32 * u, MONO), mx + 90 * u, ry + 60 * u, "#fff", "center", 1);
        txt(ctx, s.app || "Windows PowerShell", font(800, 32 * u), mx + 150 * u, ry + 46 * u, "#fff", "left", 1);
        txt(ctx, s.tipo || (global.CO_IDIOMA === "en" ? "App" : "Aplicativo"), font(500, 24 * u), mx + 150 * u, ry + 84 * u, "#aab3c5", "left", 1);
        ctx.globalAlpha = a * ko;
        ctx.restore(); rota(ctx, u, [[mx + 260 * u, ry + rh / 2, tc]], t); ctx.save();
      }
      ctx.restore();
    }
    legenda(ctx, c, t, s);
  };

  // ================= PLAYWRIGHT =================
  const PW = { bg: "#1e1e1e", pan: "#252526", bd: "#3c3c3c", tx: "#cccccc", mut: "#8b8b8b", sel: "#04395e", ok: "#3fb950", bad: "#f85149", run: "#d29922", blue: "#4fc1ff" };
  // bolinha de status: ok / falhou / rodando / espera
  function pwStatus(ctx, u, x, y, st, t, a) {
    ctx.save(); ctx.globalAlpha *= a; const r = 11 * u;
    if (st === "ok") { ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fillStyle = PW.ok; ctx.fill(); ctx.strokeStyle = "#0d1117"; ctx.lineWidth = 3 * u; ctx.beginPath(); ctx.moveTo(x - 5 * u, y); ctx.lineTo(x - 1 * u, y + 4 * u); ctx.lineTo(x + 6 * u, y - 4 * u); ctx.stroke(); }
    else if (st === "falhou") { ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fillStyle = PW.bad; ctx.fill(); ctx.strokeStyle = "#0d1117"; ctx.lineWidth = 3 * u; ctx.beginPath(); ctx.moveTo(x - 4 * u, y - 4 * u); ctx.lineTo(x + 4 * u, y + 4 * u); ctx.moveTo(x + 4 * u, y - 4 * u); ctx.lineTo(x - 4 * u, y + 4 * u); ctx.stroke(); }
    else if (st === "rodando") { ctx.strokeStyle = PW.run; ctx.lineWidth = 3.5 * u; ctx.beginPath(); ctx.arc(x, y, r - 1 * u, t * 7, t * 7 + 4.4); ctx.stroke(); }
    else { ctx.strokeStyle = "#6e7681"; ctx.lineWidth = 2.5 * u; ctx.beginPath(); ctx.arc(x, y, r - 2 * u, 0, 7); ctx.stroke(); }
    ctx.restore();
  }
  function pwPlay(ctx, u, x, y, a, cor = PW.tx) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = cor; ctx.beginPath(); ctx.moveTo(x - 6 * u, y - 8 * u); ctx.lineTo(x + 8 * u, y); ctx.lineTo(x - 6 * u, y + 8 * u); ctx.closePath(); ctx.fill(); ctx.restore(); }
  function corta(ctx, t, f, max) { if (tw(ctx, t, f) <= max) return t; let s = t; while (s.length > 3 && tw(ctx, s + "…", f) > max) s = s.slice(0, -1); return s + "…"; }
  // linha de tempo das ações: devolve quantas já rodaram (fração) e o instante do fim
  function pwTempo(s, dur, n) { const t0 = s.roda_em === undefined ? 1.0 : s.roda_em; const passo = s.passo || Math.max(0.35, Math.min(0.9, (dur * 0.62 - t0) / Math.max(n, 1))); return { t0, passo, fim: t0 + n * passo }; }
  // snapshot do site com faixa de miniaturas (filmstrip) e realce do elemento
  function pwSnapshot(ctx, c, t, s, media, x, y, w, h, a, kFeito, claro) {
    if (s.depois && t > s.depois.em) s = Object.assign({}, s, { media: s.depois.media || s.media, aba_snapshot: 2, elem: s.depois.elem || s.elem });  // troca pra aba After
    const u = c.u; const m = media && media[s.media]; const el = m && (m.video || m.img);
    const fh = 84 * u; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = claro ? "#f3f3f3" : "#1b1b1b"; ctx.fillRect(x, y, w, fh); ctx.restore();
    const nT = 7, tw0 = (w - 40 * u) / nT;
    for (let i = 0; i < nT; i++) { const ki = clamp(kFeito * nT - i); if (ki <= 0) continue; const tx = x + 20 * u + i * tw0;
      ctx.save(); ctx.globalAlpha = a * ki; rr(ctx, tx + 4 * u, y + 12 * u, tw0 - 8 * u, fh - 24 * u, 4 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.clip(); if (el) { const iw = el.videoWidth || el.width, ih = el.videoHeight || el.height; ctx.drawImage(el, tx + 4 * u, y + 12 * u, tw0 - 8 * u, (tw0 - 8 * u) * ih / iw); } ctx.restore(); }
    // abas Action / Before / After
    const ty = y + fh; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = claro ? "#fafafa" : PW.pan; ctx.fillRect(x, ty, w, 52 * u); ctx.restore();
    ["Action", "Before", "After"].forEach((n, i) => { const on = i === (s.aba_snapshot || 0); const xx = x + 30 * u + i * 130 * u;
      txt(ctx, n, font(on ? 700 : 500, 22 * u), xx, ty + 26 * u, on ? (claro ? "#111" : "#fff") : PW.mut, "left", a); if (on) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.blue; ctx.fillRect(xx, ty + 46 * u, tw(ctx, n, font(700, 22 * u)), 4 * u); ctx.restore(); } });
    const sy = ty + 52 * u, sh = y + h - sy; const e = s.elem; const foco = e ? [(e[0] + e[2]) / 2, (e[1] + e[3]) / 2] : [0.5, 0.3];
    const p = print(ctx, el, x, sy, w, sh, a, "#fff", foco, s.zoom_site || 1.6);
    if (!el) txt(ctx, s.url || "site", font(700, 30 * u), x + w / 2, sy + sh / 2, C.mut, "center", a);
    return p;
  }

  // UI MODE: {type:"pw_ui", media:"site_sauce", url:"https://www.saucedemo.com", inspecionar:"#user-name",
  //   arquivos:[["login.spec.js", ["entra com usuário e senha", ["mostra erro", "ok"]]]], roda:0, status:"ok"|"falhou",
  //   acoes:[["Navigate to", "/"], ["Fill", "getByTestId('username')"]], projeto:"chromium", legenda:"..."}
  S.pw_ui = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1720 * u, H = 760 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "Playwright Test", a, PW.bg);
    const LW = 470 * u, MW = 430 * u; const A = s.passos_pw || (s.acoes || []).filter(Array.isArray); const tm = pwTempo(s, dur, A.length);
    const feitos = s.pronto ? A.length : clamp((t - tm.t0) / tm.passo, 0, A.length); const fim = s.pronto || t >= tm.fim; const falha = s.status === "falhou";
    // painel de testes
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.pan; ctx.fillRect(x, top, LW, y + H - top); ctx.fillStyle = PW.bd; ctx.fillRect(x + LW, top, 2 * u, y + H - top); ctx.restore();
    txt(ctx, "TESTS", font(800, 20 * u), x + 24 * u, top + 34 * u, PW.mut, "left", a);
    const btnRun = [x + LW - 44 * u, top + 34 * u]; pwPlay(ctx, u, btnRun[0], btnRun[1], a, t > tm.t0 - 0.3 && !fim ? PW.run : PW.tx);
    ctx.save(); ctx.globalAlpha = a; rr(ctx, x + 20 * u, top + 62 * u, LW - 40 * u, 46 * u, 6 * u); ctx.fillStyle = "#3c3c3c"; ctx.fill(); ctx.restore();
    txt(ctx, s.filtro || "Filter (e.g. text, @tag)", font(500, 20 * u), x + 36 * u, top + 85 * u, s.filtro ? PW.tx : "#9d9d9d", "left", a);
    txt(ctx, "Projects: " + (s.projeto || "chromium"), font(600, 20 * u), x + 24 * u, top + 136 * u, PW.blue, "left", a);
    let yy = top + 186 * u, gi = 0, alvo = null;
    (s.arquivos || [["example.spec.js", ["has title"]]]).forEach(([arq, testes]) => {
      txt(ctx, "▾", font(700, 20 * u), x + 26 * u, yy, PW.mut, "left", a);
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#e8b04a"; rr(ctx, x + 50 * u, yy - 12 * u, 20 * u, 24 * u, 3 * u); ctx.fill(); ctx.restore();
      txt(ctx, arq, font(700, 23 * u), x + 82 * u, yy, PW.tx, "left", a);
      if (s.watch) { const kw = s.watch_em ? easeOut((t - s.watch_em) / 0.3) : 1; const wx = x + LW - 150 * u;  // watch: o olho que roda de novo quando salva
        ctx.save(); ctx.globalAlpha = a; rr(ctx, wx - 10 * u, yy - 18 * u, 120 * u, 36 * u, 18 * u); ctx.fillStyle = kw > 0 ? "rgba(255,210,63," + (0.18 * kw) + ")" : "transparent"; ctx.fill(); ctx.strokeStyle = kw > 0.5 ? C.yel : PW.mut; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
        txt(ctx, "👁 watch", font(700, 19 * u), wx + 50 * u, yy, kw > 0.5 ? C.yel : PW.mut, "center", a);
        if (s.watch_em) rota(ctx, u, [[wx + 50 * u, yy, s.watch_em]], t); }
      yy += 48 * u;
      testes.forEach((tt) => { const [nome, est0] = Array.isArray(tt) ? tt : [tt, s.pronto ? (s.status === "falhou" ? "falhou" : "ok") : "espera"]; const eu = gi === (s.roda || 0);
        const st = eu ? (s.pronto ? (falha ? "falhou" : "ok") : t < tm.t0 ? "espera" : fim ? (falha ? "falhou" : "ok") : "rodando") : est0;
        if (eu) { ctx.save(); ctx.globalAlpha = a * 0.9; ctx.fillStyle = PW.sel; ctx.fillRect(x, yy - 22 * u, LW, 44 * u); ctx.restore(); alvo = [x + LW - 44 * u, yy]; }
        pwStatus(ctx, u, x + 66 * u, yy, st, t, a); txt(ctx, corta(ctx, nome, font(500, 22 * u), LW - 160 * u), font(500, 22 * u), x + 92 * u, yy, PW.tx, "left", a);
        if (eu) pwPlay(ctx, u, x + LW - 44 * u, yy, a); yy += 44 * u; gi++; });
      yy += 10 * u;
    });
    // painel de ações
    const mx = x + LW + 2 * u; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.bg; ctx.fillRect(mx, top, MW, y + H - top); ctx.fillStyle = PW.bd; ctx.fillRect(mx + MW, top, 2 * u, y + H - top); ctx.restore();
    txt(ctx, "Actions", font(700, 22 * u), mx + 24 * u, top + 34 * u, "#fff", "left", a); ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.blue; ctx.fillRect(mx + 24 * u, top + 54 * u, 76 * u, 4 * u); ctx.restore();
    txt(ctx, "Metadata", font(500, 22 * u), mx + 130 * u, top + 34 * u, PW.mut, "left", a);
    yy = top + 100 * u; const nF = Math.floor(feitos);
    A.forEach(([nome, arg, ms], i) => { const k = clamp(feitos - i); if (k <= 0) return; const atual = i === Math.min(A.length - 1, nF - (fim ? 1 : 0)); const ruim = falha && fim && i === A.length - 1;
      if (atual) { ctx.save(); ctx.globalAlpha = a * k; ctx.fillStyle = ruim ? "rgba(248,81,73,.22)" : PW.sel; ctx.fillRect(mx, yy - 22 * u, MW, 44 * u); ctx.restore(); }
      txt(ctx, nome, font(700, 21 * u), mx + 24 * u, yy, ruim ? PW.bad : "#fff", "left", a * k);
      const nw = tw(ctx, nome, font(700, 21 * u)); txt(ctx, corta(ctx, arg || "", font(500, 19 * u, MONO), MW - nw - 120 * u), font(500, 19 * u, MONO), mx + 34 * u + nw, yy, PW.blue, "left", a * k);
      txt(ctx, ms || (40 + ((i * 37) % 160)) + "ms", font(500, 18 * u), mx + MW - 18 * u, yy, PW.mut, "right", a * k); yy += 44 * u; });
    // snapshot
    const sx = mx + MW + 2 * u; const p = pwSnapshot(ctx, c, t, s, media, sx, top, x + W - sx, y + H - top, a, feitos / Math.max(A.length, 1));
    if (s.elem && feitos > 0.5) caixaElem(ctx, u, p, s.elem, a * easeOut((feitos - 0.5) / 0.5), s.rotulo || null);
    if (fim && (s.selo_status !== false)) { const ka = easeOut((t - tm.fim) / 0.35) * (s.pronto ? 1 : 1); const lab = falha ? "FALHOU" : "PASSOU"; const f = font(900, 36 * u); const bw = tw(ctx, lab, f) + 60 * u;
      ctx.save(); ctx.globalAlpha = ka; rr(ctx, x + W - bw - 30 * u, y + H - 92 * u, bw, 62 * u, 31 * u); ctx.fillStyle = falha ? C.red : C.ac; ctx.fill(); ctx.restore(); txt(ctx, lab, f, x + W - bw / 2 - 30 * u, y + H - 61 * u, "#0b1a12", "center", ka); }
    if (s.clique !== false && alvo && !s.pronto) rota(ctx, u, [[alvo[0], alvo[1], tm.t0 - 0.1]], t);
    legenda(ctx, c, t, s);
  };

  // TRACE VIEWER: {type:"pw_trace", media:"...", acoes:[["Navigate to","/"],...], sel:3, falhou:true, erro:"...", aba:"Errors"|"Call"|"Source", codigo:"...", linha:7}
  S.pw_trace = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1720 * u, H = 760 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "Playwright Trace Viewer", a, PW.bg);
    const A = s.passos_pw || (s.acoes || []).filter(Array.isArray); const LW = 500 * u; const sel = s.sel === undefined ? A.length - 1 : s.sel;
    // a seleção anda de cima até a ação escolhida
    const tSel = s.sel_em === undefined ? 1.0 : s.sel_em; const curSel = Math.round(lerp(0, sel, easeInOut((t - tSel) / Math.max(0.6, sel * 0.25))));
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.pan; ctx.fillRect(x, top, LW, y + H - top); ctx.fillStyle = PW.bd; ctx.fillRect(x + LW, top, 2 * u, y + H - top); ctx.restore();
    txt(ctx, "Actions", font(700, 22 * u), x + 24 * u, top + 34 * u, "#fff", "left", a); ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.blue; ctx.fillRect(x + 24 * u, top + 54 * u, 76 * u, 4 * u); ctx.restore();
    txt(ctx, "Metadata", font(500, 22 * u), x + 130 * u, top + 34 * u, PW.mut, "left", a);
    let yy = top + 100 * u;
    A.forEach(([nome, arg, ms], i) => { const on = i === curSel; const ruim = s.falhou && i === A.length - 1;
      if (on) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = ruim ? "rgba(248,81,73,.25)" : PW.sel; ctx.fillRect(x, yy - 22 * u, LW, 44 * u); ctx.restore(); }
      if (ruim) pwStatus(ctx, u, x + 22 * u, yy, "falhou", t, a);
      txt(ctx, nome, font(700, 21 * u), x + 42 * u, yy, ruim ? PW.bad : "#fff", "left", a); const nw = tw(ctx, nome, font(700, 21 * u));
      txt(ctx, corta(ctx, arg || "", font(500, 19 * u, MONO), LW - nw - 140 * u), font(500, 19 * u, MONO), x + 52 * u + nw, yy, PW.blue, "left", a);
      txt(ctx, ms || (40 + ((i * 37) % 160)) + "ms", font(500, 18 * u), x + LW - 18 * u, yy, PW.mut, "right", a); yy += 44 * u; });
    const sx = x + LW + 2 * u, sw = x + W - sx, bh = 230 * u; const sh = y + H - top - bh;
    const p = pwSnapshot(ctx, c, t, s, media, sx, top, sw, sh, a, 1);
    if (s.elem && curSel === sel) caixaElem(ctx, u, p, s.elem, a * easeOut((t - tSel - 0.6) / 0.4), s.rotulo || null, s.falhou ? "rgba(248,81,73,.45)" : undefined);
    // painel de baixo
    const by = top + sh; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.pan; ctx.fillRect(sx, by, sw, bh); ctx.fillStyle = PW.bd; ctx.fillRect(sx, by, sw, 2 * u); ctx.restore();
    const abas = ["Call", "Log", "Errors", "Console", "Network", "Source"]; const ab = s.aba || (s.falhou ? "Errors" : "Call"); let ax = sx + 24 * u;
    abas.forEach((n) => { const on = n === ab; const f = font(on ? 700 : 500, 21 * u); txt(ctx, n + (n === "Errors" && s.falhou ? " 1" : ""), f, ax, by + 32 * u, on ? "#fff" : PW.mut, "left", a);
      const w = tw(ctx, n + (n === "Errors" && s.falhou ? " 1" : ""), f); if (on) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = PW.blue; ctx.fillRect(ax, by + 52 * u, w, 4 * u); ctx.restore(); } ax += w + 40 * u; });
    const ka = easeOut((t - tSel - Math.max(0.6, sel * 0.25) - 0.2) / 0.4);
    if (ab === "Errors" && s.erro) { String(s.erro).split("\n").slice(0, 4).forEach((l, i) => txt(ctx, corta(ctx, l, font(600, 20 * u, MONO), sw - 60 * u), font(600, 20 * u, MONO), sx + 28 * u, by + 92 * u + i * 34 * u, i ? PW.tx : PW.bad, "left", a * ka)); }
    else if (ab === "Source" && s.codigo) { const L = String(s.codigo).split("\n"); const ln = s.linha || 1; const ini = Math.max(0, ln - 3);
      L.slice(ini, ini + 4).forEach((l, i) => { const n = ini + i + 1; if (n === ln) { ctx.save(); ctx.globalAlpha = a * ka * 0.6; ctx.fillStyle = s.falhou ? "rgba(248,81,73,.35)" : PW.sel; ctx.fillRect(sx, by + 92 * u + i * 34 * u - 17 * u, sw, 34 * u); ctx.restore(); }
        txt(ctx, String(n), font(500, 19 * u, MONO), sx + 50 * u, by + 92 * u + i * 34 * u, PW.mut, "right", a); let xx = sx + 70 * u; for (const [tk, cor] of tokens(l)) { txt(ctx, tk, font(500, 20 * u, MONO), xx, by + 92 * u + i * 34 * u, cor, "left", a); xx += tw(ctx, tk, font(500, 20 * u, MONO)); } }); }
    else { const ac = A[sel] || ["", ""]; [["action", ac[0]], ["locator", ac[1] || "—"], ["duration", ac[2] || "120ms"]].forEach(([k, v], i) => { txt(ctx, k, font(600, 20 * u), sx + 28 * u, by + 92 * u + i * 38 * u, PW.mut, "left", a * ka); txt(ctx, v, font(600, 20 * u, MONO), sx + 170 * u, by + 92 * u + i * 38 * u, PW.tx, "left", a * ka); }); }
    legenda(ctx, c, t, s);
  };

  // CODEGEN / INSPECTOR: navegador (esq.) + Playwright Inspector (dir.)
  // modo "gravar": {type:"pw_codegen", media:"site_sauce", url:"https://www.saucedemo.com", inspecionar_varios:["#user-name","#password","#login-button"],
  //   acoes:[{elem:0, valor:"standard_user", linha:"await page.locator('[data-test=\"username\"]').fill('standard_user');"}, {elem:2, linha:"..."}]}
  // modo "pick": {..., modo:"pick", elem:0, locator:"getByTestId('username')"}   modo "debug": {..., modo:"debug", codigo:"...", linhas_passo:[4,5,6]}
  S.pw_codegen = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const modo = s.modo || "gravar";
    const BW = 940 * u, IW = 800 * u, H = 740 * u, gap = 20 * u; const bx = c.cx - (BW + IW + gap) / 2, ix = bx + BW + gap, y = topo(c, H);
    // navegador
    const btop = janela(ctx, bx, y, BW, H, u, "Chromium", a, "#fff");
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#eef0f4"; ctx.fillRect(bx, btop, BW, 60 * u); rr(ctx, bx + 24 * u, btop + 12 * u, BW - 48 * u, 36 * u, 18 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.restore();
    txt(ctx, (s.url || "").replace(/^https?:\/\//, ""), font(500, 20 * u), bx + 50 * u, btop + 30 * u, "#3c4043", "left", a);
    const m = media && media[s.media]; const el = m && (m.video || m.img); const els = s.elems || (s.elem && Array.isArray(s.elem[0]) ? s.elem : s.elem ? [s.elem] : []);
    const sy = btop + 60 * u, sh = y + H - sy; const f0 = els[0] ? [(els[0][0] + els[0][2]) / 2, (els[0][1] + els[0][3]) / 2] : [0.5, 0.35];
    const p = print(ctx, el, bx, sy, BW, sh, a, "#fff", f0, s.zoom_site || 1.7);
    // inspector
    const itop = janela(ctx, ix, y, IW, H, u, "Playwright Inspector", a, "#ffffff");
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#f3f3f3"; ctx.fillRect(ix, itop, IW, 64 * u); ctx.fillStyle = "#e0e0e0"; ctx.fillRect(ix, itop + 64 * u, IW, 2 * u); ctx.restore();
    const gravando = modo === "gravar", pick = modo === "pick", dbg = modo === "debug";
    let tx0 = ix + 24 * u;
    const botao = (rot, ativo, cor) => { const f = font(700, 20 * u); const w = tw(ctx, rot, f) + (cor ? 44 : 24) * u; ctx.save(); ctx.globalAlpha = a; rr(ctx, tx0, itop + 14 * u, w, 36 * u, 6 * u); ctx.fillStyle = ativo ? "#dbe9ff" : "#fff"; ctx.fill(); ctx.strokeStyle = ativo ? "#3b82f6" : "#cfcfcf"; ctx.lineWidth = 2 * u; ctx.stroke();
      if (cor) { ctx.beginPath(); ctx.arc(tx0 + 20 * u, itop + 32 * u, 7 * u, 0, 7); ctx.fillStyle = cor; ctx.fill(); } ctx.restore(); txt(ctx, rot, f, tx0 + (cor ? 34 : 12) * u, itop + 32 * u, "#202124", "left", a); const r = [tx0, itop + 32 * u, w]; tx0 += w + 12 * u; return r; };
    let bPick = null, bAssert = null;
    if (dbg) { botao("▶ Resume", false); botao("⤼ Step over", true); botao("Pick locator", false); }
    else { botao("Record", gravando, gravando ? (Math.floor(t * 2) % 2 ? "#e53935" : "#ff6b6b") : "#9e9e9e"); bPick = botao("Pick locator", pick);
      if (s.botoes_assert) { botao("Assert visibility", false); bAssert = botao("Assert text", (s.assert_em || 0) && t > s.assert_em && t < s.assert_em + 1.6); } else botao("Copy", false); }
    if (!dbg && !s.botoes_assert) txt(ctx, "Target: Test Runner ▾", font(600, 19 * u), ix + IW - 24 * u, itop + 32 * u, "#5f6368", "right", a);
    // código
    const base = dbg ? String(s.codigo || "").split("\n") : ["import { test, expect } from '@playwright/test';", "", "test('test', async ({ page }) => {", "  await page.goto('" + (s.url || "https://www.saucedemo.com").replace(/\/$/, "") + "/');"];
    const AC = s.passos_pw || (s.acoes || []).filter((q) => q && q.linha); const t0 = s.inicio_em === undefined ? 1.4 : s.inicio_em; const passo = Math.max(1.0, Math.min(2.2, (dur * 0.8 - t0) / Math.max(AC.length - (s.ja || 0), 1)));
    const tClick = AC.map((_, i) => t0 + 0.6 + i * passo); const L = base.slice(); const novas = [];
    const ja = s.ja || 0;  // as primeiras "ja" linhas já estavam gravadas (cena anterior): aparecem prontas
    if (ja) for (let i = 0; i < ja; i++) tClick[i] = -10; for (let i = ja; i < AC.length; i++) tClick[i] = t0 + 0.6 + (i - ja) * passo;
    if (gravando) { AC.forEach((ac, i) => { if (t > tClick[i] + 0.25) { L.push("  " + ac.linha); if (i >= ja) novas.push([L.length, tClick[i] + 0.25]); } }); L.push("});"); }
    const fs = Math.min(21 * u, (IW - 90 * u) / (Math.max(30, ...L.map((l) => l.length)) * 0.6)); const lh = fs * 1.75; let yy = itop + 100 * u;
    const passoDbg = dbg ? (s.linhas_passo || []) : []; const tDbg = dbg ? Math.max(0.8, (dur * 0.75 - 1) / Math.max(passoDbg.length, 1)) : 0; const iDbg = dbg ? Math.min(passoDbg.length - 1, Math.floor(clamp((t - 1) / tDbg, 0, passoDbg.length - 0.001))) : -1; const linhaDbg = passoDbg[iDbg];
    ctx.save(); ctx.beginPath(); ctx.rect(ix, itop + 66 * u, IW, (pick ? H - 300 * u : H - 120 * u)); ctx.clip();
    L.forEach((ln, i) => { const n = i + 1; const nv = novas.find((q) => q[0] === n); const kn = nv ? easeOut((t - nv[1]) / 0.3) : 1;
      if (nv) { const hl = 1 - easeOut((t - nv[1] - 1.2) / 0.6); if (hl > 0) { ctx.save(); ctx.globalAlpha = a * 0.25 * hl; ctx.fillStyle = "#3fd68a"; ctx.fillRect(ix, yy - lh / 2, IW, lh); ctx.restore(); } }
      if (dbg && n === linhaDbg) { ctx.save(); ctx.globalAlpha = a * 0.35; ctx.fillStyle = "#ffd23f"; ctx.fillRect(ix, yy - lh / 2, IW, lh); ctx.restore(); txt(ctx, "▶", font(800, fs * 0.8), ix + 12 * u, yy, "#c77c00", "left", a); }
      txt(ctx, String(n), font(500, fs * 0.85, MONO), ix + 56 * u, yy, "#9aa0a6", "right", a * kn); let xx = ix + 72 * u;
      for (const [tk, cor] of tokens(ln)) { const cc = cor === C.txt ? "#202124" : cor === C.mut ? "#80868b" : cor === "#f0a868" ? "#b8461b" : cor === C.ac2 ? "#1a56c4" : cor === C.ac ? "#188038" : cor === "#c792ea" ? "#8430ce" : cor; txt(ctx, tk, font(500, fs, MONO), xx, yy, cc, "left", a * kn); xx += tw(ctx, tk, font(500, fs, MONO)); }
      yy += lh; });
    ctx.restore();
    // pick locator: campo de locator embaixo
    const pts = [];
    if (pick) { const ly = y + H - 190 * u; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#f8f9fa"; ctx.fillRect(ix, ly, IW, 168 * u); ctx.fillStyle = "#e0e0e0"; ctx.fillRect(ix, ly, IW, 2 * u); ctx.restore();
      txt(ctx, "Locator", font(700, 20 * u), ix + 24 * u, ly + 34 * u, "#5f6368", "left", a);
      const tp = s.pick_em || 1.2, th = tp + 1.3; const kl = easeOut((t - th - 0.2) / 0.3);
      ctx.save(); ctx.globalAlpha = a; rr(ctx, ix + 24 * u, ly + 60 * u, IW - 48 * u, 64 * u, 8 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.strokeStyle = kl > 0 ? "#3b82f6" : "#cfcfcf"; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
      txt(ctx, s.locator || "getByTestId('username')", font(600, 22 * u, MONO), ix + 44 * u, ly + 92 * u, "#188038", "left", a * kl);
      if (bPick) pts.push([bPick[0] + bPick[2] / 2, bPick[1], tp]);
      const e = els[s.elem_i || 0]; if (e) { const [x0, y0] = p(e[0], e[1]), [x1, y1] = p(e[2], e[3]); pts.push([(x0 + x1) / 2, (y0 + y1) / 2, th]);
        const kh = easeOut((t - th + 0.4) / 0.25); if (kh > 0) { ctx.save(); ctx.globalAlpha = a * kh; ctx.fillStyle = "rgba(111,168,220,.55)"; ctx.fillRect(x0, y0, x1 - x0, y1 - y0); ctx.restore();
          const f = font(700, 20 * u, MONO), lab = s.locator || "getByTestId('username')", w = tw(ctx, lab, f) + 28 * u; ctx.save(); ctx.globalAlpha = a * kh; ctx.shadowColor = "rgba(0,0,0,.3)"; ctx.shadowBlur = 12 * u; rr(ctx, x0, y0 - 52 * u, w, 40 * u, 6 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.restore();
          txt(ctx, lab, f, x0 + 14 * u, y0 - 32 * u, "#188038", "left", a * kh); } } }
    // gravar: mouse clica em cada elemento e digita o valor no campo
    if (bAssert && s.assert_em) pts.push([bAssert[0] + bAssert[2] / 2, bAssert[1], s.assert_em]);
    if (gravando) AC.forEach((ac, i) => { if (i < (s.ja || 0)) return; const e = els[ac.elem === undefined ? i : ac.elem]; if (!e) return; const [x0, y0] = p(e[0], e[1]), [x1, y1] = p(e[2], e[3]); pts.push([(x0 + x1) / 2, (y0 + y1) / 2, tClick[i]]);
      const kv = t > tClick[i] ? 1 : 0; if (kv && i === AC.length - 1 && !ac.valor) { /* clique final */ }
      if (ac.valor && t > tClick[i] + 0.1) { const k = clamp((t - tClick[i] - 0.1) / 0.6); const v = ac.valor.slice(0, Math.ceil(k * ac.valor.length)); const mask = ac.senha ? "•".repeat(v.length) : v;
        ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#fff"; ctx.fillRect(x0 + 3 * u, y0 + 3 * u, x1 - x0 - 6 * u, y1 - y0 - 6 * u); ctx.restore(); txt(ctx, mask, font(500, Math.min(26 * u, (y1 - y0) * 0.5)), x0 + 14 * u, (y0 + y1) / 2, "#222", "left", a); }
      const kh = t > tClick[i] - 0.5 && t < tClick[i] + 0.6 ? 1 : 0; if (kh) { ctx.save(); ctx.globalAlpha = a * 0.5; ctx.fillStyle = "rgba(111,168,220,.55)"; ctx.fillRect(x0, y0, x1 - x0, y1 - y0); ctx.restore(); } });
    if (dbg && els.length) { const e = els[Math.max(0, iDbg) % els.length]; caixaElem(ctx, u, p, e, a * easeOut((t - 1) / 0.3), null); }
    rota(ctx, u, pts, t);
    legenda(ctx, c, t, s);
  };

  // RELATÓRIO HTML: {type:"pw_relatorio", testes:[["entra com usuário e senha","login.spec.js:9","chromium","ok","1.2s"], ...], abrir:{titulo, passos:[["adiciona a mochila","0.8s"]], erro:"..."}}
  S.pw_relatorio = (ctx, c, t, dur, s, media) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1640 * u, H = 740 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "Playwright Test Report", a, "#ffffff");
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#eef0f4"; ctx.fillRect(x, top, W, 56 * u); rr(ctx, x + 24 * u, top + 10 * u, 520 * u, 36 * u, 18 * u); ctx.fillStyle = "#fff"; ctx.fill(); ctx.restore();
    txt(ctx, "localhost:9323", font(500, 20 * u), x + 50 * u, top + 28 * u, "#3c4043", "left", a);
    const T = s.testes || []; const nOk = T.filter((q) => q[3] === "ok").length, nF = T.filter((q) => q[3] === "falhou").length, nFl = T.filter((q) => q[3] === "instavel").length, nS = T.filter((q) => q[3] === "pulado").length;
    const by = top + 100 * u; ctx.save(); ctx.globalAlpha = a; rr(ctx, x + 40 * u, by - 26 * u, 560 * u, 52 * u, 8 * u); ctx.strokeStyle = "#d0d7de"; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
    txt(ctx, "⌕  Search", font(500, 22 * u), x + 60 * u, by, "#8c959f", "left", a);
    let fx = x + 640 * u; [["All", T.length, "#24292f"], ["Passed", nOk, "#1a7f37"], ["Failed", nF, "#cf222e"], ["Flaky", nFl, "#9a6700"], ["Skipped", nS, "#57606a"]].forEach(([n, v, cor], i) => {
      const f = font(i === 0 ? 800 : 600, 22 * u); txt(ctx, n, f, fx, by, "#24292f", "left", a); const w = tw(ctx, n, f); const vb = String(v); const vw = tw(ctx, vb, font(700, 18 * u)) + 20 * u;
      ctx.save(); ctx.globalAlpha = a; rr(ctx, fx + w + 10 * u, by - 15 * u, vw, 30 * u, 15 * u); ctx.fillStyle = i === 0 ? "#eaeef2" : cor + "22"; ctx.fill(); ctx.restore(); txt(ctx, vb, font(700, 18 * u), fx + w + 10 * u + vw / 2, by, cor, "center", a); fx += w + vw + 44 * u; });
    if (s.abrir) {  // detalhe de um teste
      const d = s.abrir; const dy = top + 160 * u; const ok = d.status !== "falhou";
      pwStatus(ctx, u, x + 60 * u, dy, ok ? "ok" : "falhou", t, a); txt(ctx, d.titulo || "", font(800, 30 * u), x + 84 * u, dy, "#24292f", "left", a);
      txt(ctx, (d.arquivo || "") + "  ·  " + (d.projeto || "chromium"), font(500, 20 * u), x + 84 * u, dy + 40 * u, "#57606a", "left", a);
      if ((d.passos || []).length) txt(ctx, "Test Steps", font(800, 24 * u), x + 60 * u, dy + 100 * u, "#24292f", "left", a);
      (d.passos || []).forEach(([n, ms, st], i) => { const k = easeOut((t - 0.8 - i * 0.35) / 0.3); const yy = dy + 150 * u + i * 52 * u;
        ctx.save(); ctx.globalAlpha = a * k; ctx.fillStyle = i % 2 ? "#f6f8fa" : "#fff"; ctx.fillRect(x + 50 * u, yy - 24 * u, W - 100 * u, 48 * u); ctx.restore();
        pwStatus(ctx, u, x + 80 * u, yy, st || "ok", t, a * k); txt(ctx, n, font(600, 23 * u), x + 106 * u, yy, "#24292f", "left", a * k); txt(ctx, ms || "", font(500, 20 * u), x + W - 70 * u, yy, "#57606a", "right", a * k); });
      if (d.erro) { const ey = dy + 170 * u + (d.passos || []).length * 52 * u; const k = easeOut((t - 1.4) / 0.4);
        ctx.save(); ctx.globalAlpha = a * k; rr(ctx, x + 50 * u, ey, W - 100 * u, 120 * u, 8 * u); ctx.fillStyle = "#ffebe9"; ctx.fill(); ctx.strokeStyle = "#ff8182"; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
        String(d.erro).split("\n").slice(0, 3).forEach((l, i) => txt(ctx, l, font(600, 20 * u, MONO), x + 74 * u, ey + 32 * u + i * 30 * u, i ? "#24292f" : "#cf222e", "left", a * k)); }
      if (d.anexos) {  // print e vídeo guardados quando o teste falha
        const ay = dy + 170 * u + (d.passos || []).length * 52 * u + (d.erro ? 140 * u : 0); const th = Math.min(150 * u, y + H - ay - 50 * u), tw0 = th * 16 / 9; const ka = easeOut((t - (d.anexos_em || 2.0)) / 0.4);
        (Array.isArray(d.anexos) ? d.anexos : [["Screenshots", d.anexo_img, false], ["Videos", d.anexo_video_img || d.anexo_img, true]]).forEach(([rot, mk, play], i) => { const ax = x + 60 * u + i * (tw0 + 80 * u);
          txt(ctx, rot, font(800, 22 * u), ax, ay + 14 * u, "#24292f", "left", a * ka);
          const m = media && media[mk]; const el = m && (m.video || m.img); ctx.save(); ctx.globalAlpha = a * ka; rr(ctx, ax, ay + 34 * u, tw0, th, 6 * u); ctx.fillStyle = "#eef0f4"; ctx.fill(); ctx.clip();
          if (el) ctx.drawImage(el, ax, ay + 34 * u, tw0, th); ctx.restore(); ctx.save(); ctx.globalAlpha = a * ka; ctx.strokeStyle = "#d0d7de"; ctx.lineWidth = 2 * u; rr(ctx, ax, ay + 34 * u, tw0, th, 6 * u); ctx.stroke(); ctx.restore();
          if (play) { ctx.save(); ctx.globalAlpha = a * ka; ctx.beginPath(); ctx.arc(ax + tw0 / 2, ay + 34 * u + th / 2, 30 * u, 0, 7); ctx.fillStyle = "rgba(0,0,0,.55)"; ctx.fill(); ctx.fillStyle = "#fff"; ctx.beginPath();
            ctx.moveTo(ax + tw0 / 2 - 9 * u, ay + 34 * u + th / 2 - 14 * u); ctx.lineTo(ax + tw0 / 2 + 15 * u, ay + 34 * u + th / 2); ctx.lineTo(ax + tw0 / 2 - 9 * u, ay + 34 * u + th / 2 + 14 * u); ctx.fill(); ctx.restore();
            if (s.navegador) rota(ctx, u, [[ax + tw0 / 2, ay + 34 * u + th / 2, s.navegador.em * dur - 0.1]], t); } }); }
    } else {
      let yy = top + 170 * u; let arqAtual = null;
      T.forEach(([nome, arq, proj, st, ms], i) => { const k = easeOut((t - 0.6 - i * 0.12) / 0.3); const f0 = String(arq).split(":")[0];
        if (f0 !== arqAtual) { arqAtual = f0; ctx.save(); ctx.globalAlpha = a * k; ctx.fillStyle = "#f6f8fa"; ctx.fillRect(x + 40 * u, yy - 22 * u, W - 80 * u, 44 * u); ctx.restore(); txt(ctx, "▾  " + f0, font(700, 22 * u), x + 60 * u, yy, "#24292f", "left", a * k); yy += 50 * u; }
        pwStatus(ctx, u, x + 74 * u, yy, st === "instavel" ? "ok" : st === "pulado" ? "espera" : st, t, a * k); txt(ctx, nome, font(600, 23 * u), x + 100 * u, yy, "#24292f", "left", a * k);
        const nw = tw(ctx, nome, font(600, 23 * u)); const pf = font(700, 17 * u); const pw2 = tw(ctx, proj, pf) + 22 * u; const cores = { chromium: "#0969da", firefox: "#bc4c00", webkit: "#8250df", celular: "#1a7f37" };
        ctx.save(); ctx.globalAlpha = a * k; rr(ctx, x + 116 * u + nw, yy - 14 * u, pw2, 28 * u, 14 * u); ctx.fillStyle = (cores[proj] || "#57606a") + "22"; ctx.fill(); ctx.restore(); txt(ctx, proj, pf, x + 116 * u + nw + pw2 / 2, yy, cores[proj] || "#57606a", "center", a * k);
        if (st === "instavel") txt(ctx, "flaky", font(700, 17 * u), x + 130 * u + nw + pw2, yy, "#9a6700", "left", a * k);
        txt(ctx, arq, font(500, 18 * u), x + 100 * u, yy + 26 * u, "#57606a", "left", a * k); txt(ctx, ms || "", font(500, 20 * u), x + W - 70 * u, yy, "#57606a", "right", a * k); yy += 66 * u; });
    }
    if (s.navegador) navegadorPorCima(ctx, c, t, dur, s.navegador, media);
    legenda(ctx, c, t, s);
  };

  // GITHUB ACTIONS (tema escuro): {type:"gh_actions", workflow:"Playwright Tests", commit:"adiciona testes de login", passos:["Set up job","Install dependencies",...], status:"ok"|"falhou", pronto:false, artefato:"playwright-report"}
  S.gh_actions = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const W = 1640 * u, H = 740 * u; const x = c.cx - W / 2, y = topo(c, H);
    const top = janela(ctx, x, y, W, H, u, "github.com/" + (s.usuario || "voce") + "/" + (s.repo || "meu-primeiro-playwright") + "/actions", a, "#0d1117");
    const P = s.passos || ["Set up job", "Run actions/checkout@v4", "Run actions/setup-node@v4", "Install dependencies", "Install Playwright Browsers", "Run Playwright tests", "Run actions/upload-artifact@v4", "Complete job"];
    const t0 = s.inicio_em === undefined ? 0.8 : s.inicio_em; const passo = Math.max(0.3, Math.min(1.0, (dur * 0.7 - t0) / P.length)); const feitos = s.pronto ? P.length : clamp((t - t0) / passo, 0, P.length); const fim = feitos >= P.length; const falha = s.status === "falhou";
    txt(ctx, s.workflow || "Playwright Tests", font(800, 34 * u), x + 40 * u, top + 54 * u, "#e6edf3", "left", a);
    const st = fim ? (falha ? "falhou" : "ok") : "rodando"; pwStatus(ctx, u, x + 52 * u, top + 108 * u, st, t, a);
    txt(ctx, s.commit || "adiciona os testes", font(600, 24 * u), x + 76 * u, top + 108 * u, "#e6edf3", "left", a);
    txt(ctx, "#" + (s.numero || 1) + " · main", font(500, 20 * u), x + 76 * u, top + 142 * u, "#8b949e", "left", a);
    if (fim) { const ka = easeOut((t - (s.pronto ? 0.3 : t0 + P.length * passo)) / 0.4); const lab = falha ? "Failure" : "Success"; const f = font(900, 34 * u); const bw = tw(ctx, lab, f) + 90 * u;
      ctx.save(); ctx.globalAlpha = a * ka; rr(ctx, x + W - bw - 40 * u, top + 40 * u, bw, 70 * u, 35 * u); ctx.fillStyle = falha ? "#da3633" : "#238636"; ctx.fill(); ctx.restore();
      pwStatus(ctx, u * 1.3, x + W - bw - 40 * u + 40 * u, top + 75 * u, falha ? "falhou" : "ok", t, a * ka); txt(ctx, lab, f, x + W - bw / 2 - 40 * u + 20 * u, top + 75 * u, "#fff", "center", a * ka); }
    // coluna de jobs
    const jy = top + 190 * u; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = "#30363d"; ctx.fillRect(x, jy - 10 * u, W, 2 * u); ctx.restore();
    txt(ctx, "Jobs", font(700, 22 * u), x + 40 * u, jy + 30 * u, "#8b949e", "left", a);
    ctx.save(); ctx.globalAlpha = a; rr(ctx, x + 30 * u, jy + 56 * u, 300 * u, 50 * u, 8 * u); ctx.fillStyle = "#161b22"; ctx.fill(); ctx.restore(); pwStatus(ctx, u, x + 56 * u, jy + 81 * u, st, t, a); txt(ctx, s.job || "test", font(700, 23 * u), x + 80 * u, jy + 81 * u, "#e6edf3", "left", a);
    if (s.artefato !== false && fim && !falha) { txt(ctx, "Artifacts", font(700, 22 * u), x + 40 * u, jy + 160 * u, "#8b949e", "left", a); txt(ctx, "📦 " + (s.artefato || "playwright-report"), font(600, 22 * u), x + 40 * u, jy + 200 * u, "#58a6ff", "left", a * easeOut((t - t0 - P.length * passo) / 0.4)); }
    // passos
    const px = x + 370 * u, pw = W - 410 * u; ctx.save(); ctx.globalAlpha = a; rr(ctx, px, jy + 10 * u, pw, y + H - jy - 30 * u, 10 * u); ctx.fillStyle = "#161b22"; ctx.fill(); ctx.strokeStyle = "#30363d"; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
    const lh = Math.min(50 * u, (y + H - jy - 60 * u) / P.length);
    P.forEach((n, i) => { const yy = jy + 40 * u + i * lh; const k = feitos - i; const sp = k >= 1 ? (falha && i === P.length - 3 && fim ? "falhou" : "ok") : k > 0 ? "rodando" : "espera";
      pwStatus(ctx, u, px + 34 * u, yy, sp, t, a); txt(ctx, n, font(600, 22 * u), px + 62 * u, yy, k > 0 ? "#e6edf3" : "#6e7681", "left", a);
      if (k >= 1) txt(ctx, (1 + ((i * 7) % 23)) + "s", font(500, 19 * u), px + pw - 24 * u, yy, "#8b949e", "right", a); });
    legenda(ctx, c, t, s);
  };


  // TRADUÇÃO: lê uma linha de código como frase em português, pedaço por pedaço
  // {type:"traducao", codigo:"await expect(page).toHaveURL(/inventory/);", partes:[["expect(page)","eu espero que a página"],[".toHaveURL(/inventory/)","tenha inventory no endereço"]], legenda:"..."}
  // modo tabela: {type:"traducao", titulo:"LEIA O CÓDIGO COMO UMA FRASE", linhas:[["expect","eu espero que"], ...]}
  S.traducao = (ctx, c, t, dur, s) => {
    const u = c.u; const a = easeOut(t / 0.4); const cores = [C.ac, C.ac2, C.yel, "#ff8c42", "#c792ea"];
    if (s.linhas) {
      if (s.titulo) txt(ctx, s.titulo, caber(ctx, s.titulo, 900, 56 * u, c.W * 0.9), c.cx, c.H * 0.13, C.txt, "center", a);
      // poucas linhas: maiores e no meio da tela (sem deixar a metade de baixo vazia)
      const L = s.linhas; const g = L.length <= 3 ? 1.3 : 1; const lh = Math.min(110 * g * u, (c.H * 0.6) / L.length); const y0 = Math.max(c.H * 0.26, c.H * 0.52 - (L.length * lh) / 2); const passo = Math.max(0.35, (dur * 0.7 - 0.6) / L.length);
      // divide a largura entre código e tradução do jeito que deixa as duas letras maiores (mesma letra em todas as linhas)
      const px = (f) => parseFloat(f.match(/(\d+(\.\d+)?)px/)[1]); const maisLongo = L.reduce((m, l) => (l[0].length > m.length ? l[0] : m), "");
      let fc, xSeta, xPt, fpt, melhor = -1;
      for (const fr of [0.46, 0.42, 0.38, 0.34, 0.3, 0.26]) {
        const fc1 = caber(ctx, maisLongo, 700, 50 * g * u, c.W * fr, MONO); const xs = c.W * 0.09 + Math.max(...L.map((l) => tw(ctx, l[0], fc1))) + 50 * u, xp = xs + 50 * u, wp = c.W * 0.925 - xp;
        const fp1 = L.reduce((f, l) => { const f2 = caber(ctx, l[1], 800, 48 * g * u, wp); return px(f2) < px(f) ? f2 : f; }, font(800, 48 * g * u));
        const nota = Math.min(px(fc1), px(fp1) * 0.75); if (nota > melhor) { melhor = nota; fc = fc1; xSeta = xs; xPt = xp; fpt = fp1; } }
      L.forEach(([cod, pt], i) => { const k = easeOut((t - (s.em_frac ? s.em_frac[i] * dur : 0.5 + i * passo)) / 0.35);  /* em_frac: cada linha entra quando a narração fala dela */ if (k <= 0) return; const yy = y0 + i * lh + lh / 2; const cor = cores[i % cores.length];
        ctx.save(); ctx.globalAlpha = a * k * 0.9; rr(ctx, c.W * 0.06, yy - lh * 0.42, c.W * 0.88, lh * 0.84, 18 * u); ctx.fillStyle = C.win; ctx.fill(); ctx.fillStyle = cor; ctx.fillRect(c.W * 0.06, yy - lh * 0.42, 8 * u, lh * 0.84); ctx.restore();
        txt(ctx, cod, fc, c.W * 0.09, yy, cor, "left", a * k); txt(ctx, "→", font(800, 50 * u), xSeta, yy, C.mut, "center", a * k);
        txt(ctx, pt, fpt, xPt, yy, C.txt, "left", a * k); });
      legenda(ctx, c, t, s); return;
    }
    const cod = s.codigo || ""; const P = s.partes || [];
    const fc = caber(ctx, cod, 700, 60 * u, c.W * 0.88, MONO); const wTot = tw(ctx, cod, fc); const x0 = c.cx - wTot / 2; const yc = c.H * 0.24;
    // caixa do código
    ctx.save(); ctx.globalAlpha = a; rr(ctx, x0 - 40 * u, yc - 60 * u, wTot + 80 * u, 120 * u, 18 * u); ctx.fillStyle = C.win; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 2 * u; ctx.stroke(); ctx.restore();
    let xx = x0; for (const [tk, cor] of (s.texto_puro ? [[cod, C.txt]] : tokens(cod))) { txt(ctx, tk, fc, xx, yc, cor, "left", a); xx += tw(ctx, tk, fc); }
    const passo = s.passo || Math.max(0.9, (dur * 0.75 - 0.8) / Math.max(P.length, 1));
    // layout dos rótulos (uma vez, todos juntos): numa linha só, na ordem das partes, sem encavalar; quem sai do lugar ganha cotovelo.
    const LAY = P.map(([tr0, pt]) => { const k0 = cod.indexOf(tr0); if (k0 < 0) return null; const xa = x0 + tw(ctx, cod.slice(0, k0), fc), xb = xa + tw(ctx, tr0, fc);
      const fp = caber(ctx, pt, 800, 50 * u, Math.max(280 * u, (c.W * 0.92) / Math.max(P.length, 1))); return { xa, xb, xm: (xa + xb) / 2, fp, w: tw(ctx, pt, fp) + 52 * u, linha: 0 }; });
    { const V = LAY.map((o, i) => o && Object.assign(o, { i })).filter(Boolean).sort((p1, p2) => p1.xm - p2.xm); const gap = 24 * u, E = c.W * 0.03, D = c.W * 0.97;
      const tot = V.reduce((a0, o) => a0 + o.w + gap, -gap);
      if (tot <= D - E) {
        V.forEach((o) => { o.xc = o.xm; }); for (let k = 1; k < V.length; k++) V[k].xc = Math.max(V[k].xc, V[k - 1].xc + V[k - 1].w / 2 + gap + V[k].w / 2);
        if (V.length && V[V.length - 1].xc + V[V.length - 1].w / 2 > D) { V[V.length - 1].xc = D - V[V.length - 1].w / 2; for (let k = V.length - 2; k >= 0; k--) V[k].xc = Math.min(V[k].xc, V[k + 1].xc - V[k + 1].w / 2 - gap - V[k].w / 2); }
        if (V.length && V[0].xc - V[0].w / 2 < E) { V[0].xc = E + V[0].w / 2; for (let k = 1; k < V.length; k++) V[k].xc = Math.max(V[k].xc, V[k - 1].xc + V[k - 1].w / 2 + gap + V[k].w / 2); }
        // cotovelos: os que vão pra direita sobem conforme ficam mais à direita; os que vão pra esquerda, conforme ficam mais à esquerda (assim nenhuma linha cruza)
        const dir = V.filter((o) => o.xc - o.xm > o.w / 2 - 30 * u), esq = V.filter((o) => o.xm - o.xc > o.w / 2 - 30 * u);
        dir.forEach((o, k) => { o.lane = dir.length - 1 - k; }); esq.forEach((o, k) => { o.lane = k; });
      } else {  // não cabe numa linha: várias linhas, cada rótulo em cima da sua parte
        const oc = []; V.forEach((o) => { o.xc = Math.max(E + o.w / 2, Math.min(D - o.w / 2, o.xm)); let L = 0; while (oc.some(([l, a0, a1]) => l === L && !(o.xc + o.w / 2 + gap < a0 || o.xc - o.w / 2 - gap > a1))) L++; o.linha = L; oc.push([L, o.xc - o.w / 2, o.xc + o.w / 2]); });
      } }
    P.forEach(([trecho, pt, nota], i) => { const ini = cod.indexOf(trecho); if (ini < 0) return; const k = easeOut((t - (s.em_frac ? s.em_frac[i] * dur : 0.8 + i * passo)) / 0.4); if (k <= 0) return; const cor = cores[i % cores.length];  /* em_frac: cada parte entra quando a narração fala dela */
      const { xa, xb, xm, fp, xc, linha } = LAY[i]; const wp = LAY[i].w - 52 * u; const yp = yc + 230 * u + linha * 130 * u;
      ctx.save(); ctx.globalAlpha = a * k * 0.12; ctx.fillStyle = cor; ctx.fillRect(xa - 4 * u, yc - 40 * u, xb - xa + 8 * u, 80 * u); ctx.globalAlpha = a * k;
      ctx.fillRect(xa, yc + 70 * u, xb - xa, 6 * u); const yf = yp - 58 * u; const cot = LAY[i].lane !== undefined, xf = cot ? xc : xm;
      if (cot) { const yl = yc + 100 * u + Math.min(LAY[i].lane, 3) * 26 * u;  // cotovelo: desce, anda pro lado por cima dos rótulos, e desce até o rótulo
        ctx.fillRect(xm - 3 * u, yc + 76 * u, 6 * u, yl - yc - 76 * u); ctx.fillRect(Math.min(xm, xc) - 3 * u, yl - 3 * u, Math.abs(xc - xm) + 6 * u, 6 * u); ctx.fillRect(xc - 3 * u, yl, 6 * u, (yf - yl) * k);
      } else ctx.fillRect(xm - 3 * u, yc + 76 * u, 6 * u, (yf - yc - 76 * u) * k);
      ctx.beginPath(); ctx.moveTo(xf - 16 * u, yf - 4 * u); ctx.lineTo(xf + 16 * u, yf - 4 * u); ctx.lineTo(xf, yf + 18 * u); ctx.closePath(); ctx.fill();
      rr(ctx, xc - wp / 2 - 26 * u, yp - 38 * u, wp + 52 * u, 76 * u, 38 * u); ctx.fill(); ctx.restore();
      txt(ctx, pt, fp, xc, yp, "#0b1a12", "center", a * k);
      if (nota) txt(ctx, nota, caber(ctx, nota, 600, 32 * u, c.W * 0.5), xc, yp + 62 * u, C.mut, "center", a * k); });
    legenda(ctx, c, t, s);
  };

})(window);

"""Gera painel.html: narração de cada projeto + atalhos para subir os áudios e baixar o vídeo.

  python ferramentas/painel.py > painel.html
"""
import html, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "tsvini/custo-oculto-fabrica"

projetos = []
for nome in sorted(os.listdir(os.path.join(RAIZ, "projetos")), key=lambda n: -os.path.getmtime(os.path.join(RAIZ, "projetos", n, "projeto.json")) if os.path.exists(os.path.join(RAIZ, "projetos", n, "projeto.json")) else 0):
    f = os.path.join(RAIZ, "projetos", nome, "projeto.json")
    if not os.path.exists(f):
        continue
    p = json.load(open(f, encoding="utf8"))
    blocos = []
    for k, g in enumerate(p["script"]["long"]["parts"]):
        blocos.append({"arquivo": f"parte{k + 1}", "tipo": "Longo", "titulo": g.get("chapter") or "ABERTURA",
                       "texto": " ".join(s["text"].strip() for s in g["sentences"] if s.get("text", "").strip())})
    for i, sh in enumerate(p["script"].get("shorts", [])):
        blocos.append({"arquivo": f"short{i + 1}", "tipo": "Short", "titulo": sh.get("title", ""),
                       "texto": " ".join(s["text"].strip() for s in sh["sentences"] if s.get("text", "").strip())})
    projetos.append({"id": nome, "titulo": p.get("title", nome), "angulo": p.get("angle", ""), "blocos": blocos})

DADOS = json.dumps({"repo": REPO, "projetos": projetos}, ensure_ascii=False).replace("</", "<\\/")

print("""<title>Gravação Custo Oculto</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@500;700&display=swap">
<style>
/* Layout: mesa de gravação — roteiro em blocos de leitura, um por arquivo de áudio, com a fila de envio no topo */
:root{
  --bg:#f3f1ee; --surface:#fffdfa; --ink:#1d1a17; --muted:#6b635b; --line:#ddd6cd;
  --accent:#b3361f; --accent-ink:#fff; --ok:#2f7a4a; --ok-bg:#e3f1e7; --chip:#ece6de;
  --f-display:"Bricolage Grotesque",ui-sans-serif,system-ui,sans-serif;
  --f-read:"Source Serif 4",Georgia,"Times New Roman",serif;
  --f-mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#151311; --surface:#1e1b18; --ink:#efe9e2; --muted:#a39a90; --line:#35302b;
  --accent:#e2593e; --accent-ink:#1a0e0a; --ok:#6cc58c; --ok-bg:#1d2e23; --chip:#2a2622; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#151311; --surface:#1e1b18; --ink:#efe9e2; --muted:#a39a90; --line:#35302b;
  --accent:#e2593e; --accent-ink:#1a0e0a; --ok:#6cc58c; --ok-bg:#1d2e23; --chip:#2a2622; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:15px/1.5 var(--f-display);padding-inline:16px;padding-block:20px 64px}
.wrap{max-width:820px;margin:0 auto;display:grid;gap:22px}
header{display:grid;gap:6px}
.marca{font:700 11px var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
h1{font:800 clamp(28px,6vw,40px)/1.05 var(--f-display);margin:0;text-wrap:balance}
.angulo{color:var(--muted);margin:0;max-width:62ch}
.tabs{display:flex;gap:8px;flex-wrap:wrap}
.tabs button{font:600 14px var(--f-display);border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:7px 14px;border-radius:999px;cursor:pointer}
.tabs button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.envio{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;display:grid;gap:14px}
.passos{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:0;padding:0;list-style:none;counter-reset:p}
.passos li{counter-increment:p;display:grid;gap:4px;min-width:0}
.passos li::before{content:counter(p);font:700 12px var(--f-mono);width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:var(--chip);color:var(--ink)}
.passos b{font-weight:700}
.passos span{color:var(--muted);font-size:14px}
.acoes{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.btn{display:inline-flex;align-items:center;gap:8px;font:700 15px var(--f-display);text-decoration:none;border-radius:10px;padding:11px 16px;border:1px solid var(--line);color:var(--ink);background:var(--surface);cursor:pointer}
.btn.prim{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn:focus-visible,.tabs button:focus-visible,.copiar:focus-visible,label.feito:focus-within{outline:3px solid var(--accent);outline-offset:2px}
.progresso{font:500 13px var(--f-mono);color:var(--muted);font-variant-numeric:tabular-nums}
.barra{height:6px;background:var(--chip);border-radius:3px;overflow:hidden}
.barra i{display:block;height:100%;background:var(--ok);width:0;transition:width .3s}
.blocos{display:grid;gap:14px}
.bloco{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:grid;gap:10px;min-width:0}
.bloco.ok{border-color:var(--ok);background:linear-gradient(var(--ok-bg),var(--surface) 90px)}
.topo{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px}
.arq{font:700 14px var(--f-mono);background:var(--chip);padding:3px 9px;border-radius:6px}
.tipo{font:700 11px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.titulo{font:700 13px var(--f-display);letter-spacing:.06em;min-width:0}
.meta{margin-left:auto;font:500 12px var(--f-mono);color:var(--muted);font-variant-numeric:tabular-nums}
.texto{font:400 18px/1.65 var(--f-read);margin:0;max-width:65ch;user-select:text}
.rodape{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.copiar{font:600 14px var(--f-display);border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:8px;padding:7px 12px;cursor:pointer}
label.feito{display:inline-flex;gap:8px;align-items:center;font-weight:600;cursor:pointer;color:var(--muted)}
.bloco.ok label.feito{color:var(--ok)}
label.feito input{width:18px;height:18px;accent-color:var(--ok)}
.nota{color:var(--muted);font-size:13px;margin:0}
@media (prefers-reduced-motion: reduce){.barra i{transition:none}}
</style>

<div class="wrap">
  <header>
    <div class="marca">Custo Oculto · gravação</div>
    <div class="tabs" id="tabs" role="group" aria-label="Projeto"></div>
    <h1 id="titulo"></h1>
    <p class="angulo" id="angulo"></p>
  </header>

  <section class="envio" aria-label="Como enviar">
    <ol class="passos">
      <li><b>Grave cada bloco</b><span>Um arquivo por bloco, com o nome indicado (mp3, wav ou m4a).</span></li>
      <li><b>Suba todos de uma vez</b><span>Arraste os arquivos na página do GitHub e clique em Commit changes.</span></li>
      <li><b>Baixe o vídeo</b><span>Em uns 20 a 30 minutos, o pacote aparece em Artifacts na execução mais recente.</span></li>
    </ol>
    <div class="acoes">
      <a class="btn prim" id="subir" target="_blank" rel="noopener">Subir áudios no GitHub ↗</a>
      <a class="btn" id="baixar" target="_blank" rel="noopener">Ver gerações e baixar ↗</a>
    </div>
    <div class="progresso" id="prog"></div>
    <div class="barra" aria-hidden="true"><i id="barra"></i></div>
  </section>

  <section class="blocos" id="blocos" aria-label="Blocos de narração"></section>
  <p class="nota">Leia o texto como está escrito. A fábrica compara o áudio com estas palavras para encaixar legenda e cenas; trocar uma palavra ou outra não atrapalha.</p>
</div>

<script>
const DADOS = """ + DADOS + """;
const $ = (id) => document.getElementById(id);
const ler = (k, d) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } };
const gravar = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
let atual = DADOS.projetos[0].id; // o roteiro mais novo abre primeiro
if (!DADOS.projetos.some((p) => p.id === atual)) atual = DADOS.projetos[0].id;

function tempo(txt) { const s = Math.round(txt.length / 15); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); }

function render() {
  const p = DADOS.projetos.find((x) => x.id === atual);
  const feitos = ler("co_feitos_" + p.id, {});
  $("tabs").replaceChildren(...DADOS.projetos.map((x) => {
    const b = document.createElement("button"); b.type = "button"; b.textContent = x.titulo;
    b.setAttribute("aria-pressed", x.id === atual); b.onclick = () => { atual = x.id; gravar("co_projeto", atual); render(); }; return b;
  }));
  $("titulo").textContent = p.titulo; $("angulo").textContent = p.angulo;
  $("subir").href = "https://github.com/" + DADOS.repo + "/upload/main/projetos/" + p.id + "/audio";
  $("baixar").href = "https://github.com/" + DADOS.repo + "/actions/workflows/gerar.yml";
  const total = p.blocos.length, n = p.blocos.filter((b) => feitos[b.arquivo]).length;
  const longo = p.blocos.filter((b) => b.tipo === "Longo").reduce((s, b) => s + b.texto.length, 0);
  $("prog").textContent = n + " de " + total + " gravados · longo com uns " + tempo(" ".repeat(longo)) + " de fala";
  $("barra").style.width = (100 * n / total) + "%";
  $("blocos").replaceChildren(...p.blocos.map((b) => {
    const el = document.createElement("article"); el.className = "bloco" + (feitos[b.arquivo] ? " ok" : "");
    el.innerHTML = '<div class="topo"><span class="arq"></span><span class="tipo"></span><span class="titulo"></span><span class="meta"></span></div>' +
      '<p class="texto"></p><div class="rodape"><button type="button" class="copiar">Copiar texto</button>' +
      '<label class="feito"><input type="checkbox"> Gravei</label></div>';
    el.querySelector(".arq").textContent = b.arquivo + ".mp3";
    el.querySelector(".tipo").textContent = b.tipo;
    el.querySelector(".titulo").textContent = b.titulo;
    el.querySelector(".meta").textContent = "~" + tempo(b.texto) + " · " + b.texto.length + " caracteres";
    const t = el.querySelector(".texto"); t.textContent = b.texto;
    const cp = el.querySelector(".copiar");
    cp.onclick = () => {
      const ok = () => { cp.textContent = "Copiado"; setTimeout(() => (cp.textContent = "Copiar texto"), 1600); };
      const sel = () => { const r = document.createRange(); r.selectNodeContents(t); const s = getSelection(); s.removeAllRanges(); s.addRange(r); cp.textContent = "Selecionado, use Ctrl+C"; };
      try { navigator.clipboard.writeText(b.texto).then(ok, sel); } catch (e) { sel(); }
    };
    const cb = el.querySelector("input"); cb.id = "feito_" + p.id + "_" + b.arquivo; cb.checked = !!feitos[b.arquivo];
    cb.onchange = () => { const f = ler("co_feitos_" + p.id, {}); f[b.arquivo] = cb.checked; gravar("co_feitos_" + p.id, f); render(); };
    return el;
  }));
}
render();
</script>""")

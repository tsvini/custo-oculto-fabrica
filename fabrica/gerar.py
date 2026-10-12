"""Fábrica Custo Oculto: roteiro (JSON) -> vídeo pronto para o YouTube.

Uso:
  python -m fabrica.gerar kolynos                 # longo + todos os Shorts
  python -m fabrica.gerar kolynos --formato longo
  python -m fabrica.gerar kolynos --formato short1
  python -m fabrica.gerar kolynos --modo teste    # voz falsa, sem gastar nada (testa a montagem)
"""
import argparse, base64, copy, functools, http.server, json, os, re, shutil, subprocess, sys, threading, time

from . import midia as M
from .tts import Narrador, ErroVoz

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def log(*a):
    print(*a, flush=True)


def slugify(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower() or "video"


class _H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query); nome = os.path.basename(q.get("name", ["saida.bin"])[0])
        n = int(self.headers.get("Content-Length", 0)); dest = os.path.join(self.server.upload_dir, nome)
        with open(dest, "wb") as f:
            rest = n
            while rest > 0:
                b = self.rfile.read(min(rest, 1 << 20))
                if not b:
                    break
                f.write(b); rest -= len(b)
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")


def servidor(raiz, upload_dir):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_H, directory=raiz))
    srv.upload_dir = upload_dir
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def frases(grupo):
    return [s for s in grupo["sentences"] if s.get("text") and s["text"].strip()]


def todas_cenas(p):
    out = []
    for g in p["script"]["long"]["parts"] + p["script"].get("shorts", []):
        for s in g["sentences"]:
            sc = s.get("scene") or {}
            out.append(sc)
            if isinstance(sc.get("fallback"), dict):
                pass
    return out


def ffmpeg_final(bruto, final, codec):
    v = ["-c:v", "copy"] if codec.startswith("avc") else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", bruto, *v, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("projeto", help="nome da pasta em projetos/ (ex.: kolynos)")
    ap.add_argument("--formato", default="tudo", help="tudo | longo | shorts | short1, short2…")
    ap.add_argument("--modo", default=None, help="edge | google | teste (padrão: google se houver GOOGLE_TTS_KEY, senão edge)")
    ap.add_argument("--voz", default=None, help="troca a voz deste vídeo (ex.: pt-BR-Chirp3-HD-Orus)")
    ap.add_argument("--saida", default=os.path.join(RAIZ, "saida"))
    ap.add_argument("--previas", action="store_true", help="salva quadros de prévia em JPG")
    a = ap.parse_args()

    pasta_proj = os.path.join(RAIZ, "projetos", a.projeto)
    with open(os.path.join(pasta_proj, "projeto.json"), encoding="utf8") as f:
        p = json.load(f)
    slug = slugify(p.get("slug") or a.projeto)
    trab = os.path.join(RAIZ, "trabalho", slug); os.makedirs(trab, exist_ok=True)
    pasta_midia = os.path.join(trab, "midia"); os.makedirs(pasta_midia, exist_ok=True)
    if os.path.isdir(os.path.join(pasta_proj, "midia")):  # mídia enviada à mão tem prioridade
        for fn in os.listdir(os.path.join(pasta_proj, "midia")):
            shutil.copy2(os.path.join(pasta_proj, "midia", fn), os.path.join(pasta_midia, fn))
    saida = os.path.join(a.saida, slug); os.makedirs(saida, exist_ok=True)
    resumo = [f"# {p.get('title', slug)}", ""]; avisos = []

    # ---------- o que gerar ----------
    shorts = p["script"].get("shorts", [])
    alvos = []
    if a.formato in ("tudo", "longo"):
        alvos.append(("longo", 0))
    if a.formato in ("tudo", "shorts"):
        alvos += [("short", i) for i in range(len(shorts))]
    m = re.fullmatch(r"short(\d+)", a.formato)
    if m:
        alvos.append(("short", int(m.group(1)) - 1))

    # ---------- mídia ----------
    log("1/4 Mídia")
    cenas = todas_cenas(p); creditos = []
    M.prints([s for s in cenas if s.get("type") == "print"], pasta_midia, log)
    chaves_longo = {s.get("media") for g in p["script"]["long"]["parts"] for s in (x.get("scene") or {} for x in g["sentences"])}
    M.pexels([s for s in cenas if s.get("media") in chaves_longo], pasta_midia, False, log, creditos)
    M.pexels([s for s in cenas if s.get("media") not in chaves_longo], pasta_midia, True, log, creditos)
    with open(os.path.join(trab, "projeto_render.json"), "w", encoding="utf8") as f:
        json.dump(p, f, ensure_ascii=False)
    man = M.manifesto(pasta_midia)

    # ---------- narração ----------
    voz = dict(p.get("voz") or {})
    if a.voz:
        voz["nome"] = a.voz
    nar = Narrador(voz, a.modo)
    log(f"2/4 Narração ({nar.modo}, voz {nar.voz['nome']})")
    if nar.modo == "teste":
        avisos.append("Gerado em MODO TESTE: a voz é um ruído no ritmo da fala, só para conferir a montagem.")
    cfgs = []
    for fmt, idx in alvos:
        grupos = p["script"]["long"]["parts"] if fmt == "longo" else [shorts[idx]]
        partes = []
        for k, g in enumerate(grupos):
            wav = os.path.join(trab, f"voz_{fmt}{idx + 1 if fmt == 'short' else ''}_p{k + 1}.wav")
            tempos, dur = nar.parte([s["text"].strip() for s in frases(g)], wav)
            partes.append({"wav": "/" + os.path.relpath(wav, RAIZ), "tempos": tempos})
            log(f"  {fmt}{'' if fmt == 'longo' else idx + 1} parte {k + 1}: {dur:.1f}s")
        nome = f"{slug}_longo" if fmt == "longo" else f"{slug}_short{idx + 1}"
        cfgs.append((fmt, idx, nome, {"projeto": "/" + os.path.relpath(os.path.join(trab, "projeto_render.json"), RAIZ), "formato": fmt, "idx": idx,
                                      "partes": partes, "midia": man, "midiaBase": "/" + os.path.relpath(pasta_midia, RAIZ) + "/",
                                      "saida": nome + ".bruto", "previas": [0.02, 0.15, 0.3, 0.5, 0.7, 0.9] if a.previas else None}))
    log(f"  caracteres cobrados agora: {nar.chars} · frases reaproveitadas do cache: {nar.cache_hits}")

    # ---------- vídeo ----------
    log("3/4 Vídeo")
    from playwright.sync_api import sync_playwright
    srv, base = servidor(RAIZ, trab)
    try:
        with sync_playwright() as pw:
            canal = os.environ.get("CHROME_CHANNEL") or None
            args = ["--autoplay-policy=no-user-gesture-required", "--disable-gpu-sandbox"]
            try:
                b = pw.chromium.launch(channel=canal, args=args)
            except Exception as e:
                log(f"  Chrome '{canal}' indisponível ({str(e)[:80]}), usando Chromium")
                b = pw.chromium.launch(args=args)
            pg = b.new_page(); pg.set_default_timeout(0)
            pg.on("console", lambda msg: msg.text.startswith("progresso") and log("   ", msg.text))
            pg.on("pageerror", lambda e: log("   erro na página:", e))
            pg.goto(base + "/motor/render.html")
            for fmt, idx, nome, cfg in cfgs:
                log(f"  gerando {nome}…")
                r = pg.evaluate("cfg => gerar(cfg)", cfg)
                bruto = os.path.join(trab, cfg["saida"]); final = os.path.join(saida, nome + ".mp4")
                ffmpeg_final(bruto, final, r["codec"]); os.remove(bruto)
                with open(os.path.join(saida, nome + ".srt"), "w", encoding="utf8") as f:
                    f.write(r["srt"])
                mb = os.path.getsize(final) / 1048576
                log(f"  {nome}.mp4 pronto: {int(r['total'] // 60)}:{int(r['total'] % 60):02d}, {mb:.0f} MB, {r['segundos']:.0f}s de render ({r['codec']})")
                resumo.append(f"- **{nome}.mp4** — {int(r['total'] // 60)}:{int(r['total'] % 60):02d} · {mb:.0f} MB")
                if fmt == "longo":
                    cap = r["capitulos"]
                    with open(os.path.join(saida, "capitulos.txt"), "w", encoding="utf8") as f:
                        f.write(cap + "\n")
                    meta = p.get("meta") or {}
                    desc = (meta.get("description") or "").replace("[CAPÍTULOS]", cap)
                    if creditos:
                        desc += "\n\nImagens de apoio: " + "; ".join(dict.fromkeys(creditos))
                    txt = ["TÍTULO (opções):"] + [f"  {t}" for t in meta.get("titles", [])] + ["", "DESCRIÇÃO:", desc, "", "TAGS:", ", ".join(meta.get("tags", []))]
                    with open(os.path.join(saida, "publicar_longo.txt"), "w", encoding="utf8") as f:
                        f.write("\n".join(txt) + "\n")
                else:
                    sh = shorts[idx]
                    with open(os.path.join(saida, f"publicar_short{idx + 1}.txt"), "w", encoding="utf8") as f:
                        tags = " ".join("#" + re.sub(r"\W", "", t.title()) for t in (p.get("meta") or {}).get("tags", [])[:4])
                        f.write(f"TÍTULO:\n  {sh.get('title', '')} #shorts\n\nDESCRIÇÃO:\n{sh.get('description') or 'A história completa está no vídeo longo do canal.'}\n\n#shorts {tags}\n")
                for i, d in enumerate(r.get("previas") or []):
                    with open(os.path.join(saida, f"previa_{nome}_{i}.jpg"), "wb") as f:
                        f.write(base64.b64decode(d.split(",")[1]))
            # ---------- miniaturas ----------
            for i, th in enumerate(p.get("thumbs") or []):
                d = pg.evaluate("cfg => miniatura(cfg)", th)
                with open(os.path.join(saida, f"miniatura_{'ABCDEFG'[i]}.jpg"), "wb") as f:
                    f.write(base64.b64decode(d.split(",")[1]))
            b.close()
    finally:
        srv.shutdown()

    log("4/4 Pronto")
    resumo += ["", f"Voz: {nar.voz['nome']} ({nar.modo}) · caracteres cobrados: {nar.chars} · frases do cache: {nar.cache_hits}"]
    sem = [s.get("media") for s in cenas if s.get("type") in ("print", "video", "image") and s.get("media") and s["media"] not in man]
    if sem:
        resumo.append(f"Cenas sem mídia (usaram manchete/texto de reserva): {', '.join(dict.fromkeys(sem))}")
    resumo += [f"⚠️ {x}" for x in avisos]
    with open(os.path.join(saida, "resumo.md"), "w", encoding="utf8") as f:
        f.write("\n".join(resumo) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf8") as f:
            f.write("\n".join(resumo) + "\n")
    log("\n".join(resumo))


if __name__ == "__main__":
    try:
        main()
    except ErroVoz as e:
        log("ERRO NA VOZ:", e); sys.exit(2)

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
from .canais import canal as canal_de, bloco_afiliados

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


def montar_serie(p):
    """Série do TikTok: o longo cortado em episódios verticais (>1 min) com a narração já gravada.
    projeto.json → "serie": [{"partes": [1, 2], "capa": {...cena capa...}, "caption": "...", "hashtags": [...]}, …]"""
    import copy
    out = []
    eps = p.get("serie") or []
    for i, ep in enumerate(eps):
        grupos = [copy.deepcopy(p["script"]["long"]["parts"][k - 1]) for k in ep["partes"]]
        if ep.get("capa"):
            prim = next(s for s in grupos[0]["sentences"] if s.get("text") and s["text"].strip())
            orig = prim.get("scene") or {}
            prim["scene"] = dict(ep["capa"], type="capa")
            if orig.get("type") not in (None, "same", "capa"):
                prim["scene"]["depois"] = orig  # depois de ~1.3s volta para a cena original da frase
        fim = ep.get("fim") or (["CONTINUA NA", f"PARTE {i + 2}"] if i + 1 < len(eps) else ["FIM DA SÉRIE", "SEGUE PRO PRÓXIMO CASO"])
        out.append({"parts": grupos, "fim": fim})
    p["script"]["serie"] = out


def todas_cenas(p):
    out = []
    serie = [g for ep in p["script"].get("serie", []) for g in ep["parts"]]
    for g in p["script"]["long"]["parts"] + p["script"].get("shorts", []) + p["script"].get("tiktoks", []) + serie:
        for s in g["sentences"]:
            sc = s.get("scene") or {}
            for cena in (sc, sc.get("depois") if isinstance(sc.get("depois"), dict) else None):  # "depois" da capa também baixa a sua mídia
                if not cena:
                    continue
                out.append(cena)
                if cena.get("type") == "montagem":
                    out += [x for x in cena.get("clips", []) if isinstance(x, dict)]  # cada clipe da montagem baixa a sua mídia
            out += [x for x in sc.get("extra", []) if isinstance(x, dict)]  # mídia usada só de fundo (capa/carimbo com vídeo)
            if sc.get("type") == "recorte" and isinstance(sc.get("cena"), dict):
                out.append(sc["cena"])  # a cena de dentro do recorte também precisa da sua mídia (prints do site)
            if isinstance(sc.get("fallback"), dict):
                pass
    return out


def ffmpeg_final(bruto, final, codec):
    v = ["-c:v", "copy"] if codec.startswith("avc") else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", bruto, *v, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final]
    subprocess.run(cmd, check=True)


def render_miniaturas(pg, p, man, midia_base, saida):
    """Miniaturas do longo. 'thumbs_capa' (capa com foto, estilo dos Shorts) tem prioridade sobre 'thumbs'."""
    from PIL import Image
    feitas = []
    for i, cena in enumerate(p.get("thumbs_capa") or []):
        d = pg.evaluate("cfg => capa(cfg)", {"cena": cena, "midia": man, "midiaBase": midia_base, "vertical": False})
        feitas.append(d)
    if not feitas:
        feitas = [pg.evaluate("cfg => miniatura(cfg)", th) for th in (p.get("thumbs") or [])]
    for i, d in enumerate(feitas):
        arq = os.path.join(saida, f"miniatura_{'ABCDEFG'[i]}.jpg")
        with open(arq, "wb") as f:
            f.write(base64.b64decode(d.split(",")[1]))
        im = Image.open(arq).convert("RGB"); im.thumbnail((1280, 720)); im.save(arq, quality=88)  # limite de 2 MB do YouTube


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("projeto", help="nome da pasta em projetos/ (ex.: kolynos)")
    ap.add_argument("--formato", default="tudo", help="tudo | longo | shorts | short1… | tiktoks | tiktok1…")
    ap.add_argument("--modo", default=None, help="gravada | kokoro | google | edge | teste (padrão: gravada se houver projetos/<nome>/audio, senão kokoro)")
    ap.add_argument("--voz", default=None, help="troca a voz deste vídeo (ex.: pt-BR-Chirp3-HD-Orus)")
    ap.add_argument("--saida", default=os.path.join(RAIZ, "saida"))
    ap.add_argument("--previas", action="store_true", help="salva quadros de prévia em JPG")
    a = ap.parse_args()

    pasta_proj = os.path.join(RAIZ, "projetos", a.projeto)
    with open(os.path.join(pasta_proj, "projeto.json"), encoding="utf8") as f:
        p = json.load(f)
    montar_serie(p)
    idioma = (p.get("idioma") or "pt").lower()[:2]; C = canal_de(idioma)
    os.environ["IDIOMA_FALA"] = C["whisper"]  # reconhecimento de fala no idioma do vídeo
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
    if a.formato in ("tudo", "longo") and p["script"]["long"]["parts"]:  # projeto só de shorts não tem longo
        alvos.append(("longo", 0))
    if a.formato in ("tudo", "shorts"):
        alvos += [("short", i) for i in range(len(shorts))]
    tiktoks = p["script"].get("tiktoks", [])
    if a.formato in ("tudo", "tiktoks"):
        alvos += [("tiktok", i) for i in range(len(tiktoks))]
    serie = p["script"]["serie"]
    if a.formato in ("tudo", "serie"):
        alvos += [("serie", i) for i in range(len(serie))]
    m = re.fullmatch(r"(short|tiktok|serie)(\d+)", a.formato)
    if m:
        alvos.append((m.group(1), int(m.group(2)) - 1))

    # ---------- mídia ----------
    log("1/4 Mídia")
    cenas = todas_cenas(p); creditos = []
    if a.formato == "miniaturas":  # só refaz as miniaturas do longo (e aplica no vídeo já publicado)
        M.wikimedia([sc for sc in cenas if sc.get("wiki")], pasta_midia, log, creditos, {})
        M.logos(p, pasta_midia, log)
        man = M.manifesto(pasta_midia)
        from playwright.sync_api import sync_playwright
        srv, base = servidor(RAIZ, trab)
        try:
            with sync_playwright() as pw:
                b = pw.chromium.launch(channel=os.environ.get("CHROME_CHANNEL") or None)
                pg = b.new_page(); pg.goto(base + "/motor/render.html")
                render_miniaturas(pg, p, man, "/" + os.path.relpath(pasta_midia, RAIZ) + "/", saida)
                b.close()
        finally:
            srv.shutdown()
        with open(os.path.join(saida, f"youtube_{slug}_longo.json"), "w", encoding="utf8") as f:
            json.dump({"tipo": "longo", "miniatura": "miniatura_A.jpg"}, f)
        log("miniaturas prontas"); return
    if a.formato == "candidatos":  # só mostra opções de clipe para escolher a dedo
        M.candidatos(cenas, os.path.join(RAIZ, "previas"), log)
        return
    M.prints([s for s in cenas if s.get("type") == "print"], pasta_midia, log)
    M.telas(cenas, pasta_midia, log, idioma)
    chaves_longo = {s.get("media") for g in p["script"]["long"]["parts"] for s in (x.get("scene") or {} for x in g["sentences"])}
    M.pexels([s for s in cenas if s.get("media") in chaves_longo], pasta_midia, False, log, creditos)
    M.pexels([s for s in cenas if s.get("media") not in chaves_longo], pasta_midia, True, log, creditos)
    with open(os.path.join(trab, "projeto_render.json"), "w", encoding="utf8") as f:
        json.dump(p, f, ensure_ascii=False)
    cred_arq = {}
    M.ia_imagens(p.get("ia") or {}, pasta_midia, not p["script"]["long"]["parts"], log, os.path.join(RAIZ, "previas", f"ia_{slug}_"))
    M.wikimedia([s for s in cenas if s.get("wiki")], pasta_midia, log, creditos, cred_arq)
    M.logos(p, pasta_midia, log)
    man = M.manifesto(pasta_midia)
    for k, v in man.items():
        if k in cred_arq:
            v["credit"] = cred_arq[k]

    # ---------- narração ----------
    from . import alinhar as AL
    pasta_audio = os.path.join(pasta_proj, "audio")
    def audio_de(fmt, idx, k):
        if fmt == "serie":
            return AL.achar_audio(pasta_audio, f"parte{p['serie'][idx]['partes'][k]}")
        return AL.achar_audio(pasta_audio, f"parte{k + 1}" if fmt == "longo" else f"{fmt}{idx + 1}")
    gravada = a.modo in (None, "gravada") and os.path.isdir(pasta_audio) and any(f.lower().endswith(AL.EXTS) for f in os.listdir(pasta_audio))
    if gravada:
        a.modo = "teste"  # o sintetizador não é usado
        ok = []
        for fmt, idx in alvos:
            n = len(p["script"]["long"]["parts"]) if fmt == "longo" else len(serie[idx]["parts"]) if fmt == "serie" else 1
            faltam = [k + 1 for k in range(n) if not audio_de(fmt, idx, k)]
            if faltam:
                nome_alvo = "longo" if fmt == "longo" else f"{fmt}{idx + 1}"
                arqs = ", ".join(f"parte{k}" for k in faltam) if fmt == "longo" else nome_alvo
                avisos.append(f"{nome_alvo}: pulado, falta o áudio ({arqs}) em projetos/{a.projeto}/audio/")
                log(f"  {nome_alvo}: pulado, falta {arqs}")
            else:
                ok.append((fmt, idx))
        alvos = ok
        if not alvos:
            raise ErroVoz(f"nenhum vídeo com todos os áudios. Envie parte1…parte{len(p['script']['long']['parts'])} (longo) e/ou short1, short2… em projetos/{a.projeto}/audio/")
    elif a.modo in (None, "gravada"):
        raise ErroVoz(f"não achei áudios em projetos/{a.projeto}/audio/. Envie parte1.mp3…parte{len(p['script']['long']['parts'])}.mp3 (longo) e short1.mp3… (Shorts). Para testar a montagem sem voz, rode com modo 'teste'.")
    voz = dict(p.get("voz") or {})
    if a.voz:
        voz["nome"] = a.voz
    nar = Narrador(voz, a.modo)
    log(f"2/4 Narração ({'gravada (seus áudios)' if gravada else nar.modo + ', voz ' + nar.voz['nome']})")
    if nar.modo == "teste" and not gravada:
        avisos.append("Gerado em MODO TESTE: a voz é um ruído no ritmo da fala, só para conferir a montagem.")
    cfgs = []; taxas = []
    for fmt, idx in alvos:
        grupos = p["script"]["long"]["parts"] if fmt == "longo" else serie[idx]["parts"] if fmt == "serie" else [(tiktoks if fmt == "tiktok" else shorts)[idx]]
        partes = []
        for k, g in enumerate(grupos):
            wav = os.path.join(trab, f"voz_{fmt}{idx + 1 if fmt != 'longo' else ''}_p{k + 1}.wav")
            txts = [s["text"].strip() for s in frases(g)]
            if gravada:
                tempos, dur, taxa, palavras = AL.parte(txts, audio_de(fmt, idx, k), wav, log)
                taxas.append(f"{fmt}{'' if fmt == 'longo' else idx + 1} p{k + 1}: {taxa:.0%} ({dur:.0f}s)")
                if taxa < 0.6:
                    avisos.append(f"{fmt}{'' if fmt == 'longo' else idx + 1} parte {k + 1}: só {taxa:.0%} das palavras bateram com o roteiro. Confira se o áudio é dessa parte e se o texto não mudou.")
            else:
                tempos, dur = nar.parte(txts, wav); palavras = None
            partes.append({"wav": "/" + os.path.relpath(wav, RAIZ), "tempos": tempos, "palavras": palavras})
            log(f"  {fmt}{'' if fmt == 'longo' else idx + 1} parte {k + 1}: {dur:.1f}s")
        nome = f"{slug}_longo" if fmt == "longo" else f"{slug}_{fmt}{idx + 1}"
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
            diag = []
            pg.on("console", lambda msg: (log("   ", msg.text) if msg.text.startswith("progresso") else diag.append(msg.text[:300])))
            pg.on("pageerror", lambda e: (log("   erro na página:", e), diag.append("pageerror: " + str(e)[:300])))
            pg.goto(base + "/motor/render.html")
            for fmt, idx, nome, cfg in cfgs:
                log(f"  gerando {nome}…")
                try:
                    r = pg.evaluate("cfg => gerar(cfg)", cfg)
                except Exception:
                    print("::warning title=Console do render::" + " | ".join(diag[-25:]).replace("\n", " ")[:3500], flush=True)
                    raise
                bruto = os.path.join(trab, cfg["saida"]); final = os.path.join(saida, nome + ".mp4")
                ffmpeg_final(bruto, final, r["codec"]); os.remove(bruto)
                if r.get("eventosSom"):  # sonoplastia com sons reais (Freesound) e avaliação por IA (Gemini)
                    from . import sonoplastia
                    with open(os.path.join(RAIZ, "previas", f"eventos_{nome}.json"), "w", encoding="utf8") as fe:  # para refazer só o som depois
                        json.dump({"eventos": r["eventosSom"], "trilha": r.get("trilha"), "roteiro": r.get("roteiro", "")}, fe, ensure_ascii=False, indent=1)
                    import shutil; os.makedirs(os.path.join(RAIZ, "sem_som"), exist_ok=True); shutil.copy2(final, os.path.join(RAIZ, "sem_som", nome + "_sem_som.mp4"))
                    try:
                        sonoplastia.processar(final, r["eventosSom"], r.get("trilha"), r.get("roteiro", ""),
                                              os.path.join(RAIZ, "previas", f"som_{nome}.json"))
                    except Exception as e:
                        import traceback
                        print("::warning title=Sonoplastia falhou::" + traceback.format_exc()[-1200:].replace("\n", " | "), flush=True)
                elif r.get("sons") or r.get("trilha"):  # desenho de som simples: trilha com ducking + efeitos
                    from . import som
                    try:
                        som.mixar(final, r.get("sons"), r.get("trilha")); log(f"  som: trilha {r.get('trilha') or '-'}, {len(r.get('sons') or [])} efeitos")
                    except Exception as e:
                        log(f"  som: falhou ({str(e)[:160]})")
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
                    afil = bloco_afiliados(meta, idioma)
                    if afil:
                        desc = desc.replace("[AFILIADOS]", afil) if "[AFILIADOS]" in desc else desc + "\n\n" + afil
                    if C.get("spotify") and p.get("destino") != "curso":
                        desc += "\n\n" + C["spotify"]
                    if creditos:
                        desc += f"\n\n{C['creditos']} " + "; ".join(dict.fromkeys(creditos))
                    txt = ["TÍTULO (opções):"] + [f"  {t}" for t in meta.get("titles", [])] + ["", "DESCRIÇÃO:", desc, "", "TAGS:", ", ".join(meta.get("tags", []))]
                    with open(os.path.join(saida, "publicar_longo.txt"), "w", encoding="utf8") as f:
                        f.write("\n".join(txt) + "\n")
                    # podcast: o mesmo episódio em MP3 (padrão de podcast: -16 LUFS) + texto do episódio
                    try:
                        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vn", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                                        "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "128k", os.path.join(saida, f"podcast_{slug}.mp3")], check=True)
                        canal_url = "https://www.youtube.com/@HiddenCostCases" if idioma == "en" else "https://www.youtube.com/@Custo-Oculto-YT"
                        ver = "Watch it with images and documents on YouTube" if idioma == "en" else "Assista com imagens e documentos no YouTube"
                        with open(os.path.join(saida, "publicar_podcast.txt"), "w", encoding="utf8") as f:
                            f.write(f"TÍTULO DO EPISÓDIO:\n  {(meta.get('titles') or [p.get('title', slug)])[0]}\n\nDESCRIÇÃO:\n{desc}\n\n{ver}: {canal_url}\n")
                        resumo.append(f"- **podcast_{slug}.mp3** — episódio de podcast (Spotify: suba o MP4 para versão em vídeo ou este MP3 para só áudio)")
                    except Exception as e:
                        avisos.append(f"podcast: não consegui gerar o MP3 ({str(e)[:120]})")
                    yt = {"tipo": "longo", "caso": slug, "caso_titulo": p.get("title", slug), "video": nome + ".mp4", "legenda": nome + ".srt", "miniatura": "miniatura_A.jpg",
                          "titulo": (meta.get("titles") or [p.get("title", slug)])[0][:100], "descricao": desc[:4900], "tags": meta.get("tags", []), "idioma": idioma}
                    with open(os.path.join(saida if (gravada or nar.modo != "teste") else trab, f"youtube_{nome}.json"), "w", encoding="utf8") as f:
                        json.dump(yt, f, ensure_ascii=False, indent=1)
                elif fmt == "serie":
                    ep = p["serie"][idx]
                    with open(os.path.join(saida, f"publicar_serie{idx + 1}.txt"), "w", encoding="utf8") as f:
                        f.write(f"LEGENDA DO POST:\n{ep.get('caption', '')}\n\n{' '.join(ep.get('hashtags') or [])}\n")
                    cena0 = dict(ep["capa"], type="capa") if ep.get("capa") else None
                    if cena0:
                        d = pg.evaluate("cfg => capa(cfg)", {"cena": cena0, "midia": man, "midiaBase": cfg["midiaBase"], "vertical": True})
                        with open(os.path.join(saida, f"capa_serie{idx + 1}.jpg"), "wb") as f:
                            f.write(base64.b64decode(d.split(",")[1]))
                    if r["total"] < 61:
                        avisos.append(f"{nome}: {r['total']:.0f}s. O Programa de Recompensas do TikTok só conta vídeos com mais de 1 minuto.")
                    if r["total"] <= 180:  # Shorts aceitam até 3 min: a série também vai para o YouTube
                        tags = " ".join("#" + re.sub(r"\W", "", t.title()) for t in (p.get("meta") or {}).get("tags", [])[:3])
                        tot = len(p["serie"])
                        yt = {"tipo": "serie", "caso": slug, "video": nome + ".mp4", "miniatura": f"capa_serie{idx + 1}.jpg" if cena0 else None,
                              "titulo": ((f"{ep['titulo']} ({'part' if idioma == 'en' else 'parte'} {idx + 1})" if ep.get("titulo") else C["serie_titulo"].format(titulo=p.get('title', slug), n=idx + 1, tot=tot)) + " #shorts")[:100], "idioma": idioma,
                              "descricao": (ep.get("caption") or "") + "\n\n" + C["serie_desc"].format(tot=tot) + f"\n\n#shorts {tags}",
                              "tags": (p.get("meta") or {}).get("tags", [])}
                        with open(os.path.join(saida if (gravada or nar.modo != "teste") else trab, f"youtube_{nome}.json"), "w", encoding="utf8") as f:
                            json.dump(yt, f, ensure_ascii=False, indent=1)
                elif fmt == "tiktok":
                    tk = tiktoks[idx]
                    with open(os.path.join(saida, f"publicar_tiktok{idx + 1}.txt"), "w", encoding="utf8") as f:
                        f.write(f"LEGENDA DO POST:\n{tk.get('caption') or tk.get('title', '')}\n\n{' '.join(tk.get('hashtags') or ['#historia', '#negocios', '#empresas', '#curiosidades'])}\n"
                                + (f"\nPRODUTO PARA MARCAR (TikTok Shop): {tk['produto']}\n" if tk.get("produto") else "")
                                + "\nAo postar: marque 'Conteúdo gerado por IA' só se usar voz sintética. Não use #shorts.\n")
                    usadas = [x.get("scene", {}) for x in tk["sentences"]]
                    cred = [man[k]["credit"] for k in dict.fromkeys((sc.get("media") or sc.get("foto")) for sc in usadas) if k in man and man[k].get("credit")]
                    if cred:
                        with open(os.path.join(saida, f"publicar_tiktok{idx + 1}.txt"), "a", encoding="utf8") as f:
                            f.write("\nCRÉDITOS DAS FOTOS (cole no fim da legenda):\n" + "\n".join(cred) + "\n")
                    cena0 = (tk["sentences"][0].get("scene") or {})
                    if cena0.get("type") == "capa":
                        d = pg.evaluate("cfg => capa(cfg)", {"cena": cena0, "midia": man, "midiaBase": cfg["midiaBase"], "vertical": True})
                        with open(os.path.join(saida, f"capa_tiktok{idx + 1}.jpg"), "wb") as f:
                            f.write(base64.b64decode(d.split(",")[1]))
                    if r["total"] < 61:
                        avisos.append(f"{nome}: {r['total']:.0f}s. O Programa de Recompensas do TikTok só conta vídeos com mais de 1 minuto.")
                else:
                    sh = shorts[idx]
                    with open(os.path.join(saida, f"publicar_short{idx + 1}.txt"), "w", encoding="utf8") as f:
                        tags = " ".join("#" + re.sub(r"\W", "", t.title()) for t in (p.get("meta") or {}).get("tags", [])[:4])
                        f.write(f"TÍTULO:\n  {sh.get('title', '')} #shorts\n\nDESCRIÇÃO:\n{sh.get('description') or C['shorts_desc']}\n\n#shorts {tags}\n")
                    cena0 = (sh["sentences"][0].get("scene") or {}); capa_arq = None
                    if cena0.get("type") == "capa":
                        d = pg.evaluate("cfg => capa(cfg)", {"cena": cena0, "midia": man, "midiaBase": cfg["midiaBase"], "vertical": True})
                        capa_arq = f"capa_short{idx + 1}.jpg"
                        with open(os.path.join(saida, capa_arq), "wb") as f:
                            f.write(base64.b64decode(d.split(",")[1]))
                    yt = {"tipo": "short", "caso": slug, "video": nome + ".mp4", "titulo": (sh.get("title", "") + " #shorts")[:100],
                          "descricao": (sh.get("description") or C["shorts_desc"]) + f"\n\n#shorts {tags}", "idioma": idioma,
                          "tags": (p.get("meta") or {}).get("tags", []), "miniatura": capa_arq}
                    with open(os.path.join(saida if (gravada or nar.modo != "teste") else trab, f"youtube_{nome}.json"), "w", encoding="utf8") as f:
                        json.dump(yt, f, ensure_ascii=False, indent=1)
                for i, d in enumerate(r.get("previas") or []):
                    with open(os.path.join(saida, f"previa_{nome}_{i}.jpg"), "wb") as f:
                        f.write(base64.b64decode(d.split(",")[1]))
            # ---------- capa do longo (estilo colagem) ----------
            if p.get("capa_longo") and cfgs:
                d = pg.evaluate("cfg => capa(cfg)", {"cena": dict(p["capa_longo"], type="capa"), "midia": man, "midiaBase": cfgs[0][3]["midiaBase"], "vertical": False})
                with open(os.path.join(saida, "miniatura_capa.jpg"), "wb") as f:
                    f.write(base64.b64decode(d.split(",")[1]))
            # ---------- miniaturas ----------
            render_miniaturas(pg, p, man, "/" + os.path.relpath(pasta_midia, RAIZ) + "/", saida)
            b.close()
    finally:
        srv.shutdown()

    log("4/4 Pronto")
    resumo += ["", "Voz: gravada (seus áudios)" if gravada else f"Voz: {nar.voz['nome']} ({nar.modo}) · caracteres cobrados: {nar.chars} · frases do cache: {nar.cache_hits}"]
    sem = [s.get("media") for s in cenas if s.get("type") in ("print", "video", "image") and s.get("media") and s["media"] not in man]
    if sem:
        resumo.append(f"Cenas sem mídia (usaram manchete/texto de reserva): {', '.join(dict.fromkeys(sem))}")
        print(f"::warning title=Cenas sem imagem::{', '.join(dict.fromkeys(sem))}", flush=True)  # checagem automática: não depende de olhar o vídeo
    if p.get("destino") == "curso":  # aula de curso: não vai para YouTube nem podcast
        import glob as _g
        for f in _g.glob(os.path.join(saida, "youtube_*.json")) + _g.glob(os.path.join(saida, "podcast_*.mp3")) + _g.glob(os.path.join(saida, "publicar_*.txt")):
            os.remove(f)
        resumo.append("- aula de curso: só o MP4 e a legenda, sem publicação")
    resumo += [f"⚠️ {x}" for x in avisos]
    if taxas:
        print("::notice title=Sincronia (palavras que bateram)::" + " · ".join(taxas), flush=True)
    for x in avisos:
        print("::warning title=Aviso::" + x, flush=True)
    print("::notice title=Vídeos::" + " | ".join(r[2:] for r in resumo if r.startswith("- **")), flush=True)
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
        log("ERRO NA VOZ:", e)
        print("::error title=Erro na voz::" + str(e).replace("\n", " ")[:900], flush=True)
        sys.exit(2)
    except Exception as e:  # mostra o erro nas anotações do Actions (os logs completos nem sempre dá pra baixar)
        import traceback
        print("::error title=Erro ao gerar::" + traceback.format_exc()[-1500:].replace("\n", " | "), flush=True)
        raise

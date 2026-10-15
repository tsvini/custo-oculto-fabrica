"""Mídia automática: prints de manchete (Playwright) e clipes de apoio (Pexels).

Nada aqui é obrigatório: se um print ou clipe falhar, a cena usa a manchete desenhada
ou o texto animado de reserva, e o vídeo sai do mesmo jeito.
"""
import json, os, re, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
CONSENT = ["Aceitar e fechar", "Aceitar todos", "Aceitar tudo", "Aceitar", "Aceito", "Concordo", "Entendi", "Continuar", "Prosseguir", "OK", "Accept all", "Accept", "I agree", "Agree", "Got it"]

RUIM = re.compile(r"(not found|não encontrad|nao encontrad|error|erro 4|access denied|acesso negado|just a moment|attention required|verify you are human|captcha|assine|subscribe|forbidden)", re.I)

LIMPA_JS = r"""
() => {
  for (const el of Array.from(document.querySelectorAll('body *'))) {
    const cs = getComputedStyle(el);
    if (cs.position === 'fixed' || cs.position === 'sticky') el.remove();
  }
  document.querySelectorAll('iframe, [id*="cookie" i], [class*="cookie" i], [class*="consent" i], [id*="consent" i], [class*="paywall" i], [class*="newsletter" i], [class*="modal" i]').forEach(e => { try { e.remove(); } catch (_) {} });
  document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto';
}
"""

ACHA_JS = r"""
() => {
  const og = (document.querySelector('meta[property="og:title"]') || {}).content || '';
  const site = (document.querySelector('meta[property="og:site_name"]') || {}).content || '';
  const pub = (document.querySelector('meta[property="article:published_time"]') || {}).content || '';
  const hs = Array.from(document.querySelectorAll('h1')).filter(h => { const r = h.getBoundingClientRect(); return r.width > 200 && r.height > 20 && h.innerText.trim().length > 12; });
  let box = null, text = '';
  if (hs.length) {
    const h = hs[0]; h.scrollIntoView({block: 'center'}); const r = h.getBoundingClientRect();
    text = h.innerText.trim().replace(/\s+/g, ' ');
    let top = r.top, bottom = r.bottom;
    // inclui a linha fina (subtítulo) logo abaixo, se houver
    let n = h.nextElementSibling;
    for (let k = 0; n && k < 3; k++, n = n.nextElementSibling) {
      const rr = n.getBoundingClientRect(); const tag = n.tagName;
      if (rr.height > 0 && rr.top - bottom < 60 && /^(P|H2|DIV|SPAN)$/.test(tag) && n.innerText.trim().length > 20 && rr.height < 260) { bottom = rr.bottom; break; }
    }
    box = {x: r.left + window.scrollX, y: top + window.scrollY, w: r.width, h: bottom - top};
  }
  return {og, site, pub, text, box};
}
"""


def _baixa(url, dest, headers=None, timeout=60):
    req = urllib.request.Request(url, headers=dict({"User-Agent": UA}, **(headers or {})))
    with urllib.request.urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
        while True:
            b = r.read(1 << 16)
            if not b:
                break
            f.write(b)


def _normaliza_clipe(path, log=print):
    """Reconverte o clipe para H.264 (yuv420p, até 1920 px, 12 s, sem som): qualquer navegador decodifica."""
    import subprocess
    tmp = path + ".tmp.mp4"
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-t", "12", "-an",
                        "-vf", "scale='min(1920,iw)':-2:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "20", "-profile:v", "high", "-movflags", "+faststart", tmp], capture_output=True, text=True)
    if r.returncode == 0 and os.path.getsize(tmp) > 10000:
        os.replace(tmp, path)
    else:
        log(f"    não consegui converter {os.path.basename(path)}: {r.stderr[:150]}")
        if os.path.exists(tmp):
            os.remove(tmp)


def _uniforme(path):
    try:
        from PIL import Image, ImageStat
        im = Image.open(path).convert("L")
        return max(ImageStat.Stat(im).stddev) < 12
    except Exception:
        return True


def telas(cenas, pasta, log, idioma="pt"):
    """Cenas 'tela' com 'url': print da página inteira em 16:9 (para as aulas). 'alvo' = texto do botão/link a destacar:
    a caixa amarela e o zoom são calculados sozinhos e guardados em <media>.json."""
    alvo = [s for s in cenas if s.get("type") in ("tela", "runner", "devtools", "playground") and s.get("url") and s.get("media")]
    falta = [s for s in alvo if not os.path.exists(os.path.join(pasta, s["media"] + ".png")) or (s.get("inspecionar") and "elem" not in json.load(open(os.path.join(pasta, s["media"] + ".json"))) if os.path.exists(os.path.join(pasta, s["media"] + ".json")) else s.get("inspecionar"))]
    if falta:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            ctx = b.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=1.25, locale="en-US" if idioma == "en" else "pt-BR", user_agent=UA)
            for s in falta:
                dest = os.path.join(pasta, s["media"] + ".png"); pg = ctx.new_page(); meta = {}
                try:
                    pg.goto(s["url"], wait_until="domcontentloaded", timeout=35000); pg.wait_for_timeout(3000)
                    for txt in CONSENT:
                        try:
                            btn = pg.get_by_role("button", name=txt, exact=True)
                            if btn.count() and btn.first.is_visible():
                                btn.first.click(timeout=1500); pg.wait_for_timeout(600); break
                        except Exception:
                            pass
                    for ac in s.get("acoes") or []:  # passos antes do print: {"fill": [seletor, valor]} ou {"click": seletor}
                        try:
                            if ac.get("fill"):
                                pg.fill(ac["fill"][0], ac["fill"][1], timeout=8000)
                            elif ac.get("select"):
                                pg.select_option(ac["select"][0], ac["select"][1], timeout=8000); pg.wait_for_timeout(800)
                            elif ac.get("click"):
                                pg.click(ac["click"], timeout=8000); pg.wait_for_timeout(1200)
                        except Exception as e:
                            log(f"  tela {s['media']}: ação falhou ({str(e)[:80]})")
                    if s.get("inspecionar"):  # elemento real: posição e HTML (para DevTools / Selector Playground)
                        try:
                            el = pg.locator(s["inspecionar"]).first
                            bx = el.bounding_box()
                            if bx:
                                meta["elem"] = [bx["x"] / 1600, bx["y"] / 900, (bx["x"] + bx["width"]) / 1600, (bx["y"] + bx["height"]) / 900]
                                meta["elem_tam"] = [round(bx["width"]), round(bx["height"])]
                            info = el.evaluate("""e => ({tag: e.tagName.toLowerCase(), attrs: [...e.attributes].map(a => [a.name, a.value]),
                                pai: e.parentElement ? e.parentElement.tagName.toLowerCase() + (e.parentElement.className ? '.' + String(e.parentElement.className).split(' ')[0] : '') : '',
                                texto: (e.innerText || '').trim().slice(0, 30)})""")
                            meta["html"] = info
                        except Exception as e:
                            log(f"  tela {s['media']}: não achei {s['inspecionar']} ({str(e)[:60]})")
                    if s.get("alvo_css"):
                        try:
                            bx = pg.locator(s["alvo_css"]).first.bounding_box()
                            if bx:
                                x0, y0, x1, y1 = bx["x"] / 1600, bx["y"] / 900, (bx["x"] + bx["width"]) / 1600, (bx["y"] + bx["height"]) / 900
                                pad = 0.012; meta["caixa"] = [max(0, x0 - pad), max(0, y0 - pad * 1.8), min(1, x1 + pad), min(1, y1 + pad * 1.8)]
                                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; zw = 0.55
                                zx0 = min(max(0, cx - zw / 2), 1 - zw); zy0 = min(max(0, cy - zw / 2), 1 - zw); meta["zoom"] = [zx0, zy0, zx0 + zw, zy0 + zw]
                        except Exception as e:
                            log(f"  tela {s['media']}: não achei {s['alvo_css']} ({str(e)[:60]})")
                    if s.get("alvo"):
                        el = pg.get_by_text(s["alvo"], exact=False).locator("visible=true").first
                        try:
                            el.scroll_into_view_if_needed(timeout=3000); pg.wait_for_timeout(400)
                            bx = el.bounding_box()
                            if bx:
                                x0, y0, x1, y1 = bx["x"] / 1600, bx["y"] / 900, (bx["x"] + bx["width"]) / 1600, (bx["y"] + bx["height"]) / 900
                                pad = 0.012; meta["caixa"] = [max(0, x0 - pad), max(0, y0 - pad * 1.8), min(1, x1 + pad), min(1, y1 + pad * 1.8)]
                                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; zw = 0.55
                                zx0 = min(max(0, cx - zw / 2), 1 - zw); zy0 = min(max(0, cy - zw / 2), 1 - zw)
                                meta["zoom"] = [zx0, zy0, zx0 + zw, zy0 + zw]
                        except Exception as e:
                            log(f"  tela {s['media']}: não achei '{s['alvo']}' ({str(e)[:60]})")
                    pg.screenshot(path=dest)
                    json.dump(meta, open(os.path.join(pasta, s["media"] + ".json"), "w"))
                    log(f"  tela {s['media']}: ok ({s['url'][:60]})")
                except Exception as e:
                    log(f"  tela {s['media']}: falhou ({str(e)[:100]})")
                pg.close()
            b.close()
    for s in alvo:  # aplica caixa/zoom calculados (sem sobrescrever o que veio à mão)
        mj = os.path.join(pasta, s["media"] + ".json")
        if os.path.exists(mj):
            for k, v in json.load(open(mj)).items():
                s.setdefault(k, v)


def prints(cenas, pasta, log):
    """cenas: lista de dicts (cenas 'print' com 'url'). Salva <media>.png e preenche headline/outlet."""
    alvo = [s for s in cenas if s.get("url") and s.get("media") and not os.path.exists(os.path.join(pasta, s["media"] + ".png"))]
    if not alvo:
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1280, "height": 1000}, device_scale_factor=1.5, locale="pt-BR", user_agent=UA)
        for s in alvo:
            dest = os.path.join(pasta, s["media"] + ".png"); pg = ctx.new_page()
            try:
                resp = pg.goto(s["url"], wait_until="domcontentloaded", timeout=35000)
                if resp is not None and resp.status >= 400:
                    raise RuntimeError(f"site respondeu {resp.status}")
                pg.wait_for_timeout(2500)
                for txt in CONSENT:
                    try:
                        btn = pg.get_by_role("button", name=txt, exact=True)
                        if btn.count() and btn.first.is_visible():
                            btn.first.click(timeout=1500); pg.wait_for_timeout(600); break
                    except Exception:
                        pass
                pg.evaluate(LIMPA_JS); pg.wait_for_timeout(400)
                info = pg.evaluate(ACHA_JS)
                if RUIM.search(info.get("text") or "") or RUIM.search(pg.title() or ""):
                    raise RuntimeError("página de bloqueio/erro: " + (info.get("text") or pg.title())[:60])
                if not s.get("headline"):
                    s["headline"] = (info.get("text") or info.get("og") or "").strip()[:220] or None
                if not s.get("outlet") and info.get("site"):
                    s["outlet"] = info["site"]
                bx = info.get("box")
                if bx:
                    x = max(0, bx["x"] - 36); y = max(0, bx["y"] - 70)
                    w = min(1280 - x, max(bx["w"] + 72, 760)); h = min(bx["h"] + 120, 700)
                    pg.screenshot(path=dest, clip={"x": x, "y": y, "width": w, "height": h}, full_page=True)
                    if _uniforme(dest):
                        os.remove(dest); log(f"  print {s['media']}: imagem vazia, usando manchete desenhada")
                    else:
                        log(f"  print {s['media']}: ok ({s['url'][:60]})")
                else:
                    log(f"  print {s['media']}: título não encontrado, usando manchete desenhada")
            except Exception as e:
                log(f"  print {s['media']}: falhou ({str(e)[:120]}), usando manchete desenhada")
                if os.path.exists(dest) and _uniforme(dest):
                    os.remove(dest)
            finally:
                pg.close()
        b.close()


def pexels(cenas, pasta, vertical, log, creditos):
    key = os.environ.get("PEXELS_KEY", "").strip()
    alvo = {}; qen = {}
    for s in cenas:
        if s.get("type") == "video" and s.get("media") and s.get("search"):
            alvo.setdefault(s["media"], s["search"])
            if s.get("search_en"):
                qen.setdefault(s["media"], s["search_en"])
            if s.get("pixabay_id"):
                qen.setdefault("#" + s["media"], str(s["pixabay_id"]))
    pend = {k: q for k, q in alvo.items() if not os.path.exists(os.path.join(pasta, k + ".mp4"))}
    if not pend:
        return
    if not key:
        return pixabay(pend, pasta, vertical, log, creditos, qen)
    usados = set()
    for k, q in pend.items():
        try:
            url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
                {"query": q, "orientation": "portrait" if vertical else "landscape", "size": "medium", "per_page": 15, "locale": "pt-BR"})
            req = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                vids = json.load(r).get("videos", [])
            vids = [v for v in vids if v.get("duration", 0) >= 6 and v["id"] not in usados]
            if not vids:
                log(f"  clipe {k}: nada no Pexels para '{q}'"); continue
            v = vids[0]; usados.add(v["id"])
            arqs = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("width")]
            alvo_w = 1080 if vertical else 1920
            arqs.sort(key=lambda f: (abs(min(f["width"], f["height"]) - min(alvo_w, 1080)), -f["width"]))
            _baixa(arqs[0]["link"], os.path.join(pasta, k + ".mp4")); _normaliza_clipe(os.path.join(pasta, k + ".mp4"), log)
            nome = (v.get("user") or {}).get("name", "")
            creditos.append(f"{nome} (Pexels) – {v.get('url', '')}")
            log(f"  clipe {k}: ok ('{q}', {nome})")
        except Exception as e:
            log(f"  clipe {k}: falhou ({str(e)[:120]})")
    resto = {k: q for k, q in pend.items() if not os.path.exists(os.path.join(pasta, k + ".mp4"))}
    if resto:
        pixabay(resto, pasta, vertical, log, creditos, qen)


def pixabay(pend, pasta, vertical, log, creditos, qen=None):
    """Clipes do Pixabay (licença livre para uso comercial). Usa PIXABAY_KEY.
    qen: busca em inglês por chave (campo "search_en" da cena), que acha muito mais coisa."""
    qen = qen or {}
    key = os.environ.get("PIXABAY_KEY", "").strip()
    if not key:
        log(f"  sem PIXABAY_KEY/PEXELS_KEY: {len(pend)} clipe(s) usam o texto de reserva")
        return
    usados = set(); ok = 0
    for k, q in pend.items():
        try:
            hits = []
            if qen.get("#" + k):  # clipe escolhido a dedo
                url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "id": qen["#" + k]})
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                    hits = json.load(r).get("hits", [])
            for qq, lang in ((qen.get(k), "en"), (q, "pt")):
                if hits:
                    break
                if not qq:
                    continue
                url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
                    {"key": key, "q": qq[:100], "lang": lang, "per_page": 30, "safesearch": "true", "video_type": "film"})
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                    hits = [h for h in json.load(r).get("hits", []) if h.get("duration", 0) >= 4 and h["id"] not in usados]
                # relevância: as tags do vídeo precisam conter alguma palavra da busca
                pal = {w.lower() for w in re.findall(r"\w{4,}", qq)}
                hits = [h for h in hits if pal & {w.lower() for w in re.findall(r"\w{4,}", h.get("tags", ""))}]
            if not hits:
                log(f"  clipe {k}: nada no Pixabay para '{q}'"); continue
            def serve(h):  # prefere a orientação do formato e boa resolução
                v = h["videos"].get("large") or h["videos"].get("medium") or {}
                w, hh = v.get("width") or 0, v.get("height") or 0
                return ((hh > w) == vertical, min(w, hh) >= 720, h.get("likes", 0))
            hits.sort(key=serve, reverse=True)
            h = hits[0]; usados.add(h["id"])
            vs = h["videos"]
            alvo = 1080 if vertical else 1920
            opc = [v for v in (vs.get("large"), vs.get("medium"), vs.get("small")) if v and v.get("url")]
            opc.sort(key=lambda v: abs(max(v.get("width") or 0, v.get("height") or 0) - alvo))
            _baixa(opc[0]["url"], os.path.join(pasta, k + ".mp4")); _normaliza_clipe(os.path.join(pasta, k + ".mp4"), log)
            creditos.append(f"{h.get('user', '')} (Pixabay) – {h.get('pageURL', '')}")
            ok += 1; log(f"  clipe {k}: ok Pixabay ('{q}', {h.get('user', '')})")
        except Exception as e:
            log(f"  clipe {k}: Pixabay falhou ({str(e)[:120]})")
    print(f"::notice title=Clipes de apoio::{ok} de {len(pend)} clipes vieram do Pixabay", flush=True)


def manifesto(pasta):
    out = {}
    for f in sorted(os.listdir(pasta)) if os.path.isdir(pasta) else []:
        k, ext = os.path.splitext(f)
        if ext.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            out[k] = {"file": f, "kind": "img"}
        elif ext.lower() in (".mp4", ".webm", ".mov"):
            out[k] = {"file": f, "kind": "video"}
    return out


# ---------------- Fotos reais: Wikimedia Commons ----------------
# Só usa arquivos com licença livre (domínio público, CC0, CC BY, CC BY-SA) e guarda o crédito,
# que aparece pequeno na própria cena e vai para a descrição.
COMMONS = "https://commons.wikimedia.org/w/api.php"
UA_BOT = "CustoOcultoFabrica/1.0 (https://github.com/tsvini/custo-oculto-fabrica)"
LIVRE = re.compile(r"^(public domain|pd(?:[- ].*)?|cc0(?: 1\.0)?|cc[- ]by(?:[- ]sa)?(?:[- ]?[0-9.]+)?(?:[- ][a-z]{2})?)$", re.I)


def _limpa_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def _commons_busca(q, largura=2000):
    params = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": 20,
              "gsrsearch": q + " filetype:bitmap", "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
              "iiurlwidth": largura, "iiextmetadatafilter": "LicenseShortName|Artist|ImageDescription"}
    if q.lower().startswith("file:") or q.lower().startswith("arquivo:"):
        params = {"action": "query", "format": "json", "titles": "File:" + q.split(":", 1)[1], "prop": "imageinfo",
                  "iiprop": "url|size|mime|extmetadata", "iiurlwidth": largura, "iiextmetadatafilter": "LicenseShortName|Artist|ImageDescription"}
    url = COMMONS + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA_BOT})
    with urllib.request.urlopen(req, timeout=30) as r:
        pages = (json.load(r).get("query") or {}).get("pages") or {}
    out = []
    for pg in sorted(pages.values(), key=lambda x: x.get("index", 0)):
        ii = (pg.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata") or {}
        lic = _limpa_html((meta.get("LicenseShortName") or {}).get("value", ""))
        out.append({"title": pg.get("title", ""), "w": ii.get("width", 0), "h": ii.get("height", 0), "mime": ii.get("mime", ""),
                    "url": ii.get("thumburl") or ii.get("url"), "page": ii.get("descriptionurl", ""), "lic": lic,
                    "autor": _limpa_html((meta.get("Artist") or {}).get("value", ""))[:60]})
    return out


def wikimedia(cenas, pasta, log, creditos, creditos_arq):
    """Cenas com 'wiki': termo de busca (ou 'File:Nome.jpg'). Baixa a foto para <media>.jpg."""
    feitas = {}
    for s in cenas:
        q, k = s.get("wiki"), s.get("media") or s.get("foto")
        if not q or not k or k in feitas:
            continue
        feitas[k] = True
        dest = os.path.join(pasta, k + ".jpg")
        if any(os.path.exists(os.path.join(pasta, k + e)) for e in (".jpg", ".png", ".jpeg", ".webp")):
            continue
        termos = q if isinstance(q, list) else [q]
        achou = False
        for termo in termos:
            try:
                res = _commons_busca(termo)
            except Exception as e:
                log(f"  foto {k}: busca falhou ({str(e)[:100]})"); continue
            palavras = [w.lower() for w in re.findall(r"\w{4,}", termo) if w.lower() not in ("file", "arquivo")]
            bons = [r for r in res if r["mime"] == "image/jpeg" and r["w"] >= 800
                    and sum(w in r["title"].lower() for w in palavras) >= max(1, len(palavras) // 2)
                    and LIVRE.match(r["lic"] or "") and not re.search(r"logo|map|mapa|flag|bandeira|coat of arms|bras[aã]o", r["title"], re.I)]
            if not bons:
                log(f"  foto {k}: nada livre para '{termo}' ({len(res)} resultados)"); continue
            r = bons[0]
            try:
                _baixa(r["url"], dest, headers={"User-Agent": UA_BOT})
            except Exception as e:
                log(f"  foto {k}: download falhou ({str(e)[:100]})"); continue
            autor = r["autor"] or ("Wellcome Collection" if "Wellcome" in r["title"] else "")
            cred = f"{autor + ' / ' if autor else ''}{r['lic']} / Wikimedia Commons"
            creditos.append(f"{r['title'].replace('File:', '')}: {cred} – {r['page']}")
            creditos_arq[k] = ("Photo: " if os.environ.get("IDIOMA_FALA") == "en" else "Foto: ") + cred
            log(f"  foto {k}: {r['title']} ({r['lic']})")
            print(f"::notice title=Foto real ({k})::{r['title']} · {r['lic']} · busca '{termo}'", flush=True)
            achou = True
            break
        if not achou:
            print(f"::warning title=Sem foto ({k})::nenhuma foto livre para {termos}; a cena usa o texto de reserva", flush=True)


def coletar_logos(obj, out=None):
    """Acha todos os {"logos": {"chave": "File:Logo.svg"}} no projeto (cenas, capas, miniaturas)."""
    out = {} if out is None else out
    if isinstance(obj, dict):
        for k, v in (obj.get("logos") or {}).items():
            out.setdefault(k, v)
        for v in obj.values():
            coletar_logos(v, out)
    elif isinstance(obj, list):
        for v in obj:
            coletar_logos(v, out)
    return out


def logos(projeto, pasta, log):
    """Logos de marcas do Wikimedia Commons (arquivo exato), em PNG com fundo transparente: <chave>.png.
    No Commons só ficam logos livres (em geral 'PD-textlogo'); ainda assim confere a licença."""
    for k, arq in coletar_logos(projeto).items():
        dest = os.path.join(pasta, k + ".png")
        if os.path.exists(dest):
            continue
        try:
            res = _commons_busca(arq if arq.lower().startswith("file:") else "File:" + arq, largura=1400)
        except Exception as e:
            log(f"  logo {k}: busca falhou ({str(e)[:100]})"); continue
        r = res[0] if res else None
        if not r or not r.get("url") or not LIVRE.match(r["lic"] or ""):
            print(f"::warning title=Sem logo ({k})::{arq} não encontrado ou licença não livre ({r and r.get('lic')})", flush=True); continue
        try:
            _baixa(r["url"], dest, headers={"User-Agent": UA_BOT})
            from PIL import Image
            im = Image.open(dest).convert("RGBA"); bb = im.getchannel("A").getbbox()
            if bb:  # corta a margem transparente para o logo ocupar o espaço certo
                im.crop(bb).save(dest)
            print(f"::notice title=Logo ({k})::{r['title']} · {r['lic']}", flush=True)
        except Exception as e:
            log(f"  logo {k}: download falhou ({str(e)[:100]})")


def candidatos(cenas, pasta_saida, log):
    """Folha de contato com os 8 primeiros clipes do Pixabay de cada cena de vídeo (para escolher a dedo)."""
    from PIL import Image, ImageDraw
    key = os.environ.get("PIXABAY_KEY", "").strip()
    os.makedirs(pasta_saida, exist_ok=True); feitos = []
    vistos = set()
    for sc in cenas:
        k = sc.get("media"); q = sc.get("search_en") or sc.get("search")
        if sc.get("type") != "video" or not k or not q or k in vistos:
            continue
        vistos.add(k)
        url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "q": q[:100], "lang": "en" if sc.get("search_en") else "pt", "per_page": 8, "safesearch": "true"})
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
            hits = json.load(r).get("hits", [])[:8]
        W, H = 320, 180; folha = Image.new("RGB", (W * 4, (H + 40) * 2), (20, 20, 20)); d = ImageDraw.Draw(folha)
        for i, h in enumerate(hits):
            th = (h["videos"].get("medium") or {}).get("thumbnail") or (h["videos"].get("small") or {}).get("thumbnail")
            x, y = (i % 4) * W, (i // 4) * (H + 40)
            try:
                tmp = os.path.join(pasta_saida, "_t.jpg"); _baixa(th, tmp)
                im = Image.open(tmp).convert("RGB"); im.thumbnail((W, H)); folha.paste(im, (x, y)); os.remove(tmp)
            except Exception:
                pass
            v = h["videos"].get("large") or h["videos"].get("medium") or {}
            d.text((x + 4, y + H + 2), f"id {h['id']} · {h.get('duration')}s · {v.get('width')}x{v.get('height')}", fill=(255, 210, 60))
            d.text((x + 4, y + H + 18), h.get("tags", "")[:48], fill=(220, 220, 220))
        folha.save(os.path.join(pasta_saida, f"candidatos_{k}.jpg"), quality=85); feitos.append(k)
        log(f"  candidatos {k}: {len(hits)} ('{q}')")
    print(f"::notice title=Candidatos de clipe::{', '.join(feitos) or 'nenhuma cena de vídeo'}", flush=True)

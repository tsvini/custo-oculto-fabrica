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


def _uniforme(path):
    try:
        from PIL import Image, ImageStat
        im = Image.open(path).convert("L")
        return max(ImageStat.Stat(im).stddev) < 12
    except Exception:
        return True


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
    alvo = {}
    for s in cenas:
        if s.get("type") == "video" and s.get("media") and s.get("search"):
            alvo.setdefault(s["media"], s["search"])
    pend = {k: q for k, q in alvo.items() if not os.path.exists(os.path.join(pasta, k + ".mp4"))}
    if not pend:
        return
    if not key:
        log(f"  sem PEXELS_KEY: {len(pend)} clipe(s) usam o texto de reserva")
        return
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
            _baixa(arqs[0]["link"], os.path.join(pasta, k + ".mp4"))
            nome = (v.get("user") or {}).get("name", "")
            creditos.append(f"{nome} (Pexels) – {v.get('url', '')}")
            log(f"  clipe {k}: ok ('{q}', {nome})")
        except Exception as e:
            log(f"  clipe {k}: falhou ({str(e)[:120]})")


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
            cred = f"{r['autor'] or 'Autor desconhecido'} / {r['lic']} / Wikimedia Commons"
            creditos.append(f"{r['title'].replace('File:', '')}: {cred} – {r['page']}")
            creditos_arq[k] = "Foto: " + cred
            log(f"  foto {k}: {r['title']} ({r['lic']})")
            print(f"::notice title=Foto real ({k})::{r['title']} · {r['lic']} · busca '{termo}'", flush=True)
            achou = True
            break
        if not achou:
            print(f"::warning title=Sem foto ({k})::nenhuma foto livre para {termos}; a cena usa o texto de reserva", flush=True)

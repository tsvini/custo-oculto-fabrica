"""Podcast automático: os MP3 dos vídeos longos vão para o repositório público tsvini/custo-oculto-podcast,
que o GitHub Pages serve em https://tsvini.github.io/custo-oculto-podcast/. O Spotify (e Apple etc.) lê o feed RSS
e publica sozinho.

  python -m fabrica.podcast adicionar saida   → copia os episódios gerados e atualiza o feed
  python -m fabrica.podcast feed              → só atualiza o feed (episódio entra no dia em que o vídeo vai ao ar)

Secret: PODCAST_TOKEN (token com Contents: Read and write no repositório do podcast).
Opcional: PODCAST_EMAIL (e-mail que o Spotify usa para confirmar que o podcast é seu; fica público no feed).
"""
import datetime as dt, email.utils, glob, json, os, shutil, subprocess, sys, tempfile
from xml.sax.saxutils import escape

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "tsvini/custo-oculto-podcast"
BASE = "https://tsvini.github.io/custo-oculto-podcast"
BRT = dt.timezone(dt.timedelta(hours=-3))

SHOWS = {
    "pt": {"titulo": "Custo Oculto", "feed": "feed.xml", "capa": "capa.jpg", "lang": "pt-br", "autor": "Vinícius Torales",
           "categoria": ("Business", "Entrepreneurship"), "link": "https://www.youtube.com/@Custo-Oculto-YT",
           "descricao": "Histórias reais por trás de empresas famosas: fraudes, quedas, decisões bilionárias e quem pagou a conta. Um caso novo toda semana, do canal Custo Oculto no YouTube."},
    "en": {"titulo": "Hidden Cost", "feed": "feed-en.xml", "capa": "capa-en.jpg", "lang": "en", "autor": "Vinícius Torales",
           "categoria": ("Business", "Entrepreneurship"), "link": "https://www.youtube.com/@HiddenCostCases",
           "descricao": "The real stories behind the world's most famous companies: frauds, collapses, billion-dollar mistakes and who paid the price. A new case every week, from the Hidden Cost YouTube channel."},
}


def nota(t, m, nivel="notice"):
    print(f"::{nivel} title={t}::{m}"[:1000], flush=True)


def git(*a, cwd):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout


def clonar(dest):
    tk = os.environ.get("PODCAST_TOKEN", "").strip()
    if not tk:
        nota("Podcast", "falta o secret PODCAST_TOKEN; episódio não publicado", "warning"); return False
    git("clone", "-q", "--depth", "1", f"https://x-access-token:{tk}@github.com/{REPO}.git", dest, cwd=RAIZ)
    git("config", "user.name", "fabrica-custo-oculto", cwd=dest); git("config", "user.email", "fabrica@users.noreply.github.com", cwd=dest)
    return True


def registro():
    try:
        return {r["nome"]: r for r in json.load(open(os.path.join(RAIZ, "publicados.json"), encoding="utf8"))}
    except Exception:
        return {}


def duracao(mp3):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", mp3], capture_output=True, text=True)
    try:
        return int(float(r.stdout.strip()))
    except Exception:
        return 0


CAPAS = {"capa.jpg": "canal/podcast_capa.jpg", "capa-en.jpg": "canal/podcast_capa_en.jpg"}


def gerar_feeds(repo):
    for dest, src in CAPAS.items():  # capa vem da fábrica
        s = os.path.join(RAIZ, src)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(repo, dest))
    eps = json.load(open(os.path.join(repo, "episodios.json"), encoding="utf8")) if os.path.exists(os.path.join(repo, "episodios.json")) else []
    reg = registro(); hoje = dt.datetime.now(BRT).date(); email_dono = os.environ.get("PODCAST_EMAIL", "").strip()
    for idi, S in SHOWS.items():
        itens = []
        for e in eps:
            if e["idioma"] != idi:
                continue
            r = reg.get(e["nome"]) or {}
            quando = r.get("publishAt") or e.get("publishAt")
            if not quando:
                continue  # o vídeo ainda não foi agendado no YouTube
            q = dt.datetime.fromisoformat(quando)
            if q.astimezone(BRT).date() > hoje:
                continue  # entra no dia em que o vídeo vai ao ar
            link = f"https://youtu.be/{r['video_id']}" if r.get("video_id") else S["link"]
            itens.append((q, f"""    <item>
      <title>{escape(e['titulo'])}</title>
      <description>{escape(e['descricao'])}</description>
      <link>{link}</link>
      <guid isPermaLink="false">{escape(e['nome'])}</guid>
      <pubDate>{email.utils.format_datetime(q)}</pubDate>
      <enclosure url="{BASE}/{e['arquivo']}" length="{e['bytes']}" type="audio/mpeg"/>
      <itunes:duration>{e['segundos']}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
      <itunes:episodeType>full</itunes:episodeType>
    </item>"""))
        if not itens and not os.path.exists(os.path.join(repo, S["capa"])):
            continue
        itens.sort(key=lambda x: x[0], reverse=True)
        cat, sub = S["categoria"]
        dono = f"\n    <itunes:owner><itunes:name>{escape(S['autor'])}</itunes:name><itunes:email>{escape(email_dono)}</itunes:email></itunes:owner>" if email_dono else ""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(S['titulo'])}</title>
    <link>{S['link']}</link>
    <language>{S['lang']}</language>
    <description>{escape(S['descricao'])}</description>
    <atom:link href="{BASE}/{S['feed']}" rel="self" type="application/rss+xml"/>
    <itunes:author>{escape(S['autor'])}</itunes:author>
    <itunes:summary>{escape(S['descricao'])}</itunes:summary>
    <itunes:image href="{BASE}/{S['capa']}"/>
    <image><url>{BASE}/{S['capa']}</url><title>{escape(S['titulo'])}</title><link>{S['link']}</link></image>
    <itunes:category text="{cat}"><itunes:category text="{sub}"/></itunes:category>
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>episodic</itunes:type>{dono}
{chr(10).join(x for _, x in itens)}
  </channel>
</rss>
"""
        open(os.path.join(repo, S["feed"]), "w", encoding="utf8").write(xml)
        nota(f"Podcast {S['titulo']}", f"{len(itens)} episódio(s) no feed {BASE}/{S['feed']}")


def salvar(repo, msg):
    git("add", "-A", cwd=repo)
    if not git("status", "--porcelain", cwd=repo).strip():
        return
    git("commit", "-q", "-m", msg, cwd=repo)
    for _ in range(5):
        try:
            git("pull", "-q", "--rebase", "origin", "main", cwd=repo); git("push", "-q", "origin", "HEAD:main", cwd=repo); return
        except subprocess.CalledProcessError:
            import time; time.sleep(5)
    nota("Podcast", "não consegui salvar no repositório do podcast", "warning")


def adicionar(pasta_saida):
    with tempfile.TemporaryDirectory() as t:
        repo = os.path.join(t, "podcast")
        if not clonar(repo):
            return
        idx = os.path.join(repo, "episodios.json")
        eps = json.load(open(idx, encoding="utf8")) if os.path.exists(idx) else []
        novos = []
        for mp3 in glob.glob(os.path.join(pasta_saida, "**", "podcast_*.mp3"), recursive=True):
            d = os.path.dirname(mp3); slug = os.path.basename(mp3)[len("podcast_"):-4]
            mj = glob.glob(os.path.join(d, "youtube_*_longo.json"))
            meta = json.load(open(mj[0], encoding="utf8")) if mj else {}
            idi = (meta.get("idioma") or "pt")[:2]
            nome = f"{meta.get('caso') or slug.replace('-', '_')}_longo"
            arq = f"episodios/{idi}/{slug}.mp3"
            os.makedirs(os.path.dirname(os.path.join(repo, arq)), exist_ok=True)
            shutil.copy(mp3, os.path.join(repo, arq))
            desc = (meta.get("descricao") or "").strip()
            S = SHOWS.get(idi, SHOWS["pt"])
            desc += ("\n\n" if desc else "") + ("Watch it on YouTube: " if idi == "en" else "Assista no YouTube: ") + S["link"]
            e = {"nome": nome, "idioma": idi, "titulo": meta.get("titulo") or slug, "descricao": desc, "arquivo": arq,
                 "bytes": os.path.getsize(mp3), "segundos": duracao(mp3)}
            eps = [x for x in eps if x["nome"] != nome] + [e]; novos.append(e["titulo"])
        json.dump(eps, open(idx, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        gerar_feeds(repo)
        salvar(repo, "Episódios: " + "; ".join(novos) if novos else "Feed atualizado")
        if novos:
            nota("Podcast", "episódio(s) adicionados (entram no feed no dia em que o vídeo vai ao ar): " + "; ".join(novos))


def feed():
    with tempfile.TemporaryDirectory() as t:
        repo = os.path.join(t, "podcast")
        if clonar(repo):
            gerar_feeds(repo); salvar(repo, "Feed atualizado")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "feed"
    adicionar(sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "saida")) if cmd == "adicionar" else feed()

"""Gera projetos/<nome>/NARRACAO.md: o texto exato de cada áudio que você precisa gravar.

  python -m fabrica.narracao kolynos
"""
import json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def frases(g):
    return [s["text"].strip() for s in g["sentences"] if s.get("text", "").strip()]


def main(nome):
    pasta = os.path.join(RAIZ, "projetos", nome)
    p = json.load(open(os.path.join(pasta, "projeto.json"), encoding="utf8"))
    out = [f"# Narração — {p.get('title', nome)}", "",
           "Grave cada bloco num arquivo separado, com o nome indicado, e envie tudo de uma vez para `projetos/" + nome + "/audio/`.",
           "Leia o texto como está: a fábrica sincroniza legenda e cenas comparando o áudio com estas palavras.", ""]
    for k, g in enumerate(p["script"]["long"]["parts"]):
        cap = g.get("chapter") or ""
        out += [f"## parte{k + 1}.mp3 — longo{(' · ' + cap) if cap else ''}", "", " ".join(frases(g)), ""]
    for i, sh in enumerate(p["script"].get("shorts", [])):
        out += [f"## short{i + 1}.mp3 — Short: {sh.get('title', '')}", "", " ".join(frases(sh)), ""]
    with open(os.path.join(pasta, "NARRACAO.md"), "w", encoding="utf8") as f:
        f.write("\n".join(out))
    print(os.path.join(pasta, "NARRACAO.md"))


if __name__ == "__main__":
    main(sys.argv[1])

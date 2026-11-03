"""Completa a árvore do Explorer em todas as aulas do curso de Playwright.

Os roteiros às vezes mostram uma árvore "enxuta" (sem a pasta arquivos, sem o package.json...). Pro aluno parece que o arquivo sumiu.
Regra: tudo o que já foi criado no projeto aparece no Explorer, até alguém apagar (cena "apaga"). Uma pasta pode aparecer fechada
(sem os filhos), mas se ela está aberta, aparecem todos os arquivos dela. Ordem do VS Code: pastas primeiro, depois arquivos,
em ordem alfabética (o ponto vem antes).

Uso: python ferramentas/arvores.py  (os roteiro_playwright_*.py chamam completar() no fim do main)."""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DE_AULA = 13  # antes disso o projeto ainda está nascendo (aula 2 mostra uma prévia, a 12 renomeia o example.spec.js)


def _parse(pastas):
    """[(nivel, caminho, é_pasta)] sem a raiz"""
    out, pilha = [], []
    for l in pastas[1:]:
        nivel = (len(l) - len(l.lstrip(" "))) // 2
        nome = l.strip()
        pilha = pilha[:nivel - 1]
        cam = "/".join([x.rstrip("/") for x in pilha] + [nome.rstrip("/")])
        out.append((nivel, cam, nome.endswith("/")))
        if nome.endswith("/"):
            pilha.append(nome)
    return out


def _chave(nome, pasta):
    return (0 if pasta else 1, nome.lower().lstrip(".") if False else nome.lower())


def _montar(raiz, itens, abertas):
    """itens: {caminho: é_pasta}. Mostra os filhos só das pastas abertas."""
    filhos = {}
    for cam, pasta in itens.items():
        pai = cam.rsplit("/", 1)[0] if "/" in cam else ""
        filhos.setdefault(pai, []).append((cam, pasta))
    linhas = [raiz]

    def desce(pai, nivel):
        for cam, pasta in sorted(filhos.get(pai, []), key=lambda x: (0 if x[1] else 1, x[0].rsplit("/", 1)[-1].lower())):
            nome = cam.rsplit("/", 1)[-1]
            linhas.append("  " * nivel + nome + ("/" if pasta else ""))
            if pasta and cam in abertas:
                desce(cam, nivel + 1)
    desce("", 1)
    return linhas


def completar(log=False):
    projeto, estado, mudou, estados = None, {}, set(), {}
    for n in range(1, 84):
        arq = os.path.join(RAIZ, "projetos", f"curso-playwright-{n:02d}", "projeto.json")
        if not os.path.exists(arq):
            continue
        p = json.load(open(arq, encoding="utf8"))
        alterou = False
        for s in p["script"]["long"]["parts"][0]["sentences"]:
            c = s["scene"]
            pas = c.get("pastas")
            if not pas:
                continue
            if pas[0] != projeto:  # cada projeto guarda o seu estado (a aula 83 volta pro primeiro projeto)
                if projeto:
                    estados[projeto] = estado
                projeto = pas[0]; estado = estados.get(projeto, {}) if n >= DE_AULA else {}
            # a árvore "final" da cena (no menu de criar, o item novo entra na posição novo_pos)
            final = list(pas)
            if c.get("type") == "menu" and c.get("novo") and c.get("novo_pos") is not None:
                final.insert(c["novo_pos"], "  " * c.get("novo_nivel", 1) + c["novo"].rstrip("/") + ("/" if c.get("novo_pasta") else ""))
            itens = _parse(final)
            cena = {cam: pasta for _, cam, pasta in itens}
            abertas = {cam for _, cam, pasta in itens if pasta and any(o.startswith(cam + "/") for o in cena)}
            if n >= DE_AULA:
                # foco da cena: o arquivo aberto, o item novo, o item clicado ou apagado. Pasta aberta sem nada do foco dentro fica fechada
                # (senão a árvore inteira não cabe e as linhas encavalam)
                nomes = {x.rstrip("/") for x in (c.get("arquivo"), c.get("novo"), c.get("alvo_item"), c.get("apaga")) if x}
                foco = {cam for cam in cena if cam.rsplit("/", 1)[-1] in nomes}
                if foco:
                    abertas = {a for a in abertas if any(f.startswith(a + "/") for f in foco)}
                todos = dict(estado)
                todos.update(cena)
                # só completa dentro do que está visível: raiz e pastas abertas
                vis = {cam: pasta for cam, pasta in todos.items() if ("/" not in cam) or cam.rsplit("/", 1)[0] in abertas}
                # os pais das pastas abertas também precisam estar visíveis
                nova_final = _montar(pas[0], vis, abertas)
                if nova_final != final:
                    if c.get("type") == "menu" and c.get("novo") and c.get("novo_pos") is not None:
                        alvo = "  " * c.get("novo_nivel", 1) + c["novo"].rstrip("/") + ("/" if c.get("novo_pasta") else "")
                        i = nova_final.index(alvo)
                        c["novo_pos"] = i
                        c["pastas"] = nova_final[:i] + nova_final[i + 1:]
                    else:
                        c["pastas"] = nova_final
                    alterou = True
            estado.update(cena)
            if c.get("apaga"):
                for k in [k for k in estado if k.rsplit("/", 1)[-1] == c["apaga"].rstrip("/")]:
                    del estado[k]
        # cena de menu (criar/apagar no Explorer) com frase curta: a animação leva ~4,5 s e cortava no meio.
        # "segura" = silêncio colado na montagem depois da frase (a narração gravada não muda)
        for s in p["script"]["long"]["parts"][0]["sentences"]:
            if s["scene"].get("type") == "menu" and not s.get("pausa"):
                falta = round(4.8 - len(s["text"]) / 14.5, 1)
                seg = falta if falta >= 0.4 else None
                if s.get("segura") != seg:
                    if seg: s["segura"] = seg
                    else: s.pop("segura", None)
                    alterou = True
        if alterou:
            json.dump(p, open(arq, "w", encoding="utf8"), ensure_ascii=False, indent=1)
            mudou.add(n)
    if log:
        print("árvores completadas nas aulas:", " ".join(str(x) for x in sorted(mudou)) or "nenhuma")
    return mudou


if __name__ == "__main__":
    completar(log=True)

"""Gera projetos/curso-playwright-46..48 (módulo 10: bônus API). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Código = curso-playwright/projeto/tests/etapas/aula47/48.spec.js (validado no Actions: 119 ms, 45 ms, 43 ms com --reporter=list).
Frases com "editor + tradução" viraram duas cenas com o mesmo texto dividido (a narração é a mesma do roteiro aprovado).
A aula 46 usa a gravação real de um Chromium comum abrindo a API (ferramentas/codegen/api46.sh)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m4 import edc, real
from roteiro_playwright_m8 import cod, ln, parcial, ARV_AUTH

ARV_API = ARV_AUTH[:ARV_AUTH.index("    auth.setup.js")] + ["    api.spec.js"] + ARV_AUTH[ARV_AUTH.index("    auth.setup.js"):]
C47, C48 = cod(47), cod(48)
CMD = "npx playwright test api.spec.js --project=chromium --reporter=list"
SETUP = "  ✓  1 [setup] › tests/auth.setup.js:5:6 › faz login uma vez (539ms)"


def ed(c, legenda, de=None, ate=None, mostra=None, **kw):
    """api.spec.js no editor; digita as linhas de..ate (o resto do arquivo ainda não existe se 'mostra' corta)"""
    cc = parcial(c, mostra, ("});",)) if mostra else c
    d = dict(arquivo="api.spec.js", fonte=24)
    if max(len(l) for l in cc.split("\n")) <= 66:
        d["pastas"] = ARV_API  # linha longa (o endereço da API): sem o explorer, pra letra ficar grande
    if de:
        d.update(digitar=True, digitar_de=de, digitar_ate=ate or de)
    d.update(kw)
    return edc(cc, legenda, **d)


def tr(codigo, partes, passo=1.6):
    return {"type": "traducao", "codigo": codigo, "partes": partes, "passo": passo}


def rodar(c, legenda, linhas, n=10, **kw):
    T = [{"cmd": CMD, "em": 0.03}] + [{"out": t, "cor": cor, "em": 0.4 + i * 0.07} for i, (t, cor) in enumerate(linhas)]
    return edc("\n".join(c.split("\n")[:n]), legenda, arquivo="api.spec.js", terminal=T, **kw)


AULAS = []

# ---------- Aula 46 ----------
AULAS.append(projeto(46, "MÓDULO 10 · AULA 46", "O que é uma API, explicado do zero", [
    ("Quase todo site conversa com um servidor por trás. E pra essa conversa funcionar, existe a API.", titulo(46, "O QUE É UMA API")),
    ("Uma API é um jeito combinado de um sistema pedir dados ou ações pra outro.",
     {"type": "cards", "titulo": "API", "itens": [["📨", "Um sistema pede", "dados ou ações"], ["🤝", "Num jeito combinado", "o formato do pedido", "#69a7ff"], ["🖥", "O outro responde", "o servidor", "#ffd23f"]]}),
    ("Pensa num restaurante: você não entra na cozinha, você faz o pedido ao garçom, num formato combinado, e recebe a resposta. É uma simplificação, mas ajuda.",
     {"type": "cards", "titulo": "PENSA NUM RESTAURANTE", "itens": [["🙋", "Você", "faz o pedido"], ["🤵", "Garçom = API", "leva o pedido e traz a resposta", "#69a7ff"], ["🍳", "Cozinha = servidor", "prepara o que você pediu", "#ffd23f"]]}),
    ("Esses pedidos se chamam requisições, e cada uma tem um método. GET, buscar. POST, criar. DELETE, apagar.",
     {"type": "traducao", "titulo": "REQUISIÇÃO · O MÉTODO", "linhas": [["GET", "buscar"], ["POST", "criar"], ["DELETE", "apagar"]]}),
    ("E a resposta vem com um número, o status: duzentos é deu certo, duzentos e um é criado, quatrocentos e quatro é não encontrado.",
     {"type": "cards", "titulo": "STATUS DA RESPOSTA", "itens": [["200", "Deu certo", "OK"], ["201", "Criado", "Created", "#69a7ff"], ["404", "Não encontrado", "Not Found", "#ff6b6b"]]}),
    ("Vamos usar uma API de treino gratuita, a jsonplaceholder. Abre no navegador o endereço dela, barra posts barra um.",
     real("api46_abre", "jsonplaceholder.typicode.com/posts/1")),
    ("Esse texto com chaves é JSON: um formato de dados que muitas APIs usam.",
     {"type": "traducao", "titulo": "JSON: O POST NÚMERO 1", "linhas": [["\"userId\": 1", "o usuário que escreveu"], ["\"id\": 1", "o número do post"],
                                                                          ["\"title\": \"sunt aut facere...\"", "o título"], ["\"body\": \"quia et suscipit...\"", "o texto"]]}),
    ("Na próxima aula: o seu primeiro teste de API.", proxima("primeiro teste de API")[0]),
    ("Te vejo lá!", proxima("primeiro teste de API")[1]),
]))

# ---------- Aula 47 ----------
L_GET, L_ST, L_JSON, L_ID = ln(C47, "request.get"), ln(C47, "status()"), ln(C47, "json()"), ln(C47, "post.id")
AULAS.append(projeto(47, "MÓDULO 10 · AULA 47", "Seu primeiro teste de API", [
    ("Teste de API não abre navegador nenhum. Por isso ele é bem rápido.", titulo(47, "TESTE DE API")),
    ("Cria o api ponto spec ponto js. No teste, em vez do page, você pede o request, entre chaves.",
     ed(C47, "{ request } no lugar do { page }", de=1, ate=4, mostra=L_GET - 1)),
    ("Request quer dizer requisição.", tr("async ({ request }) => {", [["{ request }", "a requisição"]], 1.0)),
    ("const resposta igual await request ponto get, e o endereço.", ed(C47, "request.get(endereço)", de=L_GET, mostra=L_GET)),
    ("Busque o post número um e guarde a resposta.",
     tr("const resposta = await request.get('…/posts/1');", [["const resposta =", "guarde a resposta"], ["await request.get", "busque"], ["('…/posts/1')", "o post número 1"]])),
    ("expect, resposta ponto status, abre e fecha parênteses, to be duzentos.", ed(C47, "expect(resposta.status()).toBe(200)", de=L_ST, mostra=L_ST)),
    ("Eu espero que o status da resposta seja duzentos.", tr("expect(resposta.status()).toBe(200);", [["expect", "eu espero que"], ["(resposta.status())", "o status da resposta"], ["toBe(200)", "seja 200"]])),
    ("Repara nos parênteses depois do status.", ed(C47, "status() — com os parênteses", mostra=L_ST, destaque=[L_ST], destaque_em=0.2)),
    ("Depois: const post igual await resposta ponto json, com parênteses.", ed(C47, "resposta.json()", de=L_JSON, mostra=L_JSON)),
    ("Leia os dados que vieram.", tr("const post = await resposta.json();", [["const post =", "guarde em post"], ["await resposta.json()", "leia os dados que vieram"]], 1.0)),
    ("E o expect: post ponto id, to be um.", ed(C47, "post.id = o número do post", de=L_ID)),
    ("Roda: passou, em milissegundos.",
     rodar(C47, "--reporter=list mostra o tempo de cada teste", [("Running 2 tests using 2 workers", "mut"), (SETUP, "mut"),
                                                                   ("  ✓  2 [chromium] › tests/api.spec.js:3:5 › busca um post (119ms)", "ac"), ("  2 passed (1.6s)", "ac")])),
    ("Na próxima aula: criando e apagando pela API.", proxima("criando e apagando")[0]),
    ("Te vejo lá!", proxima("criando e apagando")[1]),
]))

# ---------- Aula 48 ----------
L_T2, L_DATA, L_201, L_TIT = ln(C48, "test('cria"), ln(C48, "data:"), ln(C48, "toBe(201)"), ln(C48, "post.title")
L_T3, L_DEL = ln(C48, "test('apaga"), ln(C48, "request.delete")
RO = dict(rolar=True, rolar_de=0.5, rolar_dur=0.8)
AULAS.append(projeto(48, "MÓDULO 10 · AULA 48", "Criando e apagando dados pela API", [
    ("Agora vamos simular uma criação e uma exclusão. A API de treino responde como uma de verdade, mas não guarda essas mudanças.", titulo(48, "CRIAR E APAGAR")),
    ("request ponto post, com um data: título, texto e userId.", ed(C48, "request.post(endereço, { data })", de=L_T2, ate=L_DATA + 1, mostra=L_DATA + 1, **RO)),
    ("É a requisição de criar.", tr("request.post('…/posts', { data: { title, body, userId } })", [["request.post", "criar"], ["title", "título"], ["body", "texto"], ["userId", "o usuário"]], 1.2)),
    ("A conferência: status duzentos e um, criado.", ed(C48, "201 = criado", de=L_201, mostra=L_201, **RO)),
    ("E o título que voltou é o mesmo que você mandou.", ed(C48, "o título que voltou = o que você mandou", de=L_TIT - 1, ate=L_TIT, mostra=L_TIT, **RO)),
    ("request ponto delete: apagar. Status duzentos.", ed(C48, "delete = apagar · 200", de=L_T3, ate=L_DEL + 2, **RO)),
    ("Roda os três: passaram.",
     rodar(C48, "Os três, em milissegundos", [("Running 4 tests using 4 workers", "mut"), (SETUP, "mut"),
                                              ("  ✓  2 [chromium] › tests/api.spec.js:3:5 › busca um post (119ms)", "ac"),
                                              ("  ✓  3 [chromium] › tests/api.spec.js:10:5 › cria um post (45ms)", "ac"),
                                              ("  ✓  4 [chromium] › tests/api.spec.js:19:5 › apaga um post (43ms)", "ac"), ("  4 passed (1.7s)", "ac")], n=8)),
    ("Num sistema real, essa criação e essa exclusão ficariam guardadas no banco de dados.",
     {"type": "cards", "itens": [["🧪", "API de treino", "responde, mas não guarda"], ["🗄", "Sistema real", "guarda no banco de dados", "#69a7ff"]]}),
    ("Fechamos o bônus! Agora: desafios pra você praticar.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Desafios pra praticar"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: DESAFIOS"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 10 (gerado do roteiro_playwright_m10.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo10.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

"""Gera projetos/curso-playwright-64..73 (nível 2 · módulo 13: Playwright de verdade no trabalho). Roteiro: curso-playwright/roteiros/nivel2.md,
com o filtro de qualidade: toda aula responde pra que serve, como faz (mostrando), quando usar / quando não usar, e o uso no trabalho.
Código = curso-playwright/projeto (fixtures/, dados/, tests/nivel2/*.spec.js), validado no Actions (validar_nivel2.yml);
as saídas de terminal são as reais de nivel2_resultado.txt (release bastidores), com o "aula NN:" tirado dos nomes."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, projeto, RAIZ
from roteiro_playwright_m4 import edc
from roteiro_playwright_m3 import SAUCE, LOGIN
from roteiro_playwright_m6 import A_LOGIN, TRACE6, C26, L_MOCHILA, ERRO_TRACE, A_FALHA, CARD_BUG

PROJ = os.path.join(RAIZ, "curso-playwright", "projeto")
AZUL, AMARELO, VERM, VERDE, LARANJA = "#69a7ff", "#ffd23f", "#ff6b6b", "#3fd68a", "#ff8c42"
LOJA = "https://tsvini.github.io/custo-oculto-fabrica/loja/"
API = "**/api/produtos.json"
LOGIN_LOJA = [{"fill": ["[data-test=\"usuario\"]", "cliente"]}, {"fill": ["[data-test=\"senha\"]", "leigo123"]}, {"click": "[data-test=\"entrar\"]", "espera": 1500}]
DIFF = "repo:curso-playwright/material/cenas/diff_visual.html"
COLINHA = "repo:curso-playwright/material/colinha/colinha.html"


def ler(rel):
    return re.sub(r"aula \d+: ", "", open(os.path.join(PROJ, rel), encoding="utf8").read().rstrip("\n"))


def ln(cod, trecho, n=1):
    achou = [i + 1 for i, l in enumerate(cod.split("\n")) if trecho in l]
    assert len(achou) >= n, (trecho, cod[:120])
    return achou[n - 1]


def trecho(cod, de, ate):
    return "\n".join(cod.split("\n")[de - 1:ate])


CRIADOS = []  # o que já foi criado na tela, na ordem (o Explorer só mostra o que o aluno já criou)
ORDEM_N2 = ["fixture.spec.js", "dados.spec.js", "mock.spec.js", "visual.spec.js", "soft.spec.js", "tags.spec.js", "flaky.demo.spec.js", "flaky.spec.js"]


def arvore():
    a = ["meu-primeiro-playwright"]
    if "dados" in CRIADOS: a += ["  dados/"] + (["    usuarios.json"] if "usuarios.json" in CRIADOS else [])
    if "fixtures" in CRIADOS: a += ["  fixtures/"] + (["    paginas.js"] if "paginas.js" in CRIADOS else [])
    a += ["  pages/", "  tests/"]
    if "nivel2" in CRIADOS: a += ["    nivel2/"] + ["      " + f for f in ORDEM_N2 if f in CRIADOS]
    return a + ["  .env", "  playwright.config.js"]


def ed(cod, legenda, arquivo, de=None, ate=None, linha0=1, pastas="auto", **kw):
    """editor com o arquivo; 'de'/'ate' = linhas digitadas (na numeração do trecho mostrado)"""
    for _, nome in kw.get("criar", []):
        CRIADOS.append(nome.rstrip("/"))
    if kw.get("criar"):
        kw["criar_arvore"] = arvore()
    larg = max(len(l) for l in cod.split("\n"))
    d = dict(arquivo=arquivo, linha0=linha0, fonte=30 if larg <= 50 else 26 if larg <= 64 else 22)
    d["pastas"] = (arvore() if larg <= 56 else None) if pastas == "auto" else pastas
    if de:
        d.update(digitar=True, digitar_de=de, digitar_ate=ate or de)
    d.update(kw)
    return edc(cod, legenda, **d)


def tr(codigo, partes, passo=1.6):
    return {"type": "traducao", "codigo": codigo, "partes": partes, "passo": passo}


def trl(titulo_t, linhas):
    return {"type": "traducao", "titulo": titulo_t, "linhas": linhas}


def cards(itens, titulo_c=None):
    d = {"type": "cards", "itens": itens}
    if titulo_c:
        d["titulo"] = titulo_c
    return d


def cmp(t, a, b, cor_a="white"):
    return {"type": "compare", "title": t, "items": [[a[0], a[1], cor_a], [b[0], b[1], "gold"]], "size": 90, "stagger": 1.8, "vs": False}


def term(linhas, legenda, digitar=True, fonte=26):
    """terminal do VS Code: o comando digitado e a saída real"""
    L = []
    for i, l in enumerate(linhas):
        if isinstance(l, str):
            L.append({"cmd": l, "em": 0.04} if digitar else {"cmd": l, "ja": True})
        else:
            txt, cor = l
            L.append({"out": txt, "cor": cor, "em": min(0.25 + i * 0.06, 0.8)} if digitar else {"out": txt, "cor": cor, "ja": True})
    return {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": "C:\\Users\\voce\\Documents\\meu-primeiro-playwright", "linhas": L, "legenda": legenda,
            "fonte": fonte, "fonte_min": 18, "compacto": len(L) > 10}


def video(media, legenda, url, acoes=(), **kw):
    d = {"type": "tela", "media": media, "url": url, "gravar": True, "acoes": list(acoes), "titulo": "Lojinha do Leigo", "legenda": legenda,
         "espera_inicio": 1200, "espera_fim": 2000, "delay_letra": 70}
    d.update(kw)
    return d


def fim(prox):
    return [("Te vejo na próxima!", {"type": "endcard", "sub": "PRÓXIMA: " + prox.upper()})]


AULAS = []


def aula(n, titulo_aula, frases):
    AULAS.append(projeto(n, f"MÓDULO 13 · AULA {n}", titulo_aula, frases))


# ---------- 64 · fixtures ----------
COMPRA = ler("tests/compra.spec.js"); PAG = ler("fixtures/paginas.js"); FIX = ler("tests/nivel2/fixture.spec.js")
aula(64, "O teste está montando coisa demais", [
    ("Olha o teste da compra. Antes de testar qualquer coisa, ele monta as páginas: new ProdutosPage, new CheckoutPage. E isso se repete em todo arquivo que usa uma página.",
     ed(trecho(COMPRA, 1, 12), "Montando as páginas antes de testar", "compra.spec.js", destaque=[8, 9], destaque_em=1.6)),
    ("Agora repara no page. Você nunca escreveu new page: ele chega pronto, é só pedir entre chaves. Quem prepara é o próprio Playwright.",
     tr("test('compra...', async ({ page }) => {", [["{ page }", "chega pronto"]], 1.0)),
    ("Isso se chama fixture: alguma coisa que o teste recebe pronta. O page é uma, o request das aulas de API é outra. E dá pra criar as suas.",
     cards([["🖥", "page", "o navegador, pronto"], ["⇄", "request", "a API, pronta", AZUL], ["🔑", "loginPage", "a sua, pronta", AMARELO]], "FIXTURE: O TESTE RECEBE PRONTO")),
    ("Primeiro, os imports: o test do Playwright, e as duas páginas.",
     ed(trecho(PAG, 1, 3), "fixtures/paginas.js", "paginas.js", de=1, ate=3,         criar=[["Na pasta do projeto, cria uma pasta nova chamada fixtures.", "fixtures/"], ["E dentro dela, o arquivo paginas ponto js.", "paginas.js"]])),
    ("Repara no test as base. Traduzindo: traga o test do Playwright, mas chame ele de base. Porque o nome test vai ficar pro nosso test novo, que a gente vai criar agora.",
     tr("import { test as base } from '@playwright/test';", [["test as base", "o test, com o apelido base"], ["'@playwright/test'", "do Playwright"]])),
    ("Agora: export const test igual base ponto extend. Extend quer dizer estender: pegue o test original e acrescente coisas novas nele.",
     ed(trecho(PAG, 1, 5) + "\n});", "base.extend = o test original + coisas novas", "paginas.js", de=5)),
    ("Dentro, a receita do loginPage: ele recebe o page, cria um LoginPage, e entrega pro teste com o use.",
     ed(trecho(PAG, 1, 8) + "\n});", "A receita do loginPage", "paginas.js", de=6, ate=8)),
    ("Traduzindo: loginPage, o nome que o teste vai pedir. Entre chaves, o page, a fixture que já existe. E o use: entregue isto pronto pro teste.",
     tr("loginPage: async ({ page }, use) => { await use(new LoginPage(page)); }",
        [["loginPage:", "o nome"], ["({ page }, use)", "recebe page e use"], ["use(new LoginPage(page))", "entrega pronto"]], 2.2)),
    ("O produtosPage segue a mesma receita. E no fim, exporta o expect também, pra o teste importar tudo de um lugar só.",
     ed(PAG, "A mesma receita pro produtosPage", "paginas.js", de=9, ate=14, fonte=24)),
    ("Agora um teste usando a fixture. Primeira linha, o import: em vez de vir do Playwright, o test vem das suas fixtures. E no teste, você pede o loginPage entre chaves, igual ao page, e já usa.",
     ed(FIX, "Pede o loginPage igual ao page", "fixture.spec.js", de=1, ate=7,
        criar=[["Os testes do nível dois vão ficar numa pasta separada. Dentro de tests, cria uma pasta nova chamada nivel2.", "nivel2/"], ["E dentro dela, o arquivo fixture ponto spec ponto js.", "fixture.spec.js"]])),
    ("Antes, cada teste montava as páginas. Agora ele pede, e elas chegam prontas. O teste fica só com o que importa.",
     cmp("O MESMO TESTE", ["ANTES", "NEW EM CADA TESTE"], ["DEPOIS", "PEDE E CHEGA PRONTO"])),
    ("Quando vale a pena? Quando as mesmas páginas aparecem em muitos testes, que é o caso de quase todo projeto grande. Num arquivo só, com um teste, o new na hora já resolve.",
     trl("QUANDO USAR", [["mesmas páginas em vários testes", "fixture"], ["um teste isolado", "o new na hora resolve"]])),
    ("Roda: continua passando.",
     term(["npx playwright test fixture --project=chromium", ("Running 2 tests using 1 worker", "mut"), ("  ✓  1 [setup] › tests/auth.setup.js:5:6 › faz login uma vez (551ms)", "ac"),
           ("  ✓  2 [chromium] › tests/nivel2/fixture.spec.js:3:5 › o loginPage chega pronto (468ms)", "ac"), ("  2 passed (2.4s)", "ac")], "Continua passando")),
] + fim("dados num arquivo"))

# ---------- 65 · dados num arquivo ----------
DAD = ler("tests/nivel2/dados.spec.js"); JS = ler("dados/usuarios.json")
DENTRO = """const usuarios = [
  { usuario: 'standard_user', resultado: 'sucesso' },
  { usuario: 'problem_user', resultado: 'sucesso' },
  { usuario: 'locked_out_user', resultado: 'bloqueado' },
  { usuario: 'performance_glitch_user', resultado: 'sucesso' },
  { usuario: 'visual_user', resultado: 'sucesso' },
  { usuario: 'error_user', resultado: 'sucesso' },
];

for (const { usuario, resultado } of usuarios) {
  test(`${usuario} - ${resultado}`, async ({ page, loginPage }) => {"""
aula(65, "Os dados ficaram maiores que o teste", [
    ("Lembra da lista de usuários da aula trinta e um? Imagina que agora cada usuário tem também o resultado esperado: uns entram, outro é bloqueado. Olha esse exemplo, não precisa escrever: a lista começa a ficar maior que o próprio teste.",
     ed(DENTRO, "Só um exemplo: a lista maior que o teste", "exemplo (não precisa criar)", destaque=list(range(1, 9)), destaque_em=1.6, pastas=None)),
    ("O teste deveria mostrar o comportamento: entra, e confere. Os dados podem morar num arquivo separado.",
     {"type": "cards", "itens": [["🧪", "O teste", "o comportamento"], ["📄", "Um arquivo de dados", "os usuários e senhas", "#69a7ff"]]}),
    ("Dentro, a lista de usuários, no formato JSON.",
     ed(JS, "dados/usuarios.json", "usuarios.json", de=1, ate=5,
        criar=[["Na pasta do projeto, cria uma pasta nova chamada dados.", "dados/"], ["E dentro dela, o arquivo usuarios ponto json.", "usuarios.json"]])),
    ("JSON você já viu nas aulas de API: chaves, o nome do campo entre aspas, dois pontos, e o valor. Cada par de chaves é um caso de teste.",
     trl("CADA LINHA, UM CASO", [['{ "usuario": "standard_user", "resultado": "sucesso" }', "entra"], ['{ "usuario": "locked_out_user", "resultado": "bloqueado" }', "é bloqueado"]])),
    ("Primeiras linhas: o import das fixtures, como na aula passada, e o import usuarios from, com o caminho do JSON. Pronto: a lista chega no teste.",
     ed(trecho(DAD, 1, 2), "import usuarios from '../../dados/usuarios.json'", "dados.spec.js", de=1, ate=2,
        criar=[["Agora o teste de verdade. Dentro da pasta nivel2, cria o dados ponto spec ponto js.", "dados.spec.js"]])),
    ("E o for que você já conhece. Com um detalhe novo: as chaves dentro do for. Elas pegam de cada caso o usuario e o resultado, cada um na sua variável.",
     ed(trecho(DAD, 1, 5) + "\n  });\n}", "Pegue o usuario e o resultado de cada caso", "dados.spec.js", de=4, ate=5)),
    ("Traduzindo: pra cada caso da lista, pegue os dois campos, usuario e resultado.",
     tr("for (const { usuario, resultado } of usuarios) {", [["{ usuario, resultado }", "pegue os dois campos"], ["of usuarios", "de cada caso do JSON"]])),
    ("Dentro, um if: se o resultado é sucesso, confere que entrou. Se não, confere a mensagem de bloqueado.",
     ed(DAD, "if: se o resultado for sucesso", "dados.spec.js", destaque=[8, 9, 10, 11], destaque_em=0.8)),
    ("If é se. Os três iguais querem dizer: é igual a. E else é senão.",
     tr("if (resultado === 'sucesso') { ... } else { ... }", [["if", "se"], ["===", "é igual a"], ["else", "senão"]], 1.3)),
    ("E por que separar? Um caso novo vira uma linha no JSON, sem mexer no teste. Até quem não programa consegue acrescentar. E quando os dados mudam mais do que o teste, você mexe só no arquivo.",
     cards([["+", "Caso novo", "uma linha no JSON"], ["👥", "Quem não programa", "consegue acrescentar", AZUL], ["✎", "Dados mudaram", "mexe só no arquivo", AMARELO]])),
    ("Quando não usar: se cada caso precisa de passos diferentes, o if começa a crescer, e o teste fica difícil de ler. Aí é melhor testes separados.",
     trl("QUANDO USAR", [["mesmos passos, dados diferentes", "dados num JSON"], ["passos diferentes", "testes separados"]])),
    ("Roda: um teste pra cada caso do arquivo.",
     term(["npx playwright test dados --project=chromium", ("Running 4 tests using 1 worker", "mut"), ("  ✓  1 [setup] › tests/auth.setup.js:5:6 › faz login uma vez (551ms)", "ac"),
           ("  ✓  2 [chromium] › tests/nivel2/dados.spec.js:5:7 › standard_user - sucesso (637ms)", "ac"), ("  ✓  3 [chromium] › tests/nivel2/dados.spec.js:5:7 › problem_user - sucesso (490ms)", "ac"),
           ("  ✓  4 [chromium] › tests/nivel2/dados.spec.js:5:7 › locked_out_user - bloqueado (373ms)", "ac"), ("  4 passed (3.1s)", "ac")], "Um teste pra cada caso")),
] + fim("e se o servidor responder errado?"))

# ---------- 66 · mock ----------
MOCK = ler("tests/nivel2/mock.spec.js")
L_ABORT = ln(MOCK, "route.abort"); L_T1 = ln(MOCK, "servidor fora do ar"); L_T2 = ln(MOCK, "lista vazia"); L_FUL = ln(MOCK, "route.fulfill")
aula(66, "E se o servidor responder errado?", [
    ("O site está funcionando. Mas o que a tela faz se o servidor cair? Ou se ele responder uma lista vazia? Esperar isso acontecer de verdade não dá.", titulo(66, "MOCK")),
    ("E a gente não vai derrubar o servidor da empresa pra descobrir. O Playwright fica no meio da conversa: intercepta o pedido do navegador, e responde do jeito que a gente quiser. Isso é um mock.",
     cards([["🖥", "O navegador", "pede os produtos"], ["🎭", "O Playwright no meio", "intercepta o pedido", AMARELO], ["📦", "A resposta", "você escolhe", AZUL]], "MOCK: O PLAYWRIGHT NO MEIO")),
    ("Pra isso, a Lojinha do Leigo, a loja de treino do curso. Entra com cliente e leigo123: os produtos aparecem.",
     video("n66_loja", "A Lojinha do Leigo", LOJA, LOGIN_LOJA, espera_fim=2500)),
    ("Esses produtos vêm de um endereço da API: api barra produtos ponto json. Abrindo ele no navegador, é a lista, em JSON.",
     {"type": "tela", "media": "n66_json", "url": LOJA + "api/produtos.json", "titulo": LOJA + "api/produtos.json", "legenda": "A lista de produtos, em JSON"}),
    ("Primeiro, a prova de que o Playwright consegue ficar no meio: page ponto route nesse endereço, e route ponto abort. Bloqueie.",
     ed(trecho(MOCK, L_T1, L_T1 + 4), "page.route + route.abort()", "mock.spec.js", linha0=L_T1, de=L_ABORT - L_T1 + 1, pastas=None, criar=[["Dentro da pasta nivel2, cria o mock ponto spec ponto js.", "mock.spec.js"]])),
    ("Traduzindo: route, quando o navegador pedir este endereço. Os dois asteriscos: qualquer coisa antes. E abort: bloqueie, como se o servidor estivesse fora do ar.",
     tr("page.route('**/api/produtos.json', (route) => route.abort());", [["page.route", "quando pedir"], ["'**/api/produtos.json'", "este endereço"], ["route.abort()", "bloqueie"]], 2.0)),
    ("E por que o reload? O login já carregou os produtos. Com o route ligado, a gente recarrega a página, e o pedido novo é bloqueado.",
     ed(trecho(MOCK, L_T1, L_T1 + 4), "reload: pede de novo, agora bloqueado", "mock.spec.js", linha0=L_T1, destaque=[L_ABORT - L_T1 + 2], destaque_em=0.8, pastas=None)),
    ("Olha acontecendo: a loja não conseguiu carregar os produtos, e mostra o aviso. É isso que o teste confere.",
     video("n66_erro", "Servidor fora do ar: o aviso", LOJA + "produtos.html", [{"espera": 800}, {"bloqueia": API}, {"reload": True, "espera": 4500}], pre_url=LOJA, pre_acoes=LOGIN_LOJA, espera_inicio=900)),
    ("Agora o uso mais comum: route ponto fulfill. Responda no lugar do servidor, com o que você quiser. Aqui, uma lista vazia.",
     ed(trecho(MOCK, L_T2, L_T2 + 8), "route.fulfill: responda no lugar do servidor", "mock.spec.js", linha0=L_T2, de=2, ate=6, pastas=None)),
    ("Traduzindo: fulfill, responda você. Status duzentos, deu certo. E o body, o corpo da resposta: os dois colchetes, uma lista vazia.",
     tr("route.fulfill({ status: 200, body: '[]' })", [["route.fulfill", "responda você"], ["status: 200", "deu certo"], ["body: '[]'", "uma lista vazia"]], 1.8)),
    ("E a loja mostra que nenhum produto foi encontrado. O teste confere essa mensagem.",
     video("n66_vazio", "Lista vazia: nenhum produto", LOJA + "produtos.html", [{"espera": 800}, {"responde": [API, "[]"]}, {"reload": True, "espera": 4500}], pre_url=LOJA, pre_acoes=LOGIN_LOJA, espera_inicio=900)),
    ("No trabalho, é assim que se testa o que é difícil de provocar: o servidor fora do ar, a lista vazia, um erro quinhentos, uma resposta lenta. Sem esperar acontecer, e sem estragar nada de verdade.",
     cards([["✗", "Fora do ar", "abort"], ["∅", "Lista vazia", "fulfill com []", AZUL], ["500", "Erro no servidor", "fulfill com status 500", VERM], ["🐢", "Resposta lenta", "espera antes de responder", AMARELO]], "O QUE O MOCK TESTA")),
    ("Quando não usar: pra saber se o servidor de verdade funciona. O mock testa como a tela reage. O servidor você testa com os testes de API, sem mock.",
     trl("QUANDO USAR", [["como a tela reage", "mock"], ["se o servidor funciona", "teste de API, sem mock"]])),
    ("Roda os dois.",
     term(["npx playwright test mock --project=chromium", ("Running 3 tests using 1 worker", "mut"), ("  ✓  1 [setup] › tests/auth.setup.js:5:6 › faz login uma vez (551ms)", "ac"),
           ("  ✓  2 [chromium] › tests/nivel2/mock.spec.js:14:5 › servidor fora do ar (657ms)", "ac"), ("  ✓  3 [chromium] › tests/nivel2/mock.spec.js:20:5 › lista vazia (603ms)", "ac"),
           ("  3 passed (3.4s)", "ac")], "Os dois passaram")),
] + fim("o botão funciona, mas ficou errado"))

# ---------- 67 · visual ----------
VIS = ler("tests/nivel2/visual.spec.js")
SNAP = "tests/nivel2/visual.spec.js-snapshots/login-chromium-win32.png"
aula(67, "O botão funciona, mas ficou errado", [
    ("Essa é a tela de login da Lojinha. Agora imagina que alguém mexeu no estilo do botão Entrar.",
     {"type": "tela", "media": "n67_antes", "url": LOJA, "titulo": "Lojinha do Leigo", "legenda": "Antes", "alvo": "Entrar", "zoom_em": 1.4, "caixa_em": 1.8}),
    ("Olha como ficou: laranja, menor, fora do padrão. Mas ele continua clicável, e o login funciona. Nenhum teste nosso ia reclamar.",
     {"type": "tela", "media": "n67_depois", "url": LOJA + "?estilo=quebrado", "titulo": "Lojinha do Leigo", "legenda": "Depois: o teste continua passando", "alvo": "Entrar", "zoom_em": 1.4, "caixa_em": 1.8}),
    ("Um teste visual percebe. Uma linha: to have screenshot. Tire uma foto da tela e compare com a foto guardada.",
     ed(VIS, "toHaveScreenshot", "visual.spec.js", de=7, criar=[["Dentro da pasta nivel2, cria o visual ponto spec ponto js.", "visual.spec.js"]])),
    ("Traduzindo: eu espero que a página fique igual à foto guardada com o nome login ponto png.",
     tr("await expect(page).toHaveScreenshot('login.png');", [["expect(page)", "eu espero que a página"], ["toHaveScreenshot", "fique igual à foto"], ["('login.png')", "guardada com este nome"]], 1.8)),
    ("Na primeira vez, ainda não existe foto pra comparar. Ele falha, avisa, e guarda a tela de agora como referência.",
     term(["npx playwright test visual --project=chromium", ("Error: A snapshot doesn't exist at", "#ff6b6b"), (SNAP + ", writing actual.", "#ff6b6b"), ("  1 failed", "#ff6b6b")], "1ª vez: guarda a foto de referência")),
    ("A foto fica numa pasta do lado do teste. E o nome leva o navegador e o sistema, porque cada um desenha a tela um pouquinho diferente. Por isso, no time, a foto de referência é tirada na mesma máquina que roda os testes, normalmente a do GitHub.",
     trl("UMA FOTO POR NAVEGADOR E SISTEMA", [["login-chromium-win32.png", "Chromium no Windows"], ["login-chromium-linux.png", "Chromium no Linux (GitHub)"]])),
    ("Roda de novo: agora tem com o que comparar, e a tela está igual. Passou.",
     term(["npx playwright test visual --project=chromium", ("Running 2 tests using 1 worker", "mut"), ("  ✓  1 [setup] › tests/auth.setup.js:5:6 › faz login uma vez (536ms)", "ac"),
           ("  ✓  2 [chromium] › tests/nivel2/visual.spec.js:5:5 › a tela de login não mudou (718ms)", "ac"), ("  2 passed (2.5s)", "ac")], "2ª vez: igual, passou")),
    ("Agora, com o botão mudado. Roda: falhou. Vinte e nove mil pixels diferentes, quatro por cento da tela.",
     term(["npx playwright test visual --project=chromium", ("Error: expect(page).toHaveScreenshot(expected) failed", "#ff6b6b"),
           ("  29083 pixels (ratio 0.04 of all image pixels) are different.", "#ff6b6b"), ("  1 failed", "#ff6b6b")], "Mudou: 4% da tela diferente")),
    ("E o relatório mostra lado a lado: a foto esperada, a tela atual, e a diferença.",
     {"type": "tela", "media": "n67_lado", "url": DIFF, "titulo": "Playwright Test Report", "legenda": "Esperado · atual · diferença"}),
    ("Na aba Diff, o que mudou aparece pintado. O botão inteiro.",
     {"type": "tela", "media": "n67_diff", "url": DIFF + "?diff", "titulo": "Playwright Test Report", "legenda": "Diff: o que mudou aparece pintado"}),
    ("E aí vem a pergunta de QA: foi de propósito? Se foi, você atualiza a foto. Se não foi, você acabou de achar um bug visual, e abre um card com essas três imagens.",
     cmp("FOI DE PROPÓSITO?", ["SIM", "ATUALIZA A FOTO"], ["NÃO", "BUG VISUAL: ABRE UM CARD"])),
    ("Pra atualizar a foto: traço traço update snapshots.",
     term(["npx playwright test visual --update-snapshots"], "Mudou de propósito: atualiza a foto")),
    ("Um cuidado: tela que muda sozinha, como data, hora ou propaganda, faz o teste visual falhar à toa. Use em telas estáveis: login, página de produto, um e-mail, um relatório.",
     trl("QUANDO USAR", [["tela estável: login, produto", "teste visual"], ["data, hora, propaganda", "falha à toa: evite"]])),
] + fim("todos os erros da tela de uma vez"))

# ---------- 68 · soft ----------
SOFT = ler("tests/nivel2/soft.spec.js")
SOFT_V = "\n".join(l for l in SOFT.split("\n") if not l.startswith("// duas"))
aula(68, "Quero ver todos os erros da tela de uma vez", [
    ("Uma tela com várias informações pra conferir. A primeira conferência falha, e o teste para ali. Você corrige, roda de novo, e só então descobre que a quarta também estava errada.",
     cards([["1", "1ª conferência", "falhou: o teste parou", VERM], ["↻", "Corrige e roda", "de novo"], ["4", "4ª conferência", "também estava errada", VERM]], "UM ERRO POR VEZ")),
    ("Pra isso existe o expect ponto soft. Soft é suave: anote o erro, e continue conferindo.",
     ed(SOFT_V, "expect.soft", "soft.spec.js", de=ln(SOFT_V, "entrar"), ate=ln(SOFT_V, "erro"), criar=[["Dentro da pasta nivel2, cria o soft ponto spec ponto js.", "soft.spec.js"]])),
    ("Traduzindo: expect soft, anote o erro e siga. Depois, a conferência de sempre.",
     tr("await expect.soft(page.getByTestId('entrar')).toHaveText('Login');", [["expect.soft", "anote o erro e siga"], ["toHaveText('Login')", "a conferência de sempre"]], 1.6)),
    ("Aqui, quatro conferências na tela de login da Lojinha. Duas erradas de propósito: o botão diz Entrar, e não Login. E a mensagem de erro só aparece depois que alguém erra a senha.",
     ed(SOFT_V, "Duas erradas de propósito", "soft.spec.js", destaque=[ln(SOFT_V, "entrar"), ln(SOFT_V, "'erro'")], destaque_em=1.0)),
    ("Roda: o teste vai até o fim, e mostra os dois erros juntos.",
     term(["npx playwright test soft --project=chromium", ("Error: expect(locator).toHaveText(expected) failed", "#ff6b6b"), ("Expected: \"Login\"", "ac"), ("Received: \"Entrar\"", "#ff6b6b"),
           ("Error: expect(locator).toBeVisible() failed", "#ff6b6b"), ("Expected: visible", "ac"), ("Received: hidden", "#ff6b6b"), ("  1 failed", "#ff6b6b")], "Os dois erros, de uma vez")),
    ("No trabalho: conferir a tela de detalhes de um pedido, o resumo de uma compra, um formulário com dez campos. Você quer a lista completa do que está errado, de uma vez só, pra mandar tudo junto no card.",
     cards([["🧾", "Detalhes do pedido", "vários dados"], ["🛒", "Resumo da compra", "vários valores", AZUL], ["▤", "Formulário grande", "vários campos", AMARELO]], "ONDE O SOFT AJUDA")),
    ("Mas cuidado: nos passos principais do fluxo, o expect normal continua sendo o certo. Se o login falhou, não faz sentido continuar e conferir o carrinho.",
     cmp("QUAL USAR", ["FLUXO: LOGIN, CARRINHO", "EXPECT NORMAL: PARA"], ["DADOS DA MESMA TELA", "EXPECT.SOFT: CONTINUA"])),
] + fim("não dá tempo de rodar tudo"))

# ---------- 69 · tags ----------
TAG = ler("tests/nivel2/tags.spec.js")
aula(69, "Não dá tempo de rodar tudo", [
    ("O time vai fazer uma entrega daqui a meia hora. Tem cento e cinquenta testes, e alguém pergunta: qual o mínimo pra saber se o sistema está de pé?",
     bt(("A PERGUNTA", "muted", 70), ("“Qual o mínimo pra saber se está de pé?”", "white", 70), entre=1.3)),
    ("Pra isso servem as tags: uma etiqueta no teste. Depois do nome, entre chaves: tag, arroba smoke.",
     ed(TAG, "{ tag: '@smoke' }", "tags.spec.js", de=3, pastas=None, criar=[["Dentro da pasta nivel2, cria o tags ponto spec ponto js.", "tags.spec.js"]])),
    ("Traduzindo: esse teste tem a etiqueta smoke.",
     tr("test('login funciona', { tag: '@smoke' }, async ({ page, loginPage }) => {", [["{ tag: '@smoke' }", "a etiqueta smoke"]], 1.0)),
    ("Smoke é fumaça. O nome vem da eletrônica: liga o aparelho e vê se sai fumaça. É o teste rápido de que o básico funciona: entra no sistema, abre a tela principal, faz a compra.",
     cards([["🔌", "Liga o aparelho", "e vê se sai fumaça"], ["✓", "Smoke test", "o básico funciona?", VERDE]])),
    ("Pra rodar só os marcados: traço traço grep arroba smoke.",
     term(["npx playwright test --grep @smoke --project=chromium", ("Running 2 tests using 1 worker", "mut"), ("  ✓  1 [setup] › tests/auth.setup.js:5:6 › faz login uma vez (543ms)", "ac"),
           ("  ✓  2 [chromium] › tests/nivel2/tags.spec.js:3:5 › login funciona @smoke (545ms)", "ac"), ("  2 passed (2.3s)", "ac")], "Só os marcados")),
    ("E o contrário também existe: grep invert. Rode todos, menos os marcados.",
     term(["npx playwright test tags --grep-invert @smoke --project=chromium", ("Running 2 tests using 1 worker", "mut"), ("  ✓  1 [setup] › tests/auth.setup.js:5:6 › faz login uma vez (521ms)", "ac"),
           ("  ✓  2 [chromium] › tests/nivel2/tags.spec.js:9:5 › mostra erro para usuário bloqueado (456ms)", "ac"), ("  2 passed (2.2s)", "ac")], "Todos, menos os marcados")),
    ("Na prática: antes de uma entrega, só os smoke, em poucos minutos. E com mais tempo, toda noite por exemplo, o regressivo completo: todos os testes, pra ver se nada antigo quebrou.",
     trl("NO DIA A DIA", [["antes de uma entrega", "--grep @smoke · minutos"], ["toda noite", "todos: o regressivo"]])),
    ("E dá pra ter outras etiquetas: arroba pagamento, arroba celular, arroba lento. Tag não é enfeite: ela organiza jeitos diferentes de rodar.",
     cards([["💳", "@pagamento", "só o que mexe com dinheiro"], ["📱", "@celular", "só os de tela pequena", AZUL], ["🐢", "@lento", "fora da rodada rápida", AMARELO]])),
] + fim("passou, rodei de novo, falhou"))

# ---------- 70 · flaky ----------
FLK = ler("tests/nivel2/flaky.spec.js")
DEMO = re.sub(r"^// .*\n", "", open(os.path.join(PROJ, "demos", "aula70_flaky.demo.spec.js"), encoding="utf8").read().rstrip("\n"), flags=re.M)
L_WAIT = ln(DEMO, "waitForTimeout"); L_COUNT = ln(DEMO, "count()")
CFG = open(os.path.join(PROJ, "playwright.config.js"), encoding="utf8").read().rstrip("\n")
L_RET = ln(CFG, "retries:")
REP = "npx playwright test aula70 --repeat-each=10 --project=chromium"
aula(70, "Passou. Rodei de novo. Falhou.", [
    ("Olha isso. Rodei esse teste dez vezes seguidas: nove passaram, e uma falhou. Esperava seis produtos, e encontrou zero. E eu não mudei uma linha.",
     term([REP, ("Running 10 tests using 2 workers", "mut"), ("Error: expect(received).toBe(expected)", "#ff6b6b"), ("Expected: 6", "ac"), ("Received: 0", "#ff6b6b"),
           ("  1 failed", "#ff6b6b"), ("  9 passed (52.1s)", "ac")], "10 vezes: 9 passaram, 1 falhou")),
    ("Rodei de novo, o mesmo comando, sem mexer em nada. Dessa vez passaram as dez.",
     term([REP, ("Running 10 tests using 2 workers", "mut"), ("  10 passed (55.0s)", "ac")], "De novo: as 10 passaram")),
    ("Esse é o teste flaky: às vezes passa, às vezes falha, sem nenhuma mudança que explique. E ele é perigoso: o time para de confiar nos testes, e começa a ignorar o vermelho. Até o dia em que o vermelho era um bug de verdade.",
     bt(("FLAKY", "gold", 200), ("ÀS VEZES PASSA, ÀS VEZES FALHA", "white", 80))),
    ("Olha o código. Depois do login, ele espera quatro segundos e meio, fixos, e conta os produtos.",
     ed(DEMO, "Tempo fixo e depois conta", "flaky.demo.spec.js", destaque=[L_WAIT, L_COUNT], destaque_em=1.0, pastas=None, criar=[["Pra ver isso acontecendo, cria dentro da pasta nivel2 um arquivo de exemplo: flaky ponto demo ponto spec ponto js.", "flaky.demo.spec.js"]])),
    ("O problema: esse usuário é lento de propósito. Às vezes a página carrega em quatro segundos, às vezes em cinco. Quando demora mais que a espera, a conta dá zero, e o teste falha.",
     cards([["4s", "Carregou em 4 segundos", "passou", VERDE], ["5s", "Carregou em 5 segundos", "falhou", VERM]], "ESPERA FIXA DE 4,5 SEGUNDOS")),
    ("A reação mais comum é aumentar a espera. Às vezes parece resolver. Mas aí o teste sempre espera, mesmo quando a página já carregou. E no dia em que o sistema levar mais, falha de novo.",
     cmp("AUMENTAR A ESPERA?", ["TEMPO FIXO", "LENTO E AINDA FALHA"], ["ESPERAR O QUE IMPORTA", "RÁPIDO E ESTÁVEL"])),
    ("O caminho certo: esperar o que importa. Um expect que espera sozinho, até o primeiro produto aparecer, como na aula vinte e um.",
     ed(FLK, "Espere o que importa", "flaky.spec.js", de=6, ate=7, pastas=None, criar=[["Agora o teste do jeito certo, num arquivo novo. Dentro da pasta nivel2, cria o flaky ponto spec ponto js.", "flaky.spec.js"]])),
    ("E repara: ele não espera dez segundos. Espera até dez. Apareceu em quatro? Segue em quatro.",
     tr("await expect(produtos.first()).toBeVisible({ timeout: 10000 });", [["toBeVisible", "espere aparecer"], ["{ timeout: 10000 }", "por até 10 segundos"]], 1.4)),
    ("E pra caçar teste instável, o repeat each: roda o mesmo teste várias vezes seguidas. Se falhar uma vez em dez, tem coisa pra investigar.",
     trl("CAÇANDO TESTE INSTÁVEL", [["--repeat-each=10", "roda 10 vezes seguidas"], ["falhou 1 em 10?", "tem coisa pra investigar"]])),
    ("E o retries do config faz o GitHub tentar de novo quando um teste falha. Ajuda, mas guarda essa: retry diminui o estrago, não corrige a causa.",
     ed(trecho(CFG, L_RET - 2, L_RET + 1), "retries: tenta de novo no GitHub", "playwright.config.js", linha0=L_RET - 2, destaque=[3], destaque_em=0.8)),
    ("Então, no trabalho: apareceu um flaky, investiga a causa. Quase sempre é uma espera errada, ou um teste que depende de outro. E evita o tempo fixo.",
     bt(("RETRY DIMINUI O ESTRAGO", "white", 100), ("NÃO CORRIGE A CAUSA", "gold", 120))),
] + fim("o mesmo sistema, três ambientes"))

# ---------- 71 · ambientes ----------
L_BASE = ln(CFG, "baseURL")
CFG71 = trecho(CFG, L_BASE - 1, L_BASE + 1).replace("baseURL: 'https://www.saucedemo.com',", "baseURL: process.env.BASE_URL || 'https://www.saucedemo.com',")
YML71 = """    - name: Run Playwright tests
      run: npx playwright test
      env:
        BASE_URL: https://homologacao.loja.com
        SAUCE_USER: ${{ secrets.SAUCE_USER }}
        SAUCE_PASSWORD: ${{ secrets.SAUCE_PASSWORD }}"""
aula(71, "O mesmo sistema, três ambientes", [
    ("No trabalho, o mesmo sistema existe em vários endereços: o de desenvolvimento, o de homologação, onde o time testa antes de lançar, e o de produção, o de verdade, que o cliente usa.",
     cards([["🛠", "Desenvolvimento", "dev.loja.com"], ["🧪", "Homologação", "homologacao.loja.com", AZUL], ["🌐", "Produção", "loja.com: o cliente usa", AMARELO]], "O MESMO SISTEMA, 3 ENDEREÇOS")),
    ("E a gente não quer mexer no código toda vez que muda de ambiente. Então, na linha do baseURL, antes do endereço, escreve process ponto env ponto BASE underline URL e dois risquinhos. O endereço continua lá, no fim da linha.",
     ed(CFG71, "baseURL lê uma variável", "playwright.config.js", linha0=L_BASE - 1, pastas=None, trocar=[[2, "    baseURL: 'https://www.saucedemo.com',", None, 3.0]])),
    ("Traduzindo: se existir a variável BASE URL, use ela. Os dois risquinhos querem dizer senão. Senão, use o saucedemo.",
     tr("baseURL: process.env.BASE_URL || 'https://www.saucedemo.com'", [["process.env.BASE_URL", "se existir a variável, use ela"], ["||", "senão"], ["'https://www.saucedemo.com'", "use este"]], 1.8)),
    ("Na sua máquina, você escolhe o ambiente na hora de rodar. No Windows, no terminal do VS Code, é assim. E no Mac e no Linux, assim.",
     trl("ESCOLHENDO O AMBIENTE NA HORA", [["$env:BASE_URL=\"https://homologacao.loja.com\"; npx playwright test", "Windows"], ["BASE_URL=https://homologacao.loja.com npx playwright test", "Mac e Linux"]])),
    ("Ou coloca no ponto env, igual o usuário e a senha. E no GitHub Actions, ela fica no yml. O teste continua exatamente igual.",
     ed(YML71, "No GitHub: a variável no yml", "playwright.yml", destaque=[4], destaque_em=0.8, pastas=None)),
    ("E uma regra de ouro: cuidado ao rodar testes em produção. Teste que cria pedido, apaga dado ou manda e-mail não pode rodar no site que o cliente usa.",
     cards([["🧪", "Homologação", "pode tudo"], ["⚠", "Produção", "só o que não muda nada", VERM]], "REGRA DE OURO")),
] + fim("o teste falhou, o que eu mando?"))

# ---------- 72 · evidência ----------
REL72 = {"type": "pw_relatorio", "url": SAUCE, "media": "site_sauce_falha", "acoes": LOGIN, "testes": TRACE6,
         "abrir": {"titulo": "entra com usuário e senha", "status": "falhou", "arquivo": "login.spec.js:8", "projeto": "chromium", "passos": [],
                   "erro": "Error: expect(locator).toContainText(expected) failed\nExpected substring: \"Mochila\"\nReceived string:    \"Sauce Labs Backpack\"", "anexos": True, "anexo_img": "site_sauce_falha", "anexos_em": 1.2},
         "legenda": "O erro, o print, o vídeo e o trace"}
aula(72, "O teste falhou. O que eu mando pro desenvolvedor?", [
    ("Você roda a pipeline, e um teste falha. Mandar só a automação quebrou não ajuda ninguém: quem vai corrigir não sabe nem por onde começar.",
     bt(("“A AUTOMAÇÃO QUEBROU”", "white", 84), ("NÃO AJUDA NINGUÉM", "gold", 96), entre=1.4)),
    ("Primeiro, você investiga. O relatório traz o erro, o print, o vídeo e o trace.", REL72),
    ("O erro diz o esperado e o encontrado. E o trace mostra a página no momento exato da falha.",
     {"type": "pw_trace", "media": "site_sauce_trace", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "passos_pw": A_FALHA, "falhou": True, "erro": ERRO_TRACE,
      "aba": "Errors", "sel_em": 0.6, "legenda": "O trace: a página no momento da falha"}),
    ("E aqui entra a pergunta da aula vinte e seis: é erro do teste, ou bug do sistema? Se o teste estava errado, você mesmo conserta. Se é bug, aí sim vira um card.",
     cmp("QUEM ESTÁ ERRADO?", ["O TESTE", "VOCÊ CONSERTA"], ["O SISTEMA", "VIRA UM CARD"])),
    ("Um card útil tem: um título claro, os passos pra reproduzir, o esperado, o que aconteceu, e as evidências anexadas: o print, o vídeo e o trace.",
     {"type": "tela", "media": "card_bug", "url": CARD_BUG, "titulo": "Card do bug", "legenda": "Título, passos, esperado × obtido, evidências"}),
    ("Repara no título. Não é a automação quebrou. É o que a pessoa vê de errado na tela.",
     trl("O TÍTULO DO CARD", [["A automação quebrou", "não diz nada"], ["Nome do produto aparece em inglês", "diz o problema"]])),
    ("Com um card assim, quem desenvolve reproduz o problema em minutos, sem precisar te chamar pra perguntar nada. Automação também é isso: gerar evidência que ajuda a investigar.",
     bt(("AUTOMAÇÃO TAMBÉM É", "white", 90), ("GERAR EVIDÊNCIA", "gold", 110), entre=1.4)),
] + fim("o que você já consegue fazer"))

# ---------- 73 · o que você já consegue ----------
aula(73, "O que você já consegue fazer", [
    ("Olha o que entrou nesse nível. Primeiro, as telas diferentes: formulário, upload, alerta, aba nova, iframe, mouse por cima, arrastar e tabela.",
     cards([["☑", "Formulário", "check e select"], ["⬆", "Upload", "setInputFiles", AZUL], ["⚠", "Alerta e aba", "antes do clique", AMARELO], ["▣", "Iframe e tabela", "frame e filter", VERDE]], "TELAS DIFERENTES")),
    ("Depois, o Playwright do trabalho: fixtures, dados num arquivo, mock, teste visual, soft, tags, flaky, ambientes e evidência.",
     cards([["🔑", "Fixtures e dados", "o teste limpo"], ["🎭", "Mock e visual", "o difícil de provocar", AZUL], ["🏷", "Soft, tags, flaky", "rodar com inteligência", AMARELO], ["📋", "Ambientes e card", "do jeito do time", VERDE]], "NO TRABALHO")),
    ("Tudo isso está numa página nova da colinha, a página cinco.",
     {"type": "tela", "media": "colinha_pg5", "url": COLINHA, "pagina": 5, "titulo": "colinha-playwright-para-leigos.pdf", "legenda": "Colinha · página 5"}),
    ("E agora eu quero fazer diferente. No próximo módulo, eu não vou começar te mostrando código. Você vai receber uma tarefa, como no trabalho, e vai precisar pensar primeiro.",
     bt(("PRÓXIMO MÓDULO", "muted", 70), ("UMA TAREFA", "white", 120), ("PENSA PRIMEIRO", "gold", 120))),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 14 · PROJETO 2"}),
])


def main():
    out = ["# Roteiros · Módulo 13 do nível 2 (gerado do roteiro_playwright_n2b.py)", ""]
    for slug, p in AULAS:
        for x in p["script"]["long"]["parts"][0]["sentences"]:
            sc = x["scene"]
            if sc.get("gravar") and len(x["text"]) < 90:  # vídeo da loja: tempo pra ver o resultado
                x["pausa"] = 2
            elif sc.get("type") == "terminal" and len(x["text"]) < 60:  # frase curta com a saída: tempo de ler
                x["pausa"] = 2.5
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']}{' [+pausa]' if s.get('pausa') else ''} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "nivel2_modulo13.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

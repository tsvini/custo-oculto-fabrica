"""Gera projetos/curso-playwright-74..80 (nível 2 · módulo 14: projeto 2, pensando como QA, na Lojinha do Leigo). Roteiro: curso-playwright/roteiros/nivel2.md,
com o filtro de qualidade (pra que serve, como faz mostrando, quando usar, uso no trabalho).
Código = curso-playwright/projeto2 (validado no Actions: validar_nivel2.yml, versão 2 passando e versão 1 com as duas falhas reais de ordenação)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, projeto, RAIZ
from roteiro_playwright_m4 import edc
from roteiro_playwright_m11 import desafio

P2 = os.path.join(RAIZ, "curso-playwright", "projeto2")
AZUL, AMARELO, VERM, VERDE, ROXO = "#69a7ff", "#ffd23f", "#ff6b6b", "#3fd68a", "#c792ea"
LOJA = "https://tsvini.github.io/custo-oculto-fabrica/loja/"
CENAS = "repo:curso-playwright/material/cenas/"
ler = lambda r: open(os.path.join(P2, r), encoding="utf8").read().rstrip("\n")
ARV2 = ["projeto-lojinha", "  dados/", "    login.json", "    ordenacao.json", "  fixtures/", "    paginas.js", "  pages/", "    LoginPage.js", "    ProdutosPage.js",
        "  tests/", "    login.spec.js", "    produtos.spec.js", "  .env", "  playwright.config.js", "  README.md"]
PASTA = "C:\\Users\\voce\\Documents\\projeto-lojinha"


def ln(cod, t, n=1):
    a = [i + 1 for i, l in enumerate(cod.split("\n")) if t in l]
    assert len(a) >= n, (t, cod[:100])
    return a[n - 1]


def trecho(cod, de, ate):
    return "\n".join(cod.split("\n")[de - 1:ate])


CRIADOS = []  # o que o aluno já criou na tela, no projeto 2 (o npm init já deu o tests/ e o playwright.config.js)


def arvore2():
    return [l for l in ARV2 if l.strip().rstrip("/") in CRIADOS + ["projeto-lojinha", "tests", "playwright.config.js"]]


def ed(cod, legenda, arquivo, de=None, ate=None, linha0=1, pastas="auto", **kw):
    larg = max(len(l) for l in cod.split("\n"))
    d = dict(arquivo=arquivo, linha0=linha0, fonte=30 if larg <= 50 else 26 if larg <= 64 else 22 if larg <= 84 else 19)
    for _, nome in kw.get("criar", []):
        CRIADOS.append(nome.rstrip("/"))
    if kw.get("criar"):
        kw["criar_arvore"] = arvore2()
    d["pastas"] = (arvore2() if larg <= 56 else None) if pastas == "auto" else pastas
    if de:
        d.update(digitar=True, digitar_de=de, digitar_ate=ate or de)
    d.update(kw)
    return edc(cod, legenda, **d)


def parte(cod, de, ate, legenda, arquivo, destaque=(), **kw):
    """só um pedaço do arquivo (de..ate), com a numeração certa: a letra fica grande"""
    kw.setdefault("pastas", None)
    return ed(trecho(cod, de, ate), legenda, arquivo, linha0=de, destaque=[d - de + 1 for d in destaque], **kw)


def tr(codigo, partes, passo=1.6):
    return {"type": "traducao", "codigo": codigo, "partes": partes, "passo": passo}


def trl(t, linhas):
    return {"type": "traducao", "titulo": t, "linhas": linhas}


def cards(itens, t=None):
    d = {"type": "cards", "itens": itens}
    if t:
        d["titulo"] = t
    return d


def cmp(t, a, b):
    return {"type": "compare", "title": t, "items": [[a[0], a[1], "white"], [b[0], b[1], "gold"]], "size": 90, "stagger": 1.8, "vs": False}


def term(linhas, legenda, fonte=24):
    L = []
    for i, l in enumerate(linhas):
        L.append({"cmd": l, "em": 0.04} if isinstance(l, str) else {"out": l[0], "cor": l[1], "em": min(0.22 + i * 0.045, 0.8)})
    return {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": PASTA, "linhas": L, "legenda": legenda, "fonte": fonte, "fonte_min": 16, "compacto": len(L) > 10}


def video(media, legenda, acoes, url=LOJA, **kw):
    d = {"type": "tela", "media": media, "url": url, "gravar": True, "acoes": list(acoes), "titulo": "Lojinha do Leigo", "legenda": legenda,
         "espera_inicio": 1200, "espera_fim": 2200, "delay_letra": 70}
    d.update(kw)
    return d


def pagina(nome, legenda, alvo=None, media=None):
    d = {"type": "tela", "media": media or nome, "url": CENAS + nome + ".html", "titulo": "Quadro de tarefas", "legenda": legenda}
    if alvo:
        d["alvo"] = alvo
    return d


def entrar(usuario, senha):
    return [{"fill": ["[data-test=\"usuario\"]", usuario]}, {"fill": ["[data-test=\"senha\"]", senha]}, {"click": "[data-test=\"entrar\"]", "espera": 1800}]


def fim(prox):
    return [("Te vejo na próxima!", {"type": "endcard", "sub": "PRÓXIMA: " + prox.upper()})]


AULAS = []


def aula(n, titulo_aula, frases):
    AULAS.append(projeto(n, f"MÓDULO 14 · AULA {n}", titulo_aula, frases))


# ---------- 74 · a missão ----------
aula(74, "A missão", [
    ("Nova tarefa. Você chegou no trabalho, e recebeu este card.", titulo(74, "A MISSÃO")),
    ("Como cliente, quero entrar na loja e ordenar os produtos, pra achar mais fácil o que procuro. Critérios de aceite: nenhum. E o comentário de quem pediu: testa, por favor.",
     pagina("card_historia", "A tarefa: LOJA-87")),
    ("Isso é muito comum no trabalho: uma história curta, sem detalhe nenhum. E é aqui que quem testa faz diferença.",
     bt(("HISTÓRIA CURTA", "white", 110), ("SEM DETALHE", "white", 110), ("QA FAZ A DIFERENÇA", "gold", 110))),
    ("Ainda não abre o VS Code. Primeiro, pensa como QA: o que precisa funcionar? O que pode dar errado? E o que está faltando nessa história? Pausa o vídeo e anota.",
     desafio("?", "Pensa como QA", [["✓", "O que precisa funcionar?"], ["✗", "O que pode dar errado?", VERM], ["?", "O que está faltando?", AMARELO]], legenda="Pausa o vídeo e anota")),
    ("Algumas perguntas que eu faria. Todo usuário pode entrar? E com a senha errada, o que aparece? E se deixar o campo vazio?",
     cards([["👤", "Todo usuário entra?", "e o bloqueado?"], ["🔑", "Senha errada?", "o que aparece?", AZUL], ["▭", "Campo vazio?", "tem aviso?", AMARELO]], "SOBRE ENTRAR")),
    ("E sobre ordenar: quais ordenações precisam existir? Por nome, por preço, nos dois sentidos? E um produto esgotado: ele aparece na lista, ou some? O card não diz.",
     cards([["⇅", "Quais ordenações?", "nome, preço, os dois sentidos?"], ["∅", "Produto esgotado?", "aparece ou some?", VERM], ["?", "O card não diz", "precisa perguntar", AMARELO]], "SOBRE ORDENAR")),
    ("Repara: nenhuma dessas perguntas tem código. E é isso que separa quem só escreve teste de quem testa de verdade: antes do código, a gente entende o problema.",
     bt(("ANTES DO CÓDIGO", "white", 120), ("ENTENDE O PROBLEMA", "gold", 120))),
] + fim("os cenários, em português"))

# ---------- 75 · cenários ----------
aula(75, "Os cenários, em português", [
    ("Agora, a gente transforma a tarefa em situações pra validar. Em português ainda, sem código. Isso se chama levantar os cenários.", titulo(75, "OS CENÁRIOS")),
    ("Primeiro, o caminho principal, o que precisa dar certo: o login válido, os produtos aparecem, e a ordenação funciona.",
     cards([["🔑", "Login válido", "entra na loja"], ["▦", "Os produtos", "aparecem", AZUL], ["⇅", "A ordenação", "funciona", VERDE]], "O CAMINHO PRINCIPAL")),
    ("Depois, os caminhos de erro: senha errada, usuário bloqueado, usuário vazio e senha vazia. Cada um precisa de uma mensagem clara.",
     cards([["🔑", "Senha errada", "mensagem clara", VERM], ["⛔", "Bloqueado", "mensagem clara", VERM], ["▭", "Usuário vazio", "mensagem clara", AMARELO], ["▭", "Senha vazia", "mensagem clara", AMARELO]], "OS CAMINHOS DE ERRO")),
    ("A ordenação, nos quatro sentidos: nome de A a Z, de Z a A, preço do menor pro maior, e do maior pro menor.",
     trl("A ORDENAÇÃO", [["Nome (A a Z)", "alfabética"], ["Nome (Z a A)", "alfabética, ao contrário"], ["Preço (menor para maior)", "do mais barato"], ["Preço (maior para menor)", "do mais caro"]])),
    ("E a pergunta que o card não respondia: o produto esgotado. Você não inventa a resposta: pergunta pra quem pediu, e anota no card. A resposta: ele aparece, mas sem poder comprar.",
     trl("PERGUNTOU, ANOTOU", [["E o produto esgotado?", "pergunta pra quem pediu"], ["Aparece, sem poder comprar", "a resposta, anotada no card"]])),
    ("Também decide o que não é dessa tarefa: pagamento, por exemplo. Saber limitar o escopo é trabalho de QA: senão você testa a loja inteira e não entrega nada.",
     cards([["✓", "Nessa tarefa", "login, lista, ordenação, esgotado", VERDE], ["✗", "Fora do escopo", "pagamento", VERM]], "O ESCOPO")),
    ("E cada cenário que importa vira um teste. Esses nomes vão aparecer, quase iguais, no relatório.",
     trl("CENÁRIO VIRA TESTE", [["login válido", "entra com usuário válido"], ["senha errada", "mostra erro: senha errada"], ["preço do menor pro maior", "ordena por preço do menor para o maior"], ["esgotado", "produto esgotado aparece, mas não dá pra comprar"]])),
] + fim("tem alguma coisa errada aqui"))

# ---------- 76 · o bug ----------
V1 = LOJA + "index.html?versao=1"
aula(76, "Tem alguma coisa errada aqui", [
    ("Antes de automatizar, a gente roda alguns cenários na mão, na versão que o time entregou, a versão um. Isso tem nome: teste exploratório.", titulo(76, "NA MÃO PRIMEIRO")),
    ("Login válido, com cliente e leigo123: entrou. Ok.", video("n76_ok", "Login válido: ok", entrar("cliente", "leigo123"), url=V1, zoom_pagina=1.4)),
    ("Senha errada: aparece Usuário ou senha incorretos. Ok.", video("n76_senha", "Senha errada: ok", entrar("cliente", "errada"), url=V1, zoom_pagina=1.4)),
    ("Usuário bloqueado: aparece que ele está bloqueado. Ok.", video("n76_bloq", "Usuário bloqueado: ok", entrar("bloqueado", "leigo123"), url=V1, zoom_pagina=1.4)),
    ("Agora, ordenar do menor pro maior preço.",
     video("n76_v1", "Preço: do menor pro maior?", [{"scroll": 380, "espera": 700}, {"select": ["[data-test=\"ordenar\"]", "menor"], "espera": 2500}], url=LOJA + "produtos.html", pre_url=V1, pre_acoes=entrar("cliente", "leigo123"), espera_fim=1500)),
    ("Repara nos valores: doze e cinquenta, cento e vinte e nove e noventa, quinze e noventa e nove. E o mais barato, sete e noventa e nove, quase lá no fim.",
     video("n76_precos", "12,50 · 129,90 · 15,99 … e o 7,99?", [{"select": ["[data-test=\"ordenar\"]", "menor"], "espera": 600}, {"scroll": 520, "espera": 4200}, {"scroll": 460, "espera": 4000}],
           url=LOJA + "produtos.html", pre_url=V1, pre_acoes=entrar("cliente", "leigo123"), espera_inicio=600, espera_fim=2500)),
    ("Isso não está em ordem. Antes de escrever uma linha de automação, você acabou de achar um bug.",
     bt(("ANTES DE UMA LINHA DE CÓDIGO", "white", 90), ("VOCÊ ACHOU UM BUG", "gold", 130))),
    ("E por que ele acontece? A loja compara o preço como texto. E em texto, o um vem antes do sete, igual no dicionário. Então doze e cento e vinte e nove vêm antes do sete.",
     trl("COMPARANDO COMO TEXTO", [["\"12,50\" × \"7,99\"", "o 1 vem antes do 7"], ["\"129,90\" × \"15,99\"", "12 vem antes de 15"], ["como número", "7,99 é o menor"]])),
    ("É exatamente por isso que a gente pensou nos cenários antes de abrir o editor. Quem começa direto no código testa o que lembrou. Quem pensa primeiro testa o que importa.",
     cmp("COMEÇAR PELO QUÊ?", ["DIRETO NO CÓDIGO", "TESTA O QUE LEMBROU"], ["PELOS CENÁRIOS", "TESTA O QUE IMPORTA"])),
    ("Agora, registra: o título dizendo o problema, o passo a passo, o esperado, o que aconteceu, e o print.",
     pagina("card_bug_loja", "O card do bug")),
    ("O time corrigiu e entregou a versão dois. Abre de novo e ordena: agora sim, do menor pro maior. Agora a gente automatiza, pra esse bug nunca mais voltar sem ninguém ver.",
     video("n76_v2", "Versão 2: corrigido", [{"select": ["[data-test=\"ordenar\"]", "menor"], "espera": 900}, {"scroll": 520, "espera": 3000}, {"scroll": 460, "espera": 2500}],
               url=LOJA + "produtos.html", pre_url=LOJA, pre_acoes=entrar("cliente", "leigo123"), espera_inicio=600, espera_fim=1500)),
] + fim("começando o projeto organizado"))

# ---------- 77 · projeto organizado ----------
CFG2 = ler("playwright.config.js")
aula(77, "Começando o projeto organizado", [
    ("Um projeto Playwright novo, numa pasta nova: projeto lojinha. Mas desta vez, você não está começando do zero.",
     term(["npm init playwright@latest", ("✔ Do you want to use TypeScript or JavaScript? · JavaScript", "mut"), ("✔ Where to put your end-to-end tests? · tests", "mut"),
           ("✔ Add a GitHub Actions workflow? (y/N) · true", "mut"), ("✔ Success! Created a Playwright Test project", "ac"), "npm install -D dotenv"], "Projeto novo, do mesmo jeito do primeiro")),
    ("Você já sabe do que vai precisar: pages, pros Page Objects. Fixtures, pra entregar as páginas prontas. Dados, pros casos de login e de ordenação. E os testes.",
     cards([["📄", "pages/", "LoginPage e ProdutosPage"], ["🔑", "fixtures/", "as páginas prontas", AZUL], ["{ }", "dados/", "login e ordenação", AMARELO], ["✓", "tests/", "login e produtos", VERDE]], "A ESTRUTURA")),
    ("E no config: o dotenv lá em cima, o baseURL da Lojinha, já lendo a variável de ambiente, e o testIdAttribute, porque a Lojinha também usa data-test.",
     ed(CFG2, "dotenv, baseURL e testIdAttribute", "playwright.config.js", destaque=[ln(CFG2, "dotenv.config"), ln(CFG2, "baseURL"), ln(CFG2, "testIdAttribute")], destaque_em=1.0, pastas=None,
        rolar=True, rolar_de=0.5, rolar_dur=1.0, criar=[['Primeiro, as pastas que você já sabe que vai precisar. Na pasta do projeto, cria a pasta pages.', 'pages/'], ['A pasta fixtures.', 'fixtures/'], ['E a pasta dados.', 'dados/']])),
    ("Dentro, o usuário e a senha da Lojinha. Repara na última linha, comentada: a versão. Com ela, dá pra apontar os testes pra versão um, a do bug.",
     ed(ler(".env.example"), "O .env do projeto 2", ".env", destaque=[3], destaque_em=1.6, criar=[['Na pasta do projeto, cria o arquivo ponto env.', '.env']])),
    ("Repara: no primeiro projeto, cada uma dessas coisas era novidade, e a gente foi colocando uma por vez. Agora você escolhe a estrutura no começo, com intenção.",
     cmp("A ESTRUTURA", ["PROJETO 1", "UMA NOVIDADE POR VEZ"], ["PROJETO 2", "ESCOLHIDA NO COMEÇO"])),
] + fim("page objects e fixture"))

# ---------- 78 · page objects e fixture ----------
LP = ler("pages/LoginPage.js"); PP = ler("pages/ProdutosPage.js"); FX = ler("fixtures/paginas.js")
L_ABRIR = ln(LP, "async abrir"); L_ORD = ln(PP, "async ordenarPor"); L_LER = ln(PP, "async lerPrecos"); L_PROD = ln(PP, "produto(nome)")
aula(78, "Page Objects e fixture", [
    ("O LoginPage, com a receita que você já conhece: os campos, o botão, a mensagem de erro, e o entrar.",
     parte(LP, 1, 8, "LoginPage: a mesma receita", "LoginPage.js", destaque=list(range(2, 8)), destaque_em=0.8, criar=[['Dentro da pasta pages, cria o LoginPage ponto js.', 'LoginPage.js']])),
    ("E uma ação nova, o abrir. Ela abre a loja, e se o ponto env tiver a versão, acrescenta o interrogação versão no endereço.",
     parte(LP, L_ABRIR, L_ABRIR + 3, "abrir(): a versão vem do .env", "LoginPage.js", destaque=[L_ABRIR + 1, L_ABRIR + 2], destaque_em=0.8, fonte=30)),
    ("Traduzindo: v é a versão que veio do ponto env. O interrogação quer dizer então: se tiver a versão, abre index ponto html interrogação versão igual a ela. Os dois pontos querem dizer senão: senão, só o index ponto html.",
     tr("v ? `index.html?versao=${v}` : 'index.html'", [["v ?", "se tiver a versão, então"], ["`index.html?versao=${v}`", "index.html?versao=1"], [": 'index.html'", "senão, index.html"]], 2.2)),
    ("Agora o ProdutosPage. Os elementos: o título, a caixa de ordenar, os produtos, os preços e os nomes. E a ação de ordenar, com o select option que você já conhece.",
     parte(PP, 1, L_ORD + 2, "ProdutosPage: elementos e ordenarPor", "ProdutosPage.js", destaque=[L_ORD, L_ORD + 1], destaque_em=1.8, fonte=24, criar=[['Dentro de pages, cria o ProdutosPage ponto js.', 'ProdutosPage.js']])),
    ("E uma ação que lê os preços da tela. Primeiro, all text contents: pegue o texto de todos os preços, numa lista.",
     parte(PP, L_LER - 1, L_LER + 5, "allTextContents: o texto de todos", "ProdutosPage.js", destaque=[L_LER + 1], destaque_em=0.8)),
    ("Só que eles vêm como texto: R$ doze, vírgula, cinquenta. E pra comparar, a gente precisa de número. Então, pra cada texto: tira o R$, tira o ponto do milhar, troca a vírgula por ponto, e transforma em número.",
     trl("DE TEXTO PRA NÚMERO", [["\"R$ 1.234,56\"", "o texto da tela"], [".replace('R$', '')", "tira o R$"], [".replace(/\\./g, '')", "tira o ponto do milhar"], [".replace(',', '.')", "vírgula vira ponto"], ["Number(...)", "1234.56: um número"]])),
    ("Por que a vírgula vira ponto? Porque o JavaScript escreve número do jeito americano: sete ponto noventa e nove. Com vírgula, ele não entende.",
     cmp("O MESMO PREÇO", ["\"7,99\"", "TEXTO: NÃO DÁ PRA COMPARAR"], ["7.99", "NÚMERO: DÁ PRA ORDENAR"])),
    ("E o produto, que acha o card de um produto pelo nome, com o filter has text da aula sessenta e três.",
     parte(PP, L_PROD, L_PROD + 2, "produto(nome): o card pelo nome", "ProdutosPage.js", destaque=[L_PROD, L_PROD + 1], destaque_em=0.8, fonte=30)),
    ("E a fixture que entrega os dois prontos pros testes. Igual à do módulo treze.",
     ed(FX, "A fixture: as duas páginas prontas", "paginas.js", fonte=24, criar=[['Dentro da pasta fixtures, cria o paginas ponto js.', 'paginas.js']])),
    ("Repara como foi mais rápido da segunda vez. Não porque a gente pulou explicação: porque agora você conhece a receita, e só aplica.",
     bt(("MAIS RÁPIDO", "white", 120), ("PORQUE VOCÊ CONHECE A RECEITA", "gold", 90))),
] + fim("automatizando os cenários"))

# ---------- 79 · automatizando ----------
LS = ler("tests/login.spec.js"); LJ = ler("dados/login.json"); PS = ler("tests/produtos.spec.js"); OJ = ler("dados/ordenacao.json")
L_SORT = ln(PS, ".sort("); L_FOR = ln(PS, "for (const o"); L_REV = ln(PS, "reverse()"); L_EQ = ln(PS, "toEqual"); L_DIS = ln(PS, "toBeDisabled"); L_TAG = ln(PS, "@smoke")
aula(79, "Agora sim, automatizando os cenários", [
    ("A lista de cenários vira teste. Começando pelo login: os quatro casos de erro moram no login ponto json, cada um com o usuário, a senha, e a mensagem esperada.",
     ed(LJ, "dados/login.json: os casos de erro", "login.json", pastas=None, fonte=26, rolar=True, rolar_de=3.0, rolar_dur=3.5, criar=[['Dentro da pasta dados, cria o login ponto json.', 'login.json']])),
    ("E o teste: o login válido, com a etiqueta smoke. E um for pelos casos do JSON, conferindo a mensagem de cada um.",
     parte(LS, ln(LS, "const smoke"), len(LS.split("\n")) - 1, "login.spec.js: o válido e os casos do JSON", "login.spec.js", destaque=[ln(LS, "const smoke"), ln(LS, "for (const caso"), ln(LS, "caso.mensagem")], destaque_em=1.0, criar=[['Dentro de tests, cria o login ponto spec ponto js.', 'login.spec.js']])),
    ("A ordenação: os quatro sentidos no ordenacao ponto json. Qual opção escolher, o nome do cenário, o campo, e o sentido.",
     ed(OJ, "dados/ordenacao.json: os 4 sentidos", "ordenacao.json", pastas=None, fonte=26, rolar=True, rolar_de=3.0, rolar_dur=3.0, criar=[['Dentro de dados, cria o ordenacao ponto json.', 'ordenacao.json']])),
    ("No teste, um for pelos quatro. Escolhe a opção, e lê da tela os preços ou os nomes.",
     parte(PS, L_FOR, L_FOR + 12, "Um teste pra cada sentido", "produtos.spec.js", destaque=[L_FOR, ln(PS, "ordenarPor"), ln(PS, "const naTela")], destaque_em=1.0, criar=[['Dentro de tests, cria o produtos ponto spec ponto js.', 'produtos.spec.js']])),
    ("E agora, a parte mais importante: como conferir que está em ordem? A gente pega a lista da tela, faz uma cópia, e ordena a cópia do jeito certo. Se a tela estiver certa, as duas ficam iguais.",
     cards([["👀", "A lista da tela", "do jeito que a loja mostrou"], ["⧉", "Uma cópia", "ordenada do jeito certo", AZUL], ["=", "Compara as duas", "iguais: passou", VERDE]], "CONFERINDO A ORDEM")),
    ("Traduzindo: os três pontinhos entre colchetes, faça uma cópia. Sort, ordene. A menos b, do menor pro maior, como número. E locale compare, em ordem alfabética, pros nomes.",
     tr("const esperado = [...naTela].sort((a, b) => a - b);", [["[...naTela]", "uma cópia da lista"], [".sort(", "ordene"], ["(a, b) => a - b", "do menor pro maior"]], 2.0)),
    ("Se o sentido é decrescente, reverse: inverta a lista. E o to equal compara as duas listas inteiras, item por item.",
     parte(PS, L_FOR, L_FOR + 12, "reverse e toEqual: a lista inteira", "produtos.spec.js", destaque=[L_REV, L_EQ], destaque_em=0.8)),
    ("Repara na diferença pro desafio quatro: lá, a gente conferia só o primeiro preço. Aqui, a lista inteira. E é isso que pega o bug da versão um, que tinha o primeiro errado e o resto embaralhado.",
     cmp("CONFERIR O QUÊ?", ["SÓ O PRIMEIRO", "PODE DEIXAR PASSAR"], ["A LISTA INTEIRA", "PEGA O BUG"])),
    ("E a etiqueta: só o teste do menor preço ganha o smoke. É o interrogação de novo: se a opção for menor, a etiqueta smoke. Senão, nenhuma.",
     parte(PS, L_FOR, L_FOR + 3, "Só o do menor preço é smoke", "produtos.spec.js", destaque=[L_TAG], destaque_em=0.8)),
    ("E o esgotado, do jeito que a pessoa respondeu: ele aparece, com a etiqueta de esgotado, e o botão de adicionar desabilitado. To be disabled: esteja desabilitado.",
     parte(PS, L_DIS - 3, L_DIS + 1, "toBeDisabled: aparece, mas não dá pra comprar", "produtos.spec.js", destaque=[L_DIS - 1, L_DIS], destaque_em=0.8)),
    ("Roda tudo na versão dois: dez testes, todos passando.",
     term(["npx playwright test --project=chromium --reporter=list", ("Running 10 tests using 1 worker", "mut"),
           ("  ✓   1 › Login › entra com usuário válido @smoke (590ms)", "ac"), ("  ✓   2 › Login › mostra erro: senha errada (362ms)", "ac"),
           ("  ✓   3 › Login › mostra erro: usuário bloqueado (363ms)", "ac"), ("  ✓   4 › Login › mostra erro: usuário vazio (367ms)", "ac"),
           ("  ✓   5 › Login › mostra erro: senha vazia (343ms)", "ac"), ("  ✓   6 › Produtos › ordena por nome de A a Z (412ms)", "ac"),
           ("  ✓   7 › Produtos › ordena por nome de Z a A (408ms)", "ac"), ("  ✓   8 › Produtos › ordena por preço do menor para o maior @smoke (414ms)", "ac"),
           ("  ✓   9 › Produtos › ordena por preço do maior para o menor (428ms)", "ac"), ("  ✓  10 › Produtos › produto esgotado aparece, mas não dá pra comprar (382ms)", "ac"),
           ("  10 passed (4.9s)", "ac")], "Versão 2: os 10 passando", fonte=20)),
    ("E se alguém apontar pra versão um? Liga o LOJA VERSÃO igual a um no ponto env, e roda os testes de produtos.",
     ed(ler(".env.example").replace("# LOJA_VERSAO=1   <- descomente pra testar a versão antiga, com o bug", "LOJA_VERSAO=1"), "LOJA_VERSAO=1: a versão do bug", ".env", trocar=[[3, "# LOJA_VERSAO=1   <- descomente pra testar a versão antiga, com o bug", None, 1.4]])),
    ("Os dois testes de preço ficam vermelhos. Os de nome e o do esgotado continuam verdes: o bug é só no preço.",
     term(["npx playwright test produtos --project=chromium", ("  ✓  1 › Produtos › ordena por nome de A a Z (577ms)", "ac"), ("  ✓  2 › Produtos › ordena por nome de Z a A (426ms)", "ac"),
           ("  ✘  3 › Produtos › ordena por preço do menor para o maior @smoke (441ms)", VERM), ("  ✘  4 › Produtos › ordena por preço do maior para o menor (574ms)", VERM),
           ("  ✓  5 › Produtos › produto esgotado aparece, mas não dá pra comprar (517ms)", "ac"), ("  2 failed", VERM), ("  3 passed (4.3s)", "ac")], "Versão 1: os dois de preço ficam vermelhos", fonte=22)),
    ("E olha o erro: com o sinal de menos, em verde, o que era esperado. Com o mais, em vermelho, o que veio. O sete e noventa e nove, que devia ser o primeiro, lá embaixo.",
     {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": PASTA, "fonte": 24, "fonte_min": 18, "compacto": True, "legenda": "Esperado × recebido: o 7.99 lá embaixo",
      "destaque": [4, 11], "destaque_em": 1.2,
      "linhas": [{"out": l, "cor": c, "ja": True} for l, c in [("Error: expect(received).toEqual(expected)", VERM), ("- Expected  - 3", "ac"), ("+ Received  + 3", VERM), ("  Array [", "mut"),
                 ("-   7.99,", "ac"), ("-   9.99,", "ac"), ("    12.5,", "mut"), ("+   129.9,", VERM), ("    15.99,", "mut"), ("    39.9,", "mut"), ("    59.9,", "mut"), ("+   7.99,", VERM),
                 ("    89.9,", "mut"), ("-   129.9,", "ac"), ("+   9.99,", VERM), ("  ]", "mut")]]}),
    ("Ou seja: se esse bug voltar um dia, ninguém precisa achar ele na mão de novo. A automação pega sozinha. É pra isso que serve um teste automatizado.",
     bt(("O BUG VOLTOU?", "white", 110), ("A AUTOMAÇÃO PEGA SOZINHA", "gold", 110))),
] + fim("do card à pipeline"))

# ---------- 80 · do card à pipeline ----------
README = ler("README.md")
aula(80, "Do card à pipeline", [
    ("Agora, o caminho que você já conhece: o repositório no GitHub, os secrets com o usuário e a senha da Lojinha, e o GitHub Actions. Push, e a pipeline roda.",
     {"type": "gh_actions", "usuario": "voce", "repo": "projeto-lojinha", "workflow": "Playwright Tests", "commit": "cenários da LOJA-87", "inicio_em": 1.0, "legenda": "A pipeline rodando"}),
    ("Verde: passou. E de agora em diante, toda mudança na loja passa por esses testes.",
     {"type": "gh_actions", "usuario": "voce", "repo": "projeto-lojinha", "workflow": "Playwright Tests", "commit": "cenários da LOJA-87", "pronto": True, "status": "ok", "artefato": "playwright-report", "legenda": "Verde"}),
    ("E um README que conta a história: os cenários, o que ficou fora do escopo, e o bug que você achou. Quem abrir o seu projeto entende o que você fez, sem rodar nada.",
     ed(README, "README: os cenários e o bug que você achou", "README.md", pastas=None, rolar=True, rolar_de=1.5, rolar_dur=2.0, criar=[['Na pasta do projeto, cria o README ponto md.', 'README.md']])),
    ("Olha o caminho inteiro que você fez. Recebeu o card. Levantou as dúvidas. Escreveu os cenários. Testou na mão. E achou um bug.",
     cards([["📋", "O card", "uma história curta"], ["?", "As dúvidas", "o que faltava", AMARELO], ["✎", "Os cenários", "em português", AZUL], ["🐞", "O bug", "achado na mão", VERM]], "O CAMINHO, PARTE 1")),
    ("Depois: o time corrigiu, você automatizou o que importa, subiu pro GitHub, e colocou pra rodar sozinho.",
     cards([["🔧", "A correção", "versão 2"], ["▶", "A automação", "10 testes", VERDE], ["⑂", "O GitHub", "o portfólio", AZUL], ["✓", "A pipeline", "roda sozinha", VERDE]], "O CAMINHO, PARTE 2")),
    ("Isso é muito mais importante do que saber escrever page ponto click. Você recebeu uma tarefa, pensou, achou um problema, automatizou o que importa, e colocou pra rodar sozinho.",
     bt(("MAIS QUE PAGE.CLICK", "white", 110), ("PENSOU · ACHOU · AUTOMATIZOU", "gold", 90))),
    ("E agora são dois projetos no seu GitHub. E numa entrevista, quando perguntarem conta um bug que você achou, você tem uma história de verdade pra contar.",
     bt(("2 PROJETOS NO GITHUB", "white", 110), ("+ UMA HISTÓRIA PRA ENTREVISTA", "gold", 90))),
    ("Última parte: carreira.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Carreira"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 15 · CARREIRA"}),
])


def main():
    out = ["# Roteiros · Módulo 14 do nível 2 (gerado do roteiro_playwright_n2c.py)", ""]
    for slug, p in AULAS:
        for x in p["script"]["long"]["parts"][0]["sentences"]:
            sc = x["scene"]
            if sc.get("gravar") and len(x["text"]) < 90:
                x["pausa"] = 2
            elif sc.get("type") == "terminal" and len(x["text"]) < 60:
                x["pausa"] = 3
            elif sc.get("type") == "desafio":
                x["pausa"] = 6
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']}{' [+pausa]' if s.get('pausa') else ''} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "nivel2_modulo14.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

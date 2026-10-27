"""Gera projetos/curso-playwright-35..42 (módulo 8: projeto final). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Código = tests/etapas/aula35..42.spec.js e pages/*.js (validados no Actions; o projeto final é igual ao que as aulas constroem)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m3 import codigo, ARV, SAUCE, LOGIN, CMD_HEADED
from roteiro_playwright_m4 import edc, CMD
from roteiro_playwright_m7 import ARV_U

PROJ = os.path.join(RAIZ, "curso-playwright", "projeto")
ler = lambda r: open(os.path.join(PROJ, r), encoding="utf8").read().rstrip("\n")


def cod(n):
    """código da etapa como o aluno vê: sem o 'aula NN:' do nome e com o import de pages a partir de tests/"""
    import re
    return re.sub(r"aula \d+: ", "", codigo(n)).replace("'../../pages/", "'../pages/")


def ln(c, trecho, n=1):
    """número da n-ésima linha que contém o trecho"""
    achou = [i + 1 for i, l in enumerate(c.split("\n")) if trecho in l]
    assert len(achou) >= n, (trecho, c[:200])
    return achou[n - 1]


def parcial(c, ate, fecha=("  });", "});")):
    """o arquivo só até a linha 'ate', fechando o que ficou aberto (o resto ainda não foi escrito)"""
    return "\n".join(c.split("\n")[:ate] + list(fecha))


def trecho(c, de, ate):
    return "\n".join(c.split("\n")[de - 1:ate])


ARV_C = ARV_U[:ARV_U.index("    login.spec.js")] + ["    compra.spec.js"] + ARV_U[ARV_U.index("    login.spec.js"):]
ARV_P = ARV_C[:1] + ["  .github/", "  node_modules/", "  pages/", "    LoginPage.js"] + ARV_C[3:]
ARV_P3 = ARV_P[:5] + ["    CheckoutPage.js", "    ProdutosPage.js"] + ARV_P[5:]
ARV_P3 = [ARV_P3[0], ARV_P3[1], ARV_P3[2], ARV_P3[3], "    CheckoutPage.js", "    LoginPage.js", "    ProdutosPage.js"] + ARV_P3[7:]
ARV_AUTH = ARV_P3[:ARV_P3.index("    compra.spec.js")] + ["    auth.setup.js"] + ARV_P3[ARV_P3.index("    compra.spec.js"):]
VERM = "#ff6b6b"
COMPRA = LOGIN + [{"click": "[data-test=\"add-to-cart-sauce-labs-backpack\"]"}, {"click": "[data-test=\"shopping-cart-link\"]"}, {"click": "[data-test=\"checkout\"]"},
                  {"fill": ["[data-test=\"firstName\"]", "Maria"]}, {"fill": ["[data-test=\"lastName\"]", "Silva"]}, {"fill": ["[data-test=\"postalCode\"]", "88000-000"]},
                  {"click": "[data-test=\"continue\"]"}, {"click": "[data-test=\"finish\"]"}]


def rodando(c, de, ate, legenda, acoes, media, saida=("  1 passed (3.4s)", "ac"), cmd="npx playwright test compra.spec.js --headed --project=chromium", arquivo="compra.spec.js", pastas=ARV_C, extra=None, **kw):
    """VS Code com o trecho do teste em cima, o comando no terminal e o navegador real fazendo tudo por cima"""
    nav = {"media": media, "url": SAUCE, "gravar": True, "acoes": acoes, "espera_inicio": 800, "espera_fim": 1400, "delay_letra": 60, "titulo": "Chromium", "em": 0.1, "ate": 0.84}
    nav.update(extra or {})
    return edc(trecho(c, de, ate), legenda, arquivo=arquivo, pastas=pastas, linha0=de,
               terminal=[{"cmd": cmd, "em": 0.03}, {"out": ("Running 1 test using 1 worker" if saida[0].strip().startswith("1 ") else f"Running {saida[0].split()[0]} tests using {saida[0].split()[0]} workers"), "cor": "mut", "em": 0.08}, {"out": saida[0], "cor": saida[1], "em": 0.86}], navegador=nav, **kw)



def dev36(media, acoes, dt, attrs, legenda):
    """devtools no saucedemo: botão direito › Inspecionar no elemento com esse data-test"""
    return {"type": "devtools", "media": media, "url": SAUCE, "acoes": acoes, "inspecionar": f"[data-test=\"{dt}\"]",
            "attrs": attrs, "realce": ["data-test"], "realce_em": 4.0, "realce_rotulo": dt, "legenda": legenda}


AULAS = []

# ---------- Aula 35 ----------
C35 = cod(35)
L_TESTE35 = ln(C35, "test('compra")
L_ADD = ln(C35, "add-to-cart")
L_BADGE = ln(C35, "shopping-cart-badge")
AULAS.append(projeto(35, "MÓDULO 8 · AULA 35", "O carrinho", [
    ("Começa o projeto final: o fluxo de compra completo, do login até o obrigado. Hoje, o carrinho.", titulo(35, "O CARRINHO")),
    ("Por que começar pela compra? Porque é onde a loja ganha dinheiro. Se o carrinho quebra, ninguém compra. Se o checkout quebra, ninguém paga. É o primeiro fluxo que as empresas automatizam.", {"type": "cards", "itens": [["🔑", "Login", "quebrou: ninguém entra"], ["🛒", "Carrinho", "quebrou: ninguém compra", "#69a7ff"], ["💳", "Checkout", "quebrou: ninguém paga", "#ff6b6b"]], "titulo": "O CAMINHO DO DINHEIRO"}),  # pra que / quando
    ("Depois do login, cada produto tem um botão Add to cart. Clica com o botão direito e Inspecionar: data-test igual add-to-cart-sauce-labs-backpack.",
     {"type": "devtools", "media": "site_sauce_produtos_dev", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"add-to-cart-sauce-labs-backpack\"]",
      "attrs": ["class", "data-test", "id", "name"], "realce": ["data-test"], "realce_em": 4.0, "realce_rotulo": "este", "legenda": "data-test do botão Add to cart"}),
    ("Primeira linha, o import de sempre. E o describe, a caixa dos testes, agora com o nome Compra.",
     edc(parcial(C35, 3, ("});",)), "import + describe('Compra')", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=1, digitar_ate=3, fonte=26,
         criar=[["Agora, um arquivo de teste novo pra compra. Dentro da pasta tests, cria o compra ponto spec ponto js.", "compra.spec.js"]])),
    ("Dentro, o before each. Todo teste de compra começa com a pessoa já logada, então aqui vai o goto e o login inteiro: usuário, senha e o clique. São as mesmas linhas do login ponto spec, que você escreveu nas aulas vinte e três e vinte e quatro: pode copiar de lá e colar aqui.",
     edc(parcial(C35, L_TESTE35 - 2, ("});",)), "beforeEach: abre o site e faz o login", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=4, digitar_ate=L_TESTE35 - 2, fonte=24)),
    ("Agora o teste: test, e o nome, compra uma mochila do começo ao fim. E o primeiro passo, o clique no Add to cart. O data-test é aquele que a gente achou no Inspecionar: add-to-cart-sauce-labs-backpack. Então: get by test id, esse nome entre aspas, ponto click.",
     edc(parcial(C35, L_ADD), "getByTestId('add-to-cart-sauce-labs-backpack').click()", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_TESTE35, digitar_ate=L_ADD, fonte=22)),
    ("E como saber que o clique funcionou? Olha o carrinho lá em cima: depois do Add to cart, aparece um numerozinho vermelho com um. Botão direito nele, Inspecionar: data-test igual shopping-cart-badge, a bolinha do carrinho.",
     dev36("site_sauce_badge_dev", COMPRA[:4], "shopping-cart-badge", ["class", "data-test"], "O numerozinho: data-test=\"shopping-cart-badge\"")),
    ("Então a conferência no código: o nome que a gente acabou de ver no Inspecionar, shopping-cart-badge. Get by test id, esse nome, ponto to have text, um. Se o numerozinho mostrar um, a mochila entrou no carrinho.",
     edc(C35, "shopping-cart-badge = o numerozinho do carrinho", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_BADGE, digitar_ate=L_BADGE, fonte=22)),
    ("E por que conferir? Sem essa linha, o teste só clica. Se o botão Add to cart estivesse quebrado, ele passaria do mesmo jeito. Teste sem conferência não testa nada.",
     {"type": "compare", "title": "A CONFERÊNCIA", "items": [["SÓ CLICA", "PASSA ATÉ COM BUG", "white"], ["CLICA E CONFERE", "PEGA O BUG", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),
    ("Roda com o navegador aparecendo: olha ele entrando, clicando em Add to cart, e o carrinho mostrando um.",
     rodando(C35, L_TESTE35, L_BADGE + 1, "O carrinho mostrou 1", LOGIN + [{"click": "[data-test=\"add-to-cart-sauce-labs-backpack\"]"}], "rec_carrinho")),
    ("Na próxima aula: terminando o fluxo.", proxima("finalizando a compra")[0]),
    ("Te vejo lá!", proxima("finalizando a compra")[1]),
]))

# ---------- Aula 36 ----------
C36 = cod(36)
L_CART = ln(C36, "shopping-cart-link"); L_CHECK = ln(C36, "'checkout'"); L_FIRST = ln(C36, "firstName"); L_CONT = ln(C36, "'continue'")
L_FIN = ln(C36, "'finish'"); L_HEADER = ln(C36, "complete-header"); L_T36 = ln(C36, "test('compra")
AULAS.append(projeto(36, "MÓDULO 8 · AULA 36", "Finalizando a compra", [
    ("Hoje o robô completa o fluxo inteiro da compra: carrinho, dados, revisão e finalização. É um site de treino, então nenhuma compra de verdade acontece.", titulo(36, "FINALIZANDO")),
    ("Primeiro, vamos olhar o caminho no site. Depois do Add to cart, o carrinho lá em cima, à direita, mostra um. Clica com o botão direito nele e Inspecionar: data-test igual shopping-cart-link.",
     dev36("site_sauce_cart_dev", COMPRA[:4], "shopping-cart-link", ["class", "data-test"], "O carrinho: data-test=\"shopping-cart-link\"")),
    ("Clicando nele, abre a tela do carrinho, com a mochila dentro. Lá embaixo, o botão Checkout, que quer dizer finalizar a compra. O data-test dele é checkout.",
     dev36("site_sauce_checkout_dev", COMPRA[:5], "checkout", ["class", "data-test", "id", "name"], "O botão Checkout: data-test=\"checkout\"")),
    ("Agora no código, as duas linhas: get by test id shopping-cart-link, ponto click, pra abrir o carrinho. E get by test id checkout, ponto click.",
     edc(parcial(C36, L_CHECK), "shopping-cart-link e checkout", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_CART, digitar_ate=L_CHECK, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("O checkout leva pra tela de dados, com três campos: nome, sobrenome e CEP. Os data-test são firstName, lastName e postalCode.",
     {"type": "devtools", "media": "site_sauce_dados_dev", "url": SAUCE, "acoes": COMPRA[:6], "inspecionar": "[data-test=\"firstName\"]", "aberto": True,
      "attrs": ["class", "placeholder", "data-test", "id"], "realce": ["data-test"], "realce_em": 1.0, "realce_rotulo": "firstName", "legenda": "firstName, lastName e postalCode"}),
    ("E embaixo dos campos, o botão Continue, que quer dizer continuar. Botão direito nele, e Inspecionar: data-test igual continue.",
     dev36("site_sauce_continue_dev", COMPRA[:9], "continue", ["class", "data-test", "id", "name"], "O botão Continue: data-test=\"continue\"")),
    ("No código: preenche os três com dados de teste. Qualquer nome e CEP servem, porque é uma loja de treino. Depois, clica em continue.",
     edc(parcial(C36, L_CONT), "Os três campos e continue", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_FIRST, digitar_ate=L_CONT, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("O continue leva pra tela de revisão. Aqui a pessoa confere tudo antes de pagar: o produto, o pagamento, a entrega e o total.",
     {"type": "tela", "media": "site_sauce_revisao_zoom", "url": SAUCE, "acoes": COMPRA[:10], "zoom_pagina": 1.4, "titulo": "saucedemo.com", "legenda": "A revisão: confere antes de pagar"}),
    ("E lá embaixo, o botão Finish, que quer dizer terminar. Botão direito nele, e Inspecionar: data-test igual finish.",
     dev36("site_sauce_finish_dev", COMPRA[:10], "finish", ["class", "data-test", "id", "name"], "O botão Finish: data-test=\"finish\"")),
    ("No código, na tela de revisão, clica em finish.",
     edc(parcial(C36, L_FIN), "finish", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_FIN, digitar_ate=L_FIN, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("Clicou em finish, chega a tela final: Thank you for your order. Obrigado pelo seu pedido. Essa frase só aparece quando a compra terminou de verdade.",
     {"type": "tela", "media": "site_sauce_obrigado", "url": SAUCE, "acoes": COMPRA, "alvo": "Thank you for your order!", "titulo": "saucedemo.com", "zoom_em": 1.8, "caixa_em": 2.6, "legenda": "Thank you for your order = obrigado pelo seu pedido"}),
    ("Por isso ela é a nossa conferência. Inspecionar no título: data-test igual complete-header, o cabeçalho de concluído.",
     dev36("site_sauce_header_dev", COMPRA, "complete-header", ["class", "data-test"], "O título: data-test=\"complete-header\"")),
    ("No código, a conferência final: get by test id complete-header, to have text, Thank you for your order. Se a frase aparecer, a compra terminou e o teste passa.",
     edc(C36, "complete-header = o título do final", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_HEADER, digitar_ate=L_HEADER, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("Roda com o navegador aparecendo e olha o fluxo inteiro acontecendo sozinho.",
     rodando(C36, L_T36, L_HEADER + 1, "O fluxo inteiro, sozinho", COMPRA, "rec_compra", extra={"espera_fim": 2200, "delay_letra": 45})),
    ("Agora a compra inteira roda em segundos, sempre do mesmo jeito. Fazer isso na mão, em três navegadores, toda vez que alguém muda o site, é exatamente o trabalho que a automação tira de você.", {"type": "compare", "title": "A COMPRA INTEIRA", "items": [["NA MÃO", "MINUTOS, TODA VEZ", "white"], ["AUTOMÁTICO", "SEGUNDOS, SEMPRE IGUAL", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),  # pra que / quando
    ("No trabalho, esse é o teste que roda antes de toda entrega. Se ele passa, o caminho principal da loja funciona. Se falha, a entrega para até alguém olhar.",
     {"type": "cards", "titulo": "ANTES DE TODA ENTREGA", "itens": [["✓", "Passou", "o caminho principal funciona", "#3fd68a"], ["✗", "Falhou", "a entrega para", VERM]]}),
    ("Na próxima aula: uma coisa que você talvez já tenha percebido.", proxima("percebeu?")[0]),
    ("Te vejo lá!", proxima("percebeu?")[1]),
]))

# ---------- Aula 37 ----------
L_BE = ln(C36, "test.beforeEach")
AULAS.append(projeto(37, "MÓDULO 8 · AULA 37", "Percebeu que estamos copiando código?", [
    ("Olha o login no login ponto spec, e olha o login no compra ponto spec. É o mesmo código, duas vezes.",
     edc(trecho(C36, 1, L_BE + 6), "O mesmo login do login.spec.js", arquivo="compra.spec.js", pastas=ARV_C, destaque=list(range(L_BE + 2, L_BE + 5)), destaque_em=0.6, fonte=24)),
    ("Agora imagina dez arquivos de teste. Se o botão de login mudar, você arruma em dez lugares.",
     {"type": "cards", "itens": [["📄", "10 arquivos", "o mesmo login em todos"], ["✎", "O botão mudou?", "arruma em 10 lugares", VERM]]}),
    ("A solução é guardar o jeito de usar cada página num lugar só. Isso se chama Page Object: o objeto da página.",
     {"type": "traducao", "codigo": "Page Object", "texto_puro": True, "partes": [["Page", "página"], ["Object", "objeto"]], "passo": 1.6}),
    ("Pensa num controle remoto: você aperta ligar e não precisa saber como a TV funciona por dentro.",
     {"type": "cards", "itens": [["📺", "Controle remoto", "aperta ligar e pronto"], ["⚙", "Por dentro", "você não precisa saber", "#69a7ff"]]}),
    ("O teste vai dizer só login ponto entrar. Os detalhes de como entrar ficam guardados no Page Object.",
     {"type": "compare", "items": [["3 LINHAS DE LOGIN", "EM CADA TESTE", "red"], ["login.entrar(...)", "UMA LINHA SÓ", "gold"]], "size": 80, "stagger": 1.2, "vs": True}),
    ("Quando usar? Quando a mesma página aparece em vários testes, que é o normal num projeto de verdade. Por isso quase toda empresa usa, e é pergunta comum em entrevista.",
     {"type": "traducao", "titulo": "QUANDO USAR", "linhas": [["a página aparece em vários testes", "Page Object"], ["um arquivo só, um teste só", "não precisa"]]}),
    ("Na próxima aula, a gente cria o primeiro, com calma.", proxima("criando o LoginPage")[0]),
    ("Te vejo lá!", proxima("criando o LoginPage")[1]),
]))

# ---------- Aula 38 ----------
LP = ler("pages/LoginPage.js")
L_CONS = ln(LP, "constructor"); L_THISP = ln(LP, "this.page = page"); L_USR = ln(LP, "this.usuario"); L_ERRO = ln(LP, "this.erro")
LP38 = "\n".join(LP.split("\n")[:L_ERRO] + ["  }", "}"])  # só o constructor (o entrar vem na aula 39)
AULAS.append(projeto(38, "MÓDULO 8 · AULA 38", "Criando o LoginPage, passo a passo", [
    ("Primeiro, cria uma pasta nova chamada pages. Pages quer dizer páginas: é aqui que vão ficar os arquivos de cada página do site.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [1], "pastas": ARV_C, "alvo_item": "meu-primeiro-playwright",
      "novo_pos": 3, "resultado": "arquivo", "novo": "pages", "novo_nivel": 1, "novo_pasta": True, "legenda": "New Folder › pages"}),
    ("E dentro da pasta pages, um arquivo novo: LoginPage ponto js. A página do login.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [0], "pastas": [l for l in ARV_P if l != "    LoginPage.js"], "alvo_item": "pages",
      "novo_pos": ARV_P.index("    LoginPage.js"), "resultado": "arquivo", "novo": "LoginPage.js", "novo_nivel": 2, "legenda": "Dentro de pages: New File › LoginPage.js"}),
    ("Primeira linha: export class LoginPage, e abre chaves.",
     edc("export class LoginPage {\n}", "export class LoginPage", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=1, digitar_ate=1, fonte=32)),
    ("Traduzindo: class é um molde, uma receita pra criar objetos. LoginPage é o nome do molde. E export deixa outros arquivos usarem.",
     {"type": "traducao", "codigo": "export class LoginPage {", "partes": [["export", "deixe outros arquivos usarem"], ["class", "um molde"], ["LoginPage", "o nome do molde"]], "passo": 2.0}),
    ("Dentro, o constructor, que recebe o page. Constructor quer dizer construtor: é o que roda quando alguém cria um LoginPage.",
     edc(parcial(LP38, L_CONS, ("  }", "}")), "constructor = construtor", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_CONS, digitar_ate=L_CONS + 1, fonte=30)),
    ("Primeira linha dele: this ponto page igual page. This quer dizer este: guarde o page dentro deste LoginPage.",
     edc(parcial(LP38, L_THISP, ("  }", "}")), "this = este", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_THISP, digitar_ate=L_THISP, fonte=30)),
    ("Agora os elementos da página, um por linha: this ponto usuario igual page ponto get by test id username. Guarde o campo usuário com o nome usuario.",
     edc(parcial(LP38, L_USR, ("  }", "}")), "this.usuario = o campo usuário", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_USR, digitar_ate=L_USR, fonte=28)),
    ("Mesma coisa pra senha, o botão e a mensagem de erro.",
     edc(LP38, "Senha, botão e erro", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_USR + 1, digitar_ate=L_ERRO, fonte=28)),
    ("E aqui está o ganho: se um dia o data-test do botão mudar, você troca só nesta linha, e todos os testes que usam o LoginPage continuam funcionando.",
     edc(LP38, "O botão mudou? Troca só aqui", arquivo="LoginPage.js", pastas=ARV_P, destaque=[ln(LP, "this.botaoLogin")], destaque_em=0.8, fonte=28)),
    ("Por enquanto, ele só sabe onde estão as coisas. Na próxima aula, ele aprende a fazer o login, e o teste passa a usar.", proxima("usando o LoginPage")[0]),
    ("Te vejo lá!", proxima("usando o LoginPage")[1]),
]))

# ---------- Aula 39 ----------
L_ENTRAR = ln(LP, "async entrar"); L_FILLU = ln(LP, "this.usuario.fill")
C39 = cod(39)
L_IMP = ln(C39, "import { LoginPage }"); L_NEW = ln(C39, "new LoginPage"); L_ENT = ln(C39, "login.entrar")
# a aula 39 transforma o login.spec.js da aula 24 no da 39, mostrando cada linha que sai e cada uma que entra
JJ = "\n".join
C39L = C39.split("\n"); C24L = cod(24).split("\n")
LOG39 = ["fill(process.env.SAUCE_USER)", "'password').fill(process.env.SAUCE_PASSWORD)", "'login-button').click()"]
EXP39 = ["getByText('Products')", "Sauce Labs Backpack", "toHaveCount(6)"]
LOG39B = ["fill('locked_out_user')", "'password').fill(process.env.SAUCE_PASSWORD)", "'login-button').click()", "getByText('locked out')"]


def T39(L, k):
    """linha do k-ésimo test( no arquivo"""
    return [i + 1 for i, l in enumerate(L) if l.strip().startswith("test('")][k - 1]


def trecho39(L, k):
    a = T39(L, k); b = a
    while L[b - 1] != "  });":
        b += 1
    return JJ(L[a - 1:b])


def REL39(L, k, trechos):
    """posições (no trecho do k-ésimo teste) das linhas que têm cada pedaço"""
    t = trecho39(L, k).split("\n")
    return [[i + 1 for i, l in enumerate(t) if x in l][0] for x in trechos]


def troca39(L, k, sai, entra):
    a = T39(L, k); idx = [a - 1 + r - 1 for r in REL39(L, k, sai)]
    return L[:idx[0]] + entra + L[idx[-1] + 1:]


S39_0 = C24L[:1] + [C39L[1]] + C24L[1:]
S39_1 = troca39(S39_0, 1, LOG39, [l for l in C39L if "new LoginPage" in l][:1] + [l for l in C39L if "login.entrar(process.env.SAUCE_USER" in l])
S39_2 = troca39(S39_1, 1, EXP39, [l for l in C39L if "getByTestId('title')" in l])
S39_3 = troca39(S39_2, 2, LOG39B, C39L[T39(C39L, 2):T39(C39L, 2) + 3])
assert S39_3 == C39L, "a sequência da aula tem que terminar igual à etapa 39 validada"
AULAS.append(projeto(39, "MÓDULO 8 · AULA 39", "Usando o LoginPage no teste", [
    ("Hoje o LoginPage aprende uma ação: entrar.", titulo(39, "LOGIN.ENTRAR")),
    ("Embaixo do constructor: async entrar, abre parênteses, usuario, vírgula, senha. Uma ação que recebe o usuário e a senha.",
     edc(parcial(LP, L_ENTRAR, ("  }", "}")), "async entrar(usuario, senha)", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_ENTRAR, digitar_ate=L_ENTRAR + 1, fonte=26)),
    ("Traduzindo: async avisa que essa ação tem passos que levam tempo, como preencher e clicar. E é por isso que, lá dentro, cada passo vai ter o await, espere.",
     {"type": "traducao", "codigo": "async entrar(usuario, senha) {", "partes": [["async", "leva tempo"], ["entrar", "o nome"], ["(usuario, senha)", "o que recebe"]], "passo": 2.0}),
    ("Dentro: await this ponto usuario ponto fill usuario. Preencha o campo usuário deste LoginPage com o usuário que chegou.",
     edc(parcial(LP, L_FILLU, ("  }", "}")), "Preencha o usuário deste LoginPage", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_FILLU, digitar_ate=L_FILLU, fonte=26)),
    ("Depois a senha, e o clique no botão.", edc(LP, "A senha e o clique", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_FILLU + 1, digitar_ate=L_FILLU + 2, fonte=22)),
    ("Agora no teste, o login ponto spec. Primeira coisa: import LoginPage from ponto ponto barra pages barra LoginPage. Traga o molde lá da pasta pages.",
     edc(JJ(S39_0[:6]), "../ = volte uma pasta", arquivo="login.spec.js", pastas=ARV_P, digitar=True, digitar_de=2, digitar_ate=2, fonte=24)),
    ("Traduzindo o caminho: ponto ponto barra quer dizer volte uma pasta. O teste está dentro de tests, então ele sai de lá e entra em pages, no arquivo LoginPage.",
     {"type": "traducao", "codigo": "import { LoginPage } from '../pages/LoginPage';", "partes": [["import { LoginPage }", "traga o LoginPage"], ["../", "volte uma pasta (sai de tests)"], ["pages/LoginPage", "entre em pages, no LoginPage"]], "passo": 2.2}),
    ("No primeiro teste, as três linhas do login saem: o usuário, a senha e o clique. Apaga as três.",
     edc(trecho39(S39_0, 1), "Apaga as 3 linhas do login", arquivo="login.spec.js", pastas=ARV_P, linha0=T39(S39_0, 1), apagar=REL39(S39_0, 1, LOG39), apagar_em=2.4, fonte=22)),
    ("E no lugar, duas linhas. Primeiro: const login igual new LoginPage, passando o page. New quer dizer: crie um novo, usando esse molde.",
     edc(JJ([l for i, l in enumerate(trecho39(S39_1, 1).split("\n")) if i != 2]), "new = crie um novo", arquivo="login.spec.js", pastas=ARV_P, linha0=T39(S39_1, 1), digitar=True, digitar_de=2, digitar_ate=2, fonte=22)),
    ("E a segunda: await login ponto entrar, com o usuário e a senha. As três linhas viraram uma, porque o como fazer o login agora mora no LoginPage.",
     edc(trecho39(S39_1, 1), "Três linhas viraram uma", arquivo="login.spec.js", pastas=ARV_P, linha0=T39(S39_1, 1), digitar=True, digitar_de=3, digitar_ate=3, fonte=22)),
    ("E já que agora cada arquivo cuida de uma parte, as conferências de produtos saem do teste de login: apaga a do texto Products, a da mochila e a dos seis botões.",
     edc(trecho39(S39_1, 1), "Saem as conferências de produtos", arquivo="login.spec.js", pastas=ARV_P, linha0=T39(S39_1, 1), apagar=REL39(S39_1, 1, EXP39), apagar_em=3.0, fonte=22)),
    ("Fica a do endereço, e entra uma nova, mais firme: o título da página, pelo data-test title, tem o texto Products. É o mesmo data-test que vai pro ProdutosPage na próxima aula.",
     edc(trecho39(S39_2, 1), "data-test title = o título da página", arquivo="login.spec.js", pastas=ARV_P, linha0=T39(S39_2, 1), digitar=True, digitar_de=REL39(S39_2, 1, ["getByTestId('title')"])[0], digitar_ate=REL39(S39_2, 1, ["getByTestId('title')"])[0], fonte=22)),
    ("No segundo teste, a mesma troca. Apaga as três linhas do login e a conferência do texto locked out.",
     edc(trecho39(S39_2, 2), "Segundo teste: apaga o login e a conferência", arquivo="login.spec.js", pastas=ARV_P, linha0=T39(S39_2, 2), apagar=REL39(S39_2, 2, LOG39B), apagar_em=2.6, fonte=22)),
    ("E no lugar: cria o LoginPage, entra com o usuário bloqueado, e confere a mensagem usando o elemento erro, que já está guardado no LoginPage. Login ponto erro, to contain text, locked out.",
     edc(trecho39(C39L, 2), "login.erro: o erro guardado no LoginPage", arquivo="login.spec.js", pastas=ARV_P, linha0=T39(C39L, 2), digitar=True, digitar_de=2, digitar_ate=4, fonte=22)),
    ("Lendo em português: crie um LoginPage e entre com esse usuário e essa senha.", bt(("CRIE UM LOGINPAGE", "white", 110), ("E ENTRE COM ESSE USUÁRIO", "gold", 110), ("E ESSA SENHA", "white", 90), entre=1.3)),
    ("Roda: continua passando.",
     rodando(C39, L_NEW - 1, L_NEW + 4, "Continua passando", LOGIN, "rec_login_po", saida=("  2 passed (2.6s)", "ac"), cmd="npx playwright test login.spec.js --headed --project=chromium", arquivo="login.spec.js", pastas=ARV_P)),
    ("Na próxima aula: a mesma receita pras outras páginas.", proxima("ProdutosPage e CheckoutPage")[0]),
    ("Te vejo lá!", proxima("ProdutosPage e CheckoutPage")[1]),
]))

# ---------- Aula 40 ----------
PP = ler("pages/ProdutosPage.js"); CP = ler("pages/CheckoutPage.js"); C40 = cod(40)
L_PADD = ln(PP, "async adicionar"); L_PIR = ln(PP, "async irParaCarrinho"); L_CPRE = ln(CP, "async preencherDados")
L_T40 = ln(C40, "test('compra")
# a aula 40 monta o compra.spec.js em etapas, a partir do da aula 36 (cada troca aparece na tela)
C36L = C36.split("\n"); C40L = C40.split("\n")
assert C40L[0] == C36L[0] and C40L[4:8] == C36L[1:5]
S1 = C36L[:1] + C40L[1:4] + C36L[1:]                      # + os imports
L_LOG = [i + 1 for i, l in enumerate(S1) if "getByTestId('username')" in l][0]  # 1ª das 3 linhas do login
S2 = S1[:L_LOG - 1] + C40L[8:10] + S1[L_LOG + 2:]          # login vira LoginPage
assert S2[:12] == C40L[:12], "o beforeEach tem que ficar igual ao da etapa 40"
L_TS = [i + 1 for i, l in enumerate(S2) if "test('compra" in l][0]
S3 = S2[:L_TS] + C40L[13:16] + S2[L_TS:]                   # + os dois const
L_P1 = L_TS + 4; L_PN = len(S3) - 2                        # os passos antigos (do add-to-cart até o expect final)
assert "add-to-cart" in S3[L_P1 - 1] and "complete-header" in S3[L_PN - 1]
assert S3[:L_P1 - 1] + S3[L_PN:] == [l for l in C40L if l not in C40L[16:23]], "só os passos mudam"
J = "\n".join
NOVO = lambda nome: {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [0],
                     "alvo_item": "pages", "resultado": "arquivo", "novo": nome, "novo_nivel": 2, "legenda": "Dentro de pages: New File › " + nome}
ARV_PP = ARV_P[:5] + ["    ProdutosPage.js"] + ARV_P[5:]
PPL = PP.split("\n"); CPL = CP.split("\n")
AULAS.append(projeto(40, "MÓDULO 8 · AULA 40", "A mesma receita - ProdutosPage e CheckoutPage", [
    ("Você já sabe a receita do LoginPage. Hoje a gente aplica a mesma receita em mais duas páginas.", titulo(40, "A MESMA RECEITA")),
    ("Relembrando a receita, em quatro passos: a class, que é o molde. O constructor, que recebe o page. Os elementos da página. E as ações.",
     {"type": "cards", "titulo": "A RECEITA", "itens": [["1", "class", "o molde"], ["2", "constructor", "recebe o page", "#69a7ff"], ["3", "Elementos", "os data-test", "#ffd23f"], ["4", "Ações", "o que dá pra fazer", "#c792ea"]]}),
    ("Por que mais duas? O teste da compra passa por duas telas além do login: a dos produtos e a do checkout. E cada página do site ganha o seu próprio arquivo.",
     {"type": "cards", "itens": [["🔑", "LoginPage", "já está pronto"], ["🛒", "ProdutosPage", "produtos e carrinho", "#69a7ff"], ["💳", "CheckoutPage", "dados e finalização", "#ffd23f"]]}),
    ("Começando pela página dos produtos. Dentro da pasta pages, um arquivo novo: ProdutosPage ponto js.",
     dict(NOVO("ProdutosPage.js"), pastas=ARV_P, novo_pos=5)),
    ("Passos um e dois, igualzinho ao LoginPage: export class ProdutosPage, e o constructor recebendo o page, que fica guardado no this ponto page.",
     edc(J(PPL[:3] + ["  }", "}"]), "class + constructor", arquivo="ProdutosPage.js", pastas=ARV_PP, digitar=True, digitar_de=1, digitar_ate=3, fonte=28)),
    ("Passo três, os elementos. São os data-test que você já usou nas aulas trinta e cinco e trinta e seis: o título da página, title. O ícone do carrinho, shopping-cart-link. E o numerozinho, shopping-cart-badge.",
     edc(J(PPL[:6] + ["  }", "}"]), "Os elementos: os mesmos data-test da compra", arquivo="ProdutosPage.js", pastas=ARV_PP, digitar=True, digitar_de=4, digitar_ate=6, fonte=24)),
    ("Passo quatro, as ações. A primeira é adicionar: ela recebe o nome do produto, e clica no botão Add to cart dele.",
     edc(J(PPL[:11] + ["}"]), "async adicionar(produto)", arquivo="ProdutosPage.js", pastas=ARV_PP, digitar=True, digitar_de=8, digitar_ate=11, fonte=24)),
    ("Repara na crase, igual na aula trinta e dois. Se chegar sauce-labs-backpack, o data-test vira add-to-cart-sauce-labs-backpack, o botão da mochila. E serve pra qualquer outro produto.",
     {"type": "traducao", "codigo": "`add-to-cart-${produto}`", "partes": [["add-to-cart-", "o começo do data-test"], ["${produto}", "aqui entra o nome que chegou"]], "passo": 2.2}),
    ("A segunda ação: ir para o carrinho. Ela só clica no ícone do carrinho, que já está guardado lá em cima, no this ponto icone carrinho.",
     edc(PP, "async irParaCarrinho()", arquivo="ProdutosPage.js", pastas=ARV_PP, digitar=True, digitar_de=12, digitar_ate=15, fonte=24)),
    ("Agora a página do checkout. De novo, dentro de pages: New File, CheckoutPage ponto js.",
     dict(NOVO("CheckoutPage.js"), pastas=ARV_PP, novo_pos=4)),
    ("A mesma receita: export class CheckoutPage, e o constructor recebendo o page.",
     edc(J(CPL[:3] + ["  }", "}"]), "class + constructor", arquivo="CheckoutPage.js", pastas=ARV_P3, digitar=True, digitar_de=1, digitar_ate=3, fonte=28)),
    ("Os elementos são os data-test que você viu na aula trinta e seis: o botão checkout, os três campos, nome, sobrenome e CEP, o botão continue, o botão finish, e o título final, o complete-header.",
     edc(J(CPL[:10] + ["  }", "}"]), "Os elementos: as telas do checkout", arquivo="CheckoutPage.js", pastas=ARV_P3, digitar=True, digitar_de=4, digitar_ate=10, fonte=22)),
    ("E a ação preencher dados: ela recebe o nome, o sobrenome e o CEP, preenche os três campos, e clica em continuar.",
     edc(CP, "async preencherDados(nome, sobrenome, cep)", arquivo="CheckoutPage.js", pastas=ARV_P3, digitar=True, digitar_de=12, digitar_ate=18, fonte=22, rolar=True, rolar_de=0.5, rolar_dur=0.8)),
    ("Agora o teste da compra passa a usar as três páginas. Lá em cima, os imports: traga o LoginPage, o ProdutosPage e o CheckoutPage, da pasta pages.",
     edc(J(S1[:12]), "Os imports das três páginas", arquivo="compra.spec.js", pastas=ARV_P3, digitar=True, digitar_de=2, digitar_ate=4, fonte=24)),
    ("No before each, as três linhas do login saem. Apaga as três.",
     edc(J(S1[:13]), "Apaga as três linhas do login", arquivo="compra.spec.js", pastas=ARV_P3, apagar=[L_LOG, L_LOG + 1, L_LOG + 2], apagar_em=1.6, fonte=24)),
    ("E no lugar, as duas que você aprendeu na aula trinta e nove: crie um LoginPage, e entre com o usuário e a senha.",
     edc(J(S2[:12]), "O login agora é o LoginPage", arquivo="compra.spec.js", pastas=ARV_P3, digitar=True, digitar_de=L_LOG, digitar_ate=L_LOG + 1, fonte=24)),
    ("Dentro do teste, as duas primeiras linhas criam as páginas: const produtos igual new ProdutosPage, e const checkout igual new CheckoutPage. As duas recebem o page.",
     edc(J(S3[L_TS - 1:]), "Cria as duas páginas no teste", arquivo="compra.spec.js", pastas=ARV_P3, linha0=L_TS, digitar=True, digitar_de=2, digitar_ate=3, fonte=22)),
    ("Agora os passos antigos, aqueles com o get by test id um por um. Apaga todos eles.",
     edc(J(S3[L_TS - 1:]), "Apaga os passos antigos", arquivo="compra.spec.js", pastas=ARV_P3, linha0=L_TS, apagar=list(range(L_P1 - L_TS + 1, L_PN - L_TS + 2)), apagar_em=1.8, fonte=22)),
    ("E no lugar, os passos usando as páginas: produtos ponto adicionar a mochila, confere o numerozinho, produtos ponto ir para carrinho, o botão checkout, checkout ponto preencher dados, o botão finish, e a conferência da mensagem final.",
     edc(J(C40L[L_TS - 1:]), "Os passos agora usam as páginas", arquivo="compra.spec.js", pastas=ARV_P3, linha0=L_TS, digitar=True, digitar_de=5, digitar_ate=11, fonte=22)),
    ("Compara o antes e o depois. Antes, o teste dizia como clicar em cada coisa. Agora, ele diz o que está acontecendo: adiciona, vai pro carrinho, preenche os dados.",
     {"type": "traducao", "titulo": "ANTES  ×  DEPOIS", "linhas": [["getByTestId('add-to-cart-sauce-labs-backpack').click()", "produtos.adicionar('sauce-labs-backpack')"], ["getByTestId('shopping-cart-link').click()", "produtos.irParaCarrinho()"],
                                                       ["firstName, lastName, postalCode, continue", "checkout.preencherDados(...)"]]}),
    ("Roda: o fluxo inteiro continua passando.", rodando(C40, L_T40 + 3, ln(C40, "mensagemFinal") + 1, "O fluxo inteiro continua passando", COMPRA, "rec_compra_po", pastas=ARV_P3, extra={"espera_fim": 2200, "delay_letra": 45})),
    ("E agora, se a loja mudar o botão do carrinho, você conserta num lugar só, no ProdutosPage, e todos os testes de compra voltam a passar.",
     {"type": "cards", "itens": [["✎", "O botão mudou?", "conserta no ProdutosPage"], ["✓", "Todos os testes", "voltam a passar", "#3fd68a"]]}),
    ("Na próxima aula: um relatório que se lê como roteiro.", proxima("test.step")[0]),
    ("Te vejo lá!", proxima("test.step")[1]),
]))

# ---------- Aula 41 ----------
C41 = cod(41)
L_S1 = ln(C41, "test.step('adiciona"); L_S1F = L_S1 + 3
C41L = C41.split("\n"); L_T41 = ln(C41, "test('compra")
assert C41L[:L_T41 + 3] == C40L[:L_T41 + 3], "até os dois const, a 41 é igual à 40"
FAIXAS41 = [(ln(C41, "test.step('", k), ln(C41, "test.step('", k) + 3) for k in (1, 2, 3, 4)]  # cada passo: a linha do step até o fechamento
assert all(C41L[b - 1].strip() == "});" for a, b in FAIXAS41)


def ate_passo(k, so_abre=False):
    """o teste da 41 até o passo k (o resto ainda não existe), fechando o que ficou aberto"""
    fim = FAIXAS41[k - 1][0] if so_abre else FAIXAS41[k - 1][1]
    return J(C41L[L_T41 - 1:fim] + (["    });"] if so_abre else []) + ["  });", "});"])

PASSOS = [["Before Hooks", "1.1s"], ["adiciona a mochila no carrinho", "0.3s"], ["abre o carrinho", "0.2s"], ["preenche os dados de entrega", "0.4s"], ["finaliza a compra", "0.3s"]]
AULAS.append(projeto(41, "MÓDULO 8 · AULA 41", "test.step - um relatório que se lê como roteiro", [
    ("Quando um teste longo falha, você quer saber em qual parte.", titulo(41, "TEST.STEP")),
    ("A ideia: separar a compra em quatro passos com nome. Adiciona a mochila, abre o carrinho, preenche os dados, finaliza. Pra isso, os passos de dentro do teste vão ser escritos de novo, agora em blocos. Então apaga as linhas de dentro do teste.",
     edc(J(C40L[L_T40 - 1:]), "Apaga os passos de dentro do teste", arquivo="compra.spec.js", pastas=ARV_P3, linha0=L_T40, apagar=list(range(L_T40 + 4 - L_T40 + 1, len(C40L) - 2 - L_T40 + 2)), apagar_em=3.2, fonte=22)),
    ("O primeiro passo. A sintaxe: await test ponto step, abre parênteses, o nome do passo entre aspas, vírgula, async, parênteses, seta, e abre chaves.",
     edc(ate_passo(1, so_abre=True), "await test.step('nome', async () => {", arquivo="compra.spec.js", pastas=ARV_P3, linha0=L_T41, digitar=True, digitar_de=L_S1 - L_T41 + 1, digitar_ate=L_S1 - L_T41 + 1, fonte=22)),
    ("Traduzindo: test ponto step, um passo do teste. O nome, como ele aparece no relatório. E o bloco, o que esse passo faz.",
     {"type": "traducao", "codigo": "await test.step('adiciona a mochila no carrinho', async () => {", "partes": [["test.step", "um passo do teste"], ["'adiciona a mochila no carrinho'", "o nome no relatório"], ["async () => {", "o que o passo faz:"]], "passo": 2.0}),
    ("Dentro das chaves, as duas linhas desse passo: adiciona a mochila, e confere o numerozinho. E fecha o passo: chave, parêntese, ponto e vírgula.",
     edc(ate_passo(1), "As linhas do passo, dentro dele", arquivo="compra.spec.js", pastas=ARV_P3, linha0=L_T41, digitar=True, digitar_de=FAIXAS41[0][0] - L_T41 + 2, digitar_ate=FAIXAS41[0][1] - L_T41 + 1, fonte=22)),
    ("Roda e abre o relatório: o passo aparece com esse nome.",
     {"type": "pw_relatorio", "testes": [["Compra › compra uma mochila do começo ao fim", "compra.spec.js:13", "chromium", "ok", "2.6s"]],
      "abrir": {"titulo": "compra uma mochila do começo ao fim", "arquivo": "compra.spec.js:13", "projeto": "chromium", "passos": PASSOS[:2]}, "legenda": "O passo aparece com o nome que você deu"}),
    ("Segundo passo: abre o carrinho. E aproveita pra conferir uma coisa nova: que a mochila está lá dentro. Get by text Sauce Labs Backpack, to be visible.",
     edc(ate_passo(2), "abre o carrinho + confere a mochila", arquivo="compra.spec.js", pastas=ARV_P3, linha0=L_T41, digitar=True, digitar_de=FAIXAS41[1][0] - L_T41, digitar_ate=FAIXAS41[1][1] - L_T41 + 1, fonte=22, rolar_depois=True)),
    ("Terceiro passo: preenche os dados de entrega. Dentro, o botão checkout e o preencher dados.",
     edc(J(C41L[FAIXAS41[1][0] - 2:FAIXAS41[2][1]] + ["  });", "});"]), "preenche os dados de entrega", arquivo="compra.spec.js", pastas=ARV_P3, linha0=FAIXAS41[1][0] - 1, digitar=True, digitar_de=FAIXAS41[2][0] - FAIXAS41[1][0] + 1, digitar_ate=FAIXAS41[2][1] - FAIXAS41[1][0] + 2, fonte=22)),
    ("E o quarto: finaliza a compra. O botão finish, e a conferência da mensagem final.",
     edc(J(C41L[FAIXAS41[2][0] - 2:]), "finaliza a compra", arquivo="compra.spec.js", pastas=ARV_P3, linha0=FAIXAS41[2][0] - 1, digitar=True, digitar_de=FAIXAS41[3][0] - FAIXAS41[2][0] + 1, digitar_ate=FAIXAS41[3][1] - FAIXAS41[2][0] + 2, fonte=22)),
    ("E se falhar, o relatório mostra exatamente em qual passo.",
     {"type": "pw_relatorio", "testes": [["Compra › compra uma mochila do começo ao fim", "compra.spec.js:13", "chromium", "falhou", "6.2s"]],
      "abrir": {"titulo": "compra uma mochila do começo ao fim", "status": "falhou", "arquivo": "compra.spec.js:13", "projeto": "chromium",
                "passos": PASSOS[:3] + [["preenche os dados de entrega", "5.0s", "falhou"]]}, "legenda": "Falhou: o relatório mostra o passo"}),
    ("E o relatório fica legível até pra quem não programa: alguém da equipe abre e entende o que foi testado, passo por passo.", {"type": "cards", "itens": [["📄", "Relatório", "lê como um roteiro"], ["👥", "A equipe", "entende sem programar", "#69a7ff"]]}),  # pra que / quando
    ("Quando usar? Em testes compridos, com várias etapas, como essa compra. Num teste curto, de três linhas, não precisa.",
     {"type": "traducao", "titulo": "QUANDO USAR", "linhas": [["teste comprido, várias etapas", "test.step"], ["teste curto", "não precisa"]]}),
    ("Na próxima aula: fazendo o login uma vez só.", proxima("login uma vez só")[0]),
    ("Te vejo lá!", proxima("login uma vez só")[1]),
]))

# ---------- Aula 42 ----------
GI = open(os.path.join(RAIZ, "curso-playwright", "referencia_init", ".gitignore"), encoding="utf8").read().rstrip("\n") + "\n.env"
AUTH = ler("tests/auth.setup.js"); CFG = ler("playwright.config.js"); C42 = cod(42)
L_SS = ln(AUTH, "storageState"); L_SETUP = ln(CFG, "name: 'setup'"); L_DEP = ln(CFG, "dependencies")
CFG_P = trecho(CFG, L_SETUP - 2, L_DEP + 1)
L_USE = ln(C42, "test.use"); C42L = C42.split("\n"); L_GOTO42 = ln(C42, "inventory.html"); AUTHL = AUTH.split("\n"); CFG_PL = CFG_P.split("\n")
assert "LoginPage" in C41L[1] and C41L[5].startswith("test.describe") and C41L[-1] == "});"
_sobra = [l.strip() for i, l in enumerate(C41L) if i + 1 not in [2] + list(range(6, L_T41 - 1)) + [len(C41L)] and l.strip()]
assert [l.strip() for l in C42L if l.strip() and "test.use" not in l and "inventory.html" not in l] == _sobra, "a 42 = a 41 sem o login + test.use + goto (é o que a aula mostra)"
AULAS.append(projeto(42, "MÓDULO 8 · AULA 42", "Indo além - login uma vez só com storageState", [
    ("Todo teste faz login de novo. Se o login leva dois segundos e você tem trezentos testes, são dez minutos só entrando no site.", titulo(42, "LOGIN UMA VEZ SÓ")),
    ("A ideia: fazer o login uma vez, e salvar o navegador já logado num arquivo. Os testes que precisam começar logados usam esse arquivo.",
     {"type": "cards", "itens": [["🔑", "Login uma vez", "no começo de tudo"], ["💾", "Salva num arquivo", "o navegador já logado", "#69a7ff"], ["⚡", "Os testes usam", "começam logados", "#ffd23f"]]}),
    ("O que fica salvo? Os cookies: as informações que o site guarda pra lembrar que você entrou. É por isso que esse arquivo é sensível: com ele, qualquer um entraria na sua conta.",
     {"type": "cards", "itens": [["🍪", "Cookies", "o site lembra que você entrou"], ["⚠", "Arquivo sensível", "abre a sua conta", VERM]]}),
    ("Primeiro, a proteção: esse arquivo guarda dados da sua sessão e nunca deve ir pro GitHub. Abre o gitignore: o Playwright já colocou a pasta playwright barra ponto auth lá. Confere que ela está.",
     edc(GI, "/playwright/.auth/ já está no .gitignore", arquivo=".gitignore", pastas=ARV_P3, destaque=[ln(GI, ".auth")], destaque_em=1.2, fonte=30)),
    ("Primeira linha, o import, com uma diferença: test as setup. É o mesmo test, só que com o nome setup, pra deixar claro que isso é uma preparação, e não um teste. Embaixo, uma constante com o caminho do arquivo onde o login vai ficar guardado.",
     edc(J(AUTHL[:3]), "test as setup + o caminho do arquivo", arquivo="auth.setup.js", pastas=ARV_AUTH, digitar=True, digitar_de=1, digitar_ate=3, fonte=24,
         criar=[["Agora, o arquivo que faz o login uma vez só. Dentro da pasta tests, cria o auth ponto setup ponto js. Setup quer dizer preparação.", "auth.setup.js"]])),
    ("Depois, o setup em si: abre o site, preenche o usuário e a senha, clica, e confere que entrou. É o login que você já conhece.",
     edc(J(AUTHL[:L_SS - 1] + ["});"]), "O login que você já conhece", arquivo="auth.setup.js", pastas=ARV_AUTH, digitar=True, digitar_de=5, digitar_ate=L_SS - 1, fonte=22)),
    ("E a linha nova, no fim: page ponto context, ponto storage state, com o path. Guarde o estado do navegador, os cookies, nesse arquivo.",
     edc(AUTH, "storageState = guarde o estado", arquivo="auth.setup.js", pastas=ARV_AUTH, digitar=True, digitar_de=L_SS, digitar_ate=L_SS, fonte=22)),
    ("No config, dentro dos projects, um project novo chamado setup. Ele roda os arquivos que terminam em setup ponto js.",
     edc(J([l for l in CFG_PL if "dependencies" not in l]), "project setup", arquivo="playwright.config.js", pastas=ARV_AUTH, linha0=L_SETUP - 2, digitar=True, digitar_de=3, digitar_ate=3, fonte=26)),
    ("E no project do chromium, dependencies setup: ele só começa depois que o setup terminar. Faz o mesmo no firefox, no webkit e no celular.",
     edc(CFG_P, "dependencies = depende do setup", arquivo="playwright.config.js", pastas=ARV_AUTH, linha0=L_SETUP - 2, digitar=True, digitar_de=len(CFG_PL) - 1, digitar_ate=len(CFG_PL) - 1, fonte=26)),
    ("Agora, quem usa o login salvo? Existem dois jeitos. A gente vai usar este: ligar só nos arquivos que precisam começar logados. O teste de login, por exemplo, precisa começar deslogado.",
     {"type": "cards", "itens": [["✓", "compra.spec.js", "começa logado"], ["✗", "login.spec.js", "precisa começar deslogado", VERM]]}),
    ("Agora o compra ponto spec. O login não precisa mais acontecer aqui. Então apaga o import do LoginPage, o describe, e o before each inteiro.",
     edc(J(C41L[:L_T41 - 1]), "Sai o login: import, describe e beforeEach", arquivo="compra.spec.js", pastas=ARV_AUTH, apagar=[2] + list(range(6, L_T41 - 1)), apagar_em=2.6, fonte=24)),
    ("Lá no fim do arquivo, apaga também o fechamento do describe. E seleciona tudo e aperta Shift Tab, pra o teste voltar pro canto esquerdo.",
     edc(J(C41L[-6:]), "Sai o fechamento do describe", arquivo="compra.spec.js", pastas=ARV_AUTH, linha0=len(C41L) - 5, apagar=[6], apagar_em=2.0, fonte=24)),
    ("E no lugar do login, depois dos imports: test ponto use, storage state, e o caminho do arquivo. Use esse login salvo.",
     edc(J(C42L[:L_USE + 2]), "test.use({ storageState }) = use o login salvo", arquivo="compra.spec.js", pastas=ARV_AUTH, digitar=True, digitar_de=L_USE, digitar_ate=L_USE, fonte=24)),
    ("Só falta um detalhe: o teste não passa mais pela tela de login, então ninguém abre o site. O primeiro passo começa abrindo direto a página de produtos: page ponto goto, barra inventory ponto html.",
     edc(J(C42L[L_USE + 1:L_GOTO42 + 2]), "Abre direto a página de produtos", arquivo="compra.spec.js", pastas=ARV_AUTH, linha0=L_USE + 2, digitar=True, digitar_de=L_GOTO42 - L_USE - 1, digitar_ate=L_GOTO42 - L_USE - 1, fonte=22)),
    ("Roda: o setup aparece primeiro, e a compra começa direto na página de produtos.",
     edc(trecho(C42, L_USE, L_USE + 9), "Começa direto nos produtos", arquivo="compra.spec.js", pastas=ARV_AUTH, linha0=L_USE,
         terminal=[{"cmd": "npx playwright test compra.spec.js --headed --project=chromium", "em": 0.03}, {"out": "Running 2 tests using 1 worker", "cor": "mut", "em": 0.06},
                   {"out": "  ✓ [setup] › faz login uma vez", "cor": "ac", "em": 0.09}, {"out": "  2 passed (4.1s)", "cor": "ac", "em": 0.86}],
         navegador={"media": "rec_logado", "url": "https://www.saucedemo.com/inventory.html", "pre_url": SAUCE, "pre_acoes": LOGIN, "gravar": True, "acoes": COMPRA[3:],
                    "espera_inicio": 900, "espera_fim": 2000, "delay_letra": 45, "titulo": "Chromium", "em": 0.12, "ate": 0.84})),
    ("Quando não usar: no teste do próprio login, claro, que precisa começar deslogado. E se um teste precisa de outro usuário, ele precisa de outro arquivo de login.", {"type": "traducao", "titulo": "QUANDO USAR", "linhas": [["testes que começam logados", "o login salvo"], ["o teste do login", "começa deslogado"], ["outro usuário", "outro arquivo de login"]]}),  # pra que / quando
    ("Projeto final pronto! Agora ele vai pro GitHub.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Git, GitHub e CI"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 9 · GIT E GITHUB"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 8 (gerado do roteiro_playwright_m8.py)", ""]
    for slug, p in AULAS:
        for x in p["script"]["long"]["parts"][0]["sentences"]:  # frase curta com o navegador rodando: 2 s de silêncio pra dar tempo de ver o teste e o "passed"
            if x["scene"].get("navegador") and len(x["text"]) < 50:
                x["pausa"] = 2
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo8.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

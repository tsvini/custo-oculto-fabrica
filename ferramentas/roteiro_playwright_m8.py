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
               terminal=[{"cmd": cmd, "em": 0.03}, {"out": "Running 1 test using 1 worker", "cor": "mut", "em": 0.08}, {"out": saida[0], "cor": saida[1], "em": 0.86}], navegador=nav, **kw)


AULAS = []

# ---------- Aula 35 ----------
C35 = cod(35)
L_TESTE35 = ln(C35, "test('compra")
L_ADD = ln(C35, "add-to-cart")
L_BADGE = ln(C35, "shopping-cart-badge")
AULAS.append(projeto(35, "MÓDULO 8 · AULA 35", "O carrinho", [
    ("Começa o projeto final: o fluxo de compra completo, do login até o obrigado. Hoje, o carrinho.", titulo(35, "O CARRINHO")),
    ("Depois do login, cada produto tem um botão Add to cart. Clica com o botão direito e Inspecionar: data-test igual add-to-cart-sauce-labs-backpack.",
     {"type": "devtools", "media": "site_sauce_produtos_dev", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"add-to-cart-sauce-labs-backpack\"]",
      "attrs": ["class", "data-test", "id", "name"], "realce": ["data-test"], "realce_em": 4.0, "realce_rotulo": "este", "legenda": "data-test do botão Add to cart"}),
    ("Cria o compra ponto spec ponto js, com o login no before each, do jeito que você já sabe.",
     edc(parcial(C35, L_TESTE35 - 2, ("});",)), "O login no beforeEach, como você já sabe", arquivo="compra.spec.js", pastas=ARV_C, fonte=24)),
    ("No teste: get by test id add-to-cart-sauce-labs-backpack, ponto click.",
     edc(parcial(C35, L_ADD), "getByTestId(...).click()", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_TESTE35, digitar_ate=L_ADD, fonte=22)),
    ("E a conferência: o numerozinho do carrinho mostra um. get by test id shopping-cart-badge, to have text um.",
     edc(C35, "shopping-cart-badge = o numerozinho do carrinho", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_BADGE, digitar_ate=L_BADGE, fonte=22)),
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
    ("Abre o carrinho: get by test id shopping-cart-link, click. Depois o botão checkout.",
     edc(parcial(C36, L_CHECK), "shopping-cart-link e checkout", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_CART, digitar_ate=L_CHECK, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("Na tela de dados, três campos: nome, sobrenome e CEP. Os data-test são firstName, lastName e postalCode.",
     {"type": "devtools", "media": "site_sauce_dados_dev", "url": SAUCE, "acoes": COMPRA[:6], "inspecionar": "[data-test=\"firstName\"]", "aberto": True,
      "attrs": ["class", "placeholder", "data-test", "id"], "realce": ["data-test"], "realce_em": 1.0, "realce_rotulo": "firstName", "legenda": "firstName, lastName e postalCode"}),
    ("Preenche os três e clica em continue.",
     edc(parcial(C36, L_CONT), "Os três campos e continue", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_FIRST, digitar_ate=L_CONT, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("Na tela de revisão, clica em finish.",
     edc(parcial(C36, L_FIN), "finish", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_FIN, digitar_ate=L_FIN, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("E a conferência final: complete-header, to have text, Thank you for your order.",
     edc(C36, "complete-header = o título do final", arquivo="compra.spec.js", pastas=ARV_C, digitar=True, digitar_de=L_HEADER, digitar_ate=L_HEADER, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("Roda com o navegador aparecendo e olha o fluxo inteiro acontecendo sozinho.",
     rodando(C36, L_T36, L_HEADER + 1, "O fluxo inteiro, sozinho", COMPRA, "rec_compra", extra={"espera_fim": 2200, "delay_letra": 45})),
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
    ("Na próxima aula, a gente cria o primeiro, com calma.", proxima("criando o LoginPage")[0]),
    ("Te vejo lá!", proxima("criando o LoginPage")[1]),
]))

# ---------- Aula 38 ----------
LP = ler("pages/LoginPage.js")
L_CONS = ln(LP, "constructor"); L_THISP = ln(LP, "this.page = page"); L_USR = ln(LP, "this.usuario"); L_ERRO = ln(LP, "this.erro")
LP38 = "\n".join(LP.split("\n")[:L_ERRO] + ["  }", "}"])  # só o constructor (o entrar vem na aula 39)
AULAS.append(projeto(38, "MÓDULO 8 · AULA 38", "Criando o LoginPage, passo a passo", [
    ("Cria uma pasta nova chamada pages, e dentro o arquivo LoginPage ponto js.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [1], "pastas": ARV_C, "alvo_item": "meu-primeiro-playwright",
      "novo_pos": 3, "resultado": "arquivo", "novo": "pages", "novo_nivel": 1, "novo_pasta": True, "legenda": "New Folder › pages  ·  depois LoginPage.js"}),
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
    ("Por enquanto, ele só sabe onde estão as coisas. Na próxima aula, ele aprende a fazer o login, e o teste passa a usar.", proxima("usando o LoginPage")[0]),
    ("Te vejo lá!", proxima("usando o LoginPage")[1]),
]))

# ---------- Aula 39 ----------
L_ENTRAR = ln(LP, "async entrar"); L_FILLU = ln(LP, "this.usuario.fill")
C39 = cod(39)
L_IMP = ln(C39, "import { LoginPage }"); L_NEW = ln(C39, "new LoginPage"); L_ENT = ln(C39, "login.entrar")
AULAS.append(projeto(39, "MÓDULO 8 · AULA 39", "Usando o LoginPage no teste", [
    ("Hoje o LoginPage aprende uma ação: entrar.", titulo(39, "LOGIN.ENTRAR")),
    ("Embaixo do constructor: async entrar, abre parênteses, usuario, vírgula, senha. Uma ação que recebe o usuário e a senha.",
     edc(parcial(LP, L_ENTRAR, ("  }", "}")), "async entrar(usuario, senha)", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_ENTRAR, digitar_ate=L_ENTRAR + 1, fonte=26)),
    ("Dentro: await this ponto usuario ponto fill usuario. Preencha o campo usuário deste LoginPage com o usuário que chegou.",
     edc(parcial(LP, L_FILLU, ("  }", "}")), "Preencha o usuário deste LoginPage", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_FILLU, digitar_ate=L_FILLU, fonte=26)),
    ("Depois a senha, e o clique no botão.", edc(LP, "A senha e o clique", arquivo="LoginPage.js", pastas=ARV_P, digitar=True, digitar_de=L_FILLU + 1, digitar_ate=L_FILLU + 2, fonte=22)),
    ("Agora no teste. Primeira coisa: import LoginPage from ponto ponto barra pages barra LoginPage. Traga o molde lá da pasta pages.",
     edc(C39, "../ = volte uma pasta", pastas=ARV_P, digitar=True, digitar_de=L_IMP, digitar_ate=L_IMP, fonte=22, rolar_depois=True)),
    ("Dentro do teste: const login igual new LoginPage, passando o page. New quer dizer: crie um novo, usando esse molde.",
     edc(C39, "new = crie um novo", pastas=ARV_P, digitar=True, digitar_de=L_NEW, digitar_ate=L_NEW, fonte=22, rolar_depois=True)),
    ("E as três linhas do login viram uma: await login ponto entrar, com usuário e senha.",
     edc(C39, "Três linhas viraram uma", pastas=ARV_P, digitar=True, digitar_de=L_ENT, digitar_ate=L_ENT, fonte=22, rolar_depois=True)),
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
AULAS.append(projeto(40, "MÓDULO 8 · AULA 40", "A mesma receita - ProdutosPage e CheckoutPage", [
    ("Você já sabe a receita: class, constructor, elementos e ações. Agora é só aplicar.", titulo(40, "A MESMA RECEITA")),
    ("ProdutosPage: os elementos são o título, o ícone do carrinho e o numerozinho.",
     edc(PP, "Os elementos da página de produtos", arquivo="ProdutosPage.js", pastas=ARV_P3, destaque=[ln(PP, "this.titulo"), ln(PP, "this.iconeCarrinho"), ln(PP, "this.contadorCarrinho")], destaque_em=0.6, fonte=20)),
    ("E duas ações: adicionar um produto, e ir pro carrinho. Repara no adicionar: ele recebe o nome do produto e monta o data-test com crase, igual você aprendeu na aula 32.",
     edc(PP, "adicionar(produto): o data-test com crase", arquivo="ProdutosPage.js", pastas=ARV_P3, destaque=[L_PADD, L_PADD + 1, L_PIR, L_PIR + 1], destaque_em=0.6, fonte=20)),
    ("CheckoutPage: os campos de nome, sobrenome e CEP, os botões, e a mensagem final.",
     edc(CP, "Os elementos do checkout", arquivo="CheckoutPage.js", pastas=ARV_P3, destaque=list(range(ln(CP, "this.botaoCheckout"), ln(CP, "this.mensagemFinal") + 1)), destaque_em=0.6, fonte=20, rolar=True, rolar_de=4.5, rolar_dur=1.2)),
    ("E a ação preencher dados, que preenche os três campos e clica em continuar.",
     edc(CP, "preencherDados(nome, sobrenome, cep)", arquivo="CheckoutPage.js", pastas=ARV_P3, destaque=list(range(L_CPRE, L_CPRE + 5)), destaque_em=0.6, fonte=20, rolar=True, rolar_de=0.6, rolar_dur=1.0)),
    ("No teste da compra, cada passo agora lê como uma frase: produtos ponto adicionar, produtos ponto ir para carrinho, checkout ponto preencher dados.",
     edc(C40, "Cada passo lê como uma frase", arquivo="compra.spec.js", pastas=ARV_P3, destaque=[ln(C40, "produtos.adicionar"), ln(C40, "produtos.irParaCarrinho"), ln(C40, "checkout.preencherDados")],
         destaque_em=2.6, rolar=True, rolar_de=0.6, rolar_dur=1.4, fonte=22)),
    ("Roda: o fluxo inteiro continua passando.", rodando(C40, L_T40 + 3, ln(C40, "mensagemFinal") + 1, "O fluxo inteiro continua passando", COMPRA, "rec_compra_po", pastas=ARV_P3, extra={"espera_fim": 2200, "delay_letra": 45})),
    ("Na próxima aula: um relatório que se lê como roteiro.", proxima("test.step")[0]),
    ("Te vejo lá!", proxima("test.step")[1]),
]))

# ---------- Aula 41 ----------
C41 = cod(41)
L_S1 = ln(C41, "test.step('adiciona"); L_S1F = L_S1 + 3
PASSOS = [["Before Hooks", "1.1s"], ["adiciona a mochila no carrinho", "0.3s"], ["abre o carrinho", "0.2s"], ["preenche os dados de entrega", "0.4s"], ["finaliza a compra", "0.3s"]]
AULAS.append(projeto(41, "MÓDULO 8 · AULA 41", "test.step - um relatório que se lê como roteiro", [
    ("Quando um teste longo falha, você quer saber em qual parte.", titulo(41, "TEST.STEP")),
    ("A sintaxe: await test ponto step, abre parênteses, o nome do passo entre aspas, vírgula, async, parênteses, seta, e abre chaves.",
     edc(parcial(C41, L_S1, ("    });", "  });", "});")), "await test.step('nome', async () => {", arquivo="compra.spec.js", pastas=ARV_P3, digitar=True, digitar_de=L_S1, digitar_ate=L_S1, fonte=22, rolar=True, rolar_de=0.6, rolar_dur=0.8)),
    ("Traduzindo: test ponto step, um passo do teste. O nome, como ele aparece no relatório. E o bloco, o que esse passo faz.",
     {"type": "traducao", "codigo": "await test.step('adiciona a mochila no carrinho', async () => {", "partes": [["test.step", "um passo do teste"], ["'adiciona a mochila no carrinho'", "o nome no relatório"], ["async () => {", "o que o passo faz:"]], "passo": 2.0}),
    ("Coloca o primeiro passo: adiciona a mochila no carrinho. Roda e abre o relatório: o passo aparece com esse nome.",
     {"type": "pw_relatorio", "testes": [["Compra › compra uma mochila do começo ao fim", "compra.spec.js:13", "chromium", "ok", "2.6s"]],
      "abrir": {"titulo": "compra uma mochila do começo ao fim", "arquivo": "compra.spec.js:13", "projeto": "chromium", "passos": PASSOS[:2]}, "legenda": "O passo aparece com o nome que você deu"}),
    ("Agora os outros três, do mesmo jeito: abre o carrinho, preenche os dados de entrega, finaliza a compra.",
     edc(C41, "Os quatro passos", arquivo="compra.spec.js", pastas=ARV_P3, destaque=[ln(C41, "test.step('", k) for k in (1, 2, 3, 4)], destaque_em=0.6, rolar=True, rolar_de=1.8, rolar_dur=2.0, fonte=22)),
    ("E se falhar, o relatório mostra exatamente em qual passo.",
     {"type": "pw_relatorio", "testes": [["Compra › compra uma mochila do começo ao fim", "compra.spec.js:13", "chromium", "falhou", "6.2s"]],
      "abrir": {"titulo": "compra uma mochila do começo ao fim", "status": "falhou", "arquivo": "compra.spec.js:13", "projeto": "chromium",
                "passos": PASSOS[:3] + [["preenche os dados de entrega", "5.0s", "falhou"]]}, "legenda": "Falhou: o relatório mostra o passo"}),
    ("Na próxima aula: fazendo o login uma vez só.", proxima("login uma vez só")[0]),
    ("Te vejo lá!", proxima("login uma vez só")[1]),
]))

# ---------- Aula 42 ----------
GI = open(os.path.join(RAIZ, "curso-playwright", "referencia_init", ".gitignore"), encoding="utf8").read().rstrip("\n") + "\n.env"
AUTH = ler("tests/auth.setup.js"); CFG = ler("playwright.config.js"); C42 = cod(42)
L_SS = ln(AUTH, "storageState"); L_SETUP = ln(CFG, "name: 'setup'"); L_DEP = ln(CFG, "dependencies")
CFG_P = trecho(CFG, L_SETUP - 2, L_DEP + 1)
L_USE = ln(C42, "test.use")
AULAS.append(projeto(42, "MÓDULO 8 · AULA 42", "Indo além - login uma vez só com storageState", [
    ("Todo teste faz login de novo. Em centenas de testes, é muito tempo perdido.", titulo(42, "LOGIN UMA VEZ SÓ")),
    ("A ideia: fazer o login uma vez, e salvar o navegador já logado num arquivo. Os testes que precisam começar logados usam esse arquivo.",
     {"type": "cards", "itens": [["🔑", "Login uma vez", "no começo de tudo"], ["💾", "Salva num arquivo", "o navegador já logado", "#69a7ff"], ["⚡", "Os testes usam", "começam logados", "#ffd23f"]]}),
    ("Primeiro, a proteção: esse arquivo guarda dados da sua sessão e nunca deve ir pro GitHub. Abre o gitignore: o Playwright já colocou a pasta playwright barra ponto auth lá. Confere que ela está.",
     edc(GI, "/playwright/.auth/ já está no .gitignore", arquivo=".gitignore", pastas=ARV_P3, destaque=[ln(GI, ".auth")], destaque_em=1.2, fonte=30)),
    ("Cria o auth ponto setup ponto js. Ele faz o login e, no fim, storage state, salvando tudo em playwright barra ponto auth barra usuario ponto json.",
     edc(AUTH, "storageState = o estado guardado", arquivo="auth.setup.js", pastas=ARV_AUTH, destaque=[L_SS], destaque_em=2.0, fonte=22)),
    ("No config, um project chamado setup, que roda esse arquivo. E nos outros projects, dependencies setup: eles só começam depois do setup.",
     edc(CFG_P, "dependencies = depende do setup", arquivo="playwright.config.js", pastas=ARV_AUTH, linha0=L_SETUP - 2, destaque=[3, len(CFG_P.split("\n")) - 1], destaque_em=0.8, fonte=26)),
    ("Agora, quem usa o login salvo? Existem dois jeitos. A gente vai usar este: ligar só nos arquivos que precisam começar logados. O teste de login, por exemplo, precisa começar deslogado.",
     {"type": "cards", "itens": [["✓", "compra.spec.js", "começa logado"], ["✗", "login.spec.js", "precisa começar deslogado", VERM]]}),
    ("No arquivo da compra: test ponto use, storage state, e o caminho do arquivo. Use esse login salvo.",
     edc(C42, "test.use({ storageState }) = use o login salvo", arquivo="compra.spec.js", pastas=ARV_AUTH, destaque=[L_USE], destaque_em=0.8, fonte=22, rolar_depois=True, rolar_de=3.0)),
    ("Roda: o setup aparece primeiro, e a compra começa direto na página de produtos.",
     edc(trecho(C42, L_USE, L_USE + 9), "Começa direto nos produtos", arquivo="compra.spec.js", pastas=ARV_AUTH, linha0=L_USE,
         terminal=[{"cmd": "npx playwright test compra.spec.js --headed --project=chromium", "em": 0.03}, {"out": "Running 2 tests using 1 worker", "cor": "mut", "em": 0.06},
                   {"out": "  ✓ [setup] › faz login uma vez", "cor": "ac", "em": 0.09}, {"out": "  2 passed (4.1s)", "cor": "ac", "em": 0.86}],
         navegador={"media": "rec_logado", "url": "https://www.saucedemo.com/inventory.html", "pre_url": SAUCE, "pre_acoes": LOGIN, "gravar": True, "acoes": COMPRA[3:],
                    "espera_inicio": 900, "espera_fim": 2000, "delay_letra": 45, "titulo": "Chromium", "em": 0.12, "ate": 0.84})),
    ("Projeto final pronto! Agora ele vai pro GitHub.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Git, GitHub e CI"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 9 · GIT E GITHUB"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 8 (gerado do roteiro_playwright_m8.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo8.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

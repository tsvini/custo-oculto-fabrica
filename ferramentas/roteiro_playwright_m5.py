"""Gera projetos/curso-playwright-22..25 (módulo 5: organização). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Código = curso-playwright/projeto/tests/etapas/aulaNN.spec.js (validado no Actions); only/skip validados em demos/."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m3 import codigo, ARV, SAUCE, LOGIN
from roteiro_playwright_m4 import edc, CMD

REF = os.path.join(RAIZ, "curso-playwright", "referencia_init")
CONFIG = open(os.path.join(REF, "playwright.config.js"), encoding="utf8").read().rstrip("\n").split("\n")
GITIGNORE = open(os.path.join(REF, ".gitignore"), encoding="utf8").read().rstrip("\n")
C16, C21, C22, C23, C24 = (codigo(n) for n in (16, 21, 22, 23, 24))
ARV_ENV = ARV[:5] + ["  .env"] + ARV[5:]
ARV_EX = ARV[:5] + ["  .env", "  .env.example"] + ARV[5:]


def topo(cod, n=10):
    """o começo do arquivo, como aparece no editor com o terminal aberto embaixo"""
    return "\n".join(cod.split("\n")[:n])


def vs(cod, legenda, terminal, arquivo="login.spec.js", n=10, **kw):
    return edc(topo(cod, n), legenda, arquivo=arquivo, terminal=terminal, **kw)


def run(*saida, cmd=CMD, em=0.05):
    L = [{"cmd": cmd, "em": em}]
    for i, (txt, cor) in enumerate(saida):
        L.append({"out": txt, "cor": cor, "em": [0.3, 0.55, 0.62, 0.68][min(i, 3)]})
    return L


def cfg(linhas):
    """trecho do playwright.config.js (com as linhas de verdade do arquivo e a numeração certa)"""
    return "\n".join(linhas)


# ---------- passos intermediários da aula 22 (o arquivo antes do describe) ----------
TESTE_BLOQ = """test('mostra erro para usuário bloqueado', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
  await page.getByPlaceholder('Username').fill('locked_out_user');
  await page.getByPlaceholder('Password').fill('secret_sauce');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.getByText('locked out')).toBeVisible();
});"""
DOIS = C16 + "\n\n" + TESTE_BLOQ  # linhas 1-11 = teste da aula 16; 13-18 = teste novo
LD = DOIS.split("\n")
L_T2 = [i + 1 for i, l in enumerate(LD) if "mostra erro" in l][0]       # o test do bloqueado
L_GOTOS = [i + 1 for i, l in enumerate(LD) if "page.goto" in l]           # os dois goto
assert len(L_GOTOS) == 2 and L_GOTOS[1] == L_T2 + 1
GOTO = "  await page.goto('https://www.saucedemo.com/');\n"
BE = """test.beforeEach(async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
});

"""
COM_BE = DOIS.replace(GOTO, "", 2).replace("import { test, expect } from '@playwright/test';\n\n", "import { test, expect } from '@playwright/test';\n\n" + BE)
assert COM_BE.count("page.goto") == 1 and "  await page.goto" in COM_BE.split("\n")[3]

AULAS = []

# ---------- Aula 22 ----------
REL22 = [["Login › entra com usuário e senha", "login.spec.js:8", "chromium", "ok", "1.1s"], ["Login › mostra erro para usuário bloqueado", "login.spec.js:18", "chromium", "ok", "0.7s"]]
L21 = C21.split("\n"); L_LENTO = [i + 1 for i, l in enumerate(L21) if "usuário lento" in l][0]
APAGA_LENTO = list(range(L_LENTO - 1, len(L21) + 1))  # a linha em branco antes e o teste inteiro
# o segundo teste sendo escrito, aos poucos
CAB2 = C16 + "\n\ntest('mostra erro para usuário bloqueado', async ({ page }) => {\n});"
MEIO2 = "\n".join(LD[:L_T2 + 4] + ["});"])
# o describe em volta dos dois testes (ainda sem o beforeEach)
IND = lambda txt: "\n".join(("  " + l) if l else l for l in txt.split("\n"))
C_DESC = "import { test, expect } from '@playwright/test';\n\ntest.describe('Login', () => {\n" + IND("\n".join(LD[2:])) + "\n});"
LDS = C_DESC.split("\n"); L_GOTOS_D = [i + 1 for i, l in enumerate(LDS) if "page.goto" in l]
# o beforeEach dentro do describe, com os goto ainda nos testes; depois os goto saem
C22F = C22.replace("aula 22: ", "")
C_TMP = C_DESC.replace("test.describe('Login', () => {\n", "test.describe('Login', () => {\n  test.beforeEach(async ({ page }) => {\n    await page.goto('https://www.saucedemo.com/');\n  });\n\n")
LT = C_TMP.split("\n"); L_GOTOS_T = [i + 1 for i, l in enumerate(LT) if "page.goto" in l][1:]
assert "\n".join(l for i, l in enumerate(LT) if i + 1 not in L_GOTOS_T) == C22F, "o fim da aula tem que ser igual à etapa validada"
AULAS.append(projeto(22, "MÓDULO 5 · AULA 22", "describe e beforeEach", [
    ("O seu arquivo vai crescer. Hoje você aprende a deixar ele organizado.", titulo(22, "ORGANIZANDO")),
    ("Antes, apaga aquele teste do usuário lento. Ele era só pra você ver a espera automática, e já cumpriu o papel dele.",
     edc(C21, "Apaga o teste do usuário lento", rolar=True, rolar_de=0.6, rolar_dur=1.0, apagar=APAGA_LENTO, apagar_em=2.6, fonte=24)),
    ("Agora um teste novo. Um bom teste de login não confere só quem entra: confere também quem não pode entrar. O saucedemo tem um usuário bloqueado: locked underline out underline user.",
     {"type": "tela", "media": "rec_sauce_locked", "url": SAUCE, "gravar": True, "titulo": "saucedemo.com", "legenda": "O usuário bloqueado não entra",
      "acoes": [{"fill": ["#user-name", "locked_out_user"]}, {"fill": ["#password", "secret_sauce"]}, {"click": "#login-button"}], "espera_fim": 2200, "delay_letra": 70}),
    ("Embaixo do primeiro teste, um test novo. E o nome diz o que ele confere: mostra erro para usuário bloqueado.",
     edc(CAB2, "test('mostra erro para usuário bloqueado')", digitar=True, digitar_de=L_T2, rolar=True, rolar_de=0.5, rolar_dur=0.8, fonte=24)),
    ("As quatro primeiras linhas você já conhece: abre o site, preenche o usuário, a senha, e clica em Login. A única diferença é o usuário: agora é o locked out user.",
     edc(MEIO2, "Igual ao primeiro, só muda o usuário", digitar=True, digitar_de=L_T2 + 1, digitar_ate=L_T2 + 4, vel=0.85, rolar=True, rolar_de=0.4, rolar_dur=0.8, fonte=24)),
    ("E o que esse teste confere? Olha o que aparece na tela quando o usuário bloqueado tenta entrar: uma mensagem vermelha. Sorry, this user has been locked out. Quer dizer: desculpe, esse usuário foi bloqueado.",
     {"type": "tela", "media": "site_sauce_locked_msg", "url": SAUCE, "titulo": "saucedemo.com", "acoes": [{"fill": ["#user-name", "locked_out_user"]}, {"fill": ["#password", "secret_sauce"]}, {"click": "#login-button"}],
      "alvo": "locked out", "zoom_em": 1.6, "caixa_em": 2.2, "legenda": "A mensagem: this user has been locked out"}),
    ("Então a conferência é: essa mensagem apareceu. E não precisa copiar a frase inteira: o pedaço locked out, bloqueado, já mostra que é a mensagem certa.",
     edc(DOIS, "Confere a mensagem de erro", digitar=True, digitar_de=L_T2 + 5, digitar_ate=L_T2 + 5, rolar=True, rolar_de=0.4, rolar_dur=0.8, fonte=24)),
    ("Traduzindo: eu espero que o texto locked out esteja aparecendo na tela. Se aparecer, o site barrou o usuário bloqueado, do jeito certo, e o teste passa.",
     {"type": "traducao", "codigo": "await expect(page.getByText('locked out')).toBeVisible();", "partes": [["expect", "eu espero que"], ["page.getByText('locked out')", "o texto locked out"], ["toBeVisible()", "esteja aparecendo"]], "passo": 1.6}),
    ("Agora você tem dois testes, e os dois são sobre login. Daqui a pouco, esse arquivo vai ter muito mais. Então, antes de continuar, a gente organiza em dois passos.",
     {"type": "cards", "titulo": "ORGANIZANDO EM 2 PASSOS", "itens": [["1", "describe", "junta os testes de login numa caixa"], ["2", "before each", "o que se repete antes de cada teste da caixa", "#69a7ff"]]}),
    ("O primeiro é o describe. Describe é descrever: ele junta testes do mesmo assunto numa caixa com nome. E pra que a caixa? No relatório, os testes aparecem juntos, por assunto. E o que você colocar dentro dela, como o before each daqui a pouco, vale pros testes da caixa.",
     {"type": "traducao", "codigo": "test.describe('Login', () => {", "partes": [["describe", "junte numa caixa"], ["'Login'", "com o nome Login"]], "passo": 2.0}),
    ("Logo depois do import, escreve: test ponto describe, abre parênteses, entre aspas Login, vírgula, abre e fecha parênteses, seta, e abre chaves.",
     edc("\n".join(LDS[:12]), "test.describe('Login', () => {", digitar=True, digitar_de=3, digitar_ate=3, fonte=26, destaque=[3], destaque_em=4.5)),
    ("Lá no final do arquivo, fecha a caixa: chave, parêntese e ponto e vírgula. E os dois testes vão pra dentro dela: seleciona os dois e aperta Tab, pra eles andarem um pouco pra direita.",
     edc("\n".join(LDS[12:]), "}); fecha a caixa · Tab: os testes vão pra dentro", linha0=13, digitar=True, digitar_de=len(LDS) - 12, digitar_ate=len(LDS) - 12, fonte=26, destaque=[len(LDS) - 12], destaque_em=2.0)),
    ("Agora repara numa coisa: a primeira linha dos dois testes é igual. Os dois abrem o site.",
     edc(C_DESC, "O goto se repete nos dois testes", destaque=L_GOTOS_D, destaque_em=0.6, fonte=22, rolar=True, rolar_de=2.4, rolar_dur=1.6)),
    ("E esse é o segundo passo: quando alguma coisa se repete antes de todo teste da caixa, existe o before each. Before each: antes de cada.",
     {"type": "traducao", "codigo": "test.beforeEach(async ({ page }) => {", "partes": [["before", "antes de"], ["Each", "cada"], ["({ page })", "me dê o navegador"]], "passo": 2.0}),
    ("Ele vai dentro do describe, logo no começo, antes dos testes. E lá dentro, o goto.",
     edc("\n".join(LT[:13]), "test.beforeEach dentro do describe", digitar=True, digitar_de=4, digitar_ate=6, fonte=22)),
    ("Agora o goto dos testes não precisa mais: o before each já abre o site antes de cada um. Então apaga a linha do goto do primeiro teste.",
     edc("\n".join(LT[:L_GOTOS_T[1] - 3]), "Apaga o goto do primeiro teste", apagar=[L_GOTOS_T[0]], apagar_em=2.6, destaque=[5], destaque_em=0.6, fonte=20)),
    ("E agora a mesma coisa no segundo teste: apaga a linha do goto dele também. Pronto: os dois testes começam direto no login, e quem abre o site é o before each.",
     edc("\n".join(l for i, l in enumerate(LT) if i + 1 != L_GOTOS_T[0])[0:0] + "\n".join([l for i, l in enumerate(LT) if i + 1 != L_GOTOS_T[0]][L_GOTOS_T[1] - 4:]), "Apaga o goto do segundo teste",
         linha0=L_GOTOS_T[1] - 3, apagar=[3], apagar_em=3.2, fonte=26)),
    ("O before each roda antes de cada teste: antes do teste um, abre o site. Antes do teste dois, abre de novo. Assim, cada teste começa do zero, sem depender do outro.",
     {"type": "cards", "titulo": "ANTES DE CADA", "itens": [["1", "Antes do teste 1", "abre o site"], ["2", "Antes do teste 2", "abre de novo", "#69a7ff"], ["✓", "Cada teste", "começa do zero", "#3fd68a"]]}),
    ("E por que o login não foi pro before each também? Porque o segundo teste entra com outro usuário. No before each só vai o que é igual em todos os testes.",
     {"type": "traducao", "titulo": "O QUE VAI NO BEFORE EACH", "linhas": [["abrir o site", "igual nos dois: before each"], ["o login", "muda o usuário: fica no teste"]]}),
    ("Lendo em português: um grupo chamado Login. Antes de cada teste, abra o site. Teste um: entra. Teste dois: mostra erro pro bloqueado.",
     {"type": "cards", "itens": [["▣", "Grupo Login", "describe"], ["↺", "Antes de cada", "abra o site", "#69a7ff"], ["1", "Teste 1", "entra", "#ffd23f"], ["2", "Teste 2", "erro do bloqueado", "#c792ea"]]}),
    ("E pra que a caixa? Num projeto de verdade, você tem um describe pra cada parte do site: Login, Carrinho, Checkout. Quando algo falha, você sabe na hora de qual parte é.",
     {"type": "cards", "titulo": "UM DESCRIBE POR PARTE DO SITE", "itens": [["🔑", "Login", "um describe"], ["🛒", "Carrinho", "outro describe", "#69a7ff"], ["💳", "Checkout", "outro describe", "#ffd23f"]]}),
    ("Roda: os dois passam.", vs(C22, "Os dois passam", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.1s)", "ac")))),
    ("E no relatório eles aparecem juntos, debaixo de Login.", {"type": "pw_relatorio", "testes": REL22, "legenda": "Juntos, debaixo de Login"}),
    ("Na próxima aula: o arquivo de configuração.", proxima("playwright.config")[0]),
    ("Te vejo lá!", proxima("playwright.config")[1]),
]))


def trocas(antigo, novo, de, ate, em=None):
    """linhas de..ate (1 = primeira) que mudaram entre o código antigo e o novo, no formato do 'trocar' (linha relativa ao trecho)"""
    a, n = antigo.split("\n")[de - 1:ate], novo.split("\n")[de - 1:ate]
    assert len(a) == len(n)
    r = [[i + 1, x] for i, (x, y) in enumerate(zip(a, n)) if x != y]
    if em is not None and r:
        r[0] += [None, em]
    return r

for _s in AULAS[-1][1]["script"]["long"]["parts"][0]["sentences"]:  # trava: toda linha apagada na aula 22 tem que ser um goto ou o teste lento
    _c = _s["scene"]
    if _c.get("apagar") and "goto" in _c.get("legenda", ""):
        assert all("page.goto" in _c["codigo"].split("\n")[i - 1] for i in _c["apagar"]), _c["legenda"]

# ---------- Aula 23 ----------
USE0 = 26  # o trecho do config que aparece: linhas 26 a 34 (reporter, use e o fim do use)
CFG_USE = CONFIG[USE0 - 1:34]
CFG_BASE = [l if "// baseURL" not in l else "    baseURL: 'https://www.saucedemo.com'," for l in CFG_USE]
CFG_TID = CFG_BASE[:5] + ["    testIdAttribute: 'data-test',"] + CFG_BASE[5:]
assert CFG_USE[2].strip() == "use: {" and "baseURL" in CFG_BASE[4] and CFG_USE[4].strip().startswith("// baseURL")
C23_GOTO = C22.replace("aula 22: ", "").replace("page.goto('https://www.saucedemo.com/')", "page.goto('/')")
C23L = C23.replace("aula 23: ", "")
AULAS.append(projeto(23, "MÓDULO 5 · AULA 23", "playwright.config - baseURL e data-test", [
    ("Hoje a gente mexe no arquivo de configuração. Parece assustador, mas são só duas linhas.", titulo(23, "CONFIG")),
    ("Abre o playwright ponto config ponto js e procura o use. Use quer dizer: use isso em todos os testes.",
     edc(cfg(CFG_USE), "use = use isso em todos os testes", arquivo="playwright.config.js", linha0=USE0, destaque=[3], destaque_em=1.0, fonte=26)),
    ("Repara na linha da baseURL: ela está comentada, com as duas barras na frente. Primeiro, apaga as duas barras. Depois, apaga o endereço de exemplo, o localhost, e escreve no lugar o endereço do Sauce Demo. Base URL: o endereço base.",
     edc(cfg(CFG_BASE), "baseURL = o endereço base", arquivo="playwright.config.js", linha0=USE0, fonte=26,
         trocar=[[5, CFG_USE[4], CFG_USE[4].replace("// ", ""), 4.6], [5, CFG_USE[4].replace("// ", ""), None, 7.4]])),
    ("Agora, no teste, apaga o endereço que está dentro do goto e deixa só a barra. O Playwright junta essa barra com o endereço base.",
     edc("\n".join(C23_GOTO.split("\n")[:7]), "baseURL + /  =  saucedemo.com/", fonte=28, trocar=trocas(C22.replace("aula 22: ", ""), C23_GOTO, 1, 7, em=3.0))),
    ("A vantagem: se um dia o site mudar de endereço, você troca num lugar só.",
     {"type": "cards", "itens": [["⌂", "baseURL", "o endereço num lugar só"], ["/", "page.goto('/')", "nos testes, só o caminho", "#69a7ff"]]}),
    ("E no trabalho isso é muito usado: o mesmo teste roda no site de teste da empresa e no site de verdade. Só muda o endereço base.", {'type': 'compare', 'title': 'O MESMO TESTE', 'items': [['SITE DE TESTE', 'TESTE.LOJA.COM', 'white'], ['SITE DE VERDADE', 'LOJA.COM', 'gold']], 'size': 90, 'stagger': 1.8, 'vs': False}),  # pra que / quando
    ("Segunda linha: test id attribute igual data-test. Lembra do data-test que a gente viu no Inspecionar?",
     edc(cfg(CFG_TID), "testIdAttribute: 'data-test'", arquivo="playwright.config.js", linha0=USE0, digitar=True, digitar_de=6, digitar_ate=6, fonte=26)),
    ("Por padrão, o get by test id procura data-testid. O saucedemo usa data-test. Essa linha avisa o Playwright.",
     {"type": "compare", "items": [["data-testid", "O PADRÃO DO PLAYWRIGHT", "white"], ["data-test", "O QUE O SAUCEDEMO USA", "gold"]], "size": 90, "stagger": 1.2, "vs": True}),
    ("E por que usar o data-test? Porque ele existe só pra teste. O texto Username pode mudar: alguém traduz pra Usuário, e o seletor pelo texto quebra. O data-test continua igual.", {'type': 'compare', 'title': 'SE ALGUÉM TRADUZIR A TELA', 'items': [['PELO TEXTO', 'QUEBRA', 'white'], ['PELO DATA-TEST', 'CONTINUA FUNCIONANDO', 'gold']], 'size': 90, 'stagger': 1.8, 'vs': False}),  # pra que / quando
    ("No trabalho, é comum quem testa pedir pra quem desenvolve colocar data-test nos elementos importantes. É um dos seletores mais estáveis que existem.", {'type': 'cards', 'itens': [['🙋', 'Quem testa', 'pede o data-test'], ['👩\u200d💻', 'Quem desenvolve', 'coloca uma vez', '#69a7ff'], ['✓', 'Teste estável', 'não quebra à toa', '#3fd68a']]}),  # pra que / quando
    ("Então, vamos trocar os seletores que já estão nos testes pelo data-test. Repara: o before each continua igual, ele só abre o site.",
     edc("\n".join(C23.replace("aula 23: ", "").split("\n")[:12]), "O beforeEach só abre o site", fonte=24, destaque=[4, 5, 6], destaque_em=3.0)),
    ("E de onde vêm esses nomes? Do próprio site. Clica com o botão direito no campo de usuário, e Inspecionar. Lá está: data-test igual username.",
     {"type": "devtools", "media": "site_sauce_dev_user", "url": SAUCE, "inspecionar": "[data-test=\"username\"]", "attrs": ["class", "placeholder", "type", "data-test", "id", "name"], "realce": ["data-test"], "realce_em": 2.2, "realce_rotulo": "username", "legenda": "Campo usuário: data-test=\"username\""}),
    ("No campo da senha, a mesma coisa: data-test igual password.",
     {"type": "devtools", "media": "site_sauce_dev_pass", "url": SAUCE, "inspecionar": "[data-test=\"password\"]", "attrs": ["class", "placeholder", "type", "data-test", "id", "name"], "realce": ["data-test"], "realce_em": 2.2, "realce_rotulo": "password", "legenda": "Campo senha: data-test=\"password\""}),
    ("E no botão: data-test igual login button. São esses nomes que vão dentro do get by test id.",
     {"type": "devtools", "media": "site_sauce_dev_btn", "url": SAUCE, "inspecionar": "[data-test=\"login-button\"]", "attrs": ["class", "placeholder", "type", "data-test", "id", "name"], "realce": ["data-test"], "realce_em": 2.2, "realce_rotulo": "login-button", "legenda": "Botão: data-test=\"login-button\""}),
    ("A troca é assim: onde estava get by placeholder Username, fica get by test id username. A senha vira password. E o botão vira login button.",
     {"type": "traducao", "titulo": "A MESMA COISA, OUTRO SELETOR", "linhas": [["getByPlaceholder('Username')", "getByTestId('username')"], ["getByPlaceholder('Password')", "getByTestId('password')"],
                                                                           ["getByRole('button', { name: 'Login' })", "getByTestId('login-button')"]]}),
    ("No primeiro teste, troca as três linhas do login. Repara: só o pedaço do seletor é apagado e escrito de novo. O resto da linha, o fill com o usuário, o fill com a senha e o click, continua igual.",
     edc("\n".join(C23L.split("\n")[7:12]), "Teste 1: os três seletores trocados", linha0=8, fonte=26, trocar=trocas(C23_GOTO, C23L, 8, 12, em=1.6))),
    ("E no segundo teste, a mesma troca nas três linhas. Os seletores antigos também estavam certos: é só outro caminho pro mesmo lugar. Mas o data-test é o caminho que menos quebra.",
     edc("\n".join(C23L.split("\n")[17:24]), "Teste 2: a mesma troca", linha0=18, fonte=24, trocar=trocas(C23_GOTO, C23L, 18, 24, em=1.6))),
    ("Traduzindo: ache pela etiqueta de teste chamada username.",
     {"type": "traducao", "codigo": "page.getByTestId('username')", "partes": [["getByTestId", "ache pela etiqueta de teste"], ["'username'", "chamada username"]], "passo": 2.0}),
    ("Roda pra confirmar que tudo continua passando.", vs(C23, "Tudo continua passando", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.0s)", "ac")))),
    ("Na próxima aula: tirando o usuário e a senha do código.", proxima("variáveis de ambiente")[0]),
    ("Te vejo lá!", proxima("variáveis de ambiente")[1]),
]))

# ---------- Aula 24 ----------
ENV = "SAUCE_USER=standard_user\nSAUCE_PASSWORD=secret_sauce"
CFG_TOPO = CONFIG[:15]
CFG_DOTENV = [re.sub(r"^// ", "", l) if ("dotenv" in l or "import path" in l) and l.startswith("// ") else l for l in CFG_TOPO]
assert sum(1 for a, b in zip(CFG_TOPO, CFG_DOTENV) if a != b) == 3
C24L = C24.replace("aula 24: ", "")
AULAS.append(projeto(24, "MÓDULO 5 · AULA 24", "Variáveis de ambiente - tirando usuário e senha do código", [
    ("Aqui no saucedemo o usuário e a senha são públicos. Mas em projeto de verdade, senha e chave escrita no código é um problema: quando o projeto for pro GitHub, todo mundo vê.",
     titulo(24, ".ENV")),
    ("Então a gente vai aprender o jeito usado em projetos reais: um arquivo chamado ponto env, que guarda essas informações fora do código.",
     {"type": "cards", "titulo": "O ARQUIVO .ENV", "itens": [["🔒", ".env", "usuário e senha fora do código"]]}),
    ("A ideia é simples. O ponto env fica só no seu computador. O teste não tem mais a senha escrita: ele pede pro ponto env. E cada pessoa do time coloca o próprio usuário e a própria senha no ponto env dela.",
     {"type": "cards", "itens": [["💻", "Fica no seu computador", "não vai pro GitHub"], ["📄", "O teste pede", "pro .env", "#69a7ff"], ["👥", "Cada pessoa", "com o seu usuário e senha", "#ffd23f"]]}),
    ("Pra ler esse arquivo, a gente usa um pacote chamado dotenv. Pacote é um código pronto que alguém já escreveu e que você baixa pro seu projeto.",
     {"type": "cards", "titulo": "PACOTE", "itens": [["📦", "dotenv", "um código pronto que lê o .env"]]}),
    ("No terminal: npm install traço D dotenv. Install quer dizer instalar. E o traço D marca como ferramenta de desenvolvimento do projeto.",
     vs(C23, "npm install -D dotenv", run(("added 1 package, and audited 6 packages in 1s", "mut"), ("found 0 vulnerabilities", "ac"), cmd="npm install -D dotenv"))),
    ("Na pasta do projeto, cria o arquivo ponto env.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [0], "pastas": ARV, "alvo_item": "meu-primeiro-playwright",
      "novo_pos": 5, "resultado": "arquivo", "novo": ".env", "novo_nivel": 1, "legenda": "New File › .env"}),
    ("Dentro: SAUCE underline USER igual standard user, e SAUCE underline PASSWORD igual secret sauce.",
     edc(ENV, "Usuário e senha no .env", arquivo=".env", pastas=ARV_ENV, digitar=True, fonte=32)),
    ("E antes de qualquer outra coisa: o ponto gitignore. Ignore é ignorar: é a lista de arquivos que o Git deixa de fora quando você manda o projeto pro GitHub. Escreve ponto env no final dele.",
     edc(GITIGNORE + "\n.env", ".env no .gitignore", arquivo=".gitignore", pastas=ARV_ENV, digitar=True, digitar_de=len(GITIGNORE.split("\n")) + 1, fonte=30)),
    ("Agora o config. Lá em cima já tem três linhas do dotenv, só que comentadas: com as duas barras na frente, o Playwright ignora. Apaga as duas barras das três linhas.",
     edc("\n".join(CFG_DOTENV), "Tira as duas barras das 3 linhas", arquivo="playwright.config.js", pastas=ARV_ENV, descomentar=[8, 9, 10], descomentar_em=7.2, destaque=[8, 9, 10], destaque_em=3.0, fonte=22)),
    ("Lendo em português: importe o dotenv, importe o path, que cuida dos caminhos das pastas, e leia o arquivo ponto env que está nesta pasta.",
     {"type": "traducao", "titulo": "AS 3 LINHAS DO DOTENV", "linhas": [["import dotenv from 'dotenv';", "traga o dotenv"], ["import path from 'path';", "traga o path (caminhos)"],
                                                                     ["dotenv.config({ path: ... '.env' })", "leia o .env desta pasta"]]}),
    ("No teste, apaga o standard user que está escrito, e no lugar escreve process ponto env ponto SAUCE underline USER. Depois apaga a secret sauce, e no lugar escreve process ponto env ponto SAUCE underline PASSWORD.",
     edc("\n".join(C24L.split("\n")[7:12]), "O teste pede pro .env", linha0=8, pastas=ARV_ENV, fonte=22, trocar=trocas(C23L, C24L, 8, 12, em=2.0))),
    ("No segundo teste, o usuário bloqueado continua escrito, porque ele é o que o teste quer testar. Só a senha muda: apaga a secret sauce, e no lugar vai o process ponto env ponto SAUCE underline PASSWORD.",
     edc("\n".join(C24L.split("\n")[17:24]), "Teste 2: só a senha vem do .env", linha0=18, pastas=ARV_ENV, fonte=22, trocar=trocas(C23L, C24L, 18, 24, em=6.0))),
    ("Traduzindo: process ponto env, as variáveis do ambiente. SAUCE underline USER, a variável com esse nome. Quando o teste roda, o dotenv já leu o arquivo, e aqui entra o standard user.",
     {"type": "traducao", "codigo": "process.env.SAUCE_USER", "partes": [["process.env", "as variáveis do ambiente"], ["SAUCE_USER", "a chamada SAUCE_USER"]], "passo": 2.0}),
    ("Dentro, só os nomes das variáveis, sem os valores. Example quer dizer exemplo: quem baixar copia esse arquivo, chama de ponto env, e coloca os próprios valores.",
     edc("SAUCE_USER=\nSAUCE_PASSWORD=", "Só os nomes, sem os valores", arquivo=".env.example", pastas=ARV_EX, digitar=True, fonte=32,
         criar=[["E pra quem baixar o projeto saber o que preencher, cria mais um arquivo na pasta do projeto: ponto env ponto example.", ".env.example"]])),
    ("Roda pra confirmar: continua passando.", vs(C24, "Continua passando", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.0s)", "ac")), pastas=ARV_EX)),
    ("E no GitHub, onde não existe o seu ponto env? Lá, quem entrega esses valores são os secrets, um cofre do próprio GitHub. Você vê isso na aula 45.", {'type': 'cards', 'itens': [['💻', 'Na sua máquina', 'o arquivo .env'], ['☁', 'No GitHub', 'os secrets, na aula 45', '#69a7ff']]}),  # pra que / quando
    ("Na próxima aula: rodando só o que importa.", proxima("only, skip e filtros")[0]),
    ("Te vejo lá!", proxima("only, skip e filtros")[1]),
]))

# ---------- Aula 25 ----------
C25_ONLY = C24.replace("aula 24: ", "").replace("test('mostra erro", "test.only('mostra erro")
C25_SKIP = C24.replace("aula 24: ", "").replace("test('mostra erro", "test.skip('mostra erro")
L_ONLY = [i + 1 for i, l in enumerate(C25_ONLY.split("\n")) if "test.only" in l][0]
AULAS.append(projeto(25, "MÓDULO 5 · AULA 25", "Rodando só o que importa - only, skip, arquivo e nome", [
    ("Quando você tiver dezenas de testes, não vai querer rodar todos toda hora.", titulo(25, "SÓ O QUE IMPORTA")),
    ("Pra rodar um arquivo só, coloca o nome dele: npx playwright test login ponto spec ponto js.",
     vs(C24, "Um arquivo só", run(("Running 6 tests using 4 workers", "mut"), ("  6 passed (4.3s)", "ac"), cmd="npx playwright test login.spec.js"), pastas=ARV_EX)),
    ("Pra rodar pelo nome do teste: traço g e um pedaço do nome, tipo bloqueado. O g vem de grep, que quer dizer procurar: ele filtra os testes por esse pedaço de nome.",
     vs(C24, "-g = grep = procurar pelo nome", run(("Running 3 tests using 3 workers", "mut"), ("  3 passed (2.2s)", "ac"), cmd="npx playwright test -g bloqueado"), pastas=ARV_EX)),
    ("Dentro do código: no teste do bloqueado, logo depois do test, escreve ponto only. Test ponto only: roda somente esse teste. Only quer dizer somente.",
     edc(C25_ONLY, "only = somente", pastas=ARV_EX, rolar=True, rolar_de=0.8, rolar_dur=1.0, fonte=22, trocar=[[L_ONLY, C25_ONLY.split("\n")[L_ONLY - 1].replace("test.only(", "test("), None, 2.4]])),
    ("Cuidado: esquecer um only é um erro clássico. Os outros testes param de rodar e ninguém percebe. Por isso o config já vem com forbid only, que trava isso no GitHub.",
     {"type": "cards", "itens": [["⚠", "Esqueceu o only?", "os outros param de rodar", "#ff8c42"], ["🛡", "forbidOnly", "trava isso no GitHub", "#69a7ff"]]}),
    ("Agora apaga o only e escreve skip no lugar. Test ponto skip: pula esse teste. Skip quer dizer pular. No resultado, ele aparece como skipped.",
     edc("\n".join(C25_SKIP.split("\n")[L_ONLY - 4:L_ONLY + 4]), "skip = pular: aparece como skipped", linha0=L_ONLY - 3, pastas=ARV_EX, trocar=[[4, C25_ONLY.split("\n")[L_ONLY - 1], None, 1.0]],
         terminal=run(("Running 2 tests using 1 worker", "mut"), ("  1 skipped", "yel"), ("  1 passed (1.8s)", "ac")))),
    ("E você já conhece o traço traço project igual chromium, pra rodar num navegador só.",
     {"type": "cards", "itens": [["C", "--project=chromium", "só esse navegador"]]}),
    ("Resumindo: o nome do arquivo roda só aquele arquivo. Traço g filtra pelo nome do teste. Test ponto only roda somente aquele teste. Test ponto skip pula. E traço traço project escolhe o navegador.",
     {"type": "traducao", "titulo": "RODANDO SÓ O QUE IMPORTA", "linhas": [["npx playwright test login.spec.js", "só esse arquivo"], ["npx playwright test -g bloqueado", "só os testes com esse nome"],
                                                                         ["test.only(...)", "somente esse teste"], ["test.skip(...)", "pula esse teste"], ["--project=chromium", "só esse navegador"]]}),
    ("E no dia a dia, quando usar cada um? Mexendo só no login: roda o arquivo. Um teste falhou: roda só ele, com o traço g. Investigando um teste no código: only, e tira depois. Um bug conhecido que ainda não foi corrigido: skip, com um comentário dizendo o motivo.", {'type': 'traducao', 'titulo': 'NO DIA A DIA', 'em_frac': [0.142, 0.285, 0.458, 0.665], 'linhas': [['mexendo só no login', 'login.spec.js'], ['um teste falhou', '-g bloqueado'], ['investigando no código', 'test.only, e tira depois'], ['bug conhecido, sem correção', 'test.skip + o motivo']]}),  # pra que / quando
    ("Fechamos a organização. No próximo módulo: o que fazer quando o teste falha.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Debug: quando o teste falha"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 6 · DEBUG"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 5 (gerado do roteiro_playwright_m5.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo5.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

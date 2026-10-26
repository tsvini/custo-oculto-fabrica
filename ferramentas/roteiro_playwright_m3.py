"""Gera projetos/curso-playwright-12..16 (módulo 3: primeiro teste). Roteiro aprovado em curso-playwright/roteiros/modulo3.md.
O código de cada aula é o mesmo de curso-playwright/projeto/tests/etapas/aulaNN.spec.js (validado no Actions), sem o "aula NN:" do nome."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m2 import vterm, PASTA

SAUCE = "https://www.saucedemo.com/"
ARV = ["meu-primeiro-playwright", "  .github/", "  node_modules/", "  tests/", "    login.spec.js", "  .gitignore", "  package-lock.json", "  package.json", "  playwright.config.js"]
ARV_EX = [p.replace("login.spec.js", "example.spec.js") for p in ARV]
ARV_SEM = [p for p in ARV if "login.spec.js" not in p]
LOGIN = [{"fill": ["#user-name", "standard_user"]}, {"fill": ["#password", "secret_sauce"]}, {"click": "#login-button"}]


def codigo(n):
    s = open(os.path.join(RAIZ, "curso-playwright", "projeto", "tests", "etapas", f"aula{n}.spec.js"), encoding="utf8").read().rstrip("\n")
    return re.sub(r"test\('aula \d+: ", "test('", s)


def parcial(n, k, fecha=True):
    """o arquivo da aula n só até a linha k, fechando o teste (o que vem depois ainda não foi escrito)"""
    return "\n".join(codigo(n).split("\n")[:k] + (["});"] if fecha else []))


def ed(n, legenda, de=None, ate=None, destaque=None, digitar=True, colinha=False, ate_linha=None, fecha=True, **kw):
    cod = parcial(n, ate_linha, fecha) if ate_linha else codigo(n)
    d = {"type": "editor", "arquivo": "login.spec.js", "pastas": ARV, "codigo": cod, "legenda": legenda, "fonte": 26}
    # trava: depois da linha que está sendo digitada só pode haver o fechamento do teste (nada "do futuro" na tela)
    if digitar and (ate or de):
        resto = [l for l in cod.split("\n")[(ate or de):] if l.strip()]
        assert all(l.strip() in ("});", "})", "}") for l in resto), f"aula {n}: linha do futuro na tela: {resto}"
    if max(len(l) for l in codigo(n).split("\n")) > 66:  # linha comprida: sem o Explorer, pra letra continuar grande
        del d["pastas"]
    if not digitar:
        d["digitar"] = False
    if de:
        d["digitar_de"] = de
    if ate:
        d["digitar_ate"] = ate
    if destaque:
        d["destaque"] = destaque
    if colinha:
        d.update({"colinha": True, "colinha_em": 1.6})
    d.update(kw)
    return d


def tela(media, legenda, alvo_css=None, alvo=None, acoes=None, titulo_t="saucedemo.com"):
    d = {"type": "tela", "media": media, "url": SAUCE, "titulo": titulo_t, "legenda": legenda, "zoom_em": 1.4, "caixa_em": 2.0}
    if alvo_css:
        d["alvo_css"] = alvo_css
    if alvo:
        d["alvo"] = alvo
    if acoes:
        d["acoes"] = acoes
    return d


HEADED = [{"cmd": "npx playwright test --headed --project=chromium"}, {"out": "Running 1 test using 1 worker", "cor": "mut"}, {"out": "  1 passed (2.4s)", "cor": "ac"}]

AULAS = []
AULAS.append(projeto(12, "MÓDULO 3 · AULA 12", "A receita de um teste - test e expect", [
    ("Agora começa o seu código. E a primeira coisa é apagar o exemplo: clica com o botão direito em cima do example ponto spec ponto js e escolhe Delete.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename...", "Delete"]], "caminho": [7], "pastas": ARV_EX, "apaga": "example.spec.js", "legenda": "Botão direito › Delete"}),
    ("Agora clica com o botão direito na pasta tests, escolhe New File, e dá o nome: login ponto spec ponto js.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [0], "pastas": ARV_SEM, "alvo_item": "tests", "novo_pos": 4, "resultado": "arquivo", "novo": "login.spec.js", "novo_nivel": 2, "legenda": "tests › New File › login.spec.js"}),
    ("Esse ponto spec no nome é o que avisa o Playwright: esse arquivo aqui é um teste.",
     {"type": "cards", "titulo": "LOGIN.SPEC.JS", "itens": [["✎", "login", "o nome que você escolhe"], ["✓", ".spec", "avisa: isso é um teste", "#69a7ff"], ["{ }", ".js", "arquivo JavaScript"]]}),
    ("Primeira linha: import, chaves, test, vírgula, expect, fecha chaves, from, e entre aspas arroba playwright barra test.",
     ed(12, "A primeira linha", ate=1, colinha=True, ate_linha=1, fecha=False)),
    ("Lendo em português: traga o test e o expect, de dentro do Playwright. O test serve pra criar um teste, e o expect, pra conferir o resultado.",
     {"type": "traducao", "codigo": "import { test, expect } from '@playwright/test';", "partes": [["import", "traga"], ["{ test, expect }", "test e expect"], ["from", "de dentro do"], ["'@playwright/test'", "Playwright"]], "passo": 1.8}),
    ("Agora o teste: test, abre parênteses, o nome do teste entre aspas, entra com usuário e senha, vírgula, async, abre parênteses, abre chaves, page, fecha chaves, fecha parênteses, seta, e abre chaves. E lá embaixo, fecha com chave, parêntese e ponto e vírgula.",
     ed(12, "O esqueleto do teste", de=3)),
    ("Parece muita coisa, né? Então vamos traduzir essa linha pedaço por pedaço.",
     {"type": "traducao", "codigo": "test('entra com usuário e senha', async ({ page }) => {", "partes": [["test", "crie um teste"], ["'entra com usuário e senha'", "com este nome"], ["async", "que tem esperas"], ["({ page })", "me dê o navegador"], ["=> {", "e faça isto:"]], "passo": 1.2}),
    ("O nome entre aspas é você que escolhe. Ele aparece no relatório, então escreve o que o teste faz, em português mesmo.", ed(12, "O nome aparece no relatório", digitar=False, destaque=[3], destaque_em=0.8)),
    ("O page é o navegador que o Playwright te entrega pronto. É com ele que você abre sites, digita e clica.", ed(12, "page = o navegador", digitar=False, destaque=[3], destaque_em=0.8)),
    ("E o async quer dizer que, lá dentro, a gente vai usar o await, que significa: espera esse passo terminar antes de ir pro próximo.",
     {"type": "cards", "titulo": "ASYNC E AWAIT", "itens": [["⏳", "async", "aqui dentro tem espera"], ["⏸", "await", "espera esse passo terminar", "#69a7ff"]]}),
    ("E a última linha, com chave, parêntese e ponto e vírgula, fecha tudo que foi aberto lá em cima. Os passos do teste vão aqui no meio, entre essas duas linhas.", ed(12, "Os passos vão aqui no meio", digitar=False, destaque=[3, 5], destaque_em=0.8)),
    ("Então, lendo inteiro: crie um teste chamado entra com usuário e senha, me dê o navegador, e faça o que estiver aqui dentro.", bt(("CRIE UM TESTE,", "white", 80), ("ME DÊ O NAVEGADOR", "gold", 100), ("E FAÇA O QUE ESTÁ AQUI DENTRO", "white", 72), entre=1.35)),
    ("Esse é o esqueleto de todo teste. Ainda está vazio, e na próxima aula a gente coloca o primeiro passo.", ed(12, "O esqueleto de todo teste", digitar=False)),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: PAGE.GOTO"}),
]))

CMD_HEADED = "npx playwright test --headed --project=chromium"


def vscode_term(n, legenda, terminal, **kw):
    """o VS Code inteiro: código em cima e o terminal integrado embaixo (como o aluno vê na tela dele)"""
    d = ed(n, legenda, digitar=False)
    d.update({"terminal": terminal}); d.update(kw)
    return d


AULAS.append(projeto(13, "MÓDULO 3 · AULA 13", "page.goto - abrindo um site", [
    ("Primeiro passo de todo teste: abrir o site.", titulo(13, "PAGE.GOTO")),
    ("Dentro do teste, digita await page ponto goto, e entre aspas o endereço: https dois pontos barra barra www ponto saucedemo ponto com.", ed(13, "await page.goto(endereço)", de=4, ate=4, colinha=True)),
    ("Vamos ler em português. Go to, em inglês, é ir para. Então: espere a página ir para esse endereço.",
     {"type": "traducao", "codigo": "await page.goto('https://www.saucedemo.com/');", "partes": [["await", "espere"], ["page", "a página"], ["goto", "ir para"], ["'https://www.saucedemo.com/'", "este endereço"]], "passo": 1.8}),
    ("Esse é o site de treino que a gente vai usar no curso todo: uma lojinha feita pra quem está aprendendo a testar.", tela("site_sauce", "O site de treino")),
    ("Agora roda. Aqui embaixo no VS Code, no terminal, digita: npx playwright test traço traço headed traço traço project igual chromium.",
     vscode_term(13, "No terminal do VS Code", [{"cmd": CMD_HEADED, "em": 0.2}])),
    ("O headed mostra a janela do navegador, e o project igual chromium roda só no Chromium, pra ficar mais rápido.",
     dict({"type": "cards", "itens": [["▢", "--headed", "mostra a janela"], ["C", "--project=chromium", "só no Chromium", "#69a7ff"]]}, colinha=True, colinha_em=1.2)),
    ("Aperta Enter e olha: o navegador abre sozinho, entra no saucedemo, e fecha. E no terminal aparece: um passed. O teste passou, porque abrir o site deu certo.",
     vscode_term(13, "Abriu, entrou no site e fechou", [{"cmd": CMD_HEADED, "ja": True}, {"out": "Running 1 test using 1 worker", "cor": "mut", "em": 0.08}, {"out": "  1 passed (2.4s)", "cor": "ac", "em": 0.68}],
                 navegador={"media": "rec_sauce_abre", "url": SAUCE, "gravar": True, "acoes": [], "espera_inicio": 1800, "espera_fim": 600, "titulo": "Chromium", "em": 0.12, "ate": 0.64})),
    ("Abriu e fechou bem rápido, né? É normal: por enquanto o teste só tem um passo. Conforme a gente coloca mais passos, você vai ver ele fazendo cada um.", ed(13, "Por enquanto, um passo só", digitar=False, destaque=[4], destaque_em=0.8)),
    ("Na próxima aula, a gente preenche o login.", proxima("fill: preenchendo campos")[0]),
    ("Te vejo lá!", proxima("fill: preenchendo campos")[1]),
]))

def gravacao(media, legenda, acoes, titulo_t="saucedemo.com"):
    """vídeo de verdade do navegador fazendo as ações (o aluno vê o robô digitando e clicando)"""
    return {"type": "tela", "media": media, "url": SAUCE, "gravar": True, "acoes": acoes, "titulo": titulo_t, "legenda": legenda}


AULAS.append(projeto(14, "MÓDULO 3 · AULA 14", "fill - preenchendo campos", [
    ("Hoje o robô digita usuário e senha.", titulo(14, "FILL")),
    ("Mas antes: como ele sabe qual é o campo? Olha o site: dentro do primeiro campo está escrito Username, em cinza. Isso se chama placeholder.", tela("site_sauce_user", "O texto cinza: placeholder", alvo_css="#user-name")),
    ("E o Playwright acha campos exatamente por isso. O nome do comando é get by placeholder: get by quer dizer pegar pelo, ache pelo. Então: ache pelo texto que aparece dentro do campo.",
     {"type": "traducao", "codigo": "page.getByPlaceholder('Username')", "partes": [["getByPlaceholder", "ache pelo texto de dentro do campo"], ["('Username')", "o texto: Username"]], "passo": 2.0}),
    ("Digita: await page ponto getByPlaceholder, entre aspas Username, ponto fill, e entre aspas standard underline user.", ed(14, "A linha do usuário", de=5, ate=5, vel=0.5, ate_linha=5)),
    ("Lendo em português: na página, ache o campo que tem Username escrito dentro, e preencha com standard user.",
     {"type": "traducao", "codigo": "await page.getByPlaceholder('Username').fill('standard_user');", "partes": [["page", "na página"], [".getByPlaceholder('Username')", "ache o campo Username"], [".fill('standard_user')", "e preencha com standard_user"]], "passo": 1.6}),
    ("E de onde veio o standard user? O próprio site mostra, aqui embaixo, os usuários de treino.", tela("site_sauce_cred", "O site mostra o usuário de treino", alvo="standard_user")),
    ("O fill quer dizer preencher. Ele apaga o que tiver no campo e digita o texto novo.", dict({"type": "cards", "itens": [["⌫", "Apaga", "o que tinha"], ["⌨", "Digita", "o texto novo", "#69a7ff"]]}, colinha=True, colinha_em=1.0)),
    ("A senha é igual: getByPlaceholder Password, fill secret underline sauce. Ache o campo Password e preencha com secret sauce.", ed(14, "A senha é igual", de=6, ate=6)),
    ("Agora roda com o navegador aparecendo e olha: o Playwright encontra o campo Username, preenche o usuário, depois encontra Password e preenche a senha.",
     gravacao("rec_sauce_preenche", "O robô preenchendo de verdade", [{"fill": ["#user-name", "standard_user"]}, {"fill": ["#password", "secret_sauce"]}])),
    ("Na próxima aula, a gente clica em Login e confere se deu certo.", proxima("click e expect")[0]),
    ("Te vejo lá!", proxima("click e expect")[1]),
]))

AULAS.append(projeto(15, "MÓDULO 3 · AULA 15", "Clicando no botão e conferindo se o login deu certo", [
    ("Agora falta uma coisa pro nosso login ficar completo: clicar no botão e conferir se realmente entramos.", titulo(15, "CLICAR E CONFERIR")),
    ("Primeiro, olha o botão na tela. Está escrito Login. Mas pro Playwright não importa só o texto. Ele também sabe que isso é um botão.", tela("site_sauce_botao", "Um botão, com o nome Login", alvo_css="#login-button")),
    ("É daí que vem o get by role. Role quer dizer papel, ou função. Então a gente está dizendo pro Playwright: procure um elemento que tem o papel de botão.",
     {"type": "traducao", "codigo": "page.getByRole('button')", "partes": [["getByRole", "procure pela função"], ["('button')", "de botão"]], "passo": 2.0}),
    ("Digita: await page ponto getByRole, abre parênteses, aspas button, vírgula, chaves, name dois pontos, aspas Login, fecha tudo, ponto click.", ed(15, "A linha do clique", de=7, ate=7, ate_linha=7)),
    ("Vamos ler essa linha em português. Page é a página. Get by role é procure pela função. Button é botão. Name Login é o nome que aparece pro usuário. E click é clicar.",
     {"type": "traducao", "codigo": "await page.getByRole('button', { name: 'Login' }).click();", "partes": [["page", "a página"], [".getByRole(", "procure pela função"], ["'button'", "botão"], ["{ name: 'Login' }", "com o nome Login"], [".click()", "clique"]], "passo": 1.3}),
    ("Então a frase inteira é quase isso: na página, ache o botão chamado Login e clique nele.", bt(("NA PÁGINA, ACHE O BOTÃO", "white", 100), ("CHAMADO LOGIN", "gold", 130), ("E CLIQUE NELE", "white", 100))),
    ("O await continua aparecendo no começo porque a gente quer esperar esse clique terminar antes de ir pro próximo passo.", ed(15, "await: espera o clique terminar", digitar=False, destaque=[7], destaque_em=0.6, ate_linha=7)),
    ("Agora roda com o navegador aparecendo. Ele preenche usuário, senha e clica em Login.",
     gravacao("rec_sauce_login", "O robô clicando de verdade", [{"fill": ["#user-name", "standard_user"]}, {"fill": ["#password", "secret_sauce"]}, {"click": "#login-button", "espera": 1500}])),
    ("Mas tem um problema importante aqui. O teste pode clicar no botão e mesmo assim o login dar errado. E, se a gente não conferir nada, o Playwright pode terminar o teste sem perceber o problema.", bt(("CLICAR", "white", 160), ("≠", "red", 160), ("CONFIRMAR", "gold", 160))),
    ("É por isso que existe o expect. Expect significa algo como eu espero que. Ele é a parte que verifica se o resultado ficou do jeito que a gente queria.",
     {"type": "traducao", "codigo": "expect(...)", "partes": [["expect", "eu espero que"]], "passo": 1.2}),
    ("Depois do login, olha o endereço do navegador. Antes a gente estava na página inicial. Agora apareceu inventory ponto html.",
     {"type": "compare", "title": "O ENDEREÇO MUDOU", "items": [["saucedemo.com/", "ANTES DO LOGIN", "white"], ["…/inventory.html", "DEPOIS DO LOGIN", "gold"]], "size": 90, "stagger": 1.2, "vs": False}),
    ("Então vamos usar essa mudança como prova de que o login funcionou.", tela("site_sauce_products", "inventory = entrou!", acoes=LOGIN, alvo="Products", titulo_t="saucedemo.com/inventory.html")),
    ("Digita: await expect, abre parênteses, page, fecha parênteses, ponto toHaveURL, e entre barras, inventory.", ed(15, "A conferência", de=8, ate=8, colinha=True)),
    ("Agora vamos traduzir essa linha também. Expect page é eu espero que a página. To have URL é tenha esse endereço. E inventory é o pedaço que a gente quer encontrar na URL.",
     {"type": "traducao", "codigo": "await expect(page).toHaveURL(/inventory/);", "partes": [["expect(page)", "eu espero que a página"], [".toHaveURL(", "tenha no endereço"], ["/inventory/", "a palavra inventory"]], "passo": 1.6}),
    ("Essas duas barras em volta de inventory criam uma busca por padrão. Pra gente, agora, o importante é entender assim: a URL precisa ter a palavra inventory em algum lugar.",
     {"type": "traducao", "texto_puro": True, "codigo": "https://www.saucedemo.com/inventory.html", "partes": [["inventory", "tem inventory? então passou"]], "passo": 1.2}),
    ("Então o nosso teste agora fala, em português: abra o site, preencha usuário e senha, clique em Login e confirme que entrou na página de produtos.",
     {"type": "cards", "titulo": "O SEU TESTE, EM PORTUGUÊS", "itens": [["1", "Abra", "o site"], ["2", "Preencha", "usuário e senha", "#69a7ff"], ["3", "Clique", "em Login", "#ffd23f"], ["4", "Confirme", "que entrou", "#ff6b6b"]]}),
    ("Isso é muito importante: ação não é validação. Clicar é uma ação. O expect é a conferência. Um teste de verdade normalmente precisa dos dois.",
     {"type": "compare", "title": "UM TESTE PRECISA DOS DOIS", "items": [["AÇÃO", "CLICAR, PREENCHER", "white"], ["VALIDAÇÃO", "O EXPECT CONFERE", "gold"]], "size": 120, "stagger": 1.2, "vs": True}),
    ("Agora roda de novo. Passou. E dessa vez ele não passou só porque conseguiu clicar. Ele passou porque confirmou que o login realmente funcionou.",
     vscode_term(15, "Passou porque confirmou", [{"cmd": CMD_HEADED, "em": 0.02}, {"out": "Running 1 test using 1 worker", "cor": "mut", "em": 0.1}, {"out": "  1 passed (2.4s)", "cor": "ac", "em": 0.7}],
                 navegador={"media": "rec_sauce_login_ok", "url": SAUCE, "gravar": True, "acoes": LOGIN, "espera_inicio": 900, "espera_fim": 900, "titulo": "Chromium", "em": 0.12, "ate": 0.66})),
    ("Seu primeiro teste completo está pronto. Na próxima aula, a gente vai aprender outras formas de fazer essas conferências sem precisar decorar inglês.", proxima("Os expect mais usados")[0]),
    ("Te vejo lá!", proxima("Os expect mais usados")[1]),
]))

TAB = [["expect", "eu espero que"], ["toHaveURL", "tenha no endereço"], ["toBeVisible", "esteja visível"], ["toContainText", "contenha o texto"], ["toHaveCount", "tenha essa quantidade"]]
AULAS.append(projeto(16, "MÓDULO 3 · AULA 16", "Os expect mais usados", [
    ("O expect é o coração do teste. E o jeito mais fácil de entender é ler em voz alta, como uma frase.", titulo(16, "OS EXPECT")),
    ("Olha a linha que você já tem: await expect page, to have URL inventory.", ed(16, "A conferência que você já tem", digitar=False, destaque=[8], destaque_em=0.8, ate_linha=8)),
    ("Traduzindo: expect é eu espero que. To have URL é tenha esse endereço. Então a gente pode ler a linha assim: eu espero que a página tenha inventory no endereço.",
     {"type": "traducao", "codigo": "await expect(page).toHaveURL(/inventory/);", "partes": [["expect(page)", "eu espero que a página"], [".toHaveURL(/inventory/)", "tenha inventory no endereço"]], "passo": 2.4}),
    ("Viu? Você acabou de ler inglês de programador. E os outros funcionam do mesmo jeito.", bt(("É SÓ LER", "white", 150), ("COMO UMA FRASE", "gold", 150))),
    ("O segundo é o to be visible. To be é estar, visible é visível. Eu espero que esteja visível.",
     {"type": "traducao", "codigo": "await expect(...).toBeVisible();", "partes": [["expect(...)", "eu espero que"], [".toBeVisible()", "esteja visível"]], "passo": 1.8}),
    ("Na loja, o título Products aparece lá em cima.", tela("site_sauce_products", "O título Products", acoes=LOGIN, alvo="Products", titulo_t="saucedemo.com/inventory.html")),
    ("Então: await expect, page ponto getByText Products, ponto to be visible. Lendo: eu espero que o texto Products esteja visível.", ed(16, "Eu espero que Products esteja visível", de=9, ate=9, colinha=True, ate_linha=9)),
    ("O terceiro é o to contain text. Contain é conter. Eu espero que contenha o texto.",
     {"type": "traducao", "codigo": "await expect(...).toContainText('Backpack');", "partes": [["expect(...)", "eu espero que"], [".toContainText('Backpack')", "contenha o texto Backpack"]], "passo": 1.8}),
    ("O primeiro produto se chama Sauce Labs Backpack, e backpack é mochila. A gente confere se o nome contém a palavra Backpack.",
     tela("site_sauce_mochila", "Sauce Labs Backpack = mochila", acoes=LOGIN, alvo="Sauce Labs Backpack", titulo_t="saucedemo.com/inventory.html")),
    ("Fica assim: await expect, getByText Sauce Labs Backpack, ponto to contain text Backpack.", ed(16, "Eu espero que contenha Backpack", de=10, ate=10, ate_linha=10)),
    ("O quarto é o to have count. Count quer dizer contar, ou quantidade. Eu espero que tenha essa quantidade.",
     {"type": "traducao", "codigo": "await expect(...).toHaveCount(6);", "partes": [["expect(...)", "eu espero que"], [".toHaveCount(6)", "tenha essa quantidade: 6", "count = contar / quantidade"]], "passo": 1.8}),
    ("Cada produto tem um botão Add to cart, que é adicionar ao carrinho. São seis produtos, então seis botões.",
     tela("site_sauce_botoes", "6 produtos, 6 botões Add to cart", acoes=LOGIN, alvo="Add to cart", titulo_t="saucedemo.com/inventory.html")),
    ("Então: await expect, getByRole button, nome Add to cart, ponto to have count seis.", ed(16, "Eu espero que tenha 6 botões", de=11, ate=11)),
    ("Agora olha o arquivo inteiro. No começo da aula, isso parecia código em inglês. Agora você consegue ler cada linha sozinho.", ed(16, "Você consegue ler cada linha", digitar=False, destaque=[8, 9, 10, 11], destaque_em=0.6)),
    ("Resumindo: eu espero que tenha no endereço, que esteja visível, que contenha o texto, e que tenha essa quantidade. Está tudo na sua colinha, do mesmo jeito.",
     dict({"type": "traducao", "titulo": "LEIA O CÓDIGO COMO UMA FRASE", "linhas": TAB}, colinha=True, colinha_em=2.5)),
    ("E tem outra vantagem: esses expect esperam automaticamente por alguns segundos até a condição ficar verdadeira. Por padrão, até cinco segundos. Você não precisa colocar uma espera manual.",
     bt(("ELE ESPERA", "gold", 170), ("SOZINHO", "white", 150), ("ATÉ 5 SEGUNDOS", "muted", 80))),
    ("Roda, e tudo passa. No próximo módulo, eu te mostro como achar qualquer elemento, e um truque em que o Playwright escreve o código pra você.",
     vscode_term(16, "Tudo passou!", [{"cmd": "npx playwright test --project=chromium", "em": 0.05}, {"out": "Running 1 test using 1 worker", "cor": "mut", "em": 0.45}, {"out": "  1 passed (2.6s)", "cor": "ac", "em": 0.6}])),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 4 · LOCATORS"}),
]))


def _pausas(p):
    for x in p["script"]["long"]["parts"][0]["sentences"]:  # tradução com muitas partes numa frase curta: silêncio pra todas aparecerem
        sc = x["scene"]
        if sc.get("type") == "traducao" and sc.get("partes"):
            precisa = 0.8 + (len(sc["partes"]) - 1) * sc.get("passo", 1.6) + 1.5
            falta = precisa - len(x["text"]) / 14.5
            if falta > 1.5:
                x["pausa"] = round(falta, 1)


def main():
    out = ["# Roteiros aprovados · Módulo 3 (com ajustes da revisão)", ""]
    for slug, p in AULAS:
        _pausas(p)
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo3.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

"""Gera projetos/curso-playwright-26..30 (módulo 6: debug). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Os textos de erro são a saída real das demos (curso-playwright/projeto/demos/aula26_*.demo.spec.js) rodadas no Actions.
Ajuste técnico combinado: a aula 26 quebra o toContainText ('Backpack' → 'Mochila'), porque o erro de toBeVisible não mostra "Received"."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m3 import codigo, ARV, SAUCE, LOGIN
from roteiro_playwright_m4 import edc, CMD, cg
from roteiro_playwright_m5 import vs, CONFIG, ARV_EX

C24 = codigo(24).replace("aula 24: ", "")
C26 = C24.replace("toContainText('Backpack')", "toContainText('Mochila')")
assert C26 != C24
L_MOCHILA = [i + 1 for i, l in enumerate(C26.split("\n")) if "Mochila" in l][0]  # linha 14


def run(*saida, cmd=CMD):
    L = [{"cmd": cmd, "em": 0.05}]
    for i, (txt, cor) in enumerate(saida):
        L.append({"out": txt, "cor": cor, "em": [0.3, 0.5, 0.6, 0.68][min(i, 3)]})
    return L


def term(linhas, legenda, destaque=(), em=1.0):
    return {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": "C:\\Users\\voce\\Documents\\meu-primeiro-playwright",
            "linhas": [dict(l, ja=True) for l in linhas], "legenda": legenda, "destaque": list(destaque), "destaque_em": em, "fonte": 32, "fonte_min": 26}


VERM = "#ff6b6b"
# saída real (demos/aula26_erro.demo.spec.js), com o caminho do arquivo do aluno
E1 = [{"out": "1) [chromium] › tests/login.spec.js:8:7 › Login › entra com usuário e senha", "cor": "txt"},
      {"out": "  Error: expect(locator).toContainText(expected) failed", "cor": VERM},
      {"out": "  Locator: getByText('Sauce Labs Backpack')", "cor": "txt"},
      {"out": "  Expected substring: \"Mochila\"", "cor": "ac"},
      {"out": "  Received string:    \"Sauce Labs Backpack\"", "cor": VERM},
      {"out": "  Timeout: 5000ms", "cor": "mut"}]
E2 = [{"out": "  13 |   await expect(page.getByText('Products')).toBeVisible();", "cor": "mut"},
      {"out": "> 14 |   await expect(page.getByText('Sauce Labs Backpack')).toContainText('Mochila');", "cor": "txt"},
      {"out": "     |                                                       ^", "cor": VERM},
      {"out": "  at tests/login.spec.js:14:57", "cor": "mut"}]
E3 = [{"out": "Call log:", "cor": "txt"},
      {"out": "  - Expect \"toContainText\" getByText('Sauce Labs Backpack') with timeout 5000ms", "cor": "mut"},
      {"out": "  - waiting for getByText('Sauce Labs Backpack')", "cor": "mut"},
      {"out": "    14 × locator resolved to <div …>Sauce Labs Backpack</div>", "cor": "mut"},
      {"out": "       - unexpected value \"Sauce Labs Backpack\"", "cor": VERM}]
assert max(len(l["out"]) for l in E1 + E2 + E3) <= 92


def erro_todo(legenda, destaque=()):
    """o erro inteiro, como sai no terminal do VS Code logo embaixo do comando (sempre a mesma tela, destacando uma parte)"""
    linhas = [{"cmd": CMD, "ja": True}, {"out": "Running 2 tests using 2 workers", "cor": "mut", "ja": True}] + [dict(l, ja=True) for l in E1 + E2 + E3]
    return {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": "C:\\Users\\voce\\Documents\\meu-primeiro-playwright", "linhas": linhas, "legenda": legenda,
            "destaque": list(destaque), "destaque_em": 0.6, "fonte": 22, "fonte_min": 18, "compacto": True}

TESTES = [["login.spec.js", ["entra com usuário e senha", "mostra erro para usuário bloqueado"]]]
A_LOGIN = [["Before Hooks", "", "520ms"], ["Navigate to", "\"/\"", "410ms"], ["Fill", "getByTestId('username')", "38ms"], ["Fill", "getByTestId('password')", "21ms"],
           ["Click", "getByTestId('login-button')", "96ms"], ["Expect", "toHaveURL", "12ms"], ["Expect", "toBeVisible", "9ms"], ["Expect", "toContainText", "8ms"], ["Expect", "toHaveCount", "7ms"]]
UI = {"type": "pw_ui", "media": "site_sauce_ui_logado", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "arquivos": TESTES, "passos_pw": A_LOGIN}
FALHA = [["entra com usuário e senha", "login.spec.js:8", "chromium", "falhou", "6.1s"], ["mostra erro para usuário bloqueado", "login.spec.js:18", "chromium", "ok", "0.6s"]]
TRACE6 = [[t, a, b, "ok", d] for b, ds in (("chromium", ("1.1s", "0.7s")), ("firefox", ("1.6s", "0.9s")), ("webkit", ("1.4s", "0.8s")))
          for (t, a), d in zip((("entra com usuário e senha", "login.spec.js:8"), ("mostra erro para usuário bloqueado", "login.spec.js:18")), ds)]  # o --trace on rodou os 6 (3 navegadores)
P_REL = [["Before Hooks", "0.5s"], ["Navigate to \"/\"", "0.4s"], ["Fill getByTestId('username')", "38ms"], ["Fill getByTestId('password')", "21ms"], ["Click getByTestId('login-button')", "96ms"]]

AULAS = []

# ---------- Aula 26 ----------
AULAS.append(projeto(26, "MÓDULO 6 · AULA 26", "Lendo o erro", [
    ("O teste falhou. Calma: ler o erro fica muito mais fácil quando você sabe onde olhar.", titulo(26, "LENDO O ERRO")),
    ("Vamos quebrar de propósito: na conferência da mochila, troca Backpack por Mochila.",
     edc(C26, "Backpack → Mochila (de propósito)", pastas=ARV_EX, digitar=True, digitar_de=L_MOCHILA, digitar_ate=L_MOCHILA, fonte=22, rolar_depois=True)),
    ("Roda. Falhou.", vs(C26, "Falhou", run(("Running 2 tests using 2 workers", "mut"), ("  1 failed", VERM), ("  1 passed (6.2s)", "ac")), pastas=ARV_EX)),
    ("O erro aparece aqui mesmo, no terminal do VS Code, logo embaixo do comando. E ele vem sempre na mesma ordem. Vamos ler de cima pra baixo.", erro_todo("O erro inteiro, embaixo do comando")),
    ("Primeiro, a linha que começa com o número um: qual teste falhou, em qual arquivo e em qual linha. Aqui: login ponto spec ponto js, linha oito, o teste entra com usuário e senha.",
     erro_todo("Qual teste · qual arquivo · qual linha", [2])),
    ("Logo embaixo: Expected, o que o teste esperava, e Received, o que ele encontrou na tela. Esperava Mochila, encontrou Sauce Labs Backpack.",
     erro_todo("Expected = esperado · Received = encontrado", [5, 6])),
    ("Mais pra baixo, o pedaço do seu código: o sinal de maior aponta a linha catorze, e a setinha embaixo mostra o ponto exato.", erro_todo("> aponta a linha 14", [9, 10])),
    ("Volta no VS Code, na linha catorze: é exatamente a conferência da mochila que a gente quebrou.",
     edc(C26, "Linha 14: a conferência quebrada", pastas=ARV_EX, fonte=22, destaque=[L_MOCHILA], destaque_em=0.5, rolar=True, rolar_de=0.3, rolar_dur=0.8)),
    ("E por último, o call log: tudo o que ele tentou. Ele achou o elemento, mas o texto não batia, e ficou tentando por cinco segundos antes de desistir.", erro_todo("Call log: tudo o que ele tentou", [12, 15, 16])),
    ("E aqui vem a pergunta mais importante de quem testa: o erro é do teste, ou é um bug no site? Aqui, fomos nós que escrevemos Mochila: o erro é do teste. Mas se o site mostrasse o nome errado, esse mesmo erro seria um bug de verdade, e virava um card pra quem desenvolve corrigir.", {'type': 'compare', 'title': 'QUEM ESTÁ ERRADO?', 'items': [['O TESTE', 'VOCÊ CONSERTA O CÓDIGO', 'white'], ['O SITE', 'VIRA UM CARD DE BUG', 'gold']], 'size': 90, 'stagger': 1.8, 'vs': False}),  # pra que / quando
    ("Três coisas que você vai ver bastante: timeout, alguma coisa que o teste esperava não aconteceu dentro do tempo. Strict mode violation, o seletor achou mais de um elemento quando precisava de um só. E Expected e Received, o teste esperava um valor e encontrou outro.",
     {"type": "cards", "itens": [["⏱", "Timeout", "o esperado não aconteceu a tempo"], ["⚠", "Strict mode", "achou mais de um", "#ffd23f"], ["≠", "Expected × Received", "esperava um, encontrou outro", "#ff6b6b"]]}),
    ("Então, no dia a dia, a ordem é: qual teste e qual linha. Depois, o esperado e o encontrado. E se ainda não ficou claro, as próximas aulas te dão ferramentas pra ver o teste acontecendo.", {'type': 'traducao', 'titulo': 'A ORDEM PRA LER', 'linhas': [['1. qual teste e qual linha', 'onde'], ['2. Expected × Received', 'o quê'], ['3. ainda não entendeu?', 'UI Mode e trace']]}),  # pra que / quando
    ("Pra consertar: na linha catorze, volta o Mochila pra Backpack.",
     edc(C24, "Mochila → Backpack de volta", pastas=ARV_EX, digitar=True, digitar_de=L_MOCHILA, digitar_ate=L_MOCHILA, fonte=22, rolar=True, rolar_de=0.3, rolar_dur=0.8)),
    ("Roda de novo: passou.", vs(C24, "Passou", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.1s)", "ac")), pastas=ARV_EX)),
    ("Na próxima aula: um jeito muito mais visual de rodar os testes.", proxima("UI Mode")[0]),
    ("Te vejo lá!", proxima("UI Mode")[1]),
]))

# ---------- Aula 27 ----------
AULAS.append(projeto(27, "MÓDULO 6 · AULA 27", "UI Mode", [
    ("Existe um jeito bem mais visual de rodar testes: o UI Mode.", titulo(27, "UI MODE")),
    ("Pra que serve? No terminal, você só vê o resultado: passou ou falhou. No UI Mode, você vê o teste acontecendo, passo a passo, e descobre onde e por que ele quebrou.",
     {"type": "compare", "title": "PRA QUE SERVE", "items": [["TERMINAL", "SÓ O RESULTADO", "white"], ["UI MODE", "CADA PASSO, COM A TELA", "gold"]], "size": 100, "stagger": 1.6, "vs": False}),
    ("No terminal: npx playwright test traço traço ui.", vs(C24, "--ui", run(cmd="npx playwright test --ui"), pastas=ARV_EX, colinha=True, colinha_em=1.2)),
    ("Abre uma janela com todos os seus testes do lado esquerdo. Clica no play.", dict(UI, legenda="Clica no play")),
    ("Ele roda e mostra cada passo. Clica num passo, e a tela mostra como a página estava naquele momento.", dict(UI, pronto=True, legenda="Cada passo, com a página daquele momento")),
    ("Dá pra voltar no tempo: ver a página antes e depois de cada clique.",
     dict(UI, pronto=True, media="site_sauce_ui_preenchido", acoes=LOGIN[:2], inspecionar="#login-button", aba_snapshot=1, depois={"em": 3.2, "media": "site_sauce_ui_logado"},
          legenda="Before e After: antes e depois do clique")),
    ("Isso serve pra achar problema: se um clique não fez o que devia, você compara a tela antes e depois e enxerga na hora o que aconteceu.",
     {"type": "cards", "itens": [["⏮", "Before", "a tela antes do clique"], ["⏭", "After", "a tela depois", "#69a7ff"], ["🔍", "Comparou", "achou o problema", "#ffd23f"]]}),
    ("E o watch. Pra que serve? Quando você está escrevendo um teste, você muda uma linha e quer ver se funcionou. Sem o watch, toda vez você volta no terminal e roda tudo de novo.",
     {"type": "cards", "titulo": "SEM O WATCH", "itens": [["✎", "Muda uma linha", ""], ["⌨", "Volta no terminal", "", "#ff8c42"], ["▶", "Roda de novo", "toda vez", "#ff6b6b"]]}),
    ("Watch quer dizer vigiar. Liga aquele ícone de olho, e pronto: salvou o arquivo, o teste roda de novo sozinho.", dict(UI, watch=True, watch_em=1.2, roda_em=2.6, legenda="watch = vigiar: salvou, rodou de novo")),
    ("É um dos jeitos mais confortáveis de escrever um teste novo: escreve, salva, e vê na hora.", bt(("ESCREVE, SALVA", "white", 120), ("E VÊ NA HORA", "gold", 150), entre=1.35)),
    ("Só que o UI Mode precisa de você na frente da tela. E quando o teste falha no GitHub, de madrugada? É a próxima aula.", {'type': 'bigtext', 'lines': [{'t': 'E QUANDO FALHA NO GITHUB?', 'c': 'white', 's': 100}, {'t': 'PRÓXIMA AULA: TRACE', 'c': 'gold', 's': 120}], 'stagger': 0.6}),  # pra que / quando
    ("Na próxima aula: o rastro completo de um teste.", proxima("Trace Viewer")[0]),
    ("Te vejo lá!", proxima("Trace Viewer")[1]),
]))

# ---------- Aula 28 ----------
CFG_RETRY = CONFIG[20:34]  # linhas 21 a 34: retries ... trace
assert "retries" in CFG_RETRY[1] and "trace" in CFG_RETRY[12]
A_FALHA = A_LOGIN[:7] + [["Expect", "toContainText('Mochila')", "5.0s"]]
ERRO_TRACE = "Error: expect(locator).toContainText(expected) failed\nLocator: getByText('Sauce Labs Backpack')\nExpected substring: \"Mochila\"\nReceived string:    \"Sauce Labs Backpack\""
AULAS.append(projeto(28, "MÓDULO 6 · AULA 28", "Trace Viewer", [
    ("E quando o teste falha no GitHub, onde você não estava olhando? Pra isso existe o trace.", titulo(28, "TRACE VIEWER")),
    ("O UI Mode da aula passada é pra quando você está na sua máquina, escrevendo o teste. O trace é pra investigar depois: um teste que falhou de madrugada, num computador que você nem viu.",
     {"type": "compare", "title": "QUAL USAR", "items": [["UI MODE", "NA SUA MÁQUINA, ESCREVENDO", "white"], ["TRACE", "DEPOIS, ONDE QUER QUE TENHA RODADO", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),
    ("Trace quer dizer rastro. Pensa na caixa-preta de um avião: ela grava tudo, pra depois alguém entender o que aconteceu.",
     {"type": "cards", "itens": [["✈", "Caixa-preta", "grava tudo do voo"], ["🎞", "Trace", "grava cada passo do teste", "#69a7ff"], ["🔍", "Depois", "você entende o que aconteceu", "#ffd23f"]]}),
    ("Pra gravar o rastro, roda com traço traço trace on.", vs(C24, "--trace on", run(("Running 6 tests using 4 workers", "mut"), ("  6 passed (5.1s)", "ac"), cmd="npx playwright test --trace on"), pastas=ARV_EX)),
    ("Quando termina, abre o relatório e clica num teste. Lá embaixo, em Traces, está o arquivo do rastro. Clica nele.",
     {"type": "pw_relatorio", "url": SAUCE, "media": "site_sauce_trace", "acoes": LOGIN, "testes": TRACE6,
      "abrir": {"titulo": "entra com usuário e senha", "arquivo": "login.spec.js:8", "projeto": "chromium", "passos": P_REL[:3], "anexos": [["Traces", "site_sauce_trace", False]], "anexos_em": 1.4},
      "legenda": "Traces: clica no rastro"}),
    ("Abre o Trace Viewer. Na esquerda, a lista de tudo o que o teste fez, na ordem: abriu o site, preencheu, clicou e conferiu.",
     {"type": "pw_trace", "media": "site_sauce_trace", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "passos_pw": A_LOGIN, "sel": 0, "legenda": "Actions: tudo o que o teste fez"}),
    ("Clica em qualquer passo, e o meio mostra a página exatamente naquele momento. Aqui, a conferência do título Products.",
     {"type": "pw_trace", "media": "site_sauce_trace", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "passos_pw": A_LOGIN, "sel": 6, "sel_em": 0.6, "legenda": "Clicou no passo: a página daquele momento"}),
    ("Embaixo, os detalhes do passo escolhido: o que ele fez, em qual elemento, e quanto tempo levou.",
     {"type": "pw_trace", "media": "site_sauce_trace", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "passos_pw": A_LOGIN, "sel": 6, "sel_em": 0, "aba": "Call", "legenda": "Call: o que fez, onde e quanto tempo"}),
    ("E quando o teste falha, é aqui que o trace brilha. O passo que falhou aparece em vermelho, e a aba Errors mostra o erro: esperava Mochila, encontrou Sauce Labs Backpack.",
     {"type": "pw_trace", "media": "site_sauce_trace", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "passos_pw": A_FALHA, "falhou": True, "erro": ERRO_TRACE, "aba": "Errors", "sel_em": 0.6, "legenda": "Errors: o passo vermelho e o erro"}),
    ("E a aba Source mostra a linha do seu código que falhou.",
     {"type": "pw_trace", "media": "site_sauce_trace", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "passos_pw": A_FALHA, "falhou": True, "aba": "Source", "codigo": C26, "linha": L_MOCHILA, "sel_em": 0, "legenda": "Source: a linha do código"}),
    ("E ainda tem as abas Console e Network: as mensagens da página e tudo o que ela pediu pro servidor. Num sistema de verdade, isso ajuda a saber se o problema está na tela ou no servidor.",
     {"type": "cards", "itens": [["▤", "Console", "as mensagens da página"], ["⇄", "Network", "o que ela pediu pro servidor", "#69a7ff"], ["?", "Tela ou servidor?", "dá pra descobrir", "#ffd23f"]]}),
    ("No config já vem trace on first retry: quando um teste falha e roda de novo, o trace dessa segunda tentativa é gravado. No GitHub o config já tenta de novo, então lá isso acontece sozinho. Na sua máquina, sem nova tentativa, use o traço traço trace on.",
     edc("\n".join(CFG_RETRY), "trace: 'on-first-retry'", arquivo="playwright.config.js", linha0=21, destaque=[2, 13], destaque_em=1.0, fonte=24)),
    ("E pra abrir um trace que alguém te mandou, ou que você baixou do GitHub: npx playwright show trace, e o nome do arquivo ponto zip.",
     {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": "C:\\Users\\voce\\Documents\\meu-primeiro-playwright", "linhas": [{"cmd": "npx playwright show-trace trace.zip"}], "legenda": "show-trace = abra este rastro", "fonte": 32}),
    ("Na próxima aula: pausando o teste no meio.", proxima("debug e page.pause")[0]),
    ("Te vejo lá!", proxima("debug e page.pause")[1]),
]))

# ---------- Aula 29 ----------
L24 = C24.split("\n")
L_CLICK = [i + 1 for i, l in enumerate(L24) if "login-button" in l][0]  # linha 11
C29 = "\n".join(L24[:L_CLICK] + ["    await page.pause();"] + L24[L_CLICK:])
TOPO29 = "\n".join(C29.split("\n")[:17])
AULAS.append(projeto(29, "MÓDULO 6 · AULA 29", "Modo debug e page.pause", [
    ("O teste falhou e o erro não deixa claro por quê? Às vezes você precisa ver acontecendo, passo a passo.", titulo(29, "DEBUG")),
    ("No modo normal, o teste inteiro passa em menos de um segundo. Se ele clicou rápido demais, ou a página ainda estava carregando, você não consegue ver.",
     {"type": "cards", "titulo": "O QUE VOCÊ NÃO CONSEGUE VER", "itens": [["⚡", "Clicou rápido demais", "antes da tela ficar pronta", "#ff8c42"], ["⏳", "Ainda carregando", "a página não terminou"], ["🎯", "Campo errado", "o seletor pegou outro", "#69a7ff"]]}),
    ("O trace da aula passada é a gravação: você assiste depois. O debug é ao vivo: o teste espera você, e só anda quando você manda.",
     {"type": "compare", "title": "TRACE × DEBUG", "items": [["TRACE", "GRAVAÇÃO: VOCÊ VÊ DEPOIS", "white"], ["DEBUG", "AO VIVO: ANDA QUANDO VOCÊ MANDA", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),
    ("Pra ligar, no terminal: npx playwright test traço traço debug.", vs(C24, "--debug", run(cmd="npx playwright test --debug"), pastas=ARV_EX, colinha=True, colinha_em=1.2)),
    ("Ele abre o navegador e uma janela chamada Inspector, e para antes do primeiro passo. Nada acontece até você mandar.", cg("Parado antes do primeiro passo", modo="debug", codigo="\n".join(L24[:16]), linhas_passo=[5])),
    ("No Inspector, o botão step over executa um passo por vez. Olha: preenche, para. Preenche, para. Clica, para.",
     cg("Step over: um passo de cada vez", modo="debug", codigo="\n".join(L24[:16]), linhas_passo=[9, 10, 11])),
    ("E enquanto está parado, a página está viva: dá pra olhar como ela está naquele momento, testar um seletor no pick locator, e quando quiser, o resume continua até o fim.",
     {"type": "cards", "titulo": "PARADO, VOCÊ PODE", "itens": [["👀", "Olhar a página", "do jeito que está agora"], ["🎯", "Pick locator", "testar um seletor ali mesmo", "#69a7ff"], ["▶", "Resume", "continuar até o fim", "#ffd23f"]]}),
    ("Só que o traço traço debug para logo no começo. Se o problema está no meio de um teste comprido, você ia apertar step over um monte de vezes. Pra isso existe o page ponto pause.",
     {"type": "cards", "itens": [["⏮", "--debug", "para no começo de tudo"], ["⏸", "page.pause()", "para onde você colocar", "#ffd23f"]]}),
    ("Você coloca page ponto pause bem antes do passo suspeito. Aqui, logo depois do clique no login.",
     edc(C29, "page.pause() antes do passo suspeito", pastas=ARV_EX, digitar=True, digitar_de=L_CLICK + 1, digitar_ate=L_CLICK + 1, fonte=22, rolar_depois=True)),
    ("Roda com o navegador aparecendo, traço traço headed. O teste corre normal até ali, para exatamente nessa linha e abre o Inspector.",
     cg("Parou no page.pause()", modo="debug", codigo=TOPO29, linhas_passo=[L_CLICK + 1], media="site_sauce_pause", acoes=LOGIN, inspecionar_varios=[])),
    ("Quando usar cada um? Escrevendo um teste novo, ou falhou na sua máquina e você não entende: debug ou pause. Falhou no GitHub, onde você não está: trace.",
     {"type": "traducao", "titulo": "QUANDO USAR", "linhas": [["teste novo, na sua máquina", "--debug ou page.pause()"], ["falhou e você não entende", "page.pause() antes do passo"], ["falhou no GitHub", "trace (aula passada)"]]}),
    ("E lembra de tirar o pause depois. Se ele subir pro GitHub, o teste fica parado esperando alguém que nunca vai apertar o botão, até estourar o tempo.",
     {"type": "cards", "itens": [["⏸", "page.pause()", "só enquanto você investiga"], ["✗", "Tira antes do commit", "senão trava no GitHub", "#ff6b6b"]]}),
    ("Na próxima aula: print e vídeo automático quando o teste falha.", proxima("print e vídeo")[0]),
    ("Te vejo lá!", proxima("print e vídeo")[1]),
]))

# ---------- Aula 30 ----------
CFG30 = CONFIG[25:34]  # linhas 26 a 34, já com baseURL e testIdAttribute (aula 23)
CFG30 = [l if "// baseURL" not in l else "    baseURL: 'https://www.saucedemo.com',\n    testIdAttribute: 'data-test'," for l in CFG30]
CFG30 = "\n".join(CFG30).split("\n")
i_trace = [i for i, l in enumerate(CFG30) if "trace:" in l][0]
CFG30 = CFG30[:i_trace + 1] + ["    screenshot: 'only-on-failure',", "    video: 'retain-on-failure',"] + CFG30[i_trace + 1:]
CARD_BUG = "repo:curso-playwright/material/cenas/card_bug.html"
AULAS.append(projeto(30, "MÓDULO 6 · AULA 30", "Print e vídeo quando o teste falha", [
    ("Quando um teste falha, alguém precisa corrigir. E só dizer que o teste falhou não ajuda: a pessoa precisa ver o que aconteceu.", titulo(30, "PRINT E VÍDEO")),
    ("E se o próprio teste tirasse um print e gravasse um vídeo quando falha? Ele faz isso. No config, dentro do use, adiciona duas linhas: screenshot only on failure, e video retain on failure.",
     edc("\n".join(CFG30), "screenshot e video", arquivo="playwright.config.js", linha0=26, digitar=True, digitar_de=i_trace + 2, digitar_ate=i_trace + 3, fonte=26)),
    ("Traduzindo: screenshot, print, só quando falhar. Video retain on failure: o vídeo é gravado durante o teste, e guardado só se ele falhar.",
     {"type": "traducao", "titulo": "SÓ QUANDO FALHA", "linhas": [["screenshot: 'only-on-failure'", "print, só quando falhar"], ["video: 'retain-on-failure'", "grava, e guarda só se falhar"]]}),
    ("Pra ver funcionando, quebra o teste de novo e roda.", vs(C26, "Falhou de novo (de propósito)", run(("Running 2 tests using 2 workers", "mut"), ("  1 failed", VERM), ("  1 passed (6.4s)", "ac")), pastas=ARV_EX)),
    ("Abre o relatório: lá está o print do momento do erro e o vídeo do teste inteiro.",
     {"type": "pw_relatorio", "url": SAUCE, "media": "site_sauce_falha", "acoes": LOGIN, "testes": TRACE6,
      "abrir": {"titulo": "entra com usuário e senha", "status": "falhou", "arquivo": "login.spec.js:8", "projeto": "chromium", "passos": [],
                "erro": "Error: expect(locator).toContainText(expected) failed\nExpected substring: \"Mochila\"\nReceived string:    \"Sauce Labs Backpack\"", "anexos": True, "anexo_img": "site_sauce_falha", "anexos_em": 1.2},
      "navegador": {"media": "rec_falha", "url": SAUCE, "gravar": True, "acoes": LOGIN, "espera_inicio": 800, "espera_fim": 1500, "titulo": "video.webm", "em": 0.45, "ate": 0.95},
      "legenda": "O print e o vídeo do teste"}),
    ("E no trabalho, pra que serve isso? Esse print e esse vídeo são as suas evidências.", bt(("PRINT + VÍDEO", "white", 120), ("= EVIDÊNCIA", "gold", 150))),
    ("Quando você abre o card do bug, anexa o print, o vídeo e o trace. Quem vai corrigir vê exatamente o que aconteceu, sem precisar te perguntar nada.",
     {"type": "tela", "media": "card_bug", "url": CARD_BUG, "alvo": "Anexos (evidências)", "titulo": "Card do bug", "legenda": "Anexa print, vídeo e trace no card"}),
    ("E dá pra gravar sempre, até quando passa? Dá: é só trocar pra on. Serve quando você precisa provar que funcionou, por exemplo, pra mostrar que um teste passou antes de fechar uma tarefa.",
     {"type": "traducao", "titulo": "AS OPÇÕES", "linhas": [["'off'", "nunca"], ["'only-on-failure' / 'retain-on-failure'", "só quando falha"], ["'on'", "sempre, até quando passa"]]}),
    ("Mas gravar sempre deixa tudo mais lento e enche o computador de arquivo. Por isso o padrão bom é só quando falha, e você liga o on só quando precisa de evidência de tudo.",
     {"type": "cards", "itens": [["✓", "Dia a dia", "só quando falha"], ["🎥", "Precisa provar", "liga o on", "#ffd23f"], ["🐢", "Sempre ligado", "mais lento, muito arquivo", "#ff8c42"]]}),
    ("Desfaz o erro e fechamos o módulo de debug.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Testes reais"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 7 · TESTES REAIS"}),
]))

def main():
    out = ["# Roteiros aprovados · Módulo 6 (gerado do roteiro_playwright_m6.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo6.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

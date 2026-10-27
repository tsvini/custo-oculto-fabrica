"""Gera projetos/curso-playwright-01..07 (boas-vindas + módulo 1) a partir dos roteiros aprovados
em curso-playwright/roteiros/boas-vindas-modulo1.md.  Uso: python ferramentas/roteiro_playwright_m1.py"""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAUCE = "https://www.saucedemo.com/"
A_COMPRA = [["Navigate to", "/inventory.html"], ["Click", "getByTestId('add-to-cart-sauce-labs-backpack')"], ["Click", "getByTestId('shopping-cart-link')"],
            ["Click", "getByTestId('checkout')"], ["Fill", "getByTestId('firstName')"], ["Fill", "getByTestId('postalCode')"], ["Click", "getByTestId('finish')"],
            ["Expect", "toHaveText('Thank you for your order!')"]]


def bt(*linhas, entre=None):
    d = {"type": "bigtext", "stagger": 0.25, "lines": [list(l) for l in linhas]}
    if entre:
        d["entre"] = entre  # mais espaço entre as linhas (acento não encosta na linha de cima)
    return d


def titulo(n, nome):
    return bt(("AULA " + str(n), "muted", 80), (nome, "gold", 200 if len(nome) <= 10 else 150))


def proxima(nome):
    return [{"type": "passo", "icone": "▶", "titulo": "Próxima aula", "sub": nome}, {"type": "endcard", "sub": "PRÓXIMA: " + nome.upper()}]


def projeto(n, selo, titulo_aula, frases):
    slug = f"curso-playwright-{n:02d}"
    return slug, {
        "title": f"Playwright para leigos · Aula {n}", "slug": slug, "idioma": "pt", "destino": "curso",
        "marca": ["PLAYWRIGHT", "PARA LEIGOS"], "cor_fundo": "#3fd68a", "sem_legenda": True, "legenda_y": 0.93, "selo": selo,
        "voz": {"nome": "gravada", "motor": "eleven", "eleven_voz": "Vinícius Torales"}, "serie": [],
        # como a voz fala (a legenda e a tela continuam com a grafia certa)
        "pronuncia": [[r"\b[Ss]aucedemo\b", "Sauce Demo"], [r"\bNode\.js\b", "Node jota éssi"], [r"\bjs\b", "jota éssi"],
                      [r"\b[Ll]oginPage\b", "Lóguin Pêidji"], [r"\b[Pp]rodutosPage\b", "Produtos Pêidji"], [r"\b[Cc]heckoutPage\b", "Tchécaut Pêidji"], [r"\bpages\b", "pêidjis"]],
        "meta": {"titles": [f"Aula {n}: {titulo_aula}"], "description": "", "tags": []},
        "notes": "Curso Playwright para leigos. Não publica (destino: curso). Roteiro em curso-playwright/roteiros/.",
        "script": {"long": {"parts": [{"chapter": "", "sentences": [{"text": t, "scene": s} for t, s in com_criacao(frases)]}]}, "shorts": [], "tiktoks": []},
    }


MENU_VSC = [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]]


def apagar_no_explorer(pastas, nome):
    """cena do VS Code: botão direito no arquivo › Delete › ele some do Explorer (pastas = a árvore ainda com ele)"""
    return {"type": "menu", "app": "vscode", "barra": [], "menus": [MENU_VSC[0] + ["Delete"]], "caminho": [len(MENU_VSC[0])], "pastas": pastas,
            "apaga": nome, "legenda": "Botão direito › Delete"}


def criar_no_explorer(final, nome, pasta=False):
    """cena do VS Code: botão direito na pasta de cima › New File/New Folder › o nome aparece no Explorer (final = a árvore já com o item)"""
    idx = [i for i, l in enumerate(final) if l.strip().rstrip("/") == nome.rstrip("/")][0]
    nivel = (len(final[idx]) - len(final[idx].lstrip())) // 2
    pai = next(final[j].strip().rstrip("/") for j in range(idx - 1, -1, -1) if (len(final[j]) - len(final[j].lstrip())) // 2 < nivel)
    antes = [l for i, l in enumerate(final) if i != idx and not (pasta and i > idx and (len(l) - len(l.lstrip())) // 2 > nivel and all((len(final[k]) - len(final[k].lstrip())) // 2 > nivel for k in range(idx + 1, i + 1)))]
    return {"type": "menu", "app": "vscode", "barra": [], "menus": MENU_VSC, "caminho": [1 if pasta else 0], "pastas": antes, "alvo_item": pai,
            "novo_pos": idx, "resultado": "arquivo", "novo": nome.rstrip("/"), "novo_nivel": nivel, "novo_pasta": pasta,
            "legenda": ("New Folder › " if pasta else "New File › ") + nome.rstrip("/") + ("" if nivel <= 1 else "  (dentro de " + pai + ")")}


def com_criacao(frases):
    """cena com "criar": [[fala, nome], ...] ganha antes uma cena de criação no Explorer pra cada item (pasta termina em /)"""
    out = []
    for t, s in frases:
        cr = s.pop("criar", None) if isinstance(s, dict) else None
        if cr:
            final = s.pop("criar_arvore", None) or s["pastas"]
            for k, (fala, nome) in enumerate(cr):
                pasta = nome.endswith("/")
                # pasta criada antes do arquivo de dentro: o arquivo ainda não existe nessa cena
                arv = [l for l in final if not any(l.strip() == n2.rstrip("/") or l.strip() == n2 for _, n2 in cr[k + 1:])]
                out.append((fala, criar_no_explorer(arv, nome, pasta)))
        out.append((t, s))
    return out


def term(linhas, legenda=None, pasta="C:\\Users\\voce", titulo=None):
    d = {"type": "terminal", "pasta": pasta, "linhas": linhas, "titulo": "Windows PowerShell"}
    if legenda:
        d["legenda"] = legenda
    if titulo:
        d["titulo"] = titulo
    return d



# aula 1: o projeto final rodando de verdade: VS Code com o teste de compra, o comando no terminal e o navegador real por cima fazendo tudo
_COMPRA_JS = open(os.path.join(RAIZ, "curso-playwright", "projeto", "tests", "compra.spec.js"), encoding="utf8").read().rstrip("\n").split("\n")
_LOGIN = [{"fill": ["#user-name", "standard_user"]}, {"fill": ["#password", "secret_sauce"]}, {"click": "#login-button"}]
_COMPRA = _LOGIN + [{"click": "[data-test=\"add-to-cart-sauce-labs-backpack\"]"}, {"click": "[data-test=\"shopping-cart-link\"]"}, {"click": "[data-test=\"checkout\"]"},
                    {"fill": ["[data-test=\"firstName\"]", "Maria"]}, {"fill": ["[data-test=\"lastName\"]", "Silva"]}, {"fill": ["[data-test=\"postalCode\"]", "88000-000"]},
                    {"click": "[data-test=\"continue\"]"}, {"click": "[data-test=\"finish\"]"}]
VS_COMPRA = {"type": "editor", "arquivo": "compra.spec.js", "digitar": False, "fonte": 28, "linha0": 7, "codigo": "\n".join(_COMPRA_JS[6:15]),
             "terminal": [{"cmd": "npx playwright test compra.spec.js --headed --project=chromium", "em": 0.02}, {"out": "Running 1 test using 1 worker", "cor": "mut", "em": 0.07},
                          {"out": "  1 passed (6.2s)", "cor": "ac", "em": 0.87}],
             "navegador": {"media": "rec_compra_final", "url": SAUCE, "gravar": True, "acoes": _COMPRA, "espera_inicio": 700, "espera_fim": 2000, "delay_letra": 45,
                           "titulo": "Chromium", "em": 0.09, "ate": 0.85},
             "legenda": "O robô compra sozinho"}

AULAS = []

# ---------- Aula 1 ----------
AULAS.append(projeto(1, "BOAS-VINDAS · AULA 1", "O que você vai construir", [
    ("Seja muito bem-vindo ao Playwright para Leigos. Eu sou o Vinícius.", bt(("PLAYWRIGHT", "gold", 210), ("PARA LEIGOS", "white", 130), ("AULA 1", "muted", 80))),
    ("Antes de qualquer explicação, eu quero te mostrar onde você vai chegar.", bt(("ONDE VOCÊ", "white", 150), ("VAI CHEGAR", "gold", 170))),
    ("Isso aqui é o projeto final do curso: um robô que entra numa loja de verdade, faz login, coloca produto no carrinho e finaliza a compra, sozinho.",
     VS_COMPRA),
    ("E o mesmo teste roda no Chromium, no Firefox, no WebKit, que é o motor por trás do Safari, e até simulando um celular.",
     {"type": "pw_relatorio", "testes": [["compra uma mochila do começo ao fim", "compra.spec.js:7", p, "ok", d] for p, d in (("chromium", "2.1s"), ("firefox", "2.8s"), ("webkit", "2.5s"), ("celular", "2.3s"))],
      "legenda": "Um teste, quatro navegadores"}),
    ("Quando alguma coisa quebra, o Playwright mostra exatamente onde, com foto de cada passo.",
     {"type": "pw_trace", "media": "site_sauce", "url": SAUCE, "inspecionar": "[data-test=\"login-button\"]",
      "passos_pw": [["Navigate to", "/"], ["Fill", "getByTestId('username')"], ["Fill", "getByTestId('password')"], ["Click", "getByTestId('login-button')"], ["Expect", "toHaveText('Produtos')"]],
      "falhou": True, "erro": "Error: expect(locator).toHaveText(expected)\nLocator: getByTestId('title')\nExpected: \"Produtos\"\nReceived: \"Products\"", "legenda": "Ele mostra onde quebrou"}),
    ("E no final, você vai colocar tudo no GitHub, e os testes vão rodar sozinhos toda vez que você mudar o código. Esse verde aqui é o seu projeto funcionando sem você encostar em nada.",
     {"type": "gh_actions", "commit": "adiciona o teste de compra", "legenda": "Os testes rodando sozinhos"}),
    ("E o melhor: isso tudo vai pro seu portfólio. É um projeto que você pode mostrar numa entrevista.",
     {"type": "cards", "titulo": "NO FIM DO CURSO", "itens": [["1", "Projeto", "testes de verdade"], ["2", "GitHub", "rodando sozinho", "#69a7ff"], ["3", "Currículo", "pra mostrar na entrevista", "#ffd23f"]]}),
    ("E você não vai copiar um projeto pronto. A gente vai construir tudo junto, do zero.", bt(("DO ZERO", "gold", 200), ("TUDO JUNTO", "white", 130))),
    ("Se você nunca programou, relaxa. Eu vou explicar cada linha, e você vai ver cada uma sendo escrita na tela, com calma.",
     {"type": "editor", "arquivo": "login.spec.js", "pastas": ["meu-primeiro-playwright", "tests", "login.spec.js"],
      "codigo": "import { test, expect } from '@playwright/test';\n\ntest('entra com usuário e senha', async ({ page }) => {\n  await page.goto('/');\n  await page.getByTestId('username').fill('standard_user');\n  await page.getByTestId('password').fill('secret_sauce');\n  await page.getByTestId('login-button').click();\n  await expect(page.getByTestId('title')).toHaveText('Products');\n});",
      "fonte": 28, "vel": 0.8, "legenda": "Sempre o código inteiro"}),
    ("Na próxima aula, eu te mostro como aproveitar melhor o curso, e te entrego a sua colinha.", proxima("Como usar o curso e a sua colinha")[0]),
    ("Te vejo lá!", proxima("Como usar o curso e a sua colinha")[1]),
]))

# ---------- Aula 2 ----------
COLINHA = "repo:curso-playwright/material/colinha/colinha.html"
AULAS.append(projeto(2, "BOAS-VINDAS · AULA 2", "Como usar o curso e a sua colinha", [
    ("Antes de começar, três dicas rápidas pra você aproveitar o curso ao máximo.", bt(("3 DICAS", "gold", 200), ("ANTES DE COMEÇAR", "white", 110))),
    ("Primeira: você não precisa decorar nenhum comando. Nos recursos desta aula tem uma colinha em PDF, com os principais comandos do curso organizados pra você consultar enquanto pratica.",
     {"type": "tela", "media": "colinha_pw_zoom", "url": COLINHA, "titulo": "colinha-playwright-para-leigos.pdf", "alvo": "npx playwright test", "zoom_em": 3.0, "caixa_em": 3.8,
      "legenda": "A sua colinha, nos recursos da aula"}),
    ("Baixa ela agora e deixa aberta do lado. Durante o curso, quando aparecer esse selo aqui no canto, é porque aquele comando já está na sua colinha.",
     {"type": "tela", "media": "colinha_pw", "url": COLINHA, "titulo": "colinha-playwright-para-leigos.pdf", "colinha": True, "colinha_em": 2.2, "colinha_dur": 6, "legenda": "Viu esse selo? Está na colinha"}),
    ("Segunda: faz junto comigo. Pausa o vídeo, digita, roda. É fazendo que você aprende, não só assistindo.",
     {"type": "editor", "arquivo": "login.spec.js", "fonte": 30, "digitar": True, "digitar_de": 4, "digitar_ate": 4, "vel": 0.45,
      "pastas": ["meu-primeiro-playwright", "  node_modules/", "  tests/", "    login.spec.js", "  package.json", "  playwright.config.js"],
      "codigo": "import { test, expect } from '@playwright/test';\n\ntest('entra com usuário e senha', async ({ page }) => {\n  await page.goto('https://www.saucedemo.com/');\n});",
      "terminal": [{"cmd": "npx playwright test --project=chromium", "em": 0.5}, {"out": "Running 1 test using 1 worker", "cor": "mut", "em": 0.7}, {"out": "  1 passed (1.9s)", "cor": "ac", "em": 0.8}],
      "legenda": "Pausa · digita · roda"}),
    ("Terceira: se der erro, não desanima. Tem uma aula só sobre os erros mais comuns, e você pode me chamar na área de perguntas.",
     dict(term([{"cmd": "npx playwright test", "ja": True}, {"out": "npx : O termo 'npx' não é reconhecido como nome de cmdlet,", "cor": "#ff6b6b", "ja": True},
                {"out": "função, arquivo de script ou programa operável.", "cor": "#ff6b6b", "ja": True}], "Deu erro? Aula 7: os erros mais comuns · e a área de perguntas"),
          fonte=32, fonte_min=26)),
    ("Agora, uma coisa importante sobre o próximo módulo.", {"type": "flash", "text": "MÓDULO 1", "color": "gold", "size": 190}),
    ("O módulo um é só instalação: o VS Code, o Node e o Git.",
     {"type": "cards", "titulo": "MÓDULO 1 · INSTALAÇÃO", "itens": [["1", "VS Code", "onde você escreve"], ["2", "Node.js", "o motor", "#69a7ff"], ["3", "Git", "o histórico", "#ffd23f"]]}),
    ("Se você já usa VS Code, Node e Git no seu computador, pode pular o módulo um. Se não tem certeza, fica comigo, que eu vou conferir cada um junto com você.",
     {"type": "compare", "title": "E AGORA?", "items": [["JÁ TENHO OS 3", "PULA PRO MÓDULO 2", "gold"], ["NÃO SEI", "FICA COMIGO", "white"]], "size": 110, "stagger": 1.4, "vs": False}),
    ("E se o seu computador é Mac ou Linux, tem uma aula só pra você no fim do módulo um.", {"type": "passo", "icone": "6", "titulo": "Mac ou Linux?", "sub": "Aula 6"}),
    ("E um aviso: a partir do módulo doze, o nível sobe. Se você já automatiza testes e só quer ver o Playwright mais a fundo, pode pular direto pra lá.",
     {"type": "cards", "titulo": "O MAPA DO CURSO", "itens": [["1–11", "Do zero", "módulos 1 a 11"], ["12–14", "Nível 2", "o nível sobe", "#ffd23f"], ["15", "Carreira", "currículo e portfólio", "#69a7ff"]]}),
    ("Bora começar!", {"type": "endcard", "sub": "PRÓXIMA: INSTALANDO O VS CODE"}),
]))

# ---------- Aula 3 ----------
AULAS.append(projeto(3, "MÓDULO 1 · AULA 3", "Instalando o VS Code", [
    ("Primeira instalação: o VS Code, o programa onde a gente vai escrever os testes.", titulo(3, "VS CODE")),
    ("O VS Code é um editor de código. Pensa num bloco de notas turbinado, que pinta cada parte do código de uma cor e te ajuda a não errar.",
     {"type": "bloco_vs", "vs_em": 3.2, "codigo": "import { test, expect } from '@playwright/test';\n\ntest('entra no site', async ({ page }) => {\n  await page.goto('https://www.saucedemo.com/');\n  await expect(page).toHaveTitle('Swag Labs');\n});"}),
    ("É gratuito, é da Microsoft, e é um dos editores mais usados no desenvolvimento de software. Você vai encontrar ele em muitas empresas.",
     {"type": "cards", "itens": [["R$0", "Gratuito", "não paga nada"], ["MS", "Da Microsoft", "confiável", "#69a7ff"], ["★", "Muito usado", "nas empresas", "#ffd23f"]]}),
    ("Primeiro passo: abre o navegador e entra em code ponto visualstudio ponto com. Clica no botão Download for Windows.",
     {"type": "tela", "media": "rec_vscode_download", "url": "https://code.visualstudio.com/", "gravar": True, "acoes": [{"click": "text=Download for Windows", "espera": 3500}],
      "espera_inicio": 1800, "espera_fim": 800, "titulo": "code.visualstudio.com", "legenda": "Clique em Download for Windows"}),
    ("Segundo passo: abre o arquivo que baixou, na pasta Downloads.",
     {"type": "pastas", "caminho": "Este Computador  ›  Downloads", "itens": [{"nome": "VSCodeUserSetup.exe", "arquivo": True, "novo": True}], "novo_em": 0.6, "legenda": "O instalador fica em Downloads"}),
    ("Aceita o contrato e clica em Next.",
     {"type": "instalador", "app": "Visual Studio Code", "titulo": "License Agreement", "subtitulo": "Please read the following important information", "texto": "Leia o contrato de uso do programa.", "caixas": [["I accept the agreement", True]], "botao": "Next", "legenda": "Aceite e clique em Next"}),
    ("Nessa tela, marca o Add to PATH e as duas opções Open with Code. Isso facilita muito a vida depois.",
     {"type": "instalador", "app": "Visual Studio Code", "titulo": "Select Additional Tasks", "subtitulo": "Which additional tasks should be performed?", "caixas": [["Add \"Open with Code\" action to file context menu", True], ["Add \"Open with Code\" action to directory context menu", True], ["Add to PATH", True]], "botao": "Next", "botao_em": 3.5, "legenda": "Marque essas três opções"}),
    ("Clica em Install, espera, e no final clica em Finish.",
     {"type": "instalador", "app": "Visual Studio Code", "titulo": "Installing", "subtitulo": "Please wait while Setup installs Visual Studio Code", "progresso": True, "botao": "Finish", "legenda": "Install, espera, Finish"}),
    ("Pronto! Esse é o VS Code. Na esquerda ficam os arquivos do projeto, e no meio é onde você escreve.",
     {"type": "editor", "arquivo": "Welcome", "pastas": ["SEUS ARQUIVOS", "ficam aqui"], "codigo": "// Aqui é onde você escreve o código\n// Na próxima aula, a gente instala\n// o Node.js", "digitar": True, "legenda": "Pronto, o VS Code está instalado!"}),
    ("Na próxima aula, a gente instala o Node, que é o motor que faz o Playwright funcionar.", proxima("Instalando o Node.js")[0]),
    ("Te vejo lá!", proxima("Instalando o Node.js")[1]),
]))

# ---------- Aula 4 ----------
AULAS.append(projeto(4, "MÓDULO 1 · AULA 4", "Instalando o Node.js", [
    ("Agora é a vez do Node.js.", titulo(4, "NODE.JS")),
    ("O Playwright é escrito em JavaScript, e o Node é o programa que roda JavaScript no seu computador. Sem ele, o Playwright não liga.",
     {"type": "flow", "a": "NODE.JS", "a_sub": "roda o JavaScript", "b": "PLAYWRIGHT", "b_sub": "controla o navegador", "caption": "SEM O NODE, O PLAYWRIGHT NÃO LIGA"}),
    ("Junto com o Node vem o npm, que é tipo uma loja de aplicativos pra programador. É por ele que a gente vai instalar o Playwright.",
     {"type": "cards", "itens": [["▶", "Node.js", "roda o JavaScript"], ["⬇", "npm", "a lojinha de ferramentas", "#69a7ff"]]}),
    ("Entra em nodejs ponto org e baixa a versão que tem escrito LTS. LTS é a versão estável, a que menos dá dor de cabeça.",
     {"type": "tela", "media": "site_node", "url": "https://nodejs.org/", "alvo": "LTS", "titulo": "nodejs.org", "zoom_em": 1.8, "caixa_em": 2.6, "legenda": "Baixe sempre a versão LTS"}),
    ("Abre o instalador e vai clicando em Next. Pode deixar todas as opções como vierem.",
     {"type": "instalador", "app": "Node.js", "titulo": "End-User License Agreement", "subtitulo": "Please read the following license agreement carefully", "caixas": [["I accept the terms in the License Agreement", True]], "botao": "Next", "legenda": "Pode deixar tudo no padrão"}),
    ("Clica em Install. Se o Windows pedir permissão, clica em Sim.",
     {"type": "instalador", "app": "Node.js", "titulo": "Installing Node.js", "subtitulo": "Please wait while the Setup Wizard installs Node.js", "progresso": True, "botao": "Finish", "legenda": "Se o Windows perguntar, clique em Sim"}),
    ("Agora vamos conferir. Aperta a tecla do Windows, digita PowerShell e abre.", {"type": "iniciar", "busca": "PowerShell", "tecla_em": 1.2, "legenda": "Tecla Windows › PowerShell › abra"}),
    ("Essa é a janela do terminal. É só um lugar onde você escreve comandos em vez de clicar.",
     term([{"out": "Windows PowerShell", "cor": "txt"}, {"out": "Copyright (C) Microsoft Corporation.", "cor": "mut"}, {"cmd": ""}], "O terminal: você escreve em vez de clicar", titulo="Windows PowerShell")),
    ("Digita node traço v e aperta Enter. Depois, npm traço v e Enter.",
     term([{"cmd": "node -v"}, {"out": "v22.21.0", "cor": "ac"}, {"cmd": "npm -v"}, {"out": "10.9.4", "cor": "ac"}], "node -v  e  npm -v")),
    ("Apareceu um número em cada um? Mesmo que diferente do meu, está tudo certo.", bt(("APARECEU O NÚMERO?", "white", 120), ("ESTÁ INSTALADO", "gold", 170))),
    ("Na próxima aula, a última instalação: o Git.", proxima("Instalando o Git")[0]),
    ("Te vejo lá!", proxima("Instalando o Git")[1]),
]))

# ---------- Aula 5 ----------
AULAS.append(projeto(5, "MÓDULO 1 · AULA 5", "Instalando o Git", [
    ("Última instalação: o Git.", titulo(5, "GIT")),
    ("O Git guarda o histórico do seu projeto, como os pontos de salvamento de um videogame. Deu problema? Volta pro último ponto salvo.",
     {"type": "cards", "titulo": "O SAVE DO SEU PROJETO", "itens": [["1", "Você salva", "um ponto do projeto"], ["2", "Deu problema?", "algo quebrou", "#ff6b6b"], ["3", "Volta", "pro último save", "#ffd23f"]]}),
    ("E é com ele que, no fim do curso, o seu projeto vai pro GitHub e passa a rodar os testes sozinho.", {"type": "gh_actions", "commit": "meu projeto de testes", "pronto": True, "legenda": "Lá no fim do curso"}),
    ("Entra em git traço scm ponto com, clica em Download for Windows e baixa a versão recomendada para o seu Windows.",
     {"type": "tela", "media": "site_git", "url": "https://git-scm.com/downloads/win", "alvo": "Click here to download", "titulo": "git-scm.com", "zoom_em": 1.8, "caixa_em": 2.6, "legenda": "Baixe a versão recomendada"}),
    ("O instalador tem bastante tela, mas dá pra deixar quase tudo no padrão e ir clicando em Next.",
     {"type": "instalador", "app": "Git", "titulo": "Select Components", "subtitulo": "Which components should be installed?", "caixas": [["Windows Explorer integration", True], ["Git LFS (Large File Support)", True], ["Associate .git* configuration files", True]], "botao": "Next", "legenda": "Pode deixar no padrão"}),
    ("Só uma tela merece atenção: quando ele perguntar o editor, escolhe o Visual Studio Code.",
     {"type": "instalador", "app": "Git", "titulo": "Choosing the default editor used by Git", "subtitulo": "Which editor would you like Git to use?", "texto": "Use Visual Studio Code as Git's default editor", "botao": "Next", "legenda": "Escolha o Visual Studio Code"}),
    ("Clica em Install, espera, e Finish.",
     {"type": "instalador", "app": "Git", "titulo": "Installing", "subtitulo": "Please wait while Setup installs Git", "progresso": True, "botao": "Finish", "legenda": "Install, espera, Finish"}),
    ("Pra conferir, abre o PowerShell e digita git traço traço version.", term([{"cmd": "git --version"}, {"out": "git version 2.51.0.windows.1", "cor": "ac"}], "git --version")),
    ("Apareceu a versão? Então você tem tudo: o VS Code, o Node e o Git.",
     {"type": "cards", "titulo": "TUDO PRONTO", "itens": [["✓", "VS Code", "instalado"], ["✓", "Node.js", "instalado", "#69a7ff"], ["✓", "Git", "instalado", "#ffd23f"]]}),
    ("Se o seu computador é Windows, pode pular a próxima aula, que é de Mac e Linux, e ir direto pro módulo dois.", {"type": "passo", "icone": "▶", "titulo": "Windows?", "sub": "Pule pro módulo 2"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 2"}),
]))

# ---------- Aula 6 ----------
NVM = "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash"
AULAS.append(projeto(6, "MÓDULO 1 · AULA 6", "Instalando no Mac e no Linux", [
    ("Essa aula é pra quem usa Mac ou Linux. Se você usa Windows, pode pular.", bt(("MAC", "gold", 180), ("E LINUX", "white", 150), ("AULA 6", "muted", 80))),
    ("São os mesmos três programas: o VS Code, o Node e o Git. Só muda o jeito de instalar.",
     {"type": "cards", "itens": [["1", "VS Code", "onde você escreve"], ["2", "Node.js", "o motor", "#69a7ff"], ["3", "Git", "o histórico", "#ffd23f"]]}),
    ("No Mac, pra abrir o terminal, aperta Command e espaço, digita Terminal e aperta Enter.", {"type": "passo", "icone": "⌘", "titulo": "Command + espaço", "sub": "digite Terminal"}),
    ("O VS Code: baixa em code ponto visualstudio ponto com, abre o arquivo e arrasta pra pasta Aplicativos.",
     {"type": "pastas", "titulo": "Finder", "caminho": "Finder  ›  Aplicativos", "itens": ["Calculadora", "Safari", {"nome": "Visual Studio Code", "novo": True}], "novo_em": 0.8, "legenda": "Arraste pra Aplicativos"}),
    ("O Node: em nodejs ponto org, baixa a versão LTS pra Mac e vai clicando em continuar.",
     {"type": "tela", "media": "site_node_mac_dl", "ua": "mac", "url": "https://nodejs.org/pt/download", "alvo": "Instalador", "titulo": "nodejs.org", "zoom_em": 1.6, "caixa_em": 2.4, "legenda": "Versão LTS pra Mac"}),
    ("O Git é o mais fácil: digita git traço traço version no terminal. Se não tiver, o próprio Mac oferece instalar.",
     {"type": "terminal", "titulo": "Terminal · Mac", "prompt": "voce@Mac ~ %", "linhas": [{"cmd": "git --version"}, {"out": "git version 2.39.5 (Apple Git-154)", "cor": "ac"}], "legenda": "Não tem? O Mac oferece instalar"}),
    ("Agora o Linux. Eu vou mostrar no Ubuntu. O terminal abre com Control, Alt e T.", {"type": "passo", "icone": "⌨", "titulo": "Ctrl + Alt + T", "sub": "abre o terminal no Ubuntu"}),
    ("O VS Code se instala com sudo snap install code traço traço classic. O sudo pede a sua senha do computador, e enquanto você digita não aparece nada. É normal.",
     {"type": "terminal", "titulo": "Terminal · Ubuntu", "prompt": "voce@ubuntu:~$", "linhas": [{"cmd": "sudo snap install code --classic"}, {"out": "[sudo] password for voce:", "cor": "mut"}, {"out": "code installed", "cor": "ac"}], "legenda": "A senha não aparece. É normal"}),
    ("O Git, com sudo apt install git.", {"type": "terminal", "titulo": "Terminal · Ubuntu", "prompt": "voce@ubuntu:~$", "linhas": [{"cmd": "sudo apt install git"}, {"out": "git is already the newest version", "cor": "ac"}], "legenda": "sudo apt install git"}),
    ("O Node, no Ubuntu, a gente instala com uma ferramenta chamada nvm, porque o que vem pelo apt costuma ser antigo. São três comandos, e eles estão aqui na tela e na descrição da aula.",
     {"type": "terminal", "titulo": "Terminal · Ubuntu", "prompt": "voce@ubuntu:~$", "linhas": [{"cmd": NVM}, {"out": "=> nvm source string already in ~/.bashrc", "cor": "mut"}, {"cmd": "\\. \"$HOME/.nvm/nvm.sh\""}, {"cmd": "nvm install --lts"}, {"out": "Now using node v22.21.0 (npm v10.9.4)", "cor": "ac"}], "legenda": "Os 3 comandos estão na descrição", "colinha": False}),
    ("E tem um detalhe que é só do Linux. Quando a gente instalar o Playwright, ele vai pedir umas bibliotecas do sistema. Lá na hora, eu te mostro o comando que resolve.",
     {"type": "cards", "titulo": "SÓ NO LINUX", "itens": [["!", "Bibliotecas", "o Playwright vai pedir"], ["✓", "Na hora certa", "eu mostro o comando", "#ffd23f"]]}),
    ("Pra conferir: node traço v, npm traço v e git traço traço version.",
     {"type": "terminal", "titulo": "Terminal · Ubuntu", "prompt": "voce@ubuntu:~$", "linhas": [{"cmd": "node -v"}, {"out": "v22.21.0", "cor": "ac"}, {"cmd": "npm -v"}, {"out": "10.9.4", "cor": "ac"}, {"cmd": "git --version"}, {"out": "git version 2.43.0", "cor": "ac"}], "legenda": "Um número em cada? Tudo certo"}),
    ("Todos os comandos estão na descrição da aula. Até o módulo dois!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 2"}),
]))

# ---------- Aula 7 ----------
AULAS.append(projeto(7, "MÓDULO 1 · AULA 7", "Se der erro na instalação, consulte aqui", [
    ("Se tudo funcionou até aqui, você pode pular esta aula e seguir pro módulo dois. Volta aqui se tiver algum problema.", bt(("DEU ERRO?", "white", 150), ("CONSULTE AQUI", "gold", 160), ("TUDO CERTO? PODE PULAR", "muted", 70))),
    ("Erro um: o terminal diz que node, npm ou npx não é reconhecido. Quase sempre o terminal foi aberto antes de instalar o Node.",
     term([{"cmd": "npx playwright test"}, {"out": "npx : O termo 'npx' não é reconhecido como nome de cmdlet,", "cor": "red"}, {"out": "função, arquivo de script ou programa operável.", "cor": "red"}], "Erro 1: não é reconhecido")),
    ("A solução: fecha o terminal e o VS Code e abre de novo. Se continuar, reinicia o computador.",
     {"type": "cards", "titulo": "COMO RESOLVER", "itens": [["1", "Fecha", "terminal e VS Code"], ["2", "Abre de novo", "e tenta outra vez", "#69a7ff"], ["3", "Continuou?", "reinicia o computador", "#ffd23f"]]}),
    ("Erro dois, só no Windows: a execução de scripts foi desabilitada neste sistema. É uma trava de segurança do PowerShell.",
     term([{"cmd": "npx playwright test"}, {"out": "npx : O arquivo npx.ps1 não pode ser carregado porque", "cor": "red"}, {"out": "a execução de scripts foi desabilitada neste sistema.", "cor": "red"}], "Erro 2: scripts desabilitados")),
    ("Na maioria dos computadores, resolve rodando esse comando uma vez, que está aqui na tela. Depois fecha e abre o terminal. Se o computador for da empresa, pode ser que a TI bloqueie essa mudança, e aí vale falar com eles.",
     {"type": "terminal", "titulo": "Windows PowerShell", "prompt": "PS>", "linhas": [{"cmd": "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"}], "legenda": "Roda uma vez e reabre o terminal"}),
    ("Erro três, esse já é do Playwright: aparece executable doesn't exist, o executável não existe. Quer dizer que faltam os navegadores dele.",
     term([{"cmd": "npx playwright test"}, {"out": "Error: browserType.launch: Executable doesn't exist", "cor": "red"}, {"out": "Looks like Playwright was just installed or updated.", "cor": "yel"}], "Erro 3: faltam os navegadores")),
    ("Resolve com npx playwright install. Ele baixa o Chromium, o Firefox e o WebKit. No Linux, acrescenta traço traço with traço deps, que instala as bibliotecas do sistema junto.",
     term([{"cmd": "npx playwright install"}, {"out": "Downloading Chromium, Firefox, WebKit... done", "cor": "ac"}, {"out": "# no Linux:", "cor": "mut"}, {"cmd": "npx playwright install --with-deps"}], "npx playwright install")),
    ("Erro quatro: ele diz que não acha nenhum teste, ou nenhum arquivo de configuração. É o terminal aberto na pasta errada. Olha o caminho antes do cursor: tem que terminar com o nome da pasta do projeto.",
     term([{"cmd": "npx playwright test"}, {"out": "Error: No tests found", "cor": "red"}, {"out": "", "cor": "mut"}, {"cmd": "cd meu-primeiro-playwright"}], "O caminho tem que ser o do projeto", pasta="C:\\Users\\voce")),
    ("E a dica de ouro: copia a mensagem de erro e cola no Google. Alguém já passou por isso. Programador experiente faz isso todo dia.", bt(("DICA DE OURO", "gold", 150), ("COPIA O ERRO", "white", 120), ("E COLA NO GOOGLE", "white", 120))),
    ("Volta aqui sempre que precisar. Até a próxima!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 2"}),
]))


def main():
    for slug, p in AULAS:
        for s in p["script"]["long"]["parts"][0]["sentences"]:
            s["scene"] = {k: v for k, v in s["scene"].items() if v is not None}
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")


if __name__ == "__main__":
    main()

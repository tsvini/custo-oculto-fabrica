"""Gera projetos/curso-playwright-08..11 (módulo 2: fundamentos). Roteiro aprovado em curso-playwright/roteiros/modulo2.md."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ

REF = os.path.join(RAIZ, "curso-playwright", "referencia_init")
CONFIG = open(os.path.join(REF, "playwright.config.js"), encoding="utf8").read().rstrip("\n")
EXEMPLO = open(os.path.join(REF, "tests", "example.spec.js"), encoding="utf8").read().rstrip("\n")
PASTA = "C:\\Users\\voce\\Documents\\meu-primeiro-playwright"
PACKAGE = """{
  "name": "meu-primeiro-playwright",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {},
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@playwright/test": "^1.64.1",
    "@types/node": "^26.6.5"
  }
}"""
GITIGNORE = """
# Playwright
node_modules/
/test-results/
/playwright-report/
/blob-report/
/playwright/.cache/
/playwright/.auth/""".strip("\n")
ARVORE = ["meu-primeiro-playwright", "  .github/", "  node_modules", "  tests", "    example.spec.js", "  .gitignore", "  package-lock.json", "  package.json", "  playwright.config.js"]


def vterm(linhas, legenda, colinha=False, ja=0, pastas=None, codigo=None, arquivo="Welcome"):
    """o terminal DENTRO do VS Code (painel de baixo, maior que o normal porque o assunto é o terminal)"""
    linhas = [dict(l, ja=True) if i < ja else dict(l) for i, l in enumerate(linhas)]  # as primeiras "ja" linhas já estavam na tela
    novas = [l for l in linhas if not l.get("ja")]
    for k, l in enumerate(novas):  # o comando digita primeiro, as saídas vêm uma depois da outra
        l["em"] = 0.05 if (k == 0 and "cmd" in l) else round(0.3 + 0.45 * k / max(1, len(novas) - 1), 2)
    d = {"type": "editor", "arquivo": arquivo, "pastas": pastas or ["meu-primeiro-playwright"], "digitar": False, "fonte": 24,
         "codigo": codigo or "// A pasta do projeto está aberta!", "terminal": linhas, "terminal_altura": 0.66, "legenda": legenda}
    if colinha:
        d.update({"colinha": True, "colinha_em": 1.5})
    return d


INIT = [{"cmd": "npm init playwright@latest"}]
OK = [{"out": "Need to install the following packages:", "cor": "mut"}, {"out": "  create-playwright", "cor": "txt"}, {"out": "Ok to proceed? (y) y", "cor": "yel"}]
Q1 = [{"out": "Getting started with writing end-to-end tests with Playwright:", "cor": "mut"}, {"out": "✔ Do you want to use TypeScript or JavaScript? · JavaScript", "cor": "ac"}]
Q2 = [{"out": "✔ Where to put your end-to-end tests? · tests", "cor": "ac"}]
Q3 = [{"out": "✔ Add a GitHub Actions workflow? (y/N) · true", "cor": "ac"}]
Q4 = [{"out": "✔ Install Playwright browsers? (Y/n) · true", "cor": "ac"}, {"out": "Downloading Chromium... Firefox... WebKit... done", "cor": "txt"}]
FIM = [{"out": "✔ Success! Created a Playwright Test project", "cor": "ac"}, {"out": "Happy hacking! 🎭", "cor": "yel"}]
RUN = [{"cmd": "npx playwright test"}, {"out": "Running 6 tests using 4 workers", "cor": "mut"}, {"out": "  6 passed (7.9s)", "cor": "ac"}, {"out": "To open last HTML report run:", "cor": "mut"}, {"out": "  npx playwright show-report", "cor": "txt"}]
REL = [[n, f"example.spec.js:{l}", p, "ok", d] for n, l in (("has title", 4), ("get started link", 11)) for p, d in (("chromium", "1.2s"), ("firefox", "1.9s"), ("webkit", "1.6s"))]
REL.sort(key=lambda r: (int(r[1].split(":")[1]), ["chromium", "firefox", "webkit"].index(r[2])))

AULAS = []
AULAS.append(projeto(8, "MÓDULO 2 · AULA 8", "Criando o projeto e abrindo o terminal", [
    ("Agora começa a parte boa: criar o seu projeto de testes.", bt(("MÓDULO 2", "muted", 80), ("O SEU PROJETO", "gold", 170))),
    ("Primeiro, uma pasta. Abre os Documentos e cria uma pasta nova chamada meu-primeiro-playwright, tudo minúsculo e com traço no lugar do espaço.",
     {"type": "pastas", "caminho": "Este Computador  ›  Documentos", "itens": ["Fotos", "Músicas", "Trabalho", {"nome": "meu-primeiro-playwright", "novo": True}], "novo_em": 1.0, "legenda": "meu-primeiro-playwright"}),
    ("Por que eu prefiro sem espaço e sem acento? Porque nomes simples evitam alguns problemas com caminhos e comandos. Usando traço, a gente deixa tudo mais fácil.",
     {"type": "compare", "title": "NOME DA PASTA", "items": [["meu projeto", "PODE DAR TRABALHO", "red"], ["meu-projeto", "SEM DOR DE CABEÇA", "gold"]], "size": 110, "stagger": 1.2, "vs": False}),
    ("Agora abre o VS Code, clica em File, depois Open Folder,",
     {"type": "menu", "app": "vscode", "abre": 0, "menus": [["New Text File", "New File...", "New Window", "—", "Open File...", "Open Folder...", "Open Recent ›", "—", "Save", "Save As..."]], "caminho": [5], "legenda": "File › Open Folder"}),
    ("e escolhe essa pasta: clica nela, e depois em Selecionar pasta.",
     {"type": "pastas", "titulo": "Abrir Pasta", "caminho": "Este Computador  ›  Documentos", "itens": ["Fotos", "Músicas", "Trabalho", "meu-primeiro-playwright"],
      "seleciona": 3, "seleciona_em": 0.9, "botao": "Selecionar pasta", "botao_em": 2.6, "legenda": "Clica na pasta · Selecionar pasta"}),
    ("Se ele perguntar se você confia nos autores da pasta, clica em Yes. Os autores aqui é você.",
     {"type": "instalador", "app": "Visual Studio Code", "titulo": "Do you trust the authors of the files in this folder?", "subtitulo": "Code provides features that may automatically execute files in this folder", "botao": "Yes, I trust the authors", "legenda": "A pasta é sua: pode confiar"}),
    ("Pronto: a pasta aparece vazia ali na esquerda.", {"type": "editor", "arquivo": "Welcome", "pastas": ["meu-primeiro-playwright"], "codigo": "// A pasta do projeto está aberta!\n// Por enquanto, vazia.", "legenda": "O seu projeto está aberto"}),
    ("Agora o terminal dentro do VS Code: menu Terminal, New Terminal. Você também pode usar o atalho que está aqui na tela.",
     {"type": "menu", "app": "vscode", "abre": 6, "menus": [["New Terminal       Ctrl+`", "Split Terminal", "—", "Run Task...", "Run Build Task..."]], "caminho": [0], "pastas": ["meu-primeiro-playwright"], "resultado": "terminal", "legenda": "Terminal › New Terminal  (Ctrl + `)"}),
    ("Olha o caminho antes do cursor: ele termina com meu-primeiro-playwright. Isso quer dizer que o terminal está dentro do seu projeto, que é exatamente onde ele precisa estar.",
     vterm([{"cmd": ""}], "O caminho termina no seu projeto")),
    ("Na próxima aula, a gente instala o Playwright com um comando só.", proxima("Instalando o Playwright")[0]),
    ("Te vejo lá!", proxima("Instalando o Playwright")[1]),
]))

AULAS.append(projeto(9, "MÓDULO 2 · AULA 9", "Instalando o Playwright", [
    ("Hoje é o dia: a gente instala o Playwright. E é um comando só.", titulo(9, "PLAYWRIGHT")),
    ("No terminal do VS Code, digita npm init playwright arroba latest e aperta Enter.", vterm(INIT, "npm init playwright@latest", colinha=True)),
    ("Na primeira vez, ele pergunta se pode instalar um ajudante. Aperta y e Enter.", vterm(INIT + OK, "Aperte y e Enter", ja=1)),
    ("Agora ele faz quatro perguntas. A primeira: TypeScript ou JavaScript? Vamos escolher JavaScript. Assim a gente consegue focar primeiro em aprender automação, sem adicionar outra linguagem no caminho.",
     vterm(INIT + OK[2:] + Q1, "1ª pergunta: JavaScript", ja=2)),
    ("Segunda: onde guardar os testes? Ele já sugere a pasta tests. Só aperta Enter.", vterm(INIT + Q1[1:] + Q2, "2ª pergunta: tests (só Enter)", ja=2)),
    ("Terceira: quer um workflow do GitHub Actions? Aqui digita y. É isso que, no final do curso, vai fazer seus testes rodarem sozinhos.", vterm(INIT + Q1[1:] + Q2 + Q3, "3ª pergunta: y (sim)", ja=3)),
    ("Quarta: instalar os navegadores do Playwright? Enter, que é sim. Ele baixa o Chromium, o Firefox e o WebKit, que é o motor de navegador que eu te mostrei na abertura do curso.",
     vterm(INIT + Q1[1:] + Q2 + Q3 + Q4, "4ª pergunta: Enter (sim)", ja=4)),
    ("Se você está no Linux, ele faz uma pergunta a mais, sobre as dependências do sistema. Responde y. É aquele detalhe que eu tinha comentado no módulo um.",
     {"type": "cards", "titulo": "SÓ NO LINUX", "itens": [["?", "Dependências", "do sistema?"], ["y", "Responde sim", "e ele instala", "#ffd23f"]]}),
    ("Espera terminar. Quando aparecer Happy hacking no final, deu tudo certo.", vterm(INIT + Q1[1:] + Q2 + Q3 + Q4 + FIM, "Happy hacking = deu certo", ja=6)),
    ("Olha a esquerda: apareceram vários arquivos novos. Na próxima aula, eu te explico o que é cada um.",
     {"type": "editor", "arquivo": "example.spec.js", "pastas": ARVORE, "codigo": EXEMPLO, "digitar": False, "fonte": 26, "legenda": "Vários arquivos novos"}),
    ("Te vejo lá!", proxima("Os arquivos que ele criou")[1]),
]))

AULAS.append(projeto(10, "MÓDULO 2 · AULA 10", "Os arquivos que ele criou", [
    ("O Playwright criou alguns arquivos pra você. Bora entender cada um, sem decorar nada.", titulo(10, "OS ARQUIVOS")),
    ("A pasta tests é onde ficam os seus testes. Dentro dela já veio um exemplo, o example ponto spec ponto js.",
     {"type": "editor", "arquivo": "example.spec.js", "pastas": ARVORE, "codigo": EXEMPLO, "digitar": False, "fonte": 26, "legenda": "tests: onde moram os testes"}),
    ("Nos nossos testes, os arquivos vão terminar em ponto spec ponto js. Quando você vir esse final, já sabe: é um arquivo de teste.", dict(bt((".spec.js", "gold", 200), ("= ARQUIVO DE TESTE", "white", 110)), colinha=True, colinha_em=1.2)),
    ("Abre o example. Esse é o arquivo inteiro: dois testes que entram no site do próprio Playwright e conferem umas coisas. Não precisa entender agora, a gente vai escrever o nosso do zero.",
     {"type": "editor", "arquivo": "example.spec.js", "pastas": ARVORE, "codigo": EXEMPLO, "digitar": False, "fonte": 26, "destaque": [4, 11], "destaque_em": 1.5, "legenda": "Dois testes de exemplo"}),
    ("O playwright ponto config ponto js é o painel de controle: em quais navegadores rodar, como gerar o relatório, e por aí vai. Tem bastante comentário, é normal. A gente vai mexer nele mais pra frente.",
     {"type": "editor", "arquivo": "playwright.config.js", "pastas": ARVORE, "codigo": CONFIG, "digitar": False, "rolar": True, "rolar_de": 1.5, "rolar_dur": 6.0, "fonte": 24, "legenda": "O painel de controle"}),
    ("O package ponto json é a ficha do projeto: o nome e as ferramentas que ele usa, como o próprio Playwright.",
     {"type": "editor", "arquivo": "package.json", "pastas": ARVORE, "codigo": PACKAGE, "digitar": False, "destaque": [2, 11], "destaque_em": 1.2, "fonte": 26, "legenda": "A ficha do projeto"}),
    ("A pasta node modules guarda as dependências do projeto: o Playwright e tudo que ele precisa pra funcionar. Ela fica enorme, mas você não precisa editar nada ali.",
     {"type": "cards", "titulo": "NODE_MODULES", "itens": [["▣", "Dependências", "o Playwright e o que ele precisa"], ["!", "Não edite", "ela se cuida sozinha", "#ff6b6b"]], "colinha": False}),
    ("O ponto gitignore é a lista do que não vai pro GitHub, como essa pasta node modules. E a pasta ponto github guarda o workflow que você pediu na instalação.",
     {"type": "editor", "arquivo": ".gitignore", "pastas": ARVORE, "codigo": GITIGNORE, "digitar": False, "destaque": [3], "destaque_em": 1.0, "legenda": "O que não vai pro GitHub"}),
    ("Por enquanto, lembra de duas coisas: seus testes ficam em tests e as configurações principais ficam no playwright ponto config ponto js. O restante a gente conhece quando precisar.",
     {"type": "cards", "titulo": "LEMBRA DE DUAS COISAS", "itens": [["1", "tests/", "os seus testes"], ["2", "playwright.config.js", "as configurações", "#69a7ff"]]}),
    ("Na próxima aula, a gente roda esse exemplo e vê o Playwright trabalhando pela primeira vez.", proxima("Rodando o teste de exemplo")[0]),
    ("Te vejo lá!", proxima("Rodando o teste de exemplo")[1]),
]))

EXEMPLO = open(os.path.join(RAIZ, "curso-playwright", "referencia_init", "tests", "example.spec.js"), encoding="utf8").read().rstrip("\n")


def vs11(legenda, terminal, **kw):
    """VS Code de verdade: o example.spec.js em cima (o começo dele, como fica na tela) e o terminal integrado embaixo"""
    d = {"type": "editor", "arquivo": "example.spec.js", "pastas": ARVORE, "codigo": "\n".join(EXEMPLO.split("\n")[:9]), "digitar": False, "fonte": 22, "legenda": legenda, "terminal": terminal}
    d.update(kw)
    return d


CMD = {"cmd": "npx playwright test"}
AULAS.append(projeto(11, "MÓDULO 2 · AULA 11", "Rodando o teste de exemplo e o relatório HTML", [
    ("Chegou a hora de ver o Playwright funcionando.", titulo(11, "RODANDO")),
    ("Antes de rodar, olha o que tem no arquivo de exemplo que o Playwright criou: dois testes. Um chamado has title, e outro chamado get started link.",
     {"type": "editor", "arquivo": "example.spec.js", "codigo": "\n".join(EXEMPLO.split("\n")[:12]), "digitar": False, "destaque": [4, 11], "destaque_em": 1.0, "fonte": 26, "legenda": "2 testes no arquivo"}),  # o arquivo inteiro parado: os dois test() à vista, sem rolar pra código que não é explicado
    ("O primeiro abre o site do Playwright e confere o título da página. O segundo clica no link Get started. Não precisa entender o código agora: você vai aprender tudo isso no curso.",
     {"type": "cards", "titulo": "O QUE O EXEMPLO FAZ", "itens": [["1", "has title", "abre o site e confere o título"], ["2", "get started link", "clica em Get started", "#69a7ff"]]}),
    ("Pra rodar, usa o terminal aqui embaixo no VS Code: digita npx playwright test e aperta Enter.", vs11("No terminal do VS Code", [dict(CMD, em=0.3)], colinha=True, colinha_em=1.2)),
    ("Repara: nenhuma janela de navegador abriu. É que, por padrão, o Playwright roda em modo headless, que quer dizer sem cabeça: sem janela, e por isso mais rápido.",
     vs11("Nenhuma janela abriu: headless", [dict(CMD, ja=True), {"out": "Running 6 tests using 4 workers", "cor": "mut", "em": 0.1}])),
    ("Olha o resultado: seis passaram. Mas o arquivo só tinha dois testes!",
     vs11("6 passaram… com 2 testes?", [dict(CMD, ja=True), {"out": "Running 6 tests using 4 workers", "cor": "mut", "ja": True}, {"out": "  6 passed (7.9s)", "cor": "ac", "em": 0.12}])),
    ("Isso acontece porque cada um dos dois testes rodou em três navegadores. Dois testes vezes três navegadores: seis execuções.",
     {"type": "cards", "titulo": "2 TESTES × 3 NAVEGADORES = 6 EXECUÇÕES", "itens": [["C", "Chromium", "2 execuções"], ["F", "Firefox", "2 execuções", "#ff8c42"], ["W", "WebKit", "2 execuções", "#69a7ff"]]}),
    ("E no final ele dá uma dica: npx playwright show-report. Digita isso.",
     vs11("npx playwright show-report", [{"out": "  6 passed (7.9s)", "cor": "ac", "ja": True}, {"out": "To open last HTML report run:", "cor": "mut", "ja": True}, {"out": "  npx playwright show-report", "cor": "txt", "ja": True},
                                         {"cmd": "npx playwright show-report", "em": 0.35}, {"out": "Serving HTML report at http://localhost:9323", "cor": "ac", "em": 0.7}], colinha=True, colinha_em=1.2)),
    ("O relatório abre sozinho no navegador: cada teste, em cada navegador, quanto tempo levou, e se passou ou falhou.", {"type": "pw_relatorio", "testes": REL, "legenda": "Cada teste, em cada navegador"}),
    ("Clica em qualquer teste pra ver os passos que ele fez, um por um.",
     {"type": "pw_relatorio", "testes": REL, "abrir": {"titulo": "get started link", "arquivo": "example.spec.js:11", "projeto": "chromium",
      "passos": [["Navigate to \"https://playwright.dev/\"", "0.9s"], ["Click getByRole('link', { name: 'Get started' })", "0.3s"], ["Expect \"toBeVisible\"", "0.1s"]]}, "legenda": "Os passos, um por um"}),
    ("Pra fechar o relatório, volta no terminal e aperta Control C.",
     vs11("Ctrl + C fecha o relatório", [{"cmd": "npx playwright show-report", "ja": True}, {"out": "Serving HTML report at http://localhost:9323", "cor": "ac", "ja": True}, {"out": "^C", "cor": "yel", "em": 0.45}])),
    ("Agora você já tem tudo funcionando. No próximo módulo, a gente apaga esse exemplo e escreve o seu primeiro teste, do zero.",
     {"type": "flow", "a": "EXEMPLO ✓", "a_sub": "do Playwright", "b": "SEU CÓDIGO", "b_sub": "a partir de agora", "caption": "AGORA É COM VOCÊ"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 3 · PRIMEIRO TESTE"}),
]))


def main():
    for slug, p in AULAS:
        for x in p["script"]["long"]["parts"][0]["sentences"]:
            if x["scene"].get("botao") == "Selecionar pasta":
                x["pausa"] = 2.5  # tempo de ver o clique na pasta e no botão
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")


if __name__ == "__main__":
    main()

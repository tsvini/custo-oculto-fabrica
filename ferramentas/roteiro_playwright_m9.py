"""Gera projetos/curso-playwright-43..45 (módulo 9: Git, GitHub e CI). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
As saídas do Git são as reais (rodadas numa cópia do projeto do aluno, com .env, node_modules e playwright/.auth: o .gitignore deixa os três de fora)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m4 import edc
from roteiro_playwright_m8 import cod, ln, ARV_AUTH

PROJ = os.path.join(RAIZ, "curso-playwright", "projeto")
REF = os.path.join(RAIZ, "curso-playwright", "referencia_init")
YML0 = open(os.path.join(REF, ".github", "workflows", "playwright.yml"), encoding="utf8").read().rstrip("\n")
YML = open(os.path.join(PROJ, ".github", "workflows", "playwright.yml"), encoding="utf8").read().rstrip("\n")
C42 = cod(42)
TOPO = "\n".join(C42.split("\n")[:10])
PASTA = "C:\\Users\\voce\\Documents\\meu-primeiro-playwright"
URL = "https://github.com/voce/meu-primeiro-playwright.git"
VERM = "#ff6b6b"
ARQS = ["  new file:   .env.example", "  new file:   .github/workflows/playwright.yml", "  new file:   .gitignore", "  new file:   package-lock.json", "  new file:   package.json",
        "  new file:   pages/CheckoutPage.js", "  new file:   pages/LoginPage.js", "  new file:   pages/ProdutosPage.js", "  new file:   playwright.config.js",
        "  new file:   tests/auth.setup.js", "  new file:   tests/compra.spec.js", "  new file:   tests/login.spec.js", "  new file:   tests/usuarios.spec.js"]


def git(legenda, linhas, **kw):
    """VS Code com o terminal embaixo: comando digitado e a saída real"""
    L = []
    for i, l in enumerate(linhas):
        L.append(dict(l, em=l.get("em", 0.05 if "cmd" in l else 0.45 + i * 0.04)))
    return edc(TOPO, legenda, arquivo="compra.spec.js", pastas=ARV_AUTH, terminal=L, **kw)


def termo(legenda, linhas, **kw):
    d = {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": PASTA, "linhas": linhas, "legenda": legenda}
    d.update(kw)
    return d


AULAS = []

# ---------- Aula 43 ----------
AULAS.append(projeto(43, "MÓDULO 9 · AULA 43", "Git - salvando o projeto", [
    ("O Git é um programa que guarda versões do seu projeto. Como pontos de salvamento num jogo.",
     {"type": "cards", "titulo": "GIT", "itens": [["💾", "Pontos de salvamento", "cada salvamento é um commit"], ["↺", "Voltar no tempo", "se algo quebrar", "#69a7ff"]]}),
    ("E pra quem testa, pra que serve? Se você estragar um teste, volta pra versão que funcionava. E toda empresa usa: é assim que a equipe junta o trabalho de todo mundo.", {"type": "cards", "itens": [["↩", "Voltar", "pra versão que funcionava"], ["👥", "Equipe", "junta o trabalho de todos", "#69a7ff"], ["🏢", "Empresas", "todas usam", "#ffd23f"]]}),  # pra que / quando
    ("No terminal do VS Code: git init. Init é iniciar: comece a guardar as versões desta pasta.",
     git("init = iniciar", [{"cmd": "git init"}, {"out": "Initialized empty Git repository in", "cor": "mut"}, {"out": "C:/Users/voce/Documents/meu-primeiro-playwright/.git/", "cor": "mut"}], colinha=True, colinha_em=1.2)),
    ("Depois: git add ponto. Add é adicionar, e o ponto quer dizer tudo: prepare todos os arquivos pro próximo salvamento.",
     git("add . = prepare tudo", [{"cmd": "git add ."}])),
    ("Pra conferir o que vai entrar, git status. Repara: o node modules, o ponto env e a pasta do login salvo não aparecem. O gitignore está fazendo o trabalho dele.",
     termo("Nem node_modules, nem .env, nem o login salvo", [{"cmd": "git status", "ja": True}, {"out": "Changes to be committed:", "cor": "txt", "ja": True}] + [{"out": a, "cor": "ac", "ja": True} for a in ARQS],
           compacto=True, fonte=24, fonte_min=22)),
    ("E: git commit traço m, e uma mensagem entre aspas, tipo meu primeiro projeto Playwright. Commit é o salvamento, e o traço m é a mensagem dele.",
     git("commit = o salvamento · -m = a mensagem", [{"cmd": "git commit -m \"meu primeiro projeto Playwright\""}, {"out": "[master (root-commit) 24d5d51] meu primeiro projeto Playwright", "cor": "ac"},
                                                      {"out": " 13 files changed, 324 insertions(+)", "cor": "mut"}])),
    ("Se for a primeira vez que você usa o Git, ele pode pedir seu nome e seu e-mail. São dois comandos: git config traço traço global user ponto name, e user ponto email. Depois roda o commit de novo.",
     termo("Primeira vez? Seu nome e seu e-mail", [{"cmd": "git commit -m \"meu primeiro projeto Playwright\"", "ja": True}, {"out": "Author identity unknown", "cor": VERM, "ja": True},
                                                  {"out": "*** Please tell me who you are.", "cor": VERM, "ja": True}, {"cmd": "git config --global user.name \"Seu Nome\""}, {"cmd": "git config --global user.email \"voce@email.com\""},
                                                  {"cmd": "git commit -m \"meu primeiro projeto Playwright\""}, {"out": "[master (root-commit) 24d5d51] meu primeiro projeto Playwright", "cor": "ac"}], fonte=30, fonte_min=24)),
    ("E no dia a dia? Terminou um teste e ele passou: faz um commit. E a mensagem diz o que mudou, tipo adiciona teste do carrinho. Daqui a um mês, você vai saber o que tem em cada salvamento.",
     {"type": "traducao", "titulo": "NO DIA A DIA", "linhas": [["git add .", "prepare o que mudou"], ["git commit -m \"adiciona teste do carrinho\"", "salve, com uma mensagem clara"]]}),
    ("Pronto: o seu projeto tem o primeiro ponto de salvamento. Na próxima aula, ele vai pro GitHub.", {"type": "passo", "icone": "▶", "titulo": "Próxima aula", "sub": "GitHub: enviando o projeto"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: GITHUB"}),
]))

# ---------- Aula 44 ----------
GH = {"type": "github", "usuario": "voce", "repo": "meu-primeiro-playwright"}
ARQ_GH = [[".github", True, "meu primeiro projeto Playwright"], ["pages", True, "meu primeiro projeto Playwright"], ["tests", True, "meu primeiro projeto Playwright"],
          [".env.example", False, "meu primeiro projeto Playwright"], [".gitignore", False, "meu primeiro projeto Playwright"], ["package-lock.json", False, "meu primeiro projeto Playwright"],
          ["package.json", False, "meu primeiro projeto Playwright"], ["playwright.config.js", False, "meu primeiro projeto Playwright"]]
AULAS.append(projeto(44, "MÓDULO 9 · AULA 44", "GitHub - enviando o projeto", [
    ("O GitHub é um site que guarda projetos Git na internet. É a vitrine de quem trabalha com tecnologia.", titulo(44, "GITHUB")),
    ("Pra você, ele resolve três coisas: um backup do projeto, se o computador quebrar. Um lugar onde a equipe trabalha junto. E o seu portfólio: quem for te contratar pode ver o seu código funcionando.",
     {"type": "cards", "itens": [["☁", "Backup", "se o computador quebrar"], ["👥", "Equipe", "todo mundo no mesmo projeto", "#69a7ff"], ["⭐", "Portfólio", "quem contrata vê seu código", "#ffd23f"]]}),
    ("Cria uma conta no github ponto com, se ainda não tiver. Depois clica em New repository. Repositório é a pasta do projeto, lá no GitHub. Dá o nome e cria, sem marcar nenhuma opção, porque o seu projeto já tem os arquivos dele.",
     dict(GH, tela="novo", opcoes_em=5.0, legenda="New repository · sem marcar nenhuma opção")),
    ("O GitHub mostra os comandos. No terminal: git branch traço M main. Branch é ramo: uma linha de versões do projeto. Esse comando dá o nome main pro ramo principal.",
     git("branch -M main = o ramo principal se chama main", [{"cmd": "git branch -M main"}])),
    ("Depois: git remote add origin, e o endereço do seu repositório. Remote é remoto: avise o Git que existe uma cópia lá no GitHub, chamada origin.",
     dict(GH, tela="setup", url_em=1.0, cmd_em=4.0, legenda="remote = remoto: a cópia lá no GitHub")),
    ("E o envio: git push traço u origin main. Push é empurrar: mande o projeto pro GitHub. O traço u liga a sua main com a main de lá, e nas próximas vezes basta git push.",
     git("push = empurrar · -u = liga com a main de lá", [{"cmd": f"git remote add origin {URL}", "ja": True}, {"cmd": "git push -u origin main"}, {"out": f"To {URL}", "cor": "mut"},
                                                          {"out": " * [new branch]      main -> main", "cor": "ac"}, {"out": "branch 'main' set up to track 'origin/main'.", "cor": "mut"}])),
    ("Na primeira vez, o Git pode abrir o navegador pra você entrar na sua conta do GitHub. É normal: faz o login e volta pro terminal.",
     {"type": "cards", "itens": [["🌐", "Abre o navegador", "na primeira vez"], ["🔑", "Você entra na conta", "é normal", "#69a7ff"], ["↩", "Volta pro terminal", "o envio continua", "#ffd23f"]]}),
    ("Atualiza a página do GitHub: seu projeto está lá. E repara: nem o ponto env, nem a pasta do login salvo subiram.",
     dict(GH, tela="repo", arquivos=ARQ_GH, commit="meu primeiro projeto Playwright", foco_em=2.0, foco_item=3, foco_rotulo="← o .env não subiu", url_em=99)),
    ("E daqui pra frente, o ciclo é sempre esse: add, commit e push. E o GitHub fica igual à sua máquina.",
     {"type": "traducao", "titulo": "O CICLO DE TODO DIA", "linhas": [["git add .", "prepare"], ["git commit -m \"...\"", "salve"], ["git push", "mande pro GitHub"]]}),
    ("Na próxima aula: os testes rodando sozinhos no GitHub.", proxima("GitHub Actions")[0]),
    ("Te vejo lá!", proxima("GitHub Actions")[1]),
]))

# ---------- Aula 45 ----------
L_ENV = ln(YML, "env:")
GHA = {"type": "gh_actions", "usuario": "voce", "repo": "meu-primeiro-playwright", "workflow": "Playwright Tests", "commit": "testes no GitHub Actions"}
AULAS.append(projeto(45, "MÓDULO 9 · AULA 45", "GitHub Actions - os testes rodando sozinhos", [
    ("E se o GitHub rodasse os seus testes sozinho? É isso que o GitHub Actions faz.", titulo(45, "GITHUB ACTIONS")),
    ("Por que isso importa? Sem ele, alguém precisa lembrar de rodar os testes. Com ele, toda vez que alguém manda uma mudança pro repositório, os testes rodam sozinhos. E em muitas empresas os testes ficam junto com o código do site: aí cada mudança no site passa pelos testes antes de chegar no cliente.", {"type": "compare", "title": "RODAR OS TESTES", "items": [["SEM ACTIONS", "ALGUÉM PRECISA LEMBRAR", "white"], ["COM ACTIONS", "RODA A CADA MUDANÇA", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),  # pra que / quando
    ("O Playwright já criou esse arquivo lá no começo: ponto github, workflows, playwright ponto yml.",
     edc(YML0, ".github/workflows/playwright.yml", arquivo="playwright.yml", pastas=ARV_AUTH, rolar=True, rolar_de=2.0, rolar_dur=2.0, fonte=22)),
    ("Lendo em português: quando houver um push ou um pull request na main, use uma máquina Ubuntu, instale tudo e rode os testes. Esses quandos são os gatilhos do arquivo.",
     {"type": "traducao", "titulo": "LENDO O ARQUIVO EM PORTUGUÊS", "linhas": [["on: push / pull_request", "quando houver push ou PR na main"], ["runs-on: ubuntu-latest", "use uma máquina Ubuntu"],
                                                                            ["npm ci", "instale as dependências"], ["npx playwright install", "instale os navegadores"], ["npx playwright test", "rode os testes"]]}),
    ("Pull request é quando alguém da equipe pede pra juntar uma mudança na main. Os testes rodam antes, e se ficarem vermelhos, a mudança espera o conserto.",
     {"type": "cards", "titulo": "PULL REQUEST", "itens": [["⇄", "Pede pra juntar", "uma mudança na main"], ["▶", "Os testes rodam", "antes de juntar", "#69a7ff"], ["✗", "Vermelho?", "espera o conserto", VERM]]}),
    ("E dá até pra agendar: rodar todo dia de madrugada, mesmo sem ninguém mexer. É assim que um teste aparece falhando às seis da manhã, como na aula do trace.",
     {"type": "cards", "itens": [["⇪", "A cada push", "alguém mandou mudança"], ["⇄", "A cada pull request", "antes de juntar", "#69a7ff"], ["⏰", "Agendado", "toda madrugada", "#ffd23f"]], "titulo": "QUANDO ELE RODA"}),
    ("Só falta uma coisa: o ponto env não foi pro GitHub, então lá os testes não sabem o usuário e a senha.",
     {"type": "cards", "itens": [["✗", ".env", "ficou só na sua máquina", VERM], ["?", "No GitHub", "os testes não sabem usuário e senha", "#ffd23f"]]}),
    ("No GitHub: Settings, Secrets and variables, Actions, New repository secret. Cria o SAUCE underline USER e o SAUCE underline PASSWORD. Secret é segredo: ninguém consegue ver o valor depois.",
     dict(GH, tela="secrets", clique_em=0.8, menu_em=2.0, botao_em=3.4, aviso="ninguém vê o valor depois", legenda="Settings › Secrets and variables › Actions")),
    ("No yml, no passo que roda os testes, um env que entrega esses segredos pros testes.",
     edc(YML, "env: os segredos entregues aos testes", arquivo="playwright.yml", pastas=ARV_AUTH, digitar=True, digitar_de=L_ENV, digitar_ate=L_ENV + 2, rolar=True, rolar_de=0.6, rolar_dur=0.9, fonte=22)),
    ("Traduzindo: SAUCE USER, dois pontos, e cifrão chaves chaves secrets ponto SAUCE USER. Pegue o valor guardado no cofre do GitHub, e entregue pros testes com esse nome, igual o ponto env fazia.",
     {"type": "traducao", "titulo": "DO COFRE PROS TESTES", "linhas": [["SAUCE_USER: ${{ secrets.SAUCE_USER }}", "o usuário, do cofre"], ["SAUCE_PASSWORD: ${{ secrets.SAUCE_PASSWORD }}", "a senha, do cofre"]]}),
    ("Manda pro GitHub com git push e abre a aba Actions: olha os testes rodando lá.", dict(GHA, inicio_em=1.0, legenda="Os testes rodando no GitHub")),
    ("Verde: passou. E no fim tem o relatório pra baixar, porque esse arquivo tem o passo que guarda ele.", dict(GHA, pronto=True, status="ok", artefato="playwright-report", legenda="Passou · o relatório pra baixar")),
    ("E se ficar vermelho? O GitHub te avisa por e-mail. Você baixa o relatório, abre o trace, o print e o vídeo, como nas aulas 28 e 30, e anexa no card do bug.", {"type": "cards", "itens": [["✗", "Vermelho", "o GitHub te avisa", "#ff6b6b"], ["⬇", "Baixa o relatório", "trace, print e vídeo", "#69a7ff"], ["📋", "Card do bug", "com as evidências", "#ffd23f"]]}),  # pra que / quando
    ("Fechamos o projeto! Tem bônus: testes de API.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Bônus: testes de API"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 10 · API"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 9 (gerado do roteiro_playwright_m9.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo9.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

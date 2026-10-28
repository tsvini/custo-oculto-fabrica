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
NAO_RASTREADOS = [".env.example", ".github/", ".gitignore", "package-lock.json", "package.json", "pages/", "playwright.config.js", "tests/"]
AULAS.append(projeto(43, "MÓDULO 9 · AULA 43", "Git - salvando o projeto", [
    ("O projeto está pronto. Agora, a pergunta: como guardar ele do jeito certo, de um jeito que dá pra voltar atrás se alguma coisa quebrar?",
     bt(("O PROJETO ESTÁ PRONTO", "white", 100), ("COMO GUARDAR DO JEITO CERTO?", "gold", 100))),
    ("Sem nenhuma ferramenta, o que muita gente faz é copiar a pasta. Projeto final. Projeto final dois. Projeto final agora vai. Depois de uma semana, ninguém sabe qual é qual, nem o que mudou de uma pra outra.",
     {"type": "cards", "titulo": "SEM GIT", "itens": [["📁", "projeto-final", "a primeira"], ["📁", "projeto-final-2", "mudou o quê?", "#69a7ff"], ["📁", "projeto-final-agora-vai", "qual é a certa?", "#ff6b6b"]]}),
    ("O Git resolve isso. Ele é um programa que guarda a história do seu projeto, sem copiar pasta nenhuma. Quando você manda, ele tira uma foto de como os arquivos estão naquele momento, e guarda todas as fotos, em ordem.",
     {"type": "cards", "titulo": "GIT", "itens": [["📸", "Uma foto do projeto", "quando você manda"], ["🗂", "Todas guardadas", "em ordem, com data", "#69a7ff"], ["↺", "Voltar no tempo", "pra qualquer foto", "#ffd23f"]]}),
    ("Cada foto dessas tem um nome: commit. Pensa nos pontos de salvamento de um jogo. Você salva antes da parte difícil, e se der errado, volta pro ponto salvo.",
     {"type": "traducao", "codigo": "commit", "texto_puro": True, "partes": [["commit", "uma foto do projeto, um ponto de salvamento"]], "passo": 1.6}),
    ("E uma confusão muito comum: Git e GitHub não são a mesma coisa. O Git é o programa no seu computador, aquele que você instalou na aula cinco. O GitHub é um site, onde você guarda essa história na internet. Ele é a próxima aula.",
     {"type": "compare", "title": "NÃO SÃO A MESMA COISA", "items": [["GIT", "O PROGRAMA, NO SEU COMPUTADOR", "white"], ["GITHUB", "O SITE, NA INTERNET", "gold"]], "size": 90, "stagger": 1.8, "vs": True}),
    ("E pra quem testa, pra que serve? Se você estragar um teste, volta pra versão que funcionava. É assim que a equipe junta o trabalho de todo mundo sem um apagar o do outro. E quase toda vaga de QA pede Git.",
     {"type": "cards", "itens": [["↩", "Voltar", "pra versão que funcionava"], ["👥", "Equipe", "junta o trabalho de todos", "#69a7ff"], ["💼", "Vagas", "quase todas pedem Git", "#ffd23f"]]}),
    ("Salvar com o Git tem sempre três passos. Primeiro, você muda os arquivos, que é o que você já faz. Segundo, o git add: você escolhe o que vai entrar na foto. Terceiro, o git commit: você tira a foto, com uma legenda dizendo o que mudou.",
     {"type": "cards", "titulo": "OS 3 PASSOS", "itens": [["✎", "1. Muda os arquivos", "o que você já faz"], ["📦", "2. git add", "escolhe o que vai na foto", "#69a7ff"], ["📸", "3. git commit", "tira a foto, com legenda", "#ffd23f"]]}),
    ("Agora na prática. Tudo é feito no terminal do VS Code, aqui embaixo. Antes de começar, confere o caminho antes do cursor: ele tem que terminar com o nome da pasta do projeto, igual na aula oito.",
     git("O terminal na pasta do projeto", [{"cmd": ""}])),
    ("Se é a primeira vez que você usa o Git nesse computador, ele precisa saber quem você é, porque toda foto leva o nome de quem tirou. São dois comandos: git config traço traço global user ponto name, e o seu nome entre aspas. E user ponto email, com o seu e-mail. Só uma vez por computador. E uma dica: usa o mesmo e-mail que você vai usar na conta do GitHub, na próxima aula. Assim, lá no seu perfil, cada commit aparece como seu.",
     termo("Uma vez por computador: o seu nome e o seu e-mail", [{"cmd": "git config --global user.name \"Seu Nome\""}, {"cmd": "git config --global user.email \"voce@email.com\""}], fonte=30, fonte_min=24)),
    ("Agora sim: git init. Init é iniciar. Ele avisa o Git: a partir de agora, guarde a história desta pasta.",
     git("init = iniciar", [{"cmd": "git init"}, {"out": "Initialized empty Git repository in", "cor": "mut"}, {"out": "C:/Users/voce/Documents/meu-primeiro-playwright/.git/", "cor": "mut"}], colinha=True, colinha_em=1.2)),
    ("Ele criou uma pasta escondida chamada ponto git. É lá que ficam todas as fotos. Você não precisa mexer nela, nunca. E o git init é feito uma vez só por projeto.",
     {"type": "cards", "itens": [["🙈", "A pasta .git", "escondida, onde ficam as fotos"], ["🚫", "Não mexe nela", "o Git cuida sozinho", "#ff6b6b"], ["1×", "git init", "uma vez por projeto", "#ffd23f"]]}),
    ("Agora, git status. Status é a situação: o Git te conta o que ele está vendo. Repara: tudo em vermelho, debaixo de untracked files, arquivos não rastreados. Ou seja: o Git viu os arquivos, mas eles ainda não vão na foto.",
     termo("Vermelho: o Git viu, mas ainda não vai na foto", [{"cmd": "git status"}, {"out": "On branch master", "cor": "mut"}, {"out": "No commits yet", "cor": "mut"}, {"out": "Untracked files:", "cor": "txt"}]
           + [{"out": "        " + a, "cor": VERM} for a in NAO_RASTREADOS], compacto=True, fonte=24, fonte_min=20)),
    ("Passo dois: git add ponto. Add é adicionar, e o ponto quer dizer tudo. Prepare todos os arquivos que mudaram pra próxima foto.",
     git("add . = prepare tudo pra foto", [{"cmd": "git add ."}])),
    ("Roda o git status de novo. Agora está tudo verde, debaixo de changes to be committed: mudanças que vão entrar na foto.",
     termo("Verde: preparado, vai na próxima foto", [{"cmd": "git status", "ja": True}, {"out": "Changes to be committed:", "cor": "txt", "ja": True}] + [{"out": a, "cor": "ac", "ja": True} for a in ARQS],
           compacto=True, fonte=24, fonte_min=22)),
    ("Então, a regra das cores: vermelho é o que mudou, mas ainda não vai na foto. Verde é o que já está preparado, e vai na próxima foto.",
     {"type": "compare", "title": "AS CORES DO GIT STATUS", "items": [["VERMELHO", "MUDOU, MAS NÃO VAI NA FOTO", "red"], ["VERDE", "PREPARADO, VAI NA FOTO", "green"]], "size": 80, "stagger": 1.6, "vs": False}),
    ("E repara no que não aparece na lista: o node modules, o ponto env com a sua senha, e a pasta do login salvo. É o ponto gitignore fazendo o trabalho dele, como na aula vinte e quatro. Eles nunca entram na foto.",
     {"type": "cards", "titulo": "FICAM DE FORA (.gitignore)", "itens": [["📦", "node_modules", "dá pra baixar de novo"], ["🔒", ".env", "a sua senha", "#ff6b6b"], ["🍪", "playwright/.auth", "o login salvo", "#ffd23f"]]}),
    ("Passo três, a foto: git commit traço m, e entre aspas a legenda, tipo meu primeiro projeto Playwright. Commit é a foto, e o traço m é a mensagem dela.",
     git("commit = a foto · -m = a legenda", [{"cmd": "git commit -m \"meu primeiro projeto Playwright\""}, {"out": "[master (root-commit) 24d5d51] meu primeiro projeto Playwright", "cor": "ac"},
                                              {"out": " 13 files changed, 324 insertions(+)", "cor": "mut"}])),
    ("Lendo a resposta: o vinte e quatro d cinco d cinco um é o código dessa foto, cada uma tem o seu. E treze arquivos entraram nela.",
     {"type": "traducao", "codigo": "[master (root-commit) 24d5d51] meu primeiro projeto Playwright", "partes": [["24d5d51", "o código dessa foto"], ["meu primeiro projeto Playwright", "a legenda"]], "passo": 2.0}),
    ("Pra ver a história do projeto: git log traço traço oneline. Uma foto por linha, a mais nova em cima.",
     git("log = a história do projeto", [{"cmd": "git log --oneline"}, {"out": "24d5d51 meu primeiro projeto Playwright", "cor": "ac"}])),
    ("E no dia a dia, como fica? Imagina que amanhã você muda o teste da compra. O git status mostra o arquivo em vermelho: modified, modificado.",
     termo("Mudou um arquivo: aparece em vermelho", [{"cmd": "git status"}, {"out": "Changes not staged for commit:", "cor": "txt"}, {"out": "        modified:   tests/compra.spec.js", "cor": VERM}], fonte=26, fonte_min=22)),
    ("Aí é o mesmo ciclo: git add ponto, git commit com uma legenda que diz o que mudou. E o git log já mostra duas fotos.",
     termo("O mesmo ciclo: add, commit, e a história cresce", [{"cmd": "git add ."}, {"cmd": "git commit -m \"confere a mochila no carrinho\""}, {"out": "[master 7f3a2c1] confere a mochila no carrinho", "cor": "ac"},
                                                             {"out": " 1 file changed, 1 insertion(+)", "cor": "mut"}, {"cmd": "git log --oneline"}, {"out": "7f3a2c1 confere a mochila no carrinho", "cor": "ac"},
                                                             {"out": "24d5d51 meu primeiro projeto Playwright", "cor": "ac"}], fonte=26, fonte_min=22)),
    ("E a legenda importa. Ajustes, ou teste, não diz nada. Daqui a um mês, você não lembra. Adiciona teste do carrinho, ou corrige o seletor do login, diz exatamente o que mudou.",
     {"type": "traducao", "titulo": "UMA BOA LEGENDA", "linhas": [["\"ajustes\"  /  \"teste\"", "não diz nada"], ["\"adiciona teste do carrinho\"", "diz o que mudou"], ["\"corrige o seletor do login\"", "diz o que mudou"]]}),
    ("E se você estragou um arquivo e quer ele de volta, do jeito que estava na última foto? Git restore, e o nome do arquivo. Cuidado: o que você mudou desde a última foto se perde.",
     termo("restore = volta o arquivo pra última foto", [{"cmd": "git restore tests/compra.spec.js"}], fonte=30, fonte_min=24)),
    ("Quando fazer um commit? Sempre que uma coisa ficou pronta e funcionando. Terminou um teste e ele passou: commit. Assim, se algo quebrar depois, você tem um ponto salvo bom pra voltar.",
     {"type": "cards", "titulo": "QUANDO SALVAR", "itens": [["✓", "O teste passou?", "commit"], ["🧩", "Uma parte pronta?", "commit", "#69a7ff"], ["⚠", "Vai mexer em algo grande?", "commit antes", "#ffd23f"]]}),
    ("Resumindo os comandos: git init, uma vez por projeto. Git status, o que mudou. Git add ponto, prepara. Git commit traço m, a foto com a legenda. E git log, a história.",
     {"type": "traducao", "titulo": "OS COMANDOS DO GIT", "em_frac": [0.12, 0.3, 0.46, 0.62, 0.82], "linhas": [["git init", "uma vez por projeto"], ["git status", "o que mudou (vermelho e verde)"], ["git add .", "prepara tudo pra foto"],
                                                                                 ["git commit -m \"...\"", "tira a foto, com a legenda"], ["git log --oneline", "a história do projeto"]]}),
    ("Pronto: o seu projeto tem a história dele guardada. Na próxima aula, ela vai pro GitHub, na internet.", {"type": "passo", "icone": "▶", "titulo": "Próxima aula", "sub": "GitHub: enviando o projeto"}),
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
    ("Por que isso importa? Sem ele, alguém precisa lembrar de rodar os testes. Com ele, toda vez que alguém manda uma mudança pro repositório, os testes rodam sozinhos.", {"type": "compare", "title": "RODAR OS TESTES", "items": [["SEM ACTIONS", "ALGUÉM PRECISA LEMBRAR", "white"], ["COM ACTIONS", "RODA A CADA MUDANÇA", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),  # pra que / quando
    ("E em muitas empresas, os testes ficam junto com o código do site. Aí cada mudança no site passa pelos testes antes de chegar no cliente.",
     {"type": "cards", "itens": [["✎", "Alguém muda o site", "e manda pro repositório"], ["▶", "Os testes rodam", "sozinhos", "#69a7ff"], ["✓", "Passou?", "aí chega no cliente", "#3fd68a"]]}),
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
    ("Agora o yml precisa entregar esses segredos pros testes. Só que esse arquivo já está no GitHub: ele subiu junto com o projeto, na aula quarenta e quatro. Então, onde mudar?",
     bt(("O ARQUIVO JÁ ESTÁ NO GITHUB", "white", 100), ("ONDE MUDAR?", "gold", 120))),
    ("Dá pra editar direto no site do GitHub, no lapisinho do arquivo. Mas aí o seu computador fica com a versão antiga. O jeito recomendado: muda no VS Code, e manda pro GitHub com o ciclo da aula quarenta e três. Assim, os dois ficam iguais.",
     {"type": "compare", "title": "ONDE MUDAR O ARQUIVO", "items": [["NO SITE DO GITHUB", "SEU COMPUTADOR FICA DESATUALIZADO", "white"], ["NO VS CODE + PUSH", "OS DOIS FICAM IGUAIS", "gold"]], "size": 80, "stagger": 1.8, "vs": False}),
    ("Então, no VS Code, abre o playwright ponto yml. No passo que roda os testes, escreve um env que entrega esses segredos pros testes.",
     edc(YML, "env: os segredos entregues aos testes", arquivo="playwright.yml", pastas=ARV_AUTH, digitar=True, digitar_de=L_ENV, digitar_ate=L_ENV + 2, rolar=True, rolar_de=0.6, rolar_dur=0.9, fonte=22)),
    ("Traduzindo: SAUCE USER, dois pontos, e cifrão chaves chaves secrets ponto SAUCE USER. Pegue o valor guardado no cofre do GitHub, e entregue pros testes com esse nome, igual o ponto env fazia.",
     {"type": "traducao", "titulo": "DO COFRE PROS TESTES", "linhas": [["SAUCE_USER: ${{ secrets.SAUCE_USER }}", "o usuário, do cofre"], ["SAUCE_PASSWORD: ${{ secrets.SAUCE_PASSWORD }}", "a senha, do cofre"]]}),
    ("Agora manda a mudança pro GitHub, com o ciclo de sempre. Git status: o yml aparece em vermelho, modificado. Git add ponto. Git commit, com uma legenda que diz o que mudou. E git push, que manda pro GitHub.",
     termo("O ciclo: status, add, commit e push", [{"cmd": "git status"}, {"out": "        modified:   .github/workflows/playwright.yml", "cor": VERM}, {"cmd": "git add ."},
                                                   {"cmd": "git commit -m \"entrega os secrets pros testes\""}, {"out": "[main 3b9e0d4] entrega os secrets pros testes", "cor": "ac"}, {"out": " 1 file changed, 3 insertions(+)", "cor": "mut"},
                                                   {"cmd": "git push"}, {"out": "To https://github.com/voce/meu-primeiro-playwright.git", "cor": "mut"}, {"out": "   24d5d51..3b9e0d4  main -> main", "cor": "ac"}], fonte=26, fonte_min=20)),
    ("E aqui vem a mágica: esse push é justamente o gatilho do arquivo. Abre a aba Actions no GitHub: olha os testes rodando lá, sozinhos.", dict(GHA, inicio_em=1.0, legenda="O push disparou os testes no GitHub")),
    ("Verde: passou. E no fim tem o relatório pra baixar, porque esse arquivo tem o passo que guarda ele.", dict(GHA, pronto=True, status="ok", artefato="playwright-report", legenda="Passou · o relatório pra baixar")),
    ("E se um dia alguém mudar um arquivo direto no site do GitHub, ou outra pessoa da equipe mandar uma mudança? No seu computador, git pull: puxe as mudanças de lá pra cá. Push manda, pull traz.",
     {"type": "traducao", "titulo": "PUSH E PULL", "linhas": [["git push", "manda do seu computador pro GitHub"], ["git pull", "traz do GitHub pro seu computador"]]}),
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

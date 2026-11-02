"""Gera projetos/curso-playwright-55..63 (nível 2 · módulo 12: um site que você nunca viu). Roteiro: curso-playwright/roteiros/nivel2.md.
Código = curso-playwright/projeto/tests/nivel2/internet.spec.js (validado no Actions: validar_nivel2.yml), sem o "aula NN:" dos títulos.
Vídeos reais: as páginas do the-internet gravadas pelo midia.py; o alerta, a aba nova, o hover e a tabela mudando de ordem
gravados com o Chromium de verdade numa tela virtual (ferramentas/codegen/nivel2.sh), em projetos/<aula>/midia/."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import inteiro, bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m4 import edc

SITE = "https://the-internet.herokuapp.com"
COD = re.sub(r"aula \d+: ", "", open(os.path.join(RAIZ, "curso-playwright", "projeto", "tests", "nivel2", "internet.spec.js"), encoding="utf8").read().rstrip("\n"))
L = COD.split("\n")
ARV_COM = ["meu-primeiro-playwright", "  arquivos/", "    exemplo.txt", "  pages/", "  tests/", "    compra.spec.js", "    internet.spec.js", "    login.spec.js", "  .env", "  playwright.config.js"]
ARV = [l for l in ARV_COM if "arquivos" not in l and "exemplo" not in l]  # a pasta arquivos só nasce na aula 57 (upload)
AZUL, AMARELO, VERM, VERDE = "#69a7ff", "#ffd23f", "#ff6b6b", "#3fd68a"


def ln(trecho, n=1):
    achou = [i + 1 for i, l in enumerate(L) if trecho in l]
    return achou[n - 1]


def bloco(nome):
    """linhas (de, até) do test com esse nome"""
    a = ln(f"test('{nome}'"); b = a
    while L[b - 1] != "});":
        b += 1
    return a, b


def ate(n):
    """o arquivo até a linha n (o que o aluno tem escrito naquele momento)"""
    return "\n".join(L[:n])


def ed(legenda, n_fim, de=None, ate_l=None, mostra_de=None, **kw):
    """o internet.spec.js no editor: mostra do 'mostra_de' até 'n_fim', digitando de..ate_l"""
    m0 = mostra_de or 1
    cod = "\n".join(L[m0 - 1:n_fim])
    larg = max(len(l) for l in cod.split("\n"))
    d = dict(arquivo="internet.spec.js", fonte=32 if larg <= 56 else 28, linha0=m0)
    d["pastas"] = ARV if larg <= 52 else None  # linha comprida: sem o explorer, a letra fica grande
    if de:
        d.update(digitar=True, digitar_de=de - m0 + 1, digitar_ate=(ate_l or de) - m0 + 1)
    d.update(kw)
    if m0 > 1:  # o arquivo inteiro: aparece do topo e desce até o trecho
        return inteiro(edc(cod, legenda, **d), L[:m0 - 1])
    return edc(cod, legenda, **d)


def devi(media, caminho, sel, attr, rotulo, legenda, acoes=()):
    """DevTools de verdade no the-internet: botão direito › Inspecionar (de onde vem o seletor)"""
    return {"type": "devtools", "media": media, "url": SITE + caminho, "acoes": list(acoes), "inspecionar": sel, "titulo": "the-internet.herokuapp.com" + caminho,
            "attrs": ["id", "class", "type", "name"], "realce": [attr], "realce_em": 4.0, "realce_rotulo": rotulo, "legenda": legenda}


def tr(codigo, partes, passo=1.4):
    return {"type": "traducao", "codigo": codigo, "partes": partes, "passo": passo}


def video(media, legenda, url=None, acoes=(), **kw):
    """vídeo real: gravado agora pelo midia.py (url + ações) ou já pronto em midia/ (gravação da tela virtual)"""
    d = {"type": "tela_cheia", "media": media, "legenda": legenda, "gravar": True} if not url else \
        {"type": "tela", "media": media, "url": url, "gravar": True, "acoes": list(acoes), "titulo": "the-internet.herokuapp.com", "legenda": legenda,
         "espera_inicio": 1000, "espera_fim": 1600, "delay_letra": 60}
    d.update(kw)
    return d


def tarefa(rotulo, texto, cor=AMARELO):
    return bt((rotulo, "muted", 70), ("“" + texto + "”", "white", 78 if len(texto) < 34 else 64), entre=1.3)


def roda(nome, grep, legenda, url=None, acoes=(), media=None, seg="3.1s", extra=None):
    """VS Code com o teste em cima, o comando no terminal e o navegador real por cima"""
    a, b = bloco(nome)
    nav = {"media": media or f"run_{grep.split()[0]}", "titulo": "Chromium", "em": 0.1, "ate": 0.86}
    if url:
        nav.update({"url": url, "gravar": True, "acoes": list(acoes), "espera_inicio": 900, "espera_fim": 1600, "delay_letra": 55})
    nav.update(extra or {})
    term = [{"cmd": f'npx playwright test internet -g "{grep}" --headed --project=chromium', "em": 0.03},
            {"out": "Running 2 tests using 1 worker", "cor": "mut", "em": 0.08}, {"out": f"  2 passed ({seg})", "cor": "ac", "em": 0.88}]
    cod = "\n".join(L[a - 1:min(b, a + 8)])
    return edc(cod, legenda, arquivo="internet.spec.js", linha0=a, terminal=term, navegador=nav, fonte=26, pastas=None)


def fim(prox):
    return [("Te vejo na próxima!", {"type": "endcard", "sub": "PRÓXIMA: " + prox.upper()})]


AULAS = []


def aula(n, titulo_aula, frases):
    AULAS.append(projeto(n, f"MÓDULO 12 · AULA {n}", titulo_aula, frases))


def home(media, link, legenda, depois=(), **kw):
    """vídeo real: a página inicial do the-internet, o clique no link da tela, e o que a gente faz nela"""
    return video(media, legenda, url=SITE, acoes=[{"espera": 900}, {"click": f"a[href='{link}']", "espera": 1500}] + list(depois), espera_fim=2000, **kw)


def plano(titulo_p, itens):
    cores = [None, AZUL, AMARELO, VERDE]
    return {"type": "cards", "titulo": titulo_p, "itens": [[str(i + 1), t, s] + ([cores[i % 4]] if cores[i % 4] else []) for i, (t, s) in enumerate(itens)]}


# ---------- 55 ----------
L_SITE = ln("const site")
aula(55, "Bem-vindo ao nível 2", [
    ("Até aqui você aprendeu Playwright praticamente do zero. Agora o nível sobe um pouco.", bt(("NÍVEL 2", "gold", 210), ("O NÍVEL SOBE", "white", 110))),
    ("Nos próximos módulos, eu quero te colocar em situações que aparecem quando você começa a automatizar sistemas reais.",
     {"type": "cards", "itens": [["🌐", "Site novo", "que você nunca viu"], ["🧩", "Problemas novos", "do dia a dia", AZUL], ["🛠", "Recursos novos", "do Playwright", AMARELO], ["📁", "Projeto novo", "do zero", VERDE]]}),
    ("E pra isso a gente sai um pouco do saucedemo. Vamos usar o the internet: um site de treino, feito justamente pra praticar automação. No navegador, the internet ponto herokuapp ponto com.",
     video("n55_site2", "the-internet.herokuapp.com", url=SITE, acoes=[{"espera": 1500}])),
    ("A página inicial é uma lista de links. Cada link leva pra uma tela diferente, com uma situação que aparece em sistema de verdade: uma caixinha de marcar, um arquivo pra enviar, um alerta, uma aba nova, uma tabela.",
     video("n55_lista", "Cada link é uma tela diferente", url=SITE, acoes=[{"scroll": 500, "espera": 1200}, {"scroll": 600, "espera": 1200}, {"scroll": -1100, "espera": 800}])),
    ("Em cada aula, a gente abre uma dessas telas, olha o que tem nela, faz na mão, e só depois automatiza.",
     plano("EM CADA AULA", [("Abre a tela", "pelo link da página inicial"), ("Faz na mão", "pra entender a tela"), ("Automatiza", "linha por linha")])),
    ("A ideia vai ser sempre: apareceu um problema novo, a gente descobre como resolver.", bt(("APARECEU UM PROBLEMA", "white", 100), ("A GENTE DESCOBRE", "gold", 120), ("COMO RESOLVER", "gold", 120))),
    ("Primeiro, o import de sempre.",
     ed("O import de sempre", 1, de=1, ate_l=1, criar_arvore=ARV,
        criar=[["Todos os testes desse site vão num arquivo só. Dentro da pasta tests, cria o arquivo internet ponto spec ponto js.", "internet.spec.js"]])),
    ("Agora um detalhe. Lembra do baseURL, no config? Ele guarda o endereço do saucedemo. Por isso, até agora, o goto só precisava da barra. Só que o the internet é outro endereço.",
     {"type": "traducao", "titulo": "O BASEURL É DO SAUCEDEMO", "linhas": [["baseURL no config", "saucedemo.com"], ["the internet", "outro endereço"]]}),
    ("Então a gente guarda o endereço do the internet numa constante chamada site: const site, igual, e entre aspas o endereço completo.",
     ed("const site = o endereço do the internet", L_SITE, de=L_SITE, ate_l=L_SITE)),
    ("E em cada teste, o goto junta esse endereço com o nome da tela, usando a crase da aula trinta e dois. Assim: o site, e barra checkboxes.",
     tr("page.goto(`${site}/checkboxes`)", [["${site}", "o endereço do the internet"], ["/checkboxes", "o nome da tela"]], 1.8)),
    ("Vamos começar com uma coisa que aparece em quase todo formulário.", {"type": "passo", "icone": "▶", "titulo": "Próxima aula", "sub": "O formulário mudou"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: O FORMULÁRIO MUDOU"}),
])

# ---------- 56 ----------
a, b = bloco("checkbox e dropdown")
CHK1 = "#checkboxes input >> nth=0"
aula(56, "O formulário mudou", [
    ("Imagina que caiu uma tarefa nova: validar as preferências de um formulário. Sabe aquelas caixinhas de aceito os termos e receber novidades por e-mail? E aquela lista pra escolher uma opção?",
     tarefa("NOVA TAREFA", "Validar as preferências do formulário")),
    ("No the internet tem uma tela pra cada uma. Na página inicial, clica em Checkboxes.", home("n56_home", "/checkboxes", "Página inicial › Checkboxes")),
    ("Olha a tela: duas caixinhas. A primeira vem desmarcada, a segunda vem marcada. Clicando, ela marca. Clicando de novo, desmarca.",
     video("n56_check3", "Clicou: marca · clicou de novo: desmarca", url=SITE + "/checkboxes", acoes=[{"espera": 5600}, {"check": CHK1, "espera": 1600}, {"uncheck": CHK1, "espera": 2000}])),
    ("Essa caixinha se chama checkbox, caixa de marcar. E o teste vai fazer o mesmo que a gente fez na mão: marcar a primeira, conferir que marcou, desmarcar, e conferir que desmarcou.",
     plano("O TESTE, EM PORTUGUÊS", [("Marca", "a primeira: check"), ("Confere", "marcada: expect"), ("Desmarca", "uncheck"), ("Confere", "desmarcada: expect")])),
    ("No internet ponto spec, um teste novo: checkbox e dropdown. A primeira linha dentro dele abre a tela: page ponto goto, com o site e barra checkboxes.",
     ed("O goto da tela Checkboxes", a + 1, de=a, ate_l=a + 1, mostra_de=a)),
    ("Como achar a caixinha? Botão direito nela, e Inspecionar: é um input do tipo checkbox. E repara: ela não tem id, nem data-test.",
     devi("dev56_chk", "/checkboxes", CHK1, "type", "type=\"checkbox\"", "Inspecionar: input type=\"checkbox\", sem id")),
    ("Sem id, a gente procura pela função: get by role checkbox, as caixas de marcar. E como são duas, ponto first: a primeira.",
     ed("A primeira caixa de marcar", a + 2, de=a + 2, ate_l=a + 2, mostra_de=a)),
    ("Traduzindo: const primeira, guarde com o nome primeira. Get by role checkbox, as caixas de marcar. Ponto first, a primeira.",
     tr("const primeira = page.getByRole('checkbox').first();", [["const primeira", "guarde com o nome primeira"], ["getByRole('checkbox')", "as caixas de marcar"], [".first()", "a primeira"]], 1.8)),
    ("Agora a ação: primeira ponto check. Check quer dizer marque. E não basta marcar: a gente confere. Expect primeira, to be checked: eu espero que a primeira esteja marcada.",
     ed("check = marque · toBeChecked = esteja marcada", a + 4, de=a + 3, ate_l=a + 4, mostra_de=a)),
    ("Depois, o contrário: uncheck, desmarque. E na conferência, o not na frente: eu espero que ela não esteja marcada.",
     ed("uncheck = desmarque · not = não", a + 6, de=a + 5, ate_l=a + 6, mostra_de=a)),
    ("Agora a segunda parte da tarefa. Volta na página inicial e clica em Dropdown.", home("n56_home_dd", "/dropdown", "Página inicial › Dropdown")),
    ("É uma caixa que abre uma lista: Option 1 e Option 2. A pessoa escolhe uma, e ela fica selecionada. Igual à caixa de ordenar do desafio quatro.",
     video("n56_dd3", "A lista de opções", url=SITE + "/dropdown", acoes=[{"espera": 3500}, {"select": ["#dropdown", "1"], "espera": 1500}, {"select": ["#dropdown", "2"], "espera": 2000}])),
    ("E o seletor da lista? Botão direito nela, e Inspecionar: id igual dropdown. No código, o id vai com uma cerquilha na frente.",
     devi("dev56", "/dropdown", "#dropdown", "id", "#dropdown", "Inspecionar: id=\"dropdown\" vira #dropdown")),
    ("No teste, uma linha em branco pra separar, o goto da tela do dropdown, e const lista igual page ponto locator, cerquilha dropdown.",
     ed("O goto do Dropdown e a lista", a + 9, de=a + 8, ate_l=a + 9, mostra_de=a)),
    ("A ação, com o select option do desafio quatro: escolha a opção dois. E a conferência: to have value, eu espero que a lista tenha o valor dois.",
     ed("selectOption = escolha · toHaveValue = tenha o valor", b, de=a + 10, ate_l=a + 11, mostra_de=a)),
    ("E por que o valor, e não o texto? O texto é o que a pessoa vê na tela. O valor é o que vai pro sistema quando ela salva. E é ele que precisa estar certo.",
     {'type': 'traducao', 'titulo': 'TEXTO × VALOR', 'linhas': [['Option 2', 'o que a pessoa vê'], ['value="2"', 'o que vai pro sistema']]}),
    ("Roda e olha: marcou, desmarcou, e escolheu a opção dois. Passou.",
     roda("checkbox e dropdown", "checkbox", "Marcou, desmarcou e escolheu", url=SITE + "/checkboxes",
          acoes=[{"check": CHK1, "espera": 700}, {"uncheck": CHK1, "espera": 700}, {"goto": SITE + "/dropdown", "espera": 600}, {"select": ["#dropdown", "2"], "espera": 900}], seg="3.4s")),
    ("No trabalho, isso aparece em quase todo cadastro: aceitar os termos de uso, receber novidades por e-mail, escolher o estado ou a cidade.", {'type': 'cards', 'itens': [['☑', 'Aceito os termos', 'checkbox'], ['☑', 'Receber novidades', 'checkbox', '#69a7ff'], ['▾', 'Estado e cidade', 'lista de opções', '#ffd23f']], 'titulo': 'EM QUASE TODO CADASTRO'}),
] + fim("upload de arquivo"))

# ---------- 57 ----------
a, b = bloco("upload de arquivo"); ARV = ARV_COM
aula(57, "O usuário precisa enviar um arquivo", [
    ("A tarefa mudou: o usuário precisa conseguir anexar um documento. Currículo, comprovante, planilha.", tarefa("NOVA TAREFA", "O usuário precisa anexar um documento")),
    ("No the internet, a tela é a File Upload. Na página inicial, clica nela.", home("n57_home", "/upload", "Página inicial › File Upload")),
    ("Na tela tem um botão Choose File, escolher arquivo, que abre a janela do computador pra procurar o arquivo. E o botão Upload, que envia. Depois de enviar, a página mostra o nome do arquivo.",
     video("n57_tela3", "Escolhe · envia · o nome aparece", url=SITE + "/upload",
           acoes=[{"espera": 4800}, {"upload": ["#file-upload", "curso-playwright/projeto/arquivos/exemplo.txt"], "espera": 1800}, {"click": "#file-submit", "espera": 3000}])),
    ("O teste vai fazer igual: escolher um arquivo, clicar em Upload, e conferir que o nome dele apareceu.",
     plano("O TESTE, EM PORTUGUÊS", [("Escolhe", "o arquivo: setInputFiles"), ("Envia", "clica em Upload"), ("Confere", "o nome apareceu")])),
    ("Dentro, qualquer texto. Esse é o arquivo que o teste vai enviar.",
     edc("Meu currículo de testador", "arquivos/exemplo.txt", arquivo="exemplo.txt", pastas=ARV, digitar=True, digitar_de=1, digitar_ate=1, fonte=30,
         criar=[["Mas pra enviar um arquivo, o teste precisa ter um arquivo. Na pasta do projeto, cria uma pasta nova chamada arquivos.", "arquivos/"], ["E dentro dela, um arquivo de texto: exemplo ponto txt.", "exemplo.txt"]])),
    ("No internet ponto spec, um teste novo: upload de arquivo. Primeiro, o goto da tela de upload.", ed("O goto da tela de upload", a + 1, de=a, ate_l=a + 1, mostra_de=a)),
    ("E o campo, no Inspecionar: um input do tipo file, com id igual file upload. E o botão Upload tem o id file submit.",
     devi("dev57", "/upload", "#file-upload", "id", "#file-upload", "Inspecionar: id=\"file-upload\"")),
    ("Agora a ação nova: o campo file upload, ponto set input files, e entre parênteses o caminho do arquivo: arquivos barra exemplo ponto txt.",
     ed("setInputFiles = coloque este arquivo", a + 3, de=a + 2, ate_l=a + 3, mostra_de=a)),
    ("Traduzindo: set input files, coloque este arquivo no campo. E o caminho começa na pasta do projeto: a pasta arquivos, e o exemplo ponto txt.",
     tr(".setInputFiles('arquivos/exemplo.txt')", [[".setInputFiles", "coloque no campo"], ["('arquivos/exemplo.txt')", "a partir da pasta do projeto"]], 1.8)),
    ("Repara: o Playwright não abre aquela janela do Windows pra procurar o arquivo com o mouse. Ele entrega o arquivo direto pro campo.",
     {"type": "cards", "itens": [["✗", "Sem janela do Windows", "nada de procurar com o mouse", VERM], ["✓", "Direto no campo", "o arquivo vai pronto", VERDE]]}),
    ("Depois, clica no botão Upload. E confere: a área uploaded files, onde o nome aparece, contém o texto exemplo ponto txt.",
     ed("O nome do arquivo apareceu", b, de=a + 4, ate_l=b - 1, mostra_de=a)),
    ("Roda: escolheu, enviou, e o nome apareceu.", roda("upload de arquivo", "upload", "O arquivo subiu", url=SITE + "/upload",
                   acoes=[{"upload": ["#file-upload", "curso-playwright/projeto/arquivos/exemplo.txt"], "espera": 900}, {"click": "#file-submit", "espera": 1400}], seg="3.2s")),
    ("No dia a dia, também vale testar o lado ruim: um arquivo grande demais, ou de um formato que o sistema não aceita. Ele tem que recusar com uma mensagem clara.", {'type': 'cards', 'itens': [['✓', 'Arquivo certo', 'sobe e aparece'], ['⚖', 'Grande demais', 'recusa e avisa', '#ffd23f'], ['✗', 'Formato errado', 'recusa e avisa', '#ff6b6b']], 'titulo': 'OS DOIS LADOS DO UPLOAD'}),
] + fim("uma caixa travou a página"))

# ---------- 58 ----------
a, b = bloco("alerta do navegador")
aula(58, "Uma caixa travou a página", [
    ("Agora, uma coisa diferente. Na página inicial, clica em JavaScript Alerts.", home("n58_home", "/javascript_alerts", "Página inicial › JavaScript Alerts")),
    ("Clica no primeiro botão, Click for JS Alert: o navegador abriu essa caixa, com um OK.", video("n58_alerta", "O alerta do navegador")),
    ("Enquanto ela está aberta, não dá pra usar a página: alguém tem que clicar em OK. Isso é um alerta do navegador, e no Playwright ele se chama dialog.",
     {"type": "cards", "titulo": "DIALOG", "itens": [["⚠", "A caixa do navegador", "com um OK"], ["⛔", "Trava a página", "até alguém clicar", VERM]]}),
    ("Depois do OK, aparece uma mensagem embaixo. No Inspecionar: um parágrafo, com id igual result.",
     devi("dev58", "/javascript_alerts", "#result", "id", "#result", "Inspecionar: id=\"result\"", [{"click": "button:has-text('Click for JS Alert')"}])),
    ("O teste: avisar o Playwright pra clicar em OK quando o alerta aparecer, clicar no botão, e conferir a mensagem.",
     plano("O TESTE, EM PORTUGUÊS", [("Avisa", "alerta? clica em OK"), ("Clica", "no botão"), ("Confere", "a mensagem")])),
    ("Um teste novo, alerta do navegador, com o goto da tela de alertas.", ed("O goto da tela de alertas", a + 1, de=a, ate_l=a + 1, mostra_de=a)),
    ("Agora a parte nova. Antes de clicar, a gente prepara o Playwright: page ponto on, entre aspas dialog, e uma função que recebe o dialog e faz dialog ponto accept.",
     ed("page.on('dialog') = quando aparecer um alerta", a + 4, de=a + 2, ate_l=a + 4, mostra_de=a)),
    ("Traduzindo: page on dialog, quando aparecer um alerta. Dialog accept, clique em OK.",
     tr("page.on('dialog', ... dialog.accept())", [["page.on('dialog'", "quando aparecer um alerta"], ["dialog.accept()", "clique em OK"]], 1.6)),
    ("A ordem é importante: primeiro prepara, depois clica. É como deixar um recado: quando o alerta chegar, clica em OK.",
     {"type": "cards", "titulo": "A ORDEM", "itens": [["1", "Prepara", "page.on('dialog')"], ["2", "Clica", "no botão", AZUL], ["3", "Aparece", "o alerta", AMARELO], ["4", "Aceita", "sozinho", VERDE]]}),
    ("Agora sim, o clique: get by role button, um botão com o nome Click for JS Alert. E a conferência: o result tem o texto You successfully clicked an alert.",
     ed("O clique e a mensagem do resultado", b, de=a + 5, ate_l=b - 1, mostra_de=a)),
    ("Roda.", roda("alerta do navegador", "alerta", "Preparou, clicou e aceitou", media="n58_alerta", seg="3.3s")),
    ("E sem esse preparo? O Playwright cancela o alerta sozinho, e o teste segue em frente como se nada tivesse acontecido.", {'type': 'cards', 'itens': [['⚙', 'Sem o page.on', 'o Playwright cancela sozinho', '#ff6b6b'], ['✓', 'Com o page.on', 'você decide o que fazer', '#3fd68a']]}),
    ("No trabalho, o mais comum é o tem certeza que quer excluir? E aí dá pra testar os dois lados: accept, confirma. Dismiss, cancela, e nada pode ser apagado.", {'type': 'traducao', 'titulo': 'TEM CERTEZA QUE QUER EXCLUIR?', 'linhas': [['dialog.accept()', 'confirma: apagou'], ['dialog.dismiss()', 'cancela: nada foi apagado']]}),
] + fim("o link abriu outra aba"))

# ---------- 59 ----------
a, b = bloco("nova aba")
aula(59, "O link abriu outra aba", [
    ("Imagina: você clica pra ver os detalhes de um pedido, e eles abrem em outra aba. E o teste continua olhando a aba antiga.", tarefa("NOVA TAREFA", "Os detalhes abrem em outra aba")),
    ("No the internet, essa tela é a Multiple Windows. Na página inicial, clica nela.", home("n59_home", "/windows", "Página inicial › Multiple Windows")),
    ("Tem um link: Click Here. Clicando, abre uma aba nova, escrito New Window.", video("n59_aba", "Click Here abre outra aba")),
    ("O problema: o page é a aba que o teste abriu. A aba nova é outra. Se o teste continuar olhando o page, ele nunca vê o New Window.",
     {"type": "cards", "itens": [["⧉", "Abriu outra aba", ""], ["👀", "O page olha a antiga", "", VERM], ["✓", "Pega a nova", "quando ela abrir", VERDE]]}),
    ("O teste: avisar que uma aba nova vai abrir, clicar no link, pegar a aba nova, e conferir o título dela.",
     plano("O TESTE, EM PORTUGUÊS", [("Avisa", "vai abrir uma aba"), ("Clica", "no link"), ("Pega", "a aba nova"), ("Confere", "o título")])),
    ("Um teste novo, nova aba, com o goto da tela windows.", ed("O goto da tela windows", a + 1, de=a, ate_l=a + 1, mostra_de=a)),
    ("Primeiro, o aviso: const promessa igual page ponto wait for event, popup. Popup é o nome que o Playwright dá pra uma aba ou janela nova.",
     ed("waitForEvent('popup') = espere uma nova aba", a + 2, de=a + 2, ate_l=a + 2, mostra_de=a)),
    ("Espere uma nova aba.", tr("page.waitForEvent('popup')", [["waitForEvent", "espere acontecer"], ["('popup')", "uma nova aba"]], 1.0)),
    ("Por que avisar antes de clicar? Porque a aba nova abre muito rápido. Se você só começar a esperar depois do clique, ela pode já ter aberto, e o teste fica esperando pra sempre.", {'type': 'cards', 'itens': [['1', 'Primeiro, o aviso', 'espere uma aba nova'], ['2', 'Depois, o clique', 'a aba abre', '#69a7ff'], ['3', 'Aí, pega a aba', 'await promessa', '#ffd23f']], 'titulo': 'A ORDEM'}),
    ("Agora o clique: get by role link, um link com o nome Click Here. E aí: const nova aba igual await promessa. O await espera a aba abrir, e guarda ela com o nome nova aba.",
     ed("novaAba = a aba que abriu", a + 4, de=a + 3, ate_l=a + 4, mostra_de=a)),
    ("A partir daí, a nova aba funciona igual ao page. Nela, o título New Window, com get by role heading. Heading é título. E confere que ele está visível.",
     ed("heading = título", b, de=a + 5, ate_l=b - 1, mostra_de=a)),
    ("Roda e olha as duas abas.", roda("nova aba", "nova aba", "Abriu e conferiu a aba nova", media="n59_aba", seg="3.0s")),
    ("No dia a dia, isso aparece em link de pagamento, termos de uso, nota fiscal em PDF, e em login com conta de outro site, que abre numa janela separada.", {'type': 'cards', 'itens': [['💳', 'Pagamento', 'abre em outra aba'], ['📄', 'PDF e termos', 'abrem em outra aba', '#69a7ff'], ['🔑', 'Login com outra conta', 'janela separada', '#ffd23f']]}),
] + fim("uma página dentro da página"))

# ---------- 60 ----------
a, b = bloco("iframe")
aula(60, "Tem uma página dentro da página", [
    ("Na página inicial, clica em Frames. E depois, em iFrame.",
     video("n60_home", "Página inicial › Frames › iFrame", url=SITE, acoes=[{"espera": 900}, {"click": "a[href='/frames']", "espera": 1300}, {"click": "a[href='/iframe']", "espera": 1600}], espera_fim=2000)),
    ("Olha essa tela: um editor de texto no meio, escrito Your content goes here. Só que, se você procurar esse texto do jeito normal, o Playwright não acha nada.",
     video("n60_iframe", "Um editor no meio da página", url=SITE + "/iframe", espera_fim=3000)),
    ("Por quê? Porque aquele quadro é outra página, encaixada dentro desta, como uma janelinha. Isso se chama iframe. E o Playwright só procura lá dentro se você mandar.",
     {"type": "cards", "titulo": "IFRAME", "itens": [["▭", "A página", "the-internet"], ["▣", "O iframe", "outra página dentro", AZUL], ["✎", "O editor", "lá dentro", AMARELO]]}),
    ("E o seletor do quadro? Botão direito no editor, e Inspecionar: é um iframe, com id igual mce zero ifr.",
     devi("dev60", "/iframe", "#mce_0_ifr", "id", "#mce_0_ifr", "Inspecionar: iframe com id=\"mce_0_ifr\"")),
    ("A lógica: entrar no iframe, procurar o elemento, conferir.", {"type": "cards", "itens": [["1", "Entra no iframe", "frameLocator"], ["2", "Procura", "o elemento", AZUL], ["3", "Confere", "expect", VERDE]]}),
    ("Um teste novo, iframe, com o goto da tela iframe.", ed("O goto da tela iframe", a + 1, de=a, ate_l=a + 1, mostra_de=a)),
    ("Agora, você diz em qual quadro procurar: const editor igual page ponto frame locator, e o id do iframe, com a cerquilha.",
     ed("frameLocator = procure dentro deste quadro", a + 2, de=a + 2, ate_l=a + 2, mostra_de=a)),
    ("Procure dentro deste quadro.", tr("page.frameLocator('#mce_0_ifr')", [["frameLocator", "procure dentro do quadro"], ["('#mce_0_ifr')", "este quadro"]], 1.0)),
    ("Lá dentro, o body. Body é o corpo da página, onde fica o texto. E a conferência: contém Your content goes here.",
     ed("body = o corpo da página de dentro", b, de=a + 3, ate_l=b - 1, mostra_de=a)),
    ("Traduzindo: editor locator body, o corpo da página de dentro do quadro. To contain text, contém este texto.",
     tr("editor.locator('body')  ·  toContainText(...)", [["editor.locator('body')", "o corpo da página de dentro"], ["toContainText", "contém este texto"]], 1.6)),
    ("Roda.", roda("iframe", "iframe", "Achou o texto lá dentro", url=SITE + "/iframe", acoes=[{"espera": 1500}], seg="3.6s")),
    ("No trabalho, o caso mais comum é o pagamento: o campo do cartão quase sempre é um iframe, de outra empresa, por segurança. Também aparece em vídeo, mapa e chat de atendimento.", {'type': 'cards', 'itens': [['💳', 'Campo do cartão', 'quase sempre iframe'], ['▶', 'Vídeo e mapa', 'iframe', '#69a7ff'], ['💬', 'Chat de atendimento', 'iframe', '#ffd23f']], 'titulo': 'ONDE TEM IFRAME'}),
] + fim("o botão só aparece com o mouse"))

# ---------- 61 ----------
a, b = bloco("hover")
aula(61, "O botão só aparece quando passo o mouse", [
    ("Chegou um relato de bug: não consigo clicar na opção, porque ela só aparece quando passo o mouse no usuário.", tarefa("RELATO DE BUG", "Só aparece quando passo o mouse", VERM)),
    ("Vamos reproduzir. Na página inicial, clica em Hovers.", home("n61_home", "/hovers", "Página inicial › Hovers")),
    ("Tem três fotos de usuário. Sem o mouse em cima, só a foto. Passando o mouse, aparece o nome embaixo: name user1.", video("n61_hover", "Com o mouse em cima, o nome aparece")),
    ("Passar o mouse por cima, em inglês, é hover. E no Playwright, é exatamente esse o comando.", tr("await usuario.hover();", [["usuario", "o usuário"], [".hover()", "passe o mouse por cima"]], 1.0)),
    ("O teste: conferir que o nome está escondido, passar o mouse na primeira foto, e conferir que o nome apareceu.",
     plano("O TESTE, EM PORTUGUÊS", [("Confere", "nome escondido"), ("Hover", "passa o mouse"), ("Confere", "nome visível")])),
    ("E o usuário, no Inspecionar: cada foto fica numa caixa com a classe figure. No código, classe vai com um ponto na frente: ponto figure.",
     devi("dev61", "/hovers", ".figure", "class", ".figure", "Inspecionar: class=\"figure\" vira .figure")),
    ("Um teste novo, hover, com o goto da tela hovers. Depois, const usuario: o ponto figure, ponto first, a primeira foto. E const nome: dentro dela, o texto name user1.",
     ed("A primeira foto e o nome dela", a + 3, de=a, ate_l=a + 3, mostra_de=a)),
    ("Antes do hover: not to be visible. Depois do hover: to be visible. Assim a gente testa o comportamento, não só roda um comando.",
     ed("Antes escondido · depois visível", b, de=a + 4, ate_l=b - 1, mostra_de=a)),
    ("Roda e olha o mouse passando.", roda("hover", "hover", "O nome apareceu", media="n61_hover", seg="2.9s")),
    ("No dia a dia: menus que abrem quando o mouse passa por cima, e aquelas dicas que aparecem num balãozinho. E lembra: no celular não existe passar o mouse, então ali o site precisa de outro jeito.", {'type': 'cards', 'itens': [['☰', 'Menus', 'abrem com o mouse'], ['💬', 'Dicas em balão', 'aparecem com o mouse', '#69a7ff'], ['📱', 'No celular', 'não tem mouse', '#ffd23f']]}),
] + fim("arrastar e soltar"))

# ---------- 62 ----------
a, b = bloco("arrastar e soltar")
aula(62, "O usuário precisa arrastar um item", [
    ("Tem tela em que a pessoa reorganiza as coisas arrastando: quadro de tarefas, lista, arquivos.", titulo(62, "ARRASTAR")),
    ("No the internet, clica em Drag and Drop.", home("n62_home", "/drag_and_drop", "Página inicial › Drag and Drop")),
    ("Duas caixas: A e B. Dá pra pegar a A com o mouse, arrastar, e soltar em cima da B. Aí elas trocam de lugar.",
     video("n62_drag3", "Arrastar a A até a B", url=SITE + "/drag_and_drop", acoes=[{"espera": 2800}, {"drag": ["#column-a", "#column-b"], "espera": 2500}])),
    ("As duas caixas, no Inspecionar: id igual column a, e column b.",
     devi("dev62", "/drag_and_drop", "#column-a", "id", "#column-a", "Inspecionar: id=\"column-a\" e id=\"column-b\"")),
    ("Um teste novo, arrastar e soltar, com o goto da tela drag and drop. E guarda as duas caixas: caixa A, com o id column a, e caixa B, com o id column b.",
     ed("As duas caixas", a + 3, de=a, ate_l=a + 3, mostra_de=a)),
    ("Agora, um comando só faz o arrastar: caixa A ponto drag to, caixa B.", ed("dragTo = arraste até", a + 4, de=a + 4, ate_l=a + 4, mostra_de=a)),
    ("A caixa A, arraste até a caixa B.", tr("caixaA.dragTo(caixaB)", [[".dragTo", "arraste até"], ["(caixaB)", "a caixa B"]], 1.0)),
    ("E não basta confiar que arrastou: a gente confere. Depois de trocar, o título da primeira caixa, o header dentro da column a, tem que mostrar B.",
     ed("A primeira caixa mostra B", b, de=a + 5, ate_l=b - 1, mostra_de=a)),
    ("Roda.", roda("arrastar e soltar", "arrastar", "Arrastou e conferiu", url=SITE + "/drag_and_drop", acoes=[{"drag": ["#column-a", "#column-b"], "espera": 1500}], seg="4.1s")),
    ("Repara no padrão que se repete: faz a ação, e confere o resultado. Clicou, arrastou, enviou, tanto faz. Sem a conferência, o teste não testa nada.", {'type': 'bigtext', 'lines': [['FAZ A AÇÃO', 'white', 120], ['E CONFERE O RESULTADO', 'gold', 120]], 'stagger': 0.6}),
] + fim("a tabela mudou de ordem"))

# ---------- 63 ----------
a, b = bloco("tabela pelo conteúdo")
aula(63, "A tabela mudou de ordem e o teste quebrou", [
    ("Um problema bem real. Na página inicial, clica em Sortable Data Tables.", home("n63_home", "/tables", "Página inicial › Sortable Data Tables")),
    ("Uma tabela de clientes: sobrenome, nome, e-mail, valor devido e site. A tarefa: conferir que o Tim Conway deve cinquenta dólares.",
     video("n63_tabela", "Uma tabela de clientes", url=SITE + "/tables", espera_fim=2500)),
    ("Dava pra dizer: pegue a quarta linha. Só que essa tabela deixa ordenar: clicando no título de uma coluna, as linhas mudam de lugar. E aí o teste começa a olhar pra pessoa errada.",
     video("n63_ordem", "Ordenou: a pessoa mudou de lugar")),
    ("A tabela, no Inspecionar: id igual table one. As linhas são row, e cada quadradinho é uma cell.",
     devi("dev63", "/tables", "#table1", "id", "#table1", "Inspecionar: id=\"table1\"")),
    ("Então, em vez da posição, a gente procura pelo conteúdo: a linha que tem o nome Conway.",
     {"type": "compare", "title": "COMO ACHAR A LINHA", "items": [["A 4ª LINHA", "QUEBRA SE A ORDEM MUDAR", "red"], ["A LINHA DO CONWAY", "ACHA SEMPRE", "gold"]], "size": 100, "stagger": 1.2, "vs": False}),
    ("Um teste novo, tabela pelo conteúdo, com o goto da tela tables. Depois, const linha: a tabela table one, ponto get by role row, as linhas, ponto filter has text Conway.",
     ed("filter({ hasText }) = a linha que tem este texto", a + 4, de=a, ate_l=a + 4, mostra_de=a)),
    ("Ache a linha que tem este nome.", tr("getByRole('row').filter({ hasText: 'Conway' })", [["getByRole('row')", "as linhas"], [".filter({ hasText: 'Conway' })", "a que tem Conway"]], 1.0)),
    ("Dentro dessa linha, as células: get by role cell. E o valor devido é a quarta coluna. Só que o nth conta a partir do zero. Então a quarta coluna é o nth três.",
     ed("nth(3) = a quarta coluna", b, de=a + 5, ate_l=b - 1, mostra_de=a)),
    ("Zero, o sobrenome. Um, o nome. Dois, o e-mail. E três, o valor devido. E a conferência: tem o texto cinquenta dólares.",
     {"type": "traducao", "titulo": "O NTH CONTA DO ZERO", "linhas": [["nth(0)", "sobrenome: Conway"], ["nth(1)", "nome: Tim"], ["nth(2)", "e-mail"], ["nth(3)", "valor devido: $50.00"]]}),
    ("Roda.", roda("tabela pelo conteúdo", "tabela", "Achou pela pessoa, não pela posição", url=SITE + "/tables", acoes=[{"espera": 1500}], seg="2.8s")),
    ("O internet ponto spec fica no projeto, junto com os outros testes. Terminou e passou? O ciclo da aula quarenta e cinco: git add, git commit e git push. E o GitHub roda esses testes também, nos três navegadores.",
     {"type": "traducao", "titulo": "SOBE PRO GITHUB", "linhas": [["git add .", "prepara tudo"], ['git commit -m "testes do the-internet"', "a foto com a legenda"], ["git push", "manda pro GitHub"]]}),
    ("Fechamos o site novo! Agora, recursos que aparecem em projetos de verdade.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Playwright de verdade no trabalho"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 13"}),
])


def main():
    out = ["# Roteiros · Módulo 12 do nível 2 (gerado do roteiro_playwright_n2a.py)", ""]
    for slug, p in AULAS:
        for x in p["script"]["long"]["parts"][0]["sentences"]:  # frase curta com vídeo rodando: tempo pra ver
            sc = x["scene"]
            if (sc.get("navegador") or sc.get("gravar")) and len(x["text"]) < 70:
                x["pausa"] = 2.5
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']}{' [+pausa]' if s.get('pausa') else ''} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "nivel2_modulo12.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

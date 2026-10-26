"""Gera projetos/curso-playwright-55..63 (nível 2 · módulo 12: um site que você nunca viu). Roteiro: curso-playwright/roteiros/nivel2.md.
Código = curso-playwright/projeto/tests/nivel2/internet.spec.js (validado no Actions: validar_nivel2.yml), sem o "aula NN:" dos títulos.
Vídeos reais: as páginas do the-internet gravadas pelo midia.py; o alerta, a aba nova, o hover e a tabela mudando de ordem
gravados com o Chromium de verdade numa tela virtual (ferramentas/codegen/nivel2.sh), em projetos/<aula>/midia/."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m4 import edc

SITE = "https://the-internet.herokuapp.com"
COD = re.sub(r"aula \d+: ", "", open(os.path.join(RAIZ, "curso-playwright", "projeto", "tests", "nivel2", "internet.spec.js"), encoding="utf8").read().rstrip("\n"))
L = COD.split("\n")
ARV = ["meu-primeiro-playwright", "  arquivos/", "    exemplo.txt", "  pages/", "  tests/", "    compra.spec.js", "    internet.spec.js", "    login.spec.js", "  .env", "  playwright.config.js"]
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
    return edc(cod, legenda, **d)


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


# ---------- 55 ----------
L_SITE = ln("const site")
aula(55, "Bem-vindo ao nível 2", [
    ("Até aqui você aprendeu Playwright praticamente do zero. Agora o nível sobe um pouco.", bt(("NÍVEL 2", "gold", 210), ("O NÍVEL SOBE", "white", 110))),
    ("Nos próximos módulos, eu quero te colocar em situações que aparecem quando você começa a automatizar sistemas reais.",
     {"type": "cards", "itens": [["🌐", "Site novo", "que você nunca viu"], ["🧩", "Problemas novos", "do dia a dia", AZUL], ["🛠", "Recursos novos", "do Playwright", AMARELO], ["📁", "Projeto novo", "do zero", VERDE]]}),
    ("E pra isso a gente sai um pouco do saucedemo. Vamos usar o the internet: um site de treino com várias páginas diferentes.",
     video("n55_site", "the-internet.herokuapp.com", url=SITE, acoes=[{"scroll": 500, "espera": 900}, {"scroll": 600, "espera": 900}, {"scroll": -1100, "espera": 600}])),
    ("Tem upload, nova aba, iframe, alerta, tabela. Mas eu não quero que você decore uma lista de comandos.",
     {"type": "cards", "titulo": "O QUE TEM LÁ", "itens": [["⬆", "Upload", ""], ["⧉", "Nova aba", "", AZUL], ["▣", "Iframe", "", AMARELO], ["⚠", "Alerta", "", VERM], ["▦", "Tabela", "", VERDE]]}),
    ("A ideia vai ser sempre: apareceu um problema novo, a gente descobre como resolver.", bt(("APARECEU UM PROBLEMA", "white", 100), ("A GENTE DESCOBRE", "gold", 120), ("COMO RESOLVER", "gold", 120))),
    ("Cria o arquivo internet ponto spec ponto js. Como o baseURL ainda aponta pro saucedemo, aqui a gente usa o endereço completo.",
     ed("const site = o endereço completo", L_SITE, de=1, ate_l=L_SITE)),
    ("Vamos começar com uma coisa que aparece em quase todo formulário.", {"type": "passo", "icone": "▶", "titulo": "Próxima aula", "sub": "O formulário mudou"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: O FORMULÁRIO MUDOU"}),
])

# ---------- 56 ----------
a, b = bloco("checkbox e dropdown"); L_CHK, L_TBC, L_DD, L_HV = ln(".check()"), ln("toBeChecked()"), ln("#dropdown"), ln("toHaveValue")
aula(56, "O formulário mudou", [
    ("Imagina que caiu uma tarefa nova: validar as preferências de um formulário.", tarefa("NOVA TAREFA", "Validar as preferências do formulário")),
    ("Abrindo a tela, tem duas coisas que a gente ainda não usou: a caixa de marcar e a lista de opções.",
     video("n56_check", "A caixa de marcar: checkbox", url=SITE + "/checkboxes", acoes=[{"check": "#checkboxes input >> nth=0", "espera": 900}, {"uncheck": "#checkboxes input >> nth=0", "espera": 900}])),
    ("Pra marcar: ponto check. Pra desmarcar: ponto uncheck.", ed("check = marque", L_CHK, de=a, ate_l=L_CHK, mostra_de=a)),
    ("check, marque. uncheck, desmarque.", tr("primeira.check()  ·  primeira.uncheck()", [[".check()", "marque"], [".uncheck()", "desmarque"]], 1.2)),
    ("Mas clicar não basta: a gente confere. to be checked, esteja marcada. E com o not na frente: não esteja marcada.",
     ed("toBeChecked = esteja marcada", L_TBC + 2, de=L_TBC, ate_l=L_TBC + 2, mostra_de=a)),
    ("Agora o segundo campo: aqui a pessoa escolhe uma opção. Você já viu isso no desafio quatro: select option.",
     video("n56_dropdown", "A lista de opções: selectOption", url=SITE + "/dropdown", acoes=[{"select": ["#dropdown", "1"], "espera": 900}, {"select": ["#dropdown", "2"], "espera": 900}])),
    ("E a conferência: to have value, tenha o valor dois.", ed("toHaveValue = tenha o valor", b, de=L_DD - 1, ate_l=L_HV, mostra_de=a + 3)),
    ("E por que o valor, e não o texto? O texto é o que a pessoa vê na tela. O valor é o que vai pro sistema quando ela salva. E é ele que precisa estar certo.", {'type': 'traducao', 'titulo': 'TEXTO × VALOR', 'linhas': [['Option 2', 'o que a pessoa vê'], ['value="2"', 'o que vai pro sistema']]}),
    ("Roda e olha.", roda("checkbox e dropdown", "checkbox", "Marcou, desmarcou e escolheu", url=SITE + "/checkboxes",
                         acoes=[{"check": "#checkboxes input >> nth=0", "espera": 700}, {"uncheck": "#checkboxes input >> nth=0", "espera": 700},
                                {"goto": SITE + "/dropdown", "espera": 600}, {"select": ["#dropdown", "2"], "espera": 900}], seg="3.4s")),
    ("No trabalho, isso aparece em quase todo cadastro: aceitar os termos de uso, receber novidades por e-mail, escolher o estado ou a cidade.", {'type': 'cards', 'itens': [['☑', 'Aceito os termos', 'checkbox'], ['☑', 'Receber novidades', 'checkbox', '#69a7ff'], ['▾', 'Estado e cidade', 'lista de opções', '#ffd23f']], 'titulo': 'EM QUASE TODO CADASTRO'}),
] + fim("upload de arquivo"))

# ---------- 57 ----------
a, b = bloco("upload de arquivo"); L_UP = ln("setInputFiles")
aula(57, "O usuário precisa enviar um arquivo", [
    ("A tarefa mudou: o usuário precisa conseguir anexar um documento. Currículo, comprovante, planilha.", tarefa("NOVA TAREFA", "O usuário precisa anexar um documento")),
    ("Na tela tem um campo de escolher arquivo e um botão Upload.", video("n57_tela", "Escolher arquivo · Upload", url=SITE + "/upload", espera_fim=2500)),
    ("Primeiro, um arquivo de exemplo dentro do projeto: uma pasta arquivos, com um texto dentro.",
     edc("Meu currículo de testador", "arquivos/exemplo.txt", arquivo="exemplo.txt", pastas=ARV, digitar=True, digitar_de=1, digitar_ate=1, fonte=30)),
    ("Agora: set input files, coloque este arquivo no campo.", ed("setInputFiles = coloque este arquivo", L_UP, de=a, ate_l=L_UP, mostra_de=a)),
    ("set input files: coloque este arquivo no campo.", tr(".setInputFiles('arquivos/exemplo.txt')", [[".setInputFiles", "coloque no campo"], ["('arquivos/exemplo.txt')", "este arquivo"]], 1.2)),
    ("Repara: o Playwright não abre aquela janela do Windows pra procurar o arquivo com o mouse. Ele entrega o arquivo direto pro campo.",
     {"type": "cards", "itens": [["✗", "Sem janela do Windows", "nada de procurar com o mouse", VERM], ["✓", "Direto no campo", "o arquivo vai pronto", VERDE]]}),
    ("Clica em Upload e confere que o nome do arquivo apareceu na página.", ed("O nome do arquivo apareceu", b, de=L_UP + 1, ate_l=b - 1, mostra_de=a)),
    ("Roda.", roda("upload de arquivo", "upload", "O arquivo subiu", url=SITE + "/upload",
                   acoes=[{"upload": ["#file-upload", "curso-playwright/projeto/arquivos/exemplo.txt"], "espera": 900}, {"click": "#file-submit", "espera": 1400}], seg="3.2s")),
    ("No dia a dia, também vale testar o lado ruim: um arquivo grande demais, ou de um formato que o sistema não aceita. Ele tem que recusar com uma mensagem clara.", {'type': 'cards', 'itens': [['✓', 'Arquivo certo', 'sobe e aparece'], ['⚖', 'Grande demais', 'recusa e avisa', '#ffd23f'], ['✗', 'Formato errado', 'recusa e avisa', '#ff6b6b']], 'titulo': 'OS DOIS LADOS DO UPLOAD'}),
] + fim("uma caixa travou a página"))

# ---------- 58 ----------
a, b = bloco("alerta do navegador"); L_ON, L_ACC, L_CLK = ln("page.on('dialog'"), ln("dialog.accept()"), ln("Click for JS Alert")
aula(58, "Uma caixa travou a página", [
    ("Agora aconteceu uma coisa diferente: clicamos num botão e o navegador abriu essa caixa.", video("n58_alerta", "O alerta do navegador")),
    ("Enquanto ela está aberta, não dá pra usar a página. Isso é um alerta do navegador, um dialog.",
     {"type": "cards", "titulo": "DIALOG", "itens": [["⚠", "A caixa do navegador", "com um OK"], ["⛔", "Trava a página", "até alguém clicar", VERM]]}),
    ("A gente precisa preparar o Playwright antes de o alerta aparecer: page ponto on, dialog, e dialog ponto accept.", ed("page.on('dialog') = quando aparecer um alerta", L_ACC + 1, de=L_ON, ate_l=L_ACC + 1, mostra_de=a)),
    ("Quando aparecer um alerta, aceite.", tr("page.on('dialog', ... dialog.accept())", [["page.on('dialog'", "quando aparecer um alerta"], ["dialog.accept()", "aceite"]], 1.0)),
    ("A ordem é importante: primeiro prepara, depois clica. Se você tentar reagir só depois, o alerta já passou.",
     {"type": "cards", "titulo": "A ORDEM", "itens": [["1", "Prepara", "page.on('dialog')"], ["2", "Clica", "no botão", AZUL], ["3", "Aparece", "o alerta", AMARELO], ["4", "Aceita", "sozinho", VERDE]]}),
    ("No fim, confere a mensagem: You successfully clicked an alert.", ed("A mensagem do resultado", b, de=L_CLK, ate_l=b - 1, mostra_de=a)),
    ("Roda.", roda("alerta do navegador", "alerta", "Preparou, clicou e aceitou", media="n58_alerta", seg="3.3s")),
    ("E sem esse preparo? O Playwright cancela o alerta sozinho, e o teste segue em frente como se nada tivesse acontecido.", {'type': 'cards', 'itens': [['⚙', 'Sem o page.on', 'o Playwright cancela sozinho', '#ff6b6b'], ['✓', 'Com o page.on', 'você decide o que fazer', '#3fd68a']]}),
    ("No trabalho, o mais comum é o tem certeza que quer excluir? E aí dá pra testar os dois lados: accept, confirma. Dismiss, cancela, e nada pode ser apagado.", {'type': 'traducao', 'titulo': 'TEM CERTEZA QUE QUER EXCLUIR?', 'linhas': [['dialog.accept()', 'confirma: apagou'], ['dialog.dismiss()', 'cancela: nada foi apagado']]}),
] + fim("o link abriu outra aba"))

# ---------- 59 ----------
a, b = bloco("nova aba"); L_PROM, L_NOVA = ln("waitForEvent('popup')"), ln("await promessa")
aula(59, "O link abriu outra aba", [
    ("Imagina: você clica pra ver os detalhes de um pedido, e eles abrem em outra aba. E o teste continua olhando a aba antiga.", video("n59_aba", "Click Here abre outra aba")),
    ("Então a gente precisa pegar a aba nova quando ela abrir.", {"type": "cards", "itens": [["⧉", "Abriu outra aba", ""], ["👀", "O teste olha a antiga", "", VERM], ["✓", "Pega a nova", "quando ela abrir", VERDE]]}),
    ("Primeiro, o aviso: const promessa igual page ponto wait for event, popup.", ed("waitForEvent('popup') = espere uma nova aba", L_PROM, de=a, ate_l=L_PROM, mostra_de=a)),
    ("Espere uma nova aba.", tr("page.waitForEvent('popup')", [["waitForEvent", "espere acontecer"], ["('popup')", "uma nova aba"]], 1.0)),
    ("Por que avisar antes de clicar? Porque a aba nova abre muito rápido. Se você só começar a esperar depois do clique, ela pode já ter aberto, e o teste fica esperando pra sempre.", {'type': 'cards', 'itens': [['1', 'Primeiro, o aviso', 'espere uma aba nova'], ['2', 'Depois, o clique', 'a aba abre', '#69a7ff'], ['3', 'Aí, pega a aba', 'await promessa', '#ffd23f']], 'titulo': 'A ORDEM'}),
    ("Depois clica no link. E aí: const novaAba igual await promessa. Guarde a aba que abriu.", ed("novaAba = a aba que abriu", L_NOVA, de=L_PROM + 1, ate_l=L_NOVA, mostra_de=a)),
    ("A partir daí, você usa a nova aba igual ao page: confere que ela mostra New Window.", ed("novaAba funciona igual ao page", b, de=b - 2, ate_l=b - 1, mostra_de=a)),
    ("Roda e olha as duas abas.", roda("nova aba", "nova aba", "Abriu e conferiu a aba nova", media="n59_aba", seg="3.0s")),
    ("No dia a dia, isso aparece em link de pagamento, termos de uso, nota fiscal em PDF, e em login com conta de outro site, que abre numa janela separada.", {'type': 'cards', 'itens': [['💳', 'Pagamento', 'abre em outra aba'], ['📄', 'PDF e termos', 'abrem em outra aba', '#69a7ff'], ['🔑', 'Login com outra conta', 'janela separada', '#ffd23f']]}),
] + fim("uma página dentro da página"))

# ---------- 60 ----------
a, b = bloco("iframe"); L_FR = ln("frameLocator")
aula(60, "Tem uma página dentro da página", [
    ("Olha essa tela: tem um editor de texto no meio. Só que o seletor normal não acha nada lá dentro.", video("n60_iframe", "Um editor no meio da página", url=SITE + "/iframe", espera_fim=3000)),
    ("Por quê? Porque aquele pedaço é outra página, encaixada nesta. Isso se chama iframe.",
     {"type": "cards", "titulo": "IFRAME", "itens": [["▭", "A página", "the-internet"], ["▣", "O iframe", "outra página dentro", AZUL], ["✎", "O editor", "lá dentro", AMARELO]]}),
    ("Primeiro, você diz em qual quadro procurar: frame locator.", ed("frameLocator = procure dentro deste quadro", L_FR, de=a, ate_l=L_FR, mostra_de=a)),
    ("Procure dentro deste quadro.", tr("page.frameLocator('#mce_0_ifr')", [["frameLocator", "procure dentro do quadro"], ["('#mce_0_ifr')", "este quadro"]], 1.0)),
    ("O frame locator recebe o seletor do iframe. Aqui, o id dele. E daí pra frente, tudo o que você procura é lá dentro.", {'type': 'traducao', 'titulo': 'ENTRANDO NO QUADRO', 'linhas': [["frameLocator('#mce_0_ifr')", 'este quadro, pelo id'], ["getByText('...')", 'procure lá dentro']]}),
    ("Depois, procura normalmente lá dentro, e confere o texto do editor.", ed("Lá dentro, igual a sempre", b, de=L_FR + 1, ate_l=b - 1, mostra_de=a)),
    ("A lógica: entrar no iframe, procurar o elemento, conferir.", {"type": "cards", "itens": [["1", "Entra no iframe", "frameLocator"], ["2", "Procura", "o elemento", AZUL], ["3", "Confere", "expect", VERDE]]}),
    ("Roda.", roda("iframe", "iframe", "Achou o texto lá dentro", url=SITE + "/iframe", acoes=[{"espera": 1500}], seg="3.6s")),
    ("No trabalho, o caso mais comum é o pagamento: o campo do cartão quase sempre é um iframe, de outra empresa, por segurança. Também aparece em vídeo, mapa e chat de atendimento.", {'type': 'cards', 'itens': [['💳', 'Campo do cartão', 'quase sempre iframe'], ['▶', 'Vídeo e mapa', 'iframe', '#69a7ff'], ['💬', 'Chat de atendimento', 'iframe', '#ffd23f']], 'titulo': 'ONDE TEM IFRAME'}),
] + fim("o botão só aparece com o mouse"))

# ---------- 61 ----------
a, b = bloco("hover"); L_NOME, L_NOT, L_HOV = ln("getByText('name: user1')"), ln("not.toBeVisible()"), ln("usuario.hover()")
aula(61, "O botão só aparece quando passo o mouse", [
    ("Chegou um relato de bug: não consigo clicar na opção, porque ela só aparece quando passo o mouse no usuário.", tarefa("RELATO DE BUG", "Só aparece quando passo o mouse", VERM)),
    ("Vamos reproduzir: sem o mouse em cima, o nome está escondido. Com o mouse, ele aparece.", video("n61_hover", "Com o mouse em cima, o nome aparece")),
    ("No Playwright: hover. Passe o mouse por cima.", tr("await usuario.hover();", [["usuario", "o usuário"], [".hover()", "passe o mouse por cima"]], 1.0)),
    ("Antes do hover: not to be visible. Depois do hover: to be visible. Assim a gente testa o comportamento, não só roda um comando.",
     ed("Antes escondido · depois visível", b, de=a, ate_l=b - 1, mostra_de=a)),
    ("Roda e olha o mouse passando.", roda("hover", "hover", "O nome apareceu", media="n61_hover", seg="2.9s")),
    ("No dia a dia: menus que abrem quando o mouse passa por cima, e aquelas dicas que aparecem num balãozinho. E lembra: no celular não existe passar o mouse, então ali o site precisa de outro jeito.", {'type': 'cards', 'itens': [['☰', 'Menus', 'abrem com o mouse'], ['💬', 'Dicas em balão', 'aparecem com o mouse', '#69a7ff'], ['📱', 'No celular', 'não tem mouse', '#ffd23f']]}),
] + fim("arrastar e soltar"))

# ---------- 62 ----------
a, b = bloco("arrastar e soltar"); L_DRAG = ln("dragTo")
aula(62, "O usuário precisa arrastar um item", [
    ("Tem tela em que a pessoa reorganiza as coisas arrastando: quadro de tarefas, lista, arquivos.", titulo(62, "ARRASTAR")),
    ("No nosso exemplo, duas caixas: A e B. A gente quer arrastar a A até a B.", video("n62_drag", "Arrastar a A até a B", url=SITE + "/drag_and_drop", acoes=[{"drag": ["#column-a", "#column-b"], "espera": 1500}])),
    ("Um comando: drag to. Arraste até.", ed("dragTo = arraste até", L_DRAG, de=a, ate_l=L_DRAG, mostra_de=a)),
    ("A caixa A, arraste até a caixa B.", tr("caixaA.dragTo(caixaB)", [[".dragTo", "arraste até"], ["(caixaB)", "a caixa B"]], 1.0)),
    ("E não basta confiar que arrastou: a gente confere que a primeira caixa agora mostra B.", ed("A primeira caixa mostra B", b, de=b - 2, ate_l=b - 1, mostra_de=a)),
    ("Roda.", roda("arrastar e soltar", "arrastar", "Arrastou e conferiu", url=SITE + "/drag_and_drop", acoes=[{"drag": ["#column-a", "#column-b"], "espera": 1500}], seg="4.1s")),
    ("Repara no padrão que se repete: faz a ação, e confere o resultado. Clicou, arrastou, enviou, tanto faz. Sem a conferência, o teste não testa nada.", {'type': 'bigtext', 'lines': [['FAZ A AÇÃO', 'white', 120], ['E CONFERE O RESULTADO', 'gold', 120]], 'stagger': 0.6}),
] + fim("a tabela mudou de ordem"))

# ---------- 63 ----------
a, b = bloco("tabela pelo conteúdo"); L_ROW = ln("filter({ hasText")
aula(63, "A tabela mudou de ordem e o teste quebrou", [
    ("Um problema bem real: uma tabela de clientes.", video("n63_tabela", "Uma tabela de clientes", url=SITE + "/tables", espera_fim=2500)),
    ("Dava pra dizer: pegue a segunda linha. Só que amanhã alguém ordena a tabela por nome, a pessoa muda de lugar, e o teste começa a olhar pra pessoa errada.",
     video("n63_ordem", "Ordenou: a pessoa mudou de lugar")),
    ("Então, em vez da posição, a gente procura pelo conteúdo: get by role row, filter has text.", ed("filter({ hasText }) = a linha que tem este texto", L_ROW, de=a, ate_l=L_ROW, mostra_de=a)),
    ("Ache a linha que tem este nome.", tr("getByRole('row').filter({ hasText: 'Conway' })", [["getByRole('row')", "as linhas"], [".filter({ hasText: 'Conway' })", "a que tem Conway"]], 1.0)),
    ("E dentro dessa linha, o valor devido: confere que é cinquenta dólares.", ed("O valor devido dessa pessoa", b, de=b - 2, ate_l=b - 1, mostra_de=a)),
    ("Antes: a segunda linha. Depois: a linha que tem o nome da pessoa. Se a ordem mudar, o teste continua achando a pessoa certa.",
     {"type": "compare", "title": "COMO ACHAR A LINHA", "items": [["A 2ª LINHA", "QUEBRA SE A ORDEM MUDAR", "red"], ["A LINHA DO CONWAY", "ACHA SEMPRE", "gold"]], "size": 100, "stagger": 1.2, "vs": False}),
    ("Roda.", roda("tabela pelo conteúdo", "tabela", "Achou pela pessoa, não pela posição", url=SITE + "/tables", acoes=[{"espera": 1500}], seg="2.8s")),
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

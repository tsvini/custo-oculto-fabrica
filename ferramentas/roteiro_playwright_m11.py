"""Gera projetos/curso-playwright-49..54 (módulo 11: desafios). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Formato: desafio -> "pausa o vídeo e tenta" (contagem na tela + silêncio de verdade na narração: campo "pausa") -> dica (gravação real)
-> solução digitada com tradução -> o teste rodando (VS Code + terminal + navegador real por cima).
Código = curso-playwright/projeto/tests/etapas/aula49..54.spec.js (o desafios.spec.js crescendo; o 54 é igual ao arquivo final)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import inteiro, bt, titulo, projeto, RAIZ
from roteiro_playwright_m3 import SAUCE, LOGIN
from roteiro_playwright_m4 import edc
from roteiro_playwright_m8 import cod, ln, trecho
from roteiro_playwright_m10 import ARV_API

ARV_D = ["meu-primeiro-playwright", "  .github/", "  node_modules/", "  pages/", "  tests/", "    api.spec.js", "    compra.spec.js", "    desafios.spec.js", "    login.spec.js", "  .env", "  playwright.config.js"]  # enxuto: só a pasta tests aberta
INV = "https://www.saucedemo.com/inventory.html"
AMARELO, AZUL, VERM = "#ffd23f", "#69a7ff", "#ff6b6b"

# saídas do terminal (formato real do Actions: o setup do login salvo roda junto, por isso "2 tests"; -g = só o desafio da aula, aula 25)
def _saida(g, seg):
    return (f'npx playwright test -g "{g}" --headed --project=chromium', [("Running 2 tests using 1 worker", "mut", 0.08), (f"  2 passed ({seg})", "ac", 0.87)])


SAIDAS = {49: _saida("senha errada", "4.6s"), 50: _saida("campos vazios", "4.2s"), 51: _saida("remove do carrinho", "4.9s"),
          52: _saida("ordena", "4.7s"), 53: _saida("logout", "5.6s"), 54: _saida("desafio final", "6.3s")}


def desafio(n, nome, itens, legenda="O desafio", contagem=0):
    return {"type": "desafio", "numero": n, "titulo": nome, "itens": itens, "contagem": contagem, "legenda": legenda}


def pausa(d, texto="Agora sim: pausa o vídeo e tenta. Quando voltar, a solução."):
    """depois da dica e do DevTools: a mesma tela do desafio, agora com a contagem"""
    return (texto, dict(d, contagem=5, legenda="Pausa o vídeo e tenta"))


def video(media, legenda, acoes, url=SAUCE, logado=False, **kw):
    """gravação real do navegador (a dica): o aluno vê a tela de verdade"""
    d = {"type": "tela", "media": media, "url": INV if logado else url, "gravar": True, "acoes": acoes, "titulo": "saucedemo.com", "legenda": legenda,
         "espera_inicio": 1000, "espera_fim": 2200, "delay_letra": 70}
    if logado:
        d.update({"pre_acoes": LOGIN, "pre_url": SAUCE})
    d.update(kw)
    return d


def dev(media, dt, legenda, acoes=(), logado=False):
    """DevTools de verdade: botão direito › Inspecionar no elemento com esse data-test (de onde vem o seletor)"""
    return {"type": "devtools", "media": media, "url": SAUCE, "acoes": (LOGIN if logado else []) + [a for a in acoes], "inspecionar": f"[data-test=\"{dt}\"]",
            "attrs": ["class", "data-test", "id", "name"], "realce": ["data-test"], "realce_em": 4.0, "realce_rotulo": dt, "legenda": legenda}


def solucao(c, chave, legenda, **kw):
    """o desafios.spec.js com o teste novo sendo digitado (e rolado até ele)"""
    a = ln(c, chave); b = a
    L = c.split("\n"); ind = len(L[a - 1]) - len(L[a - 1].lstrip())
    while L[b - 1] != " " * ind + "});":
        b += 1
    d = dict(arquivo="desafios.spec.js", digitar=True, digitar_de=a, digitar_ate=b, fonte=24, vel=kw.pop("vel", 0.7))  # sem explorer: as linhas passam de 80 caracteres
    if len(L) > 16:
        d.update(rolar=True, rolar_de=0.2, rolar_dur=0.6)
    d.update(kw)
    return edc(c, legenda, **d), (a, b)


def passos(c, ab, partes):
    """a solução digitada em partes, uma fala por parte: partes = [(quantas linhas, fala, legenda), ...] a partir da linha do test("""
    a, b = ab; L = c.split("\n"); out = []; ini = a
    assert sum(k for k, _, _ in partes) == b - a, (sum(k for k, _, _ in partes), b - a)
    for k, fala, leg in partes:
        fim = ini + k - 1
        cod = L[:fim] + L[b - 1:]  # o que já foi escrito + o fechamento do teste e o resto do arquivo
        d = dict(arquivo="desafios.spec.js", digitar=True, digitar_de=ini, digitar_ate=fim, fonte=24)
        if len(cod) > 16:
            d.update(rolar=True, rolar_de=0.2, rolar_dur=0.6, rolar_ate=fim + 3)
        out.append((fala, edc("\n".join(cod), leg, **d)))
        ini = fim + 1
    return out


def rodando(c, ab, legenda, acoes, media, n, logado=False, **kw):
    a, b = ab; b = min(b, a + 8)  # com o terminal aberto cabem ~9 linhas; o navegador cobre o editor durante a execução
    nav = {"media": media, "url": INV if logado else SAUCE, "gravar": True, "acoes": acoes, "espera_inicio": 800, "espera_fim": 1800, "delay_letra": 55,
           "titulo": "Chromium", "em": 0.12, "ate": 0.84}
    if logado:
        nav.update({"pre_acoes": LOGIN, "pre_url": SAUCE})
    cmd, linhas = SAIDAS[n]
    term = [{"cmd": cmd, "em": 0.03}] + [{"out": t, "cor": cor, "em": em} for t, cor, em in linhas]
    return edc(trecho(c, a, b), legenda, arquivo="desafios.spec.js", pastas=ARV_D, linha0=a, terminal=term, navegador=nav, fonte=24, **kw)


def fim(sub):
    return {"type": "endcard", "sub": sub}


AULAS = []


def aula(n, titulo_aula, frases, pausas):
    slug, p = projeto(n, f"MÓDULO 11 · AULA {n}", titulo_aula, frases)
    # silêncio de verdade depois da frase (a narração fica parada e a cena continua):
    #  desafio: a contagem de 5 s inteira · solução: ~0,55 s por linha digitada · o teste rodando: tempo de ver o navegador e o "passed"
    for x in p["script"]["long"]["parts"][0]["sentences"]:
        sc, fala = x["scene"], len(x["text"]) / 14.5
        if sc.get("type") == "desafio" and sc.get("contagem"):
            x["pausa"] = 6
        elif sc.get("navegador"):
            x["pausa"] = 4
        elif sc.get("digitar") and sc.get("digitar_de"):
            falta = (sc["digitar_ate"] - sc["digitar_de"] + 1) * 0.55 + 1.0 - fala
            if falta > 0.8:
                x["pausa"] = 2 * round(falta / 2 + 0.25)
    AULAS.append((slug, p))


JJ = "\n".join


def preencher():
    # ---------- Aula 49 ----------
    D49 = desafio("1", "Senha errada", [["👤", "usuário certo: standard_user"], ["🔑", "senha errada (qualquer uma)", VERM], ["✓", "confere a mensagem de erro", AMARELO]])
    C = cod(49); ed, ab = solucao(C, "test('desafio 1", "fill, fill, click e o expect")
    CAB49 = ln(C, "test('desafio 1") - 2  # import, describe e beforeEach (até a linha em branco antes do teste)
    aula(49, "Desafio 1 - senha errada", [
        ("Primeiro desafio: o que acontece quando alguém erra a senha?", titulo(49, "DESAFIO 1")),
        ("Isso se chama cenário negativo: testar o que acontece quando a pessoa erra. No trabalho, é onde mais aparece bug, porque quase ninguém lembra de testar.",
         {"type": "cards", "itens": [["✓", "Cenário positivo", "tudo dá certo", "#3fd68a"], ["✗", "Cenário negativo", "a pessoa erra", "#ff6b6b"]]}),  # pra que / quando
        ("O teste: usuário certo, senha errada, e conferir a mensagem de erro.", D49),
        ("Dica: a mensagem fica no data-test error, e contém do not match.",
         video("dica49", "data-test=\"error\" · contém do not match", [{"fill": ["#user-name", "standard_user"]}, {"fill": ["#password", "senha_errada"]}, {"click": "#login-button"}])),
        ("E de onde vem esse error? Errando a senha, botão direito na mensagem vermelha, e Inspecionar. Lá está: data-test igual error.",
         dev("dev49", "error", "Inspecionar: data-test=\"error\"", [{"fill": ["#user-name", "standard_user"]}, {"fill": ["#password", "senha_errada"]}, {"click": "#login-button"}])),
        ("O começo de sempre: o import, um describe chamado Desafios, e o before each que abre o site.",
         edc(JJ(C.split("\n")[:CAB49] + ["});"]), "O começo: import, describe e beforeEach", arquivo="desafios.spec.js", pastas=ARV_D, digitar=True, digitar_de=1, digitar_ate=CAB49, fonte=26,
             criar=[["Os desafios vão num arquivo só deles. Dentro da pasta tests, cria o desafios ponto spec ponto js.", "desafios.spec.js"]])),
        pausa(D49),
    ] + passos(C, ab, [
        (1, "Solução. O nome do teste diz o que ele confere: desafio um, senha errada mostra erro.", "O nome diz o que o teste confere"),
        (2, "Preenche o usuário certo, standard user. E na senha, qualquer coisa errada: aqui, senha underline errada.", "Usuário certo, senha errada"),
        (1, "Clica no botão de login, igual a sempre.", "O clique no Login"),
        (1, "E a conferência: o elemento error contém o texto do not match, que quer dizer não confere.", "error contém: do not match"),
    ]) + [
        ("Contém o texto: não precisa ser a mensagem inteira.",
         {"type": "traducao", "codigo": "toContainText('do not match')", "partes": [["toContainText", "contém o texto"], ["('do not match')", "só um pedaço da mensagem"]], "passo": 1.2}),
        ("Roda e olha: o erro aparece e o teste passa.",
         rodando(C, ab, "O erro aparece e o teste passa", [{"fill": ["#user-name", "standard_user"]}, {"fill": ["#password", "senha_errada"]}, {"click": "#login-button"}], "run49", 49)),
        ("Te vejo no próximo desafio!", fim("PRÓXIMO: DESAFIO 2")),
    ], [1])

    # ---------- Aula 50 ----------
    D50 = desafio("2", "Campos vazios", [["▭", "não preenche nada"], ["▶", "clica em Login", AZUL], ["✓", "confere a mensagem de erro", AMARELO]])
    C = cod(50); ed, ab = solucao(C, "test('desafio 2", "Só o clique e o expect")
    aula(50, "Desafio 2 - campos vazios", [
        ("Desafio dois: e se a pessoa clicar em Login sem preencher nada?", titulo(50, "DESAFIO 2")),
        ("Por que testar isso? Porque é a primeira coisa que alguém apressado faz: clica sem preencher. O sistema precisa avisar, e não pode deixar entrar nem travar.",
         {"type": "cards", "itens": [["⚡", "Alguém apressado", "clica sem preencher"], ["✓", "O sistema avisa", "Username is required", "#3fd68a"], ["✗", "Não pode", "entrar nem travar", VERM]]}),
        ("O teste: não preenche nada, clica em Login, e confere a mensagem de erro.", D50),
        ("Dica: a mensagem é Username is required.", video("dica50", "Username is required", [{"click": "#login-button"}])),
        pausa(D50),
    ] + passos(C, ab, [
        (1, "Solução. O nome: desafio dois, campos vazios. E repara: nenhum fill. A pessoa não preencheu nada, então o teste também não preenche.", "Nenhum fill: nada preenchido"),
        (1, "Só o clique no botão de login.", "Só o clique"),
        (1, "E a conferência: o mesmo elemento error, agora com o texto Username is required, o usuário é obrigatório.", "error contém: Username is required"),
    ]) + [
        ("Repara: nem todo teste preenche tudo, e um bom teste também confere o que dá errado.", bt(("BOM TESTE", "gold", 150), ("TAMBÉM CONFERE", "white", 110), ("O QUE DÁ ERRADO", "white", 110))),
        ("Roda: passou.", rodando(C, ab, "Passou", [{"click": "#login-button"}], "run50", 50)),
        ("Te vejo no próximo!", fim("PRÓXIMO: DESAFIO 3")),
    ], [1])

    # ---------- Aula 51 ----------
    D51 = desafio("3", "Remover do carrinho", [["＋", "adiciona a mochila"], ["−", "remove de novo", AZUL], ["✓", "o carrinho fica vazio", AMARELO]])
    C = cod(51); ed, ab = solucao(C, "test('desafio 3", "toHaveCount(0)")
    L_LOG51 = ln(C, "test.describe('logado'"); L_BE51 = ln(C, "inventory.html")
    ADD = {"click": "[data-test=\"add-to-cart-sauce-labs-backpack\"]", "espera": 1400}
    REM = {"click": "[data-test=\"remove-sauce-labs-backpack\"]", "espera": 1400}
    aula(51, "Desafio 3 - remover do carrinho", [
        ("Desafio três: adicionar a mochila e depois remover.", titulo(51, "DESAFIO 3")),
        ("No trabalho, o remover quebra mais do que parece: o número não atualiza, ou o produto continua lá. E quase ninguém testa, porque todo mundo só testa o adicionar.",
         {"type": "cards", "itens": [["＋", "Adicionar", "todo mundo testa", "#3fd68a"], ["−", "Remover", "quase ninguém testa", VERM]]}),
        ("O teste: adiciona a mochila, remove de novo, e confere que o carrinho ficou vazio.", D51),
        ("Dica: depois de adicionar, o botão vira Remove, com data-test remove-sauce-labs-backpack. E quando o carrinho fica vazio, o numerozinho some da página.",
         video("dica51", "Add to cart vira Remove · o numerozinho some", [ADD, REM], logado=True)),
        ("E o botão Remove: depois de adicionar a mochila, botão direito nele, e Inspecionar. Data-test igual remove sauce labs backpack.",
         dev("dev51", "remove-sauce-labs-backpack", "Inspecionar: data-test=\"remove-sauce-labs-backpack\"", [ADD], logado=True)),
        ("Os desafios daqui pra frente começam logados. Lembra do login salvo da aula quarenta e dois? Dentro do describe, uma caixa nova chamada logado. Nela, o test ponto use com o storage state, e um before each que abre direto a página de produtos.",
         inteiro(edc(JJ(C.split("\n")[L_LOG51 - 2:L_BE51 + 2] + ["  });", "});"]), "describe('logado') + test.use", arquivo="desafios.spec.js", pastas=ARV_D, linha0=L_LOG51 - 1, digitar=True, digitar_de=2, digitar_ate=L_BE51 + 2 - L_LOG51 + 1, fonte=22), C.split("\n")[:L_LOG51 - 2])),
        pausa(D51),
    ] + passos(C, ab, [
        (3, "Solução. Primeiro, adiciona a mochila, e confere que o numerozinho do carrinho mostra um.", "Adiciona e confere: 1"),
        (1, "Depois, clica no Remove, o botão que apareceu no lugar do Add to cart.", "O clique no Remove"),
        (1, "E pra conferir que o carrinho ficou vazio, to have count zero:", "toHaveCount(0)"),
    ]) + [
        ("eu espero que o seletor encontre zero elementos.",
         {"type": "traducao", "codigo": "expect(...).toHaveCount(0);", "partes": [["expect", "eu espero que"], ["toHaveCount(0)", "encontre zero elementos"]], "passo": 1.0}),
        ("Roda.", rodando(C, ab, "Passou", [ADD, REM], "run51", 51, logado=True)),
        ("Te vejo no próximo!", fim("PRÓXIMO: DESAFIO 4")),
    ], [1])

    # ---------- Aula 52 ----------
    D52 = desafio("4", "Ordenar por preço", [["⇅", "ordena do menor pro maior"], ["✓", "o primeiro preço é o menor", AMARELO]])
    C = cod(52); ed, ab = solucao(C, "test('desafio 4", "selectOption('lohi') e o primeiro preço")
    SEL = {"select": ["[data-test=\"product-sort-container\"]", "lohi"], "espera": 1800}
    aula(52, "Desafio 4 - ordenar por preço", [
        ("Desafio quatro: ordenar do menor pro maior preço.", titulo(52, "DESAFIO 4")),
        ("Ordenar parece simples, mas é um bug clássico: o site ordena o preço como se fosse texto, e o doze e cinquenta aparece antes do sete e noventa e nove.",
         {"type": "traducao", "titulo": "O BUG CLÁSSICO DA ORDENAÇÃO", "linhas": [["7.99 · 9.99 · 12.50", "certo: como número"], ["12.50 · 7.99 · 9.99", "errado: como texto"]]}),
        ("O teste: ordena do menor pro maior, e confere que o primeiro preço é o menor.", D52),
        ("Dica: a caixa de ordenar é um select, uma caixa de opções.", video("dica52", "A caixa de ordenar: um select", [SEL], logado=True)),
        ("De onde vêm os seletores? A caixa de ordenar, no Inspecionar: data-test igual product sort container.",
         dev("dev52_sort", "product-sort-container", "Inspecionar: data-test=\"product-sort-container\"", logado=True)),
        ("E o preço de cada produto: data-test igual inventory item price.",
         dev("dev52_preco", "inventory-item-price", "Inspecionar: data-test=\"inventory-item-price\"", logado=True)),
        ("Pra escolher uma opção, existe o select option, escolha a opção. A do menor preço se chama lohi, de low to high: do baixo pro alto.",
         {"type": "traducao", "codigo": "selectOption('lohi')", "partes": [["selectOption", "escolha a opção"], ["('lohi')", "low to high: do baixo pro alto"]], "passo": 2.4}),
        pausa(D52),
    ] + passos(C, ab, [
        (2, "Solução. Na caixa de ordenar, select option lohi: do menor pro maior.", "selectOption('lohi')"),
        (1, "E a conferência: como a gente conhece os produtos desse site de treino, o primeiro preço da lista tem que ser sete e noventa e nove.", "O primeiro preço: $7.99"),
    ]) + [
        ("Ponto first: o primeiro.", {"type": "traducao", "codigo": "getByTestId('inventory-item-price').first()", "partes": [[".first()", "o primeiro"]], "passo": 0.8}),
        ("Esse sete e noventa e nove é fixo porque o site de treino nunca muda os preços. Num sistema de verdade, preço muda, e esse teste quebraria. Aí o certo é conferir se a lista inteira está em ordem, sem número fixo. É isso que você faz no módulo 14.",
         {"type": "cards", "titulo": "$7.99 É UM NÚMERO FIXO", "itens": [["✓", "Site de treino", "o preço nunca muda", "#3fd68a"], ["✗", "Sistema de verdade", "o preço mudou, o teste quebra", VERM], ["⇅", "Módulo 14", "confere a lista inteira em ordem", AMARELO]]}),
        ("Roda.", rodando(C, ab, "Passou: $7.99 primeiro", [SEL], "run52", 52, logado=True)),
        ("Te vejo no próximo!", fim("PRÓXIMO: DESAFIO 5")),
    ], [1])

    # ---------- Aula 53 ----------
    D53 = desafio("5", "Logout", [["☰", "abre o menu"], ["⎋", "clica em Logout", AZUL], ["✓", "o botão de Login voltou", AMARELO]])
    C = cod(53); ed, ab = solucao(C, "test('desafio 5", "menu, logout e o botão de Login de volta")
    MENU = [{"click": "#react-burger-menu-btn", "espera": 1300}, {"click": "[data-test=\"logout-sidebar-link\"]", "espera": 1200}]
    aula(53, "Desafio 5 - logout", [
        ("Desafio cinco: sair do sistema.", titulo(53, "DESAFIO 5")),
        ("Por que testar o sair? Porque se ele falhar num computador compartilhado, a próxima pessoa entra direto na sua conta.",
         {"type": "cards", "itens": [["⎋", "Clicou em sair", "e achou que saiu"], ["✗", "Não saiu de verdade", "a próxima pessoa entra na sua conta", VERM]]}),
        ("O teste: abre o menu, clica em Logout, e confere que o botão de Login voltou.", D53),
        ("Dica: o menu é aquele botão de três risquinhos, com nome Open Menu. Lá dentro tem o Logout.",
         video("dica53", "☰ Open Menu › Logout", [{"click": "#react-burger-menu-btn", "espera": 2500}], logado=True, espera_fim=1500)),
        ("E o Logout: com o menu aberto, botão direito nele, e Inspecionar. Data-test igual logout sidebar link.",
         dev("dev53", "logout-sidebar-link", "Inspecionar: data-test=\"logout-sidebar-link\"", [{"click": "#react-burger-menu-btn"}], logado=True)),
        pausa(D53),
    ] + passos(C, ab, [
        (2, "Solução. Primeiro, abre o menu. O botão de três risquinhos não tem data-test, então a gente usa o get by role: um botão com o nome Open Menu.", "getByRole: o botão Open Menu"),
        (1, "Depois, clica no Logout, pelo data-test logout sidebar link.", "O clique no Logout"),
        (1, "E a conferência: o botão de login apareceu de novo. Se ele está visível, a pessoa saiu mesmo.", "O Login voltou: saiu mesmo"),
    ]) + [
        ("Roda.", rodando(C, ab, "Passou: saiu e o Login voltou", MENU, "run53", 53, logado=True)),
        ("Te vejo no desafio final!", fim("PRÓXIMO: DESAFIO FINAL")),
    ], [1])

    # ---------- Aula 54 ----------
    D54 = desafio("FINAL", "Compra com dois produtos", [["🎒", "mochila + lanterna da bike"], ["🛒", "carrinho, checkout e dados", AZUL], ["$", "confere o total", AMARELO], ["✓", "finaliza a compra", AMARELO]])
    C = cod(54); ed, ab = solucao(C, "test('desafio final", "Passo a passo", vel=0.85)
    DOIS = [{"click": "[data-test=\"add-to-cart-sauce-labs-backpack\"]"}, {"click": "[data-test=\"add-to-cart-sauce-labs-bike-light\"]"},
            {"click": "[data-test=\"shopping-cart-link\"]"}, {"click": "[data-test=\"checkout\"]"},
            {"fill": ["[data-test=\"firstName\"]", "Maria"]}, {"fill": ["[data-test=\"lastName\"]", "Silva"]}, {"fill": ["[data-test=\"postalCode\"]", "88000-000"]},
            {"click": "[data-test=\"continue\"]", "espera": 1500}]
    aula(54, "Desafio final - compra com dois produtos", [
        ("Desafio final: comprar dois produtos e conferir o total.", titulo(54, "DESAFIO FINAL")),
        ("Por que conferir o total? Porque é dinheiro: um erro de soma no carrinho é o tipo de bug que a empresa não pode deixar passar.",
         {"type": "cards", "itens": [["$", "O total", "é dinheiro"], ["✗", "Erro de soma", "não pode passar", VERM]]}),
        ("O teste: a mochila e a lanterna da bike, carrinho, checkout e dados, confere o total e finaliza a compra.", D54),
        ("Dica: a mochila e a lanterna da bicicleta, bike light. O total fica no data-test total-label. Com os preços desse site de treino, o total conhecido é quarenta e três e dezoito.",
         video("dica54", "total-label: $43.18", DOIS, logado=True, delay_letra=45, espera_fim=2500)),
        ("E o total, na tela de revisão: botão direito, e Inspecionar. Data-test igual total label.",
         dev("dev54", "total-label", "Inspecionar: data-test=\"total-label\"", DOIS, logado=True)),
        pausa(D54, "Agora sim: pausa o vídeo e tenta. Esse é maior, sem pressa. Quando voltar, a solução."),
    ] + passos(C, ab, [
        (4, "Solução, passo a passo. Adiciona a mochila e a lanterna, e confere que o carrinho mostra dois.", "Dois produtos: o carrinho mostra 2"),
        (6, "Vai pro carrinho, clica em checkout, preenche nome, sobrenome e CEP, e continua.", "Carrinho, checkout e dados"),
        (1, "Antes de finalizar, a conferência mais importante: o total contém quarenta e três e dezoito.", "O total: $43.18"),
        (2, "E por último, o finish, e a mensagem final: Thank you for your order.", "Finaliza e confere"),
    ]) + [
        ("De onde vem esse quarenta e três e dezoito? Da conta que o site faz:",
         {"type": "tela", "media": "tela54_total", "url": SAUCE, "acoes": LOGIN + DOIS, "alvo_css": ".summary_info", "titulo": "saucedemo.com", "legenda": "Item total, Tax e Total", "zoom_em": 1.0, "caixa_em": 1.6}),
        ("A mochila custa vinte e nove e noventa e nove, e a lanterna, nove e noventa e nove. Somando, trinta e nove e noventa e oito. Mais três e vinte de imposto: quarenta e três e dezoito.",
         {"type": "traducao", "titulo": "DE ONDE VEM O $43.18", "linhas": [["mochila", "$29.99"], ["+ lanterna", "$9.99"], ["= Item total", "$39.98"], ["+ Tax (imposto)", "$3.20"], ["= Total", "$43.18"]]}),
        ("Esse número só funciona porque o site de treino nunca muda os preços. Se amanhã a mochila custasse trinta, o total seria outro, e o teste ia falhar mesmo com o site funcionando certinho.",
         {"type": "cards", "titulo": "E SE O PREÇO MUDAR?", "itens": [["✓", "Hoje", "total $43.18: passa", "#3fd68a"], ["✗", "Mochila a $30.00", "o total muda: o teste quebra", VERM]]}),
        ("Numa loja de verdade, o certo é o teste fazer a conta sozinho: ler os preços da tela e somar. No módulo 14 você aprende a ler os preços da tela como número, que é o primeiro passo pra isso.",
         {"type": "cards", "titulo": "VALOR FIXO × CONTA", "itens": [["✓", "Site de treino", "valor fixo serve", "#3fd68a"], ["+", "Loja de verdade", "o teste soma os preços da tela", AMARELO]]}),
        ("Roda e olha o fluxo inteiro.", rodando(C, ab, "O fluxo inteiro, sozinho", DOIS + [{"click": "[data-test=\"finish\"]"}], "run54", 54, logado=True)),
        ("Se você conseguiu montar boa parte desse desafio sozinho, você já está juntando seletores, ações e conferências sem copiar um roteiro pronto. Esse é um grande passo.",
         bt(("SELETORES", "white", 110), ("AÇÕES", "white", 110), ("CONFERÊNCIAS", "gold", 130), entre=1.25)),
        ("Você terminou a parte do zero. A partir de agora, o nível sobe. Te vejo lá!", fim("PRÓXIMA: NÍVEL 2")),
    ], [1, 3])


def main():
    preencher()
    out = ["# Roteiros aprovados · Módulo 11 (gerado do roteiro_playwright_m11.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']}{' [+pausa]' if s.get('pausa') else ''} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo11.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

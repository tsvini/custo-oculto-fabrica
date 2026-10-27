"""Gera projetos/curso-playwright-17..21 (módulo 4: locators). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Código de cada aula = curso-playwright/projeto/tests/etapas/aulaNN.spec.js (validado no Actions).
Textos de erro e dados do site (XPath, classe, 20 botões, 5,1 s do usuário lento) vieram da sonda/demos rodadas no Actions."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m3 import codigo, ed, tela, vscode_term, ARV, SAUCE, LOGIN, CMD_HEADED

XPATH = "/html/body/div/div/div[2]/div[1]/div/div/form/div[1]/input"  # o "Copy full XPath" do campo Username (sonda)
CMD = "npx playwright test --project=chromium"


def edc(cod, legenda, arquivo="login.spec.js", **kw):
    """editor com um código montado aqui (trechos que não são o arquivo inteiro de uma etapa)"""
    d = {"type": "editor", "arquivo": arquivo, "pastas": ARV, "codigo": cod, "legenda": legenda, "fonte": 26, "digitar": False}
    if max(len(l) for l in cod.split("\n")) > 66:
        del d["pastas"]
    d.update(kw)
    return d


def cg(legenda, passos=(), modo="gravar", media="site_sauce_cg", **kw):
    """janela do codegen: navegador + Playwright Inspector (animado com os elementos reais do site)"""
    d = {"type": "pw_codegen", "modo": modo, "media": media, "url": SAUCE, "legenda": legenda,
         "inspecionar_varios": ["#user-name", "#password", "#login-button"], "passos_pw": list(passos)}
    d.update(kw)
    return d


U = "[data-test=\"username\"]"
P_CG = [{"linha": f"await page.locator('{U}').click();", "elem": 0},
        {"linha": f"await page.locator('{U}').fill('standard_user');", "elem": 0, "valor": "standard_user"},
        {"linha": "await page.locator('[data-test=\"password\"]').click();", "elem": 1},
        {"linha": "await page.locator('[data-test=\"password\"]').fill('secret_sauce');", "elem": 1, "valor": "secret_sauce", "senha": True},
        {"linha": "await page.locator('[data-test=\"login-button\"]').click();", "elem": 2}]
P_EXPECT = P_CG + [{"linha": "await expect(page.locator('[data-test=\"title\"]')).toContainText('Products');", "elem": 0}]



def real(media, legenda, video=True):
    """gravação real da tela (o codegen de verdade, gravado no Xvfb por ferramentas/codegen/aulas19e20.sh); arquivo em projetos/<aula>/midia/"""
    d = {"type": "tela_cheia", "media": media, "legenda": legenda}
    if video:
        d["gravar"] = True
    return d


AULAS = []

# ---------- Aula 17 ----------
AULAS.append(projeto(17, "MÓDULO 4 · AULA 17", "Como o Playwright acha os elementos", [
    ("Até agora você achou coisas na tela de três jeitos: pelo texto cinza do campo, pela função e pelo texto. Hoje você vê o mapa completo.", titulo(17, "LOCATORS")),
    ("Todo comando que acha um elemento começa com get by, que quer dizer: ache pelo. O que muda é o que vem depois.",
     {"type": "traducao", "codigo": "page.getByRole('button')", "partes": [["getBy", "ache pelo"], ["Role", "o que vem depois muda"]], "passo": 2.0}),
    ("get by role: ache pela função. Botão, link, campo, título. É o tipo de seletor que o Playwright recomenda, porque ele parte do que a pessoa usa na tela.",
     dict(tela("site_sauce_botao", "getByRole('button'): ache pela função botão", alvo_css="#login-button"))),
    ("get by text: ache pelo texto que aparece. get by placeholder: pelo texto cinza de dentro do campo. E get by label: pela etiqueta escrita do lado do campo.",
     {"type": "cards", "itens": [["Aa", "getByText", "pelo texto que aparece"], ["▭", "getByPlaceholder", "pelo texto cinza do campo", "#69a7ff"], ["🏷", "getByLabel", "pela etiqueta do lado do campo", "#ffd23f"]]}),
    ("E get by test id: ache por uma etiqueta que o próprio desenvolvedor deixou no código, só pra teste.",
     {"type": "devtools", "media": "site_sauce_dev", "url": SAUCE, "inspecionar": "#user-name", "aberto": True, "attrs": ["placeholder", "data-test", "id"],
      "realce": ["data-test"], "realce_em": 1.0, "realce_rotulo": "etiqueta de teste", "legenda": "getByTestId: a etiqueta data-test"}),
    ("Mas de onde vem tudo isso? Do código da página. Clica com o botão direito no campo Username e escolhe Inspecionar.",
     {"type": "devtools", "media": "site_sauce_dev", "url": SAUCE, "inspecionar": "#user-name", "legenda": "Botão direito › Inspecionar"}),
    ("Olha o que aparece: input, placeholder igual Username, e data-test igual username.",
     {"type": "devtools", "media": "site_sauce_dev", "url": SAUCE, "inspecionar": "#user-name", "aberto": True, "attrs": ["placeholder", "data-test", "id"],
      "realce": ["placeholder", "data-test"], "realce_em": 1.0, "realce_rotulo": "olha aqui", "legenda": "placeholder e data-test"}),
    ("Esse placeholder é o que o get by placeholder usa. E esse data-test é a tal etiqueta de teste.",
     {"type": "traducao", "codigo": "placeholder=\"Username\"  data-test=\"username\"", "texto_puro": True,
      "partes": [["placeholder=\"Username\"", "o getByPlaceholder usa este"], ["data-test=\"username\"", "a etiqueta de teste"]], "passo": 2.2}),
    ("Então o mesmo campo pode ser achado de mais de um jeito.",
     {"type": "compare", "title": "O MESMO CAMPO, DOIS CAMINHOS", "items": [["getByPlaceholder('Username')", "PELO TEXTO CINZA", "white"], ["[data-test=\"username\"]", "PELA ETIQUETA DE TESTE", "gold"]], "size": 60, "stagger": 1.0, "vs": False}),
    ("Qual usar? Prefira os seletores que representam o que a pessoa vê e usa: função, etiqueta, placeholder e texto. E quando o sistema tem uma etiqueta de teste estável, o test id também é uma boa opção.",
     {"type": "cards", "titulo": "QUAL USAR?", "itens": [["👁", "O que a pessoa vê", "função, etiqueta, placeholder, texto"], ["⚑", "Test id", "quando existe uma etiqueta estável", "#c792ea"]]}),
    ("Isso está na sua colinha, pra você não precisar decorar.", dict(bt(("ESTÁ NA SUA", "white", 110), ("COLINHA", "gold", 190)), colinha=True, colinha_em=0.6)),
    ("Na próxima aula: por que alguns seletores quebram o teste sem o site ter quebrado.", proxima("bons e maus seletores")[0]),
    ("Te vejo lá!", proxima("bons e maus seletores")[1]),
]))

# ---------- Aula 18 ----------
COD_STRICT = """import { test, expect } from '@playwright/test';

test('clica no botão', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
  await page.getByPlaceholder('Username').fill('standard_user');
  await page.getByPlaceholder('Password').fill('secret_sauce');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.getByRole('button').click();
});"""
ERRO_STRICT = [{"cmd": CMD, "em": 0.05},
               {"out": "Error: locator.click: Error: strict mode violation:", "cor": "#ff6b6b", "em": 0.3},
               {"out": "getByRole('button') resolved to 20 elements", "cor": "#ff6b6b", "em": 0.36}, {"out": "  1 failed", "cor": "#ff6b6b", "em": 0.5}]
AULAS.append(projeto(18, "MÓDULO 4 · AULA 18", "Bons e maus seletores - por que um teste quebra", [
    ("Um teste que quebra sem o site ter quebrado é o pior tipo de teste. E muitas vezes a causa é um seletor frágil.", titulo(18, "SELETORES")),
    ("Olha esse seletor, que muita gente copia do navegador: um caminho enorme, com div, div, form, div, input.",
     {"type": "traducao", "codigo": XPATH, "texto_puro": True, "partes": [[XPATH, "copiado do navegador: Copy full XPath"]], "passo": 1.5}),
    ("Traduzindo: dentro da div, dentro de outra div, dentro do formulário, o primeiro campo. Ele descreve o caminho até o campo, não o campo.",
     {"type": "traducao", "codigo": XPATH, "texto_puro": True, "partes": [["/div/div/div[2]/div[1]/div/div", "dentro de várias divs"], ["/form", "dentro do formulário"], ["/div[1]/input", "o primeiro campo"]], "passo": 2.2}),
    ("Se o desenvolvedor colocar uma div a mais, esse caminho deixa de existir e o teste quebra, mesmo com o login funcionando perfeitamente.",
     {"type": "compare", "title": "UMA DIV A MAIS NA PÁGINA", "items": [["…/div/div/form/…", "HOJE: ACHA O CAMPO", "white"], ["…/div/div/div/form/…", "AMANHÃ: NÃO ACHA MAIS", "red"]], "size": 60, "stagger": 1.4, "vs": False}),
    ("Outro exemplo frágil: achar pela classe de estilo, tipo ponto btn underline action. Classe de visual costuma mudar quando alguém mexe na aparência do site.",
     {"type": "traducao", "codigo": "class=\"submit-button btn_action\"", "texto_puro": True, "partes": [["btn_action", "classe de visual: muda com a aparência"]], "passo": 1.6}),
    ("Agora os bons: get by placeholder Username, get by role button chamado Login. Eles descrevem o que a pessoa vê na tela.",
     {"type": "traducao", "titulo": "OS BONS", "linhas": [["getByPlaceholder('Username')", "o campo com Username escrito"], ["getByRole('button', { name: 'Login' })", "o botão chamado Login"]]}),
    ("Regra prática: prefira seletores que representam o que a pessoa usa na tela. Quando isso não for suficiente, use uma etiqueta de teste estável, feita pra automação.",
     bt(("O QUE A PESSOA USA", "gold", 120), ("PRIMEIRO", "white", 100), ("DEPOIS, A ETIQUETA DE TESTE", "muted", 70))),
    ("É por isso que o get by test id é bom quando existe: a etiqueta foi criada só pra teste, e é bem mais difícil alguém mudar sem querer.",
     {"type": "cards", "titulo": "GET BY TEST ID", "itens": [["⚑", "Feita pra teste", "ninguém muda sem querer", "#c792ea"]]}),
    ("Mais um cuidado: o seletor precisa achar um elemento só. Se na página de produtos você pedir get by role button sem nome, ele acha um monte de botões, e o Playwright reclama.",
     edc(COD_STRICT, "Achou 20 botões: o Playwright reclama", arquivo="botao.spec.js", pastas=ARV[:4] + ["    botao.spec.js"] + ARV[4:], terminal=ERRO_STRICT, destaque=[8], destaque_em=0.6)),
    ("Esse erro se chama strict mode violation: modo rigoroso, achou mais de um. A solução é ser mais específico, colocando o nome do botão, por exemplo.",
     {"type": "traducao", "codigo": "strict mode violation: resolved to 20 elements", "texto_puro": True,
      "partes": [["strict mode", "modo rigoroso"], ["violation", "quebrou a regra"], ["resolved to 20 elements", "achou 20 elementos"]], "passo": 2.0}),
    ("Resumindo: o que ajuda e o que atrapalha.",
     {"type": "compare", "items": [["AJUDA", "FUNÇÃO, TEXTO, TEST ID", "gold"], ["ATRAPALHA", "CAMINHO, CLASSE DE VISUAL", "red"]], "size": 120, "stagger": 1.0, "vs": True}),
    ("Na próxima aula, o Playwright escreve o código pra você.", proxima("codegen")[0]),
    ("Te vejo lá!", proxima("codegen")[1]),
]))

# ---------- Aula 19 ----------
AULAS.append(projeto(19, "MÓDULO 4 · AULA 19", "Codegen - o Playwright escreve o código pra você", [
    ("E se o Playwright escrevesse o código pra você? Ele escreve.", titulo(19, "CODEGEN")),
    ("No terminal do VS Code, digita: npx playwright codegen, espaço, e o endereço do saucedemo.",
     vscode_term(16, "No terminal do VS Code", [{"cmd": "npx playwright codegen https://www.saucedemo.com/", "em": 0.25}], colinha=True, colinha_em=1.2)),
    ("Abrem duas janelas: o navegador, e o Playwright Inspector, que vai anotando tudo o que você faz.", real("cg_abre", "Navegador + Playwright Inspector", video=False)),
    ("Agora é só usar o site. Olha: eu clico no Username e digito standard user. A linha de código aparece sozinha.", real("cg19_usuario", "A linha aparece sozinha")),
    ("Senha, clique no Login. Cada coisa que você faz vira uma linha.", real("cg19_senha", "Cada ação vira uma linha")),
    ("Repara no seletor que ele escolheu. O codegen tenta achar um jeito bom e único de identificar cada elemento. Nem sempre é o mesmo que você escolheria, por isso a gente revisa o código gerado.",
     {"type": "traducao", "codigo": f"page.locator('{U}')", "partes": [["locator", "ache"], [f"'{U}'", "pela etiqueta de teste username"]], "passo": 2.2}),
    ("Na barra de cima tem botões pra criar conferências: conferir se algo está visível, ou se o texto está certo. Clica em um e depois no título Products. Pronto, apareceu um expect.",
     real("cg19_assert", "Assert text: apareceu um expect")),
    ("Quando terminar, copia o código e cola no seu arquivo.", edc(codigo(19), "Cola num arquivo novo", arquivo="codegen.spec.js")),
    ("Mas atenção: o codegen é um ponto de partida, não o teste pronto. Ele não sabe o que você quer conferir, e às vezes escolhe um seletor ruim. Sempre revisa.",
     {"type": "cards", "titulo": "PONTO DE PARTIDA", "itens": [["⚡", "Rápido", "descobre seletores e começa o teste"], ["✎", "Revise", "o nome, as conferências e os seletores", "#ff8c42"]]}),
    ("Use pra descobrir seletores e pra começar rápido. Depois, arruma com o que você aprendeu.", bt(("CODEGEN COMEÇA", "white", 120), ("VOCÊ TERMINA", "gold", 150), entre=1.35)),
    ("Na próxima aula: testando um seletor antes de usar.", proxima("pick locator")[0]),
    ("Te vejo lá!", proxima("pick locator")[1]),
]))

# ---------- Aula 20 ----------
AULAS.append(projeto(20, "MÓDULO 4 · AULA 20", "Pick Locator - testando um seletor antes de usar", [
    ("Às vezes você não sabe se um seletor vai funcionar. Dá pra testar antes de rodar o teste.", titulo(20, "PICK LOCATOR")),
    ("No codegen, clica no botão Pick locator, que quer dizer escolher seletor.", real("cg20_pick", "Pick locator = escolher seletor")),
    ("Passa o mouse em cima de qualquer coisa da página: ele mostra o seletor que usaria.",
     real("cg20_passa", "Ele mostra o seletor de cada coisa")),
    ("E dá pra fazer o contrário: escreve um seletor na caixinha, e ele pinta na página o que encontrou.",
     real("cg20_um", "Escreve o seletor: ele pinta o que achou")),
    ("Se pintou um elemento só, é um bom primeiro sinal: aí confere se o seletor também é claro e resistente a mudanças. Se pintou vários, ele está vago. Se não pintou nada, ele está errado.",
     real("cg20_varios", "Vários: vago · Nenhum: errado")),
    ("Testando o seletor antes, você evita rodar o teste várias vezes pra descobrir.", bt(("TESTE O SELETOR", "white", 120), ("ANTES", "gold", 190))),
    ("Na próxima aula: por que no Playwright você quase nunca precisa mandar o teste esperar.", proxima("espera automática")[0]),
    ("Te vejo lá!", proxima("espera automática")[1]),
]))

# ---------- Aula 21 ----------
C21 = codigo(21)
L21 = C21.split("\n")
C21_SEM_TIMEOUT = C21.replace("toBeVisible({ timeout: 10000 });", "toBeVisible();")
assert C21_SEM_TIMEOUT != C21
NOVO = "\n".join(L21[12:])  # o teste novo (linha 13 em diante), como aparece com o editor rolado até ele
AULAS.append(projeto(21, "MÓDULO 4 · AULA 21", "Espera automática - por que não precisa de sleep", [
    ("É comum encontrar testes com espera fixa: espera três segundos, depois clica. No Playwright, na maioria das vezes você não precisa disso.", titulo(21, "AUTO-WAIT")),
    ("Isso se chama auto-wait: espera automática.", {"type": "traducao", "codigo": "auto-wait", "texto_puro": True, "partes": [["auto", "automática"], ["wait", "espera"]], "passo": 1.2}),
    ("Antes de clicar, o Playwright confere sozinho se o elemento está pronto pra receber o clique: se está visível, parado, habilitado, e se nada está na frente dele.",
     {"type": "cards", "titulo": "ANTES DE CLICAR, ELE CONFERE", "itens": [["👁", "Visível", ""], ["⏸", "Parado", "sem animação", "#69a7ff"], ["✓", "Habilitado", "", "#ffd23f"], ["▢", "Nada na frente", "", "#c792ea"]]}),
    ("E os expects que conferem a página, como o to have URL e o to be visible, também tentam de novo. Por padrão, por até cinco segundos.",
     {"type": "cards", "titulo": "OS EXPECTS TAMBÉM ESPERAM", "itens": [["↻", "toHaveURL", "tenta de novo"], ["↻", "toBeVisible", "tenta de novo", "#69a7ff"], ["⏱", "5 segundos", "o padrão", "#ffd23f"]]}),
    ("Pra ver isso, vamos usar um usuário especial do saucedemo, o performance glitch user. Ele é lento de propósito.", tela("site_sauce_glitch", "O usuário lento de propósito", alvo="performance_glitch_user")),
    ("Cria um teste novo com esse usuário. É igual ao primeiro, só muda o nome do usuário.",
     edc(C21_SEM_TIMEOUT, "Teste novo: só muda o usuário", digitar=True, digitar_de=16, digitar_ate=16, rolar=True, rolar_de=1.2, rolar_dur=1.4, fonte=24)),
    ("Só que esse login às vezes passa de cinco segundos. Então, nessa conferência, a gente dá mais tempo: dentro dos parênteses do to be visible, escreve timeout dez mil.",
     edc(C21, "Mais tempo só nesta conferência", rolar=True, rolar_de=0.6, rolar_dur=0.8, fonte=24, trocar=[[19, C21.split("\n")[18].replace("toBeVisible({ timeout: 10000 })", "toBeVisible()"), None, 2.4]])),
    ("Traduzindo: timeout dez mil. São milissegundos: espere até dez segundos, só nessa conferência. Os outros expects continuam com cinco.",
     {"type": "traducao", "codigo": "toBeVisible({ timeout: 10000 })", "partes": [["timeout", "tempo máximo"], ["10000", "10 mil milissegundos = 10 segundos"]], "passo": 2.2}),
    ("Roda com o navegador aparecendo e olha: o clique em Login acontece, a página demora, e o teste espera sozinho até os produtos aparecerem.",
     edc(NOVO, "Ele espera sozinho", linha0=13, terminal=[{"cmd": CMD_HEADED, "em": 0.02}, {"out": "Running 2 tests using 2 workers", "cor": "mut", "em": 0.08}, {"out": "  2 passed (6.9s)", "cor": "ac", "em": 0.86}],
         navegador={"media": "rec_sauce_glitch", "url": SAUCE, "gravar": True, "acoes": [{"fill": ["#user-name", "performance_glitch_user"]}, {"fill": ["#password", "secret_sauce"]}, {"click": "#login-button"}],
                    "espera_inicio": 900, "espera_fim": 6000, "delay_letra": 60, "titulo": "Chromium", "em": 0.1, "ate": 0.84})),
    ("O que não fazer: page ponto wait for timeout três mil. Isso para o teste por três segundos sempre, mesmo quando o site já carregou. Deixa tudo lento, e ainda pode falhar se um dia demorar quatro.",
     {"type": "compare", "items": [["waitForTimeout(3000)", "ESPERA 3 s SEMPRE", "red"], ["auto-wait", "ESPERA SÓ O NECESSÁRIO", "gold"]], "size": 70, "stagger": 1.4, "vs": True}),
    ("Regra prática: confie na espera automática, e aumente o timeout só no lugar onde o sistema é lento de verdade.",
     bt(("CONFIE NA", "white", 110), ("ESPERA AUTOMÁTICA", "gold", 130), ("TIMEOUT SÓ ONDE PRECISA", "muted", 70))),
    ("Fechamos os locators! No próximo módulo, a gente organiza os testes.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Organizando os testes"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 5 · ORGANIZAÇÃO"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 4 (gerado do roteiro_playwright_m4.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo4.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

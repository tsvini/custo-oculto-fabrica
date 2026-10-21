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


def ed(n, legenda, de=None, ate=None, destaque=None, digitar=True, colinha=False, **kw):
    d = {"type": "editor", "arquivo": "login.spec.js", "pastas": ARV, "codigo": codigo(n), "legenda": legenda, "fonte": 26}
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
    ("Agora começa o seu código. E a primeira coisa é apagar o exemplo: clica com o botão direito no example ponto spec ponto js e escolhe Delete.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename...", "Delete"]], "caminho": [7], "pastas": ARV_EX, "ponto": [0.02, 0.18], "legenda": "Botão direito › Delete"}),
    ("Na pasta tests, cria um arquivo novo: login ponto spec ponto js.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [0], "pastas": ARV_SEM[:4], "ponto": [0.02, 0.12], "resultado": "arquivo", "novo": "login.spec.js", "novo_nivel": 2, "legenda": "tests › New File › login.spec.js"}),
    ("Primeira linha: import, chaves, test, vírgula, expect, fecha chaves, from, e entre aspas arroba playwright barra test. Ela traz duas ferramentas: o test, pra criar um teste, e o expect, pra conferir.",
     ed(12, "A primeira linha", ate=1, colinha=True, codigo=codigo(12).split("\n")[0])),
    ("Agora o teste: test, abre parênteses, o nome do teste entre aspas, entra com usuário e senha, vírgula, async, abre parênteses, abre chaves, page, fecha chaves, fecha parênteses, seta, e abre chaves. E lá embaixo, fecha com chave, parêntese e ponto e vírgula.",
     ed(12, "O esqueleto do teste", de=3)),
    ("Calma, eu explico cada pedaço. O nome entre aspas aparece no relatório, então escreve o que o teste faz, em português mesmo.", ed(12, "O nome aparece no relatório", digitar=False, destaque=[3], destaque_em=0.8)),
    ("O page é o navegador que o Playwright te entrega. É com ele que você abre sites e clica nas coisas.", ed(12, "page = o navegador", digitar=False, destaque=[3], destaque_em=0.8)),
    ("E o async quer dizer que, lá dentro, a gente vai usar o await, que significa: espera esse passo terminar antes de ir pro próximo.",
     {"type": "cards", "titulo": "ASYNC E AWAIT", "itens": [["⏳", "async", "aqui dentro tem espera"], ["⏸", "await", "espera esse passo terminar", "#69a7ff"]]}),
    ("Esse é o esqueleto de todo teste. Ainda está vazio, e na próxima aula a gente coloca o primeiro passo.", ed(12, "O esqueleto de todo teste", digitar=False)),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: PAGE.GOTO"}),
]))

AULAS.append(projeto(13, "MÓDULO 3 · AULA 13", "page.goto - abrindo um site", [
    ("Primeiro passo de todo teste: abrir o site.", titulo(13, "PAGE.GOTO")),
    ("Dentro do teste, digita await page ponto goto, e entre aspas o endereço: https dois pontos barra barra www ponto saucedemo ponto com.", ed(13, "await page.goto(endereço)", de=4, ate=4, colinha=True)),
    ("Esse é o site de treino que a gente vai usar no curso todo: uma lojinha feita pra quem está aprendendo a testar.", tela("site_sauce", "O site de treino")),
    ("Agora roda, mas dessa vez quero que você veja o navegador abrindo. No terminal: npx playwright test traço traço headed traço traço project igual chromium.", vterm(HEADED[:1], "--headed --project=chromium")),
    ("O headed mostra a janela, e o project igual chromium roda só no Chromium, pra ficar mais rápido.",
     dict({"type": "cards", "itens": [["▢", "--headed", "mostra a janela"], ["C", "--project=chromium", "só no Chromium", "#69a7ff"]]}, colinha=True, colinha_em=1.2)),
    ("Viu? O navegador abriu o site e fechou. O teste passou, porque abrir o site deu certo.", vterm(HEADED, "1 passou: o site abriu", ja=1)),
    ("Na próxima aula, a gente preenche o login.", proxima("fill: preenchendo campos")[0]),
    ("Te vejo lá!", proxima("fill: preenchendo campos")[1]),
]))

AULAS.append(projeto(14, "MÓDULO 3 · AULA 14", "fill - preenchendo campos", [
    ("Hoje o robô digita usuário e senha.", titulo(14, "FILL")),
    ("Mas antes: como ele sabe qual é o campo? Olha o site: dentro do primeiro campo está escrito Username, em cinza. Isso se chama placeholder.", tela("site_sauce_user", "O texto cinza: placeholder", alvo_css="#user-name")),
    ("E o Playwright acha campos exatamente por isso: page ponto getByPlaceholder, e entre aspas Username.", ed(14, "getByPlaceholder('Username')", de=5, ate=5, vel=0.5)),
    ("Depois, ponto fill, e o que digitar: standard underline user, o usuário de treino que o próprio site mostra embaixo.", tela("site_sauce_cred", "O site mostra o usuário de treino", alvo="standard_user")),
    ("O fill apaga o que tiver no campo e digita o texto novo.", dict({"type": "cards", "itens": [["⌫", "Apaga", "o que tinha"], ["⌨", "Digita", "o texto novo", "#69a7ff"]]}, colinha=True, colinha_em=1.0)),
    ("A senha é igual: getByPlaceholder Password, fill secret underline sauce.", ed(14, "A senha é igual", de=6, ate=6)),
    ("Roda com o headed e olha o robô digitando.", tela("site_sauce_preenchido", "O robô digitou!", acoes=LOGIN[:2], alvo_css="#password")),
    ("Na próxima aula, a gente clica em Login e confere se deu certo.", proxima("click e expect")[0]),
    ("Te vejo lá!", proxima("click e expect")[1]),
]))

AULAS.append(projeto(15, "MÓDULO 3 · AULA 15", "click e expect - conferindo o resultado", [
    ("Hoje o teste fica completo: clicar e conferir.", titulo(15, "CLICK E EXPECT")),
    ("Pra achar o botão, a gente usa o getByRole: o papel dele é button, de botão, e o nome é o texto escrito nele, Login.", tela("site_sauce_botao", "Papel: botão · Nome: Login", alvo_css="#login-button")),
    ("Digita: await page ponto getByRole, abre parênteses, aspas button, vírgula, chaves, name dois pontos, aspas Login, fecha tudo, ponto click.", ed(15, "getByRole('button', { name: 'Login' })", de=7, ate=7)),
    ("Agora a parte mais importante do teste: a conferência. Se logou, o endereço do site muda pra inventory.",
     tela("site_sauce_products", "O endereço mudou pra inventory", acoes=LOGIN, alvo="Products", titulo_t="saucedemo.com/inventory.html")),
    ("Então: await expect, abre parênteses, page, fecha parênteses, ponto toHaveURL, e entre barras, inventory. Essas barras criam uma busca por padrão. Nesse caso, a gente está dizendo que a URL precisa ter a palavra inventory em algum lugar.",
     ed(15, "await expect(page).toHaveURL(/inventory/)", de=8, ate=8, colinha=True)),
    ("Sem o expect, o teste só clica. Ele não confere nada, e passaria até se o login desse errado.",
     {"type": "compare", "title": "O EXPECT FAZ A DIFERENÇA", "items": [["SEM EXPECT", "SÓ CLICA", "red"], ["COM EXPECT", "CONFERE DE VERDADE", "gold"]], "size": 120, "stagger": 1.2, "vs": True}),
    ("Roda. Passou! Esse é o seu primeiro teste completo: abre, preenche, clica e confere.",
     {"type": "cards", "titulo": "TODO TESTE É ASSIM", "itens": [["1", "Abre", "goto"], ["2", "Acha", "getBy...", "#69a7ff"], ["3", "Faz", "fill, click", "#ffd23f"], ["4", "Confere", "expect", "#ff6b6b"]]}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: OS EXPECT MAIS USADOS"}),
]))

AULAS.append(projeto(16, "MÓDULO 3 · AULA 16", "Os expect mais usados", [
    ("O expect é o coração do teste, então vale conhecer os mais usados.", titulo(16, "OS EXPECT")),
    ("toHaveURL você já conhece: confere o endereço.", ed(16, "toHaveURL: o endereço", digitar=False, destaque=[8], destaque_em=0.8, codigo="\n".join(codigo(16).split("\n")[:8] + ["});"]))),
    ("toBeVisible confere se algo está aparecendo na tela. Por exemplo, o título Products: await expect, page ponto getByText Products, ponto toBeVisible.", ed(16, "toBeVisible: está aparecendo", de=9, ate=9, colinha=True)),
    ("toContainText confere se um texto aparece no meio de outro. O nome do primeiro produto contém Backpack: await expect, e ponto toContainText Backpack.", ed(16, "toContainText: tem esse texto", de=10, ate=10)),
    ("E toHaveCount confere quantos existem. Na loja tem seis botões Add to cart, um pra cada produto: await expect, getByRole button Add to cart, ponto toHaveCount seis.", ed(16, "toHaveCount: quantos existem", de=11, ate=11)),
    ("Tem também o toHaveText, que confere o texto exato, e o not, que faz o contrário de qualquer um. Todos estão na sua colinha.",
     dict({"type": "cards", "itens": [["=", "toHaveText", "o texto exato"], ["!", "not", "o contrário", "#ff6b6b"]]}, colinha=True, colinha_em=1.0)),
    ("E um detalhe que faz o Playwright brilhar: os expect do Playwright esperam automaticamente por alguns segundos até a condição ficar verdadeira. Por padrão, esse tempo é de até cinco segundos.",
     bt(("ELE ESPERA", "gold", 170), ("SOZINHO", "white", 150), ("ATÉ 5 SEGUNDOS", "muted", 80))),
    ("Roda, e tudo passa. No próximo módulo, a gente aprende a achar qualquer elemento, e eu te mostro um truque em que o Playwright escreve o código pra você.",
     vterm([{"cmd": "npx playwright test --project=chromium"}, {"out": "Running 1 test using 1 worker", "cor": "mut"}, {"out": "  1 passed (2.6s)", "cor": "ac"}], "Tudo passou!")),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 4 · LOCATORS"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 3 (com ajustes da revisão)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo3.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

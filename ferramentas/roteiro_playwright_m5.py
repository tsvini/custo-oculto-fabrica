"""Gera projetos/curso-playwright-22..25 (módulo 5: organização). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Código = curso-playwright/projeto/tests/etapas/aulaNN.spec.js (validado no Actions); only/skip validados em demos/."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m3 import codigo, ARV, SAUCE, LOGIN
from roteiro_playwright_m4 import edc, CMD

REF = os.path.join(RAIZ, "curso-playwright", "referencia_init")
CONFIG = open(os.path.join(REF, "playwright.config.js"), encoding="utf8").read().rstrip("\n").split("\n")
GITIGNORE = open(os.path.join(REF, ".gitignore"), encoding="utf8").read().rstrip("\n")
C16, C21, C22, C23, C24 = (codigo(n) for n in (16, 21, 22, 23, 24))
ARV_ENV = ARV[:5] + ["  .env"] + ARV[5:]
ARV_EX = ARV[:5] + ["  .env", "  .env.example"] + ARV[5:]


def topo(cod, n=10):
    """o começo do arquivo, como aparece no editor com o terminal aberto embaixo"""
    return "\n".join(cod.split("\n")[:n])


def vs(cod, legenda, terminal, arquivo="login.spec.js", n=10, **kw):
    return edc(topo(cod, n), legenda, arquivo=arquivo, terminal=terminal, **kw)


def run(*saida, cmd=CMD, em=0.05):
    L = [{"cmd": cmd, "em": em}]
    for i, (txt, cor) in enumerate(saida):
        L.append({"out": txt, "cor": cor, "em": [0.3, 0.55, 0.62, 0.68][min(i, 3)]})
    return L


def cfg(linhas):
    """trecho do playwright.config.js (com as linhas de verdade do arquivo e a numeração certa)"""
    return "\n".join(linhas)


# ---------- passos intermediários da aula 22 (o arquivo antes do describe) ----------
TESTE_BLOQ = """test('mostra erro para usuário bloqueado', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
  await page.getByPlaceholder('Username').fill('locked_out_user');
  await page.getByPlaceholder('Password').fill('secret_sauce');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.getByText('locked out')).toBeVisible();
});"""
DOIS = C16 + "\n\n" + TESTE_BLOQ  # linhas 1-11 = teste da aula 16; 13-18 = teste novo
LD = DOIS.split("\n")
L_T2 = [i + 1 for i, l in enumerate(LD) if "mostra erro" in l][0]       # o test do bloqueado
L_GOTOS = [i + 1 for i, l in enumerate(LD) if "page.goto" in l]           # os dois goto
assert len(L_GOTOS) == 2 and L_GOTOS[1] == L_T2 + 1
GOTO = "  await page.goto('https://www.saucedemo.com/');\n"
BE = """test.beforeEach(async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
});

"""
COM_BE = DOIS.replace(GOTO, "", 2).replace("import { test, expect } from '@playwright/test';\n\n", "import { test, expect } from '@playwright/test';\n\n" + BE)
assert COM_BE.count("page.goto") == 1 and "  await page.goto" in COM_BE.split("\n")[3]

AULAS = []

# ---------- Aula 22 ----------
REL22 = [["Login › entra com usuário e senha", "login.spec.js:8", "chromium", "ok", "1.1s"], ["Login › mostra erro para usuário bloqueado", "login.spec.js:18", "chromium", "ok", "0.7s"]]
AULAS.append(projeto(22, "MÓDULO 5 · AULA 22", "describe e beforeEach", [
    ("O seu arquivo vai crescer. Hoje você aprende a deixar ele organizado.", titulo(22, "ORGANIZANDO")),
    ("Antes, apaga aquele teste do usuário lento. Ele era só pra você ver a espera automática.",
     edc(C21, "Apaga o teste do usuário lento", rolar=True, rolar_de=1.0, rolar_dur=1.2, destaque=list(range(14, 21)), destaque_em=2.4, fonte=24)),
    ("Agora vamos criar um segundo teste. O saucedemo tem um usuário que não consegue entrar: o usuário bloqueado, locked underline out underline user.",
     {"type": "tela", "media": "rec_sauce_locked", "url": SAUCE, "gravar": True, "titulo": "saucedemo.com", "legenda": "O usuário bloqueado não entra",
      "acoes": [{"fill": ["#user-name", "locked_out_user"]}, {"fill": ["#password", "secret_sauce"]}, {"click": "#login-button"}], "espera_fim": 2200, "delay_letra": 70}),
    ("Escreve o teste novo embaixo do primeiro. Ele preenche o usuário bloqueado e espera ver a mensagem locked out.",
     edc(DOIS, "O teste do usuário bloqueado", digitar=True, digitar_de=L_T2, rolar=True, rolar_de=0.8, rolar_dur=1.0, fonte=24)),
    ("Repara: a linha do goto se repete nos dois testes.", edc(DOIS, "O goto se repete", destaque=L_GOTOS, destaque_em=0.6, rolar=True, rolar_de=2.2, rolar_dur=1.4, fonte=24)),
    ("Quando algo se repete antes de todo teste, existe o before each. Before each: antes de cada.",
     {"type": "traducao", "codigo": "test.beforeEach(async ({ page }) => {", "partes": [["before", "antes de"], ["Each", "cada"], ["({ page })", "me dê o navegador"]], "passo": 2.0}),
    ("Coloca o goto lá dentro, e apaga dos testes.", edc(COM_BE, "O goto vai pro beforeEach", destaque=[3, 4, 5], destaque_em=0.6, rolar=True, rolar_de=2.6, rolar_dur=1.6, fonte=24)),
    ("Agora o describe. Describe é descrever: ele junta testes do mesmo assunto numa caixa com nome.",
     {"type": "traducao", "codigo": "test.describe('Login', () => {", "partes": [["describe", "junte numa caixa"], ["'Login'", "com o nome Login"]], "passo": 2.0}),
    ("Logo depois do import, escreve: test ponto describe, abre parênteses, entre aspas Login, vírgula, abre e fecha parênteses, seta, e abre chaves.",
     edc("\n".join(C22.replace("aula 22: ", "").split("\n")[:12]), "test.describe('Login', () => {", digitar=True, digitar_de=3, digitar_ate=3, fonte=26, destaque=[3], destaque_em=4.5)),
    ("E lá no final do arquivo, fecha a caixa: chave, parêntese e ponto e vírgula. Os dois testes e o before each ficam aqui dentro.",
     edc("\n".join(C22.replace("aula 22: ", "").split("\n")[12:]), "}); fecha a caixa do describe", linha0=13, digitar=True, digitar_de=12, digitar_ate=12, fonte=26, destaque=[12], destaque_em=2.0)),
    ("Tudo que está dentro desse describe é sobre login.", edc(C22.replace("aula 22: ", ""), "Tudo aqui dentro é sobre login", fonte=22, destaque=[3, 24], destaque_em=0.3, rolar=True, rolar_de=0.6, rolar_dur=1.8)),
    ("Lendo em português: um grupo chamado Login. Antes de cada teste, abra o site. Teste um: entra. Teste dois: mostra erro pro bloqueado.",
     {"type": "cards", "itens": [["▣", "Grupo Login", "describe"], ["↺", "Antes de cada", "abra o site", "#69a7ff"], ["1", "Teste 1", "entra", "#ffd23f"], ["2", "Teste 2", "erro do bloqueado", "#c792ea"]]}),
    ("Roda: os dois passam.", vs(C22, "Os dois passam", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.1s)", "ac")))),
    ("E no relatório eles aparecem juntos, debaixo de Login.", {"type": "pw_relatorio", "testes": REL22, "legenda": "Juntos, debaixo de Login"}),
    ("Na próxima aula: o arquivo de configuração.", proxima("playwright.config")[0]),
    ("Te vejo lá!", proxima("playwright.config")[1]),
]))

# ---------- Aula 23 ----------
USE0 = 26  # o trecho do config que aparece: linhas 26 a 34 (reporter, use e o fim do use)
CFG_USE = CONFIG[USE0 - 1:34]
CFG_BASE = [l if "// baseURL" not in l else "    baseURL: 'https://www.saucedemo.com'," for l in CFG_USE]
CFG_TID = CFG_BASE[:5] + ["    testIdAttribute: 'data-test',"] + CFG_BASE[5:]
assert CFG_USE[2].strip() == "use: {" and "baseURL" in CFG_BASE[4]
AULAS.append(projeto(23, "MÓDULO 5 · AULA 23", "playwright.config - baseURL e data-test", [
    ("Hoje a gente mexe no arquivo de configuração. Parece assustador, mas são só duas linhas.", titulo(23, "CONFIG")),
    ("Abre o playwright ponto config ponto js e procura o use. Use quer dizer: use isso em todos os testes.",
     edc(cfg(CFG_USE), "use = use isso em todos os testes", arquivo="playwright.config.js", linha0=USE0, destaque=[3], destaque_em=1.0, fonte=26)),
    ("Tira o comentário da baseURL e coloca o endereço do saucedemo. Base URL: o endereço base.",
     edc(cfg(CFG_BASE), "baseURL = o endereço base", arquivo="playwright.config.js", linha0=USE0, digitar=True, digitar_de=5, digitar_ate=5, fonte=26)),
    ("Agora, no teste, o goto fica só com uma barra. O Playwright junta essa barra com o endereço base.",
     edc(C22.replace("aula 22: ", "").replace("page.goto('https://www.saucedemo.com/')", "page.goto('/')"), "baseURL + /  =  saucedemo.com/", digitar=True, digitar_de=5, digitar_ate=5, fonte=22, rolar_depois=True)),
    ("A vantagem: se um dia o site mudar de endereço, você troca num lugar só.",
     {"type": "cards", "itens": [["⌂", "baseURL", "o endereço num lugar só"], ["/", "page.goto('/')", "nos testes, só o caminho", "#69a7ff"]]}),
    ("Segunda linha: test id attribute igual data-test. Lembra do data-test que a gente viu no Inspecionar?",
     edc(cfg(CFG_TID), "testIdAttribute: 'data-test'", arquivo="playwright.config.js", linha0=USE0, digitar=True, digitar_de=6, digitar_ate=6, fonte=26)),
    ("Por padrão, o get by test id procura data-testid. O saucedemo usa data-test. Essa linha avisa o Playwright.",
     {"type": "compare", "items": [["data-testid", "O PADRÃO DO PLAYWRIGHT", "white"], ["data-test", "O QUE O SAUCEDEMO USA", "gold"]], "size": 90, "stagger": 1.2, "vs": True}),
    ("Agora o get by test id também funciona no saucedemo. Pra você ver esse outro caminho, a gente vai trocar os seletores que já estão nos testes. Repara: o before each continua igual, ele só abre o site.",
     edc("\n".join(C23.replace("aula 23: ", "").split("\n")[:12]), "O beforeEach só abre o site", fonte=24, destaque=[4, 5, 6], destaque_em=3.0)),
    ("A troca é assim: onde estava get by placeholder Username, fica get by test id username. A senha vira password. E o botão vira login button.",
     {"type": "traducao", "titulo": "A MESMA COISA, OUTRO SELETOR", "linhas": [["getByPlaceholder('Username')", "getByTestId('username')"], ["getByPlaceholder('Password')", "getByTestId('password')"],
                                                                           ["getByRole('button', { name: 'Login' })", "getByTestId('login-button')"]]}),
    ("No primeiro teste, as três linhas do login trocadas.",
     edc("\n".join(C23.replace("aula 23: ", "").split("\n")[7:12]), "Teste 1: os três seletores trocados", linha0=8, digitar=True, digitar_de=2, digitar_ate=4, fonte=28)),
    ("E no segundo teste, a mesma troca. Os seletores antigos também estavam certos: é só outro caminho pro mesmo lugar.",
     edc("\n".join(C23.replace("aula 23: ", "").split("\n")[17:24]), "Teste 2: a mesma troca", linha0=18, digitar=True, digitar_de=2, digitar_ate=4, fonte=24)),
    ("Traduzindo: ache pela etiqueta de teste chamada username.",
     {"type": "traducao", "codigo": "page.getByTestId('username')", "partes": [["getByTestId", "ache pela etiqueta de teste"], ["'username'", "chamada username"]], "passo": 2.0}),
    ("Roda pra confirmar que tudo continua passando.", vs(C23, "Tudo continua passando", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.0s)", "ac")))),
    ("Na próxima aula: tirando o usuário e a senha do código.", proxima("variáveis de ambiente")[0]),
    ("Te vejo lá!", proxima("variáveis de ambiente")[1]),
]))

# ---------- Aula 24 ----------
ENV = "SAUCE_USER=standard_user\nSAUCE_PASSWORD=secret_sauce"
CFG_TOPO = CONFIG[:15]
CFG_DOTENV = [re.sub(r"^// ", "", l) if ("dotenv" in l or "import path" in l) and l.startswith("// ") else l for l in CFG_TOPO]
assert sum(1 for a, b in zip(CFG_TOPO, CFG_DOTENV) if a != b) == 3
AULAS.append(projeto(24, "MÓDULO 5 · AULA 24", "Variáveis de ambiente - tirando usuário e senha do código", [
    ("Aqui no saucedemo o usuário e a senha são públicos. Mas em projeto de verdade, senha e chave escrita no código é um problema: quando o projeto for pro GitHub, todo mundo vê.",
     titulo(24, ".ENV")),
    ("Então a gente vai aprender o jeito usado em projetos reais: um arquivo chamado ponto env, que guarda essas informações fora do código.",
     {"type": "cards", "titulo": "O ARQUIVO .ENV", "itens": [["🔒", ".env", "usuário e senha fora do código"]]}),
    ("A ideia é simples. O ponto env fica só no seu computador. O teste não tem mais a senha escrita: ele pede pro ponto env. E cada pessoa do time coloca o próprio usuário e a própria senha no ponto env dela.",
     {"type": "cards", "itens": [["💻", "Fica no seu computador", "não vai pro GitHub"], ["📄", "O teste pede", "pro .env", "#69a7ff"], ["👥", "Cada pessoa", "com o seu usuário e senha", "#ffd23f"]]}),
    ("Pra ler esse arquivo, a gente usa um pacote chamado dotenv. Pacote é um código pronto que alguém já escreveu e que você baixa pro seu projeto.",
     {"type": "cards", "titulo": "PACOTE", "itens": [["📦", "dotenv", "um código pronto que lê o .env"]]}),
    ("No terminal: npm install traço D dotenv. Install quer dizer instalar. E o traço D marca como ferramenta de desenvolvimento do projeto.",
     vs(C23, "npm install -D dotenv", run(("added 1 package, and audited 6 packages in 1s", "mut"), ("found 0 vulnerabilities", "ac"), cmd="npm install -D dotenv"))),
    ("Na pasta do projeto, cria o arquivo ponto env.",
     {"type": "menu", "app": "vscode", "barra": [], "menus": [["New File...", "New Folder...", "—", "Cut", "Copy", "—", "Rename..."]], "caminho": [0], "pastas": ARV, "alvo_item": "meu-primeiro-playwright",
      "novo_pos": 5, "resultado": "arquivo", "novo": ".env", "novo_nivel": 1, "legenda": "New File › .env"}),
    ("Dentro: SAUCE underline USER igual standard user, e SAUCE underline PASSWORD igual secret sauce.",
     edc(ENV, "Usuário e senha no .env", arquivo=".env", pastas=ARV_ENV, digitar=True, fonte=32)),
    ("E antes de qualquer outra coisa: o ponto gitignore. Ignore é ignorar: é a lista de arquivos que o Git deixa de fora quando você manda o projeto pro GitHub. Escreve ponto env no final dele.",
     edc(GITIGNORE + "\n.env", ".env no .gitignore", arquivo=".gitignore", pastas=ARV_ENV, digitar=True, digitar_de=len(GITIGNORE.split("\n")) + 1, fonte=30)),
    ("Agora o config. Lá em cima já tem três linhas do dotenv, só que comentadas: com as duas barras na frente, o Playwright ignora. Apaga as duas barras das três linhas.",
     edc("\n".join(CFG_DOTENV), "Tira as duas barras das 3 linhas", arquivo="playwright.config.js", pastas=ARV_ENV, digitar=True, digitar_de=8, digitar_ate=10, fonte=22)),
    ("Lendo em português: importe o dotenv, importe o path, que cuida dos caminhos das pastas, e leia o arquivo ponto env que está nesta pasta.",
     {"type": "traducao", "titulo": "AS 3 LINHAS DO DOTENV", "linhas": [["import dotenv from 'dotenv';", "traga o dotenv"], ["import path from 'path';", "traga o path (caminhos)"],
                                                                     ["dotenv.config({ path: ... '.env' })", "leia o .env desta pasta"]]}),
    ("No teste, onde estava escrito standard user, troca por process ponto env ponto SAUCE underline USER. E a senha, por process ponto env ponto SAUCE underline PASSWORD.",
     edc("\n".join(C24.replace("aula 24: ", "").split("\n")[7:12]), "O teste pede pro .env", linha0=8, pastas=ARV_ENV, digitar=True, digitar_de=2, digitar_ate=3, fonte=22)),
    ("No segundo teste, o usuário bloqueado continua escrito, porque ele é o que o teste quer testar. Só a senha vem do ponto env.",
     edc("\n".join(C24.replace("aula 24: ", "").split("\n")[17:24]), "Teste 2: só a senha vem do .env", linha0=18, pastas=ARV_ENV, digitar=True, digitar_de=3, digitar_ate=3, fonte=22)),
    ("Traduzindo: process ponto env, as variáveis do ambiente. SAUCE underline USER, a variável com esse nome. Quando o teste roda, o dotenv já leu o arquivo, e aqui entra o standard user.",
     {"type": "traducao", "codigo": "process.env.SAUCE_USER", "partes": [["process.env", "as variáveis do ambiente"], ["SAUCE_USER", "a chamada SAUCE_USER"]], "passo": 2.0}),
    ("E pra quem baixar o projeto saber o que preencher, cria um ponto env ponto example só com os nomes das variáveis, sem os valores.",
     edc("SAUCE_USER=\nSAUCE_PASSWORD=", "Só os nomes, sem os valores", arquivo=".env.example", pastas=ARV_EX, digitar=True, fonte=32)),
    ("Roda pra confirmar: continua passando.", vs(C24, "Continua passando", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.0s)", "ac")), pastas=ARV_EX)),
    ("Na próxima aula: rodando só o que importa.", proxima("only, skip e filtros")[0]),
    ("Te vejo lá!", proxima("only, skip e filtros")[1]),
]))

# ---------- Aula 25 ----------
C25_ONLY = C24.replace("aula 24: ", "").replace("test('mostra erro", "test.only('mostra erro")
C25_SKIP = C24.replace("aula 24: ", "").replace("test('mostra erro", "test.skip('mostra erro")
L_ONLY = [i + 1 for i, l in enumerate(C25_ONLY.split("\n")) if "test.only" in l][0]
AULAS.append(projeto(25, "MÓDULO 5 · AULA 25", "Rodando só o que importa - only, skip, arquivo e nome", [
    ("Quando você tiver dezenas de testes, não vai querer rodar todos toda hora.", titulo(25, "SÓ O QUE IMPORTA")),
    ("Pra rodar um arquivo só, coloca o nome dele: npx playwright test login ponto spec ponto js.",
     vs(C24, "Um arquivo só", run(("Running 6 tests using 4 workers", "mut"), ("  6 passed (4.3s)", "ac"), cmd="npx playwright test login.spec.js"), pastas=ARV_EX)),
    ("Pra rodar pelo nome do teste: traço g e um pedaço do nome, tipo bloqueado. O g vem de grep, que quer dizer procurar: ele filtra os testes por esse pedaço de nome.",
     vs(C24, "-g = grep = procurar pelo nome", run(("Running 3 tests using 3 workers", "mut"), ("  3 passed (2.2s)", "ac"), cmd="npx playwright test -g bloqueado"), pastas=ARV_EX)),
    ("Dentro do código, test ponto only: roda somente esse teste. Only quer dizer somente.",
     edc(C25_ONLY, "only = somente", pastas=ARV_EX, digitar=True, digitar_de=L_ONLY, digitar_ate=L_ONLY, rolar=True, rolar_de=0.8, rolar_dur=1.0, fonte=22)),
    ("Cuidado: esquecer um only é um erro clássico. Os outros testes param de rodar e ninguém percebe. Por isso o config já vem com forbid only, que trava isso no GitHub.",
     {"type": "cards", "itens": [["⚠", "Esqueceu o only?", "os outros param de rodar", "#ff8c42"], ["🛡", "forbidOnly", "trava isso no GitHub", "#69a7ff"]]}),
    ("E test ponto skip: pula esse teste. Skip quer dizer pular. No resultado, ele aparece como skipped.",
     edc("\n".join(C25_SKIP.split("\n")[L_ONLY - 4:L_ONLY + 4]), "skip = pular: aparece como skipped", linha0=L_ONLY - 3, pastas=ARV_EX, destaque=[4], destaque_em=0.6,
         terminal=run(("Running 2 tests using 1 worker", "mut"), ("  1 skipped", "yel"), ("  1 passed (1.8s)", "ac")))),
    ("E você já conhece o traço traço project igual chromium, pra rodar num navegador só.",
     {"type": "cards", "itens": [["C", "--project=chromium", "só esse navegador"]]}),
    ("Resumindo: o nome do arquivo roda só aquele arquivo. Traço g filtra pelo nome do teste. Test ponto only roda somente aquele teste. Test ponto skip pula. E traço traço project escolhe o navegador.",
     {"type": "traducao", "titulo": "RODANDO SÓ O QUE IMPORTA", "linhas": [["npx playwright test login.spec.js", "só esse arquivo"], ["npx playwright test -g bloqueado", "só os testes com esse nome"],
                                                                         ["test.only(...)", "somente esse teste"], ["test.skip(...)", "pula esse teste"], ["--project=chromium", "só esse navegador"]]}),
    ("Fechamos a organização. No próximo módulo: o que fazer quando o teste falha.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Debug: quando o teste falha"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 6 · DEBUG"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 5 (gerado do roteiro_playwright_m5.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo5.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

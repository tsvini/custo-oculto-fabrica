"""Gera projetos/curso-playwright-31..34 (módulo 7: testes reais). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Código = tests/etapas/aula32.spec.js (validado). Ajuste técnico: com o nome fixo dentro do for, o Playwright recusa
("duplicate test title", saída real de demos/aula31_repetido.demo.spec.js) — a aula 32 abre mostrando esse erro."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m3 import codigo, ARV, SAUCE, LOGIN, CMD_HEADED
from roteiro_playwright_m4 import edc, CMD
from roteiro_playwright_m5 import vs, CONFIG, ARV_EX

ARV_U = ARV_EX[:ARV_EX.index("    login.spec.js") + 1] + ["    usuarios.spec.js"] + ARV_EX[ARV_EX.index("    login.spec.js") + 1:]
C32 = codigo(32).replace("aula 32: ", "")
C31 = C32.replace("test(`login funciona para ${usuario}`", "test('login funciona'")
assert C31 != C32
L31 = C31.split("\n")
LISTA = L31[2]                       # const usuarios = [...];
L_FOR = 5                            # for (const usuario of usuarios) {
L_TEST = 6
L_FILL = [i + 1 for i, l in enumerate(L31) if "fill(usuario)" in l][0]
L_TIME = [i + 1 for i, l in enumerate(L31) if "timeout: 10000" in l][0]
assert L31[L_FOR - 1].startswith("for (") and "test(" in L31[L_TEST - 1]
VERM = "#ff6b6b"


def run(*saida, cmd=CMD):
    L = [{"cmd": cmd, "em": 0.05}]
    for i, (txt, cor) in enumerate(saida):
        L.append({"out": txt, "cor": cor, "em": [0.3, 0.5, 0.6, 0.68][min(i, 3)]})
    return L


AULAS = []

# ---------- Aula 31 ----------
USU4 = ["standard_user", "problem_user", "performance_glitch_user", "visual_user"]
AULAS.append(projeto(31, "MÓDULO 7 · AULA 31", "Uma lista de usuários e um teste que se repete", [
    ("O saucedemo tem vários usuários que entram normalmente: standard, problem, performance glitch e visual.",
     {"type": "tela", "media": "site_sauce_users", "url": SAUCE, "titulo": "saucedemo.com", "legenda": "Vários usuários", "alvo_css": "[data-test=\"login-credentials\"]", "zoom_em": 1.4, "caixa_em": 2.0}),
    ("E o teste do login é igual pra todos: abre o site, preenche, clica e confere. A única coisa que muda é o nome do usuário.",
     {"type": "traducao", "titulo": "4 TESTES IGUAIS: SÓ MUDA O NOME", "linhas": [["fill('standard_user')", "teste 1"], ["fill('problem_user')", "teste 2"], ["fill('performance_glitch_user')", "teste 3"], ["fill('visual_user')", "teste 4"]]}),
    ("Dá pra copiar o teste quatro vezes? Dá. Mas aí, se o botão de login mudar, você conserta em quatro lugares. E pra testar um quinto usuário, copia tudo de novo.",
     {"type": "cards", "titulo": "COPIAR 4 VEZES", "itens": [["⧉", "4 cópias", "do mesmo teste", "#ff8c42"], ["✎", "O botão mudou?", "conserta em 4 lugares", VERM], ["+", "Mais um usuário?", "copia tudo de novo", "#ffd23f"]]}),
    ("E isso acontece muito num sistema de verdade: cliente, administrador, usuário novo. O mesmo teste precisa funcionar pra todos.",
     {"type": "cards", "titulo": "NUM SISTEMA DE VERDADE", "itens": [["👤", "Cliente", "faz compras"], ["🛠", "Administrador", "gerencia a loja", "#69a7ff"], ["🆕", "Usuário novo", "primeiro acesso", "#ffd23f"]]}),
    ("A solução tem duas partes: uma lista com os nomes, e uma repetição que roda o teste uma vez pra cada nome da lista.",
     {"type": "cards", "titulo": "A SOLUÇÃO", "itens": [["[ ]", "Uma lista", "com os nomes"], ["↻", "Uma repetição", "roda o teste pra cada nome", "#ffd23f"]]}),
    ("Primeiro, a lista. Cria o arquivo usuarios ponto spec ponto js e escreve: const usuarios igual, abre colchetes.",
     edc("import { test, expect } from '@playwright/test';\n\nconst usuarios = [", "Uma lista: const usuarios = [", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=3, fonte=30)),
    ("Traduzindo: const, guarde com o nome usuarios. O igual, o que vem depois é o valor. E os colchetes abrem uma lista.",
     {"type": "traducao", "codigo": "const usuarios = [", "partes": [["const", "guarde"], ["usuarios", "com o nome usuarios"], ["=", "o valor é"], ["[", "uma lista"]], "passo": 1.8}),
    ("Pensa numa lista de compras: um item depois do outro. No código, cada nome vai entre aspas, e a vírgula separa um do outro. No fim, fecha os colchetes.",
     edc("\n".join(L31[:3]), "Itens entre aspas, separados por vírgula", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=3, vel=0.7, fonte=26)),
    ("Pronto: a lista usuarios guarda quatro nomes. Agora, a repetição: for, abre parênteses, const usuario of usuarios, fecha parênteses e abre chaves.",
     edc("\n".join(L31[:4] + [L31[L_FOR - 1], "}"]), "for (const usuario of usuarios)", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=L_FOR, fonte=26)),
    ("Traduzindo: for, para cada. usuario, um nome que a gente dá pra cada item. of usuarios, da lista usuarios. Então: para cada usuário da lista.",
     {"type": "traducao", "codigo": "for (const usuario of usuarios) {", "partes": [["for", "para cada"], ["const usuario", "item da vez: usuario"], ["of usuarios", "da lista usuarios"]], "passo": 2.0}),
    ("Voltando pra lista de compras: pra cada item da lista, você pega ele no mercado. O for faz igual: pra cada nome da lista, ele roda o que está dentro das chaves.",
     {"type": "cards", "titulo": "PARA CADA ITEM DA LISTA", "itens": [["🛒", "Lista de compras", "pega cada item"], ["↻", "for", "roda o que está nas chaves", "#ffd23f"]]}),
    ("Na primeira volta, usuario vale standard user. Na segunda, problem user. Na terceira, performance glitch user. E na quarta, visual user. Quatro nomes, quatro voltas.",
     {"type": "cards", "titulo": "O QUE ESTÁ DENTRO DO FOR RODA 4 VEZES", "itens": [["1", "standard_user", "1ª volta"], ["2", "problem_user", "2ª volta", "#69a7ff"], ["3", "performance_glitch_user", "3ª volta", "#ffd23f"], ["4", "visual_user", "4ª volta", "#c792ea"]]}),
    ("Agora, dentro das chaves do for, vai o teste de login que você já conhece. Por enquanto, com o nome fixo: login funciona.",
     edc(C31, "O teste dentro do for", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=L_TEST, fonte=24)),
    ("E onde antes tinha standard user, agora vai a palavra usuario: o nome da volta da vez.",
     edc(C31, "fill(usuario): o nome da volta da vez", arquivo="usuarios.spec.js", pastas=ARV_U, destaque=[L_FILL], destaque_em=0.6, fonte=24)),
    ("Repara: usuario está sem aspas. Com aspas, ele ia digitar a palavra usuario, letra por letra. Sem aspas, ele digita o valor guardado: o nome da volta.",
     {"type": "traducao", "titulo": "COM ASPAS × SEM ASPAS", "linhas": [["fill('usuario')", "digita a palavra usuario"], ["fill(usuario)", "digita o nome da volta"]]}),
    ("E o timeout de dez segundos na conferência final? O performance glitch demora uns cinco segundos pra entrar, e o expect espera cinco. Então, só nessa linha, a gente dá dez.",
     edc(C31, "O usuário lento: 10 segundos só aqui", arquivo="usuarios.spec.js", pastas=ARV_U, destaque=[L_TIME - 1, L_TIME], destaque_em=0.6, fonte=24)),
    ("Esse jeito tem nome: teste orientado a dados. Um teste, vários dados. Use sempre que o passo a passo é o mesmo e só muda o que você digita.",
     {"type": "traducao", "titulo": "QUANDO USAR", "linhas": [["mesmos passos, dados diferentes", "uma lista + for"], ["passos diferentes", "testes separados"]]}),
    ("E o melhor: quer testar um quinto usuário? É só um nome a mais na lista. Nenhuma linha de teste nova.",
     {"type": "cards", "itens": [["+", "Mais um usuário?", "um nome a mais na lista"], ["✓", "Linhas de teste novas", "nenhuma", "#3fd68a"]]}),
    ("Só que, se você rodar agora, vai dar um erro. Na próxima aula você entende por quê, e conserta.", proxima("nome dinâmico do teste")[0]),
    ("Te vejo lá!", proxima("nome dinâmico do teste")[1]),
]))

# ---------- Aula 32 ----------
REL32 = [[f"login funciona para {u}", f"usuarios.spec.js:{L_TEST}", "chromium", "ok", d] for u, d in (("standard_user", "0.9s"), ("problem_user", "1.0s"), ("performance_glitch_user", "5.7s"), ("visual_user", "1.1s"))]
AULAS.append(projeto(32, "MÓDULO 7 · AULA 32", "O nome do teste que muda sozinho", [
    ("Se você rodar agora, o Playwright nem começa. Ele reclama: duplicate test title, nome de teste repetido.",
     vs(C31, "Nome de teste repetido: ele não deixa", run(("Error: duplicate test title \"login funciona\",", VERM), ("first declared in usuarios.spec.js:6", VERM)), arquivo="usuarios.spec.js", pastas=ARV_U)),
    ("Por quê? O for criou quatro testes, e os quatro se chamam login funciona. Se um deles falhasse, como você ia saber qual?",
     {"type": "traducao", "titulo": "4 TESTES, O MESMO NOME", "linhas": [["standard_user", "login funciona"], ["problem_user", "login funciona"], ["performance_glitch_user", "login funciona"], ["visual_user", "login funciona"]]}),
    ("A solução é colocar o nome do usuário dentro do nome do teste.", bt(("O NOME DO USUÁRIO", "gold", 120), ("DENTRO DO NOME DO TESTE", "white", 100))),
    ("Até aqui, todo texto foi entre aspas. Com aspas, o texto é fixo: sai exatamente o que está escrito. Pra misturar texto com o valor de uma variável, existe a crase.",
     {"type": "compare", "title": "ASPAS × CRASE", "items": [["'ASPAS'", "TEXTO FIXO", "white"], ["`CRASE`", "TEXTO + VALOR", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),
    ("No teclado brasileiro, a crase fica na tecla do acento agudo, com shift. Aperta, e depois a barra de espaço, pra ela aparecer.",
     {"type": "cards", "titulo": "DIGITANDO A CRASE", "itens": [["⇧", "Shift", "segura"], ["´", "Tecla do acento", "aperta", "#69a7ff"], ["␣", "Espaço", "a crase aparece", "#ffd23f"]]}),
    ("Então, troca as aspas do nome do teste por crase, e escreve: login funciona para, cifrão, abre chaves, usuario, fecha chaves.",
     edc(C32, "Crase: texto + valor", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=L_TEST, digitar_ate=L_TEST, vel=0.7, fonte=24)),
    ("Traduzindo: a crase abre um texto que aceita valores. E cifrão chaves abre um espaço dentro dele: coloque aqui o valor de usuario.",
     {"type": "traducao", "codigo": "`login funciona para ${usuario}`", "partes": [["`", "texto que aceita valores"], ["${usuario}", "coloque aqui o valor de usuario"]], "passo": 2.4}),
    ("Em cada volta do for, o valor entra ali. Na primeira, login funciona para standard user. Na segunda, para problem user. E assim por diante.",
     {"type": "traducao", "titulo": "UM NOME DIFERENTE EM CADA VOLTA", "linhas": [["1ª volta", "login funciona para standard_user"], ["2ª volta", "login funciona para problem_user"],
                                                                              ["3ª volta", "login funciona para performance_glitch_user"], ["4ª volta", "login funciona para visual_user"]]}),
    ("Roda de novo: agora são quatro testes, cada um com o nome do seu usuário.", {"type": "pw_relatorio", "testes": REL32, "legenda": "Quatro testes, quatro nomes"}),
    ("E o nome não serve só pro Playwright deixar rodar. Se um teste falhar, o relatório diz na hora qual usuário quebrou.",
     bt(("QUAL USUÁRIO FALHOU?", "white", 110), ("ESTÁ NO NOME DO TESTE", "gold", 130))),
    ("E dá até pra rodar um só: traço g e um pedaço do nome, tipo performance. Só o teste daquele usuário roda.",
     vs(C32, "-g performance: só aquele usuário", run(("Running 1 test using 1 worker", "mut"), ("  1 passed (5.9s)", "ac"), cmd="npx playwright test -g performance --project=chromium"), arquivo="usuarios.spec.js", pastas=ARV_U)),
    ("A crase vai aparecer muito: numa mensagem com o nome da pessoa, num endereço com um número no meio, e no projeto final, montando um data-test.",
     {"type": "traducao", "titulo": "A CRASE NO DIA A DIA", "linhas": [["`Olá, ${nome}`", "mensagem com o nome"], ["`/produto/${id}`", "endereço com o número"], ["`add-to-cart-${produto}`", "data-test montado (aula 40)"]]}),
    ("Na próxima aula: três navegadores ao mesmo tempo.", proxima("3 navegadores e paralelo")[0]),
    ("Te vejo lá!", proxima("3 navegadores e paralelo")[1]),
]))

# ---------- Aula 33 ----------
PROJ = CONFIG[36:51]  # linhas 37 a 51: os três projects
assert "projects" in PROJ[0] and "webkit" in "".join(PROJ)
L_NOMES = [i + 1 for i, l in enumerate(PROJ) if "name:" in l]
PAR = CONFIG[16:24]   # linhas 17 a 24: fullyParallel ... workers
L_PAR = [i + 1 for i, l in enumerate(PAR) if "fullyParallel" in l or "workers" in l]
AULAS.append(projeto(33, "MÓDULO 7 · AULA 33", "3 navegadores e testes em paralelo", [
    ("Lembra que, com dois testes, apareciam seis execuções? Hoje você entende de onde vem.", titulo(33, "PARALELO")),
    ("Sem o traço traço project, o Playwright roda em três navegadores: Chromium, Firefox e WebKit, que é o motor usado pelo Safari.",
     {"type": "cards", "itens": [["C", "Chromium", "a base do Chrome"], ["F", "Firefox", "", "#ff8c42"], ["W", "WebKit", "o motor usado pelo Safari", "#69a7ff"]]}),
    ("Dois testes, vezes três navegadores: seis execuções. Cada teste roda uma vez em cada navegador.",
     {"type": "traducao", "titulo": "2 TESTES × 3 NAVEGADORES = 6", "linhas": [["entra com usuário e senha", "chromium · firefox · webkit"], ["mostra erro para bloqueado", "chromium · firefox · webkit"]]}),
    ("Eles estão no config, nos projects.", edc("\n".join(PROJ), "projects: os três navegadores", arquivo="playwright.config.js", linha0=37, destaque=L_NOMES, destaque_em=0.6, fonte=22)),
    ("Por que três? Porque um site pode funcionar no Chrome e quebrar no Safari. Cada navegador desenha a página do seu jeito, e bug de um navegador só acontece bastante.", {"type": "cards", "itens": [["✓", "Chromium", "funcionou", "#3fd68a"], ["✓", "Firefox", "funcionou", "#3fd68a"], ["✗", "WebKit (Safari)", "o botão sumiu", "#ff6b6b"]], "titulo": "O MESMO SITE"}),  # pra que / quando
    ("Roda tudo: dezoito testes, que são os seis do projeto vezes três navegadores. E repara na linha workers. Aqui na minha máquina apareceram quatro; na sua pode aparecer outro número. Worker é um trabalhador: um processo que ajuda a rodar testes ao mesmo tempo.",
     vs(C32, "workers = trabalhadores", run(("Running 18 tests using 4 workers", "mut"), ("  18 passed (14.2s)", "ac"), cmd="npx playwright test"), arquivo="usuarios.spec.js", pastas=ARV_U)),
    ("Paralelo quer dizer vários testes ao mesmo tempo, em vez de um por vez. Por isso cada teste precisa ser independente: nenhum pode depender de outro.",
     {"type": "compare", "items": [["UM POR VEZ", "MAIS DEVAGAR", "white"], ["AO MESMO TEMPO", "CADA TESTE INDEPENDENTE", "gold"]], "size": 90, "stagger": 1.2, "vs": True}),
    ("Um exemplo: se um teste esvazia o carrinho enquanto outro está conferindo o carrinho, rodando ao mesmo tempo, um atrapalha o outro. Por isso, cada teste prepara sozinho tudo o que precisa.",
     {"type": "cards", "titulo": "TESTES QUE DEPENDEM UM DO OUTRO", "itens": [["A", "Teste A", "esvazia o carrinho"], ["B", "Teste B", "confere o carrinho", "#69a7ff"], ["✗", "Ao mesmo tempo", "um atrapalha o outro", VERM]]}),
    ("E por que paralelo? Velocidade. Duzentos testes de cinco segundos, um de cada vez, levam mais de quinze minutos. Com quatro workers, uns quatro minutos.", {"type": "compare", "title": "200 TESTES DE 5 SEGUNDOS", "items": [["UM POR VEZ", "MAIS DE 15 MINUTOS", "white"], ["4 WORKERS", "UNS 4 MINUTOS", "gold"]], "size": 90, "stagger": 1.8, "vs": False}),  # pra que / quando
    ("No config, o fully parallel true liga isso. E no GitHub ele usa um worker só: a máquina de lá é pequena, e um de cada vez fica mais estável.",
     edc("\n".join(PAR), "fullyParallel e workers", arquivo="playwright.config.js", linha0=17, destaque=L_PAR, destaque_em=0.6, fonte=26)),
    ("No dia a dia, enquanto escreve, roda só no Chromium com traço traço project igual chromium, que é mais rápido. Os três navegadores ficam pro GitHub, que roda tudo a cada mudança.", {"type": "traducao", "titulo": "NO DIA A DIA", "linhas": [["escrevendo o teste", "--project=chromium"], ["no GitHub, a cada mudança", "os 3 navegadores"]]}),  # pra que / quando
    ("Na próxima aula: testando com tela de celular.", proxima("celular")[0]),
    ("Te vejo lá!", proxima("celular")[1]),
]))

# ---------- Aula 34 ----------
CEL = ["", "    {", "      name: 'celular',", "      use: { ...devices['Pixel 7'] },", "    },"]
PROJ34 = PROJ + CEL
L_CEL = len(PROJ) + 2
AULAS.append(projeto(34, "MÓDULO 7 · AULA 34", "Celular - emulando dispositivos", [
    ("Muita gente acessa os sites pelo celular. O Playwright consegue imitar aparelhos conhecidos.", titulo(34, "CELULAR")),
    ("Ele tem uma lista de aparelhos prontos, com tamanho de tela, toque e outras características. Isso ajuda muito, mas não substitui todos os testes num aparelho de verdade.",
     {"type": "cards", "itens": [["📱", "Pixel 7", "tela, toque, navegador"], ["📱", "iPhone 13", "", "#69a7ff"], ["⚠", "Não substitui tudo", "teste também no aparelho real", "#ff8c42"]]}),
    ("No config, cria um project novo chamado celular, usando o Pixel 7.",
     edc("\n".join(PROJ34), "project celular: Pixel 7", arquivo="playwright.config.js", linha0=37, digitar=True, digitar_de=L_CEL, digitar_ate=L_CEL + 2, fonte=24, rolar=True, rolar_de=0.8, rolar_dur=1.0)),
    ("Traduzindo: devices, a lista de aparelhos. Pixel 7, o nome do aparelho. E os três pontinhos: pegue todas as configurações dele, o tamanho da tela, o toque e o resto.",
     {"type": "traducao", "codigo": "use: { ...devices['Pixel 7'] }", "partes": [["...", "tudo dele"], ["devices", "aparelhos"], ["['Pixel 7']", "o Pixel 7"]], "passo": 2.2}),
    ("Quer outro aparelho? É só trocar o nome: iPhone 13, iPad Mini, e dezenas de outros.",
     {"type": "traducao", "titulo": "TROCA O NOME, TROCA O APARELHO", "linhas": [["devices['Pixel 7']", "Android"], ["devices['iPhone 13']", "iPhone"], ["devices['iPad Mini']", "tablet"]]}),
    ("Roda com project igual celular e com o navegador aparecendo: olha, o site abre no tamanho de celular.",
     edc("\n".join(codigo(24).replace("aula 24: ", "").split("\n")[:10]), "Tamanho de celular", pastas=ARV_U,
         terminal=[{"cmd": "npx playwright test login.spec.js --project=celular --headed", "em": 0.03}, {"out": "Running 2 tests using 2 workers", "cor": "mut", "em": 0.08}, {"out": "  2 passed (3.1s)", "cor": "ac", "em": 0.86}],
         navegador={"media": "rec_celular", "url": SAUCE, "gravar": True, "dispositivo": "Pixel 7", "acoes": LOGIN, "espera_inicio": 900, "espera_fim": 1500, "delay_letra": 70, "titulo": "Pixel 7", "em": 0.1, "ate": 0.84})),
    ("E o mesmo teste funciona, sem mudar nada no código.", vs(codigo(24).replace("aula 24: ", ""), "O mesmo código", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (3.1s)", "ac"), cmd="npx playwright test login.spec.js --project=celular"), pastas=ARV_U)),
    ("E o que ele pega? Coisas que só acontecem em tela pequena: o menu que vira três risquinhos, um botão que fica fora da tela, um texto por cima do outro.", {"type": "cards", "itens": [["☰", "Menu", "vira três risquinhos"], ["⬚", "Botão", "fora da tela", "#ff6b6b"], ["▤", "Texto", "por cima do outro", "#ffd23f"]], "titulo": "SÓ EM TELA PEQUENA"}),  # pra que / quando
    ("Vale ligar quando muita gente usa o site pelo celular, uma loja por exemplo. E antes de um lançamento importante, confere também num aparelho de verdade.", {"type": "traducao", "titulo": "QUANDO USAR", "linhas": [["muita gente acessa pelo celular", "project celular"], ["antes de um lançamento", "+ um aparelho de verdade"]]}),  # pra que / quando
    ("Fechamos os testes reais. Agora: o projeto final!", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "O projeto final"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 8 · PROJETO FINAL"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 7 (gerado do roteiro_playwright_m7.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo7.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

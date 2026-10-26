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
AULAS.append(projeto(31, "MÓDULO 7 · AULA 31", "Uma lista de usuários e um teste que se repete", [
    ("O saucedemo tem vários usuários que entram normalmente: standard, problem, performance glitch e visual. Copiar o mesmo teste quatro vezes? Não.",
     {"type": "tela", "media": "site_sauce_users", "url": SAUCE, "titulo": "saucedemo.com", "legenda": "Vários usuários", "alvo_css": "[data-test=\"login-credentials\"]", "zoom_em": 1.4, "caixa_em": 2.0}),
    ("Primeiro, uma ideia nova: uma lista. Cria o arquivo usuarios ponto spec ponto js e escreve: const usuarios igual, abre colchetes.",
     edc("import { test, expect } from '@playwright/test';\n\nconst usuarios = [", "Uma lista: const usuarios = [", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=3, fonte=30)),
    ("Traduzindo: const, guarde com o nome usuarios. O igual, o que vem depois é o valor. E os colchetes abrem uma lista.",
     {"type": "traducao", "codigo": "const usuarios = [", "partes": [["const", "guarde"], ["usuarios", "com o nome usuarios"], ["=", "o valor é"], ["[", "uma lista"]], "passo": 1.8}),
    ("Dentro da lista, os nomes entre aspas, separados por vírgula. A vírgula separa um item do outro.",
     edc("\n".join(L31[:3]), "Itens entre aspas, separados por vírgula", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=3, fonte=26)),
    ("Agora a repetição: for, abre parênteses, const usuario of usuarios.",
     edc("\n".join(L31[:4] + [L31[L_FOR - 1], "}"]), "for (const usuario of usuarios)", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=L_FOR, fonte=26)),
    ("Traduzindo: for, para cada. usuario, um nome que a gente dá pra cada item. of usuarios, da lista usuarios. Então: para cada usuário da lista.",
     {"type": "traducao", "codigo": "for (const usuario of usuarios) {", "partes": [["for", "para cada"], ["const usuario", "item da vez: usuario"], ["of usuarios", "da lista usuarios"]], "passo": 2.0}),
    ("E o que estiver dentro das chaves do for se repete uma vez pra cada item. Quatro nomes, quatro vezes.",
     {"type": "cards", "titulo": "O QUE ESTÁ DENTRO DO FOR RODA 4 VEZES", "itens": [["1", "standard_user", "1ª volta"], ["2", "problem_user", "2ª volta", "#69a7ff"], ["3", "performance_glitch_user", "3ª volta", "#ffd23f"], ["4", "visual_user", "4ª volta", "#c792ea"]]}),
    ("Por enquanto, o nome do teste é fixo: login funciona. Na próxima aula, a gente faz o nome mudar com o usuário.",
     edc(C31, "O teste dentro do for", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=L_TEST, fonte=24)),
    ("Dentro do teste, onde antes tinha standard user, agora vai a palavra usuario: o item da vez.",
     edc(C31, "fill(usuario): o item da vez", arquivo="usuarios.spec.js", pastas=ARV_U, destaque=[L_FILL], destaque_em=0.6, fonte=24)),
    ("Repara no timeout de dez segundos na conferência final. É uma exceção, por causa do performance glitch, que você conheceu na aula 21.",
     edc(C31, "Exceção: o usuário lento", arquivo="usuarios.spec.js", pastas=ARV_U, destaque=[L_TIME], destaque_em=0.6, fonte=24)),
    ("Na próxima aula: um nome de teste que muda sozinho.", proxima("nome dinâmico do teste")[0]),
    ("Te vejo lá!", proxima("nome dinâmico do teste")[1]),
]))

# ---------- Aula 32 ----------
REL32 = [[f"login funciona para {u}", f"usuarios.spec.js:{L_TEST}", "chromium", "ok", d] for u, d in (("standard_user", "0.9s"), ("problem_user", "1.0s"), ("performance_glitch_user", "5.7s"), ("visual_user", "1.1s"))]
AULAS.append(projeto(32, "MÓDULO 7 · AULA 32", "O nome do teste que muda sozinho", [
    ("Se você rodar agora, o Playwright nem começa. Ele reclama: duplicate test title, nome de teste repetido. Os quatro testes teriam o mesmo nome, e ele não deixa.",
     vs(C31, "Nome de teste repetido: ele não deixa", run(("Error: duplicate test title \"login funciona\",", VERM), ("first declared in usuarios.spec.js:6", VERM)), arquivo="usuarios.spec.js", pastas=ARV_U)),
    ("A solução é colocar o nome do usuário dentro do nome do teste.", bt(("O NOME DO USUÁRIO", "gold", 120), ("DENTRO DO NOME DO TESTE", "white", 100))),
    ("Pra isso, troca as aspas por crase. Com crase, dá pra misturar texto com o valor de uma variável.",
     edc(C32, "Crase: texto + valor", arquivo="usuarios.spec.js", pastas=ARV_U, digitar=True, digitar_de=L_TEST, digitar_ate=L_TEST, fonte=24)),
    ("E o valor entra assim: cifrão, abre chaves, usuario, fecha chaves.",
     {"type": "traducao", "codigo": "`login funciona para ${usuario}`", "partes": [["`", "crase"], ["${usuario}", "o valor de usuario"]], "passo": 1.8}),
    ("Traduzindo: cifrão chaves quer dizer: coloque aqui o valor de usuario.",
     {"type": "traducao", "titulo": "COLOQUE AQUI O VALOR DE USUARIO", "linhas": [["standard_user", "login funciona para standard_user"], ["problem_user", "login funciona para problem_user"],
                                                                              ["performance_glitch_user", "login funciona para performance_glitch_user"], ["visual_user", "login funciona para visual_user"]]}),
    ("Roda: quatro testes, cada um com o nome do seu usuário.", {"type": "pw_relatorio", "testes": REL32, "legenda": "Quatro testes, quatro nomes"}),
    ("Quer testar mais um usuário? Só coloca o nome na lista.", {"type": "cards", "itens": [["+", "Mais um usuário?", "só coloca o nome na lista"]]}),
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
    ("Lembra das seis execuções com dois testes? Hoje você entende de onde vem.", titulo(33, "PARALELO")),
    ("Sem o traço traço project, o Playwright roda em três navegadores: Chromium, Firefox e WebKit, que é o motor usado pelo Safari.",
     {"type": "cards", "itens": [["C", "Chromium", "a base do Chrome"], ["F", "Firefox", "", "#ff8c42"], ["W", "WebKit", "o motor usado pelo Safari", "#69a7ff"]]}),
    ("Eles estão no config, nos projects.", edc("\n".join(PROJ), "projects: os três navegadores", arquivo="playwright.config.js", linha0=37, destaque=L_NOMES, destaque_em=0.6, fonte=22)),
    ("Roda tudo e repara na linha workers. Aqui na minha máquina apareceram quatro; na sua pode aparecer outro número. Worker é um trabalhador: um processo que ajuda a rodar testes ao mesmo tempo.",
     vs(C32, "workers = trabalhadores", run(("Running 18 tests using 4 workers", "mut"), ("  18 passed (14.2s)", "ac"), cmd="npx playwright test"), arquivo="usuarios.spec.js", pastas=ARV_U)),
    ("Paralelo quer dizer vários testes ao mesmo tempo, em vez de um por vez. Por isso cada teste precisa ser independente: nenhum pode depender de outro.",
     {"type": "compare", "items": [["UM POR VEZ", "MAIS DEVAGAR", "white"], ["AO MESMO TEMPO", "CADA TESTE INDEPENDENTE", "gold"]], "size": 90, "stagger": 1.2, "vs": True}),
    ("No config, o fully parallel true liga isso. E no GitHub ele usa um worker só, pra execução ficar mais estável e previsível.",
     edc("\n".join(PAR), "fullyParallel e workers", arquivo="playwright.config.js", linha0=17, destaque=L_PAR, destaque_em=0.6, fonte=26)),
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
    ("Roda com project igual celular e com o navegador aparecendo: olha, o site abre no tamanho de celular.",
     edc("\n".join(codigo(24).replace("aula 24: ", "").split("\n")[:10]), "Tamanho de celular", pastas=ARV_U,
         terminal=[{"cmd": "npx playwright test login.spec.js --project=celular --headed", "em": 0.03}, {"out": "Running 2 tests using 2 workers", "cor": "mut", "em": 0.08}, {"out": "  2 passed (3.1s)", "cor": "ac", "em": 0.86}],
         navegador={"media": "rec_celular", "url": SAUCE, "gravar": True, "dispositivo": "Pixel 7", "acoes": LOGIN, "espera_inicio": 900, "espera_fim": 1500, "delay_letra": 70, "titulo": "Pixel 7", "em": 0.1, "ate": 0.84})),
    ("E o mesmo teste funciona, sem mudar nada no código.", vs(codigo(24).replace("aula 24: ", ""), "O mesmo código", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (3.1s)", "ac"), cmd="npx playwright test login.spec.js --project=celular"), pastas=ARV_U)),
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

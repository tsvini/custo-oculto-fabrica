"""Gera projetos/curso-playwright-26..30 (módulo 6: debug). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Os textos de erro são a saída real das demos (curso-playwright/projeto/demos/aula26_*.demo.spec.js) rodadas no Actions.
Ajuste técnico combinado: a aula 26 quebra o toContainText ('Backpack' → 'Mochila'), porque o erro de toBeVisible não mostra "Received"."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, proxima, projeto, RAIZ
from roteiro_playwright_m3 import codigo, ARV, SAUCE, LOGIN
from roteiro_playwright_m4 import edc, CMD, cg
from roteiro_playwright_m5 import vs, CONFIG, ARV_EX

C24 = codigo(24).replace("aula 24: ", "")
C26 = C24.replace("toContainText('Backpack')", "toContainText('Mochila')")
assert C26 != C24
L_MOCHILA = [i + 1 for i, l in enumerate(C26.split("\n")) if "Mochila" in l][0]  # linha 14


def run(*saida, cmd=CMD):
    L = [{"cmd": cmd, "em": 0.05}]
    for i, (txt, cor) in enumerate(saida):
        L.append({"out": txt, "cor": cor, "em": [0.3, 0.5, 0.6, 0.68][min(i, 3)]})
    return L


def term(linhas, legenda, destaque=(), em=1.0):
    return {"type": "terminal", "titulo": "Terminal — VS Code", "pasta": "C:\\Users\\voce\\Documents\\meu-primeiro-playwright",
            "linhas": [dict(l, ja=True) for l in linhas], "legenda": legenda, "destaque": list(destaque), "destaque_em": em, "fonte": 32, "fonte_min": 26}


VERM = "#ff6b6b"
# saída real (demos/aula26_erro.demo.spec.js), com o caminho do arquivo do aluno
E1 = [{"out": "1) [chromium] › tests/login.spec.js:8:7 › Login › entra com usuário e senha", "cor": "txt"},
      {"out": "  Error: expect(locator).toContainText(expected) failed", "cor": VERM},
      {"out": "  Locator: getByText('Sauce Labs Backpack')", "cor": "txt"},
      {"out": "  Expected substring: \"Mochila\"", "cor": "ac"},
      {"out": "  Received string:    \"Sauce Labs Backpack\"", "cor": VERM},
      {"out": "  Timeout: 5000ms", "cor": "mut"}]
E2 = [{"out": "  13 |   await expect(page.getByText('Products')).toBeVisible();", "cor": "mut"},
      {"out": "> 14 |   await expect(page.getByText('Sauce Labs Backpack')).toContainText('Mochila');", "cor": "txt"},
      {"out": "     |                                                       ^", "cor": VERM},
      {"out": "  at tests/login.spec.js:14:57", "cor": "mut"}]
E3 = [{"out": "Call log:", "cor": "txt"},
      {"out": "  - Expect \"toContainText\" getByText('Sauce Labs Backpack') with timeout 5000ms", "cor": "mut"},
      {"out": "  - waiting for getByText('Sauce Labs Backpack')", "cor": "mut"},
      {"out": "    14 × locator resolved to <div …>Sauce Labs Backpack</div>", "cor": "mut"},
      {"out": "       - unexpected value \"Sauce Labs Backpack\"", "cor": VERM}]
assert max(len(l["out"]) for l in E1 + E2 + E3) <= 92

TESTES = [["login.spec.js", ["entra com usuário e senha", "mostra erro para usuário bloqueado"]]]
A_LOGIN = [["Before Hooks", "", "520ms"], ["Navigate to", "\"/\"", "410ms"], ["Fill", "getByTestId('username')", "38ms"], ["Fill", "getByTestId('password')", "21ms"],
           ["Click", "getByTestId('login-button')", "96ms"], ["Expect", "toHaveURL", "12ms"], ["Expect", "toBeVisible", "9ms"], ["Expect", "toContainText", "8ms"], ["Expect", "toHaveCount", "7ms"]]
UI = {"type": "pw_ui", "media": "site_sauce_ui_logado", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "arquivos": TESTES, "passos_pw": A_LOGIN}
FALHA = [["entra com usuário e senha", "login.spec.js:8", "chromium", "falhou", "6.1s"], ["mostra erro para usuário bloqueado", "login.spec.js:18", "chromium", "ok", "0.6s"]]
P_REL = [["Before Hooks", "0.5s"], ["Navigate to \"/\"", "0.4s"], ["Fill getByTestId('username')", "38ms"], ["Fill getByTestId('password')", "21ms"], ["Click getByTestId('login-button')", "96ms"]]

AULAS = []

# ---------- Aula 26 ----------
AULAS.append(projeto(26, "MÓDULO 6 · AULA 26", "Lendo o erro", [
    ("O teste falhou. Calma: ler o erro fica muito mais fácil quando você sabe onde olhar.", titulo(26, "LENDO O ERRO")),
    ("Vamos quebrar de propósito: na conferência da mochila, troca Backpack por Mochila.",
     edc(C26, "Backpack → Mochila (de propósito)", pastas=ARV_EX, digitar=True, digitar_de=L_MOCHILA, digitar_ate=L_MOCHILA, fonte=22, rolar_depois=True)),
    ("Roda. Falhou.", vs(C26, "Falhou", run(("Running 2 tests using 2 workers", "mut"), ("  1 failed", VERM), ("  1 passed (6.2s)", "ac")), pastas=ARV_EX)),
    ("Vamos ler de cima pra baixo. Primeiro: qual teste falhou, e em qual arquivo e linha.", term(E1, "Qual teste, qual arquivo, qual linha", destaque=[0])),
    ("Depois: Expected, o que você esperava, e Received, o que ele encontrou.", term(E1, "Expected = esperado · Received = encontrado", destaque=[3, 4])),
    ("Depois, o pedaço do seu código, com uma setinha apontando a linha exata.", term(E2, "A setinha aponta a linha", destaque=[1, 2])),
    ("E o call log, que mostra tudo o que ele tentou. Repara: ele ficou tentando por cinco segundos antes de desistir.", term(E3, "Call log: tudo o que ele tentou", destaque=[1, 4], em=1.4)),
    ("Três coisas que você vai ver bastante: timeout, alguma coisa que o teste esperava não aconteceu dentro do tempo. Strict mode violation, o seletor achou mais de um elemento quando precisava de um só. E Expected e Received, o teste esperava um valor e encontrou outro.",
     {"type": "cards", "itens": [["⏱", "Timeout", "o esperado não aconteceu a tempo"], ["⚠", "Strict mode", "achou mais de um", "#ffd23f"], ["≠", "Expected × Received", "esperava um, encontrou outro", "#ff6b6b"]]}),
    ("Volta pra Backpack e roda: passou.", vs(C24, "Passou", run(("Running 2 tests using 2 workers", "mut"), ("  2 passed (2.1s)", "ac")), pastas=ARV_EX)),
    ("Na próxima aula: um jeito muito mais visual de rodar os testes.", proxima("UI Mode")[0]),
    ("Te vejo lá!", proxima("UI Mode")[1]),
]))

# ---------- Aula 27 ----------
AULAS.append(projeto(27, "MÓDULO 6 · AULA 27", "UI Mode", [
    ("Existe um jeito bem mais visual de rodar testes: o UI Mode.", titulo(27, "UI MODE")),
    ("No terminal: npx playwright test traço traço ui.", vs(C24, "--ui", run(cmd="npx playwright test --ui"), pastas=ARV_EX, colinha=True, colinha_em=1.2)),
    ("Abre uma janela com todos os seus testes do lado esquerdo. Clica no play.", dict(UI, legenda="Clica no play")),
    ("Ele roda e mostra cada passo. Clica num passo, e a tela mostra como a página estava naquele momento.", dict(UI, pronto=True, legenda="Cada passo, com a página daquele momento")),
    ("Dá pra voltar no tempo: ver a página antes e depois de cada clique.",
     dict(UI, pronto=True, media="site_sauce_ui_preenchido", acoes=LOGIN[:2], inspecionar="#login-button", aba_snapshot=1, depois={"em": 3.2, "media": "site_sauce_ui_logado"},
          legenda="Before e After: antes e depois do clique")),
    ("E tem o watch, que quer dizer vigiar, aquele ícone de olho: você salva o arquivo e o teste roda de novo sozinho.", dict(UI, watch=True, watch_em=1.2, roda_em=2.6, legenda="watch = vigiar: salvou, rodou de novo")),
    ("É um dos jeitos mais confortáveis de escrever um teste novo: escreve, salva, e vê na hora.", bt(("ESCREVE, SALVA", "white", 120), ("E VÊ NA HORA", "gold", 150), entre=1.35)),
    ("Na próxima aula: o rastro completo de um teste.", proxima("Trace Viewer")[0]),
    ("Te vejo lá!", proxima("Trace Viewer")[1]),
]))

# ---------- Aula 28 ----------
CFG_RETRY = CONFIG[20:34]  # linhas 21 a 34: retries ... trace
assert "retries" in CFG_RETRY[1] and "trace" in CFG_RETRY[12]
AULAS.append(projeto(28, "MÓDULO 6 · AULA 28", "Trace Viewer", [
    ("E quando o teste falha no GitHub, onde você não estava olhando? Pra isso existe o trace.", titulo(28, "TRACE VIEWER")),
    ("Trace quer dizer rastro: é um arquivo com tudo o que aconteceu no teste.", {"type": "traducao", "codigo": "trace", "texto_puro": True, "partes": [["trace", "rastro: tudo o que aconteceu"]], "passo": 1.2}),
    ("Roda com traço traço trace on.", vs(C24, "--trace on", run(("Running 6 tests using 4 workers", "mut"), ("  6 passed (5.1s)", "ac"), cmd="npx playwright test --trace on"), pastas=ARV_EX)),
    ("Abre o relatório e clica no trace do teste.",
     {"type": "pw_relatorio", "url": SAUCE, "media": "site_sauce_trace", "acoes": LOGIN, "testes": FALHA,
      "abrir": {"titulo": "entra com usuário e senha", "arquivo": "login.spec.js:8", "projeto": "chromium", "passos": P_REL[:3], "anexos": [["Traces", "site_sauce_trace", False]], "anexos_em": 1.4},
      "legenda": "Traces: clica no trace"}),
    ("Em cima, a linha do tempo. Na esquerda, os passos. No meio, a página. E embaixo, o console e a rede.",
     {"type": "pw_trace", "media": "site_sauce_trace", "url": SAUCE, "acoes": LOGIN, "inspecionar": "[data-test=\"title\"]", "passos_pw": A_LOGIN, "sel": 6, "legenda": "Passos, página, console e rede"}),
    ("No config já vem trace on first retry: quando um teste falha e roda de novo, o trace dessa segunda tentativa é gravado. No GitHub o config já tenta de novo, então lá isso acontece sozinho. Na sua máquina, sem nova tentativa, use o traço traço trace on.",
     edc("\n".join(CFG_RETRY), "trace: 'on-first-retry'", arquivo="playwright.config.js", linha0=21, destaque=[2, 13], destaque_em=1.0, fonte=24)),
    ("Na próxima aula: pausando o teste no meio.", proxima("debug e page.pause")[0]),
    ("Te vejo lá!", proxima("debug e page.pause")[1]),
]))

# ---------- Aula 29 ----------
L24 = C24.split("\n")
L_CLICK = [i + 1 for i, l in enumerate(L24) if "login-button" in l][0]  # linha 11
C29 = "\n".join(L24[:L_CLICK] + ["    await page.pause();"] + L24[L_CLICK:])
TOPO29 = "\n".join(C29.split("\n")[:17])
AULAS.append(projeto(29, "MÓDULO 6 · AULA 29", "Modo debug e page.pause", [
    ("Às vezes você quer ver o teste devagar, um passo de cada vez.", titulo(29, "DEBUG")),
    ("No terminal: npx playwright test traço traço debug.", vs(C24, "--debug", run(cmd="npx playwright test --debug"), pastas=ARV_EX, colinha=True, colinha_em=1.2)),
    ("Ele abre o navegador e para antes do primeiro passo.", cg("Parado antes do primeiro passo", modo="debug", codigo="\n".join(L24[:16]), linhas_passo=[5])),
    ("No Inspector, o botão step over executa um passo por vez. Olha: preenche, para. Preenche, para. Clica, para.",
     cg("Step over: um passo de cada vez", modo="debug", codigo="\n".join(L24[:16]), linhas_passo=[9, 10, 11])),
    ("Outra forma, pra usar na sua máquina enquanto escreve o teste: page ponto pause no meio do código.",
     edc(C29, "page.pause()", pastas=ARV_EX, digitar=True, digitar_de=L_CLICK + 1, digitar_ate=L_CLICK + 1, fonte=22, rolar_depois=True)),
    ("Pause é pausar: rodando com o navegador aparecendo, o teste para exatamente ali e abre o Inspector.",
     cg("Parou no page.pause()", modo="debug", codigo=TOPO29, linhas_passo=[L_CLICK + 1], media="site_sauce_pause", acoes=LOGIN, inspecionar_varios=[])),
    ("É uma ferramenta de desenvolvimento: lembra de tirar o pause depois, senão o teste fica parado esperando você.",
     {"type": "cards", "itens": [["⏸", "page.pause()", "só enquanto você investiga"], ["✗", "Tira depois", "senão o teste fica parado", "#ff6b6b"]]}),
    ("Na próxima aula: print e vídeo automático quando o teste falha.", proxima("print e vídeo")[0]),
    ("Te vejo lá!", proxima("print e vídeo")[1]),
]))

# ---------- Aula 30 ----------
CFG30 = CONFIG[25:34]  # linhas 26 a 34, já com baseURL e testIdAttribute (aula 23)
CFG30 = [l if "// baseURL" not in l else "    baseURL: 'https://www.saucedemo.com',\n    testIdAttribute: 'data-test'," for l in CFG30]
CFG30 = "\n".join(CFG30).split("\n")
i_trace = [i for i, l in enumerate(CFG30) if "trace:" in l][0]
CFG30 = CFG30[:i_trace + 1] + ["    screenshot: 'only-on-failure',", "    video: 'retain-on-failure',"] + CFG30[i_trace + 1:]
AULAS.append(projeto(30, "MÓDULO 6 · AULA 30", "Print e vídeo quando o teste falha", [
    ("E se o próprio teste tirasse um print e gravasse um vídeo quando falha? Ele faz isso.", titulo(30, "PRINT E VÍDEO")),
    ("No config, dentro do use, adiciona duas linhas: screenshot only on failure, e video retain on failure.",
     edc("\n".join(CFG30), "screenshot e video", arquivo="playwright.config.js", linha0=26, digitar=True, digitar_de=i_trace + 2, digitar_ate=i_trace + 3, fonte=26)),
    ("Traduzindo: screenshot, print, só quando falhar. Video retain on failure: o vídeo é gravado durante o teste, e guardado só se ele falhar.",
     {"type": "traducao", "titulo": "SÓ QUANDO FALHA", "linhas": [["screenshot: 'only-on-failure'", "print, só quando falhar"], ["video: 'retain-on-failure'", "grava, e guarda só se falhar"]]}),
    ("Quebra o teste de novo e roda.", vs(C26, "Falhou de novo (de propósito)", run(("Running 2 tests using 2 workers", "mut"), ("  1 failed", VERM), ("  1 passed (6.4s)", "ac")), pastas=ARV_EX)),
    ("Abre o relatório: lá está o print do momento do erro e o vídeo do teste inteiro.",
     {"type": "pw_relatorio", "url": SAUCE, "media": "site_sauce_falha", "acoes": LOGIN, "testes": FALHA,
      "abrir": {"titulo": "entra com usuário e senha", "status": "falhou", "arquivo": "login.spec.js:8", "projeto": "chromium", "passos": [],
                "erro": "Error: expect(locator).toContainText(expected) failed\nExpected substring: \"Mochila\"\nReceived string:    \"Sauce Labs Backpack\"", "anexos": True, "anexo_img": "site_sauce_falha", "anexos_em": 1.2},
      "navegador": {"media": "rec_falha", "url": SAUCE, "gravar": True, "acoes": LOGIN, "espera_inicio": 800, "espera_fim": 1500, "titulo": "video.webm", "em": 0.45, "ate": 0.95},
      "legenda": "O print e o vídeo do teste"}),
    ("E por que só quando falha? Porque gravar sempre deixa tudo mais lento e enche o computador de arquivo.",
     {"type": "cards", "itens": [["🐢", "Gravar sempre", "mais lento, muito arquivo", "#ff8c42"], ["✓", "Só quando falha", "o que você precisa pra investigar"]]}),
    ("Desfaz o erro e fechamos o módulo de debug.", {"type": "passo", "icone": "▶", "titulo": "Próximo módulo", "sub": "Testes reais"}),
    ("Te vejo lá!", {"type": "endcard", "sub": "PRÓXIMA: MÓDULO 7 · TESTES REAIS"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 6 (gerado do roteiro_playwright_m6.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo6.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

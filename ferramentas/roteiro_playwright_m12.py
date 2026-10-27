"""Gera projetos/curso-playwright-81..83 (módulo 15: carreira; eram as aulas 55 a 57). Roteiro aprovado em curso-playwright/roteiros/modulo4-ao-fim.md.
Frases com duas ideias (ex.: a tabela e o aviso) viraram duas cenas com o mesmo texto dividido; a narração é a do roteiro aprovado."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro_playwright_m1 import bt, titulo, projeto, RAIZ
from roteiro_playwright_m4 import edc
from roteiro_playwright_m8 import ARV_AUTH

COLINHA = "repo:curso-playwright/material/colinha/colinha.html"
AMARELO, AZUL, VERM = "#ffd23f", "#69a7ff", "#ff6b6b"
ARV_R = ["meu-primeiro-playwright", "  .github/", "  node_modules/", "  pages/", "  tests/", "  .env", "  .gitignore", "  package.json", "  playwright.config.js", "  README.md"]

README = """# Meu primeiro projeto Playwright

![Playwright Tests](https://github.com/voce/meu-primeiro-playwright/actions/workflows/playwright.yml/badge.svg)

Testes de ponta a ponta da loja de treino saucedemo.com.

## Tecnologias
Playwright, JavaScript, Page Object, GitHub Actions

## Instalação
npm install
npx playwright install

## Rodando os testes
npx playwright test"""

AULAS = []

# ---------- Aula 55 ----------
AULAS.append(projeto(81, "MÓDULO 15 · AULA 81", "Veio do Cypress? Um mapa das ideias", [
    ("Se você já usou Cypress, várias ideias vão parecer familiares. Mas não pense no Playwright como uma simples troca de comandos.", titulo(81, "VEIO DO CYPRESS?")),
    ("Algumas aproximações ajudam: cy ponto visit lembra page ponto goto. cy ponto contains lembra get by text. should lembra expect.",
     {"type": "traducao", "titulo": "APROXIMAÇÕES (NÃO É TROCA 1 POR 1)", "linhas": [["cy.visit('/')", "page.goto('/')"], ["cy.contains('Products')", "page.getByText('Products')"], [".should('be.visible')", "expect(...).toBeVisible()"]]}),
    ("Mas o modelo muda. No Playwright você escreve await em cada passo, e os seletores são objetos que você guarda e reaproveita.",
     {"type": "bloco_vs", "vs_em": 2.4,
      "codigo_esq": "cy.visit('/');\ncy.get('[data-test=username]')\n  .type('standard_user');\ncy.get('[data-test=login-button]')\n  .click();",
      "janela_esq": "login.cy.js", "titulo_esq": "CYPRESS", "sub_esq": "comandos numa fila",
      "codigo": "const usuario = page.getByTestId('username');\nconst botao = page.getByTestId('login-button');\n\nawait page.goto('/');\nawait usuario.fill('standard_user');\nawait botao.click();",
      "janela_dir": "login.spec.js", "titulo_dir": "PLAYWRIGHT", "sub_dir": "await em cada passo · seletor guardado"}),
    ("As duas ferramentas resolvem problemas parecidos, com abordagens diferentes. Saber as duas te deixa mais forte no mercado.",
     bt(("CYPRESS", "white", 120), ("+ PLAYWRIGHT", "gold", 150), ("MAIS FORTE NO MERCADO", "muted", 70))),
    ("Te vejo na próxima!", {"type": "endcard", "sub": "PRÓXIMA: CURRÍCULO E ENTREVISTA"}),
]))

# ---------- Aula 56 ----------
AULAS.append(projeto(82, "MÓDULO 15 · AULA 82", "O seu projeto no currículo e na entrevista", [
    ("Agora você tem um projeto de automação. Vamos colocar isso no seu currículo do jeito certo.", titulo(82, "CURRÍCULO")),
    ("No currículo, escreve o que você realmente fez: testes de ponta a ponta com Playwright e JavaScript, Page Object e fixtures, testes de API, vários navegadores e execução no GitHub Actions.",
     {"type": "traducao", "titulo": "NO CURRÍCULO", "linhas": [["Playwright + JavaScript", "testes de ponta a ponta"], ["Page Object + fixtures", "código organizado e reaproveitável"],
                                                             ["request (API)", "testes de API"], ["projects", "Chromium, Firefox, WebKit e celular"], ["GitHub Actions", "testes rodando a cada push"]]}),
    ("E do nível dois: mock de rede, teste visual, tags e dados em JSON. E o mais importante: dois projetos no GitHub, um deles com um bug que você achou.",
     {"type": "traducao", "titulo": "NO CURRÍCULO · NÍVEL 2", "linhas": [["route (mock)", "testa erro e lista vazia sem derrubar nada"], ["toHaveScreenshot", "teste visual"],
                                                                       ["tags + JSON", "smoke, regressivo e dados separados"], ["2 projetos no GitHub", "um com um bug real achado"]]}),
    ("A regra: só coloca o que você consegue explicar numa entrevista.", bt(("SÓ COLOCA", "white", 120), ("O QUE VOCÊ EXPLICA", "gold", 140))),
    ("Perguntas que costumam aparecer e que você já sabe responder: o que é auto-wait? Por que preferir seletores pela função? O que é Page Object?",
     {"type": "cards", "titulo": "PERGUNTA → RESPOSTA CURTA", "itens": [["?", "Auto-wait", "ele espera o elemento ficar pronto"], ["?", "Seletor pela função", "parte do que a pessoa usa", AZUL],
                                                                     ["?", "Page Object", "cada página vira uma classe", AMARELO]]}),
    ("E o que é um teste flaky, que às vezes passa e às vezes falha? E como evitar?",
     {"type": "cards", "titulo": "FLAKY", "itens": [["≈", "Às vezes passa", "às vezes falha", VERM], ["✓", "Como evitar", "expect que espera, sem tempo fixo", "#3fd68a"]]}),
    ("E uma pergunta que quase sempre aparece: conta um bug que você achou. E você tem uma história: a ordenação da Lojinha, achada na mão, antes de automatizar, registrada num card, e depois coberta pelos testes.",
     {"type": "cards", "titulo": "CONTA UM BUG QUE VOCÊ ACHOU", "itens": [["🐞", "O bug", "a ordenação por preço"], ["👀", "Como achou", "testando na mão, antes do código", AZUL],
                                                                       ["📋", "O que fez", "card com print", AMARELO], ["✓", "E depois", "automatizou: nunca mais volta", "#3fd68a"]]}),
    ("Mostrar o projeto funcionando no GitHub ajuda muito a transformar o que está no currículo numa demonstração concreta.",
     {"type": "gh_actions", "usuario": "voce", "repo": "meu-primeiro-playwright", "workflow": "Playwright Tests", "commit": "testes no GitHub Actions", "pronto": True, "status": "ok",
      "artefato": "playwright-report", "legenda": "O currículo vira demonstração"}),
    ("Te vejo na última aula!", {"type": "endcard", "sub": "PRÓXIMA: PORTFÓLIO E COLINHA"}),
]))

# ---------- Aula 57 ----------
L_SELO = 3
AULAS.append(projeto(83, "MÓDULO 15 · AULA 83", "Seu projeto pronto pro portfólio e a colinha completa", [
    ("Última aula. Vamos deixar o seu projeto pronto pra quem visitar.", titulo(83, "PORTFÓLIO")),
    ("Dentro, escreve: o objetivo, as tecnologias, o que precisa instalar, como instalar, e os comandos pra rodar os testes.",
     edc(README, "README.md: a vitrine do projeto", arquivo="README.md", pastas=ARV_R, digitar=True, digitar_de=5, digitar_ate=16, vel=0.85, fonte=22,
         criar=[["Na pasta do projeto, cria um arquivo novo: README ponto md. É a primeira coisa que alguém vê quando abre o seu projeto no GitHub.", "README.md"]])),
    ("Coloca o selinho do GitHub Actions. O próprio GitHub gera o código dele, com o endereço do seu repositório e do seu workflow.",
     edc(README, "O selo: o endereço do repositório + o do workflow", arquivo="README.md", digitar=True, digitar_de=L_SELO, digitar_ate=L_SELO, vel=0.6, fonte=22, destaque=[L_SELO], destaque_em=99)),
    ("Ele mostra se os testes estão passando.",
     {"type": "github", "tela": "readme", "usuario": "voce", "repo": "meu-primeiro-playwright", "titulo_readme": "Meu primeiro projeto Playwright", "selo_em": 0.3, "foco_em": 0.8,
      "linhas_readme": [["p", "Testes de ponta a ponta da loja de treino saucedemo.com."], ["h", "Tecnologias"], ["p", "Playwright, JavaScript, Page Object, GitHub Actions"]],
      "legenda": "Verde: os testes estão passando"}),
    ("E a sua colinha completa: do primeiro comando ao Page Object,",
     {"type": "tela", "media": "colinha_pg4", "url": COLINHA, "pagina": 4, "titulo": "colinha-playwright-para-leigos.pdf", "legenda": "Page Object"}),
    ("ao login salvo, ao GitHub Actions e à API.",
     {"type": "tela", "media": "colinha_pg4b", "url": COLINHA, "pagina": 4, "rolar_y": 900, "titulo": "colinha-playwright-para-leigos.pdf", "legenda": "Login salvo, API e GitHub Actions"}),
    ("E a página cinco, com o nível dois inteiro. São cinco páginas: deixa ela aberta enquanto pratica.",
     {"type": "tela", "media": "colinha_pg5", "url": COLINHA, "pagina": 5, "titulo": "colinha-playwright-para-leigos.pdf", "legenda": "Página 5: o nível 2"}),
    ("Você começou sem saber nada e terminou com dois projetos: o primeiro, com login, compra, API e tudo rodando no GitHub.",
     {"type": "cards", "titulo": "PROJETO 1", "itens": [["🔑", "Login", "vários usuários"], ["🛒", "Compra", "do começo ao fim", AZUL], ["⇄", "API", "em milissegundos", AMARELO], ["✓", "GitHub", "rodando sozinho", "#3fd68a"]]}),
    ("E o segundo, que começou num card: os cenários, o bug achado na mão, e a automação que garante que ele não volta.",
     {"type": "cards", "titulo": "PROJETO 2", "itens": [["📋", "O card", "e as dúvidas"], ["✎", "Os cenários", "em português", AZUL], ["🐞", "O bug", "achado na mão", VERM], ["✓", "A automação", "de guarda no GitHub", "#3fd68a"]]}),
    ("Próximos passos: pratique, crie novos cenários e mantenha o seu GitHub atualizado.",
     {"type": "cards", "titulo": "PRÓXIMOS PASSOS", "itens": [["⌨", "Pratique", "um pouco todo dia"], ["＋", "Novos cenários", "outros sites e fluxos", AZUL], ["⑂", "GitHub atualizado", "a sua vitrine", AMARELO]]}),
    ("E se o curso te ajudou, deixa uma avaliação honesta na Udemy. Ela ajuda a melhorar o curso e orienta outros alunos.",
     bt(("★★★★★", "gold", 130), ("SUA AVALIAÇÃO", "white", 120), ("AJUDA OUTROS ALUNOS", "muted", 70))),
    ("Até a próxima!", {"type": "endcard", "sub": "OBRIGADO POR FAZER O CURSO!"}),
]))


def main():
    out = ["# Roteiros aprovados · Módulo 12 (gerado do roteiro_playwright_m12.py)", ""]
    for slug, p in AULAS:
        d = os.path.join(RAIZ, "projetos", slug); os.makedirs(d, exist_ok=True)
        json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        out.append("## " + p["meta"]["titles"][0])
        out += [f"{i}. {s['text']} [{s['scene']['type']}]" for i, s in enumerate(p["script"]["long"]["parts"][0]["sentences"], 1)] + [""]
        print(slug, len(p["script"]["long"]["parts"][0]["sentences"]), "frases")
    open(os.path.join(RAIZ, "curso-playwright", "roteiros", "modulo15.md"), "w", encoding="utf8").write("\n".join(out))


if __name__ == "__main__":
    main()

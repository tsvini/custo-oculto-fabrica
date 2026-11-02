"""Vini QA lote 2: 6 shorts de dicas de Cypress que fecham com o cupom LANCAMENTO (até 3/12).
Uso: python ferramentas/viniqa_lote2.py  → projetos/viniqa-lote2/projeto.json e agenda.json"""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = "https://www.udemy.com/course/cypress-para-leigos-testes-automatizados-do-zero/?couponCode=LANCAMENTO"
AZUL, AMARELO, VERM = "#69a7ff", "#ffd23f", "#ff6b6b"


def bt(*linhas):
    return {"type": "bigtext", "stagger": 0.25, "lines": [list(l) for l in linhas]}


def ed(cod, legenda, destaque=(), fonte=28, arquivo="login.cy.js"):
    d = {"type": "editor", "arquivo": arquivo, "codigo": cod, "legenda": legenda, "fonte": fonte}
    if destaque:
        d["destaque"] = list(destaque)
    return d


CTA = ("Curso completo de Cypress do zero: até três de dezembro, sai por vinte e quatro e noventa com o cupom LANCAMENTO. Link na bio.",
       bt(("R$ 24,90", "gold", 170), ("CUPOM LANCAMENTO", "white", 110), ("LINK NA BIO", "white", 110)))

SHORTS = [
    ("Pare de usar cy.wait com tempo fixo", [
        ("Para de usar cy ponto wait com tempo fixo no seu teste.", bt(("CY.WAIT(3000)?", "white", 120), ("PARA COM ISSO", "gold", 130))),
        ("Esperar três segundos na sorte deixa o teste lento. E se o site demorar quatro, ele quebra do mesmo jeito.",
         {"type": "cards", "itens": [["⏱", "Espera fixa", "lento sempre"], ["✗", "Site demorou mais", "quebra igual", VERM]]}),
        ("O Cypress já espera sozinho: o should tenta de novo, por até quatro segundos, até o elemento aparecer.",
         ed("cy.get('[data-test=\"title\"]')\n  .should('have.text', 'Products')", "should espera sozinho", destaque=[2], fonte=34)),
        ("Ou seja: espere o que importa, não o relógio.", bt(("ESPERE O QUE IMPORTA", "gold", 110), ("NÃO O RELÓGIO", "white", 130))),
        CTA]),
    ("Teste também o que dá errado", [
        ("Um bom teste de login não confere só quem entra. Confere também quem não pode entrar.", bt(("QUEM NÃO", "white", 140), ("PODE ENTRAR?", "gold", 140))),
        ("Isso se chama cenário negativo: senha errada, campo vazio, usuário bloqueado. É onde mais aparece bug.",
         {"type": "traducao", "titulo": "CENÁRIO NEGATIVO", "linhas": [["senha errada", "mostra o erro?"], ["campo vazio", "avisa?"], ["usuário bloqueado", "barra a entrada?"]]}),
        ("No Cypress: preenche a senha errada, clica, e confere que a mensagem de erro apareceu.",
         ed("cy.get('[data-test=\"username\"]').type('standard_user')\ncy.get('[data-test=\"password\"]').type('errada')\ncy.get('[data-test=\"login-button\"]').click()\ncy.get('[data-test=\"error\"]')\n  .should('contain', 'do not match')", "Senha errada: o erro aparece", destaque=[4, 5], fonte=24)),
        ("Quase ninguém testa isso. Por isso é tão valioso.", bt(("QUASE NINGUÉM TESTA", "white", 110), ("POR ISSO VALE OURO", "gold", 120))),
        CTA]),
    ("describe e it em português", [
        ("Describe e it parecem difíceis. Mas lendo em português, é bem simples.", bt(("DESCRIBE E IT", "white", 140), ("EM PORTUGUÊS", "gold", 140))),
        ("Describe é descrever: junta os testes de um assunto numa caixa com nome.",
         {"type": "traducao", "codigo": "describe('Login', () => {", "partes": [["describe", "junte numa caixa"], ["'Login'", "chamada Login"]], "passo": 1.4}),
        ("E o it é cada teste dessa caixa: o nome diz o que ele confere.",
         {"type": "traducao", "codigo": "it('entra com usuário e senha', () => {", "partes": [["it", "um teste"], ["'entra com usuário e senha'", "o que ele confere"]], "passo": 1.4}),
        ("Lendo tudo: na caixa Login, um teste que entra com usuário e senha.", bt(("NA CAIXA LOGIN", "white", 120), ("UM TESTE QUE ENTRA", "gold", 120))),
        CTA]),
    ("Rode só o teste que você está mexendo", [
        ("Tem vinte testes no arquivo e quer rodar só um? Tem um jeito.", bt(("20 TESTES", "white", 150), ("QUER RODAR SÓ 1?", "gold", 120))),
        ("Coloca ponto only logo depois do it. Only quer dizer somente: o Cypress roda só esse.",
         ed("it.only('entra com usuário e senha', () => {\n  cy.visit('/')\n})", "only = somente esse", destaque=[1], fonte=30)),
        ("E o ponto skip faz o contrário: pula esse teste.",
         ed("it.skip('teste que ainda não está pronto', () => {\n  cy.visit('/')\n})", "skip = pula esse", destaque=[1], fonte=30)),
        ("Só não esquece de tirar o only antes de mandar pro GitHub, senão os outros testes param de rodar.",
         {"type": "cards", "itens": [["⚠", "Esqueceu o only?", "os outros param de rodar", VERM], ["✓", "Tira antes do push", "e roda tudo", "#3fd68a"]]}),
        CTA]),
    ("O básico de automação que todo QA júnior precisa", [
        ("Tá começando em QA e quer aprender automação? Todo teste é feito de três coisas.", bt(("TODO TESTE", "white", 150), ("É FEITO DE 3 COISAS", "gold", 110))),
        ("Primeiro, o seletor: como o robô acha o botão na tela.", {"type": "traducao", "titulo": "TODO TESTE", "linhas": [["1. seletor", "acha o botão"]]}),
        ("Depois, a ação: clicar, digitar, escolher.", {"type": "traducao", "titulo": "TODO TESTE", "linhas": [["1. seletor", "acha o botão"], ["2. ação", "clica, digita"]]}),
        ("E a conferência: o teste confere se deu certo. Sem ela, não é teste.",
         {"type": "traducao", "titulo": "TODO TESTE", "linhas": [["1. seletor", "acha o botão"], ["2. ação", "clica, digita"], ["3. conferência", "deu certo?"]]}),
        CTA]),
    ("Cypress ou Playwright: qual aprender primeiro?", [
        ("Cypress ou Playwright: qual aprender primeiro?", {"type": "compare", "items": [["CYPRESS", "", "white"], ["PLAYWRIGHT", "", "gold"]], "size": 110, "stagger": 0.8, "vs": True}),
        ("Os dois são ótimos e muito usados em empresa. A lógica é a mesma: seletor, ação e conferência.",
         {"type": "cards", "itens": [["✓", "Os dois", "muito usados"], ["=", "A mesma lógica", "seletor, ação, conferência", AZUL]]}),
        ("Pra quem nunca automatizou nada, o Cypress é o mais fácil de começar: abre, roda e você vê o teste acontecendo.",
         bt(("PRA COMEÇAR", "white", 130), ("CYPRESS", "gold", 170))),
        ("E quando você aprende um, o outro fica muito mais fácil. O curso de Playwright está chegando.",
         bt(("APRENDEU UM", "white", 130), ("O OUTRO FICA FÁCIL", "gold", 120))),
        CTA]),
]

DATAS = ["2026-11-16", "2026-11-18", "2026-11-20", "2026-11-23", "2026-11-25", "2026-11-27"]
TAGS = ["#cypress #qa #testes #automacao", "#qa #testes #cypress #bugs", "#cypress #qa #programacao #testes",
        "#cypress #qa #dicas #testesautomatizados", "#qa #carreira #automacao #tecnologia", "#cypress #playwright #qa #automacao"]


def main():
    lote1 = json.load(open(os.path.join(RAIZ, "projetos", "viniqa-lote1", "projeto.json"), encoding="utf8"))
    p = {k: lote1[k] for k in ("title", "slug", "idioma", "destino", "marca", "cor_fundo", "legenda_y", "voz", "serie", "notes")}
    p.update(title="Vini QA · lote 2", slug="viniqa-lote2", meta={"titles": ["Vini QA lote 2"], "description": "", "tags": []})
    p["script"] = {"long": {"parts": [{"chapter": "", "sentences": [{"text": "Vini QA.", "scene": bt(("VINI QA", "gold", 150))}]}]},
                   "shorts": [{"title": t, "sentences": [{"text": a, "scene": b} for a, b in fr]} for t, fr in SHORTS], "tiktoks": []}
    d = os.path.join(RAIZ, "projetos", "viniqa-lote2"); os.makedirs(d, exist_ok=True)
    json.dump(p, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    ag = {"canal": "Vini QA", "link_curso": LINK, "cupom": {"texto": "🔥 Até 3/12, sai por R$ 24,90 com o cupom LANCAMENTO (já vem aplicado no link).", "ate": "2026-12-03"},
          "videos": [{"short": i + 1, "data": DATAS[i], "hora": "12:00", "titulo": t,
                      "legenda": f"{fr[0][0]} Curso completo de Cypress do zero: link na bio. {TAGS[i]}"} for i, (t, fr) in enumerate(SHORTS)]}
    json.dump(ag, open(os.path.join(d, "agenda.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("ok", len(SHORTS), "shorts")


if __name__ == "__main__":
    main()

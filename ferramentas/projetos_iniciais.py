"""Monta os projetos iniciais de cada módulo do Playwright para Leigos: o projeto do aluno exatamente como ele está
no começo daquele módulo (= o fim do módulo anterior). Saída: curso-playwright/material/projetos-iniciais/<nome>/ e um .zip de cada.
Os arquivos vêm das etapas validadas (curso-playwright/projeto/tests/etapas) e do projeto final; o config é montado a partir do
que o "npm init playwright" gera, com as mesmas mudanças das aulas. Validado no Actions (validar_iniciais.yml)."""
import os, re, shutil, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CP = os.path.join(RAIZ, "curso-playwright")
REF, PROJ = os.path.join(CP, "referencia_init"), os.path.join(CP, "projeto")
SAIDA = os.path.join(CP, "material", "projetos-iniciais")
ler = lambda *p: open(os.path.join(*p), encoding="utf8").read()


def etapa(n):
    s = ler(PROJ, "tests", "etapas", f"aula{n}.spec.js")
    return re.sub(r"aula \d+: ", "", s).replace("'../../pages/", "'../pages/")


CFG_REF = ler(REF, "playwright.config.js")
CFG_ENV = (CFG_REF.replace("// import dotenv from 'dotenv';", "import dotenv from 'dotenv';").replace("// import path from 'path';", "import path from 'path';")
           .replace("// dotenv.config(", "dotenv.config(")
           .replace("    // baseURL: 'http://localhost:3000',", "    baseURL: 'https://www.saucedemo.com',\n    testIdAttribute: 'data-test',"))
CFG_PRINT = CFG_ENV.replace("    trace: 'on-first-retry',\n", "    trace: 'on-first-retry',\n    screenshot: 'only-on-failure',\n    video: 'retain-on-failure',\n")
CFG_CEL = CFG_PRINT.replace("      use: { ...devices['Desktop Safari'] },\n    },\n", "      use: { ...devices['Desktop Safari'] },\n    },\n\n    {\n      name: 'celular',\n      use: { ...devices['Pixel 7'] },\n    },\n", 1)
assert CFG_ENV != CFG_REF and CFG_PRINT != CFG_ENV and CFG_CEL != CFG_PRINT

PKG_REF = ler(REF, "package.json")
PKG_ENV = ler(PROJ, "package.json")
YML_REF = ler(REF, ".github", "workflows", "playwright.yml")
YML_ENV = ler(PROJ, ".github", "workflows", "playwright.yml")
GIT_REF = ler(REF, ".gitignore")
GIT_ENV = ler(PROJ, ".gitignore")
ENV_EX = ler(PROJ, ".env.example")
FINAL = {f"tests/{a}": ler(PROJ, "tests", a) for a in ("auth.setup.js", "compra.spec.js", "login.spec.js", "usuarios.spec.js")}
FINAL.update({f"pages/{a}": ler(PROJ, "pages", a) for a in sorted(os.listdir(os.path.join(PROJ, "pages")))})

import re as _re
NIVEL2_INTERNET = _re.sub(r"aula \d+: ", "", ler(PROJ, "tests", "nivel2", "internet.spec.js"))
P2 = os.path.join(CP, "projeto2")
PROJ2 = {os.path.relpath(os.path.join(r, f), P2).replace(os.sep, "/"): ler(r, f) for r, _, fs in os.walk(P2) if "node_modules" not in r for f in fs if f != "package-lock.json"}
PROJ2[".github/workflows/playwright.yml"] = YML_ENV.replace("SAUCE_USER", "LOJA_USUARIO").replace("SAUCE_PASSWORD", "LOJA_SENHA")

LEIA = """Projeto inicial · {titulo}

Este é o projeto exatamente como ele fica no começo deste módulo. Use se você se perdeu ou quer começar daqui.

1. Descompacte numa pasta (sem espaço e sem acento no nome, ex.: meu-primeiro-playwright).
2. Abra a pasta no VS Code (File › Open Folder).
3. No terminal do VS Code:  npm install
4. E depois:                npx playwright install
{env}5. Pra conferir que está tudo certo:  npx playwright test --project=chromium
"""
ENV_PASSO = "   Copie o arquivo .env.example para .env (é ali que ficam o usuário e a senha).\n"

BASE_REF = {".gitignore": GIT_REF, "package.json": PKG_REF, ".github/workflows/playwright.yml": YML_REF}
BASE_ENV = {".gitignore": GIT_ENV, "package.json": PKG_ENV, ".github/workflows/playwright.yml": YML_REF, ".env.example": ENV_EX}

ETAPAS = [
    ("modulo-03", "Módulo 3 · O primeiro teste", dict(BASE_REF, **{"playwright.config.js": CFG_REF, "tests/example.spec.js": ler(REF, "tests", "example.spec.js")})),
    ("modulo-04", "Módulo 4 · Achando os elementos", dict(BASE_REF, **{"playwright.config.js": CFG_REF, "tests/login.spec.js": etapa(16)})),
    ("modulo-05", "Módulo 5 · Organizando os testes", dict(BASE_REF, **{"playwright.config.js": CFG_REF, "tests/login.spec.js": etapa(21)})),
    ("modulo-06", "Módulo 6 · Quando o teste falha", dict(BASE_ENV, **{"playwright.config.js": CFG_ENV, "tests/login.spec.js": etapa(24)})),
    ("modulo-07", "Módulo 7 · Mais testes com pouco código", dict(BASE_ENV, **{"playwright.config.js": CFG_PRINT, "tests/login.spec.js": etapa(24)})),
    ("modulo-08", "Módulo 8 · O projeto final", dict(BASE_ENV, **{"playwright.config.js": CFG_CEL, "tests/login.spec.js": etapa(24), "tests/usuarios.spec.js": FINAL["tests/usuarios.spec.js"]})),
    ("modulo-09", "Módulo 9 · Git, GitHub e Actions", dict(BASE_ENV, **{"playwright.config.js": ler(PROJ, "playwright.config.js")}, **FINAL)),
    ("modulo-10", "Módulo 10 · Testes de API", dict(BASE_ENV, **{"playwright.config.js": ler(PROJ, "playwright.config.js"), ".github/workflows/playwright.yml": YML_ENV}, **FINAL)),
    ("modulo-11", "Módulo 11 · Desafios", dict(BASE_ENV, **{"playwright.config.js": ler(PROJ, "playwright.config.js"), ".github/workflows/playwright.yml": YML_ENV,
                                                          "tests/api.spec.js": ler(PROJ, "tests", "api.spec.js")}, **FINAL)),
    ("projeto-final", "Projeto final (com os desafios resolvidos)", dict(BASE_ENV, **{"playwright.config.js": ler(PROJ, "playwright.config.js"), ".github/workflows/playwright.yml": YML_ENV,
                                                          "tests/api.spec.js": ler(PROJ, "tests", "api.spec.js"), "tests/desafios.spec.js": ler(PROJ, "tests", "desafios.spec.js")}, **FINAL)),

    ("modulo-12", "Módulo 12 · Nível 2: um site que você nunca viu", dict(BASE_ENV, **{"playwright.config.js": ler(PROJ, "playwright.config.js"), ".github/workflows/playwright.yml": YML_ENV,
                                                          "tests/api.spec.js": ler(PROJ, "tests", "api.spec.js"), "tests/desafios.spec.js": ler(PROJ, "tests", "desafios.spec.js")}, **FINAL)),
    ("modulo-13", "Módulo 13 · Playwright de verdade no trabalho", dict(BASE_ENV, **{"playwright.config.js": ler(PROJ, "playwright.config.js"), ".github/workflows/playwright.yml": YML_ENV,
                                                          "tests/api.spec.js": ler(PROJ, "tests", "api.spec.js"), "tests/desafios.spec.js": ler(PROJ, "tests", "desafios.spec.js"),
                                                          "tests/nivel2/internet.spec.js": NIVEL2_INTERNET, "arquivos/exemplo.txt": ler(PROJ, "arquivos", "exemplo.txt")}, **FINAL)),
    ("projeto-2-final", "Projeto 2 · Lojinha do Leigo (o projeto do módulo 14, pronto)", PROJ2),
]


def main():
    shutil.rmtree(SAIDA, ignore_errors=True); os.makedirs(SAIDA)
    for nome, titulo, arqs in ETAPAS:
        d = os.path.join(SAIDA, nome)
        arqs = dict(arqs); arqs["LEIA-ME.txt"] = LEIA.format(titulo=titulo, env=ENV_PASSO if ".env.example" in arqs else "")
        if nome == "projeto-2-final":
            arqs["LEIA-ME.txt"] = arqs["LEIA-ME.txt"].replace("o projeto exatamente como ele fica no começo deste módulo", "o projeto 2 pronto, do jeito que ele fica no fim do módulo 14").replace("ex.: meu-primeiro-playwright", "ex.: projeto-lojinha")
        for rel, conteudo in arqs.items():
            p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf8", newline="\n").write(conteudo if conteudo.endswith("\n") else conteudo + "\n")
        z = os.path.join(SAIDA, f"playwright-para-leigos-{nome}.zip")
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel in sorted(arqs):
                zf.write(os.path.join(d, rel), os.path.join("projeto-lojinha" if nome == "projeto-2-final" else "meu-primeiro-playwright", rel))
        print(nome, len(arqs), "arquivos")


if __name__ == "__main__":
    main()

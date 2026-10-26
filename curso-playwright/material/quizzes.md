# Quizzes da Udemy: Playwright para Leigos

Um quiz no fim de cada módulo. Na Udemy: **Currículo › + Item do currículo › Quiz**, depois **+ Pergunta**.
Em cada pergunta, a resposta certa está marcada com ✅. O texto depois de "Por quê" vai no campo de explicação da resposta certa. Nas erradas, a explicação é opcional.
O módulo 11 (desafios) não tem quiz: os próprios desafios já são a prática.

---

## Quiz do Módulo 1: Preparando o computador

**1. Pra que serve o VS Code?**
- ✅ Pra escrever o código dos testes
- Pra rodar os testes no navegador
- Pra guardar o projeto na internet
- Pra instalar o Playwright

Por quê: o VS Code é o editor, onde a gente escreve. Quem roda os testes é o Playwright, e quem guarda na internet é o GitHub.

**2. Qual versão do Node.js você deve baixar?**
- ✅ A LTS
- A mais nova de todas (Current)
- Qualquer uma, tanto faz
- A mais antiga, que é mais leve

Por quê: LTS quer dizer suporte de longo prazo. É a versão mais estável, a que as empresas usam.

**3. Você instalou o Node, abriu o terminal e digitou `npx`, mas aparece "não é reconhecido". O que fazer primeiro?**
- ✅ Fechar e abrir de novo o terminal e o VS Code
- Desinstalar o Windows
- Instalar o Python
- Trocar de navegador

Por quê: quase sempre o terminal foi aberto antes da instalação, então ele ainda não conhece o Node. Reabrir resolve na maioria das vezes.

**4. No Windows, aparece "a execução de scripts foi desabilitada neste sistema". O que é isso?**
- ✅ Uma trava de segurança do PowerShell, que se libera com um comando uma vez só
- Um vírus no computador
- Um erro no código do teste
- Falta de internet

Por quê: é a política de execução do PowerShell. O comando `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` libera.

---

## Quiz do Módulo 2: Criando o projeto

**1. Qual comando cria o projeto e instala o Playwright?**
- ✅ `npm init playwright@latest`
- `npx playwright test`
- `git init`
- `node -v`

Por quê: é ele que faz as quatro perguntas e cria a estrutura toda do projeto, com os navegadores.

**2. Por que é melhor uma pasta chamada `meu-primeiro-playwright` do que `meu primeiro playwright`?**
- ✅ Nome sem espaço e sem acento evita problemas com caminhos e comandos
- O Playwright não funciona em pastas com letra minúscula
- É uma regra do Windows
- Pasta com traço roda mais rápido

Por quê: espaço e acento às vezes atrapalham no terminal. Com traço, tudo fica mais simples.

**3. Como o Playwright sabe que um arquivo é de teste?**
- ✅ O nome termina em `.spec.js`
- O arquivo fica na área de trabalho
- O nome começa com "teste"
- O arquivo tem mais de 10 linhas

Por quê: por padrão, ele procura arquivos `.spec.js` (ou `.test.js`) na pasta de testes.

**4. Em qual pasta você nunca precisa mexer?**
- ✅ `node_modules`
- `tests`
- `pages`
- Nenhuma, todas são editadas sempre

Por quê: a `node_modules` guarda as bibliotecas instaladas pelo npm. Ela é recriada sozinha e nem vai pro GitHub.

**5. O que o `npx playwright show-report` faz?**
- ✅ Abre o relatório HTML da última execução
- Roda os testes de novo
- Mostra a versão do Playwright
- Apaga os testes que falharam

Por quê: o relatório lista cada teste, em cada navegador, com o que passou e o que falhou.

---

## Quiz do Módulo 3: O primeiro teste

**1. Pra que serve o `await`?**
- ✅ Esperar aquele passo terminar antes de ir pro próximo
- Deixar o teste mais rápido
- Repetir o passo várias vezes
- Esconder o navegador

Por quê: abrir um site ou clicar leva um tempinho. Sem o `await`, o teste corre na frente e falha sem motivo claro.

**2. O que faz o `fill`?**
- ✅ Apaga o que tinha no campo e digita o texto novo
- Clica no campo
- Confere se o campo está preenchido
- Acrescenta o texto no fim do que já tinha

Por quê: fill quer dizer preencher. Ele limpa o campo antes de digitar.

**3. Como se lê `await expect(page).toHaveURL(/inventory/)`?**
- ✅ Eu espero que a página tenha "inventory" no endereço
- Vá para o endereço inventory
- Clique no link inventory
- Espere 5 segundos e abra o inventory

Por quê: o `expect` é a conferência. Ele não faz nada no site, só verifica.

**4. Qual a diferença entre `toHaveText` e `toContainText`?**
- ✅ `toHaveText` confere o texto exato; `toContainText` aceita só um pedaço
- Não tem diferença
- `toContainText` só funciona em botões
- `toHaveText` só funciona em títulos

Por quê: com `toContainText('do not match')`, você não precisa escrever a mensagem de erro inteira.

**5. Pra conferir que um elemento sumiu da tela, você usa...**
- ✅ `not.toBeVisible()`
- `toBeHidden(false)`
- `toBeVisible(0)`
- `toHaveCount('nada')`

Por quê: o `not` inverte qualquer expect: "eu espero que não esteja visível".

---

## Quiz do Módulo 4: Achando os elementos

**1. Qual desses seletores costuma ser o mais confiável?**
- ✅ `getByTestId('username')`, uma etiqueta feita só pra teste
- `locator('div:nth-child(3) > input')`
- O XPath completo copiado do navegador
- A classe CSS do botão

Por quê: o data-test não muda quando o visual muda. Seletor pela posição ou pela classe quebra à toa.

**2. O que o `getByRole('button', { name: 'Login' })` procura?**
- ✅ Um botão com o nome Login, do jeito que uma pessoa enxerga
- Qualquer coisa escrita Login
- Um campo chamado button
- O primeiro botão da página

Por quê: get by role acha pela função do elemento (botão, link, campo) e pelo nome dele.

**3. Pra que serve o Codegen?**
- ✅ Você clica no site e ele escreve o código do teste
- Ele corrige os erros do seu código
- Ele roda os testes mais rápido
- Ele publica o projeto no GitHub

Por quê: `npx playwright codegen` grava as suas ações. É ótimo pra descobrir seletores.

**4. O teste dá "strict mode violation: resolved to 20 elements". O que aconteceu?**
- ✅ O seletor achou 20 elementos, e o Playwright não sabe em qual clicar
- O site tem 20 erros
- O teste demorou 20 segundos
- Faltam 20 navegadores

Por quê: o seletor precisa ser específico. Ou você melhora o seletor, ou escolhe um, com `.first()`.

**5. Por que no Playwright quase nunca é preciso colocar "espera 3 segundos"?**
- ✅ Ele espera sozinho o elemento ficar pronto antes de agir ou conferir
- Porque os sites são sempre rápidos
- Porque ele não usa navegador
- Porque o VS Code espera por ele

Por quê: é a espera automática (auto-wait). Tempo fixo deixa o teste lento ou instável.

---

## Quiz do Módulo 5: Organizando os testes

**1. Pra que serve o `test.beforeEach`?**
- ✅ Rodar um passo antes de cada teste, como abrir o site
- Rodar os testes em ordem alfabética
- Pular o primeiro teste
- Rodar uma vez só, no fim de tudo

Por quê: assim você não repete o `goto` em todo teste.

**2. Com `baseURL: 'https://www.saucedemo.com'` no config, o `page.goto('/')` abre...**
- ✅ O saucedemo
- Uma página em branco
- O Google
- Dá erro, porque falta o endereço

Por quê: o baseURL é o começo do endereço. O `/` é colado nele.

**3. Por que usar o arquivo `.env` pro usuário e a senha?**
- ✅ Pra senha não ficar no código nem subir pro GitHub
- Porque o Playwright só lê senha de arquivo
- Pra o teste rodar mais rápido
- Porque o VS Code exige

Por quê: o `.env` fica no `.gitignore`. No GitHub, a senha vai nos Secrets.

**4. O que acontece se você esquecer um `test.only` no código e mandar pro GitHub?**
- ✅ O GitHub Actions falha de propósito, por causa do `forbidOnly`
- Nada, ele é ignorado
- Todos os testes rodam duas vezes
- O GitHub apaga o teste

Por quê: o config gerado tem `forbidOnly: !!process.env.CI`. É uma proteção pra ninguém esquecer.

**5. Qual comando roda só os testes que têm "bloqueado" no nome?**
- ✅ `npx playwright test -g "bloqueado"`
- `npx playwright test bloqueado.only`
- `npx playwright skip bloqueado`
- `npx playwright bloqueado`

Por quê: o `-g` (grep) filtra pelo título do teste.

---

## Quiz do Módulo 6: Quando o teste falha

**1. No erro, o que é "Expected" e "Received"?**
- ✅ Expected é o que você pediu; Received é o que tinha de verdade
- Expected é o tempo; Received é o navegador
- Os dois querem dizer erro
- Expected é o arquivo; Received é a linha

Por quê: comparar os dois quase sempre mostra o problema na hora.

**2. Pra que serve o Trace Viewer?**
- ✅ Ver o filme do teste, passo a passo, com a página, o console e a rede
- Escrever o teste por você
- Mandar o erro por e-mail
- Rodar o teste em outro computador

Por quê: é a caixa-preta do teste. Serve muito quando o teste falha no GitHub, onde você não estava olhando.

**3. O que faz o `await page.pause()`?**
- ✅ Para o teste ali e abre o inspetor, pra você investigar
- Espera 1 segundo
- Encerra o teste com sucesso
- Pula o próximo passo

Por quê: é um ponto de parada. Você confere a tela e continua quando quiser.

**4. Com `screenshot: 'only-on-failure'` no config, quando o print é tirado?**
- ✅ Só quando o teste falha
- Em todo passo
- Nunca
- Só no primeiro teste

Por quê: assim o relatório tem a foto do momento do erro, sem encher o projeto de imagens.

---

## Quiz do Módulo 7: Mais testes com pouco código

**1. Pra que serve o `for (const usuario of usuarios)` em volta do teste?**
- ✅ Criar o mesmo teste para cada usuário da lista
- Rodar o teste até ele passar
- Deixar o teste mais rápido
- Apagar os usuários depois do teste

Por quê: a lista tem 4 usuários, então o for cria 4 testes, sem copiar código.

**2. O teste dentro do for deu "duplicate test title". Como resolver?**
- ✅ Colocar o usuário no nome do teste, com crase e `${usuario}`
- Apagar o for
- Rodar com `--headed`
- Trocar de navegador

Por quê: cada teste precisa de um nome diferente. Com a crase, o nome muda sozinho a cada volta.

**3. O que são os projects no config?**
- ✅ Os navegadores e aparelhos em que os testes rodam
- As pastas do projeto
- Os arquivos de teste
- As contas do GitHub

Por quê: com chromium, firefox, webkit e celular, cada teste roda 4 vezes, uma em cada.

**4. Emular um celular no Playwright substitui testar num celular de verdade?**
- ✅ Não. Ajuda muito, mas não substitui um aparelho real
- Sim, é exatamente igual
- Sim, desde que use o Pixel 7
- Não, porque emulação não funciona

Por quê: ele simula a tela, o toque e o navegador do aparelho. Um celular real ainda pode ter diferenças.

---

## Quiz do Módulo 8: O projeto final

**1. Por que criar um Page Object (como o `LoginPage`)?**
- ✅ Se o site mudar, você conserta num lugar só, e todos os testes continuam funcionando
- Porque o Playwright não aceita teste sem classe
- Pra o teste rodar em mais navegadores
- Pra esconder o código do professor

Por quê: o seletor e as ações da página ficam na classe. Os testes só chamam `login.entrar(...)`.

**2. O que o `constructor(page)` faz no Page Object?**
- ✅ Recebe o page e guarda os elementos da página
- Abre o site
- Roda o teste
- Apaga o page

Por quê: é a construção do objeto. Ele roda uma vez, quando você faz `new LoginPage(page)`.

**3. Pra que serve o `test.step`?**
- ✅ Dividir o teste em etapas com nome, que aparecem no relatório
- Rodar um teste dentro do outro
- Pular uma etapa
- Repetir uma etapa

Por quê: quando falha, o relatório mostra exatamente em qual etapa foi.

**4. O que o `storageState` resolve?**
- ✅ Fazer o login uma vez e reaproveitar nos outros testes
- Guardar os prints do teste
- Salvar o código no GitHub
- Deixar o navegador aberto pra sempre

Por quê: o setup faz o login e guarda num arquivo. Os testes começam já logados, e ficam mais rápidos.

---

## Quiz do Módulo 9: Git, GitHub e Actions

**1. O que é um commit?**
- ✅ Um ponto de salvamento do projeto, com uma mensagem
- O envio pro GitHub
- Um teste que passou
- Um erro do Git

Por quê: `git commit -m "mensagem"` salva aquela versão. Quem manda pro GitHub é o `git push`.

**2. Por que o `.env` e o `node_modules` não aparecem no GitHub?**
- ✅ Porque estão no `.gitignore`
- Porque o GitHub apaga
- Porque são grandes demais
- Porque estão escondidos no Windows

Por quê: o `.gitignore` lista o que o Git deve deixar de fora.

**3. No GitHub Actions, como os testes sabem o usuário e a senha, se o `.env` não subiu?**
- ✅ Pelos Secrets do repositório, entregues no `env` do yml
- Eles adivinham
- O GitHub lê o `.env` do seu computador
- Não precisa, os testes rodam sem login

Por quê: Settings › Secrets and variables › Actions. Ninguém vê o valor depois de salvo.

**4. Quando o workflow do Playwright roda no GitHub?**
- ✅ A cada push ou pull request na main
- Só quando você clica em rodar
- Uma vez por mês
- Nunca, ele só existe pra enfeitar

Por quê: é o gatilho "on: push / pull_request" do arquivo playwright.yml.

---

## Quiz do Módulo 10: Testes de API

**1. Num teste de API, no lugar do `page`, você pede...**
- ✅ O `request`
- O `browser`
- O `api`
- O `fetch`

Por quê: `async ({ request })`. Não abre navegador nenhum, por isso é tão rápido.

**2. Qual método busca dados e qual cria?**
- ✅ GET busca; POST cria
- GET cria; POST busca
- Os dois buscam
- DELETE cria

Por quê: e o DELETE apaga.

**3. O que quer dizer o status 201?**
- ✅ Criado com sucesso
- Não encontrado
- Erro no servidor
- Acesso negado

Por quê: 200 é deu certo, 201 é criado, 404 é não encontrado.

**4. Qual destas linhas está certa?**
- ✅ `expect(resposta.status()).toBe(200)`
- `expect(resposta.status).toBe(200)`
- `expect(resposta).status(200)`
- `expect(200).toBe(resposta)`

Por quê: o `status()` é uma função, então leva os parênteses.

---

## Quiz do Módulo 12: Um site que você nunca viu

**1. Você marcou uma caixa com `.check()`. Qual é a conferência certa?**
- ✅ `await expect(caixa).toBeChecked();`
- `await expect(caixa).toBeVisible();`
- Não precisa conferir: se o check rodou, marcou
- `await expect(caixa).toHaveText('marcado');`

Por quê: fazer a ação não basta, o teste precisa conferir o resultado. `toBeChecked()` diz que a caixa está marcada.

**2. Um botão abre um alerta do navegador. Onde vai o `page.on('dialog', ...)`?**
- ✅ Antes do clique que abre o alerta
- Depois do clique
- No fim do teste
- Em qualquer lugar, tanto faz

Por quê: o Playwright precisa estar preparado antes de o alerta aparecer. Sem o preparo, ele cancela o alerta sozinho.

**3. Um link abre outra aba. Qual a ordem certa?**
- ✅ `const promessa = page.waitForEvent('popup')`, depois o clique, depois `await promessa`
- O clique, depois `page.waitForEvent('popup')`
- O clique e depois continuar usando o `page`
- Abrir a aba nova com `page.goto`

Por quê: a aba abre muito rápido. Se você começar a esperar só depois do clique, pode perder ela.

**4. O seletor normal não acha um campo que está dentro de um editor encaixado na página. Por quê?**
- ✅ Porque aquele pedaço é um iframe: outra página dentro da página. Primeiro o `frameLocator`
- Porque o campo está escondido
- Porque precisa de um `waitForTimeout`
- Porque o Playwright não funciona nesse site

Por quê: o iframe é outra página encaixada. O `frameLocator` diz em qual quadro procurar.

**5. Por que procurar a linha da tabela com `filter({ hasText: 'Conway' })` em vez de "a segunda linha"?**
- ✅ Porque se alguém ordenar a tabela, a pessoa muda de lugar, e o teste continua achando a pessoa certa
- Porque é mais curto de escrever
- Porque o Playwright não sabe contar linhas
- Porque a segunda linha nunca existe

Por quê: procurar pelo conteúdo deixa o teste estável quando a ordem muda.

---

## Quiz do Módulo 13: Playwright de verdade no trabalho

**1. O que é uma fixture?**
- ✅ Alguma coisa que o teste recebe pronta, como o `page` ou o seu `loginPage`
- Um teste que nunca falha
- Um arquivo de dados em JSON
- Um tipo de erro do Playwright

Por quê: o `page` é uma fixture que o Playwright prepara. Com `test.extend`, você cria as suas.

**2. Você quer saber como a loja reage se o servidor cair. O que usar?**
- ✅ Um mock: `page.route` com `route.abort()`
- Desligar o servidor da empresa
- Um teste visual
- Um `waitForTimeout` bem grande

Por quê: o mock coloca o Playwright no meio da conversa e testa a tela sem estragar nada de verdade.

**3. O teste visual falhou porque alguém mudou o botão de propósito. O que fazer?**
- ✅ Atualizar a foto de referência com `--update-snapshots`
- Apagar o teste visual
- Abrir um card de bug
- Rodar de novo até passar

Por quê: se a mudança foi de propósito, a foto guardada precisa ser atualizada. Se não foi, aí sim é bug visual.

**4. Quando usar `expect.soft`?**
- ✅ Pra conferir vários dados independentes da mesma tela e ver todos os erros de uma vez
- Em todos os passos do fluxo
- Pra deixar o teste mais rápido
- Pra esconder os erros

Por quê: nos passos principais do fluxo, o expect normal continua certo. Se o login falhou, não faz sentido seguir.

**5. Um teste às vezes passa e às vezes falha, sem mudança no código. Qual é a melhor correção?**
- ✅ Trocar o tempo fixo por um expect que espera o que importa
- Aumentar o `waitForTimeout`
- Ligar o retry e esquecer
- Apagar o teste

Por quê: o retry diminui o estrago, mas não corrige a causa. Quase sempre o flaky é uma espera errada.

**6. Pra rodar só os testes críticos antes de uma entrega:**
- ✅ `npx playwright test --grep @smoke`
- `npx playwright test --repeat-each=10`
- `npx playwright test --update-snapshots`
- `npx playwright test --ui`

Por quê: a tag `@smoke` marca o mínimo pra saber se o sistema está de pé, e o `--grep` roda só os marcados.

---

## Quiz do Módulo 14: Projeto 2, pensando como QA

**1. Você recebeu um card sem critérios de aceite. Qual é o primeiro passo?**
- ✅ Entender o problema: o que precisa funcionar, o que pode dar errado e o que está faltando
- Abrir o VS Code e começar a escrever os testes
- Devolver o card sem fazer nada
- Testar só o que está escrito

Por quê: antes do código, a gente entende o problema. As perguntas são o que separa quem escreve teste de quem testa.

**2. O card não diz se o produto esgotado aparece. O que fazer?**
- ✅ Perguntar pra quem pediu e anotar a resposta no card
- Decidir sozinho
- Ignorar o produto esgotado
- Testar os dois jeitos e ver qual passa

Por quê: você não inventa regra de negócio. Pergunta, anota, e aí testa.

**3. Por que a ordenação da versão 1 colocava R$ 12,50 antes de R$ 7,99?**
- ✅ Porque a loja comparava o preço como texto, e em texto o "1" vem antes do "7"
- Porque o produto de R$ 12,50 estava em promoção
- Porque o teste estava errado
- Porque a internet estava lenta

Por quê: comparando como texto, a ordem é a do dicionário. Como número, 7,99 é o menor.

**4. Como o teste confere que os preços estão em ordem?**
- ✅ Lê todos os preços da tela, faz uma cópia, ordena a cópia do jeito certo e compara as duas com `toEqual`
- Confere só o primeiro preço
- Confere se a lista tem 8 produtos
- Tira um print da tela

Por quê: conferir só o primeiro pode deixar passar o bug. A lista inteira pega.

**5. Pagamento não fazia parte da tarefa. O que isso mostra?**
- ✅ Que limitar o escopo também é trabalho de QA
- Que pagamento não precisa ser testado nunca
- Que o card estava errado
- Que o projeto ficou incompleto

Por quê: sem limitar o escopo, você testa a loja inteira e não entrega a tarefa.

---

## Quiz do Módulo 15: Carreira

**1. O que colocar no currículo sobre o projeto?**
- ✅ Só o que você consegue explicar numa entrevista
- Todas as ferramentas que existem
- Que você é especialista em Playwright
- Nada, projeto de curso não conta

Por quê: o entrevistador vai perguntar. Um projeto no GitHub que você sabe explicar vale muito.

**2. O que é um teste flaky?**
- ✅ Um teste que às vezes passa e às vezes falha, sem ninguém mudar nada
- Um teste que sempre falha
- Um teste muito lento
- Um teste sem expect

Por quê: quase sempre é espera mal feita. A solução é esperar a coisa certa, não um tempo fixo.

**3. No Cypress existe o `cy.visit()`. No Playwright, o mais parecido é...**
- ✅ `page.goto()`
- `page.visit()`
- `cy.goto()`
- `request.get()`

Por quê: as ideias são parecidas, mas no Playwright cada passo leva `await`.

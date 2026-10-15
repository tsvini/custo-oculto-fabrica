# Quizzes da Udemy: Cypress para Leigos

Um quiz no fim de cada módulo. Na Udemy: **Currículo › + Item do currículo › Quiz**, depois **+ Pergunta**.
Em cada pergunta, a resposta certa está marcada com ✅. O texto depois de "Por quê" vai no campo de explicação da resposta certa. Nas erradas, a explicação é opcional.

---

## Quiz do Módulo 1: Preparando o computador

**1. Pra que serve o VS Code?**
- ✅ Pra escrever código, como o Word serve pra escrever texto
- Pra rodar os testes no navegador
- Pra guardar o projeto na internet
- Pra instalar programas no computador

Por quê: o VS Code é o editor, onde a gente escreve os testes. Quem roda é o Cypress, e quem guarda na internet é o GitHub.

**2. Qual versão do Node.js você deve baixar?**
- ✅ A LTS
- A mais nova de todas (Current)
- Qualquer uma, tanto faz
- A versão 1.0

Por quê: LTS quer dizer suporte de longo prazo. É a versão mais estável, a que as empresas usam.

**3. Como você confere se o Node foi instalado?**
- ✅ Digitando `node -v` no terminal
- Procurando o ícone do Node na área de trabalho
- Abrindo o site nodejs.org de novo
- Reiniciando o computador

Por quê: se aparecer um número de versão (tipo v22.11.0), está instalado. Não importa se o número é diferente do da aula.

**4. O Git é como...**
- ✅ O "salvar" do videogame: guarda cada versão do projeto
- Um navegador de internet
- Um antivírus
- Um editor de código

Por quê: cada commit é um save. Se algo der errado, dá pra voltar pra um save anterior.

**5. Na instalação do VS Code, qual opção é a mais importante marcar?**
- ✅ Add to PATH
- Create a desktop icon
- Register as an editor for supported file types
- Nenhuma, pode deixar tudo desmarcado

Por quê: o Add to PATH deixa o computador achar o VS Code pelo terminal. Sem ele, alguns comandos não funcionam.

---

## Quiz do Módulo 2: O projeto

**1. No mundo da programação, um projeto é...**
- ✅ Uma pasta com os arquivos dele
- Um programa que você instala
- Um site na internet
- Um arquivo do Word

Por quê: projeto é só uma pasta. A nossa se chama `meu-primeiro-teste`.

**2. Qual é o melhor nome pra pasta do projeto?**
- ✅ `meu-primeiro-teste`
- `Meu Primeiro Teste`
- `meu_primeiro_teste_ÁÉÍ`
- `meu primeiro teste`

Por quê: tudo minúsculo, sem acento e sem espaço. Alguns programas se confundem com espaço e acento.

**3. O que o comando `npm init -y` faz?**
- ✅ Transforma a pasta num projeto e cria o package.json
- Instala o Cypress
- Abre o Cypress
- Apaga a pasta node_modules

Por quê: o `-y` quer dizer "sim pra tudo", então ele cria o package.json sem fazer perguntas.

**4. Pra que serve o `--save-dev` em `npm install cypress --save-dev`?**
- ✅ Avisa que o Cypress é uma ferramenta de quem desenvolve, não uma parte do site
- Salva o projeto no GitHub
- Deixa a instalação mais rápida
- Instala a versão de desenvolvimento, que é instável

Por quê: é tipo a régua do pedreiro. Ela ajuda a construir a casa, mas não faz parte da casa.

**5. O que você deve fazer com a pasta `node_modules`?**
- ✅ Nada, nunca precisa mexer nela
- Apagar depois de instalar
- Editar os arquivos dela pra configurar o Cypress
- Subir ela pro GitHub

Por quê: é onde as ferramentas ficam instaladas de verdade. É enorme e o npm cuida dela sozinho.

---

## Quiz do Módulo 3: O primeiro teste

**1. Qual comando abre a janela do Cypress?**
- ✅ `npx cypress open`
- `npm cypress start`
- `cypress abrir`
- `node cypress`

Por quê: o npm instala as ferramentas e o npx usa elas. `npx cypress open` quer dizer "usa o Cypress e abre ele".

**2. Que tipo de teste a gente escolhe na primeira tela do Cypress?**
- ✅ E2E Testing
- Component Testing
- Unit Testing
- Performance Testing

Por quê: E2E quer dizer de ponta a ponta, o teste que usa o site do jeito que uma pessoa usaria.

**3. Qual é a diferença entre `describe` e `it`?**
- ✅ O describe é o caderno de receitas, e cada it é uma receita (um teste)
- O describe roda primeiro e o it roda depois
- O it é o caderno e o describe é a receita
- Não tem diferença, são a mesma coisa

Por quê: um describe agrupa vários testes. Cada it é um teste separado.

**4. Por que o arquivo se chama `login.cy.js` e não só `login.js`?**
- ✅ O `.cy` avisa o Cypress que esse arquivo é um teste
- Porque o VS Code exige
- Porque o arquivo fica mais leve
- Não precisa, os dois funcionam igual

Por quê: o Cypress procura os arquivos que terminam em `.cy.js` dentro da pasta e2e.

**5. Pra que serve o `should` no teste?**
- ✅ É a conferência: ele confere se aconteceu o que deveria
- Pra esperar alguns segundos
- Pra clicar num botão
- Pra abrir o site

Por quê: sem o should, o teste só clica e digita, mas não confere nada. É ele que faz o teste passar ou falhar.

---

## Quiz do Módulo 4: Indo além

**1. Qual é o seletor mais seguro de usar?**
- ✅ `[data-test="username"]`
- `.input_error.form_input`
- `div > form > div > input`
- `cy.contains('Username')`

Por quê: o data-test foi feito pra testes. A classe muda quando o visual do site muda, e o teste quebra à toa.

**2. Como você descobre o seletor de um campo?**
- ✅ Botão direito no campo › Inspecionar, ou a mira do Cypress (Selector Playground)
- Adivinhando o nome do campo
- Olhando o código do Cypress
- Perguntando pro dono do site

Por quê: o Inspecionar mostra o HTML real do campo, e o Selector Playground já sugere o seletor pronto pra copiar.

**3. O que o `beforeEach` faz?**
- ✅ Roda antes de cada teste do describe
- Roda uma vez só, antes de tudo
- Roda depois de cada teste
- Pula o teste se ele falhar

Por quê: assim você não repete o `cy.visit` em todo teste. Tudo o que fica nele roda antes de cada it.

**4. O teste ficou vermelho com "Timed out retrying". O que isso quer dizer, quase sempre?**
- ✅ O Cypress não achou o elemento: confira o seletor
- O computador está lento
- O Cypress está com defeito
- O teste passou, mas demorou

Por quê: ele tentou achar o elemento por alguns segundos e não conseguiu. Na maioria das vezes é um seletor errado ou uma letra trocada.

**5. Qual é a diferença entre `npx cypress open` e `npx cypress run`?**
- ✅ O open abre a janela pra escrever e ver; o run roda tudo sem janela e mostra um resumo
- O run é só pra Mac
- O open roda mais rápido
- Não tem diferença

Por quê: o run é o jeito que os testes rodam todo dia nas empresas, automaticamente.

---

## Quiz do Módulo 5: O projeto final

**1. Qual é a diferença entre `should('contain', ...)` e `should('have.text', ...)`?**
- ✅ O contain confere se o texto está no meio; o have.text confere se é exatamente aquele texto
- São iguais
- O have.text é mais rápido
- O contain só funciona com números

Por quê: o have.text é mais rigoroso. Pro número do carrinho, a gente quer exatamente "1".

**2. Num arquivo onde todo teste precisa estar logado, onde o login deve ficar?**
- ✅ No beforeEach
- Copiado dentro de cada it
- No final do arquivo
- No package.json

Por quê: assim cada teste já começa logado, sem repetir código.

**3. Pra que serve o arquivo `.gitignore` com `node_modules` dentro?**
- ✅ Avisa o Git pra não subir a pasta node_modules pro GitHub
- Apaga a pasta node_modules
- Esconde os testes que falharam
- Instala o Git

Por quê: a node_modules é gigante e qualquer pessoa recria ela com `npm install`.

**4. Qual a ordem certa dos comandos do Git pra subir o projeto?**
- ✅ `git init` › `git add .` › `git commit -m "..."` › `git push`
- `git push` › `git commit` › `git add .` › `git init`
- `git commit` › `git init` › `git push` › `git add .`
- `git add .` › `git push` › `git init` › `git commit`

Por quê: liga o Git, separa os arquivos, salva o jogo e manda pra internet.

**5. Por que vale a pena colocar o projeto no GitHub?**
- ✅ Vira portfólio: o recrutador pode clicar e ver os seus testes funcionando
- Porque o Cypress só funciona no GitHub
- Porque o projeto roda mais rápido lá
- Não vale a pena, é só pra empresa grande

Por quê: "sei Cypress" no currículo é uma frase; um link com testes de verdade é uma prova.

---

## Quiz do Módulo 7: Carreira

**1. O que é um teste negativo?**
- ✅ Testar o que acontece quando o usuário faz algo errado, como errar a senha
- Um teste que sempre falha
- Um teste que foi apagado
- Um teste feito sem o Cypress

Por quê: o sistema tem que funcionar no caminho feliz e também avisar direito quando algo dá errado.

**2. Como escrever o Cypress no currículo do jeito certo?**
- ✅ "Automatizei testes E2E de login, carrinho e compra com Cypress" + o link do GitHub
- "Sei Cypress"
- "Cypress: avançado"
- Não colocar, porque é só um curso

Por quê: mostre o que você fez, não só o nome da ferramenta.

**3. Numa entrevista te perguntam: "o que é uma asserção?". Qual a melhor resposta?**
- ✅ É a conferência do teste. No Cypress é o should, que confere se aconteceu o que deveria
- É o nome do arquivo de teste
- É o comando que abre o site
- É quando o teste falha

Por quê: resposta curta, certa e com um exemplo do que você usou.

**4. QA e programador são...**
- ✅ Do mesmo time: os dois querem que o sistema fique bom
- Rivais: o QA existe pra achar erro do programador
- A mesma pessoa
- Áreas que não conversam

Por quê: o QA ajuda o time a entregar com qualidade. Achar um bug antes do cliente é uma vitória de todo mundo.

**5. Qual é a melhor forma de continuar evoluindo depois do curso?**
- ✅ Praticar em outros sites de treino e subir cada projeto novo no GitHub
- Assistir o curso de novo sem escrever código
- Decorar todos os comandos do Cypress
- Esperar uma vaga aparecer

Por quê: cada teste que você escreve te deixa melhor, e o GitHub vai virando o seu portfólio.

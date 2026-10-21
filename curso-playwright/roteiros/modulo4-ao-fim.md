# Roteiros · Aulas 17 a 53 (para aprovação)

Regras que valem para todas as aulas abaixo:
- **Vídeo real:** sempre que a narração diz "olha ele clicando / digitando / rodando", a tela mostra um **vídeo real** do navegador (gravado pela fábrica). Print só para explicar de onde vem um seletor.
- **Teste rodando:** quando um teste roda, aparece o VS Code com o terminal embaixo. Se for com o navegador aparecendo, a janela real abre por cima, faz o teste e fecha, e o resultado aparece no terminal.
- **Linha nova:** toda linha nova é traduzida pedaço por pedaço (estilo da aula 15). O código aparece sempre inteiro e só a linha nova é digitada.
- **Validação:** todo código é validado no Actions antes de virar vídeo.
- Sem "Fala, pessoal", sem legenda queimada e com o selo da colinha quando ela é citada.

---

# Módulo 4 · Locators

## Aula 17: Como o Playwright acha os elementos
1. Até agora você achou coisas na tela de três jeitos: pelo texto cinza do campo, pela função e pelo texto. Hoje você vê o mapa completo. [título]
2. Todo comando que acha um elemento começa com get by, que quer dizer: ache pelo. O que muda é o que vem depois. [tradução: getBy → ache pelo]
3. get by role: ache pela função. Botão, link, campo, título. É o preferido do Playwright, porque é assim que uma pessoa enxerga a tela. [cards]
4. get by text: ache pelo texto que aparece. get by placeholder: pelo texto cinza de dentro do campo. E get by label: pela etiqueta escrita do lado do campo. [cards]
5. E get by test id: ache por uma etiqueta que o próprio desenvolvedor deixou no código, só pra teste. [cards]
6. Mas de onde vem tudo isso? Do código da página. Clica com o botão direito no campo Username e escolhe Inspecionar. [vídeo real: botão direito › Inspecionar]
7. Olha o que aparece: input, placeholder igual Username, e data-test igual username. [DevTools com a linha destacada]
8. Esse placeholder é o que o get by placeholder usa. E esse data-test é a tal etiqueta de teste. [tradução em cima do HTML]
9. Então o mesmo campo pode ser achado de mais de um jeito. [editor: duas linhas, placeholder e data-test, achando o mesmo campo]
10. Qual usar? A ordem que o próprio Playwright recomenda: primeiro get by role. Depois label, placeholder ou texto. E o test id quando nada disso serve. [ranking 1-2-3]
11. Essa ordem está na sua colinha, pra você não precisar decorar. [selo colinha]
12. Na próxima aula: por que alguns seletores quebram o teste sem o site ter quebrado. [passo] / Te vejo lá! [endcard]

## Aula 18: Bons e maus seletores - por que um teste quebra
1. Um teste que quebra sem o site ter quebrado é o pior tipo de teste. E quase sempre a culpa é do seletor. [título]
2. Olha esse seletor, que muita gente copia do navegador: um caminho enorme, com div, div, form, div, input. [editor com o seletor ruim]
3. Traduzindo: dentro da div, dentro de outra div, dentro do formulário, o primeiro campo. Ele descreve o caminho até o campo, não o campo. [tradução]
4. Se o desenvolvedor colocar uma div a mais, esse caminho deixa de existir e o teste quebra, mesmo com o login funcionando perfeitamente. [animação: caminho se partindo]
5. Outro mau exemplo: achar pela classe de estilo, tipo ponto btn underline action. Classe serve pra deixar bonito, e muda quando alguém muda o visual. [compare]
6. Agora os bons: get by placeholder Username, get by role button chamado Login. Eles descrevem o que a pessoa vê na tela. [editor]
7. A regra é simples: se a pessoa usando o site não enxerga, o seu teste também não deveria depender disso. [bigtext]
8. E o get by test id? É ótimo quando existe, porque a etiqueta de teste foi feita só pra isso, e ninguém muda sem querer. [cards]
9. Mais um cuidado: o seletor precisa achar um elemento só. Se na página de produtos você pedir get by role button sem nome, ele acha um monte de botões, e o Playwright reclama. [vídeo real: VS Code + terminal com o erro]
10. Esse erro se chama strict mode violation: modo rigoroso, achou mais de um. A solução é ser mais específico, colocando o nome do botão, por exemplo. [tradução do erro]
11. Resumindo: o que ajuda e o que atrapalha. [compare: AJUDA × ATRAPALHA]
12. Na próxima aula, o Playwright escreve o código pra você. [passo] / Te vejo lá! [endcard]

## Aula 19: Codegen - o Playwright escreve o código pra você
1. E se o Playwright escrevesse o código pra você? Ele escreve. [título]
2. No terminal do VS Code, digita: npx playwright codegen, espaço, e o endereço do saucedemo. [VS Code + terminal]
3. Abrem duas janelas: o navegador, e o Playwright Inspector, que vai anotando tudo o que você faz. [codegen]
4. Agora é só usar o site. Olha: eu clico no Username e digito standard user. A linha de código aparece sozinha. [codegen animado: digitação e código nascendo]
5. Senha, clique no Login. Cada coisa que você faz vira uma linha. [codegen animado]
6. Repara nos seletores que ele escolheu. Ele achou aquela etiqueta data-test que a gente viu na aula 17. [destaque nas linhas]
7. Na barra de cima tem botões pra criar conferências: conferir se algo está visível, ou se o texto está certo. Clica em um e depois no título Products. Pronto, apareceu um expect. [codegen animado]
8. Quando terminar, copia o código e cola no seu arquivo. [editor]
9. Mas atenção: o codegen é um ponto de partida, não o teste pronto. Ele não sabe o que você quer conferir, e às vezes escolhe um seletor ruim. Sempre revisa. [cards]
10. Use pra descobrir seletores e pra começar rápido. Depois, arruma com o que você aprendeu. [bigtext]
11. Na próxima aula: testando um seletor antes de usar. [passo] / Te vejo lá! [endcard]

## Aula 20: Inspector - testando um seletor antes de usar
1. Às vezes você não sabe se um seletor vai funcionar. Dá pra testar antes de rodar o teste. [título]
2. No codegen, clica no botão Pick locator, que quer dizer escolher seletor. [codegen: botão Pick locator]
3. Passa o mouse em cima de qualquer coisa da página: ele mostra o seletor que usaria. [codegen pick animado, mouse passando]
4. E dá pra fazer o contrário: escreve um seletor na caixinha, e ele pinta na página o que encontrou. [codegen pick: digitando o seletor]
5. Se pintou um elemento só, está perfeito. Se pintou vários, o seletor está vago. Se não pintou nada, ele está errado. [cards: 1 ✓ · vários ⚠ · nenhum ✗]
6. Testa o seletor antes, e evita rodar o teste dez vezes pra descobrir. [bigtext]
7. Na próxima aula: por que no Playwright você quase nunca precisa mandar o teste esperar. [passo] / Te vejo lá! [endcard]

## Aula 21: Espera automática - por que não precisa de sleep
1. Em muitas ferramentas antigas, você mandava o teste esperar: espera três segundos, depois clica. No Playwright, quase nunca. [título]
2. Isso se chama auto-wait: espera automática. [tradução]
3. Antes de clicar, o Playwright confere sozinho: o botão existe? Está visível? Parou de se mexer? Está habilitado? Só aí ele clica. [cards checklist]
4. E o expect também espera. Ele fica tentando de novo, por até cinco segundos, até dar certo. [cards]
5. Pra ver isso, vamos usar um usuário especial do saucedemo, o performance glitch user. Ele é lento de propósito. [tela]
6. Cria um teste novo com esse usuário. É igual ao primeiro, só muda o nome do usuário. [editor: só a linha que muda é digitada]
7. Roda com o navegador aparecendo e olha: o login demora... e o teste espera sozinho, sem você escrever nada. [vídeo real com o performance_glitch_user]
8. E se o sistema demorar mais que cinco segundos? Aí dá pra aumentar o tempo só nessa conferência, com timeout. [editor]
9. Traduzindo: timeout dez mil. São milissegundos: espere até dez segundos. [tradução]
10. O que não fazer: page ponto wait for timeout três mil. Isso para o teste por três segundos sempre, mesmo quando o site já carregou. Deixa tudo lento, e ainda pode falhar se um dia demorar quatro. [compare: ERRADO × CERTO]
11. A regra: confie na espera automática. Só aumente o timeout quando o sistema for lento de verdade. [bigtext]
12. Fechamos os locators! No próximo módulo, a gente organiza os testes. [passo] / Te vejo lá! [endcard]

---

# Módulo 5 · Organização

## Aula 22: describe e beforeEach
1. O seu arquivo vai crescer. Hoje você aprende a deixar ele organizado. [título]
2. Vamos criar um segundo teste. O saucedemo tem um usuário que não consegue entrar: o locked out user, usuário bloqueado. [vídeo real: login com locked_out_user e a mensagem de erro]
3. Escreve o teste novo embaixo do primeiro. Ele preenche o usuário bloqueado e espera ver a mensagem locked out. [editor: só o teste novo digitado]
4. Repara: a linha do goto se repete nos dois testes. [editor: as duas linhas destacadas]
5. Quando algo se repete antes de todo teste, existe o before each. Before each: antes de cada. [tradução]
6. Coloca o goto lá dentro, e apaga dos testes. [editor]
7. Agora o describe. Describe é descrever: ele junta testes do mesmo assunto numa caixa com nome. [tradução]
8. Tudo que está dentro desse describe é sobre login. [editor com o bloco destacado]
9. Lendo em português: um grupo chamado Login. Antes de cada teste, abra o site. Teste um: entra. Teste dois: mostra erro pro bloqueado. [cards]
10. Roda: os dois passam. E no relatório eles aparecem juntos, debaixo de Login. [VS Code + terminal, depois relatório]
11. Na próxima aula: o arquivo de configuração. [passo] / Te vejo lá! [endcard]

## Aula 23: playwright.config - baseURL e data-test
1. Hoje a gente mexe no arquivo de configuração. Parece assustador, mas são só duas linhas. [título]
2. Abre o playwright ponto config ponto js e procura o use. Use quer dizer: use isso em todos os testes. [editor + tradução]
3. Tira o comentário da baseURL e coloca o endereço do saucedemo. Base URL: o endereço base. [editor digitando]
4. Agora, no teste, o goto fica só com uma barra. O Playwright junta essa barra com o endereço base. [editor + tradução]
5. A vantagem: se um dia o site mudar de endereço, você troca num lugar só. [cards]
6. Segunda linha: test id attribute igual data-test. Lembra do data-test que a gente viu no Inspecionar? [DevTools]
7. Por padrão, o get by test id procura data-testid. O saucedemo usa data-test. Essa linha avisa o Playwright. [compare]
8. Agora dá pra trocar os seletores do login por get by test id: username, password e login-button. [editor: troca linha a linha]
9. Traduzindo: ache pela etiqueta de teste chamada username. [tradução]
10. Roda pra confirmar que tudo continua passando. [VS Code + terminal: 2 passed]
11. Na próxima aula: tirando o usuário e a senha do código. [passo] / Te vejo lá! [endcard]

## Aula 24: Variáveis de ambiente - tirando usuário e senha do código
1. Usuário e senha escritos no código são um problema: quando o projeto for pro GitHub, todo mundo vê. [título]
2. A solução é um arquivo chamado ponto env, que guarda essas informações fora do código. [cards]
3. Primeiro, instala o pacote que lê esse arquivo. No terminal: npm install traço D dotenv. [VS Code + terminal]
4. Na pasta do projeto, cria o arquivo ponto env. Dentro: SAUCE underline USER igual standard user, e SAUCE underline PASSWORD igual secret sauce. [menu + editor]
5. No config, tira o comentário daquelas três linhas do dotenv. Elas mandam ler o arquivo ponto env. [editor]
6. No teste, troca o texto por process ponto env ponto SAUCE underline USER. [editor]
7. Traduzindo: process ponto env, as variáveis do ambiente. SAUCE underline USER, a variável com esse nome. [tradução]
8. Agora o mais importante: o ponto env não pode ir pro GitHub. Abre o ponto gitignore e escreve ponto env no final. [editor]
9. E pra quem baixar o projeto saber o que preencher, cria um ponto env ponto example só com os nomes. [editor]
10. Roda pra confirmar: continua passando. [VS Code + terminal]
11. Na próxima aula: rodando só o que importa. [passo] / Te vejo lá! [endcard]

## Aula 25: Rodando só o que importa - only, skip, arquivo e nome
1. Quando você tiver dezenas de testes, não vai querer rodar todos toda hora. [título]
2. Pra rodar um arquivo só, coloca o nome dele: npx playwright test login ponto spec ponto js. [VS Code + terminal]
3. Pra rodar pelo nome do teste: traço g e um pedaço do nome, tipo bloqueado. O g vem de grep, que quer dizer procurar. [VS Code + terminal + tradução]
4. Dentro do código, test ponto only: roda somente esse teste. Only quer dizer somente. [editor + tradução]
5. Cuidado: esquecer um only é um erro clássico. Os outros testes param de rodar e ninguém percebe. Por isso o config já vem com forbid only, que trava isso no GitHub. [cards]
6. E test ponto skip: pula esse teste. Skip quer dizer pular. No resultado, ele aparece como skipped. [editor + terminal]
7. E você já conhece o traço traço project igual chromium, pra rodar num navegador só. [cards]
8. Resumo de tudo numa tabela. [tradução em tabela]
9. Fechamos a organização. No próximo módulo: o que fazer quando o teste falha. [passo] / Te vejo lá! [endcard]

---

# Módulo 6 · Debug

## Aula 26: Lendo o erro
1. O teste falhou. Calma: o erro do Playwright é um dos mais fáceis de ler. [título]
2. Vamos quebrar de propósito: troca o texto Products por Produtos. [editor]
3. Roda. Falhou. [VS Code + terminal: 1 failed]
4. Vamos ler de cima pra baixo. Primeiro: qual teste falhou, e em qual arquivo e linha. [terminal com destaque]
5. Depois: Expected, o que você esperava, e Received, o que ele encontrou. [tradução]
6. Depois, o pedaço do seu código, com uma setinha apontando a linha exata. [terminal com destaque]
7. E o call log, que mostra tudo o que ele tentou. Repara: ele ficou tentando por cinco segundos antes de desistir. [terminal com destaque]
8. Os três erros que você mais vai ver: timeout, que é não achou; strict mode, que é achou mais de um; e expected received, que é achou, mas está diferente. [cards]
9. Volta pra Products e roda: passou. [VS Code + terminal]
10. Na próxima aula: um jeito muito mais visual de rodar os testes. [passo] / Te vejo lá! [endcard]

## Aula 27: UI Mode
1. Existe um jeito bem mais visual de rodar testes: o UI Mode. [título]
2. No terminal: npx playwright test traço traço ui. [VS Code + terminal]
3. Abre uma janela com todos os seus testes do lado esquerdo. Clica no play. [UI Mode animado]
4. Ele roda e mostra cada passo. Clica num passo, e a tela mostra como a página estava naquele momento. [UI Mode animado]
5. Dá pra voltar no tempo: ver a página antes e depois de cada clique. [UI Mode animado]
6. E tem o olhinho, o modo vigiar: você salva o arquivo e o teste roda de novo sozinho. [UI Mode animado]
7. É o melhor jeito de escrever um teste novo: escreve, salva, e vê na hora. [bigtext]
8. Na próxima aula: o rastro completo de um teste. [passo] / Te vejo lá! [endcard]

## Aula 28: Trace Viewer
1. E quando o teste falha no GitHub, onde você não estava olhando? Pra isso existe o trace. [título]
2. Trace quer dizer rastro: é um arquivo com tudo o que aconteceu no teste. [tradução]
3. Roda com traço traço trace on. [VS Code + terminal]
4. Abre o relatório e clica no trace do teste. [relatório]
5. Em cima, a linha do tempo. Na esquerda, os passos. No meio, a página. E embaixo, o console e a rede. [Trace Viewer animado]
6. No config já vem trace on first retry: quando um teste falha no GitHub e roda de novo, o trace é gravado sozinho. [editor com destaque]
7. Na próxima aula: pausando o teste no meio. [passo] / Te vejo lá! [endcard]

## Aula 29: Modo debug e page.pause
1. Às vezes você quer ver o teste devagar, um passo de cada vez. [título]
2. No terminal: npx playwright test traço traço debug. Ele abre o navegador e para antes do primeiro passo. [VS Code + terminal, depois o Inspector]
3. No Inspector, o botão step over executa um passo por vez. Olha: um clique, para; outro clique, para. [Inspector animado, passo a passo]
4. Outra forma: page ponto pause no meio do teste. Pause é pausar: o teste para exatamente ali. [editor + tradução]
5. Lembra de tirar o pause depois, senão o teste fica parado esperando você. [cards]
6. Na próxima aula: print e vídeo automático quando o teste falha. [passo] / Te vejo lá! [endcard]

## Aula 30: Print e vídeo quando o teste falha
1. E se o próprio teste tirasse um print e gravasse um vídeo quando falha? Ele faz isso. [título]
2. No config, dentro do use, adiciona duas linhas: screenshot only on failure, e video retain on failure. [editor digitando só as duas]
3. Traduzindo: screenshot, print, só quando falhar. Video, guardar o vídeo só quando falhar. [tradução]
4. Quebra o teste de novo e roda. [VS Code + terminal: failed]
5. Abre o relatório: lá está o print do momento do erro e o vídeo do teste inteiro. [relatório com print e vídeo real]
6. E por que só quando falha? Porque gravar sempre deixa tudo mais lento e enche o computador de arquivo. [cards]
7. Desfaz o erro e fechamos o módulo de debug. [passo] / Te vejo lá! [endcard]

---

# Módulo 7 · Testes reais

## Aula 31: Vários usuários - testes com dados
1. O saucedemo tem vários usuários: standard, problem, performance glitch e visual. Copiar o mesmo teste quatro vezes? Não. [tela com a lista de usuários]
2. Cria o arquivo usuarios ponto spec ponto js. Primeira coisa: uma lista. const usuarios igual, abre colchetes, e os quatro nomes. [editor]
3. Traduzindo: const, guarde com o nome usuarios. Colchetes, uma lista. [tradução]
4. Agora: for, abre parênteses, const usuario of usuarios. Para cada usuário dessa lista. [tradução]
5. Dentro, o teste. Repara no nome com crase e cifrão: o nome do usuário entra no nome do teste. [editor + tradução]
6. E o timeout de dez segundos, por causa daquele usuário lento que você já conhece. [editor com destaque]
7. Roda: quatro testes, um pra cada usuário. [VS Code + terminal: 4 passed]
8. Quer testar mais um usuário? Só coloca o nome na lista. [cards]
9. Na próxima aula: três navegadores ao mesmo tempo. [passo] / Te vejo lá! [endcard]

## Aula 32: 3 navegadores e testes em paralelo
1. Lembra das seis execuções com dois testes? Hoje você entende de onde vem. [título]
2. Sem o traço traço project, o Playwright roda em três navegadores: Chromium, Firefox e WebKit, que é o motor do Safari. [cards]
3. Eles estão no config, nos projects. [editor com destaque]
4. Roda tudo e repara: using quatro workers. Workers são trabalhadores: quantos testes rodam ao mesmo tempo. [VS Code + terminal + tradução]
5. Paralelo quer dizer vários testes ao mesmo tempo, em vez de um por vez. Por isso cada teste precisa ser independente: nenhum pode depender de outro. [compare: um por vez × ao mesmo tempo]
6. No config, o fully parallel true liga isso. E workers um no GitHub, porque a máquina de lá é pequena. [editor com destaque]
7. Na próxima aula: testando como se fosse um celular. [passo] / Te vejo lá! [endcard]

## Aula 33: Celular - emulando dispositivos
1. Muita gente acessa os sites pelo celular. O Playwright testa isso sem você ter um celular. [título]
2. Ele tem uma lista de aparelhos prontos, com tamanho de tela, toque, tudo. [cards]
3. No config, cria um project novo chamado celular, usando o Pixel 7. [editor digitando só o bloco novo]
4. Roda com project igual celular e com o navegador aparecendo: olha, o site abre no tamanho de celular. [vídeo real em tela de celular]
5. E o mesmo teste funciona, sem mudar nada no código. [VS Code + terminal: passed]
6. Fechamos os testes reais. Agora: o projeto final! [passo] / Te vejo lá! [endcard]

---

# Módulo 8 · Projeto final

## Aula 34: O carrinho
1. Começa o projeto final: uma compra completa, do login até o obrigado. Hoje, o carrinho. [título]
2. Depois do login, cada produto tem um botão Add to cart. Clica com o botão direito e Inspecionar: data-test igual add-to-cart-sauce-labs-backpack. [vídeo real + DevTools]
3. Cria o compra ponto spec ponto js, com o login no before each, igual você já sabe. [editor]
4. No teste: get by test id add-to-cart-sauce-labs-backpack, ponto click. [editor + tradução]
5. E a conferência: o numerozinho do carrinho mostra um. get by test id shopping-cart-badge, to have text um. [editor + tradução]
6. Roda com o navegador aparecendo: olha ele entrando, clicando em Add to cart, e o carrinho virando um. [vídeo real]
7. Na próxima aula: terminando a compra. [passo] / Te vejo lá! [endcard]

## Aula 35: Finalizando a compra
1. Hoje o robô compra a mochila de verdade. [título]
2. Abre o carrinho: get by test id shopping-cart-link, click. Depois o botão checkout. [editor + tradução]
3. Na tela de dados, três campos: nome, sobrenome e CEP. Os data-test são firstName, lastName e postalCode. [vídeo real + DevTools]
4. Preenche os três e clica em continue. [editor: linha a linha]
5. Na última tela, clica em finish. [editor]
6. E a conferência final: complete-header, to have text, Thank you for your order. [editor + tradução]
7. Roda com o navegador aparecendo e olha a compra inteira acontecendo sozinha. [vídeo real da compra completa]
8. Na próxima aula: uma coisa que você talvez já tenha percebido. [passo] / Te vejo lá! [endcard]

## Aula 36: Percebeu que estamos copiando código?
1. Olha o login no login ponto spec, e olha o login no compra ponto spec. É o mesmo código, duas vezes. [editor lado a lado]
2. Agora imagina dez arquivos de teste. Se o botão de login mudar, você arruma em dez lugares. [animação: 10 arquivos se acendendo]
3. A solução é guardar o jeito de usar cada página num lugar só. Isso se chama Page Object. [bigtext]
4. Pensa num controle remoto: você aperta ligar e não precisa saber como a TV funciona por dentro. [cards]
5. O teste vai dizer só login ponto entrar. Os detalhes de como entrar ficam guardados no Page Object. [compare: antes × depois]
6. Na próxima aula, a gente cria o primeiro. [passo] / Te vejo lá! [endcard]

## Aula 37: Page Object, versão simples
1. Cria uma pasta nova chamada pages, e dentro o arquivo LoginPage ponto js. [menu]
2. Primeira linha: export class LoginPage. Class é um molde. Export deixa outros arquivos usarem. [editor + tradução]
3. Dentro, o constructor: o que fica pronto quando você cria um LoginPage. Ele recebe o page e guarda os campos: usuário, senha, botão e erro. [editor + tradução]
4. O this quer dizer: deste objeto. this ponto usuario: o campo usuário deste LoginPage. [tradução]
5. Agora a ação: async entrar, recebendo usuário e senha. Preenche, preenche, clica. [editor]
6. No teste: import LoginPage, depois const login igual new LoginPage page. New quer dizer: crie um novo. [editor + tradução]
7. E o login vira uma linha só: await login ponto entrar. [editor]
8. Lendo em português: crie um LoginPage e entre com esse usuário e essa senha. [bigtext]
9. Faz a mesma coisa pra página de produtos e pro checkout. O código completo de cada um aparece aqui. [editor com os dois arquivos]
10. Roda tudo: continua passando, e agora o teste lê como uma história. [VS Code + terminal]
11. Na próxima aula: um relatório que se lê como roteiro. [passo] / Te vejo lá! [endcard]

## Aula 38: test.step - um relatório que se lê como roteiro
1. Quando um teste longo falha, você quer saber em qual parte. [título]
2. test ponto step: um passo com nome. Step quer dizer passo. [tradução]
3. Divide a compra em quatro passos: adiciona a mochila, abre o carrinho, preenche os dados, finaliza a compra. [editor]
4. Roda e abre o relatório: os passos aparecem com os nomes que você deu, em português. [relatório]
5. E se falhar, ele mostra exatamente em qual passo. [relatório com um passo vermelho]
6. Na próxima aula: fazendo login uma vez só. [passo] / Te vejo lá! [endcard]

## Aula 39: Indo além - login uma vez só com storageState
1. Todo teste faz login de novo. Em centenas de testes, isso é muito tempo perdido. [título]
2. A ideia: fazer o login uma vez, e guardar o navegador já logado num arquivo. [cards]
3. Cria o auth ponto setup ponto js. Ele faz o login e, no fim, storage state, guardando tudo em playwright barra ponto auth. [editor + tradução: storageState → guarde o estado]
4. No config, um project chamado setup, que roda primeiro. Os outros dependem dele: dependencies. [editor + tradução]
5. No teste da compra: test ponto use storage state, apontando pro arquivo. O teste já começa logado. [editor]
6. E esse arquivo já está no gitignore, porque ele guarda o seu login. [editor com destaque]
7. Roda: o setup aparece primeiro, e a compra começa direto na página de produtos. [VS Code + terminal + vídeo real]
8. Projeto final pronto! Agora ele vai pro GitHub. [passo] / Te vejo lá! [endcard]

---

# Módulo 9 · CI

## Aula 40: Subindo o projeto pro GitHub
1. Seu projeto merece estar no GitHub: é a vitrine de quem trabalha com tecnologia. [título]
2. Cria uma conta no github ponto com, se ainda não tiver, e clica em New repository. Dá o nome e cria. [tela GitHub]
3. No terminal do VS Code, um comando por vez: git init, git add ponto, git commit traço m e uma mensagem. [VS Code + terminal + tradução de cada comando]
4. Depois: git branch traço M main, git remote add origin e o endereço do seu repositório, e git push. [VS Code + terminal]
5. Atualiza a página do GitHub: seu projeto está lá. [tela GitHub]
6. E repara: o ponto env não subiu. O gitignore fez o trabalho dele. [tela com destaque]
7. Na próxima aula: os testes rodando sozinhos no GitHub. [passo] / Te vejo lá! [endcard]

## Aula 41: GitHub Actions - os testes rodando sozinhos
1. E se os testes rodassem sozinhos toda vez que você manda código novo? É isso que o GitHub Actions faz. [título]
2. O Playwright já criou esse arquivo lá no começo: ponto github, workflows, playwright ponto yml. [editor]
3. Lendo em português: quando alguém mandar código, use uma máquina Ubuntu, instale tudo e rode os testes. [tradução em tabela]
4. Só falta uma coisa: o ponto env não está no GitHub, então os testes não sabem o usuário e a senha. [cards]
5. No GitHub: Settings, Secrets and variables, Actions, New repository secret. Cria o SAUCE underline USER e o SAUCE underline PASSWORD. [tela GitHub, passo a passo]
6. No yml, no passo de rodar os testes, um env que lê esses segredos. [editor digitando só as linhas novas]
7. Manda pro GitHub e abre a aba Actions: olha os testes rodando lá. [gh_actions animado]
8. Verde: passou. E o relatório fica guardado pra baixar. [gh_actions]
9. Fechamos o projeto! Tem bônus: testes de API. [passo] / Te vejo lá! [endcard]

---

# Módulo 10 · Bônus API

## Aula 42: O que é uma API, explicado do zero
1. Quase todo site conversa com um servidor por trás. Essa conversa é a API. [título]
2. Pensa num restaurante: você não entra na cozinha, você pede ao garçom. A API é o garçom. [cards: você · garçom · cozinha]
3. Os pedidos têm tipos: GET, buscar. POST, criar. DELETE, apagar. [tradução]
4. E a resposta vem com um número, o status: duzentos é deu certo, duzentos e um é criado, quatrocentos e quatro é não encontrado. [cards]
5. Vamos usar uma API de treino gratuita: jsonplaceholder. Abre no navegador o barra posts barra um. [tela real]
6. Esse texto com chaves é JSON: o jeito que as APIs mandam dados. [tradução em cima do JSON]
7. Na próxima aula: o seu primeiro teste de API. [passo] / Te vejo lá! [endcard]

## Aula 43: Seu primeiro teste de API
1. Teste de API não abre navegador nenhum. É muito mais rápido. [título]
2. Cria o api ponto spec ponto js. No lugar do page, agora você pede o request. [editor + tradução: request → pedido]
3. await request ponto get e o endereço: busca o post número um. [editor + tradução]
4. expect resposta ponto status, to be duzentos: eu espero que o status seja duzentos. [tradução]
5. Depois, resposta ponto json, pra ler os dados. E o expect: o id é um. [editor + tradução]
6. Roda: passou, em milissegundos. [VS Code + terminal]
7. Na próxima aula: criando e apagando pela API. [passo] / Te vejo lá! [endcard]

## Aula 44: Criando, buscando e apagando dados pela API
1. Agora o robô cria e apaga dados. [título]
2. request ponto post, com um data: título, texto e userId. É o pedido de criar. [editor + tradução]
3. A conferência: status duzentos e um, criado. E o título que voltou é o mesmo que você mandou. [editor + tradução]
4. request ponto delete: apagar. Status duzentos. [editor + tradução]
5. Roda os três: passaram. [VS Code + terminal]
6. Um aviso: essa API de treino finge que criou e apagou, mas não guarda de verdade. Num sistema real, ela guardaria. [cards]
7. Fechamos o bônus! Agora: desafios pra você praticar. [passo] / Te vejo lá! [endcard]

---

# Módulo 11 · Desafios
Formato de todos: desafio → "pausa o vídeo e tenta" (contagem de 5 segundos na tela) → dica → solução digitada linha a linha com tradução → vídeo real rodando.

## Aula 45: Desafio 1 - senha errada
1. Primeiro desafio: o que acontece quando alguém erra a senha? [título]
2. O teste: usuário certo, senha errada, e conferir a mensagem de erro. Pausa o vídeo e tenta fazer sozinho. [cards + contagem]
3. Dica: a mensagem fica no data-test error, e contém do not match. [vídeo real mostrando o erro]
4. Solução: preenche, preenche, clica, e expect error to contain text do not match. [editor + tradução]
5. Roda e olha: o erro aparece e o teste passa. [vídeo real + terminal] / Te vejo no próximo desafio! [endcard]

## Aula 46: Desafio 2 - campos vazios
1. Desafio dois: e se a pessoa clicar em Login sem preencher nada? [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: a mensagem é Username is required. [vídeo real]
4. Solução: só o clique e o expect. Repara: um bom teste também testa o que dá errado. [editor + tradução]
5. Roda: passou. [vídeo real + terminal] / Te vejo no próximo! [endcard]

## Aula 47: Desafio 3 - remover do carrinho
1. Desafio três: adicionar a mochila e depois remover. [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: depois de adicionar, o botão vira Remove, com data-test remove-sauce-labs-backpack. E quando o carrinho está vazio, o numerozinho some. [vídeo real]
4. Solução: e pra conferir que sumiu, to have count zero: eu espero que tenha zero desses. [editor + tradução]
5. Roda. [vídeo real + terminal] / Te vejo no próximo! [endcard]

## Aula 48: Desafio 4 - ordenar por preço
1. Desafio quatro: ordenar do menor pro maior preço. [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: a caixa de ordenar é um select. Pra escolher uma opção, existe o select option. A opção do menor preço se chama lohi, de low to high. [vídeo real + tradução]
4. Solução: e a conferência: o primeiro preço da lista é sete e noventa e nove. Ponto first: o primeiro. [editor + tradução]
5. Roda. [vídeo real + terminal] / Te vejo no próximo! [endcard]

## Aula 49: Desafio 5 - logout
1. Desafio cinco: sair do sistema. [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: o menu é aquele botão de três risquinhos, com nome Open Menu. Lá dentro tem o Logout. [vídeo real]
4. Solução: clica no menu, clica no logout, e confere que o botão de Login voltou. [editor + tradução]
5. Roda. [vídeo real + terminal] / Te vejo no desafio final! [endcard]

## Aula 50: Desafio final - compra com dois produtos
1. Desafio final: comprar dois produtos e conferir o total. [título]
2. Pausa e tenta. Esse é maior, sem pressa. [cards + contagem]
3. Dica: a mochila e a lanterna da bicicleta, bike light. O total com imposto fica no data-test total-label: quarenta e três e dezoito. [vídeo real]
4. Solução, passo a passo. [editor: linha a linha com tradução das novas]
5. Roda e olha a compra inteira. [vídeo real + terminal]
6. Se você fez esse sozinho, você já sabe escrever testes de verdade. [bigtext] / Te vejo na última parte! [endcard]

---

# Módulo 12 · Carreira

## Aula 51: Veio do Cypress? O mapa Cypress para Playwright
1. Se você já usou Cypress, a boa notícia: quase tudo tem um equivalente direto. [título]
2. cy ponto visit vira page ponto goto. cy ponto get com type vira fill. cy ponto contains vira get by text. should be visible vira expect to be visible. [tabela de tradução]
3. A maior diferença: no Playwright você escreve await em cada passo. [compare]
4. E o que o Playwright faz de diferente: três navegadores, várias abas, paralelo de graça e API no mesmo teste. [cards]
5. As duas são ótimas. Saber as duas te deixa muito mais forte no mercado. [bigtext]
6. Te vejo na próxima! [endcard]

## Aula 52: O seu projeto no currículo e na entrevista
1. Agora você tem um projeto de automação de verdade. Vamos colocar isso no seu currículo. [título]
2. No currículo, escreve o que você fez, não só a ferramenta: automação de testes end-to-end com Playwright e JavaScript, Page Object, testes de API e execução no GitHub Actions. [cards]
3. Perguntas que caem em entrevista e que você já sabe responder: o que é auto-wait? [cards: pergunta → resposta curta]
4. Por que preferir get by role? O que é Page Object? O que é um teste flaky, que às vezes passa e às vezes falha, e como evitar? [cards]
5. E a dica de ouro: fala do seu projeto mostrando o GitHub. Código funcionando convence mais que qualquer certificado. [bigtext]
6. Te vejo na última aula! [endcard]

## Aula 53: Seu projeto pronto pro portfólio e a colinha completa
1. Última aula. Vamos deixar o seu projeto bonito pra quem visitar. [título]
2. Cria um README ponto md: o que o projeto testa, como rodar, e as tecnologias. [editor]
3. Coloca o selinho do GitHub Actions: ele mostra pra todo mundo que os seus testes estão passando. [tela GitHub com o selo]
4. E a sua colinha: ela tem tudo o que você aprendeu, do primeiro comando ao Page Object. Deixa ela aberta enquanto você pratica. [colinha, página por página]
5. Você começou sem saber nada e terminou com um projeto completo: login, compra, API e tudo rodando sozinho no GitHub. [montagem rápida das aulas]
6. Parabéns! E se o curso te ajudou, deixa a sua avaliação: isso ajuda muito. [bigtext]
7. Até a próxima! [endcard]

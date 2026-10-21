# Roteiros · Aulas 17 a 57 (revisados com a revisão completa)

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
3. get by role: ache pela função. Botão, link, campo, título. É o tipo de seletor que o Playwright recomenda, porque ele parte do que a pessoa usa na tela. [cards]
4. get by text: ache pelo texto que aparece. get by placeholder: pelo texto cinza de dentro do campo. E get by label: pela etiqueta escrita do lado do campo. [cards]
5. E get by test id: ache por uma etiqueta que o próprio desenvolvedor deixou no código, só pra teste. [cards]
6. Mas de onde vem tudo isso? Do código da página. Clica com o botão direito no campo Username e escolhe Inspecionar. [vídeo real: botão direito › Inspecionar]
7. Olha o que aparece: input, placeholder igual Username, e data-test igual username. [DevTools com a linha destacada]
8. Esse placeholder é o que o get by placeholder usa. E esse data-test é a tal etiqueta de teste. [tradução em cima do HTML]
9. Então o mesmo campo pode ser achado de mais de um jeito. [editor: duas linhas, placeholder e data-test, achando o mesmo campo]
10. Qual usar? Prefira os seletores que representam o que a pessoa vê e usa: função, etiqueta, placeholder e texto. E quando o sistema tem uma etiqueta de teste estável, o test id também é uma boa opção. [cards]
11. Isso está na sua colinha, pra você não precisar decorar. [selo colinha]
12. Na próxima aula: por que alguns seletores quebram o teste sem o site ter quebrado. [passo] / Te vejo lá! [endcard]

## Aula 18: Bons e maus seletores - por que um teste quebra
1. Um teste que quebra sem o site ter quebrado é o pior tipo de teste. E muitas vezes a causa é um seletor frágil. [título]
2. Olha esse seletor, que muita gente copia do navegador: um caminho enorme, com div, div, form, div, input. [editor com o seletor ruim]
3. Traduzindo: dentro da div, dentro de outra div, dentro do formulário, o primeiro campo. Ele descreve o caminho até o campo, não o campo. [tradução]
4. Se o desenvolvedor colocar uma div a mais, esse caminho deixa de existir e o teste quebra, mesmo com o login funcionando perfeitamente. [animação: caminho se partindo]
5. Outro exemplo frágil: achar pela classe de estilo, tipo ponto btn underline action. Classe de visual costuma mudar quando alguém mexe na aparência do site. [compare]
6. Agora os bons: get by placeholder Username, get by role button chamado Login. Eles descrevem o que a pessoa vê na tela. [editor]
7. Regra prática: prefira seletores que representam o que a pessoa usa na tela. Quando isso não for suficiente, use uma etiqueta de teste estável, feita pra automação. [bigtext]
8. É por isso que o get by test id é bom quando existe: a etiqueta foi criada só pra teste, e é bem mais difícil alguém mudar sem querer. [cards]
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
6. Repara no seletor que ele escolheu. O codegen tenta achar um jeito bom e único de identificar cada elemento. Nem sempre é o mesmo que você escolheria, por isso a gente revisa o código gerado. [destaque nas linhas]
7. Na barra de cima tem botões pra criar conferências: conferir se algo está visível, ou se o texto está certo. Clica em um e depois no título Products. Pronto, apareceu um expect. [codegen animado]
8. Quando terminar, copia o código e cola no seu arquivo. [editor]
9. Mas atenção: o codegen é um ponto de partida, não o teste pronto. Ele não sabe o que você quer conferir, e às vezes escolhe um seletor ruim. Sempre revisa. [cards]
10. Use pra descobrir seletores e pra começar rápido. Depois, arruma com o que você aprendeu. [bigtext]
11. Na próxima aula: testando um seletor antes de usar. [passo] / Te vejo lá! [endcard]

## Aula 20: Pick Locator - testando um seletor antes de usar
1. Às vezes você não sabe se um seletor vai funcionar. Dá pra testar antes de rodar o teste. [título]
2. No codegen, clica no botão Pick locator, que quer dizer escolher seletor. [codegen: botão Pick locator]
3. Passa o mouse em cima de qualquer coisa da página: ele mostra o seletor que usaria. [codegen pick animado, mouse passando]
4. E dá pra fazer o contrário: escreve um seletor na caixinha, e ele pinta na página o que encontrou. [codegen pick: digitando o seletor]
5. Se pintou um elemento só, é um bom primeiro sinal: aí confere se o seletor também é claro e resistente a mudanças. Se pintou vários, ele está vago. Se não pintou nada, ele está errado. [cards: 1 ✓ · vários ⚠ · nenhum ✗]
6. Testando o seletor antes, você evita rodar o teste várias vezes pra descobrir. [bigtext]
7. Na próxima aula: por que no Playwright você quase nunca precisa mandar o teste esperar. [passo] / Te vejo lá! [endcard]

## Aula 21: Espera automática - por que não precisa de sleep
1. É comum encontrar testes com espera fixa: espera três segundos, depois clica. No Playwright, na maioria das vezes você não precisa disso. [título]
2. Isso se chama auto-wait: espera automática. [tradução]
3. Antes de clicar, o Playwright confere sozinho se o elemento está pronto pra receber o clique: se está visível, parado, habilitado, e se nada está na frente dele. [cards checklist]
4. E os expects que conferem a página, como o to have URL e o to be visible, também tentam de novo. Por padrão, por até cinco segundos. [cards]
5. Pra ver isso, vamos usar um usuário especial do saucedemo, o performance glitch user. Ele é lento de propósito. [tela]
6. Cria um teste novo com esse usuário. É igual ao primeiro, só muda o nome do usuário. [editor: só a linha que muda é digitada]
7. Só que esse login às vezes passa de cinco segundos. Então, nessa conferência, a gente dá mais tempo: timeout dez mil. [editor: digita só o timeout no expect]
8. Traduzindo: timeout dez mil. São milissegundos: espere até dez segundos, só nessa conferência. Os outros expects continuam com cinco. [tradução]
9. Roda com o navegador aparecendo e olha: o clique em Login acontece, a página demora... e o teste espera sozinho até os produtos aparecerem. [vídeo real com o performance_glitch_user]
10. O que não fazer: page ponto wait for timeout três mil. Isso para o teste por três segundos sempre, mesmo quando o site já carregou. Deixa tudo lento, e ainda pode falhar se um dia demorar quatro. [compare: ERRADO × CERTO]
11. Regra prática: confie na espera automática, e aumente o timeout só no lugar onde o sistema é lento de verdade. [bigtext]
12. Fechamos os locators! No próximo módulo, a gente organiza os testes. [passo] / Te vejo lá! [endcard]

---

# Módulo 5 · Organização

## Aula 22: describe e beforeEach
1. O seu arquivo vai crescer. Hoje você aprende a deixar ele organizado. [título]
2. Vamos criar um segundo teste. O saucedemo tem um usuário que não consegue entrar: o usuário bloqueado, locked underline out underline user. [vídeo real: login com locked_out_user e a mensagem de erro]
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
8. Agora o get by test id também funciona no saucedemo. Vamos trocar os seletores do login só pra você ver esse outro caminho. Os que a gente usou antes continuam certos. [editor: troca linha a linha]
9. Traduzindo: ache pela etiqueta de teste chamada username. [tradução]
10. Roda pra confirmar que tudo continua passando. [VS Code + terminal: 2 passed]
11. Na próxima aula: tirando o usuário e a senha do código. [passo] / Te vejo lá! [endcard]

## Aula 24: Variáveis de ambiente - tirando usuário e senha do código
1. Aqui no saucedemo o usuário e a senha são públicos. Mas em projeto de verdade, senha e chave escrita no código é um problema: quando o projeto for pro GitHub, todo mundo vê. [título]
2. Então a gente vai aprender o jeito usado em projetos reais: um arquivo chamado ponto env, que guarda essas informações fora do código. [cards]
3. Primeiro, instala o pacote que lê esse arquivo. No terminal: npm install traço D dotenv. O traço D marca como ferramenta de desenvolvimento do projeto. [VS Code + terminal]
4. Na pasta do projeto, cria o arquivo ponto env. Dentro: SAUCE underline USER igual standard user, e SAUCE underline PASSWORD igual secret sauce. [menu + editor]
4b. E antes de qualquer outra coisa: abre o ponto gitignore e escreve ponto env no final. Assim esse arquivo nunca vai pro GitHub. [editor]
5. No config, tira o comentário daquelas três linhas do dotenv. Elas mandam ler o arquivo ponto env. [editor]
6. No teste, troca o texto por process ponto env ponto SAUCE underline USER. [editor]
7. Traduzindo: process ponto env, as variáveis do ambiente. SAUCE underline USER, a variável com esse nome. [tradução]
8. E pra quem baixar o projeto saber o que preencher, cria um ponto env ponto example só com os nomes das variáveis, sem os valores. [editor]
10. Roda pra confirmar: continua passando. [VS Code + terminal]
11. Na próxima aula: rodando só o que importa. [passo] / Te vejo lá! [endcard]

## Aula 25: Rodando só o que importa - only, skip, arquivo e nome
1. Quando você tiver dezenas de testes, não vai querer rodar todos toda hora. [título]
2. Pra rodar um arquivo só, coloca o nome dele: npx playwright test login ponto spec ponto js. [VS Code + terminal]
3. Pra rodar pelo nome do teste: traço g e um pedaço do nome, tipo bloqueado. O g vem de grep, que quer dizer procurar: ele filtra os testes por esse pedaço de nome. [VS Code + terminal + tradução]
4. Dentro do código, test ponto only: roda somente esse teste. Only quer dizer somente. [editor + tradução]
5. Cuidado: esquecer um only é um erro clássico. Os outros testes param de rodar e ninguém percebe. Por isso o config já vem com forbid only, que trava isso no GitHub. [cards]
6. E test ponto skip: pula esse teste. Skip quer dizer pular. No resultado, ele aparece como skipped. [editor + terminal]
7. E você já conhece o traço traço project igual chromium, pra rodar num navegador só. [cards]
8. Resumo de tudo numa tabela. [tradução em tabela]
9. Fechamos a organização. No próximo módulo: o que fazer quando o teste falha. [passo] / Te vejo lá! [endcard]

---

# Módulo 6 · Debug

## Aula 26: Lendo o erro
1. O teste falhou. Calma: ler o erro fica muito mais fácil quando você sabe onde olhar. [título]
2. Vamos quebrar de propósito: troca o texto Products por Produtos. [editor]
3. Roda. Falhou. [VS Code + terminal: 1 failed]
4. Vamos ler de cima pra baixo. Primeiro: qual teste falhou, e em qual arquivo e linha. [terminal com destaque]
5. Depois: Expected, o que você esperava, e Received, o que ele encontrou. [tradução]
6. Depois, o pedaço do seu código, com uma setinha apontando a linha exata. [terminal com destaque]
7. E o call log, que mostra tudo o que ele tentou. Repara: ele ficou tentando por cinco segundos antes de desistir. [terminal com destaque]
8. Três coisas que você vai ver bastante: timeout, alguma coisa que o teste esperava não aconteceu dentro do tempo. Strict mode violation, o seletor achou mais de um elemento quando precisava de um só. E Expected e Received, o teste esperava um valor e encontrou outro. [cards]
9. Volta pra Products e roda: passou. [VS Code + terminal]
10. Na próxima aula: um jeito muito mais visual de rodar os testes. [passo] / Te vejo lá! [endcard]

## Aula 27: UI Mode
1. Existe um jeito bem mais visual de rodar testes: o UI Mode. [título]
2. No terminal: npx playwright test traço traço ui. [VS Code + terminal]
3. Abre uma janela com todos os seus testes do lado esquerdo. Clica no play. [UI Mode animado]
4. Ele roda e mostra cada passo. Clica num passo, e a tela mostra como a página estava naquele momento. [UI Mode animado]
5. Dá pra voltar no tempo: ver a página antes e depois de cada clique. [UI Mode animado]
6. E tem o watch, que quer dizer vigiar, aquele ícone de olho: você salva o arquivo e o teste roda de novo sozinho. [UI Mode animado com o nome watch na tela]
7. É um dos jeitos mais confortáveis de escrever um teste novo: escreve, salva, e vê na hora. [bigtext]
8. Na próxima aula: o rastro completo de um teste. [passo] / Te vejo lá! [endcard]

## Aula 28: Trace Viewer
1. E quando o teste falha no GitHub, onde você não estava olhando? Pra isso existe o trace. [título]
2. Trace quer dizer rastro: é um arquivo com tudo o que aconteceu no teste. [tradução]
3. Roda com traço traço trace on. [VS Code + terminal]
4. Abre o relatório e clica no trace do teste. [relatório]
5. Em cima, a linha do tempo. Na esquerda, os passos. No meio, a página. E embaixo, o console e a rede. [Trace Viewer animado]
6. No config já vem trace on first retry: quando um teste falha e roda de novo, o trace dessa segunda tentativa é gravado. No GitHub o config já tenta de novo, então lá isso acontece sozinho. Na sua máquina, sem nova tentativa, use o traço traço trace on. [editor com destaque em trace e retries]
7. Na próxima aula: pausando o teste no meio. [passo] / Te vejo lá! [endcard]

## Aula 29: Modo debug e page.pause
1. Às vezes você quer ver o teste devagar, um passo de cada vez. [título]
2. No terminal: npx playwright test traço traço debug. Ele abre o navegador e para antes do primeiro passo. [VS Code + terminal, depois o Inspector]
3. No Inspector, o botão step over executa um passo por vez. Olha: um clique, para; outro clique, para. [Inspector animado, passo a passo]
4. Outra forma, pra usar na sua máquina enquanto escreve o teste: page ponto pause no meio do código. Pause é pausar: rodando com o navegador aparecendo, o teste para exatamente ali e abre o Inspector. [editor + tradução + vídeo real parando]
5. É uma ferramenta de desenvolvimento: lembra de tirar o pause depois, senão o teste fica parado esperando você. [cards]
6. Na próxima aula: print e vídeo automático quando o teste falha. [passo] / Te vejo lá! [endcard]

## Aula 30: Print e vídeo quando o teste falha
1. E se o próprio teste tirasse um print e gravasse um vídeo quando falha? Ele faz isso. [título]
2. No config, dentro do use, adiciona duas linhas: screenshot only on failure, e video retain on failure. [editor digitando só as duas]
3. Traduzindo: screenshot, print, só quando falhar. Video retain on failure: o vídeo é gravado durante o teste, e guardado só se ele falhar. [tradução]
4. Quebra o teste de novo e roda. [VS Code + terminal: failed]
5. Abre o relatório: lá está o print do momento do erro e o vídeo do teste inteiro. [relatório com print e vídeo real]
6. E por que só quando falha? Porque gravar sempre deixa tudo mais lento e enche o computador de arquivo. [cards]
7. Desfaz o erro e fechamos o módulo de debug. [passo] / Te vejo lá! [endcard]

---

# Módulo 7 · Testes reais

## Aula 31: Uma lista de usuários e um teste que se repete
1. O saucedemo tem vários usuários que entram normalmente: standard, problem, performance glitch e visual. Copiar o mesmo teste quatro vezes? Não. [tela com a lista de usuários]
2. Primeiro, uma ideia nova: uma lista. Cria o arquivo usuarios ponto spec ponto js e escreve: const usuarios igual, abre colchetes. [editor]
3. Traduzindo: const, guarde com o nome usuarios. O igual, o que vem depois é o valor. E os colchetes abrem uma lista. [tradução]
4. Dentro da lista, os nomes entre aspas, separados por vírgula. A vírgula separa um item do outro. [editor digitando item por item]
5. Agora a repetição: for, abre parênteses, const usuario of usuarios. [editor]
6. Traduzindo: for, para cada. usuario, um nome que a gente dá pra cada item. of usuarios, da lista usuarios. Então: para cada usuário da lista. [tradução]
7. E o que estiver dentro das chaves do for se repete uma vez pra cada item. Quatro nomes, quatro vezes. [animação: a lista passando item por item]
8. Por enquanto, o nome do teste é fixo: login funciona. Na próxima aula, a gente faz o nome mudar com o usuário. [editor]
9. Dentro do teste, onde antes tinha standard user, agora vai a palavra usuario: o item da vez. [editor + destaque]
10. Repara no timeout de dez segundos na conferência final. É uma exceção, por causa do performance glitch, que você conheceu na aula 21. [editor com destaque]
11. Na próxima aula: um nome de teste que muda sozinho. [passo] / Te vejo lá! [endcard]

## Aula 32: O nome do teste que muda sozinho
1. Se você rodar o teste da aula passada, os quatro aparecem com o mesmo nome. Aí, se um falhar, qual foi? [VS Code + terminal: nomes repetidos]
2. A solução é colocar o nome do usuário dentro do nome do teste. [bigtext]
3. Pra isso, troca as aspas por crase. Com crase, dá pra misturar texto com o valor de uma variável. [editor + tradução: crase]
4. E o valor entra assim: cifrão, abre chaves, usuario, fecha chaves. [editor digitando]
5. Traduzindo: cifrão chaves quer dizer: coloque aqui o valor de usuario. [tradução]
6. Roda: quatro testes, cada um com o nome do seu usuário. [VS Code + terminal: 4 passed com os nomes]
7. Quer testar mais um usuário? Só coloca o nome na lista. [cards]
8. Na próxima aula: três navegadores ao mesmo tempo. [passo] / Te vejo lá! [endcard]

## Aula 33: 3 navegadores e testes em paralelo
1. Lembra das seis execuções com dois testes? Hoje você entende de onde vem. [título]
2. Sem o traço traço project, o Playwright roda em três navegadores: Chromium, Firefox e WebKit, que é o motor usado pelo Safari. [cards]
3. Eles estão no config, nos projects. [editor com destaque]
4. Roda tudo e repara na linha workers. Aqui na minha máquina apareceram quatro; na sua pode aparecer outro número. Worker é um trabalhador: um processo que ajuda a rodar testes ao mesmo tempo. [VS Code + terminal + tradução]
5. Paralelo quer dizer vários testes ao mesmo tempo, em vez de um por vez. Por isso cada teste precisa ser independente: nenhum pode depender de outro. [compare: um por vez × ao mesmo tempo]
6. No config, o fully parallel true liga isso. E no GitHub ele usa um worker só, pra execução ficar mais estável e previsível. [editor com destaque]
7. Na próxima aula: testando com tela de celular. [passo] / Te vejo lá! [endcard]

## Aula 34: Celular - emulando dispositivos
1. Muita gente acessa os sites pelo celular. O Playwright consegue imitar aparelhos conhecidos. [título]
2. Ele tem uma lista de aparelhos prontos, com tamanho de tela, toque e outras características. Isso ajuda muito, mas não substitui todos os testes num aparelho de verdade. [cards]
3. No config, cria um project novo chamado celular, usando o Pixel 7. [editor digitando só o bloco novo]
4. Roda com project igual celular e com o navegador aparecendo: olha, o site abre no tamanho de celular. [vídeo real em tela de celular]
5. E o mesmo teste funciona, sem mudar nada no código. [VS Code + terminal: passed]
6. Fechamos os testes reais. Agora: o projeto final! [passo] / Te vejo lá! [endcard]

---

# Módulo 8 · Projeto final

## Aula 35: O carrinho
1. Começa o projeto final: o fluxo de compra completo, do login até o obrigado. Hoje, o carrinho. [título]
2. Depois do login, cada produto tem um botão Add to cart. Clica com o botão direito e Inspecionar: data-test igual add-to-cart-sauce-labs-backpack. [vídeo real + DevTools]
3. Cria o compra ponto spec ponto js, com o login no before each, do jeito que você já sabe. [editor]
4. No teste: get by test id add-to-cart-sauce-labs-backpack, ponto click. [editor + tradução]
5. E a conferência: o numerozinho do carrinho mostra um. get by test id shopping-cart-badge, to have text um. [editor + tradução]
6. Roda com o navegador aparecendo: olha ele entrando, clicando em Add to cart, e o carrinho mostrando um. [vídeo real]
7. Na próxima aula: terminando o fluxo. [passo] / Te vejo lá! [endcard]

## Aula 36: Finalizando a compra
1. Hoje o robô completa o fluxo inteiro da compra: carrinho, dados, revisão e finalização. É um site de treino, então nenhuma compra de verdade acontece. [título]
2. Abre o carrinho: get by test id shopping-cart-link, click. Depois o botão checkout. [editor + tradução]
3. Na tela de dados, três campos: nome, sobrenome e CEP. Os data-test são firstName, lastName e postalCode. [vídeo real + DevTools]
4. Preenche os três e clica em continue. [editor: linha a linha]
5. Na tela de revisão, clica em finish. [editor]
6. E a conferência final: complete-header, to have text, Thank you for your order. [editor + tradução]
7. Roda com o navegador aparecendo e olha o fluxo inteiro acontecendo sozinho. [vídeo real do fluxo completo]
8. Na próxima aula: uma coisa que você talvez já tenha percebido. [passo] / Te vejo lá! [endcard]

## Aula 37: Percebeu que estamos copiando código?
1. Olha o login no login ponto spec, e olha o login no compra ponto spec. É o mesmo código, duas vezes. [editor lado a lado]
2. Agora imagina dez arquivos de teste. Se o botão de login mudar, você arruma em dez lugares. [animação: 10 arquivos se acendendo]
3. A solução é guardar o jeito de usar cada página num lugar só. Isso se chama Page Object: o objeto da página. [bigtext + tradução]
4. Pensa num controle remoto: você aperta ligar e não precisa saber como a TV funciona por dentro. [cards]
5. O teste vai dizer só login ponto entrar. Os detalhes de como entrar ficam guardados no Page Object. [compare: antes × depois, sem código novo]
6. Na próxima aula, a gente cria o primeiro, com calma. [passo] / Te vejo lá! [endcard]

## Aula 38: Criando o LoginPage, passo a passo
1. Cria uma pasta nova chamada pages, e dentro o arquivo LoginPage ponto js. [menu]
2. Primeira linha: export class LoginPage, e abre chaves. [editor]
3. Traduzindo: class é um molde, uma receita pra criar objetos. LoginPage é o nome do molde. E export deixa outros arquivos usarem. [tradução]
4. Dentro, o constructor, que recebe o page. Constructor quer dizer construtor: é o que roda quando alguém cria um LoginPage. [editor + tradução]
5. Primeira linha dele: this ponto page igual page. This quer dizer este: guarde o page dentro deste LoginPage. [editor + tradução]
6. Agora os elementos da página, um por linha: this ponto usuario igual page ponto get by test id username. Guarde o campo usuário com o nome usuario. [editor + tradução]
7. Mesma coisa pra senha, o botão e a mensagem de erro. [editor: uma linha por vez]
8. Por enquanto, ele só sabe onde estão as coisas. Na próxima aula, ele aprende a fazer o login, e o teste passa a usar. [passo] / Te vejo lá! [endcard]

## Aula 39: Usando o LoginPage no teste
1. Hoje o LoginPage aprende uma ação: entrar. [título]
2. Embaixo do constructor: async entrar, abre parênteses, usuario, vírgula, senha. Uma ação que recebe o usuário e a senha. [editor + tradução]
3. Dentro: await this ponto usuario ponto fill usuario. Preencha o campo usuário deste LoginPage com o usuário que chegou. [editor + tradução]
4. Depois a senha, e o clique no botão. [editor]
5. Agora no teste. Primeira coisa: import LoginPage from ponto ponto barra pages barra LoginPage. Traga o molde lá da pasta pages. [editor + tradução: ponto ponto barra = volte uma pasta]
6. Dentro do teste: const login igual new LoginPage, passando o page. New quer dizer: crie um novo, usando esse molde. [editor + tradução]
7. E as três linhas do login viram uma: await login ponto entrar, com usuário e senha. [editor: as três linhas somem, uma entra]
8. Lendo em português: crie um LoginPage e entre com esse usuário e essa senha. [bigtext]
9. Roda: continua passando. [VS Code + terminal + vídeo real]
10. Na próxima aula: a mesma receita pras outras páginas. [passo] / Te vejo lá! [endcard]

## Aula 40: A mesma receita - ProdutosPage e CheckoutPage
1. Você já sabe a receita: class, constructor, elementos e ações. Agora é só aplicar. [título]
2. ProdutosPage: os elementos são o título, o ícone do carrinho e o numerozinho. [editor]
3. E duas ações: adicionar um produto, e ir pro carrinho. Repara no adicionar: ele recebe o nome do produto e monta o data-test com crase, igual você aprendeu na aula 32. [editor + tradução]
4. CheckoutPage: os campos de nome, sobrenome e CEP, os botões, e a mensagem final. [editor]
5. E a ação preencher dados, que preenche os três campos e clica em continuar. [editor]
6. No teste da compra, cada passo agora lê como uma frase: produtos ponto adicionar, produtos ponto ir para carrinho, checkout ponto preencher dados. [editor]
7. Roda: o fluxo inteiro continua passando. [VS Code + terminal + vídeo real]
8. Na próxima aula: um relatório que se lê como roteiro. [passo] / Te vejo lá! [endcard]

## Aula 41: test.step - um relatório que se lê como roteiro
1. Quando um teste longo falha, você quer saber em qual parte. [título]
2. A sintaxe: await test ponto step, abre parênteses, o nome do passo entre aspas, vírgula, async, parênteses, seta, e abre chaves. [editor]
3. Traduzindo: test ponto step, um passo do teste. O nome, como ele aparece no relatório. E o bloco, o que esse passo faz. [tradução]
4. Coloca o primeiro passo: adiciona a mochila no carrinho. Roda e abre o relatório: o passo aparece com esse nome. [editor + relatório]
5. Agora os outros três, do mesmo jeito: abre o carrinho, preenche os dados de entrega, finaliza a compra. [editor]
6. E se falhar, o relatório mostra exatamente em qual passo. [relatório com um passo vermelho]
7. Na próxima aula: fazendo o login uma vez só. [passo] / Te vejo lá! [endcard]

## Aula 42: Indo além - login uma vez só com storageState
1. Todo teste faz login de novo. Em centenas de testes, é muito tempo perdido. [título]
2. A ideia: fazer o login uma vez, e salvar o navegador já logado num arquivo. Os testes que precisam começar logados usam esse arquivo. [cards]
3. Primeiro, a proteção: esse arquivo guarda dados da sua sessão e nunca deve ir pro GitHub. Abre o gitignore: o Playwright já colocou a pasta playwright barra ponto auth lá. Confere que ela está. [editor com destaque]
4. Cria o auth ponto setup ponto js. Ele faz o login e, no fim, storage state, salvando tudo em playwright barra ponto auth barra usuario ponto json. [editor + tradução: storage state = o estado guardado]
5. No config, um project chamado setup, que roda esse arquivo. E nos outros projects, dependencies setup: eles só começam depois do setup. [editor + tradução: dependencies = depende de]
6. Agora, quem usa o login salvo? Existem dois jeitos. A gente vai usar este: ligar só nos arquivos que precisam começar logados. O teste de login, por exemplo, precisa começar deslogado. [cards]
7. No arquivo da compra: test ponto use, storage state, e o caminho do arquivo. Use esse login salvo. [editor + tradução]
8. Roda: o setup aparece primeiro, e a compra começa direto na página de produtos. [VS Code + terminal + vídeo real]
9. Projeto final pronto! Agora ele vai pro GitHub. [passo] / Te vejo lá! [endcard]

---

# Módulo 9 · Git, GitHub e CI

## Aula 43: Git - salvando o projeto
1. O Git é um programa que guarda versões do seu projeto. Como pontos de salvamento num jogo. [título + cards]
2. No terminal do VS Code: git init. Init é iniciar: comece a guardar as versões desta pasta. [VS Code + terminal + tradução]
3. Depois: git add ponto. Add é adicionar, e o ponto quer dizer tudo: prepare todos os arquivos pro próximo salvamento. [VS Code + terminal + tradução]
4. Repara que o node modules, o ponto env e a pasta do login salvo não entram: o gitignore está fazendo o trabalho dele. [VS Code + destaque]
5. E: git commit traço m, e uma mensagem entre aspas, tipo meu primeiro projeto Playwright. Commit é o salvamento, e o traço m é a mensagem dele. [VS Code + terminal + tradução]
6. Se for a primeira vez que você usa o Git, ele pode pedir seu nome e seu e-mail. São dois comandos: git config traço traço global user ponto name, e user ponto email. Depois roda o commit de novo. [VS Code + terminal com o aviso real]
7. Pronto: o seu projeto tem o primeiro ponto de salvamento. Na próxima aula, ele vai pro GitHub. [passo] / Te vejo lá! [endcard]

## Aula 44: GitHub - enviando o projeto
1. O GitHub é um site que guarda projetos Git na internet. É a vitrine de quem trabalha com tecnologia. [título]
2. Cria uma conta no github ponto com, se ainda não tiver. Depois clica em New repository, dá o nome e cria, sem marcar nenhuma opção. [tela GitHub]
3. O GitHub mostra os comandos. No terminal: git branch traço M main. Dá o nome main pro ramo principal. [VS Code + terminal + tradução]
4. Depois: git remote add origin, e o endereço do seu repositório. Remote é remoto: avise o Git que existe uma cópia lá no GitHub, chamada origin. [VS Code + terminal + tradução]
5. E o envio: git push traço u origin main. Push é empurrar: mande o projeto pro GitHub. O traço u liga a sua main com a main de lá, e nas próximas vezes basta git push. [VS Code + terminal + tradução]
6. Na primeira vez, o Git pode abrir o navegador pra você entrar na sua conta do GitHub. É normal: faz o login e volta pro terminal. [cards]
7. Atualiza a página do GitHub: seu projeto está lá. E repara: nem o ponto env, nem a pasta do login salvo subiram. [tela GitHub com destaque]
8. Na próxima aula: os testes rodando sozinhos no GitHub. [passo] / Te vejo lá! [endcard]

## Aula 45: GitHub Actions - os testes rodando sozinhos
1. E se o GitHub rodasse os seus testes sozinho? É isso que o GitHub Actions faz. [título]
2. O Playwright já criou esse arquivo lá no começo: ponto github, workflows, playwright ponto yml. [editor]
3. Lendo em português: quando houver um push ou um pull request na main, use uma máquina Ubuntu, instale tudo e rode os testes. Esses quandos são os gatilhos do arquivo. [tradução em tabela]
4. Só falta uma coisa: o ponto env não foi pro GitHub, então lá os testes não sabem o usuário e a senha. [cards]
5. No GitHub: Settings, Secrets and variables, Actions, New repository secret. Cria o SAUCE underline USER e o SAUCE underline PASSWORD. Secret é segredo: ninguém consegue ver o valor depois. [tela GitHub, passo a passo]
6. No yml, no passo que roda os testes, um env que entrega esses segredos pros testes. [editor digitando só as linhas novas]
7. Manda pro GitHub com git push e abre a aba Actions: olha os testes rodando lá. [gh_actions animado]
8. Verde: passou. E no fim tem o relatório pra baixar, porque esse arquivo tem o passo que guarda ele. [gh_actions com o artifact]
9. Fechamos o projeto! Tem bônus: testes de API. [passo] / Te vejo lá! [endcard]

---

# Módulo 10 · Bônus API

## Aula 46: O que é uma API, explicado do zero
1. Quase todo site conversa com um servidor por trás. E pra essa conversa funcionar, existe a API. [título]
2. Uma API é um jeito combinado de um sistema pedir dados ou ações pra outro. Pensa num restaurante: você não entra na cozinha, você faz o pedido ao garçom, num formato combinado, e recebe a resposta. É uma simplificação, mas ajuda. [cards: você · garçom · cozinha]
3. Esses pedidos se chamam requisições, e cada uma tem um método. GET, buscar. POST, criar. DELETE, apagar. [tradução]
4. E a resposta vem com um número, o status: duzentos é deu certo, duzentos e um é criado, quatrocentos e quatro é não encontrado. [cards]
5. Vamos usar uma API de treino gratuita, a jsonplaceholder. Abre no navegador o endereço dela, barra posts barra um. [vídeo real abrindo a página]
6. Esse texto com chaves é JSON: um formato de dados que muitas APIs usam. [tradução em cima do JSON]
7. Na próxima aula: o seu primeiro teste de API. [passo] / Te vejo lá! [endcard]

## Aula 47: Seu primeiro teste de API
1. Teste de API não abre navegador nenhum. Por isso ele é bem rápido. [título]
2. Cria o api ponto spec ponto js. No teste, em vez do page, você pede o request, entre chaves. Request quer dizer requisição. [editor + tradução]
3. const resposta igual await request ponto get, e o endereço. Busque o post número um e guarde a resposta. [editor + tradução]
4. expect, resposta ponto status, abre e fecha parênteses, to be duzentos. Eu espero que o status da resposta seja duzentos. Repara nos parênteses depois do status. [editor + tradução]
5. Depois: const post igual await resposta ponto json, com parênteses. Leia os dados que vieram. E o expect: post ponto id, to be um. [editor + tradução]
6. Roda: passou, em milissegundos. [VS Code + terminal]
7. Na próxima aula: criando e apagando pela API. [passo] / Te vejo lá! [endcard]

## Aula 48: Criando e apagando dados pela API
1. Agora vamos simular uma criação e uma exclusão. A API de treino responde como uma de verdade, mas não guarda essas mudanças. [título]
2. request ponto post, com um data: título, texto e userId. É a requisição de criar. [editor + tradução]
3. A conferência: status duzentos e um, criado. E o título que voltou é o mesmo que você mandou. [editor + tradução]
4. request ponto delete: apagar. Status duzentos. [editor + tradução]
5. Roda os três: passaram. [VS Code + terminal]
6. Num sistema real, essa criação e essa exclusão ficariam guardadas no banco de dados. [cards]
7. Fechamos o bônus! Agora: desafios pra você praticar. [passo] / Te vejo lá! [endcard]

---

# Módulo 11 · Desafios
Formato de todos: desafio → "pausa o vídeo e tenta" (contagem de 5 segundos na tela) → dica → solução digitada linha a linha com tradução → vídeo real rodando.

## Aula 49: Desafio 1 - senha errada
1. Primeiro desafio: o que acontece quando alguém erra a senha? [título]
2. O teste: usuário certo, senha errada, e conferir a mensagem de erro. Pausa o vídeo e tenta fazer sozinho. [cards + contagem]
3. Dica: a mensagem fica no data-test error, e contém do not match. [vídeo real mostrando o erro]
4. Solução: preenche, preenche, clica, e expect error to contain text do not match. Contém o texto: não precisa ser a mensagem inteira. [editor + tradução]
5. Roda e olha: o erro aparece e o teste passa. [vídeo real + terminal] / Te vejo no próximo desafio! [endcard]

## Aula 50: Desafio 2 - campos vazios
1. Desafio dois: e se a pessoa clicar em Login sem preencher nada? [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: a mensagem é Username is required. [vídeo real]
4. Solução: só o clique e o expect. Repara: nem todo teste preenche tudo, e um bom teste também confere o que dá errado. [editor + tradução]
5. Roda: passou. [vídeo real + terminal] / Te vejo no próximo! [endcard]

## Aula 51: Desafio 3 - remover do carrinho
1. Desafio três: adicionar a mochila e depois remover. [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: depois de adicionar, o botão vira Remove, com data-test remove-sauce-labs-backpack. E quando o carrinho fica vazio, o numerozinho some da página. [vídeo real]
4. Solução: pra conferir que ele saiu da página, to have count zero: eu espero que o seletor encontre zero elementos. [editor + tradução]
5. Roda. [vídeo real + terminal] / Te vejo no próximo! [endcard]

## Aula 52: Desafio 4 - ordenar por preço
1. Desafio quatro: ordenar do menor pro maior preço. [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: a caixa de ordenar é um select, uma caixa de opções. Pra escolher uma opção, existe o select option, escolha a opção. A do menor preço se chama lohi, de low to high: do baixo pro alto. [vídeo real + tradução]
4. Solução: como a gente conhece os produtos desse site de treino, a conferência é simples: depois de ordenar, o primeiro preço é sete e noventa e nove. Ponto first: o primeiro. [editor + tradução]
5. Roda. [vídeo real + terminal] / Te vejo no próximo! [endcard]

## Aula 53: Desafio 5 - logout
1. Desafio cinco: sair do sistema. [título]
2. Pausa e tenta. [cards + contagem]
3. Dica: o menu é aquele botão de três risquinhos, com nome Open Menu. Lá dentro tem o Logout. [vídeo real]
4. Solução: clica no menu, clica no logout, e confere que o botão de Login voltou. [editor + tradução]
5. Roda. [vídeo real + terminal] / Te vejo no desafio final! [endcard]

## Aula 54: Desafio final - compra com dois produtos
1. Desafio final: comprar dois produtos e conferir o total. [título]
2. Pausa e tenta. Esse é maior, sem pressa. [cards + contagem]
3. Dica: a mochila e a lanterna da bicicleta, bike light. O total fica no data-test total-label. Com os preços desse site de treino, o total conhecido é quarenta e três e dezoito. [vídeo real]
4. Solução, passo a passo. [editor: linha a linha com tradução das novas]
5. Roda e olha o fluxo inteiro. [vídeo real + terminal]
6. Se você conseguiu montar boa parte desse desafio sozinho, você já está juntando seletores, ações e conferências sem copiar um roteiro pronto. Esse é um grande passo. [bigtext] / Te vejo na última parte! [endcard]

---

# Módulo 12 · Carreira

## Aula 55: Veio do Cypress? Um mapa das ideias
1. Se você já usou Cypress, várias ideias vão parecer familiares. Mas não pense no Playwright como uma simples troca de comandos. [título]
2. Algumas aproximações ajudam: cy ponto visit lembra page ponto goto. cy ponto contains lembra get by text. should lembra expect. [tabela com o aviso: aproximações]
3. Mas o modelo muda. No Playwright você escreve await em cada passo, e os seletores são objetos que você guarda e reaproveita. [compare]
4. As duas ferramentas resolvem problemas parecidos, com abordagens diferentes. Saber as duas te deixa mais forte no mercado. [bigtext]
5. Te vejo na próxima! [endcard]

## Aula 56: O seu projeto no currículo e na entrevista
1. Agora você tem um projeto de automação. Vamos colocar isso no seu currículo do jeito certo. [título]
2. No currículo, escreve o que você realmente fez: testes de ponta a ponta com Playwright e JavaScript, Page Object, testes de API, vários navegadores e execução no GitHub Actions. [cards]
3. A regra: só coloca o que você consegue explicar numa entrevista. [bigtext]
4. Perguntas que costumam aparecer e que você já sabe responder: o que é auto-wait? Por que preferir seletores pela função? O que é Page Object? [cards: pergunta → resposta curta]
5. E o que é um teste flaky, que às vezes passa e às vezes falha? E como evitar? [cards]
6. Mostrar o projeto funcionando no GitHub ajuda muito a transformar o que está no currículo numa demonstração concreta. [bigtext]
7. Te vejo na última aula! [endcard]

## Aula 57: Seu projeto pronto pro portfólio e a colinha completa
1. Última aula. Vamos deixar o seu projeto pronto pra quem visitar. [título]
2. Cria um README ponto md com: o objetivo, as tecnologias, o que precisa instalar, como instalar, e os comandos pra rodar os testes. [editor]
3. Coloca o selinho do GitHub Actions. O próprio GitHub gera o código dele, com o endereço do seu repositório e do seu workflow. Ele mostra se os testes estão passando. [tela GitHub com o selo]
4. E a sua colinha completa: do primeiro comando ao Page Object, ao login salvo, ao GitHub Actions e à API. Deixa ela aberta enquanto pratica. [colinha, página por página]
5. Você começou sem saber nada e terminou com um projeto completo: login, compra, API e tudo rodando no GitHub. [montagem rápida das aulas]
6. Próximos passos: pratique, crie novos cenários e mantenha o seu GitHub atualizado. [cards]
7. E se o curso te ajudou, deixa uma avaliação honesta na Udemy. Ela ajuda a melhorar o curso e orienta outros alunos. [bigtext]
8. Até a próxima! [endcard]

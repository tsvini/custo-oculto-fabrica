# Roteiros aprovados · Módulo 8 (gerado do roteiro_playwright_m8.py)

## Aula 35: O carrinho
1. Começa o projeto final: o fluxo de compra completo, do login até o obrigado. Hoje, o carrinho. [bigtext]
2. Depois do login, cada produto tem um botão Add to cart. Clica com o botão direito e Inspecionar: data-test igual add-to-cart-sauce-labs-backpack. [devtools]
3. Cria o compra ponto spec ponto js, com o login no before each, do jeito que você já sabe. [editor]
4. No teste: get by test id add-to-cart-sauce-labs-backpack, ponto click. [editor]
5. E a conferência: o numerozinho do carrinho mostra um. get by test id shopping-cart-badge, to have text um. [editor]
6. Roda com o navegador aparecendo: olha ele entrando, clicando em Add to cart, e o carrinho mostrando um. [editor]
7. Na próxima aula: terminando o fluxo. [passo]
8. Te vejo lá! [endcard]

## Aula 36: Finalizando a compra
1. Hoje o robô completa o fluxo inteiro da compra: carrinho, dados, revisão e finalização. É um site de treino, então nenhuma compra de verdade acontece. [bigtext]
2. Abre o carrinho: get by test id shopping-cart-link, click. Depois o botão checkout. [editor]
3. Na tela de dados, três campos: nome, sobrenome e CEP. Os data-test são firstName, lastName e postalCode. [devtools]
4. Preenche os três e clica em continue. [editor]
5. Na tela de revisão, clica em finish. [editor]
6. E a conferência final: complete-header, to have text, Thank you for your order. [editor]
7. Roda com o navegador aparecendo e olha o fluxo inteiro acontecendo sozinho. [editor]
8. Na próxima aula: uma coisa que você talvez já tenha percebido. [passo]
9. Te vejo lá! [endcard]

## Aula 37: Percebeu que estamos copiando código?
1. Olha o login no login ponto spec, e olha o login no compra ponto spec. É o mesmo código, duas vezes. [editor]
2. Agora imagina dez arquivos de teste. Se o botão de login mudar, você arruma em dez lugares. [cards]
3. A solução é guardar o jeito de usar cada página num lugar só. Isso se chama Page Object: o objeto da página. [traducao]
4. Pensa num controle remoto: você aperta ligar e não precisa saber como a TV funciona por dentro. [cards]
5. O teste vai dizer só login ponto entrar. Os detalhes de como entrar ficam guardados no Page Object. [compare]
6. Na próxima aula, a gente cria o primeiro, com calma. [passo]
7. Te vejo lá! [endcard]

## Aula 38: Criando o LoginPage, passo a passo
1. Cria uma pasta nova chamada pages, e dentro o arquivo LoginPage ponto js. [menu]
2. Primeira linha: export class LoginPage, e abre chaves. [editor]
3. Traduzindo: class é um molde, uma receita pra criar objetos. LoginPage é o nome do molde. E export deixa outros arquivos usarem. [traducao]
4. Dentro, o constructor, que recebe o page. Constructor quer dizer construtor: é o que roda quando alguém cria um LoginPage. [editor]
5. Primeira linha dele: this ponto page igual page. This quer dizer este: guarde o page dentro deste LoginPage. [editor]
6. Agora os elementos da página, um por linha: this ponto usuario igual page ponto get by test id username. Guarde o campo usuário com o nome usuario. [editor]
7. Mesma coisa pra senha, o botão e a mensagem de erro. [editor]
8. Por enquanto, ele só sabe onde estão as coisas. Na próxima aula, ele aprende a fazer o login, e o teste passa a usar. [passo]
9. Te vejo lá! [endcard]

## Aula 39: Usando o LoginPage no teste
1. Hoje o LoginPage aprende uma ação: entrar. [bigtext]
2. Embaixo do constructor: async entrar, abre parênteses, usuario, vírgula, senha. Uma ação que recebe o usuário e a senha. [editor]
3. Dentro: await this ponto usuario ponto fill usuario. Preencha o campo usuário deste LoginPage com o usuário que chegou. [editor]
4. Depois a senha, e o clique no botão. [editor]
5. Agora no teste. Primeira coisa: import LoginPage from ponto ponto barra pages barra LoginPage. Traga o molde lá da pasta pages. [editor]
6. Dentro do teste: const login igual new LoginPage, passando o page. New quer dizer: crie um novo, usando esse molde. [editor]
7. E as três linhas do login viram uma: await login ponto entrar, com usuário e senha. [editor]
8. Lendo em português: crie um LoginPage e entre com esse usuário e essa senha. [bigtext]
9. Roda: continua passando. [editor]
10. Na próxima aula: a mesma receita pras outras páginas. [passo]
11. Te vejo lá! [endcard]

## Aula 40: A mesma receita - ProdutosPage e CheckoutPage
1. Você já sabe a receita: class, constructor, elementos e ações. Agora é só aplicar. [bigtext]
2. ProdutosPage: os elementos são o título, o ícone do carrinho e o numerozinho. [editor]
3. E duas ações: adicionar um produto, e ir pro carrinho. Repara no adicionar: ele recebe o nome do produto e monta o data-test com crase, igual você aprendeu na aula 32. [editor]
4. CheckoutPage: os campos de nome, sobrenome e CEP, os botões, e a mensagem final. [editor]
5. E a ação preencher dados, que preenche os três campos e clica em continuar. [editor]
6. No teste da compra, cada passo agora lê como uma frase: produtos ponto adicionar, produtos ponto ir para carrinho, checkout ponto preencher dados. [editor]
7. Roda: o fluxo inteiro continua passando. [editor]
8. Na próxima aula: um relatório que se lê como roteiro. [passo]
9. Te vejo lá! [endcard]

## Aula 41: test.step - um relatório que se lê como roteiro
1. Quando um teste longo falha, você quer saber em qual parte. [bigtext]
2. A sintaxe: await test ponto step, abre parênteses, o nome do passo entre aspas, vírgula, async, parênteses, seta, e abre chaves. [editor]
3. Traduzindo: test ponto step, um passo do teste. O nome, como ele aparece no relatório. E o bloco, o que esse passo faz. [traducao]
4. Coloca o primeiro passo: adiciona a mochila no carrinho. Roda e abre o relatório: o passo aparece com esse nome. [pw_relatorio]
5. Agora os outros três, do mesmo jeito: abre o carrinho, preenche os dados de entrega, finaliza a compra. [editor]
6. E se falhar, o relatório mostra exatamente em qual passo. [pw_relatorio]
7. Na próxima aula: fazendo o login uma vez só. [passo]
8. Te vejo lá! [endcard]

## Aula 42: Indo além - login uma vez só com storageState
1. Todo teste faz login de novo. Em centenas de testes, é muito tempo perdido. [bigtext]
2. A ideia: fazer o login uma vez, e salvar o navegador já logado num arquivo. Os testes que precisam começar logados usam esse arquivo. [cards]
3. Primeiro, a proteção: esse arquivo guarda dados da sua sessão e nunca deve ir pro GitHub. Abre o gitignore: o Playwright já colocou a pasta playwright barra ponto auth lá. Confere que ela está. [editor]
4. Cria o auth ponto setup ponto js. Ele faz o login e, no fim, storage state, salvando tudo em playwright barra ponto auth barra usuario ponto json. [editor]
5. No config, um project chamado setup, que roda esse arquivo. E nos outros projects, dependencies setup: eles só começam depois do setup. [editor]
6. Agora, quem usa o login salvo? Existem dois jeitos. A gente vai usar este: ligar só nos arquivos que precisam começar logados. O teste de login, por exemplo, precisa começar deslogado. [cards]
7. No arquivo da compra: test ponto use, storage state, e o caminho do arquivo. Use esse login salvo. [editor]
8. Roda: o setup aparece primeiro, e a compra começa direto na página de produtos. [editor]
9. Projeto final pronto! Agora ele vai pro GitHub. [passo]
10. Te vejo lá! [endcard]

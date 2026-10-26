# Roteiros · Nível 2 (aulas 55 a 80) · versão 2

Junta o roteiro revisado (aulas abrindo com um problema real, flaky abrindo com a falha, bug no projeto 2) com três correções:
1. **O bug do projeto 2 é de verdade:** o projeto 2 usa a **Lojinha do Leigo**, a loja de treino do próprio curso. A versão 1 tem um bug real na ordenação por preço (ela compara o preço como texto); a versão 2 é a corrigida. O aluno abre as duas e vê com os próprios olhos.
2. **O mock tem uma API pra fingir:** a Lojinha do Leigo busca os produtos num `api/produtos.json`. A aula 66 usa ela (a saucedemo não tem API).
3. **A nova aba usa o jeito mais simples:** `const promessa = page.waitForEvent('popup')`, clica, e `await promessa`. Faz o mesmo que o `Promise.all`, com menos coisa estranha pra um iniciante.

Ordem do curso: aulas 1 a 54 sem mudança · Módulo 12 (55 a 63) · Módulo 13 (64 a 73) · Módulo 14 (74 a 80) · Módulo 15 · Carreira (81 a 83, as antigas 55 a 57).
Formato: narração, e entre colchetes [o que aparece na tela]. Todo código passa no GitHub Actions antes de virar aula.

---

## Ajuste na aula 2 (frase nova, depois da do Mac e Linux)
- "E um aviso: a partir do módulo doze, o nível sobe. Se você já automatiza testes e só quer ver o Playwright mais a fundo, pode pular direto pra lá." [mapa: módulos 1 a 11 "do zero" · 12 a 14 "nível 2" · 15 "carreira"]

## Ajuste no fim da aula 54
- "Você terminou a parte do zero. A partir de agora, o nível sobe. Te vejo lá!" [endcard: PRÓXIMA: NÍVEL 2]

---

# Módulo 12 · Um site que você nunca viu

## Aula 55: Bem-vindo ao nível 2
1. Até aqui você aprendeu Playwright praticamente do zero. Agora o nível sobe um pouco. [título: NÍVEL 2]
2. Nos próximos módulos, eu quero te colocar em situações que aparecem quando você começa a automatizar sistemas reais. [site novo → problemas novos → recursos novos → projeto novo]
3. E pra isso a gente sai um pouco do saucedemo. Vamos usar o the internet: um site de treino com várias páginas diferentes. [vídeo real: abrindo the-internet.herokuapp.com e rolando a lista]
4. Tem upload, nova aba, iframe, alerta, tabela. Mas eu não quero que você decore uma lista de comandos. [vídeo real]
5. A ideia vai ser sempre: apareceu um problema novo, a gente descobre como resolver. [bigtext]
6. Cria o arquivo internet ponto spec ponto js. Como o baseURL ainda aponta pro saucedemo, aqui a gente usa o endereço completo. [editor]
7. Vamos começar com uma coisa que aparece em quase todo formulário. [passo] / Te vejo lá! [endcard]

## Aula 56: O formulário mudou
1. Imagina que caiu uma tarefa nova: validar as preferências de um formulário. [título + card da tarefa]
2. Abrindo a tela, tem duas coisas que a gente ainda não usou: a caixa de marcar e a lista de opções. [vídeo real: checkboxes]
3. Pra marcar: ponto check. Pra desmarcar: ponto uncheck. [editor + tradução: check = marque · uncheck = desmarque]
4. Mas clicar não basta: a gente confere. to be checked, esteja marcada. E com o not na frente: não esteja marcada. [editor + tradução]
5. Agora o segundo campo: aqui a pessoa escolhe uma opção. Você já viu isso no desafio quatro: select option. [vídeo real: dropdown]
6. E a conferência: to have value, tenha o valor dois. [editor + tradução]
7. Roda e olha. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 57: O usuário precisa enviar um arquivo
1. A tarefa mudou: o usuário precisa conseguir anexar um documento. Currículo, comprovante, planilha. [título + card da tarefa]
2. Na tela tem um campo de escolher arquivo e um botão Upload. [vídeo real]
3. Primeiro, um arquivo de exemplo dentro do projeto: uma pasta arquivos, com um texto dentro. [editor: arquivos/exemplo.txt]
4. Agora: set input files, coloque este arquivo no campo. [editor + tradução]
5. Repara: o Playwright não abre aquela janela do Windows pra procurar o arquivo com o mouse. Ele entrega o arquivo direto pro campo. [cards]
6. Clica em Upload e confere que o nome do arquivo apareceu na página. [editor]
7. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 58: Uma caixa travou a página
1. Agora aconteceu uma coisa diferente: clicamos num botão e o navegador abriu essa caixa. [título + vídeo real: o alerta aparecendo]
2. Enquanto ela está aberta, não dá pra usar a página. Isso é um alerta do navegador, um dialog. [vídeo real]
3. A gente precisa preparar o Playwright antes de o alerta aparecer: page ponto on, dialog, e dialog ponto accept. Quando aparecer um alerta, aceite. [editor + tradução]
4. A ordem é importante: primeiro prepara, depois clica. Se você tentar reagir só depois, o alerta já passou. [preparar → clicar → aparece → aceita]
5. No fim, confere a mensagem: You successfully clicked an alert. [editor]
6. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 59: O link abriu outra aba
1. Imagina: você clica pra ver os detalhes de um pedido, e eles abrem em outra aba. E o teste continua olhando a aba antiga. [título + vídeo real: Click Here abrindo outra aba]
2. Então a gente precisa pegar a aba nova quando ela abrir. [cards]
3. Primeiro, o aviso: const promessa igual page ponto wait for event, popup. Espere uma nova aba. [editor + tradução]
4. Depois clica no link. E aí: const novaAba igual await promessa. Guarde a aba que abriu. [editor + tradução]
5. A partir daí, você usa a nova aba igual ao page: confere que ela mostra New Window. [editor]
6. Roda e olha as duas abas. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 60: Tem uma página dentro da página
1. Olha essa tela: tem um editor de texto no meio. Só que o seletor normal não acha nada lá dentro. [título + vídeo real: iframe]
2. Por quê? Porque aquele pedaço é outra página, encaixada nesta. Isso se chama iframe. [página principal › iframe › editor + DevTools mostrando o iframe]
3. Primeiro, você diz em qual quadro procurar: frame locator. Procure dentro deste quadro. [editor + tradução]
4. Depois, procura normalmente lá dentro, e confere o texto do editor. [editor]
5. A lógica: entrar no iframe, procurar o elemento, conferir. [passo a passo]
6. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 61: O botão só aparece quando passo o mouse
1. Chegou um relato de bug: não consigo clicar na opção, porque ela só aparece quando passo o mouse no usuário. [título + card do bug]
2. Vamos reproduzir: sem o mouse em cima, o nome está escondido. Com o mouse, ele aparece. [vídeo real: hovers]
3. No Playwright: hover. Passe o mouse por cima. [editor + tradução]
4. Antes do hover: not to be visible. Depois do hover: to be visible. Assim a gente testa o comportamento, não só roda um comando. [editor]
5. Roda e olha o mouse passando. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 62: O usuário precisa arrastar um item
1. Tem tela em que a pessoa reorganiza as coisas arrastando: quadro de tarefas, lista, arquivos. [título]
2. No nosso exemplo, duas caixas: A e B. A gente quer arrastar a A até a B. [vídeo real: drag and drop]
3. Um comando: drag to. Arraste até. [editor + tradução]
4. E não basta confiar que arrastou: a gente confere que a primeira caixa agora mostra B. [editor]
5. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 63: A tabela mudou de ordem e o teste quebrou
1. Um problema bem real: uma tabela de clientes. [título + vídeo real: tables]
2. Dava pra dizer: pegue a segunda linha. Só que amanhã alguém ordena a tabela por nome, a pessoa muda de lugar, e o teste começa a olhar pra pessoa errada. [vídeo real: clicando no cabeçalho e a ordem mudando]
3. Então, em vez da posição, a gente procura pelo conteúdo: get by role row, filter has text. Ache a linha que tem este nome. [editor + tradução]
4. E dentro dessa linha, o valor devido: confere que é cinquenta dólares. [editor]
5. Antes: a segunda linha. Depois: a linha que tem o nome da pessoa. Se a ordem mudar, o teste continua achando a pessoa certa. [compare]
6. Roda. [VS Code + terminal] / Fechamos o site novo! Agora, recursos que aparecem em projetos de verdade. [endcard]

---

# Módulo 13 · Playwright de verdade no trabalho

## Aula 64: O teste está montando coisa demais
1. Olha um dos nossos testes: antes de testar qualquer coisa, ele monta o LoginPage, o ProdutosPage. E isso se repete em vários arquivos. [título + editor com os news destacados]
2. O Playwright já entrega uma coisa pronta: o page. E se a gente pudesse fazer o mesmo com as nossas páginas? Isso são as fixtures. [cards: page · request · a sua]
3. Uma fixture é algo que o teste recebe pronto. Cria o fixtures ponto js: test ponto extend, ensinando como montar o loginPage. [editor digitando]
4. Lendo em português: estenda o test com um loginPage, que é criado assim, e entregue pronto pro teste. [tradução]
5. No teste, você importa esse test novo e pede o loginPage entre chaves, igual ao page. [editor]
6. Sem new em cada arquivo: o teste fica só com o que importa. [compare: antes × depois]
7. Roda: continua passando. [VS Code + terminal] / Te vejo na próxima! [endcard]

## Aula 65: Os dados ficaram maiores que o teste
1. Temos vários usuários pra validar. Dava pra deixar tudo dentro do teste, mas olha como ele começa a crescer. [título + editor com o bloco grande de dados]
2. O teste deveria deixar claro o comportamento. Então a gente separa os dados: usuarios ponto json. [editor]
3. No teste, importa o JSON e usa o for que você conhece da aula trinta e um. [editor]
4. Nesse tipo de teste, acrescentar um caso novo pode virar só mais uma entrada no JSON. E ajuda quando os dados mudam mais que a lógica do teste. [cards]
5. Roda: um teste pra cada linha do arquivo. [VS Code + terminal] / Te vejo na próxima! [endcard]

## Aula 66: E se o servidor responder errado?
1. Uma situação interessante: o site está funcionando. Mas o que a tela faz se o servidor responder diferente, ou cair? [título]
2. A gente não vai derrubar o servidor da empresa pra descobrir. A gente controla a conversa. Isso é um mock. [normal: navegador → servidor · com mock: navegador → Playwright → resposta controlada]
3. Pra isso, a Lojinha do Leigo, a loja de treino do curso. Ela busca os produtos num endereço da API. [vídeo real: a loja + DevTools › Network mostrando o produtos.json]
4. Primeiro, a prova de que o Playwright está no meio: page ponto route nesse endereço, e route ponto abort. Bloqueie. [editor + tradução]
5. Roda: a loja mostra que não conseguiu carregar os produtos. [navegador real]
6. Agora o uso de verdade: route ponto fulfill, responda no lugar do servidor, com uma lista vazia. [editor + tradução]
7. E a conferência: a loja mostra nenhum produto encontrado. [navegador real + terminal passando]
8. É assim que se testa erro, lista vazia e lentidão, sem esperar isso acontecer de verdade. [bigtext] / Te vejo na próxima! [endcard]

## Aula 67: O botão funciona, mas ficou errado
1. Imagina que alguém mexeu no botão de comprar. Ele continua clicável, o teste continua passando. Mas ele ficou visualmente errado. [título + compare: antes × depois]
2. Um teste comum não percebe. Um teste visual percebe: to have screenshot. Tire uma foto e compare com a guardada. [editor + tradução]
3. Na primeira vez, ele ainda não tem foto pra comparar: então guarda essa como referência. [terminal com a mensagem real]
4. Roda de novo: a tela está igual, passou. [terminal]
5. Agora a gente muda alguma coisa. O relatório mostra o esperado, o atual e a diferença pintada. [relatório real]
6. Se a mudança foi de propósito, atualiza a foto com traço traço update snapshots. Se não foi, você acabou de achar um bug visual. [terminal] / Te vejo na próxima! [endcard]

## Aula 68: Quero ver todos os erros da tela de uma vez
1. Uma tela com dez informações. A primeira conferência falha, o teste para. Você corrige, roda de novo, e só então descobre que a quinta também estava errada. [título + animação]
2. Pra isso existe o expect ponto soft: anote o erro e continue conferindo. [editor + tradução]
3. Três conferências, duas erradas de propósito: no fim, o relatório mostra as duas. [terminal com as duas falhas reais]
4. Cuidado: pros passos principais do fluxo, o expect normal continua sendo o certo. O soft é pra vários dados independentes na mesma tela. [compare] / Te vejo na próxima! [endcard]

## Aula 69: Não dá tempo de rodar tudo
1. O time vai fazer uma entrega. Tem muitos testes, e alguém pergunta: qual o mínimo pra saber se o sistema está de pé? [título]
2. Pra isso servem as tags: uma etiqueta no teste, arroba smoke. [editor]
3. E roda só os marcados: traço traço grep arroba smoke. [terminal]
4. Em vez de cento e cinquenta testes, dez críticos. Depois, com mais tempo, o regressivo completo. [cards]
5. Tag não é enfeite: ela organiza jeitos diferentes de rodar. [bigtext] / Te vejo na próxima! [endcard]

## Aula 70: Passou. Rodei de novo. Falhou.
1. Olha isso. Rodei: passou. Rodei de novo o mesmo teste: falhou. Não mudei uma linha. [título + terminal real: passou, falhou, passou]
2. Esse é o teste flaky: às vezes passa, às vezes falha, sem nenhuma mudança que explique. [bigtext]
3. A reação mais comum: coloca três segundos de espera aí e vê se resolve. Às vezes parece resolver. [editor: waitForTimeout(3000)]
4. Mas agora o teste sempre espera três segundos. E no dia em que o sistema levar quatro, falha de novo. [compare]
5. O caminho certo: esperar o que importa. Um expect que espera sozinho, como na aula vinte e um. [editor]
6. Pra achar teste instável: traço traço repeat each igual a dez. Se falhar duas em dez, tem coisa pra investigar. [terminal real]
7. E o retries do config tenta de novo no GitHub. Mas guarda essa: retry diminui o estrago, não corrige a causa. [bigtext] / Te vejo na próxima! [endcard]

## Aula 71: O mesmo sistema, três ambientes
1. No trabalho, o mesmo sistema existe em vários endereços: o de teste, o de homologação e o de verdade. [título + cards]
2. E a gente não quer mexer no código toda vez. Então o baseURL lê uma variável. [editor]
3. Traduzindo: se existe uma BASE URL, use ela. Se não, use esse endereço. [tradução do ||]
4. Na sua máquina, você só muda a variável na hora de rodar. No GitHub Actions, ela fica no yml. O teste continua igual. [terminal + editor] / Te vejo na próxima! [endcard]

## Aula 72: O teste falhou. O que eu mando pro desenvolvedor?
1. Você roda a pipeline e um teste falha. Mandar só "a automação quebrou" não ajuda ninguém. [título]
2. O relatório do Playwright traz o erro, a linha, o print, o vídeo, o trace e os passos. Vamos abrir uma falha de verdade. [relatório real]
3. Aqui dá pra ver onde quebrou, o que era esperado e o que aconteceu. E o trace mostra a execução inteira. [relatório + trace]
4. Uma mensagem útil pro time: o cenário, o esperado, o que aconteceu, e o trace junto. [cartão de bug]
5. Automação também é gerar evidência que ajuda a investigar. [bigtext] / Te vejo na próxima! [endcard]

## Aula 73: O que você já consegue fazer
1. Olha o que entrou nesse nível: site novo, fixtures, dados num arquivo, mock, teste visual, soft, tags, flaky, ambientes e relatórios. [montagem]
2. Tudo isso está numa página nova da colinha. [colinha: página 5]
3. E agora eu quero fazer diferente. No próximo módulo, eu não vou começar te mostrando código. Você vai receber uma tarefa, e vai precisar pensar primeiro. [bigtext] / Te vejo lá! [endcard]

---

# Módulo 14 · Projeto 2, pensando como QA (na Lojinha do Leigo)

## Aula 74: A missão
1. Nova tarefa. Você recebeu este card. [título + card]
2. Como cliente, quero entrar na loja e ordenar os produtos, pra achar mais fácil o que procuro. E a instrução é só: testa. [card da história]
3. Ainda não abre o VS Code. Primeiro, pensa como QA: o que precisa funcionar? O que pode dar errado? O que está faltando nessa história? [perguntas + contagem: pausa e pensa]
4. Por exemplo: todo usuário pode entrar? E com a senha errada? Quais ordenações precisam existir? E um produto esgotado, aparece ou não? O card não diz. [cards]
5. Antes do código, a gente entende o problema. [bigtext] / Te vejo na próxima! [endcard]

## Aula 75: Os cenários, em português
1. Agora a gente transforma a tarefa em situações pra validar. [título]
2. O caminho principal: login válido, os produtos aparecem, a ordenação funciona. [lista]
3. Os caminhos de erro: senha errada, usuário bloqueado, campo vazio. [lista]
4. A ordenação: nome de A a Z, de Z a A, preço do menor pro maior e do maior pro menor. [lista]
5. E a pergunta que o card não respondia: o produto esgotado. A gente pergunta pra quem pediu, e anota a resposta: ele aparece, mas sem poder comprar. [card: pergunta → resposta]
6. Também decide o que não é dessa tarefa: pagamento, por exemplo. Saber limitar o escopo também é trabalho de QA. [cards]
7. Cada cenário que importa vira um teste. [lista virando nomes de teste] / Te vejo na próxima! [endcard]

## Aula 76: Tem alguma coisa errada aqui
1. Antes de automatizar, vamos rodar alguns cenários na mão, na versão que o time entregou. [título + vídeo real: a Lojinha do Leigo, versão 1]
2. Login válido: ok. Senha errada: ok. Usuário bloqueado: ok. [vídeo real]
3. Agora, ordenar do menor pro maior preço. Repara nos valores: cento e vinte e nove e noventa, quinze e noventa e nove, trinta e nove e noventa, sete e noventa e nove. [vídeo real + preços destacados]
4. Isso não está em ordem. Antes de escrever uma linha de automação, você acabou de achar um bug. [bigtext]
5. É exatamente por isso que a gente pensou nos cenários antes de abrir o editor. [bigtext]
6. Vamos registrar: o título, o passo a passo, o esperado, o que aconteceu, e o print. [cartão de bug]
7. O time corrigiu e entregou a versão dois. Abre de novo: agora sim, do menor pro maior. Agora a gente automatiza. [vídeo real: versão 2] / Te vejo na próxima! [endcard]

## Aula 77: Começando o projeto organizado
1. Um projeto Playwright novo. Mas desta vez você não está começando do zero. [título + terminal: npm init playwright]
2. Você já sabe que vai precisar de: pages, fixtures, dados e testes. [explorer com as pastas]
3. E no config: o baseURL da Lojinha do Leigo, o testIdAttribute e o dotenv. [editor]
4. Repara: no primeiro projeto, cada uma dessas coisas era novidade. Agora você escolhe a estrutura com intenção. [bigtext] / Te vejo na próxima! [endcard]

## Aula 78: Page Objects e fixture
1. O LoginPage, e o ProdutosPage, desta vez com uma ação de ordenar e uma que lê os preços da tela. [editor]
2. E a fixture que entrega os dois prontos pros testes. [editor]
3. O teste começa assim: recebendo o loginPage e o produtosPage. [editor]
4. Repara como foi mais rápido da segunda vez. Não porque a gente pulou explicação: porque agora você conhece a receita. [bigtext] / Te vejo na próxima! [endcard]

## Aula 79: Agora sim, automatizando os cenários
1. A lista vira teste. Login: válido, senha errada, bloqueado, campo vazio. Os dados vêm do JSON. [editor]
2. Ordenação: os quatro sentidos, sem copiar o mesmo teste quatro vezes. Os dados controlam a execução. [editor]
3. E pra conferir a ordem de verdade: lê todos os preços da tela e compara com a mesma lista, ordenada. [editor + tradução]
4. O esgotado: aparece, com o botão desabilitado. to be disabled. [editor + tradução]
5. O cenário principal marcado com arroba smoke. [editor]
6. Roda tudo na versão dois: passou. [VS Code + terminal real]
7. E se alguém aponta pra versão um? Os testes de preço ficam vermelhos. A automação pegaria esse bug sozinha. [terminal real: as duas falhas na versão 1] / Te vejo na próxima! [endcard]

## Aula 80: Do card à pipeline
1. GitHub, os secrets, e o GitHub Actions. Push, e a pipeline roda: verde. [gh_actions]
2. Um README que conta os cenários e o bug que você achou. [editor]
3. Olha o caminho inteiro que você fez: o card, as dúvidas, os cenários, o teste na mão, o bug, a correção, a automação, o GitHub e o CI. [fluxo animado]
4. Isso é muito mais importante do que saber escrever page ponto click. Você recebeu uma tarefa, pensou, achou um problema, automatizou o que importa, e colocou pra rodar sozinho. [bigtext]
5. E agora são dois projetos no seu GitHub, e uma história muito melhor pra contar numa entrevista. [bigtext]
6. Última parte: carreira. [passo] / Te vejo lá! [endcard]

---

# Módulo 15 · Carreira (aulas 81 a 83)
As antigas 55, 56 e 57, com ajustes:
- **Aula 82 (currículo):** a lista ganha "mock de rede, teste visual e fixtures" e "dois projetos no GitHub". E uma pergunta de entrevista nova: "Conta um bug que você achou." (a resposta é a história da aula 76).
- **Aula 83 (portfólio):** a colinha passa a ter 5 páginas, e a montagem final inclui o projeto 2.

---

# A Lojinha do Leigo (o que já está pronto)
- Fica em `docs/loja` do repositório, publicada pelo GitHub Pages (tsvini.github.io/custo-oculto-fabrica/loja/).
- Login com `cliente` e `bloqueado` (senha `leigo123`), mensagens de erro para campo vazio, senha errada e usuário bloqueado.
- Produtos vindos de `api/produtos.json`, ordenação nos 4 sentidos, um produto esgotado com o botão desabilitado, e o contador do carrinho.
- `?versao=1`: a versão com o bug (a ordenação por preço compara texto: R$ 129,90 vem antes de R$ 7,99). Sem o parâmetro: a versão corrigida.
- Tudo com `data-test`, igual ao saucedemo, então o `getByTestId` funciona do mesmo jeito.

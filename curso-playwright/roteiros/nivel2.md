# Roteiros · Nível 2 (aulas 55 a 80) + ajustes

Nova ordem do curso:
- Aulas 1 a 54 (do básico aos desafios): não mudam de número.
- **Módulo 12 · Um site que você nunca viu**: aulas 55 a 63.
- **Módulo 13 · Playwright de verdade no trabalho**: aulas 64 a 73.
- **Módulo 14 · Projeto 2, pensando como QA**: aulas 74 a 80.
- **Módulo 15 · Carreira**: aulas 81 a 83 (eram as 55 a 57).

Formato de cada frase: a narração, e entre colchetes [o que aparece na tela].
Todo código passa no GitHub Actions antes de virar aula.

---

## Ajuste na aula 2 (uma frase nova, depois da do Mac e Linux)
- "E um aviso: a partir do módulo doze, o nível sobe. Se você já automatiza testes e só quer ver o Playwright mais a fundo, pode pular direto pra lá." [mapa do curso: módulos 1 a 11 "do zero" · 12 a 14 "nível 2" · 15 "carreira"]

## Ajuste no fim da aula 54
- O "Te vejo na última parte!" vira: "Você terminou a parte do zero. A partir de agora, o nível sobe. Te vejo lá!" [endcard: PRÓXIMA: NÍVEL 2]

---

# Módulo 12 · Um site que você nunca viu

## Aula 55: Bem-vindo ao nível 2
1. Você já sabe o básico. Agora o nível sobe. [título: NÍVEL 2]
2. Nos próximos três módulos: um site novo, recursos que você vai usar no trabalho, e um segundo projeto do zero. [cards: site novo · trabalho de verdade · projeto 2]
3. Se em algum momento ficar difícil, volta na aula do assunto. A colinha continua do seu lado. [colinha aberta]
4. O site novo é o the-internet: uma coleção de páginas de treino, cada uma com um desafio diferente. [vídeo real: abrindo the-internet.herokuapp.com e rolando a lista]
5. Cria um arquivo novo, internet ponto spec ponto js. E como o baseURL do config aponta pro saucedemo, aqui a gente usa o endereço completo. [editor: o arquivo novo com a constante do endereço]
6. Na próxima aula: caixas de marcar e listas. [passo] / Te vejo lá! [endcard]

## Aula 56: Checkbox e dropdown
1. Dois elementos que aparecem em todo formulário: a caixa de marcar e a lista de opções. [título]
2. Abre a página checkboxes: duas caixas, uma marcada e outra não. [vídeo real]
3. Pra marcar: ponto check. Pra desmarcar: ponto uncheck. [editor digitando + tradução: check = marque · uncheck = desmarque]
4. E a conferência: to be checked, esteja marcada. Com o not na frente: não esteja marcada. [editor + tradução]
5. Agora a página dropdown. Você já conhece o select option, do desafio quatro. [vídeo real abrindo a lista]
6. Escolhe a opção dois e confere com to have value: tenha o valor dois. [editor + tradução]
7. Roda e olha. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 57: Upload de arquivo
1. Mandar um arquivo pro site: currículo, foto, planilha. Como testar isso? [título]
2. Abre a página upload: um botão Escolher arquivo e um botão Upload. [vídeo real]
3. Primeiro, um arquivo de exemplo no projeto: uma pasta arquivos, com um texto dentro. [editor: arquivos/exemplo.txt]
4. O comando é set input files: coloque estes arquivos no campo. Ele não abre a janelinha do Windows: entrega o arquivo direto. [editor + tradução]
5. Clica em Upload e confere que o nome do arquivo apareceu na página. [editor]
6. Roda e olha o arquivo subindo. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 58: Alerta do navegador
1. Sabe aquela caixinha do navegador com um OK? Ela trava a página até alguém clicar. [título]
2. Abre a página javascript alerts e clica no primeiro botão: aparece o alerta. [vídeo real]
3. O Playwright fecha esses alertas sozinho, clicando em cancelar. Pra decidir o que fazer, você escuta o alerta antes de ele aparecer. [cards: sozinho, ele cancela · você escuta antes]
4. page ponto on, dialog: quando aparecer um alerta, faça isto. E dentro: dialog ponto accept, aceite. [editor + tradução]
5. Repara na ordem: primeiro você prepara o ouvido, depois clica no botão. Ao contrário, o alerta já passou. [editor com destaque na ordem]
6. Confere a mensagem do resultado: You successfully clicked an alert. [editor]
7. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 59: Nova aba
1. Alguns links abrem uma aba nova. E o teste continua olhando a aba antiga. [título]
2. Abre a página windows e clica em Click Here: abre outra aba. [vídeo real]
3. O jeito certo: espera o evento de página nova e clica, ao mesmo tempo. [editor: o Promise.all com waitForEvent('popup')]
4. Lendo em português: espere uma nova janela abrir enquanto você clica no link. E guarda a nova aba numa constante. [tradução]
5. A partir daí, você usa a nova aba igual ao page: confere que ela tem o texto New Window. [editor]
6. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 60: Iframe, uma página dentro da página
1. Às vezes um pedaço da tela é outra página, encaixada. Isso se chama iframe. [título]
2. Abre a página iframe: o editor de texto no meio é uma página dentro da página. [vídeo real + DevTools mostrando o iframe]
3. O seletor normal não enxerga lá dentro. Primeiro você entra no iframe, com frame locator. [editor + tradução: frameLocator = entre neste quadro]
4. Depois, procura o elemento como sempre, e confere o texto que está dentro do editor. [editor]
5. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 61: Hover, o menu que só aparece com o mouse em cima
1. Tem coisa que só aparece quando o mouse passa por cima. [título]
2. Abre a página hovers: passa o mouse na foto e aparece o nome do usuário. [vídeo real]
3. O comando é hover: passe o mouse por cima. [editor + tradução]
4. Antes do hover, o nome está escondido: not to be visible. Depois do hover: to be visible. [editor]
5. Roda e olha o mouse passando. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 62: Arrastar e soltar
1. Arrastar um item de um lugar pro outro: quadro de tarefas, lista, upload. [título]
2. Abre a página drag and drop: duas caixas, A e B. [vídeo real]
3. Um comando só: drag to, arraste até. A caixa A, arraste até a caixa B. [editor + tradução]
4. E a conferência: agora a primeira caixa mostra B. [editor]
5. Roda. [VS Code + terminal + navegador real] / Te vejo na próxima! [endcard]

## Aula 63: Lendo uma tabela
1. Tabelas aparecem em todo sistema: pedidos, clientes, relatórios. [título]
2. Abre a página tables: uma tabela com nome, e-mail e valor devido. [vídeo real]
3. Pra achar uma linha pelo texto: get by role row, com o filter has text. Ache a linha que tem este texto. [editor + tradução]
4. E dentro dessa linha, a célula do valor: confere que é cinquenta dólares. [editor]
5. Assim o teste não depende da posição da linha: se a tabela mudar de ordem, ele continua achando a pessoa certa. [compare: pela posição × pelo texto]
6. Roda. [VS Code + terminal] / Fechamos o site novo! Agora, recursos do dia a dia de trabalho. [endcard]

---

# Módulo 13 · Playwright de verdade no trabalho

## Aula 64: Fixtures, o seu próprio page
1. Lembra do page que o Playwright te entrega pronto? Você pode criar os seus. [título: FIXTURES]
2. Uma fixture é uma coisa que o teste recebe pronta. O page é uma fixture. [cards: page · request · a sua]
3. Cria o arquivo fixtures ponto js. Com test ponto extend, você ensina o Playwright a montar um loginPage pronto. [editor digitando]
4. Lendo em português: estenda o test com um loginPage, que é criado assim, e entregue pro teste. [tradução]
5. No teste, você importa esse test novo, e pede o loginPage entre chaves, igual ao page. [editor]
6. Sem new, sem repetir: o teste fica só com o que importa. [compare: antes × depois]
7. Roda. [VS Code + terminal] / Te vejo na próxima! [endcard]

## Aula 65: Dados de teste num arquivo
1. E se o mesmo teste precisar rodar com vários dados diferentes? [título]
2. Cria um arquivo usuarios ponto json, com uma lista: o usuário e a mensagem que ele deve ver. [editor]
3. No teste, importa o JSON e usa o for que você já conhece, da aula trinta e um. [editor]
4. Agora quem não programa também consegue acrescentar um caso novo: é só uma linha no JSON. [cards]
5. Roda: um teste pra cada linha do arquivo. [VS Code + terminal] / Te vejo na próxima! [endcard]

## Aula 66: Mock, fingindo a resposta do servidor
1. Como testar a tela quando o servidor cai? Você não vai derrubar o servidor de verdade. Você finge. [título: MOCK]
2. Mock é fingir: o navegador pede, e o Playwright responde no lugar do servidor. [cards: navegador · Playwright no meio · servidor]
3. Primeiro, um exemplo que você enxerga: page ponto route, e bloquear todas as imagens do saucedemo. [editor + tradução: route = intercepte · abort = bloqueie]
4. Roda: a loja aparece sem nenhuma foto. [navegador real: produtos sem imagem]
5. Agora uma resposta inventada: route ponto fulfill, responda com este JSON. [editor + tradução]
6. Abre o endereço da API: em vez do post de verdade, aparece o que você escreveu. [navegador real]
7. No trabalho, é assim que se testa erro, lentidão e tela vazia, sem depender de ninguém. [bigtext] / Te vejo na próxima! [endcard]

## Aula 67: Teste visual
1. O botão mudou de cor sem ninguém pedir. Um teste normal não percebe. Um teste visual percebe. [título]
2. to have screenshot: tire uma foto da tela e compare com a foto guardada. [editor + tradução]
3. Na primeira vez, ele falha de propósito: ainda não tem foto pra comparar, então ele guarda essa como a referência. [terminal com a mensagem real]
4. Roda de novo: passou, a tela está igual à foto. [terminal]
5. Se a tela mudar, ele mostra no relatório as duas fotos e a diferença pintada. [relatório: esperado · atual · diferença]
6. Mudou de propósito? Atualiza a foto com traço traço update snapshots. [terminal] / Te vejo na próxima! [endcard]

## Aula 68: Soft assertions, conferir tudo antes de falhar
1. Quando um expect falha, o teste para ali. Às vezes você quer saber tudo o que está errado de uma vez. [título]
2. expect ponto soft: confira, anote o erro, e continue. [editor + tradução]
3. Três conferências soft, duas erradas de propósito: o relatório mostra as duas no fim. [terminal com as duas falhas reais]
4. Use em telas com muitos campos pra conferir. Pros passos principais, o expect normal continua sendo o certo. [compare] / Te vejo na próxima! [endcard]

## Aula 69: Tags, o teste rápido e o completo
1. Antes de cada entrega, nem sempre dá tempo de rodar tudo. [título: TAGS]
2. Coloca uma etiqueta no teste: arroba smoke, no nome ou no tag. [editor]
3. Roda só os marcados: traço traço grep arroba smoke. [terminal]
4. E o contrário, tudo menos esses: grep invert. [terminal]
5. No dia a dia: smoke a cada mudança, que é rápido; o regressivo completo, antes de entregar. [cards] / Te vejo na próxima! [endcard]

## Aula 70: O teste flaky, e como resolver de verdade
1. Flaky é o teste que às vezes passa e às vezes falha, sem ninguém mudar nada. [título: FLAKY]
2. O jeito errado de resolver: wait for timeout, esperar um tempo fixo. Ou é lento demais, ou ainda não é suficiente. [editor com o jeito errado riscado]
3. O jeito certo: espere a coisa que importa. Um expect que espera sozinho, igual ao da aula vinte e um. [editor]
4. Pra achar o flaky: traço traço repeat each igual a dez. Roda o mesmo teste dez vezes. [terminal real]
5. E o retries no config ajuda no GitHub, mas não conserta nada: o relatório marca o teste como flaky, pra você ir atrás. [relatório com o selo flaky] / Te vejo na próxima! [endcard]

## Aula 71: Outro ambiente, o mesmo teste
1. Na empresa, o mesmo sistema existe em vários lugares: o de testes, o de homologação e o de verdade. [título]
2. No config, o baseURL lê uma variável: se ela existir, usa ela; se não, usa o saucedemo. [editor + tradução do ||]
3. Pra rodar em outro lugar, você só muda a variável na hora de rodar. Nenhuma linha do teste muda. [terminal]
4. No GitHub Actions, a mesma ideia: a variável fica no yml. [editor] / Te vejo na próxima! [endcard]

## Aula 72: Relatórios e o que mandar pro time
1. O teste falhou. O que você manda pro desenvolvedor? [título]
2. O relatório HTML: o passo, o erro, a foto, o vídeo e o trace. [relatório real]
3. No GitHub Actions, o relatório fica pra baixar no fim da execução. [gh_actions com o artefato]
4. Uma boa mensagem de bug: o que fez, o que esperava, o que aconteceu, e o trace junto. [cards] / Te vejo na próxima! [endcard]

## Aula 73: Revisão do nível 2
1. Revisando: site novo, fixtures, dados num arquivo, mock, teste visual, soft, tags, flaky, ambientes e relatórios. [montagem rápida]
2. Na colinha tem uma página nova com tudo isso. [colinha: página 5]
3. Agora, o projeto dois: do zero, pensando como QA. [passo] / Te vejo lá! [endcard]

---

# Módulo 14 · Projeto 2, pensando como QA

## Aula 74: A missão
1. Você recebeu uma tarefa: a tela de login e de produtos de uma loja. Testa. [título: PROJETO 2]
2. Antes de abrir o VS Code, um QA pensa: o que pode dar errado aqui? [bigtext]
3. A história de usuário: como cliente, eu quero entrar na loja e ordenar os produtos, pra achar o mais barato. [cartão de história]
4. Na próxima aula: transformar isso em casos de teste, em português. [passo] / Te vejo lá! [endcard]

## Aula 75: Os cenários, em português
1. Primeiro no papel, depois no código. [título]
2. O caminho feliz: entra e ordena. [lista]
3. Os caminhos tristes: senha errada, usuário bloqueado, campo vazio. [lista]
4. Os limites: ordenar por nome de A a Z e de Z a A, e por preço nos dois sentidos. [lista]
5. E o que não testar agora: pagamento, por exemplo, que é outra história. Saber dizer não também é trabalho de QA. [cards]
6. Cada linha dessa lista vira um teste. [lista virando nomes de teste] / Te vejo na próxima! [endcard]

## Aula 76: A estrutura do projeto
1. Uma pasta nova, um projeto Playwright novo, igual ao módulo dois. [terminal: npm init playwright]
2. Desta vez, já começando organizado: pages, fixtures, dados e testes. [explorer com as pastas]
3. O config com baseURL, testIdAttribute e o dotenv, como você já sabe. [editor] / Te vejo na próxima! [endcard]

## Aula 77: Os Page Objects e a fixture
1. O LoginPage e o ProdutosPage, desta vez com um método de ordenar. [editor]
2. A fixture que entrega os dois prontos. [editor]
3. Repara como vai mais rápido da segunda vez: é a mesma receita. [bigtext] / Te vejo na próxima! [endcard]

## Aula 78: Os testes, um por cenário
1. Os testes de login: um pra cada caminho, com os dados vindos do JSON. [editor]
2. Os testes de ordenar: os quatro sentidos, com um for. [editor]
3. E o smoke marcado com a tag. [editor]
4. Roda tudo. [VS Code + terminal real] / Te vejo na próxima! [endcard]

## Aula 79: CI e README
1. GitHub, os secrets e o Actions, como no módulo nove. [gh_actions]
2. Um README que conta os cenários: quem visita entende o que você testou e por quê. [editor]
3. O selo verde. [GitHub com o selo] / Te vejo na próxima! [endcard]

## Aula 80: O que você acabou de fazer
1. Você recebeu uma tarefa, pensou nos cenários, organizou, automatizou e colocou pra rodar sozinho. [montagem]
2. É exatamente isso que um QA de automação faz no trabalho. E agora são dois projetos no seu GitHub. [bigtext]
3. Última parte: a sua carreira. [passo] / Te vejo lá! [endcard]

---

# Módulo 15 · Carreira (aulas 81 a 83)
As antigas 55, 56 e 57, com dois ajustes:
- **Aula 82 (currículo):** a lista ganha "mock de rede, teste visual e fixtures" e "dois projetos no GitHub".
- **Aula 83 (portfólio):** a colinha passa a ter 5 páginas, e a montagem final inclui o projeto 2.

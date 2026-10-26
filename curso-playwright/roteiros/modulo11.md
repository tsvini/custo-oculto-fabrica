# Roteiros aprovados · Módulo 11 (gerado do roteiro_playwright_m11.py)

## Aula 49: Desafio 1 - senha errada
1. Primeiro desafio: o que acontece quando alguém erra a senha? [bigtext]
2. Isso se chama cenário negativo: testar o que acontece quando a pessoa erra. No trabalho, é onde mais aparece bug, porque quase ninguém lembra de testar. [cards]
3. O teste: usuário certo, senha errada, e conferir a mensagem de erro. Pausa o vídeo e tenta fazer sozinho. [+pausa] [desafio]
4. Dica: a mensagem fica no data-test error, e contém do not match. [tela]
5. Solução: preenche, preenche, clica, e expect error to contain text do not match. [editor]
6. Contém o texto: não precisa ser a mensagem inteira. [traducao]
7. Roda e olha: o erro aparece e o teste passa. [+pausa] [editor]
8. Te vejo no próximo desafio! [endcard]

## Aula 50: Desafio 2 - campos vazios
1. Desafio dois: e se a pessoa clicar em Login sem preencher nada? [bigtext]
2. Por que testar isso? Porque é a primeira coisa que alguém apressado faz: clica sem preencher. O sistema precisa avisar, e não pode deixar entrar nem travar. [cards]
3. Pausa e tenta. [+pausa] [desafio]
4. Dica: a mensagem é Username is required. [tela]
5. Solução: só o clique e o expect. [+pausa] [editor]
6. Repara: nem todo teste preenche tudo, e um bom teste também confere o que dá errado. [bigtext]
7. Roda: passou. [+pausa] [editor]
8. Te vejo no próximo! [endcard]

## Aula 51: Desafio 3 - remover do carrinho
1. Desafio três: adicionar a mochila e depois remover. [bigtext]
2. No trabalho, o remover quebra mais do que parece: o número não atualiza, ou o produto continua lá. E quase ninguém testa, porque todo mundo só testa o adicionar. [cards]
3. Pausa e tenta. [+pausa] [desafio]
4. Dica: depois de adicionar, o botão vira Remove, com data-test remove-sauce-labs-backpack. E quando o carrinho fica vazio, o numerozinho some da página. [tela]
5. Solução: pra conferir que ele saiu da página, to have count zero: [editor]
6. eu espero que o seletor encontre zero elementos. [traducao]
7. Roda. [+pausa] [editor]
8. Te vejo no próximo! [endcard]

## Aula 52: Desafio 4 - ordenar por preço
1. Desafio quatro: ordenar do menor pro maior preço. [bigtext]
2. Ordenar parece simples, mas é um bug clássico: o site ordena o preço como se fosse texto, e o doze e cinquenta aparece antes do sete e noventa e nove. [traducao]
3. Pausa e tenta. [+pausa] [desafio]
4. Dica: a caixa de ordenar é um select, uma caixa de opções. [tela]
5. Pra escolher uma opção, existe o select option, escolha a opção. A do menor preço se chama lohi, de low to high: do baixo pro alto. [traducao]
6. Solução: como a gente conhece os produtos desse site de treino, a conferência é simples: depois de ordenar, o primeiro preço é sete e noventa e nove. [editor]
7. Conferir só o primeiro é o jeito mais simples. No módulo 14, você confere a lista inteira, e pega exatamente esse bug numa loja de verdade. [bigtext]
8. Ponto first: o primeiro. [traducao]
9. Roda. [+pausa] [editor]
10. Te vejo no próximo! [endcard]

## Aula 53: Desafio 5 - logout
1. Desafio cinco: sair do sistema. [bigtext]
2. Por que testar o sair? Porque se ele falhar num computador compartilhado, a próxima pessoa entra direto na sua conta. [cards]
3. Pausa e tenta. [+pausa] [desafio]
4. Dica: o menu é aquele botão de três risquinhos, com nome Open Menu. Lá dentro tem o Logout. [tela]
5. Solução: clica no menu, clica no logout, e confere que o botão de Login voltou. [editor]
6. Roda. [+pausa] [editor]
7. Te vejo no desafio final! [endcard]

## Aula 54: Desafio final - compra com dois produtos
1. Desafio final: comprar dois produtos e conferir o total. [bigtext]
2. Por que conferir o total? Porque é dinheiro: um erro de soma no carrinho é o tipo de bug que a empresa não pode deixar passar. [cards]
3. Pausa e tenta. Esse é maior, sem pressa. [+pausa] [desafio]
4. Dica: a mochila e a lanterna da bicicleta, bike light. O total fica no data-test total-label. Com os preços desse site de treino, o total conhecido é quarenta e três e dezoito. [tela]
5. Solução, passo a passo. [+pausa] [editor]
6. Roda e olha o fluxo inteiro. [+pausa] [editor]
7. Se você conseguiu montar boa parte desse desafio sozinho, você já está juntando seletores, ações e conferências sem copiar um roteiro pronto. Esse é um grande passo. [bigtext]
8. Você terminou a parte do zero. A partir de agora, o nível sobe. Te vejo lá! [endcard]

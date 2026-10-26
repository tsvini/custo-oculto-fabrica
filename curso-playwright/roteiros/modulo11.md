# Roteiros aprovados · Módulo 11 (gerado do roteiro_playwright_m11.py)

## Aula 49: Desafio 1 - senha errada
1. Primeiro desafio: o que acontece quando alguém erra a senha? [bigtext]
2. O teste: usuário certo, senha errada, e conferir a mensagem de erro. Pausa o vídeo e tenta fazer sozinho. [+pausa] [desafio]
3. Dica: a mensagem fica no data-test error, e contém do not match. [tela]
4. Solução: preenche, preenche, clica, e expect error to contain text do not match. [editor]
5. Contém o texto: não precisa ser a mensagem inteira. [traducao]
6. Roda e olha: o erro aparece e o teste passa. [editor]
7. Te vejo no próximo desafio! [endcard]

## Aula 50: Desafio 2 - campos vazios
1. Desafio dois: e se a pessoa clicar em Login sem preencher nada? [bigtext]
2. Pausa e tenta. [+pausa] [desafio]
3. Dica: a mensagem é Username is required. [tela]
4. Solução: só o clique e o expect. [editor]
5. Repara: nem todo teste preenche tudo, e um bom teste também confere o que dá errado. [bigtext]
6. Roda: passou. [editor]
7. Te vejo no próximo! [endcard]

## Aula 51: Desafio 3 - remover do carrinho
1. Desafio três: adicionar a mochila e depois remover. [bigtext]
2. Pausa e tenta. [+pausa] [desafio]
3. Dica: depois de adicionar, o botão vira Remove, com data-test remove-sauce-labs-backpack. E quando o carrinho fica vazio, o numerozinho some da página. [tela]
4. Solução: pra conferir que ele saiu da página, to have count zero: [editor]
5. eu espero que o seletor encontre zero elementos. [traducao]
6. Roda. [editor]
7. Te vejo no próximo! [endcard]

## Aula 52: Desafio 4 - ordenar por preço
1. Desafio quatro: ordenar do menor pro maior preço. [bigtext]
2. Pausa e tenta. [+pausa] [desafio]
3. Dica: a caixa de ordenar é um select, uma caixa de opções. [tela]
4. Pra escolher uma opção, existe o select option, escolha a opção. A do menor preço se chama lohi, de low to high: do baixo pro alto. [traducao]
5. Solução: como a gente conhece os produtos desse site de treino, a conferência é simples: depois de ordenar, o primeiro preço é sete e noventa e nove. [editor]
6. Ponto first: o primeiro. [traducao]
7. Roda. [editor]
8. Te vejo no próximo! [endcard]

## Aula 53: Desafio 5 - logout
1. Desafio cinco: sair do sistema. [bigtext]
2. Pausa e tenta. [+pausa] [desafio]
3. Dica: o menu é aquele botão de três risquinhos, com nome Open Menu. Lá dentro tem o Logout. [tela]
4. Solução: clica no menu, clica no logout, e confere que o botão de Login voltou. [editor]
5. Roda. [editor]
6. Te vejo no desafio final! [endcard]

## Aula 54: Desafio final - compra com dois produtos
1. Desafio final: comprar dois produtos e conferir o total. [bigtext]
2. Pausa e tenta. Esse é maior, sem pressa. [+pausa] [desafio]
3. Dica: a mochila e a lanterna da bicicleta, bike light. O total fica no data-test total-label. Com os preços desse site de treino, o total conhecido é quarenta e três e dezoito. [tela]
4. Solução, passo a passo. [+pausa] [editor]
5. Roda e olha o fluxo inteiro. [editor]
6. Se você conseguiu montar boa parte desse desafio sozinho, você já está juntando seletores, ações e conferências sem copiar um roteiro pronto. Esse é um grande passo. [bigtext]
7. Te vejo na última parte! [endcard]

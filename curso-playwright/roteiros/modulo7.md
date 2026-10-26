# Roteiros aprovados · Módulo 7 (gerado do roteiro_playwright_m7.py)

## Aula 31: Uma lista de usuários e um teste que se repete
1. O saucedemo tem vários usuários que entram normalmente: standard, problem, performance glitch e visual. Copiar o mesmo teste quatro vezes? Não. [tela]
2. Primeiro, uma ideia nova: uma lista. Cria o arquivo usuarios ponto spec ponto js e escreve: const usuarios igual, abre colchetes. [editor]
3. Traduzindo: const, guarde com o nome usuarios. O igual, o que vem depois é o valor. E os colchetes abrem uma lista. [traducao]
4. Dentro da lista, os nomes entre aspas, separados por vírgula. A vírgula separa um item do outro. [editor]
5. Agora a repetição: for, abre parênteses, const usuario of usuarios. [editor]
6. Traduzindo: for, para cada. usuario, um nome que a gente dá pra cada item. of usuarios, da lista usuarios. Então: para cada usuário da lista. [traducao]
7. E o que estiver dentro das chaves do for se repete uma vez pra cada item. Quatro nomes, quatro vezes. [cards]
8. Por enquanto, o nome do teste é fixo: login funciona. Na próxima aula, a gente faz o nome mudar com o usuário. [editor]
9. Dentro do teste, onde antes tinha standard user, agora vai a palavra usuario: o item da vez. [editor]
10. Repara no timeout de dez segundos na conferência final. É uma exceção, por causa do performance glitch, que você conheceu na aula 21. [editor]
11. Na próxima aula: um nome de teste que muda sozinho. [passo]
12. Te vejo lá! [endcard]

## Aula 32: O nome do teste que muda sozinho
1. Se você rodar agora, o Playwright nem começa. Ele reclama: duplicate test title, nome de teste repetido. Os quatro testes teriam o mesmo nome, e ele não deixa. [editor]
2. A solução é colocar o nome do usuário dentro do nome do teste. [bigtext]
3. Pra isso, troca as aspas por crase. Com crase, dá pra misturar texto com o valor de uma variável. [editor]
4. E o valor entra assim: cifrão, abre chaves, usuario, fecha chaves. [traducao]
5. Traduzindo: cifrão chaves quer dizer: coloque aqui o valor de usuario. [traducao]
6. Roda: quatro testes, cada um com o nome do seu usuário. [pw_relatorio]
7. Quer testar mais um usuário? Só coloca o nome na lista. [cards]
8. Na próxima aula: três navegadores ao mesmo tempo. [passo]
9. Te vejo lá! [endcard]

## Aula 33: 3 navegadores e testes em paralelo
1. Lembra das seis execuções com dois testes? Hoje você entende de onde vem. [bigtext]
2. Sem o traço traço project, o Playwright roda em três navegadores: Chromium, Firefox e WebKit, que é o motor usado pelo Safari. [cards]
3. Eles estão no config, nos projects. [editor]
4. Roda tudo e repara na linha workers. Aqui na minha máquina apareceram quatro; na sua pode aparecer outro número. Worker é um trabalhador: um processo que ajuda a rodar testes ao mesmo tempo. [editor]
5. Paralelo quer dizer vários testes ao mesmo tempo, em vez de um por vez. Por isso cada teste precisa ser independente: nenhum pode depender de outro. [compare]
6. No config, o fully parallel true liga isso. E no GitHub ele usa um worker só, pra execução ficar mais estável e previsível. [editor]
7. Na próxima aula: testando com tela de celular. [passo]
8. Te vejo lá! [endcard]

## Aula 34: Celular - emulando dispositivos
1. Muita gente acessa os sites pelo celular. O Playwright consegue imitar aparelhos conhecidos. [bigtext]
2. Ele tem uma lista de aparelhos prontos, com tamanho de tela, toque e outras características. Isso ajuda muito, mas não substitui todos os testes num aparelho de verdade. [cards]
3. No config, cria um project novo chamado celular, usando o Pixel 7. [editor]
4. Roda com project igual celular e com o navegador aparecendo: olha, o site abre no tamanho de celular. [editor]
5. E o mesmo teste funciona, sem mudar nada no código. [editor]
6. Fechamos os testes reais. Agora: o projeto final! [passo]
7. Te vejo lá! [endcard]

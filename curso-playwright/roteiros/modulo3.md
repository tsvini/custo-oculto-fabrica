# Roteiros aprovados · Módulo 3 (com ajustes da revisão)

## Aula 12: A receita de um teste - test e expect
1. Agora começa o seu código. E a primeira coisa é apagar o exemplo: clica com o botão direito no example ponto spec ponto js e escolhe Delete. [menu]
2. Na pasta tests, cria um arquivo novo: login ponto spec ponto js. [menu]
3. Primeira linha: import, chaves, test, vírgula, expect, fecha chaves, from, e entre aspas arroba playwright barra test. Ela traz duas ferramentas: o test, pra criar um teste, e o expect, pra conferir. [editor]
4. Agora o teste: test, abre parênteses, o nome do teste entre aspas, entra com usuário e senha, vírgula, async, abre parênteses, abre chaves, page, fecha chaves, fecha parênteses, seta, e abre chaves. E lá embaixo, fecha com chave, parêntese e ponto e vírgula. [editor]
5. Calma, eu explico cada pedaço. O nome entre aspas aparece no relatório, então escreve o que o teste faz, em português mesmo. [editor]
6. O page é o navegador que o Playwright te entrega. É com ele que você abre sites e clica nas coisas. [editor]
7. E o async quer dizer que, lá dentro, a gente vai usar o await, que significa: espera esse passo terminar antes de ir pro próximo. [cards]
8. Esse é o esqueleto de todo teste. Ainda está vazio, e na próxima aula a gente coloca o primeiro passo. [editor]
9. Te vejo lá! [endcard]

## Aula 13: page.goto - abrindo um site
1. Primeiro passo de todo teste: abrir o site. [bigtext]
2. Dentro do teste, digita await page ponto goto, e entre aspas o endereço: https dois pontos barra barra www ponto saucedemo ponto com. [editor]
3. Esse é o site de treino que a gente vai usar no curso todo: uma lojinha feita pra quem está aprendendo a testar. [tela]
4. Agora roda, mas dessa vez quero que você veja o navegador abrindo. No terminal: npx playwright test traço traço headed traço traço project igual chromium. [terminal]
5. O headed mostra a janela, e o project igual chromium roda só no Chromium, pra ficar mais rápido. [cards]
6. Viu? O navegador abriu o site e fechou. O teste passou, porque abrir o site deu certo. [terminal]
7. Na próxima aula, a gente preenche o login. [passo]
8. Te vejo lá! [endcard]

## Aula 14: fill - preenchendo campos
1. Hoje o robô digita usuário e senha. [bigtext]
2. Mas antes: como ele sabe qual é o campo? Olha o site: dentro do primeiro campo está escrito Username, em cinza. Isso se chama placeholder. [tela]
3. E o Playwright acha campos exatamente por isso: page ponto getByPlaceholder, e entre aspas Username. [editor]
4. Depois, ponto fill, e o que digitar: standard underline user, o usuário de treino que o próprio site mostra embaixo. [tela]
5. O fill apaga o que tiver no campo e digita o texto novo. [cards]
6. A senha é igual: getByPlaceholder Password, fill secret underline sauce. [editor]
7. Roda com o headed e olha o robô digitando. [tela]
8. Na próxima aula, a gente clica em Login e confere se deu certo. [passo]
9. Te vejo lá! [endcard]

## Aula 15: click e expect - conferindo o resultado
1. Hoje o teste fica completo: clicar e conferir. [bigtext]
2. Pra achar o botão, a gente usa o getByRole: o papel dele é button, de botão, e o nome é o texto escrito nele, Login. [tela]
3. Digita: await page ponto getByRole, abre parênteses, aspas button, vírgula, chaves, name dois pontos, aspas Login, fecha tudo, ponto click. [editor]
4. Agora a parte mais importante do teste: a conferência. Se logou, o endereço do site muda pra inventory. [tela]
5. Então: await expect, abre parênteses, page, fecha parênteses, ponto toHaveURL, e entre barras, inventory. Essas barras criam uma busca por padrão. Nesse caso, a gente está dizendo que a URL precisa ter a palavra inventory em algum lugar. [editor]
6. Sem o expect, o teste só clica. Ele não confere nada, e passaria até se o login desse errado. [compare]
7. Roda. Passou! Esse é o seu primeiro teste completo: abre, preenche, clica e confere. [cards]
8. Te vejo lá! [endcard]

## Aula 16: Os expect mais usados
1. O expect é o coração do teste, então vale conhecer os mais usados. [bigtext]
2. toHaveURL você já conhece: confere o endereço. [editor]
3. toBeVisible confere se algo está aparecendo na tela. Por exemplo, o título Products: await expect, page ponto getByText Products, ponto toBeVisible. [editor]
4. toContainText confere se um texto aparece no meio de outro. O nome do primeiro produto contém Backpack: await expect, e ponto toContainText Backpack. [editor]
5. E toHaveCount confere quantos existem. Na loja tem seis botões Add to cart, um pra cada produto: await expect, getByRole button Add to cart, ponto toHaveCount seis. [editor]
6. Tem também o toHaveText, que confere o texto exato, e o not, que faz o contrário de qualquer um. Todos estão na sua colinha. [cards]
7. E um detalhe que faz o Playwright brilhar: os expect do Playwright esperam automaticamente por alguns segundos até a condição ficar verdadeira. Por padrão, esse tempo é de até cinco segundos. [bigtext]
8. Roda, e tudo passa. No próximo módulo, a gente aprende a achar qualquer elemento, e eu te mostro um truque em que o Playwright escreve o código pra você. [terminal]
9. Te vejo lá! [endcard]

# Roteiros aprovados · Módulo 9 (gerado do roteiro_playwright_m9.py)

## Aula 43: Git - salvando o projeto
1. O Git é um programa que guarda versões do seu projeto. Como pontos de salvamento num jogo. [cards]
2. No terminal do VS Code: git init. Init é iniciar: comece a guardar as versões desta pasta. [editor]
3. Depois: git add ponto. Add é adicionar, e o ponto quer dizer tudo: prepare todos os arquivos pro próximo salvamento. [editor]
4. Repara que o node modules, o ponto env e a pasta do login salvo não entram: o gitignore está fazendo o trabalho dele. [terminal]
5. E: git commit traço m, e uma mensagem entre aspas, tipo meu primeiro projeto Playwright. Commit é o salvamento, e o traço m é a mensagem dele. [editor]
6. Se for a primeira vez que você usa o Git, ele pode pedir seu nome e seu e-mail. São dois comandos: git config traço traço global user ponto name, e user ponto email. Depois roda o commit de novo. [terminal]
7. Pronto: o seu projeto tem o primeiro ponto de salvamento. Na próxima aula, ele vai pro GitHub. [passo]
8. Te vejo lá! [endcard]

## Aula 44: GitHub - enviando o projeto
1. O GitHub é um site que guarda projetos Git na internet. É a vitrine de quem trabalha com tecnologia. [bigtext]
2. Cria uma conta no github ponto com, se ainda não tiver. Depois clica em New repository, dá o nome e cria, sem marcar nenhuma opção. [github]
3. O GitHub mostra os comandos. No terminal: git branch traço M main. Dá o nome main pro ramo principal. [editor]
4. Depois: git remote add origin, e o endereço do seu repositório. Remote é remoto: avise o Git que existe uma cópia lá no GitHub, chamada origin. [github]
5. E o envio: git push traço u origin main. Push é empurrar: mande o projeto pro GitHub. O traço u liga a sua main com a main de lá, e nas próximas vezes basta git push. [editor]
6. Na primeira vez, o Git pode abrir o navegador pra você entrar na sua conta do GitHub. É normal: faz o login e volta pro terminal. [cards]
7. Atualiza a página do GitHub: seu projeto está lá. E repara: nem o ponto env, nem a pasta do login salvo subiram. [github]
8. Na próxima aula: os testes rodando sozinhos no GitHub. [passo]
9. Te vejo lá! [endcard]

## Aula 45: GitHub Actions - os testes rodando sozinhos
1. E se o GitHub rodasse os seus testes sozinho? É isso que o GitHub Actions faz. [bigtext]
2. O Playwright já criou esse arquivo lá no começo: ponto github, workflows, playwright ponto yml. [editor]
3. Lendo em português: quando houver um push ou um pull request na main, use uma máquina Ubuntu, instale tudo e rode os testes. Esses quandos são os gatilhos do arquivo. [traducao]
4. Só falta uma coisa: o ponto env não foi pro GitHub, então lá os testes não sabem o usuário e a senha. [cards]
5. No GitHub: Settings, Secrets and variables, Actions, New repository secret. Cria o SAUCE underline USER e o SAUCE underline PASSWORD. Secret é segredo: ninguém consegue ver o valor depois. [github]
6. No yml, no passo que roda os testes, um env que entrega esses segredos pros testes. [editor]
7. Manda pro GitHub com git push e abre a aba Actions: olha os testes rodando lá. [gh_actions]
8. Verde: passou. E no fim tem o relatório pra baixar, porque esse arquivo tem o passo que guarda ele. [gh_actions]
9. Fechamos o projeto! Tem bônus: testes de API. [passo]
10. Te vejo lá! [endcard]

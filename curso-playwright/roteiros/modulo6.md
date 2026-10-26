# Roteiros aprovados · Módulo 6 (gerado do roteiro_playwright_m6.py)

## Aula 26: Lendo o erro
1. O teste falhou. Calma: ler o erro fica muito mais fácil quando você sabe onde olhar. [bigtext]
2. Vamos quebrar de propósito: na conferência da mochila, troca Backpack por Mochila. [editor]
3. Roda. Falhou. [editor]
4. Vamos ler de cima pra baixo. Primeiro: qual teste falhou, e em qual arquivo e linha. [terminal]
5. Depois: Expected, o que você esperava, e Received, o que ele encontrou. [terminal]
6. Depois, o pedaço do seu código, com uma setinha apontando a linha exata. [terminal]
7. E o call log, que mostra tudo o que ele tentou. Repara: ele ficou tentando por cinco segundos antes de desistir. [terminal]
8. Três coisas que você vai ver bastante: timeout, alguma coisa que o teste esperava não aconteceu dentro do tempo. Strict mode violation, o seletor achou mais de um elemento quando precisava de um só. E Expected e Received, o teste esperava um valor e encontrou outro. [cards]
9. Volta pra Backpack e roda: passou. [editor]
10. Na próxima aula: um jeito muito mais visual de rodar os testes. [passo]
11. Te vejo lá! [endcard]

## Aula 27: UI Mode
1. Existe um jeito bem mais visual de rodar testes: o UI Mode. [bigtext]
2. No terminal: npx playwright test traço traço ui. [editor]
3. Abre uma janela com todos os seus testes do lado esquerdo. Clica no play. [pw_ui]
4. Ele roda e mostra cada passo. Clica num passo, e a tela mostra como a página estava naquele momento. [pw_ui]
5. Dá pra voltar no tempo: ver a página antes e depois de cada clique. [pw_ui]
6. E tem o watch, que quer dizer vigiar, aquele ícone de olho: você salva o arquivo e o teste roda de novo sozinho. [pw_ui]
7. É um dos jeitos mais confortáveis de escrever um teste novo: escreve, salva, e vê na hora. [bigtext]
8. Na próxima aula: o rastro completo de um teste. [passo]
9. Te vejo lá! [endcard]

## Aula 28: Trace Viewer
1. E quando o teste falha no GitHub, onde você não estava olhando? Pra isso existe o trace. [bigtext]
2. Trace quer dizer rastro: é um arquivo com tudo o que aconteceu no teste. [traducao]
3. Roda com traço traço trace on. [editor]
4. Abre o relatório e clica no trace do teste. [pw_relatorio]
5. Em cima, a linha do tempo. Na esquerda, os passos. No meio, a página. E embaixo, o console e a rede. [pw_trace]
6. No config já vem trace on first retry: quando um teste falha e roda de novo, o trace dessa segunda tentativa é gravado. No GitHub o config já tenta de novo, então lá isso acontece sozinho. Na sua máquina, sem nova tentativa, use o traço traço trace on. [editor]
7. Na próxima aula: pausando o teste no meio. [passo]
8. Te vejo lá! [endcard]

## Aula 29: Modo debug e page.pause
1. Às vezes você quer ver o teste devagar, um passo de cada vez. [bigtext]
2. No terminal: npx playwright test traço traço debug. [editor]
3. Ele abre o navegador e para antes do primeiro passo. [pw_codegen]
4. No Inspector, o botão step over executa um passo por vez. Olha: preenche, para. Preenche, para. Clica, para. [pw_codegen]
5. Outra forma, pra usar na sua máquina enquanto escreve o teste: page ponto pause no meio do código. [editor]
6. Pause é pausar: rodando com o navegador aparecendo, o teste para exatamente ali e abre o Inspector. [pw_codegen]
7. É uma ferramenta de desenvolvimento: lembra de tirar o pause depois, senão o teste fica parado esperando você. [cards]
8. Na próxima aula: print e vídeo automático quando o teste falha. [passo]
9. Te vejo lá! [endcard]

## Aula 30: Print e vídeo quando o teste falha
1. E se o próprio teste tirasse um print e gravasse um vídeo quando falha? Ele faz isso. [bigtext]
2. No config, dentro do use, adiciona duas linhas: screenshot only on failure, e video retain on failure. [editor]
3. Traduzindo: screenshot, print, só quando falhar. Video retain on failure: o vídeo é gravado durante o teste, e guardado só se ele falhar. [traducao]
4. Quebra o teste de novo e roda. [editor]
5. Abre o relatório: lá está o print do momento do erro e o vídeo do teste inteiro. [pw_relatorio]
6. E por que só quando falha? Porque gravar sempre deixa tudo mais lento e enche o computador de arquivo. [cards]
7. Desfaz o erro e fechamos o módulo de debug. [passo]
8. Te vejo lá! [endcard]

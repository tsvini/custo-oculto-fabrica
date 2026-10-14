# Fábrica Custo Oculto

Roteiro entra, vídeo pronto sai. Roda sozinha nos servidores do GitHub (grátis).

**O que ela faz em cada vídeo**
1. **Mídia:** tira o print da manchete de cada matéria citada e baixa os clipes de apoio do Pexels. Quando um site bloqueia o print, a cena mostra a manchete desenhada no estilo de recorte de jornal.
2. **Voz:** narra frase por frase com o Google Cloud (vozes Chirp 3 HD). Cada frase tem o tempo exato, então legenda e cenas ficam sincronizadas. Frases repetidas não são cobradas de novo.
3. **Vídeo:** monta o longo (1920×1080) e os Shorts (1080×1920) com o mesmo motor do Estúdio. O som sai em −14 LUFS, o padrão do YouTube.
4. **Entrega:** MP4, legenda `.srt`, capítulos, título, descrição, tags e duas miniaturas para o Teste A/B.

## Configuração (uma vez só)

Em **Settings → Secrets and variables → Actions → New repository secret**, crie:

| Nome | De onde vem |
|---|---|
| `GOOGLE_TTS_KEY` | console.cloud.google.com → APIs e serviços → Credenciais → Chave de API (restrita à Cloud Text-to-Speech API) |
| `PEXELS_KEY` | pexels.com/api (opcional; sem ela, as cenas de clipe usam texto animado) |

## Como gerar um vídeo (voz gravada por você)

1. Abra `projetos/<nome>/NARRACAO.md`. Ele tem o texto exato de cada arquivo: `parte1.mp3` … `parteN.mp3` (longo) e `short1.mp3`… (Shorts).
2. Grave cada bloco num arquivo separado com esse nome (mp3, wav, m4a ou ogg).
3. No GitHub, entre em `projetos/<nome>/`, clique em **Add file → Upload files**, escreva `audio/` antes do nome se a pasta ainda não existir, ou arraste os arquivos dentro da pasta `audio`. **Envie todos de uma vez** (um commit só).
4. A fábrica começa sozinha. Ela ouve cada áudio, acha onde cada frase começa e termina e monta legenda e cenas no tempo certo.
5. Em uns 20–30 minutos, abra a execução na aba **Actions** e baixe o pacote em **Artifacts** (fica 14 dias).

Se faltar algum áudio, aquele vídeo é pulado e o resumo da execução diz qual arquivo falta. Se a leitura fugir muito do texto, o resumo avisa também.

Para gerar de novo sem trocar os áudios: **Actions → Gerar vídeo → Run workflow** (projeto `kolynos`, modo `gravada`). O modo `teste` monta o vídeo com voz falsa, só para conferir as cenas.

Para criar o NARRACAO.md de um projeto novo: `python -m fabrica.narracao <nome>`.

**Para trocar um print:** coloque a imagem em `projetos/<nome>/midia/print01.png`, com o mesmo nome da cena. Arquivo enviado à mão sempre tem prioridade.

## TikTok

Cada projeto pode ter `script.tiktoks`: vídeos verticais de 70–90 s (o Programa de Recompensas só conta vídeos com mais de 1 minuto). Legenda e marca ficam fora das áreas que o TikTok cobre (botões à direita, texto embaixo).

1. O texto de cada um está em `NARRACAO.md`, nos blocos `tiktok1.mp3`, `tiktok2.mp3`…
2. Grave e envie os arquivos para `projetos/<nome>/audio/`. Se o envio tiver só áudios de TikTok, a fábrica gera só os TikToks.
3. O pacote traz `<nome>_tiktokN.mp4` e `publicar_tiktokN.txt`, com a legenda do post, as hashtags e o produto para marcar no TikTok Shop.

## Canal em inglês (Hidden Cost) e links de afiliado

- **Idioma:** no `projeto.json`, `"idioma": "en"` manda o caso para o **Hidden Cost** (@HiddenCostCases). Sem esse campo é português (Custo Oculto). A narração do ElevenLabs, o reconhecimento de fala, a legenda, os textos fixos e a publicação seguem o idioma. Cada canal tem a própria agenda.
- **Abertura:** a intro gravada do canal fica em `canal/intro.mp3` (pt) e `canal/intro_en.mp3` (en). Se não existir intro no idioma, a frase de abertura é narrada junto com o resto.
- **Publicação:** o Hidden Cost usa o secret `YT_REFRESH_TOKEN_EN`. Sem ele, os vídeos em inglês esperam na fila.
- **Afiliados:** em `meta.afiliados`, uma lista de `{"titulo": "...", "busca": "termos da busca"}` ou `{"titulo": "...", "asin": "B0..."}`. A fábrica monta o link com a tag certa (`custooculto-20` na Amazon Brasil, `hiddencost-20` na Amazon EUA) e coloca no fim da descrição do longo, com o aviso obrigatório. Para escolher o lugar, escreva `[AFILIADOS]` na descrição.

## Vozes

Padrão: **sua voz gravada** (modo `gravada`). As trocas de cena não têm mais o "bum" de impacto; só a trilha de fundo baixa.

Alternativa sintética: Google Chirp 3 HD com `modo: google` + secret `GOOGLE_TTS_KEY` (exige conta com cartão).

## Custos

- **GitHub Actions:** grátis até 2.000 minutos por mês em repositório privado, o bastante para umas 60 gerações.

## Rodar no próprio computador (opcional)

```
pip install -r requirements.txt && python -m playwright install chromium
python -m fabrica.gerar kolynos --modo teste
```

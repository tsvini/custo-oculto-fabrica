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

## Como gerar um vídeo

**Automático:** basta salvar um `projetos/<nome>/projeto.json` novo ou alterado no repositório. A fábrica começa sozinha.

**Pelo botão:** aba **Actions** → **Gerar vídeo** → **Run workflow**. Preencha:
- **projeto:** o nome da pasta, ex.: `kolynos`
- **formato:** `tudo`, `longo`, `shorts` ou `short1`
- **voz:** opcional, troca a voz só desta vez
- **modo:** `google` usa a voz de verdade; `teste` usa uma voz falsa e não gasta nada

Um longo de 7 minutos leva uns 20–30 minutos. Ao final, abra a execução e baixe o pacote em **Artifacts**. Ele fica disponível por 14 dias.

**Para trocar um print:** coloque a imagem em `projetos/<nome>/midia/print01.png`, com o mesmo nome da cena. Arquivo enviado à mão sempre tem prioridade.

## Vozes

A voz fica em `"voz": {"nome": "pt-BR-Chirp3-HD-Charon", "velocidade": 1.05}` dentro do `projeto.json`.

Vozes masculinas: Charon, Orus, Algenib, Iapetus, Schedar, Fenrir, Puck, Enceladus, Achird, Algieba, Alnilam, Rasalgethi, Sadachbia, Sadaltager, Umbriel, Zubenelgenubi.

Vozes femininas: Kore, Aoede, Leda, Zephyr, Despina, Erinome, Gacrux, Achernar, Autonoe, Callirrhoe, Laomedeia, Pulcherrima, Sulafat, Vindemiatrix.

O nome completo é sempre `pt-BR-Chirp3-HD-<Nome>`.

## Custos

- **Google TTS:** grátis até 1 milhão de caracteres por mês. Um longo tem uns 5 mil.
- **GitHub Actions:** grátis até 2.000 minutos por mês em repositório privado, o bastante para umas 60 gerações.

## Rodar no próprio computador (opcional)

```
pip install -r requirements.txt && python -m playwright install chromium
python -m fabrica.gerar kolynos --modo teste
```

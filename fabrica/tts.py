"""Narração frase a frase. Motores:
- edge: vozes neurais do Microsoft Edge (grátis, sem conta, sem cartão). Padrão.
- google: Google Cloud Text-to-Speech (Chirp 3 HD), precisa de GOOGLE_TTS_KEY.
- teste: voz falsa, só para conferir a montagem.

Gerar frase a frase dá o tempo exato de cada frase (legenda e cenas sincronizadas
sem adivinhação) e permite cache: refazer um vídeo não gasta caracteres de novo.
"""
import asyncio, base64, hashlib, io, json, os, subprocess, tempfile, time, wave
import urllib.request, urllib.error
import numpy as np

SR = 48000
CACHE = os.environ.get("TTS_CACHE", ".cache/tts")
API = "https://texttospeech.googleapis.com/v1/text:synthesize"

VOZ_PADRAO = {"nome": "pt-BR-Chirp3-HD-Charon", "velocidade": 1.05, "pausa": 0.24, "pausa_virgula": 0.12}


VOZ_EDGE_PADRAO = "pt-BR-AntonioNeural"


class ErroVoz(RuntimeError):
    pass


def _wav_to_np(data):
    with wave.open(io.BytesIO(data)) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if sw != 2:
        raise ErroVoz(f"formato de áudio inesperado ({sw * 8} bits)")
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        n2 = int(round(len(x) * SR / sr))
        x = np.interp(np.linspace(0, len(x) - 1, n2), np.arange(len(x)), x).astype(np.float32)
    return x


def _np_to_wav(x, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def _google(text, voz, key):
    lang = "-".join(voz["nome"].split("-")[:2])
    body = {"input": {"text": text}, "voice": {"languageCode": lang, "name": voz["nome"]},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR, "speakingRate": float(voz.get("velocidade", 1.0))}}
    data = json.dumps(body).encode()
    for tent in range(6):
        req = urllib.request.Request(API + "?key=" + key, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return base64.b64decode(json.load(r)["audioContent"])
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf8", "replace")[:400]
            if e.code in (429, 500, 502, 503, 504) and tent < 5:
                time.sleep(2 * (tent + 1)); continue
            if e.code in (400, 403):
                raise ErroVoz(f"Google TTS recusou ({e.code}). Confira a chave GOOGLE_TTS_KEY, se a API Text-to-Speech está ativada e o nome da voz '{voz['nome']}'. Detalhe: {msg}")
            raise ErroVoz(f"Google TTS erro {e.code}: {msg}")
        except urllib.error.URLError as e:
            if tent < 5:
                time.sleep(2 * (tent + 1)); continue
            raise ErroVoz(f"sem conexão com o Google TTS: {e}")


def _edge(text, voz):
    import edge_tts
    nome = voz["nome"] if "Neural" in voz["nome"] else VOZ_EDGE_PADRAO
    pct = int(round((float(voz.get("velocidade", 1.0)) - 1) * 100))
    rate = f"{pct:+d}%"
    with tempfile.TemporaryDirectory() as d:
        mp3, wav = os.path.join(d, "f.mp3"), os.path.join(d, "f.wav")
        for tent in range(6):
            try:
                asyncio.run(edge_tts.Communicate(text, nome, rate=rate).save(mp3))
                break
            except Exception as e:
                if tent == 5:
                    raise ErroVoz(f"voz do Edge falhou ({nome}): {e}")
                time.sleep(3 * (tent + 1))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", wav], check=True)
        with open(wav, "rb") as f:
            return f.read()


def _teste(text, voz):
    """Voz falsa para testar a fábrica sem internet: ruído com ritmo de fala."""
    rng = np.random.default_rng(int(hashlib.md5(text.encode()).hexdigest()[:8], 16))
    dur = max(0.6, len(text) / 15.5 / float(voz.get("velocidade", 1.0)))
    n = int(dur * SR); t = np.arange(n) / SR
    env = 0.5 + 0.5 * np.sin(2 * np.pi * 4.2 * t + rng.uniform(0, 6)) ** 2
    x = (rng.standard_normal(n) * 0.05 + 0.12 * np.sin(2 * np.pi * 140 * t)) * env
    return np.concatenate([np.zeros(int(0.12 * SR)), x, np.zeros(int(0.2 * SR))]).astype(np.float32)


def _trim(x, thr_db=-45, keep=0.03):
    win = SR // 100
    n = len(x) // win
    if n == 0:
        return x
    rms = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    on = np.where(20 * np.log10(rms) > thr_db)[0]
    if not len(on):
        return x
    a = max(0, on[0] * win - int(keep * SR)); b = min(len(x), (on[-1] + 1) * win + int(keep * SR))
    return x[a:b]


class Narrador:
    def __init__(self, voz=None, modo=None):
        self.voz = dict(VOZ_PADRAO, **(voz or {}))
        self.key = os.environ.get("GOOGLE_TTS_KEY", "").strip()
        self.modo = modo or ("google" if self.key else "edge")
        if self.modo == "edge" and "Neural" not in self.voz["nome"]:
            self.voz["nome"] = VOZ_EDGE_PADRAO
        if self.modo == "google" and not self.key:
            raise ErroVoz("falta a chave GOOGLE_TTS_KEY. No GitHub: Settings → Secrets and variables → Actions → New repository secret.")
        self.chars = 0      # caracteres cobrados nesta execução
        self.cache_hits = 0

    def frase(self, text):
        k = hashlib.sha1(json.dumps([self.modo, self.voz["nome"], self.voz.get("velocidade"), text]).encode()).hexdigest()
        path = os.path.join(CACHE, k[:2], k + ".wav")
        if os.path.exists(path):
            self.cache_hits += 1
            with open(path, "rb") as f:
                return _wav_to_np(f.read())
        if self.modo == "google":
            x = _wav_to_np(_google(text, self.voz, self.key)); self.chars += len(text)
        elif self.modo == "edge":
            x = _wav_to_np(_edge(text, self.voz))
        else:
            x = _teste(text, self.voz)
        x = _trim(x)
        _np_to_wav(x, path)
        return x

    def parte(self, frases, saida_wav):
        """Narra uma lista de frases, junta com pausas e devolve os tempos [ini, fim] de cada uma."""
        lead = 0.15
        pedacos = [np.zeros(int(lead * SR), np.float32)]; t = lead; tempos = []
        for i, txt in enumerate(frases):
            x = self.frase(txt)
            tempos.append([round(t, 3), round(t + len(x) / SR, 3)])
            pedacos.append(x); t += len(x) / SR
            if i < len(frases) - 1:
                p = self.voz["pausa"] if txt.rstrip()[-1:] in ".!?…" else self.voz["pausa_virgula"]
                pedacos.append(np.zeros(int(p * SR), np.float32)); t += p
        pedacos.append(np.zeros(int(0.25 * SR), np.float32))
        y = np.concatenate(pedacos)
        # volume uniforme: RMS da fala em -18 dBFS, com limitador suave
        win = SR // 100; n = len(y) // win
        rms = np.sqrt((y[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
        fala = rms[20 * np.log10(rms) > -45]
        if len(fala):
            y = y * (10 ** (-18 / 20) / np.sqrt((fala ** 2).mean()))
            a = np.abs(y); m = a > 0.7
            y[m] = np.sign(y[m]) * (0.7 + 0.2 * np.tanh((a[m] - 0.7) / 0.2))
        _np_to_wav(y.astype(np.float32), saida_wav)
        return tempos, len(y) / SR

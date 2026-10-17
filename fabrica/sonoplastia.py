"""Sonoplastia dos Shorts com som de verdade e validação por IA.

1. Cada cena traz "sons": [{"busca": "supermarket ambience", "tipo": "amb"|"fx", "palavra"?: "bilhão", "vol"?: 0.3}]
   - amb = ambiente que cobre a cena inteira (entra e sai suave, abaixa quando a voz fala)
   - fx  = efeito pontual, no instante da palavra (ou no início da cena)
2. Busca as gravações reais mais bem avaliadas no Freesound (licença CC0: uso livre, comercial, sem crédito).
3. O Gemini (que escuta áudio) ouve os candidatos e escolhe o que mais combina com a cena.
4. Mixa: voz + trilha + ambientes + efeitos, com volume normalizado.
5. O Gemini assiste o vídeo pronto, dá nota de 0 a 10 e aponta problemas por evento; a fábrica corrige
   (remove, sobe/abaixa volume, adianta/atrasa) e remixa até nota >= 9 (no máximo 3 rodadas).
O relatório fica em previas/som_<nome>.json.
"""
import base64
import json
import math
import os
import re
import subprocess
import tempfile
import time

import numpy as np
import requests

from . import som

SR = som.SR
FS = "https://freesound.org/apiv2"
GEM = "https://generativelanguage.googleapis.com/v1beta/models"
MODELOS = [m for m in [os.environ.get("GEMINI_MODELO"), "gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-flash"] if m]


def log(*a):
    print(*a, flush=True)


# ---------------- Freesound ----------------
def candidatos(busca, tipo, n=3):
    """Tenta a busca completa e, se não achar, versões mais simples (ex.: 'object dropped in metal trash can' → 'trash can')."""
    w = busca.split(); tentativas = [busca, " ".join(w[-2:]), " ".join(w[:2]), w[-1]]
    vistos = set()
    for q in tentativas:
        if not q or q in vistos:
            continue
        vistos.add(q)
        r = _candidatos(q, tipo, n)
        if r:
            if q != busca:
                log(f"  freesound '{busca}': usando '{q}'")
            return r
    return []


def _candidatos(busca, tipo, n=3):
    key = os.environ.get("FREESOUND_KEY", "").strip()
    if not key:
        return []
    dur = "[3 TO 180]" if tipo == "amb" else "[0.1 TO 8]"
    params = {"query": busca, "filter": f'license:"Creative Commons 0" duration:{dur}', "sort": "rating_desc",
              "fields": "id,name,duration,previews,avg_rating,num_downloads,num_ratings,tags", "page_size": 15, "token": key}
    try:
        r = requests.get(f"{FS}/search/text/", params=params, timeout=30); r.raise_for_status()
        res = r.json().get("results", [])
    except Exception as e:
        log(f"  freesound '{busca}': falhou ({str(e)[:120]})"); return []
    # popularidade e avaliação juntas (som que muita gente baixou e aprovou)
    res = [x for x in res if x.get("previews")]
    res.sort(key=lambda x: -(x.get("avg_rating") or 0) * math.log(2 + (x.get("num_downloads") or 0)) * min(1, (x.get("num_ratings") or 0) / 3))
    out = []
    for x in res[:n]:
        try:
            b = requests.get(x["previews"]["preview-hq-mp3"], timeout=60).content
            out.append({"id": x["id"], "nome": x["name"], "mp3": b, "dur": x.get("duration")})
        except Exception:
            pass
    return out


def _decodifica(mp3):
    with tempfile.TemporaryDirectory() as d:
        a = os.path.join(d, "a.mp3"); o = os.path.join(d, "a.f32")
        open(a, "wb").write(mp3)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a, "-ac", "1", "-ar", str(SR), "-f", "f32le", o], check=True)
        return np.fromfile(o, dtype=np.float32).astype(np.float64)


def _corta_silencio(x, limiar=0.02):
    idx = np.where(np.abs(x) > limiar * (np.abs(x).max() + 1e-9))[0]
    return x[idx[0]:idx[-1] + 1] if len(idx) else x


# ---------------- Gemini ----------------
def _gemini(partes, json_saida=True):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    corpo = {"contents": [{"parts": partes}]}
    if json_saida:
        corpo["generationConfig"] = {"responseMimeType": "application/json", "temperature": 0.2}
    for m in MODELOS:
        for tent in range(4):
            try:
                r = requests.post(f"{GEM}/{m}:generateContent?key={key}", json=corpo, timeout=300)
                if r.status_code == 429:
                    time.sleep(10 * (tent + 1)); continue
                if r.status_code == 404:
                    break
                r.raise_for_status()
                partes_r = r.json()["candidates"][0]["content"]["parts"]
                txt = "".join(x.get("text", "") for x in partes_r if not x.get("thought"))
                if not json_saida:
                    return txt
                txt = re.sub(r"^```(json)?|```$", "", txt.strip()).strip()
                v = json.loads(txt)
                if isinstance(v, list):
                    v = v[0] if v and isinstance(v[0], dict) else {"itens": v}
                return v
            except Exception as e:
                log(f"  gemini {m}: {str(e)[:160]}"); time.sleep(5)
    return None


def escolhe(busca, cena, cands):
    """O Gemini ouve os candidatos e escolhe o melhor (ou nenhum). Desligado por padrão: estoura o limite do plano grátis."""
    if len(cands) <= 1 or not os.environ.get("GEMINI_API_KEY") or not os.environ.get("SOM_ESCOLHA_IA"):
        return cands[0] if cands else None
    partes = [{"text": (f"Você é sonoplasta de vídeos curtos virais. Cena: {cena}. Som pedido: '{busca}'. "
                        f"Ouça os {len(cands)} candidatos na ordem e escolha o que soa mais profissional e mais combina com a cena. "
                        "Responda JSON: {\"melhor\": índice começando em 0, ou -1 se nenhum servir, \"motivo\": \"...\"}")}]
    for c in cands:
        partes.append({"inline_data": {"mime_type": "audio/mpeg", "data": base64.b64encode(c["mp3"]).decode()}})
    r = _gemini(partes) or {}
    i = r.get("melhor", 0) if isinstance(r, dict) else 0
    if isinstance(i, int) and 0 <= i < len(cands):
        return cands[i]
    return None if i == -1 else cands[0]


# ---------------- mixagem ----------------
def _rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-9)


def mixar(voz, eventos, trilha_arr=None, vol_trilha=0.32):
    n = len(voz); mix = voz.copy()
    env = np.sqrt(som._lp(voz ** 2, 0.0008)); env = env / (env.max() + 1e-9)
    duck = 1 - 0.45 * np.clip(env * 3, 0, 1)  # abaixa o que não é voz quando a voz fala
    alvo_voz = _rms(voz[np.abs(voz) > 0.02]) if np.any(np.abs(voz) > 0.02) else 0.1
    if trilha_arr is not None:
        mix += vol_trilha * trilha_arr[:n] * duck[:len(trilha_arr[:n])]
    for ev in eventos:
        a = ev.get("audio")
        if a is None or ev.get("removido"):
            continue
        i0 = int(max(0, ev["t0"]) * SR)
        if i0 >= n:
            continue
        if ev["tipo"] == "amb":
            m = min(n - i0, int(max(0.5, ev["t1"] - ev["t0"]) * SR))
            base = np.tile(a, int(m / max(1, len(a))) + 1)[:m]
            f = min(int(0.4 * SR), m // 3); rampa = np.ones(m)
            rampa[:f] = np.linspace(0, 1, f); rampa[m - f:] = np.linspace(1, 0, f)
            s = base / _rms(base) * alvo_voz * ev.get("vol", 0.18) * rampa * duck[i0:i0 + m]
        else:
            s = a[: int(6 * SR)]; m = min(len(s), n - i0)
            s = s[:m] / (np.abs(s).max() + 1e-9) * ev.get("vol", 0.5) * (np.abs(voz).max() + 1e-9)
        mix[i0:i0 + m] += s
    pico = np.abs(mix).max()
    return mix * (0.97 / pico) if pico > 0.97 else mix


def _escreve(video, mix, saida):
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.f32"); mix.astype(np.float32).tofile(wav)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", wav,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", saida], check=True)


def avalia(video, eventos, roteiro):
    """O Gemini assiste (versão leve do vídeo) e dá nota ao som, com problemas por evento."""
    if not os.environ.get("GEMINI_API_KEY"):
        return None
    with tempfile.TemporaryDirectory() as d:
        leve = os.path.join(d, "l.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-vf", "scale=360:-2,fps=12", "-c:v", "libx264", "-b:v", "500k",
                        "-c:a", "aac", "-b:a", "128k", leve], check=True)
        dado = base64.b64encode(open(leve, "rb").read()).decode()
    lista = "\n".join(f"{k}: {e['t0']:.1f}s–{e['t1']:.1f}s {e['tipo']} '{e['busca']}' vol {e.get('vol')}" + (" (removido)" if e.get("removido") else "")
                      for k, e in enumerate(eventos))
    p = (f"Você é editor e sonoplasta sênior de Shorts/TikToks virais em português. Assista e ESCUTE com atenção este vídeo.\n"
         f"Roteiro: {roteiro}\nEventos de som colocados (índice: tempo, tipo, descrição, volume):\n{lista}\n\n"
         "Avalie SÓ o som (efeitos, ambientes, trilha e equilíbrio com a narração): cada som combina com o que aparece e com o que é dito? "
         "entra no momento certo? está alto ou baixo demais? cobre a voz? soa barato/artificial? falta algum som óbvio?\n"
         "Responda JSON: {\"nota\": 0-10, \"resumo\": \"...\", \"problemas\": [{\"evento\": índice, \"problema\": \"...\", "
         "\"acao\": \"remover\"|\"mais_alto\"|\"mais_baixo\"|\"adiantar\"|\"atrasar\", \"segundos\": número (para adiantar/atrasar)}], "
         "\"faltando\": [{\"t\": segundos, \"busca\": \"descrição curta em inglês para banco de sons\", \"tipo\": \"fx\"|\"amb\"}]}")
    return _gemini([{"text": p}, {"inline_data": {"mime_type": "video/mp4", "data": dado}}])


def aplica(eventos, aval):
    for pr in (aval or {}).get("problemas", []):
        k = pr.get("evento")
        if not isinstance(k, int) or not 0 <= k < len(eventos):
            continue
        e = eventos[k]; a = pr.get("acao")
        if a == "remover":
            e["removido"] = True
        elif a == "mais_alto":
            e["vol"] = round(min(1.0, e.get("vol", 0.4) * 1.4), 3)
        elif a == "mais_baixo":
            e["vol"] = round(e.get("vol", 0.4) * 0.6, 3)
        elif a in ("adiantar", "atrasar"):
            s = float(pr.get("segundos") or 0.2) * (-1 if a == "adiantar" else 1)
            e["t0"] = max(0, e["t0"] + s); e["t1"] = max(e["t0"] + 0.3, e["t1"] + s)


BIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor", "sons", "freesound")


def busca_audio(ev, cena_txt, cache):
    """Pega o som na biblioteca guardada (motor/sons/freesound) ou busca no Freesound e guarda para os próximos vídeos."""
    q = ev["busca"]; slug = re.sub(r"[^a-z0-9]+", "_", q.lower()).strip("_")[:60] + "_" + ev.get("tipo", "fx")
    arq = os.path.join(BIB, slug + ".mp3")
    if q not in cache:
        if os.path.exists(arq):
            info = json.load(open(arq + ".json", encoding="utf8")) if os.path.exists(arq + ".json") else {"id": "?", "nome": slug}
            cache[q] = (_corta_silencio(_decodifica(open(arq, "rb").read())), info)
        else:
            cands = candidatos(q, ev["tipo"], n=3 if os.environ.get("SOM_ESCOLHA_IA") else 1)
            c = escolhe(q, cena_txt, cands)
            if c:
                os.makedirs(BIB, exist_ok=True); open(arq, "wb").write(c["mp3"])
                json.dump({"id": c["id"], "nome": c["nome"]}, open(arq + ".json", "w", encoding="utf8"), ensure_ascii=False)
                cache[q] = (_corta_silencio(_decodifica(c["mp3"])), {"id": c["id"], "nome": c["nome"]})
            else:
                cache[q] = (None, None)
    ev["audio"], c = cache[q]
    ev["fonte"] = f"freesound #{c['id']} {c['nome']}" if c else None


def processar(video, eventos, trilha=None, roteiro="", relatorio=None, rodadas=2, meta=9.5):
    """eventos: [{t0, t1, tipo, busca, vol, cena}] já com tempos absolutos. Troca o áudio do vídeo."""
    voz = som._le(video); n = len(voz)
    trilha_arr = None
    if trilha:
        base = som._arquivo("trilha_" + trilha)
        if base is not None and len(base) > SR:
            tr = np.tile(base, n // len(base) + 1)[:n]; t = np.arange(n) / SR; dur = n / SR
            trilha_arr = tr / (np.abs(base).max() + 1e-9) * np.clip(np.minimum(t / 1.0, (dur - t) / 1.2), 0, 1)
    cache = {}
    for ev in eventos:
        if ev.get("vol") is None:
            ev["vol"] = 0.18 if ev.get("tipo") == "amb" else 0.5
        if ev.get("t1") is None:
            ev["t1"] = ev["t0"] + 3
        busca_audio(ev, ev.get("cena", ""), cache)
    hist = []; melhor = None
    with tempfile.TemporaryDirectory() as d:
        for rodada in range(1, rodadas + 1):
            tmp = os.path.join(d, f"r{rodada}.mp4")
            _escreve(video, mixar(voz, eventos, trilha_arr), tmp)
            av = avalia(tmp, eventos, roteiro)
            nota = (av or {}).get("nota")
            hist.append({"rodada": rodada, "nota": nota, "avaliacao": av,
                         "eventos": [{k: v for k, v in e.items() if k != "audio"} for e in eventos]})
            log(f"  som rodada {rodada}: nota {nota} · {(av or {}).get('resumo', 'sem avaliação')[:160]}")
            if melhor is None or (nota or 0) > (melhor[0] or 0):
                melhor = (nota, tmp)
            if av is None or (nota or 0) >= meta:
                break
            aplica(eventos, av)
            for f in ((av or {}).get("faltando", []) if os.environ.get("SOM_ACEITA_SUGESTAO") else [])[:4]:  # som que o avaliador sentiu falta (desligado: menos é mais)
                try:
                    ev = {"t0": float(f["t"]), "t1": float(f["t"]) + 3, "tipo": f.get("tipo", "fx"), "busca": f["busca"], "cena": "sugerido pelo avaliador"}
                    ev["vol"] = 0.18 if ev["tipo"] == "amb" else 0.45
                    busca_audio(ev, ev["cena"], cache); eventos.append(ev)
                except Exception:
                    pass
        os.replace(melhor[1], video)
    if relatorio:
        with open(relatorio, "w", encoding="utf8") as f:
            json.dump({"nota_final": melhor[0], "rodadas": hist}, f, ensure_ascii=False, indent=1)
    print(f"::notice title=Nota do som::{os.path.basename(video)}: {melhor[0]} (em {len(hist)} rodada(s))", flush=True)
    return melhor[0]

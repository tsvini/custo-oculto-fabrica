"""Confere as cenas de editor: código cortado (sem rolar) e o que está em cada linha destacada/digitada.
Uso: python ferramentas/checa_codigo.py projetos/curso-playwright-22 [...]   (mesmas contas do S.editor em motor/aula.js)"""
import json, math, sys

def cenas(p):
    d = json.load(open(p + "/projeto.json"))
    return [(i + 1, x["text"], x["scene"]) for g in d["script"]["long"]["parts"] for i, x in enumerate(g["sentences"])]

prob = 0
for p in sys.argv[1:]:
    for n, txt, s in cenas(p):
        if s.get("type") != "editor":
            continue
        L = s["codigo"].split("\n"); maxch = max(10, *(len(l) for l in L))
        W, H = 1500, 700; side = 330 if s.get("pastas") else 0
        fs = min(s.get("fonte") or (30 if len(L) > 12 else 36), (W - side - 140) / (maxch * 0.6))
        PH = round(H * 0.4) if s.get("terminal") else 0
        if PH: fs = min(fs, (H - PH - 64 - 100) / ((len(L) - 0.4) * 1.55))
        lh = fs * 1.55; cabem = math.floor((H - PH - 40 - 64 - 100) / lh) + 1
        l0 = s.get("linha0", 1)
        if len(L) > cabem and not s.get("rolar") and not s.get("rolar_depois") and not PH:
            prob += 1; print(f"{p} frase {n}: CÓDIGO CORTADO ({len(L)} linhas, cabem {cabem}) — {s.get('legenda')}")
        if fs < 14:
            prob += 1; print(f"{p} frase {n}: letra pequena demais ({fs:.1f})")
        for k in s.get("destaque", []):
            print(f"{p} frase {n}: destaque {k + l0 - 1}: {L[k - 1].strip() if 0 < k <= len(L) else '??? FORA DO ARQUIVO'}")
        if s.get("digitar") is not False and (s.get("digitar_de") or s.get("digitar_ate")):
            de, ate = s.get("digitar_de", 1), s.get("digitar_ate", len(L))
            print(f"{p} frase {n}: digita {de + l0 - 1}-{ate + l0 - 1}: {' | '.join(l.strip() for l in L[de - 1:ate])[:150]}")
print("problemas:", prob)

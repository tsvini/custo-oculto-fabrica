"""Monta projetos/explicadores/projeto.json: TikToks/Shorts no formato "explicador" (estilo cinema).

Formato inspirado no que mais roda no TikTok: gancho em segunda pessoa ("imagine que você..."), explica um conceito,
corte a cada ~1,2s (montagem de clipes livres do Pixabay), preto e branco e legenda de 1 palavra no centro.
Cada um termina puxando para o caso completo no canal.
"""
import json, os

S = lambda text, scene: {"text": text, "scene": scene}


def clip(k, busca):
    return {"type": "video", "media": "x_" + k, "search": busca, "search_en": busca}


def mont(*clips, cada=1.2):
    return {"type": "montagem", "cada": cada, "clips": list(clips), "fallback": {"type": "bigtext", "lines": []}}


C = {k: clip(k, q) for k, q in {
    "dinheiro": "counting money cash", "cofre": "bank vault", "bolsa": "stock market screen", "executivo": "businessman office night",
    "predio": "skyscraper city night", "papel": "documents papers desk", "calc": "calculator accounting", "notas": "money bills falling",
    "reuniao": "business meeting", "telefone": "man phone call office", "carro": "car night city", "policia": "police car lights",
    "loja": "shopping store", "caixa": "cash register", "planilha": "spreadsheet computer screen", "relogio": "clock ticking",
    "fila": "people queue", "multidao": "crowd city street", "banco": "bank building", "cartao": "credit card payment",
    "grafico": "chart going down", "assinatura": "signing contract", "luzes": "city lights night aerial", "chuva": "rain window night",
}.items()}

_n = [0]


def v(*buscas, cada=2.6):
    """Clipes escolhidos pelo sentido da frase; cada um fica ~2,6s na tela (1 clipe = a frase inteira)."""
    cl = []
    for q in buscas:
        _n[0] += 1; cl.append(clip(f"{_n[0]:02d}", q))
    return cl[0] if len(cl) == 1 else mont(*cl, cada=cada)


rombo = [
    S("Imagine que você é dono de uma loja que todo mundo conhece.", v("department store shoppers walking", "shopping mall crowd")),
    S("Você compra dos fornecedores e combina de pagar daqui a meses.", v("warehouse boxes delivery truck", "signing contract pen")),
    S("Só que o fornecedor não quer esperar. Então um banco paga ele agora, e você fica devendo pro banco.", v("bank building exterior", "businessman handshake money")),
    S("Isso tem nome: risco sacado. E é uma dívida.", v("accountant calculator invoice")),
    S("Agora imagine que essa dívida não aparece no seu balanço como dívida bancária.", v("financial report spreadsheet", "putting papers in drawer")),
    S("A empresa parece mais saudável do que é. O lucro parece maior. A ação sobe.", v("stock market chart rising green", "stock exchange board")),
    S("Investidor compra. Banco empresta mais. Todo mundo confia.", v("business people shaking hands", "investors meeting table")),
    S("Até o dia em que alguém olha os números de verdade.", v("auditor reviewing documents", "magnifying glass document")),
    S("E quando uma dívida escondida aparece, ela não aparece aos poucos. Aparece de uma vez.", v("stock market crash red screen")),
    S("Em janeiro de dois mil e vinte e três, a Americanas anunciou inconsistências de cerca de vinte bilhões de reais.", v("newspaper breaking news", "pile of money")),
    S("O presidente tinha nove dias no cargo e pediu demissão.", v("businessman leaving office", "empty office chair")),
    S("A ação despencou e a empresa entrou em recuperação judicial.", v("falling chart stock", "court building")),
    S("Os ex-diretores acusados negam irregularidades e não há condenação definitiva.", v("judge gavel courtroom")),
    S("Mas a conta já ficou com acionistas, bancos, fornecedores e funcionários.", v("worried office workers", "people walking city street")),
    S("O caso completo da Americanas está no canal Custo Oculto.", v("city skyline night aerial")),
]

fgc = [
    S("Imagine que um banco te oferece um CDB pagando muito mais que todos os outros.", v("bank building exterior", "man looking at phone banking app")),
    S("Cento e quarenta por cento do CDI. Bom demais pra ser verdade?", v("money growing chart", "counting money cash")),
    S("Muita gente pensa: tudo bem, se o banco quebrar, o FGC me paga.", v("man thinking at desk", "piggy bank coins")),
    S("O FGC é o Fundo Garantidor de Créditos. Ele devolve até duzentos e cinquenta mil reais por pessoa, por banco.", v("bank vault door", "stack of banknotes")),
    S("Mas de onde vem o dinheiro do FGC?", v("question mark", "man thinking")),
    S("Das contribuições dos próprios bancos. E esse custo acaba indo pra tarifa, pro juro e pra todo cliente do sistema.", v("bank fees credit card payment", "people paying at cashier")),
    S("Ou seja: quando um banco que pagava demais quebra, a conta não some. Ela se espalha.", v("money falling", "crowd city street")),
    S("Foi o que aconteceu com o Banco Master. Um milhão e seiscentas mil pessoas tinham dinheiro lá.", v("long queue people", "crowd of people")),
    S("O Banco Central decretou a liquidação, e a estimativa é que o FGC tenha que cobrir cerca de quarenta e um bilhões de reais.", v("central bank building", "pile of money")),
    S("É a maior conta da história do fundo.", v("stack of money")),
    S("Os investigados negam irregularidades e ninguém foi julgado até agora.", v("judge gavel courtroom")),
    S("Da próxima vez que um CDB pagar muito acima do mercado, lembra dessa história.", v("man looking at phone banking app")),
    S("O caso completo do Banco Master está no canal Custo Oculto.", v("city skyline night aerial")),
]

projeto = {
    "title": "Explicadores",
    "slug": "explicadores",
    "estilo": "cinema",
    "voz": {"nome": "gravada", "motor": "eleven", "eleven_voz": "Vinícius Torales"},
    "script": {"long": {"parts": []}, "shorts": [], "tiktoks": [
        {"title": "Como uma empresa esconde um rombo de bilhões", "estilo": "cinema",
         "caption": "Imagine que você é dono de uma loja que todo mundo conhece… e uma dívida não aparece no balanço. Foi assim que o caso Americanas começou. Os acusados negam.",
         "hashtags": ["#americanas", "#dinheiro", "#economia", "#financas", "#negocios"], "sentences": rombo},
        {"title": "Quem paga quando um banco quebra?", "estilo": "cinema",
         "caption": "Um CDB pagando 140% do CDI e o FGC garantindo tudo. Parece seguro. Mas quem paga essa conta? Investigados negam e ninguém foi julgado.",
         "hashtags": ["#bancomaster", "#fgc", "#cdb", "#investimentos", "#dinheiro"], "sentences": fgc},
    ]},
    "meta": {"titles": ["Explicadores"], "description": "", "tags": ["custo oculto"]},
    "notes": "Teste de formato (17/10/2026), inspirado num vídeo de 300 mil views que o Vinícius mandou: gancho 'imagine que você', P&B, corte a cada 1,2s, legenda de 1 palavra.\n"
             "FATOS: Americanas, jan/2023, inconsistências ~R$ 20 bi, presidente com 9 dias pediu demissão, RJ (já checados no caso Americanas).\n"
             "FGC: garantia de até R$ 250 mil por CPF por instituição; fundo mantido por contribuições das instituições associadas; Banco Master: 1,6 mi de investidores, conta estimada ~R$ 41 bi (já checados no caso Banco Master).",
}

d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", "explicadores")
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
json.dump(projeto, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print([sum(len(s["text"]) for s in t["sentences"]) for t in projeto["script"]["tiktoks"]])

"""Nestlé x Garoto — Short no padrão novo (cenas reais + no máx. 5 de IA, som por evento, trilha trap).
Roteiro revisado em 19/10/2026 (pesquisa + revisão da outra IA). Fatos e fontes nas notas."""
import json, os

W, G, R = "white", "gold", "red"
LOGOS = {"logo_nestle": ["File:Nestlé textlogo.svg", "File:Nestle textlogo.svg", "File:Nestlé.svg", "File:Logo Nestlé.svg", "File:Nestle logo.svg"],
         "logo_garoto": ["File:Garoto logo.svg", "File:Logo Garoto.svg", "File:Garoto.svg", "File:Chocolates Garoto logo.svg", "File:Garoto logo.png"]}
WIKI_FAB = ["Fábrica da Garoto Vila Velha", "Chocolates Garoto Vila Velha", "Garoto chocolate factory", "Fábrica de Chocolates Garoto"]
WIKI_CADE = ["Conselho Administrativo de Defesa Econômica", "CADE Brasília", "Sede do CADE"]
WIKI_SER = ["Serenata de Amor chocolate", "Serenata de Amor Garoto", "Bombom Serenata de Amor"]

S = lambda t, sc: {"text": t, "scene": sc}
fx = lambda b, pal=None, vol=None, mx=None: {k: v for k, v in {"tipo": "fx", "busca": b, "palavra": pal, "vol": vol, "max": mx}.items() if v is not None}
def im(k, **kw): return dict({"type": "image", "media": k, "z0": 1.0, "z1": 1.12, "dim": 0.35}, **kw)
def wim(k, wiki, **kw): return dict(im(k, **kw), wiki=wiki)
def mont(*clips, sobre=None, sons=None, sobre_em=None):
    d = {"type": "montagem", "auto": True, "clips": list(clips), "fallback": {"type": "bigtext", "lines": []}}
    if sobre: d["sobre"] = sobre
    if sons: d["sons"] = sons
    if sobre_em: d["sobre_em"] = sobre_em
    return d
big = lambda *ls: {"type": "bigtext", "lines": [list(l) for l in ls]}

frases = [
    S("A Nestlé comprou a Garoto em dois mil e dois.",
      {"type": "capa", "foto": "garoto_fabrica", "wiki": WIKI_FAB, "seta": False, "recorte": "Nestlé x Garoto · 2002",
       "faixa": "A Nestlé comprou a Garoto", "linhas": [["e o CADE", W, 190], ["PROIBIU", G, 260]], "selo": "Nestlé x Garoto",
       "logo": "logo_nestle", "logos": {"logo_nestle": LOGOS["logo_nestle"]},
       "depois": mont(wim("garoto_fabrica", WIKI_FAB, dim=0.25), im("ia_negocio", dim=0.25))}),
    S("Dois anos depois, o Cade proibiu o negócio.",
      {"type": "stamp", "org": "CADE · 2004", "title": "NESTLÉ + GAROTO", "stamp": "VETADO", "stamp_palavra": "proibiu",
       "fundo": "ia_votacao", "fundo_dim": 0.5, "sons": [fx("rubber stamp hit", "proibiu", 0.75)]}),
    S("Só tinha um problema: a compra já tinha acontecido.",
      mont(wim("garoto_fabrica", WIKI_FAB, dim=0.6), sobre=big(("MAS A COMPRA", W, 130), ("JÁ TINHA", W, 150), ("ACONTECIDO", G, 170)),
           sons=[fx("cinematic boom hit", "acontecido", 0.6)])),
    S("Na época, Nestlé e Garoto juntas tinham mais da metade do mercado brasileiro de chocolates.",
      mont(im("ia_gondola", dim=0.55), sobre=big(("MAIS DA", W, 140), ("METADE", G, 220), ("DO CHOCOLATE DO BRASIL", W, 90)), sobre_em=1.2)),
    S("Por cinco votos a um, o Cade mandou a Nestlé vender a Garoto em até cento e cinquenta dias.",
      mont(im("ia_votacao", dim=0.55), wim("garoto_fabrica", WIKI_FAB, dim=0.55, palavra="mandou"),
           sobre=big(("5 x 1", G, 240), ("VENDA EM 150 DIAS", W, 100)))),
    S("Mas a lei daquela época permitia concluir uma aquisição antes da análise.",
      im("ia_negocio", dim=0.4, lower="A LEI DEIXAVA COMPRAR ANTES")),
    S("Então a Nestlé já controlava a empresa, e levou o caso pra Justiça.",
      mont(wim("garoto_fabrica", WIKI_FAB, dim=0.4), im("ia_justica", dim=0.4, palavra="Justiça"))),
    S("A disputa se arrastou por anos.",
      mont(im("ia_arquivo", dim=0.5), sobre=big(("2005", W, 120), ("2009", W, 120), ("2016", W, 120)))),
    S("Em dois mil e dezessete, chegou a ser prevista a venda de marcas como Serenata de Amor, Chokito, Lollo e Sensação.",
      mont(im("ia_gondola", dim=0.6),
           sobre={"type": "bullets", "title": "2017 · IAM SER VENDIDAS", "items": ["SERENATA DE AMOR", "CHOKITO", "LOLLO", "SENSAÇÃO"],
                  "size": 76, "last_gold": False, "stagger": 0.7}, sons=[fx("fast whoosh", None, 0.35, 0.5)])),
    S("Não aconteceu.", big(("NÃO", W, 220), ("ACONTECEU", R, 200))),
    S("Só em dois mil e vinte e três, vinte e um anos depois, o Cade aprovou a compra, com restrições.",
      mont(wim("garoto_fabrica", WIKI_FAB, dim=0.55), sobre={"type": "counter", "value": 21, "suffix": " ANOS", "over": "2002 → 2023",
           "label": "APROVADA COM RESTRIÇÕES", "color": [245, 170, 40], "size": 260},
           sons=[fx("deep cinematic boom", "vinte", 0.6)])),
    S("E o caso ajudou a mudar a lei brasileira.", im("ia_votacao", dim=0.45, lower="O CASO MUDOU A LEI")),
    S("Hoje, uma compra desse tamanho precisa ser analisada antes de ser concluída.",
      mont(im("ia_votacao", dim=0.55), sobre=big(("PRIMEIRO O CADE", W, 110), ("DEPOIS A COMPRA", G, 130)))),
    S("Você sabia que a Garoto é da Nestlé?",
      mont(wim("garoto_fabrica", WIKI_FAB, dim=0.55), sobre=big(("A GAROTO", W, 170), ("É DA", W, 130), ("NESTLÉ", G, 200)))),
]

E_ = ", vertical composition"
projeto = {
    "title": "Nestlé x Garoto", "slug": "garoto", "idioma": "pt", "trilha": "trap",
    "voz": {"nome": "gravada", "motor": "eleven", "eleven_voz": "Vinícius Torales"},
    "pronuncia": [[r"\bLollo\b", "Lólo"]],
    "script": {"long": {"parts": []}, "tiktoks": [],
               "shorts": [{"title": "A Nestlé comprou a Garoto. O CADE proibiu. Mas a compra já tinha acontecido", "sentences": frases}]},
    "ia": {  # no máximo 5 (cota grátis da Cloudflare é curta)
        "ia_negocio": "2002 corporate office, two executives shaking hands over a signed acquisition contract, a box of assorted chocolates on the table, warm light, faces out of focus" + E_,
        "ia_gondola": "Brazilian supermarket candy aisle full of colorful chocolate bars and bonbon boxes, shoppers blurred in background" + E_,
        "ia_votacao": "Brazilian government council meeting room in Brasilia, officials at a long table raising hands to vote, microphones, formal atmosphere, faces not recognizable" + E_,
        "ia_justica": "Brazilian federal court building facade at dusk with stone columns, dramatic sky" + E_,
        "ia_arquivo": "towering stacks of old dusty legal case folders tied with string in a dim archive room, years of paperwork" + E_,
    },
    "meta": {"titles": ["Nestlé x Garoto"], "description": "", "tags": ["nestle", "garoto", "cade", "chocolate", "negocios"]},
    "notes": ("FATOS (checados 19/10/2026): compra anunciada fev/2002 (Forbes); veto do CADE fev/2004 por 5x1 e prazo de 150 dias p/ vender a concorrente com até 20% (Forbes; Câmara 02/04/2004); "
              "juntas: mais da metade (ACNielsen 30,8%+24,4%; CADE fala em >58%); lei da época permitia consumar antes da análise; mudança em 2012 (análise prévia) em parte pelo caso (gov.br/CADE; Seu Dinheiro); "
              "Justiça 2005, decisão 2009 p/ novo julgamento (A Gazeta); 2017: previsto vender Serenata de Amor, Chokito, Lollo, Sensação (iProfesional 22/09/2017), não aconteceu (A Gazeta 2022); "
              "aprovação 07/06/2023 com restrições, 21 anos, caso mais antigo do CADE (Forbes; STJ 29/06/2023). Valor da compra fora do roteiro (fontes divergem: R$ 566 mi Forbes x ~US$ 250 mi Câmara)."),
}
d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", "garoto")
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
json.dump(projeto, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(sum(len(s["text"]) for s in frases), "caracteres")

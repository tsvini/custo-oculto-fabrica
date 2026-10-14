"""Monta projetos/netflix/projeto.json (Netflix x Blockbuster)."""
import json, os

G, W, R, GR, M = "gold", "white", "red", "green", "muted"


def big(*lines):
    return {"type": "bigtext", "stagger": 0.25, "lines": [list(l) for l in lines]}


IDS = {'familia_sofa': 190117, 'correio': 43658, 'aviao': 264862}


def vid(media, en, lower, fb):
    d = {"type": "video", "media": media, "search": en, "search_en": en, "start": 0.0, "dim": 0.4, "lower": lower, "fallback": fb}
    if media in IDS:
        d["pixabay_id"] = IDS[media]
    return d


def img(media, wiki, lower, fb):
    return {"type": "image", "media": media, "wiki": wiki, "lower": lower, "dim": 0.4, "fallback": fb}


def foto(media, arquivo, lower, fb):
    return img(media, ["File:" + arquivo], lower, fb)


def prt(media, url, source, fb):
    return {"type": "print", "media": media, "url": url, "source": source, "rotate": -1.0, "fallback": fb}


SAME = {"type": "same"}
S = lambda text, scene: {"text": text, "scene": scene}
FOTO_BEND = ["File:The Last Blockbuster storefront.jpg", "Blockbuster Bend Oregon"]
FOTO_BB = ["Blockbuster Video store"]


def capa(faixa, linhas, recorte, foto="bend", wiki=FOTO_BEND, selo="Netflix x Blockbuster"):
    return {"type": "capa", "foto": foto, "wiki": wiki, "seta": False, "recorte": recorte, "faixa": faixa, "linhas": linhas, "selo": selo}


CAPA_ABERTURA = capa("Netflix x Blockbuster", [["US$ 50", G, 250], ["MILHÕES", W, 200], ["RECUSARAM", R, 200]], "Netflix · 2000")

long_parts = [
    {"chapter": "", "sentences": [
        dict(S("Fala galera, aqui é o Vinícius do canal Custo Oculto.", CAPA_ABERTURA), abertura=True),
        S("Ano dois mil. Dois empresários de uma empresa pequena entram na sala do presidente da maior locadora do mundo.", {"type": "date", "month": "TEXAS", "day": "EUA", "year": "2000", "tag": "SEDE DA BLOCKBUSTER"}),
        S("A proposta: vender a empresa deles por cinquenta milhões de dólares.", {"type": "counter", "value": 50, "prefix": "US$ ", "suffix": " MI", "over": "A PROPOSTA", "label": "PELA EMPRESA INTEIRA", "color": G, "size": 230}),
        S("Segundo um dos fundadores, o presidente da Blockbuster mal conseguiu segurar o riso.", big(("ELE QUASE", W, 140), ("RIU", R, 220))),
        S("A empresa pequena se chamava Netflix.", {"type": "flash", "text": "NETFLIX", "tint": "red", "size": 190}),
        S("Uma empresa que mandava DVD pelo correio e dava prejuízo.", big(("DVD PELO CORREIO", W, 120), ("E PREJUÍZO", R, 160))),
        S("Dez anos depois, a Blockbuster pediu falência. E a Netflix virou uma das maiores empresas de entretenimento do planeta.", {"type": "compare", "title": "DEZ ANOS DEPOIS", "items": [["FALÊNCIA", "BLOCKBUSTER · 2010", R], ["+300 MI", "ASSINANTES NETFLIX", G]], "size": 150, "stagger": 1.2, "vs": False}),
        S("Mas a história que todo mundo conta, de que a Blockbuster quebrou só porque riu da Netflix, está errada.", {"type": "stamp", "org": "A VERSÃO FAMOSA", "title": "QUEBROU PORQUE RIU", "stamp": "ERRADA", "stamp_at": 0.9}),
        S("O motivo real é bem mais interessante. E passa até pelo Brasil.", big(("O MOTIVO REAL", W, 130), ("PASSA PELO BRASIL", G, 120))),
        S("Neste vídeo você vai ver o império das locadoras, a reunião dos cinquenta milhões, a guerra que a Netflix quase perdeu e o erro que realmente derrubou a Blockbuster.", {"type": "bullets", "items": ["O IMPÉRIO DAS LOCADORAS", "A REUNIÃO DOS US$ 50 MI", "A GUERRA", "O ERRO DE VERDADE"], "size": 80, "last_gold": True}),
    ]},
    {"chapter": "O IMPÉRIO DA LOCADORA", "sentences": [
        S("A Blockbuster abriu a primeira loja em mil novecentos e oitenta e cinco, nos Estados Unidos.", big(("1985", G, 230), ("A PRIMEIRA LOJA", W, 110))),
        S("Em mil novecentos e oitenta e sete, o empresário Wayne Huizenga assumiu o controle e acelerou a expansão.", big(("1987", G, 220), ("WAYNE HUIZENGA", W, 120), ("ASSUME", M, 90))),
        S("Em mil novecentos e noventa e quatro, vendeu a rede pro grupo Viacom por sete vírgula seis bilhões de dólares.", {"type": "counter", "value": 7, "prefix": "US$ ", "suffix": ",6 BI", "over": "VIACOM COMPRA · 1994", "label": "O PREÇO DA BLOCKBUSTER", "color": G, "size": 220}),
        S("Em poucos anos, virou a maior rede de locadoras do mundo.", vid("prateleira_vhs", "video rental store shelves", "A maior locadora do mundo", big(("A MAIOR", W, 150), ("DO MUNDO", G, 170)))),
        S("No auge, em dois mil e quatro, eram mais de nove mil lojas pelo mundo.", {"type": "counter", "value": 9, "prefix": "+", "suffix": " MIL LOJAS", "over": "AUGE · 2004", "label": "BLOCKBUSTER NO MUNDO", "color": G, "size": 200}),
        S("Sexta à noite, a família ia até a locadora escolher o filme do fim de semana. Era quase um ritual.", vid("familia_sofa", "family watching movie popcorn couch", "Sexta à noite", big(("SEXTA", W, 160), ("À NOITE", G, 170)))),
        S("No Brasil, a gente tinha a locadora do bairro. Mas a Blockbuster também chegou por aqui, com lojas grandes, azul e amarelo.", big(("AZUL", W, 160), ("E AMARELO", G, 160))),
        S("E tinha um detalhe que pouca gente lembra: a multa por atraso.", {"type": "stamp", "org": "DEVOLUÇÃO EM ATRASO", "title": "FITA DEVOLVIDA 2 DIAS DEPOIS", "stamp": "MULTA", "stamp_at": 0.9}),
        S("Esqueceu de devolver a fita? Pagava. E a Blockbuster ganhava muito dinheiro com isso.", big(("A MULTA", W, 150), ("DAVA LUCRO", G, 170))),
        S("No ano dois mil, só as multas por atraso renderam cerca de oitocentos milhões de dólares. Dezesseis por cento de tudo o que a empresa faturava.", {"type": "counter", "value": 800, "prefix": "US$ ", "suffix": " MI", "over": "SÓ EM MULTAS · 2000", "label": "16% DO FATURAMENTO", "color": G, "size": 210}),
        S("Guarda essa informação, porque ela vai ser importante no fim da história.", {"type": "flash", "text": "GUARDA\nISSO", "color": G, "size": 160}),
    ]},
    {"chapter": "O DVD PELO CORREIO", "sentences": [
        S("Em mil novecentos e noventa e sete, Reed Hastings e Marc Randolph fundaram a Netflix, na Califórnia.", big(("1997", G, 230), ("REED HASTINGS", W, 110), ("MARC RANDOLPH", W, 110))),
        S("A ideia era alugar DVD pela internet e mandar pelo correio.", vid("correio", "mailbox envelope mail delivery", "DVD pelo correio", big(("DVD", G, 220), ("PELO CORREIO", W, 120)))),
        S("O site entrou no ar em mil novecentos e noventa e oito, com menos de mil filmes no catálogo.", big(("1998", G, 220), ("O SITE NO AR", W, 120))),
        S("E tem uma lenda famosa sobre esse começo.", {"type": "flash", "text": "A LENDA", "color": G, "size": 180}),
        S("Reed Hastings contou que teve a ideia depois de pagar quarenta dólares de multa por atrasar a devolução do filme Apollo 13.", {"type": "stamp", "org": "MULTA POR ATRASO", "title": "APOLLO 13", "stamp": "US$ 40", "stamp_at": 0.9}),
        S("Mas o outro fundador, Marc Randolph, chama essa história de ficção conveniente. Uma história boa pra explicar por que a Netflix era melhor.", big(("FICÇÃO", W, 160), ("CONVENIENTE?", R, 150))),
        S("Verdade ou não, a multa por atraso era exatamente o ponto fraco que a Netflix queria atacar.", big(("O PONTO FRACO", W, 130), ("A MULTA", R, 190))),
        S("Depois veio a assinatura: um valor fixo por mês e nada de multa por atraso.", {"type": "compare", "title": "O MODELO", "items": [["MULTA", "BLOCKBUSTER", R], ["SEM MULTA", "NETFLIX", G]], "size": 160, "stagger": 1.2, "vs": True}),
        S("Pro cliente parecia ótimo. Pra empresa, era um buraco.", big(("PRO CLIENTE", W, 130), ("UM BURACO", R, 170))),
        S("Por volta do ano dois mil, a Netflix perdia cerca de cinquenta milhões de dólares por ano e estava cheia de dívidas.", {"type": "counter", "value": 50, "prefix": "-US$ ", "suffix": " MI", "over": "PREJUÍZO POR ANO", "label": "NETFLIX · ANO 2000", "color": R, "size": 210}),
        S("Foi nessa situação que os fundadores pegaram um avião pro Texas.", vid("aviao", "airplane takeoff", "Rumo ao Texas", big(("RUMO AO", W, 140), ("TEXAS", G, 200)))),
    ]},
    {"chapter": "OS CINQUENTA MILHÕES", "sentences": [
        S("A proposta era simples: a Blockbuster comprava a Netflix por cinquenta milhões de dólares.", {"type": "counter", "value": 50, "prefix": "US$ ", "suffix": " MI", "over": "A PROPOSTA", "label": "NETFLIX À VENDA", "color": G, "size": 230}),
        S("A Netflix cuidaria da parte online, com a marca Blockbuster, e as lojas divulgariam o serviço.", {"type": "flow", "a": "NETFLIX", "a_sub": "cuida do online", "b": "BLOCKBUSTER", "b_sub": "marca e lojas", "caption": "O ACORDO PROPOSTO"}),
        S("O diretor financeiro da Netflix, Barry McCarthy, também estava na reunião.", big(("NA SALA", W, 140), ("3 DA NETFLIX", G, 150))),
        S("Na época, a Blockbuster faturava na casa dos cinco bilhões de dólares por ano.", {"type": "compare", "title": "O TAMANHO DE CADA UM", "items": [["US$ 5 BI", "FATURAMENTO BLOCKBUSTER", G], ["US$ 50 MI", "PREÇO DA NETFLIX", W]], "size": 150, "stagger": 1.2, "vs": False}),
        S("Cinquenta milhões era cerca de um por cento disso.", big(("CERCA DE", W, 130), ("1%", G, 260))),
        S("O presidente, John Antioco, recusou. E, segundo Marc Randolph, parecia estar segurando o riso.", {"type": "stamp", "org": "BLOCKBUSTER · 2000", "title": "COMPRAR A NETFLIX", "stamp": "RECUSADO", "stamp_at": 0.9}),
        S("Segundo relatos, a Netflix ainda tentou outras vezes. A resposta foi sempre não.", big(("OUTRAS VEZES", W, 140), ("SEMPRE NÃO", R, 160))),
        S("E tem um detalhe que mostra onde a Blockbuster estava apostando.", {"type": "flash", "text": "UM DETALHE", "color": G, "size": 160}),
        S("Naquele mesmo ano, ela assinou um acordo de vinte anos com a Enron, pra filmes sob demanda pela internet.", {"type": "stamp", "org": "BLOCKBUSTER + ENRON · 2000", "title": "ACORDO DE 20 ANOS", "stamp": "ASSINADO", "stamp_at": 0.9}),
        S("Meses depois, a Enron quebrou num dos maiores escândalos contábeis da história. E o acordo foi junto.", big(("A ENRON", W, 150), ("QUEBROU", R, 190))),
        S("Mas aqui vai a minha opinião: naquele dia, recusar não foi burrice.", {"type": "flash", "text": "MINHA\nOPINIÃO", "color": G, "size": 160}),
        S("A Netflix dava prejuízo, dependia do correio, e o streaming ainda nem existia.", {"type": "bullets", "title": "A NETFLIX EM 2000", "items": ["DAVA PREJUÍZO", "DEPENDIA DO CORREIO", "SEM STREAMING"], "size": 90, "last_gold": True}),
        S("O erro da Blockbuster não foi aquele não. Foi o que veio depois.", big(("O ERRO", W, 150), ("VEIO DEPOIS", R, 160))),
    ]},
    {"chapter": "A GUERRA QUE A NETFLIX QUASE PERDEU", "sentences": [
        S("Em dois mil e quatro, a Blockbuster lançou o próprio aluguel pela internet.", {"type": "date", "month": "BLOCKBUSTER", "day": "ON", "year": "2004", "tag": "ALUGUEL PELA INTERNET"}),
        S("Em cerca de dois anos, chegou a uns dois milhões de assinantes.", {"type": "counter", "value": 2, "suffix": " MILHÕES", "over": "BLOCKBUSTER ONLINE", "label": "EM CERCA DE 2 ANOS", "color": G, "size": 210}),
        S("Pra ter ideia, a Netflix tinha levado nove anos pra chegar a uns seis milhões.", {"type": "compare", "title": "ASSINANTES", "items": [["2 MI", "BLOCKBUSTER EM ~2 ANOS", G], ["6 MI", "NETFLIX EM ~9 ANOS", W]], "size": 160, "stagger": 1.2, "vs": False}),
        S("Ou seja: em dois anos, a Blockbuster chegou a um terço do que a Netflix levou quase uma década pra construir.", big(("EM 2 ANOS", W, 140), ("UM TERÇO", G, 180), ("DA NETFLIX", W, 120))),
        S("E em dois mil e seis veio a jogada mais forte: alugar pela internet e poder devolver na loja, trocando por outro filme na hora.", {"type": "flow", "a": "PEDE ONLINE", "a_sub": "recebe em casa", "b": "TROCA NA LOJA", "b_sub": "na hora", "caption": "TOTAL ACCESS · 2006"}),
        S("Era algo que a Netflix simplesmente não tinha como oferecer.", big(("A NETFLIX", W, 140), ("NÃO TINHA LOJA", R, 150))),
        S("Pensa no cliente: recebia o DVD em casa e, quando queria outro na hora, passava na loja da esquina. Era o melhor dos dois mundos.", big(("O MELHOR", W, 150), ("DOS DOIS MUNDOS", G, 130))),
        S("E a Blockbuster tinha uma vantagem que dinheiro nenhum compra rápido: milhares de lojas espalhadas pelas cidades.", big(("MILHARES", G, 180), ("DE LOJAS", W, 150))),
        S("Num trimestre de dois mil e sete, a Netflix chegou a perder cinquenta e cinco mil assinantes.", {"type": "counter", "value": 55, "prefix": "-", "suffix": " MIL", "over": "NETFLIX · 2007", "label": "ASSINANTES PERDIDOS NUM TRIMESTRE", "color": R, "size": 220}),
        S("Anos depois, o próprio Reed Hastings admitiu: se não fosse a dívida, a Blockbuster podia ter acabado com eles.", big(("PODIA TER", W, 140), ("ACABADO COM A NETFLIX", R, 100))),
        S("E o próprio Antioco disse depois que, se a estratégia tivesse continuado, a Blockbuster podia ter chegado a uns dez milhões de assinantes online.", {"type": "counter", "value": 10, "suffix": " MILHÕES", "over": "SEGUNDO ANTIOCO", "label": "O QUE A BLOCKBUSTER ONLINE PODIA TER", "color": G, "size": 200}),
        S("Naquele momento, quem estava ganhando a guerra era a Blockbuster.", {"type": "flash", "text": "BLOCKBUSTER\nGANHANDO", "tint": "red", "size": 140}),
    ]},
    {"chapter": "O ERRO DE VERDADE", "sentences": [
        S("Só que essa guerra custou caro. Pra competir, a Blockbuster tinha acabado com a multa por atraso, uma das suas maiores fontes de dinheiro.", big(("SEM MULTA", W, 150), ("SEM DINHEIRO", R, 150))),
        S("E começou uma briga lá dentro. O investidor Carl Icahn pressionou, e Antioco perdeu o cargo.", {"type": "flow", "a": "CARL ICAHN", "a_sub": "investidor", "b": "ANTIOCO", "b_sub": "fora do cargo", "caption": "A BRIGA INTERNA"}),
        S("O novo presidente aumentou o preço do serviço online e acabou com a troca grátis na loja.", {"type": "stamp", "org": "NOVA DIREÇÃO · 2007", "title": "TROCA GRÁTIS NA LOJA", "stamp": "CANCELADA", "stamp_at": 0.9}),
        S("E gastou dinheiro em outras apostas, como a compra da Movielink, um serviço de filmes pela internet que nunca decolou.", big(("NOVAS APOSTAS", W, 130), ("SEM RESULTADO", R, 140))),
        S("O crescimento parou na hora.", big(("O CRESCIMENTO", W, 130), ("PAROU", R, 210))),
        S("E tem uma ironia: anos depois, o próprio Antioco investiu na Netflix. Mas vendeu cedo, antes da grande alta.", big(("ANTIOCO", W, 150), ("INVESTIU NA NETFLIX", G, 110), ("E VENDEU CEDO", R, 110))),
        S("Enquanto isso, também em dois mil e sete, a Netflix lançou o streaming.", {"type": "date", "month": "NETFLIX", "day": "▶", "year": "2007", "tag": "COMEÇA O STREAMING"}),
        S("Em setembro de dois mil e dez, a Blockbuster pediu falência, com uma dívida perto de um bilhão de dólares.", {"type": "counter", "value": 900, "prefix": "+US$ ", "suffix": " MI", "over": "SETEMBRO DE 2010", "label": "DÍVIDAS NA FALÊNCIA", "color": R, "size": 200}),
        S("Aqui está o custo oculto.", {"type": "flash", "text": "O CUSTO\nOCULTO", "tint": "red", "size": 160}),
        S("Na época, ainda eram cerca de vinte e cinco mil funcionários. Milhares de lojas fecharam, e muita gente perdeu o emprego.", vid("loja_fechada", "closed store empty shop", "Lojas fechando", big(("LOJAS", W, 160), ("FECHADAS", R, 170)))),
        S("Em dois mil e onze, o que sobrou foi vendido num leilão por cerca de trezentos e vinte milhões de dólares.", {"type": "compare", "title": "BLOCKBUSTER", "items": [["US$ 5 BI", "FATURAVA POR ANO", W], ["US$ 320 MI", "VENDIDA EM 2011", R]], "size": 150, "stagger": 1.2, "vs": False}),
        S("Se você lembra de alugar filme na locadora, segue o Custo Oculto. Toda semana tem uma marca nova por aqui.", {"type": "bigtext", "stagger": 0.25, "lines": [["SEGUE O CANAL", G, 150], ["TODA SEMANA, UMA MARCA", W, 80]]}),
    ]},
    {"chapter": "E NO BRASIL?", "sentences": [
        S("E no Brasil? A Blockbuster também tinha lojas por aqui.", big(("E NO", W, 150), ("BRASIL?", G, 210))),
        S("Em janeiro de dois mil e sete, a Lojas Americanas comprou as cento e vinte e sete lojas da Blockbuster no país, por cento e oitenta e seis milhões de reais.", {"type": "counter", "value": 127, "suffix": " LOJAS", "over": "JANEIRO DE 2007", "label": "R$ 186 MI · AMERICANAS COMPRA A BLOCKBUSTER", "color": G, "size": 210}),
        S("Muitas viraram Americanas Express.", big(("VIRARAM", W, 140), ("AMERICANAS EXPRESS", R, 110))),
        S("Sim, a mesma Americanas do nosso último caso.", {"type": "flash", "text": "A MESMA\nAMERICANAS", "tint": "red", "size": 140}),
        S("Hoje só existe uma Blockbuster no mundo, em Bend, no Oregon. Virou ponto turístico.", img("bend", FOTO_BEND, "A última Blockbuster · Bend, Oregon", big(("SÓ RESTA", W, 140), ("UMA", G, 220)))),
        S("Do outro lado, a Netflix chegou ao Brasil em dois mil e onze.", big(("2011", G, 220), ("NETFLIX NO BRASIL", W, 110))),
        S("Em dois mil e treze, lançou House of Cards, a primeira série própria de sucesso. E deixou de ser locadora pra virar estúdio.", big(("DE LOCADORA", W, 140), ("A ESTÚDIO", G, 170))),
        S("E a Netflix passou de trezentos milhões de assinantes.", {"type": "counter", "value": 300, "prefix": "+", "suffix": " MILHÕES", "over": "NETFLIX", "label": "DE ASSINANTES", "color": G, "size": 200}),
        S("A lição oculta é uma só.", {"type": "flash", "text": "A LIÇÃO\nOCULTA", "tint": "red", "size": 160}),
        S("Toda empresa grande tem a sua multa por atraso: um dinheiro fácil que o cliente odeia.", big(("TODA EMPRESA", W, 130), ("TEM A SUA MULTA", R, 140))),
        S("Enquanto esse dinheiro entra, ninguém lá dentro quer mexer nele. E é exatamente aí que alguém de fora aparece e faz diferente.", big(("ALGUÉM DE FORA", W, 130), ("FAZ DIFERENTE", G, 150))),
        S("O que derrubou a Blockbuster não foi dizer não. Foi defender a multa, as lojas e a dívida, quando o cliente já queria outra coisa.", {"type": "bullets", "title": "O QUE DERRUBOU", "items": ["A DÍVIDA", "A BRIGA INTERNA", "DEFENDER O MODELO VELHO"], "size": 90, "last_gold": True}),
        S("E você? Qual foi o último filme que alugou numa locadora? Conta aqui nos comentários.", big(("QUAL FOI", W, 140), ("O ÚLTIMO FILME?", G, 140), ("COMENTA", M, 90))),
        S("E a pergunta que fica é: qual empresa de hoje está rindo da próxima Netflix?", {"type": "endcard", "sub": "NETFLIX X BLOCKBUSTER"}),
    ]},
]

FIM = "O caso completo está no canal. Procura Netflix no Custo Oculto."
shorts = [
    {"title": "A Blockbuster podia ter comprado a Netflix por US$ 50 milhões", "sentences": [
        S("A Blockbuster podia ter comprado a Netflix por cinquenta milhões de dólares.", capa("Podia ter comprado", [["A NETFLIX", R, 220], ["por US$ 50", G, 200], ["MILHÕES", W, 190]], "Netflix · 2000")),
        S("No ano dois mil, os fundadores da Netflix ofereceram a empresa inteira.", big(("2000", G, 220), ("A OFERTA", W, 130))),
        S("O presidente da Blockbuster recusou. Segundo um dos fundadores, quase rindo.", {"type": "stamp", "org": "BLOCKBUSTER · 2000", "title": "COMPRAR A NETFLIX", "stamp": "RECUSADO", "stamp_at": 0.9}),
        S("Dez anos depois, a Blockbuster faliu.", big(("2010", R, 220), ("FALÊNCIA", W, 150))),
        S("Mas o motivo real não foi esse não. Foi o que veio depois.", big(("O MOTIVO", W, 140), ("FOI OUTRO", R, 160))),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("PROCURA NETFLIX", G, 130), ("NO CUSTO OCULTO", W, 100))),
    ]},
    {"title": "A jogada que quase matou a Netflix", "sentences": [
        S("A Blockbuster quase acabou com a Netflix. E pouca gente sabe disso.", capa("Pouca gente sabe", [["QUASE", W, 220], ["MATOU", R, 260], ["a Netflix", G, 200]], "Blockbuster · 2006")),
        S("Em dois mil e seis, a Blockbuster deixou alugar pela internet e trocar o filme na loja, na hora.", {"type": "flow", "a": "PEDE ONLINE", "a_sub": "recebe em casa", "b": "TROCA NA LOJA", "b_sub": "na hora", "caption": "TOTAL ACCESS"}),
        S("A Netflix não tinha loja. Num trimestre, perdeu cinquenta e cinco mil assinantes.", {"type": "counter", "value": 55, "prefix": "-", "suffix": " MIL", "over": "NETFLIX · 2007", "label": "ASSINANTES PERDIDOS", "color": R, "size": 220}),
        S("Aí a Blockbuster trocou de presidente, e o novo acabou com a jogada.", {"type": "stamp", "org": "NOVA DIREÇÃO", "title": "A JOGADA VENCEDORA", "stamp": "CANCELADA", "stamp_at": 0.9}),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("PROCURA NETFLIX", G, 130), ("NO CUSTO OCULTO", W, 100))),
    ]},
    {"title": "A Americanas comprou a Blockbuster no Brasil", "sentences": [
        S("Você sabia que a Americanas comprou a Blockbuster no Brasil?", capa("Você sabia?", [["AMERICANAS", R, 200], ["COMPROU A", W, 170], ["BLOCKBUSTER", G, 190]], "Brasil · 2007", foto="loja_am", wiki=["Lojas Americanas"], selo="Netflix x Blockbuster")),
        S("Em janeiro de dois mil e sete, foram cento e vinte e sete lojas, por cento e oitenta e seis milhões de reais.", {"type": "counter", "value": 127, "suffix": " LOJAS", "over": "JANEIRO DE 2007", "label": "R$ 186 MILHÕES", "color": G, "size": 210}),
        S("Muitas viraram Americanas Express.", big(("VIRARAM", W, 140), ("AMERICANAS EXPRESS", R, 110))),
        S("Enquanto isso, lá fora, a Blockbuster caminhava pra falência.", big(("LÁ FORA", W, 140), ("FALÊNCIA", R, 180))),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("PROCURA NETFLIX", G, 130), ("NO CUSTO OCULTO", W, 100))),
    ]},
    {"title": "Só existe uma Blockbuster no mundo", "sentences": [
        S("Já foram mais de nove mil lojas. Hoje só existe uma Blockbuster no mundo.", capa("+ de 9 mil lojas", [["SÓ", W, 230], ["SOBROU", R, 250], ["UMA", G, 260]], "Bend, Oregon")),
        S("Ela fica em Bend, no Oregon, nos Estados Unidos, e virou ponto turístico.", img("bend", FOTO_BEND, "A última Blockbuster · Bend, Oregon", big(("BEND", G, 220), ("OREGON", W, 140)))),
        S("A rede pediu falência em dois mil e dez, com mais de novecentos milhões de dólares em dívidas.", {"type": "counter", "value": 900, "prefix": "+US$ ", "suffix": " MI", "over": "FALÊNCIA · 2010", "label": "EM DÍVIDAS", "color": R, "size": 200}),
        S("E dez anos antes, tinha recusado comprar a Netflix.", big(("RECUSOU", R, 170), ("A NETFLIX", W, 160))),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("PROCURA NETFLIX", G, 130), ("NO CUSTO OCULTO", W, 100))),
    ]},
]

tiktoks = [
    {"title": "A Blockbuster recusou comprar a Netflix por US$ 50 milhões",
     "caption": "A Blockbuster recusou comprar a Netflix por US$ 50 milhões. Mas o erro de verdade veio depois. E a história passa pela Americanas.",
     "hashtags": ["#netflix", "#blockbuster", "#negocios", "#nostalgia", "#curiosidades"],
     "sentences": [
        S("A Blockbuster recusou comprar a Netflix por cinquenta milhões de dólares.", capa("Recusaram", [["A NETFLIX", R, 220], ["por US$ 50", G, 200], ["MILHÕES", W, 190]], "Netflix · 2000")),
        S("No ano dois mil, a Netflix mandava DVD pelo correio e dava prejuízo.", big(("DVD", G, 220), ("PELO CORREIO", W, 120))),
        S("E a Blockbuster? Só em multa por atraso, ganhou cerca de oitocentos milhões de dólares naquele ano.", {"type": "counter", "value": 800, "prefix": "US$ ", "suffix": " MI", "over": "SÓ EM MULTAS · 2000", "label": "BLOCKBUSTER", "color": G, "size": 210}),
        S("Os fundadores ofereceram a empresa inteira pra Blockbuster, que faturava bilhões.", {"type": "compare", "title": "O TAMANHO DE CADA UM", "items": [["US$ 5 BI", "BLOCKBUSTER", G], ["US$ 50 MI", "NETFLIX", W]], "size": 150, "stagger": 1.2, "vs": False}),
        S("O presidente recusou, quase rindo.", {"type": "stamp", "org": "BLOCKBUSTER · 2000", "title": "COMPRAR A NETFLIX", "stamp": "RECUSADO", "stamp_at": 0.9}),
        S("Na época, a Netflix dava prejuízo e mandava DVD pelo correio. Recusar parecia até sensato.", big(("RECUSAR", W, 150), ("PARECIA SENSATO", G, 130))),
        S("Mas aqui vai a minha opinião: o erro não foi esse.", {"type": "flash", "text": "MINHA\nOPINIÃO", "color": G, "size": 160}),
        S("Anos depois, a Blockbuster quase venceu, deixando alugar online e trocar o filme na loja.", big(("QUASE", W, 160), ("VENCEU", G, 190))),
        S("Só que uma briga interna derrubou o presidente, e o novo cancelou a jogada.", big(("BRIGA", W, 160), ("INTERNA", R, 170))),
        S("E tem ironia: anos depois, o presidente que recusou a Netflix investiu nela. E vendeu cedo demais.", big(("INVESTIU", W, 150), ("E VENDEU CEDO", R, 140))),
        S("Em setembro de dois mil e dez, a Blockbuster pediu falência.", big(("2010", R, 220), ("FALÊNCIA", W, 150))),
        S("Com uma dívida perto de um bilhão de dólares e milhares de lojas fechadas.", big(("QUASE", W, 150), ("US$ 1 BI", R, 200), ("EM DÍVIDAS", W, 110))),
        S("E no Brasil, quem comprou as lojas dela foi a Americanas.", big(("NO BRASIL", W, 150), ("AMERICANAS", R, 170))),
        S("Hoje sobrou uma única Blockbuster no mundo, no Oregon.", img("bend", FOTO_BEND, "A última Blockbuster", big(("SÓ RESTA", W, 140), ("UMA", G, 220)))),
        S("Qual foi o último filme que você alugou? Conta aqui.", big(("QUAL FOI", W, 140), ("O ÚLTIMO FILME?", G, 140), ("COMENTA", M, 90))),
     ]},
]


# ---------- material real ----------
F_BB = "Anchorage Blockbuster video store (41894010352).jpg"
TROCAS = {
    "A Blockbuster abriu a primeira loja": foto("bb_loja", F_BB, "Blockbuster", big(("1985", G, 230), ("A PRIMEIRA LOJA", W, 110))),
    "Em poucos anos, virou a maior rede": foto("bb_prateleira", "Anchorage Blockbuster video store (41894012562).jpg", "A maior locadora do mundo", big(("A MAIOR", W, 150), ("DO MUNDO", G, 170))),
    "No Brasil, a gente tinha a locadora do bairro": foto("bb_azul", "Blockbuster Video store Rockhampton.jpg", "Azul e amarelo", big(("AZUL", W, 160), ("E AMARELO", G, 160))),
    "No ano dois mil, só as multas por atraso": prt("print_multas", "https://www.nbcnews.com/id/wbna39332696", "NBC News · 2010",
                                                  {"type": "counter", "value": 800, "prefix": "US$ ", "suffix": " MI", "over": "SÓ EM MULTAS · 2000", "label": "16% DO FATURAMENTO", "color": G, "size": 210}),
    "Em mil novecentos e noventa e sete, Reed Hastings": foto("hastings", "Reed Hastings 2010 A.jpg", "Reed Hastings, cofundador da Netflix", big(("1997", G, 230), ("REED HASTINGS", W, 110), ("MARC RANDOLPH", W, 110))),
    "Reed Hastings contou que teve a ideia": prt("print_apollo", "https://www.cnbc.com/2017/05/23/netflix-ceo-reed-hastings-on-how-the-company-was-born.html", "CNBC · 2017",
                                                 {"type": "stamp", "org": "MULTA POR ATRASO", "title": "APOLLO 13", "stamp": "US$ 40", "stamp_at": 0.9}),
    "Mas o outro fundador, Marc Randolph": foto("randolph", "Marc Randolph by Gage Skidmore.jpg", "Marc Randolph, cofundador da Netflix", big(("FICÇÃO", W, 160), ("CONVENIENTE?", R, 150))),
    "O presidente, John Antioco, recusou.": prt("print_fortune", "https://fortune.com/2023/04/14/netflix-cofounder-marc-randolph-recalls-blockbuster-rejecting-chance-to-buy-it/", "Fortune · 14/04/2023",
                                                {"type": "stamp", "org": "BLOCKBUSTER · 2000", "title": "COMPRAR A NETFLIX", "stamp": "RECUSADO", "stamp_at": 0.9}),
    "E começou uma briga lá dentro": foto("icahn", "Carl Icahn, 1980s.jpg", "Carl Icahn, investidor (anos 1980)", {"type": "flow", "a": "CARL ICAHN", "a_sub": "investidor", "b": "ANTIOCO", "b_sub": "fora do cargo", "caption": "A BRIGA INTERNA"}),
    "Na época, ainda eram cerca de vinte e cinco mil": foto("bb_fechando", "Blockbuster Video store Closing, Miami Beach Florida, November 2013.jpg", "Loja fechando · Miami Beach, 2013", big(("LOJAS", W, 160), ("FECHADAS", R, 170))),
    "Em dois mil e onze, o que sobrou foi vendido": prt("print_dish", "https://techcrunch.com/2011/04/06/dish-wins-bankruptcy-auction-buys-blockbuster-assets-for-228m-in-cash/", "TechCrunch · 06/04/2011",
                                                        {"type": "compare", "title": "BLOCKBUSTER", "items": [["US$ 5 BI", "FATURAVA POR ANO", W], ["US$ 320 MI", "VENDIDA EM 2011", R]], "size": 150, "stagger": 1.2, "vs": False}),
    "Em janeiro de dois mil e sete, a Lojas Americanas comprou": prt("print_jb", "https://www.jb.com.br/economia/noticias/2007/01/24/lojas-americanas-compram-blockbuster-no-brasil-por-r-1862-mi.html", "Jornal do Brasil · 24/01/2007",
                                                        {"type": "counter", "value": 127, "suffix": " LOJAS", "over": "JANEIRO DE 2007", "label": "R$ 186 MI · AMERICANAS COMPRA A BLOCKBUSTER", "color": G, "size": 210}),
    "Do outro lado, a Netflix chegou ao Brasil": foto("netflix_sede", "Netflix headquarters.jpg", "Sede da Netflix · Los Gatos, Califórnia", big(("2011", G, 220), ("NETFLIX NO BRASIL", W, 110))),
    "O presidente da Blockbuster recusou. Segundo um dos fundadores": prt("print_fortune", "https://fortune.com/2023/04/14/netflix-cofounder-marc-randolph-recalls-blockbuster-rejecting-chance-to-buy-it/", "Fortune · 14/04/2023",
                                                {"type": "stamp", "org": "BLOCKBUSTER · 2000", "title": "COMPRAR A NETFLIX", "stamp": "RECUSADO", "stamp_at": 0.9}),
    "Em janeiro de dois mil e sete, foram cento e vinte e sete lojas": prt("print_jb", "https://www.jb.com.br/economia/noticias/2007/01/24/lojas-americanas-compram-blockbuster-no-brasil-por-r-1862-mi.html", "Jornal do Brasil · 24/01/2007",
                                                {"type": "counter", "value": 127, "suffix": " LOJAS", "over": "JANEIRO DE 2007", "label": "R$ 186 MILHÕES", "color": G, "size": 210}),
}


def aplica_trocas(grupos):
    usadas = set()
    for g in grupos:
        for s in g["sentences"]:
            for k, sc in TROCAS.items():
                if s["text"].startswith(k):
                    s["scene"] = sc; usadas.add(k)
    return usadas


_u = aplica_trocas(long_parts) | aplica_trocas(shorts) | aplica_trocas(tiktoks)
assert not [k for k in TROCAS if k not in _u], [k for k in TROCAS if k not in _u]

projeto = {
    "title": "Netflix",
    "slug": "netflix",
    "angle": "A Blockbuster recusou comprar a Netflix por US$ 50 milhões. Mas o erro que matou a locadora veio depois, e a história passa pela Americanas.",
    "voz": {"nome": "gravada", "motor": "eleven", "eleven_voz": "Vinícius Torales"},
    "script": {"long": {"parts": long_parts}, "shorts": shorts, "tiktoks": tiktoks},
    "serie": [
        {"partes": [1, 2], "capa": capa("Parte 1 de 4", [["US$ 50", G, 250], ["MILHÕES", W, 200], ["E UMA RISADA", R, 170]], "Netflix · Parte 1", selo="Netflix x Blockbuster · Parte 1"),
         "caption": "Netflix x Blockbuster, parte 1: a proposta de US$ 50 milhões e o império das locadoras. Segue pra ver a parte 2.",
         "hashtags": ["#netflix", "#blockbuster", "#nostalgia", "#negocios", "#serie"]},
        {"partes": [3, 4], "capa": capa("Parte 2 de 4", [["A REUNIÃO", W, 200], ["QUE VALIA", G, 190], ["BILHÕES", R, 220]], "Netflix · Parte 2", selo="Netflix x Blockbuster · Parte 2"),
         "caption": "Netflix x Blockbuster, parte 2: a Netflix dava prejuízo e ofereceu a empresa inteira. E a minha opinião sobre aquele não.",
         "hashtags": ["#netflix", "#blockbuster", "#negocios", "#historia", "#serie"]},
        {"partes": [5, 6], "capa": capa("Parte 3 de 4", [["A GUERRA", W, 220], ["QUE A NETFLIX", G, 170], ["QUASE PERDEU", R, 190]], "Netflix · Parte 3", selo="Netflix x Blockbuster · Parte 3"),
         "caption": "Netflix x Blockbuster, parte 3: a jogada que quase matou a Netflix e o erro que derrubou a Blockbuster.",
         "hashtags": ["#netflix", "#blockbuster", "#negocios", "#nostalgia", "#serie"]},
        {"partes": [7], "capa": capa("Parte 4 de 4", [["E NO", W, 220], ["BRASIL?", G, 260], ["a Americanas", R, 170]], "Netflix · Final", selo="Netflix x Blockbuster · Final"),
         "caption": "Netflix x Blockbuster, parte final: a Americanas comprou a Blockbuster no Brasil, e só sobrou uma loja no mundo.",
         "hashtags": ["#netflix", "#blockbuster", "#americanas", "#nostalgia", "#serie"]},
    ],
    "meta": {
        "titles": [
            "NETFLIX: A Empresa Que a Blockbuster Recusou Comprar Por US$ 50 Milhões",
            "NETFLIX Quase Foi Vendida Por US$ 50 Milhões. A Blockbuster Riu",
        ],
        "description": "No ano 2000, os fundadores da Netflix ofereceram a empresa inteira à Blockbuster por US$ 50 milhões. A proposta foi recusada. Dez anos depois, a Blockbuster faliu, e a Netflix passou de 300 milhões de assinantes. Mas o erro que derrubou a maior locadora do mundo não foi aquele não. Neste vídeo: o império das locadoras, a guerra que quase matou a Netflix, a briga interna na Blockbuster e como a Americanas comprou a Blockbuster no Brasil.\n\n[CAPÍTULOS]\n\nFontes: Marc Randolph (cofundador da Netflix), em entrevistas e no livro That Will Never Work; Today I Found Out; Fortune (14/04/2023); TechCrunch (06/04/2011); Jornal do Brasil (24/01/2007); Portal Tela.\n\n#Netflix #Blockbuster #CustoOculto",
        "tags": ["netflix", "blockbuster", "netflix blockbuster", "o que aconteceu com a blockbuster", "blockbuster falência", "americanas blockbuster", "custo oculto"],
    },
    "thumbs_capa": [
        capa("Netflix x Blockbuster", [["US$ 50", G, 260], ["MILHÕES", W, 210], ["RECUSARAM", R, 190]], "Netflix · 2000"),
        capa("A Blockbuster riu", [["DA", W, 200], ["NETFLIX", R, 260], ["e faliu", G, 190]], "Netflix · 2000"),
    ],
    "thumbs": [
        {"glow": "red", "lines": [{"text": "NETFLIX", "color": "red", "size": 150}, {"text": "US$ 50 MI", "color": "gold", "size": 170}, {"text": "RECUSADA", "color": "white", "size": 120}]},
        {"glow": "gold", "lines": [{"text": "BLOCKBUSTER", "color": "gold", "size": 120}, {"text": "RIU DA", "color": "white", "size": 130}, {"text": "NETFLIX", "color": "red", "size": 160}]},
    ],
    "notes": "FATOS CHECADOS (com fonte)\n"
             "- 2000: Hastings e Randolph (e Barry McCarthy) oferecem a Netflix à Blockbuster por US$ 50 mi; Antioco recusa; Randolph diz que ele parecia segurar o riso; Netflix perdia ~US$ 50 mi/ano e tinha dívidas; Blockbuster faturava na casa de US$ 5 bi (Today I Found Out; Fortune 14/04/2023)\n"
             "- Blockbuster Online 2004, ~2 mi de assinantes em ~2 anos; Total Access 2006; Netflix perdeu 55 mil assinantes num trimestre de 2007; Icahn pressiona, Antioco sai, Keyes encarece e acaba com a troca grátis; Hastings: 'se não fosse a dívida, podiam ter nos matado' (Today I Found Out)\n"
             "- Fim da multa por atraso em 2005 custou caro (Today I Found Out)\n"
             "- 1985 primeira loja; +9 mil lojas no auge; falência 2010 com dívidas acima de US$ 900 mi; última loja em Bend, Oregon (Portal Tela, ago/2025)\n"
             "- Falência em set/2010; Dish vence leilão em abr/2011, ~US$ 320 mi (US$ 228 mi em dinheiro) (TechCrunch, 06/04/2011)\n"
             "- Americanas compra 127 lojas da Blockbuster no Brasil por R$ 186,2 mi, anúncio 24/01/2007; plano Americanas Express (Jornal do Brasil)\n"
             "- Netflix fundada em 1997 por Hastings e Randolph; streaming em 2007; +300 mi de assinantes (último número divulgado, 301,6 mi no 4º tri de 2024)\n"
             "- REVISÃO: prévia (voz clonada + abertura + material real) aprovada por Vinícius em 14/10/2026\n"
             "- Estrutura variada: abre na reunião (cold open), desmonta o mito, opinião explícita no capítulo 4.",
}

d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", "netflix")
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
json.dump(projeto, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
n = sum(len(s["text"]) for p in long_parts for s in p["sentences"])
print("tiktok:", sum(len(x["text"]) for x in tiktoks[0]["sentences"]), "caracteres;", "longo:", n, "caracteres;",
      "partes:", [sum(len(s["text"]) for s in p["sentences"]) for p in long_parts], "shorts:", [sum(len(s["text"]) for s in sh["sentences"]) for sh in shorts])

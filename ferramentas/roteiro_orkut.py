"""Monta projetos/orkut/projeto.json (Orkut: a rede que o Brasil adotou e o Google deixou morrer)."""
import json, os

G, W, R, GR, M = "gold", "white", "red", "green", "muted"


def big(*lines):
    return {"type": "bigtext", "stagger": 0.25, "lines": [list(l) for l in lines]}


def img(media, wiki, lower, fb):
    return {"type": "image", "media": media, "wiki": wiki, "lower": lower, "dim": 0.4, "fallback": fb}


def foto(media, arquivo, lower, fb):
    return img(media, ["File:" + arquivo], lower, fb)


def prt(media, url, source, fb):
    return {"type": "print", "media": media, "url": url, "source": source, "rotate": -1.0, "fallback": fb}


SAME = {"type": "same"}
S = lambda text, scene: {"text": text, "scene": scene}

# logos (Wikimedia Commons; a fábrica usa o primeiro candidato com licença livre)
LOGOS = {
    "logo_orkut": ["File:Logo ORKUT.svg", "File:Orkut.svg", "File:Orkut logo.png", "File:Orkut Logo 2.png"],
    "logo_facebook": ["File:Facebook Logo (2019).svg", "File:Facebook logo (2019).svg", "File:Facebook New Logo (2015).svg"],
    "logo_google": ["File:Google 2015 logo.svg"],
}


def logo(chave, sub=None, chave2=None, placa=False):
    d = {"type": "logo", "logo": chave, "logos": {chave: LOGOS[chave]}, "placa": placa}
    if chave2:
        d["logo2"] = chave2; d["logos"][chave2] = LOGOS[chave2]
    if sub:
        d["sub"] = sub
    return d


F_LAN = "Lan house (3318312453).jpg"


def capa(faixa, linhas, recorte, foto="lan", wiki=None, selo="Orkut · Custo Oculto"):
    return {"type": "capa", "foto": foto, "wiki": wiki or ["File:" + F_LAN], "seta": False, "recorte": recorte, "faixa": faixa,
            "linhas": linhas, "selo": selo, "logo": "logo_orkut", "logos": {"logo_orkut": LOGOS["logo_orkut"]}}


CAPA_ABERTURA = capa("12 anos depois", [["O BRASIL", W, 220], ["QUER O ORKUT", G, 190], ["DE VOLTA", R, 200]], "Orkut · 2026")

long_parts = [
    {"chapter": "", "sentences": [
        dict(S("Fala galera, aqui é o Vinícius do canal Custo Oculto.", CAPA_ABERTURA), abertura=True),
        S("Em outubro de dois mil e vinte e seis, o criador do Orkut pediu ajuda pra trazer a rede de volta.", logo("logo_orkut", "OUTUBRO DE 2026")),
        S("Em poucos dias, mais de trezentas mil pessoas assinaram o apoio.", {"type": "counter", "value": 300, "prefix": "+", "suffix": " MIL", "over": "EM POUCOS DIAS", "label": "APOIADORES DO NOVO ORKUT", "color": G, "size": 220}),
        S("E quase setenta por cento delas eram brasileiras.", {"type": "counter", "value": 69, "suffix": "%", "over": "DOS APOIADORES", "label": "SÃO DO BRASIL", "color": GR, "size": 240}),
        S("Na carta, ele escreveu: num feed, você é plateia. Numa comunidade, você é membro.", big(("NO FEED", W, 130), ("VOCÊ É PLATEIA", R, 130), ("NA COMUNIDADE", W, 120), ("VOCÊ É MEMBRO", G, 130))),
        S("Ou seja, ele quer de volta exatamente o que fez o Orkut ser o Orkut.", big(("O QUE FEZ", W, 140), ("O ORKUT SER", G, 140), ("O ORKUT", R, 170))),
        S("Uma rede social que morreu há doze anos ainda faz o Brasil inteiro sentir saudade.", big(("MORREU", W, 160), ("HÁ 12 ANOS", R, 170))),
        S("Mas por que um site americano, criado por um engenheiro turco, virou a cara do Brasil?", big(("SITE AMERICANO", W, 120), ("CRIADOR TURCO", W, 120), ("CARA DO BRASIL", G, 140))),
        S("E por que o Google, dono de tudo isso, deixou o Orkut morrer?", big(("POR QUE O GOOGLE", W, 120), ("DEIXOU MORRER?", R, 150))),
        S("Porque essa história tem um lado que pouca gente lembra, e uma decisão do Google que, na minha opinião, foi o erro de verdade.", big(("UM LADO", W, 150), ("QUE POUCA GENTE", W, 120), ("LEMBRA", G, 170))),
        S("Neste vídeo você vai ver como o Orkut nasceu, como o Brasil tomou conta, os problemas que o Google não queria, a virada do Facebook e o que pode acontecer agora.", {"type": "bullets", "items": ["COMO NASCEU", "O BRASIL TOMA CONTA", "OS PROBLEMAS", "A VIRADA DO FACEBOOK", "O QUE VEM AGORA"], "size": 78, "last_gold": True}),
    ]},
    {"chapter": "UM PROJETO DE FIM DE SEMANA", "sentences": [
        S("O Orkut foi lançado em vinte e dois de janeiro de dois mil e quatro.", {"type": "date", "month": "JANEIRO", "day": "22", "year": "2004", "tag": "LANÇAMENTO DO ORKUT"}),
        S("O nome vem do próprio criador, Orkut Büyükkökten, um engenheiro turco que trabalhava no Google.", foto("criador", "Hello Orkut Büyükkökten 2015.jpg", "Orkut Büyükkökten, criador do Orkut", big(("ORKUT", G, 200), ("BÜYÜKKÖKTEN", W, 110)))),
        S("Ele já tinha criado redes antes, quando estudava na Universidade Stanford, nos Estados Unidos.", big(("STANFORD", G, 190), ("REDES ANTES", W, 130))),
        S("O Google deixava os engenheiros usarem parte do tempo em projetos pessoais. O Orkut nasceu assim.", foto("googleplex", "Googleplex with Pride colors 2015.gk.jpg", "Sede do Google · Mountain View", big(("PROJETO", W, 160), ("PESSOAL", G, 170)))),
        S("Detalhe: o Facebook tinha sido lançado poucas semanas depois, mas só pra universitários americanos.", big(("O FACEBOOK", W, 140), ("SÓ PRA", M, 90), ("UNIVERSITÁRIOS", G, 120))),
        S("Ou seja, por algumas semanas, o Orkut nasceu antes do Facebook.", big(("O ORKUT", G, 170), ("NASCEU ANTES", W, 140))),
        S("E logo no começo veio um problema: uma empresa processou o Google dizendo que o Orkut copiava o código de outra rede social.", {"type": "stamp", "org": "JUNHO DE 2004", "title": "AFFINITY ENGINES", "stamp": "PROCESSO", "stamp_at": 0.9}),
        S("O Orkut também só entrava quem recebia convite de um amigo. E isso virou status.", big(("SÓ COM", W, 140), ("CONVITE", G, 200))),
        S("Dentro, dava pra avaliar os amigos como confiável, legal e sexy. E tinha até uma lista secreta de paqueras.", {"type": "bullets", "items": ["CONFIÁVEL", "LEGAL", "SEXY", "LISTA DE PAQUERAS"], "size": 100, "last_gold": True}),
        S("Era tudo meio ingênuo. E foi exatamente isso que pegou o brasileiro.", big(("MEIO INGÊNUO", W, 140), ("PEGOU O BRASILEIRO", G, 130))),
        S("No começo, mais da metade dos usuários eram americanos. Os brasileiros eram uns cinco por cento.", {"type": "compare", "title": "MARÇO DE 2004", "items": [["51%", "ESTADOS UNIDOS", W], ["5%", "BRASIL", G]], "size": 170, "stagger": 1.2, "vs": False}),
        S("Isso ia mudar muito rápido.", big(("ISSO IA", W, 150), ("MUDAR", R, 200))),
    ]},
    {"chapter": "O BRASIL TOMA CONTA", "sentences": [
        S("Os brasileiros chegaram em massa, um convidando o outro.", big(("UM CONVIDANDO", W, 130), ("O OUTRO", G, 180))),
        S("Internet em casa era cara e lenta, e a lan house virou ponto de encontro de muita gente.", big(("INTERNET", W, 150), ("CARA E LENTA", R, 150))),
        S("Quem não tinha computador em casa ia pra lan house, pagava por hora e corria pro Orkut.", foto("lan", F_LAN, "Lan house no Brasil", big(("LAN HOUSE", G, 170), ("POR HORA", W, 140)))),
        S("Segundo a Exame, num certo momento, onze de cada catorze milhões de brasileiros na internet estavam no Orkut.", {"type": "counter", "value": 11, "suffix": " DE 14 MI", "over": "BRASILEIROS NA INTERNET", "label": "ESTAVAM NO ORKUT", "color": G, "size": 170}),
        S("Tinha os recados no mural, os depoimentos que a pessoa precisava aprovar, e as comunidades.", {"type": "bullets", "items": ["SCRAPS", "DEPOIMENTOS", "COMUNIDADES"], "size": 110, "last_gold": True}),
        S("Comunidades como Eu odeio acordar cedo viraram um jeito de dizer quem você era.", big(("EU ODEIO", W, 150), ("ACORDAR CEDO", G, 150))),
        S("Tinha também Tô com fome e já escovei os dentes, e milhares de outras parecidas.", big(("TÔ COM FOME", W, 140), ("E JÁ ESCOVEI", G, 130), ("OS DENTES", G, 130))),
        S("Os temas coloridos do perfil, por exemplo, só existiam no Brasil e na Índia.", big(("TEMAS", G, 190), ("SÓ NO BRASIL", W, 120), ("E NA ÍNDIA", W, 120))),
        S("Pra muita gente, o Orkut foi a primeira coisa que fez na internet.", big(("A PRIMEIRA COISA", W, 120), ("NA INTERNET", G, 150))),
        S("Você não seguia ninguém. Você entrava numa comunidade e virava membro.", big(("VOCÊ NÃO SEGUIA", W, 120), ("VIRAVA MEMBRO", G, 150))),
        S("E ter muitos amigos e depoimentos no perfil virou sinal de popularidade.", big(("MUITOS AMIGOS", W, 140), ("POPULARIDADE", G, 150))),
        S("Quando o Orkut acabou, o Brasil era mais da metade de todo o tráfego do site.", {"type": "counter", "value": 55, "suffix": "%", "over": "SETEMBRO DE 2014", "label": "DO TRÁFEGO VINHA DO BRASIL", "color": GR, "size": 230}),
        S("A Índia vinha em segundo. Os Estados Unidos, que começaram com metade, tinham virado três por cento.", {"type": "compare", "title": "SETEMBRO DE 2014", "items": [["55%", "BRASIL", G], ["18%", "ÍNDIA", W], ["3%", "EUA", R]], "size": 150, "stagger": 1.0, "vs": False}),
    ]},
    {"chapter": "OS PROBLEMAS QUE O GOOGLE NÃO QUERIA", "sentences": [
        S("Só que crescer desse jeito trouxe problema junto.", big(("CRESCER", W, 160), ("TROUXE PROBLEMA", R, 140))),
        S("Teve caso de racismo e outros crimes em comunidades, que foram parar na polícia e na Justiça.", big(("CRIMES", R, 180), ("NAS COMUNIDADES", W, 120))),
        S("Em dois mil e seis, a Justiça Federal intimou o Google por causa de crimes no Orkut.", {"type": "stamp", "org": "JUSTIÇA FEDERAL · 2006", "title": "GOOGLE INTIMADO", "stamp": "ORKUT", "stamp_at": 0.9}),
        S("Um juiz mandou o Google entregar dados de usuários, com multa diária. O Google resistiu, dizendo que os dados estavam nos Estados Unidos.", {"type": "flow", "a": "JUSTIÇA", "a_sub": "pede os dados", "b": "GOOGLE", "b_sub": "dados nos EUA", "caption": "A BRIGA DOS DADOS"}),
        S("E teve vírus se espalhando pelos recados. Um deles, em dezembro de dois mil e sete, infectou mais de setecentos mil perfis.", {"type": "counter", "value": 700, "prefix": "+", "suffix": " MIL", "over": "DEZEMBRO DE 2007", "label": "PERFIS INFECTADOS POR UM VÍRUS", "color": R, "size": 210}),
        S("Antes disso, em dois mil e seis, outro vírus usava os recados pra roubar senha de banco.", big(("RECADO", W, 150), ("ROUBAVA SENHA", R, 140), ("DE BANCO", W, 120))),
        S("E não era só aqui. Na Índia, comunidades do Orkut foram parar na Justiça. E países como o Irã e a Arábia Saudita chegaram a bloquear o site.", big(("BLOQUEADO", R, 170), ("IRÃ", W, 120), ("ARÁBIA SAUDITA", W, 110))),
        S("Em dois mil e oito, o Google tomou uma decisão inédita: passou o comando do Orkut pro Google Brasil, em Minas Gerais.", logo("logo_google", "2008 · O ORKUT VIRA BRASILEIRO", placa=True)),
        S("Ou seja: a rede ficou tão brasileira que passou a ser cuidada daqui.", big(("TÃO BRASILEIRA", G, 150), ("QUE VEIO PRA CÁ", W, 130))),
        S("Pense no tamanho disso: uma empresa americana mudou o comando de um produto inteiro por causa de um país só.", big(("UM PAÍS SÓ", G, 180), ("MUDOU O COMANDO", W, 130))),
    ]},
    {"chapter": "A VIRADA DO FACEBOOK", "sentences": [
        S("Enquanto isso, o Facebook crescia no mundo inteiro.", foto("zuck", "Mark Zuckerberg - f8 2011 (6182905955).jpg", "Mark Zuckerberg · 2011", big(("O FACEBOOK", W, 150), ("CRESCIA", G, 170)))),
        S("Em dois mil e dez, o filme A Rede Social contou a história do Facebook e deixou o site ainda mais famoso.", big(("2010", G, 210), ("A REDE SOCIAL", W, 130))),
        S("O Orkut até tentou reagir com aplicativos e jogos, como o Colheita Feliz, que virou febre.", big(("COLHEITA", G, 170), ("FELIZ", G, 170))),
        S("Tinha feed de notícias, privacidade melhor e funcionava bem no celular. O Orkut não.", {"type": "compare", "title": "2011", "items": [["FEED E CELULAR", "FACEBOOK", G], ["PARADO NO TEMPO", "ORKUT", R]], "size": 120, "stagger": 1.2, "vs": True}),
        S("O código do Orkut era antigo e difícil de crescer. E o Google estava de olho em outra coisa: o Google Mais, lançado em dois mil e onze.", big(("O GOOGLE", W, 150), ("APOSTOU NO", M, 90), ("GOOGLE+", R, 190))),
        S("Em dois mil e nove, o Orkut até ganhou um visual novo. Mas chegou por convite, aos poucos, enquanto o Facebook corria.", big(("VISUAL NOVO", W, 140), ("CHEGOU", W, 110), ("DEVAGAR", R, 170))),
        S("Em dezembro de dois mil e onze, aconteceu a virada.", logo("logo_orkut", "DEZEMBRO DE 2011", "logo_facebook")),
        S("Segundo a comScore, o Facebook teve trinta e seis milhões de visitantes no Brasil. O Orkut, trinta e quatro.", {"type": "compare", "title": "BRASIL · DEZ/2011 · COMSCORE", "items": [["36,1 MI", "FACEBOOK", G], ["34,4 MI", "ORKUT", R]], "size": 170, "stagger": 1.2, "vs": True}),
        S("Num ano, o Facebook quase triplicou no Brasil. O Orkut cresceu cinco por cento.", {"type": "compare", "title": "CRESCIMENTO EM 1 ANO", "items": [["+192%", "FACEBOOK", G], ["+5%", "ORKUT", R]], "size": 180, "stagger": 1.2, "vs": False}),
        S("E a debandada começou. Primeiro os amigos, depois a família, depois todo mundo.", big(("A DEBANDADA", R, 160), ("COMEÇOU", W, 150))),
        S("Menos de três anos depois da virada, o Orkut estaria fechado.", big(("MENOS DE", W, 140), ("3 ANOS", R, 210))),
        S("Quem ficava no Orkut via o perfil dos amigos parado, com o último recado de meses atrás.", big(("PERFIS", W, 150), ("ABANDONADOS", R, 160))),
    ]},
    {"chapter": "O FIM E A MINHA OPINIÃO", "sentences": [
        S("Em trinta de junho de dois mil e catorze, o Google anunciou o fim.", {"type": "date", "month": "JUNHO", "day": "30", "year": "2014", "tag": "O GOOGLE ANUNCIA O FIM"}),
        S("O argumento foi que YouTube, Blogger e Google Mais tinham crescido mais rápido que o Orkut.", big(("OS OUTROS", W, 140), ("CRESCERAM MAIS", G, 140))),
        S("Os usuários ganharam um prazo pra salvar fotos e recados antes do desligamento.", big(("UM PRAZO", W, 150), ("PRA SALVAR", G, 150))),
        S("Em trinta de setembro de dois mil e catorze, o Orkut saiu do ar.", {"type": "stamp", "org": "30 DE SETEMBRO DE 2014", "title": "ORKUT", "stamp": "FORA DO AR", "stamp_at": 0.9}),
        S("O Google não vendeu o Orkut. Simplesmente desligou. Depois, o nome voltou pro próprio criador.", big(("NÃO VENDEU", W, 140), ("DESLIGOU", R, 190))),
        S("E aqui vai a minha opinião: o Orkut não perdeu só porque o Facebook era melhor.", {"type": "flash", "text": "MINHA\nOPINIÃO", "color": G, "size": 160}),
        S("O Google tinha a maior rede social do Brasil e da Índia nas mãos e nunca tratou isso como prioridade.", big(("NUNCA FOI", W, 150), ("PRIORIDADE", R, 170))),
        S("Apostou tudo no Google Mais, que também acabou fechando anos depois.", big(("GOOGLE+", R, 200), ("TAMBÉM FECHOU", W, 130))),
        S("Ou seja, o Google largou a rede que funcionava pra apostar numa que nunca pegou.", big(("LARGOU", W, 160), ("O QUE FUNCIONAVA", G, 130))),
        S("E o custo oculto disso ficou com a gente.", {"type": "flash", "text": "O CUSTO\nOCULTO", "color": R, "size": 170}),
        S("Fotos, depoimentos e recados de milhões de brasileiros dependiam de uma empresa que podia desligar tudo.", big(("SUAS MEMÓRIAS", W, 130), ("NA MÃO DE OUTRO", R, 130))),
        S("Deu pra baixar os dados por um tempo. Depois, o arquivo das comunidades também foi desligado.", big(("ARQUIVO", W, 150), ("DESLIGADO", R, 170))),
        S("Hoje o Facebook virou Meta, com bilhões de usuários. E o Orkut virou lembrança.", big(("O FACEBOOK", W, 140), ("VIROU META", G, 150), ("O ORKUT, LEMBRANÇA", R, 110))),
    ]},
    {"chapter": "O ORKUT VAI VOLTAR?", "sentences": [
        S("O criador do Orkut tentou de novo com outra rede, a Hello, em dois mil e dezesseis. Não vingou e foi encerrada.", big(("HELLO", G, 200), ("NÃO VINGOU", R, 150))),
        S("Em dois mil e vinte e dois, o site do Orkut voltou ao ar só com uma carta do criador.", big(("2022", G, 210), ("SÓ UMA CARTA", W, 130))),
        S("E agora, em outubro de dois mil e vinte e seis, veio a campanha de apoio.", prt("print_exame", "https://exame.com/tecnologia/o-orkut-esta-de-volta-entenda-se-a-rede-social-vai-ser-relancada/", "Exame · outubro de 2026",
                                                                                     logo("logo_orkut", "CAMPANHA DE APOIO · 2026"))),
        S("Segundo o site GD, já existe uma empresa por trás, a Orkut Inc, com o próprio Orkut como presidente.", big(("ORKUT INC", G, 180), ("JÁ EXISTE", W, 130))),
        S("A proposta é uma rede de pessoas reais e comunidades, num momento em que tem cada vez mais robô e conteúdo falso por aí.", big(("PESSOAS REAIS", G, 150), ("E COMUNIDADES", W, 130))),
        S("Ele diz que bots, deepfakes e conteúdo de inteligência artificial fazem a gente nem saber se tem uma pessoa do outro lado.", big(("BOTS", R, 160), ("DEEPFAKES", R, 150), ("TEM ALGUÉM AÍ?", W, 120))),
        S("Quem apoia recebe um cartão de apoiador pra compartilhar e chamar mais gente.", big(("CARTÃO", G, 180), ("DE APOIADOR", W, 130))),
        S("Mas atenção: assinar o apoio não cria conta, não reserva nome e não tem data de lançamento.", {"type": "stamp", "org": "O NOVO ORKUT", "title": "DATA DE LANÇAMENTO", "stamp": "NENHUMA", "stamp_at": 0.9}),
        S("Depois do Brasil, quem mais assinou foi Portugal, com quase onze por cento.", {"type": "compare", "title": "QUEM ASSINOU", "items": [["68,9%", "BRASIL", G], ["10,8%", "PORTUGAL", W]], "size": 170, "stagger": 1.2, "vs": False}),
        S("E não, os seus perfis, fotos e recados antigos não voltam.", big(("SEUS RECADOS", W, 140), ("NÃO VOLTAM", R, 160))),
        S("Eu acho que a saudade é real. Mas saudade não garante que uma rede social nova vai dar certo.", big(("SAUDADE", G, 180), ("NÃO GARANTE", W, 140))),
        S("O mais curioso é que quem pede a volta é praticamente a mesma geração que lotava as lan houses.", big(("A MESMA GERAÇÃO", W, 130), ("DAS LAN HOUSES", G, 140))),
        S("E se a nova rede sair, ela vai brigar com gigantes que hoje têm bilhões de usuários. Não é pouca coisa.", big(("CONTRA", W, 140), ("BILHÕES", R, 200), ("DE USUÁRIOS", W, 120))),
        S("E você? Voltaria pro Orkut? E qual era a sua comunidade? Conta aqui nos comentários.", big(("VOCÊ VOLTARIA?", G, 150), ("COMENTA", M, 100))),
    ]},
]

shorts = [
    {"title": "O Brasil quer o Orkut de volta",
     "sentences": [
        S("O Brasil quer o Orkut de volta.", capa("12 anos depois", [["O BRASIL", W, 220], ["QUER O ORKUT", G, 190], ["DE VOLTA", R, 200]], "Orkut · 2026")),
        S("Em outubro de dois mil e vinte e seis, o criador pediu apoio pra lançar um novo Orkut.", logo("logo_orkut", "OUTUBRO DE 2026")),
        S("Mais de trezentas mil pessoas assinaram. Quase setenta por cento, brasileiras.", {"type": "counter", "value": 300, "prefix": "+", "suffix": " MIL", "over": "APOIADORES", "label": "69% DO BRASIL", "color": G, "size": 220}),
        S("Mas assinar não cria conta nem tem data de lançamento. E os recados antigos não voltam.", {"type": "stamp", "org": "O NOVO ORKUT", "title": "DATA DE LANÇAMENTO", "stamp": "NENHUMA", "stamp_at": 0.9}),
        S("Você voltaria? Procura Orkut no Custo Oculto.", big(("VOCÊ VOLTARIA?", G, 150), ("CASO COMPLETO NO CANAL", W, 90))),
     ]},
    {"title": "O dia em que o Facebook passou o Orkut no Brasil",
     "sentences": [
        S("Dezembro de dois mil e onze. O dia em que o Facebook passou o Orkut no Brasil.", capa("Dezembro de 2011", [["O DIA", W, 220], ["QUE O ORKUT", G, 190], ["PERDEU", R, 220]], "Orkut · 2011")),
        S("Segundo a comScore, trinta e seis milhões de visitantes no Facebook. Trinta e quatro no Orkut.", {"type": "compare", "title": "BRASIL · DEZ/2011", "items": [["36,1 MI", "FACEBOOK", G], ["34,4 MI", "ORKUT", R]], "size": 170, "stagger": 1.2, "vs": True}),
        S("Num ano, o Facebook quase triplicou. O Orkut cresceu cinco por cento.", {"type": "compare", "title": "EM 1 ANO", "items": [["+192%", "FACEBOOK", G], ["+5%", "ORKUT", R]], "size": 180, "stagger": 1.2, "vs": False}),
        S("Três anos depois, o Google desligou o Orkut. Procura Orkut no Custo Oculto.", {"type": "stamp", "org": "30/09/2014", "title": "ORKUT", "stamp": "FORA DO AR", "stamp_at": 0.9}),
     ]},
]

tiktoks = [
    {"title": "O Brasil quer o Orkut de volta",
     "caption": "12 anos depois do fim, o criador do Orkut pediu apoio pra trazer a rede de volta. E quase 70% dos apoiadores são brasileiros. Mas tem um detalhe que pouca gente leu.",
     "hashtags": ["#orkut", "#nostalgia", "#redessociais", "#internet", "#curiosidades"],
     "sentences": [
        S("Doze anos depois do fim, o Brasil quer o Orkut de volta.", capa("12 anos depois", [["O BRASIL", W, 220], ["QUER O ORKUT", G, 190], ["DE VOLTA", R, 200]], "Orkut · 2026")),
        S("Em outubro de dois mil e vinte e seis, o criador, Orkut Büyükkökten, pediu apoio pra lançar uma nova rede.", logo("logo_orkut", "OUTUBRO DE 2026")),
        S("Foi ele quem criou o Orkut em dois mil e quatro, como projeto pessoal dentro do Google.", big(("2004", G, 220), ("PROJETO PESSOAL", W, 120))),
        S("Em poucos dias, mais de trezentas mil pessoas assinaram. Quase setenta por cento, brasileiras.", {"type": "counter", "value": 300, "prefix": "+", "suffix": " MIL", "over": "APOIADORES", "label": "69% DO BRASIL", "color": G, "size": 220}),
        S("Faz sentido. Quando o Orkut fechou, o Brasil era mais da metade de todo o tráfego do site.", {"type": "counter", "value": 55, "suffix": "%", "over": "SETEMBRO DE 2014", "label": "DO TRÁFEGO ERA DO BRASIL", "color": GR, "size": 230}),
        S("No auge, segundo a Exame, onze de cada catorze milhões de brasileiros na internet estavam lá.", {"type": "counter", "value": 11, "suffix": " DE 14 MI", "over": "BRASILEIROS NA INTERNET", "label": "ESTAVAM NO ORKUT", "color": G, "size": 170}),
        S("Era a rede das lan houses, dos scraps, dos depoimentos e de comunidades como Eu odeio acordar cedo.", big(("SCRAPS", G, 160), ("DEPOIMENTOS", W, 130), ("COMUNIDADES", W, 130))),
        S("A rede ficou tão brasileira que, em dois mil e oito, o Google passou o comando dela pro Brasil.", big(("O GOOGLE", W, 140), ("TROUXE PRO BRASIL", G, 130))),
        S("Mas o Facebook chegou com feed e celular, e passou o Orkut em dezembro de dois mil e onze.", logo("logo_orkut", "DEZEMBRO DE 2011", "logo_facebook")),
        S("Em dois mil e catorze, o Google desligou tudo.", {"type": "stamp", "org": "30/09/2014", "title": "ORKUT", "stamp": "FORA DO AR", "stamp_at": 0.9}),
        S("Agora o detalhe que pouca gente leu: assinar o apoio não cria conta e não tem data de lançamento.", big(("SEM CONTA", W, 150), ("SEM DATA", R, 170))),
        S("E os recados e depoimentos antigos não voltam.", big(("OS RECADOS", W, 150), ("NÃO VOLTAM", R, 160))),
        S("Você voltaria pro Orkut? Qual era sua comunidade? Comenta aqui.", big(("VOCÊ VOLTARIA?", G, 150), ("COMENTA", M, 100))),
     ]},
]


# ---------- material real ----------
TROCAS = {
    "Quem não tinha computador em casa": foto("lan", F_LAN, "Lan house no Brasil", big(("LAN HOUSE", G, 170), ("POR HORA", W, 140))),
    "Os brasileiros chegaram em massa": foto("lan2", "Lan house 3 (4541311332).jpg", "Lan house no Brasil", big(("UM CONVIDANDO", W, 130), ("O OUTRO", G, 180))),
    "Tinha os recados no mural": foto("lan3", "Lan house 2 (4541314304).jpg", "Lan house no Brasil", {"type": "bullets", "items": ["SCRAPS", "DEPOIMENTOS", "COMUNIDADES"], "size": 110, "last_gold": True}),
    "Segundo a comScore, o Facebook teve": prt("print_comscore", "https://www.comscore.com/ger/Insights/Pressemitteilung/2012/1/Facebook-Blasts-into-Top-Position-in-Brazilian-Social-Networking-Market", "comScore · janeiro de 2012",
                                             {"type": "compare", "title": "BRASIL · DEZ/2011 · COMSCORE", "items": [["36,1 MI", "FACEBOOK", G], ["34,4 MI", "ORKUT", R]], "size": 170, "stagger": 1.2, "vs": True}),
    "Segundo a Exame, num certo momento": prt("print_exame_hist", "https://exame.com/tecnologia/orkut-o-que-aconteceu-com-a-rede-social-preferida-dos-brasileiros/", "Exame",
                                            {"type": "counter", "value": 11, "suffix": " DE 14 MI", "over": "BRASILEIROS NA INTERNET", "label": "ESTAVAM NO ORKUT", "color": G, "size": 170}),
    "Segundo o site GD, já existe uma empresa": prt("print_gd", "https://gd.eurisko.com.br/2026/10/09/exclusivo-orkut-ja-tem-300-mil-apoiadores-e-uma-empresa-por-tras-do-projeto/", "GD · 09/10/2026",
                                                  big(("ORKUT INC", G, 180), ("JÁ EXISTE", W, 130))),
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
    "title": "Orkut",
    "slug": "orkut",
    "angle": "12 anos depois do fim, o Brasil quer o Orkut de volta. Como uma rede americana virou a cara do Brasil, e por que o Google deixou ela morrer.",
    "voz": {"nome": "gravada", "motor": "eleven", "eleven_voz": "Vinícius Torales"},
    "script": {"long": {"parts": long_parts}, "shorts": shorts, "tiktoks": tiktoks},
    "serie": [
        {"partes": [1, 2], "titulo": "O Brasil quer o Orkut de volta. Mas como ele nasceu?",
         "capa": capa("Parte 1 de 4", [["O BRASIL", W, 220], ["QUER O ORKUT", G, 190], ["DE VOLTA", R, 200]], "Orkut · Parte 1", selo="Orkut · Parte 1"),
         "caption": "Em outubro de 2026, mais de 300 mil pessoas pediram o Orkut de volta. Quase 70% brasileiras. Como uma rede criada por um engenheiro turco no Google virou a cara do Brasil? Parte 1 de 4.",
         "hashtags": ["#orkut", "#nostalgia", "#redessociais", "#internet", "#serie"]},
        {"partes": [3, 4], "titulo": "Lan house, scraps e comunidades: como o Brasil tomou o Orkut",
         "capa": capa("Parte 2 de 4", [["O BRASIL", W, 220], ["TOMOU", G, 230], ["O ORKUT", R, 210]], "Orkut · Parte 2", selo="Orkut · Parte 2"),
         "caption": "Lan house, scraps, depoimentos e 'Eu odeio acordar cedo'. Como o Orkut ficou tão brasileiro que o Google passou o comando pro Brasil. Parte 2 de 4.",
         "hashtags": ["#orkut", "#nostalgia", "#lanhouse", "#internet", "#serie"]},
        {"partes": [5, 6], "titulo": "O dia em que o Facebook passou o Orkut no Brasil",
         "capa": capa("Parte 3 de 4", [["O DIA", W, 220], ["QUE O ORKUT", G, 190], ["PERDEU", R, 220]], "Orkut · Parte 3", selo="Orkut · Parte 3"),
         "caption": "Dezembro de 2011: o Facebook passa o Orkut no Brasil. E três anos depois o Google desliga tudo. Na minha opinião, o erro foi do Google. Parte 3 de 4.",
         "hashtags": ["#orkut", "#facebook", "#google", "#nostalgia", "#serie"]},
        {"partes": [7], "titulo": "O Orkut vai voltar? O que ninguém te contou",
         "capa": capa("Parte 4 de 4", [["O ORKUT", W, 220], ["VAI", G, 240], ["VOLTAR?", R, 220]], "Orkut · Final", selo="Orkut · Final"),
         "caption": "Orkut Inc, 300 mil apoiadores e nenhuma data. O que é verdade sobre a volta do Orkut. Parte final.",
         "hashtags": ["#orkut", "#nostalgia", "#redessociais", "#noticias", "#serie"]},
    ],
    "meta": {
        "titles": [
            "ORKUT: Por Que o Google Deixou Morrer a Rede Que o Brasil Ainda Quer de Volta",
            "O Que Aconteceu Com o ORKUT? E Por Que o Brasil Quer Ele de Volta",
        ],
        "description": "Em outubro de 2026, o criador do Orkut pediu apoio para lançar uma nova rede, e mais de 300 mil pessoas assinaram, quase 70% brasileiras. Neste vídeo: como o Orkut nasceu dentro do Google em 2004, como o Brasil tomou conta (lan house, scraps, depoimentos e comunidades), os problemas na Justiça, a decisão de passar o comando para o Google Brasil em 2008, a virada do Facebook em dezembro de 2011, o fim em 30/09/2014 e o que se sabe sobre o novo Orkut.\n\n[CAPÍTULOS]\n\nFontes: Wikipedia (Orkut); Exame; comScore (jan/2012); GD (09/10/2026); ProPakistani (12/10/2026); Canaltech.\n\n#Orkut #Nostalgia #CustoOculto",
        "tags": ["orkut", "o que aconteceu com o orkut", "orkut vai voltar", "orkut 2026", "novo orkut", "orkut büyükkökten", "orkut facebook", "nostalgia internet", "custo oculto"],
    },
    "thumbs_capa": [
        capa("12 anos depois", [["O BRASIL", W, 210], ["QUER O ORKUT", G, 180], ["DE VOLTA", R, 200]], "Orkut · 2026"),
        capa("O Google deixou morrer", [["POR QUE", W, 200], ["O ORKUT", G, 230], ["MORREU?", R, 210]], "Orkut · 2014"),
    ],
    "thumbs": [
        {"glow": "red", "lines": [{"text": "ORKUT", "color": "red", "size": 170}, {"text": "VAI VOLTAR?", "color": "gold", "size": 140}]},
        {"glow": "gold", "lines": [{"text": "POR QUE O", "color": "white", "size": 120}, {"text": "ORKUT", "color": "gold", "size": 170}, {"text": "MORREU?", "color": "red", "size": 150}]},
    ],
    "notes": "FATOS CHECADOS (com fonte)\n"
             "- Lançado em 22/01/2004 por Orkut Büyükkökten, engenheiro do Google, como projeto pessoal; processo da Affinity Engines (InCircle) em jun/2004 (Wikipedia; Canaltech)\n"
             "- Acesso só por convite (Canaltech)\n"
             "- Tráfego 31/03/2004: EUA 51,36%, Japão 7,74%, Brasil 5,16%; 30/09/2014: Brasil 55,5%, Índia 18,4%, EUA 3,3% (Wikipedia)\n"
             "- No auge, 11 dos 14 milhões de internautas brasileiros estavam no Orkut (Exame)\n"
             "- 2006: Justiça Federal intima o Google; juiz manda entregar dados de ~24 usuários com multa diária; Google alega dados nos EUA (Wikipedia)\n"
             "- 19/12/2007: worm infecta mais de 700 mil usuários (Wikipedia)\n"
             "- 2008: Google Brasil (Minas Gerais) passa a operar o Orkut, por causa da base brasileira e das questões legais (Wikipedia; Canaltech)\n"
             "- Dez/2011: Facebook 36,1 mi de visitantes únicos no Brasil (+192% em 1 ano) vs Orkut 34,4 mi (+5%) (comScore, jan/2012)\n"
             "- Código antigo, difícil de escalar; Facebook com feed, privacidade e celular; Google+ lançado em 2011 (Exame)\n"
             "- Anúncio 30/06/2014, fim 30/09/2014; motivo oficial: YouTube, Blogger e Google+ cresceram mais (Wikipedia; Exame)\n"
             "- Exportação de dados até 2016; arquivo de comunidades desativado em 2017 (Wikipedia; Exame)\n"
             "- Hello (2016) encerrada; site reativado em abr/2022 com carta do criador (Canaltech; Olhar Digital)\n"
             "- 08/10/2026: campanha de apoio no orkut.com; sem data, não cria conta nem reserva nome (Exame; ProPakistani 12/10/2026)\n"
             "- +300 mil assinaturas em 135 países, Brasil 68,9%; Orkut Inc com Büyükkökten como CEO (GD, 09/10/2026)\n"
             "- Estrutura variada: abre na notícia de 2026 (gancho atual), história, opinião explícita no capítulo 6, pergunta final.\n"
             "- Logo do Orkut na capa e em cenas de abertura (pedido do Vinícius em 14/10/2026).",
}

d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", "orkut")
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
json.dump(projeto, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
n = sum(len(s["text"]) for p in long_parts for s in p["sentences"] if not s.get("abertura"))
print("tiktok:", sum(len(x["text"]) for x in tiktoks[0]["sentences"]), "caracteres;", "longo:", n, "caracteres;",
      "partes:", [sum(len(s["text"]) for s in p["sentences"]) for p in long_parts], "shorts:", [sum(len(s["text"]) for s in sh["sentences"]) for sh in shorts])

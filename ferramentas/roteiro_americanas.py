"""Monta projetos/americanas/projeto.json (roteiro do caso Americanas)."""
import json, os

G, W, R, GR, M = "gold", "white", "red", "green", "muted"
FOTO_LOJA = ["Lojas Americanas fachada", "Lojas Americanas", "Americanas loja"]
FOTO_B3 = ["B3 Bolsa de Valores São Paulo edifício", "Bolsa de Valores de São Paulo", "BM&FBovespa building"]
FOTO_RIO = ["Tribunal de Justiça do Estado do Rio de Janeiro", "Fórum Central Rio de Janeiro"]
FOTO_MADRI = ["Puerta de Alcalá Madrid", "Puerta de Alcalá", "Madrid skyline"]


def big(*lines):
    return {"type": "bigtext", "stagger": 0.25, "lines": [list(l) for l in lines]}


IDS = {'banco_agencia': 214695, 'papeis': 87146, 'loja_corredor': 21117, 'loja_corredor_v': 21117, 'loja_prateleira': 1735, 'escritorio_meta': 148867, 'compra_online': 108458, 'galpao': 43658, 'galpao_v': 43658, 'celular_queda': 33805, 'celular_queda_v': 33805}


def vid(media, en, lower, fb):
    d = {"type": "video", "media": media, "search": en, "search_en": en, "start": 0.0, "dim": 0.4, "lower": lower, "fallback": fb}
    if media in IDS:
        d["pixabay_id"] = IDS[media]
    return d


def img(media, wiki, lower, fb):
    return {"type": "image", "media": media, "wiki": wiki, "lower": lower, "dim": 0.4, "fallback": fb}


SAME = {"type": "same"}
S = lambda text, scene: {"text": text, "scene": scene}

long_parts = [
    {"chapter": "", "sentences": [
        S("Na noite de onze de janeiro de dois mil e vinte e três, uma das empresas mais conhecidas do Brasil soltou um comunicado.", {"type": "date", "month": "JANEIRO", "day": "11", "year": "2023", "tag": "O COMUNICADO"}),
        S("Ela tinha encontrado um buraco de vinte bilhões de reais nas próprias contas.", {"type": "counter", "value": 20, "prefix": "R$ ", "suffix": " BI", "over": "INCONSISTÊNCIAS CONTÁBEIS", "label": "NAS CONTAS DA EMPRESA", "color": R, "size": 230}),
        S("O presidente, que tinha assumido fazia nove dias, pediu demissão na mesma hora.", big(("9 DIAS", G, 220), ("NO CARGO", W, 110))),
        S("No dia seguinte, as ações caíram setenta e sete por cento.", {"type": "counter", "value": 77, "prefix": "-", "suffix": "%", "over": "AÇÕES EM UM DIA", "label": "12 DE JANEIRO DE 2023", "color": R, "size": 240}),
        S("A empresa era a Americanas.", img("loja", FOTO_LOJA, "Americanas", {"type": "flash", "text": "AMERICANAS", "tint": "red", "size": 170})),
        S("A loja onde quase todo brasileiro já comprou um chocolate, um carregador ou um presente de última hora.", vid("loja_corredor", "store aisle shopping shelves", "A loja de todo mundo", big(("A LOJA", W, 140), ("DE TODO MUNDO", G, 150)))),
        S("Meses depois, a própria empresa admitiu que não era erro. Era fraude.", {"type": "stamp", "org": "AMERICANAS · JUNHO 2023", "title": "INCONSISTÊNCIAS", "stamp": "FRAUDE", "stamp_at": 0.9}),
        S("E a conta dessa fraude caiu em gente que nunca teve nada a ver com ela.", big(("A CONTA", W, 140), ("CAIU EM QUEM?", R, 150))),
        S("Neste vídeo, você vai entender como esse buraco ficou escondido por anos, quem pagou a conta e onde o caso está hoje.", {"type": "bullets", "items": ["COMO FICOU ESCONDIDO", "QUEM PAGOU A CONTA", "ONDE ESTÁ HOJE"], "size": 90, "last_gold": True}),
    ]},
    {"chapter": "A LOJA DE TUDO", "sentences": [
        S("A Americanas nasceu em mil novecentos e vinte e nove, em Niterói, no Rio de Janeiro.", big(("1929", G, 230), ("NITERÓI · RJ", W, 110), ("A PRIMEIRA LOJA", M, 80))),
        S("A ideia era simples: vender de tudo, barato.", vid("loja_prateleira", "supermarket shelves products", "Vender de tudo, barato", big(("DE TUDO", W, 160), ("BARATO", G, 190)))),
        S("Em mil novecentos e oitenta e dois, o controle foi comprado por três sócios que depois virariam alguns dos homens mais ricos do país.", big(("1982", G, 200), ("3 SÓCIOS", W, 130), ("COMPRAM O CONTROLE", M, 80))),
        S("Jorge Paulo Lemann, Marcel Telles e Beto Sicupira.", {"type": "bullets", "items": ["JORGE PAULO LEMANN", "MARCEL TELLES", "BETO SICUPIRA"], "size": 90, "last_gold": False}),
        S("Os mesmos nomes que depois ajudaram a criar gigantes como a AB InBev, dona de algumas das cervejas mais vendidas do mundo.", big(("OS MESMOS SÓCIOS", W, 110), ("DE GIGANTES", G, 160), ("GLOBAIS", W, 110))),
        S("A Americanas virou sinônimo de eficiência. Corte de custos, metas agressivas e muito crescimento.", vid("escritorio_meta", "business meeting charts office", "Cultura de metas", big(("METAS", G, 200), ("AGRESSIVAS", W, 140)))),
        S("Depois veio a internet. O grupo criou a B2W, com a Americanas ponto com, o Submarino e o Shoptime.", vid("compra_online", "online shopping laptop credit card", "B2W · comércio eletrônico", big(("AMERICANAS.COM", G, 120), ("SUBMARINO", W, 110), ("SHOPTIME", W, 110)))),
        S("Em dois mil e vinte e um, tudo virou uma empresa só.", {"type": "flow", "a": "LOJAS AMERICANAS", "a_sub": "lojas físicas", "b": "B2W", "b_sub": "internet", "caption": "2021: UMA EMPRESA SÓ"}),
        S("No fim de dois mil e vinte e dois, eram mais de mil e oitocentas lojas e quarenta e quatro mil funcionários.", {"type": "compare", "title": "AMERICANAS · DEZ 2022", "items": [["1.882", "LOJAS", G], ["44 MIL", "FUNCIONÁRIOS", W]], "size": 170, "stagger": 1.2, "vs": False}),
        S("Por fora, era uma das empresas mais sólidas do Brasil.", vid("galpao", "warehouse boxes logistics", "Por fora: sólida", big(("POR FORA", W, 130), ("SÓLIDA", G, 190)))),
    ]},
    {"chapter": "OS NOVE DIAS", "sentences": [
        S("Em agosto de dois mil e vinte e dois, a Americanas anunciou um novo presidente.", {"type": "date", "month": "AGOSTO", "day": "19", "year": "2022", "tag": "NOVO PRESIDENTE ANUNCIADO"}),
        S("Sérgio Rial, um executivo vindo do Santander.", big(("SÉRGIO RIAL", W, 150), ("NOVO PRESIDENTE", G, 100))),
        S("Ele era um nome respeitado no mercado, e a chegada dele foi vista como um sinal de que a Americanas ia acelerar.", big(("NOME RESPEITADO", W, 120), ("NO MERCADO", G, 140))),
        S("Ele assumiu no dia dois de janeiro de dois mil e vinte e três.", {"type": "date", "month": "JANEIRO", "day": "02", "year": "2023", "tag": "PRIMEIRO DIA"}),
        S("Dois dias depois, segundo o próprio Rial, apareceu o problema.", {"type": "date", "month": "JANEIRO", "day": "04", "year": "2023", "tag": "O PROBLEMA APARECE"}),
        S("Uma dívida enorme com bancos que não aparecia do jeito certo no balanço.", vid("papeis", "stack of documents office", "O balanço", big(("UMA DÍVIDA", W, 140), ("ESCONDIDA", R, 180)))),
        S("No dia onze, a empresa contou ao mercado. E ele saiu.", {"type": "events", "row": 140, "events": [["02/01", "Rial assume", G], ["04/01", "O problema aparece", W], ["11/01", "Comunicado e saída", R]]}),
        S("Nove dias no cargo.", SAME),
        S("No dia seguinte, a ação despencou setenta e sete por cento. Foi uma das maiores quedas em um dia na história da bolsa brasileira.", img("b3", FOTO_B3, "Bolsa de valores · São Paulo", {"type": "counter", "value": 77, "prefix": "-", "suffix": "%", "over": "EM UM DIA", "label": "UMA DAS MAIORES QUEDAS DA B3", "color": R, "size": 230})),
        S("E o Rial disse uma frase que assustou ainda mais: o problema vinha de sete a nove anos.", big(("O PROBLEMA VINHA", W, 110), ("DE 7 A 9 ANOS", R, 160))),
        S("Ou seja, por anos, os números que todo mundo via não eram os números de verdade.", big(("OS NÚMEROS", W, 140), ("NÃO ERAM REAIS", R, 150))),
    ]},
    {"chapter": "COMO FUNCIONAVA", "sentences": [
        S("Pra entender o rombo, você precisa entender duas coisas.", {"type": "flash", "text": "DUAS\nCOISAS", "color": G, "size": 170}),
        S("A primeira se chama risco sacado.", big(("1", G, 200), ("RISCO SACADO", W, 140))),
        S("Funciona assim: a Americanas comprava de um fornecedor e só pagava depois.", {"type": "flow", "a": "FORNECEDOR", "a_sub": "vende para a Americanas", "b": "AMERICANAS", "b_sub": "paga depois", "caption": "RISCO SACADO"}),
        S("O fornecedor não queria esperar, então um banco pagava ele na hora.", vid("banco_agencia", "bank building facade", "O banco adianta", big(("O BANCO", W, 140), ("PAGA NA HORA", G, 150)))),
        S("E a Americanas ficava devendo para o banco, com juros.", {"type": "flow", "a": "BANCO", "a_sub": "pagou o fornecedor", "b": "AMERICANAS", "b_sub": "deve ao banco, com juros", "caption": "UMA DÍVIDA BANCÁRIA"}),
        S("Isso é uma dívida com banco. Mas, no balanço, ela aparecia como se fosse só uma conta normal com fornecedor.", {"type": "stamp", "org": "NO BALANÇO", "title": "DÍVIDA COM BANCO", "stamp": "FORNECEDOR?", "stamp_at": 0.9}),
        S("Assim, a empresa parecia muito menos endividada do que estava.", big(("PARECIA", W, 140), ("MENOS ENDIVIDADA", G, 130))),
        S("Somando esse tipo de financiamento, eram cerca de vinte bilhões de reais.", {"type": "counter", "value": 20, "prefix": "R$ ", "suffix": ",6 BI", "over": "FINANCIAMENTOS", "label": "CONTABILIZADOS DO JEITO ERRADO", "color": R, "size": 220}),
        S("A segunda coisa se chama verba de propaganda.", big(("2", G, 200), ("VERBA DE PROPAGANDA", W, 110))),
        S("Fornecedores pagam pra Americanas expor e anunciar os produtos deles. Isso é normal no varejo.", vid("loja_prateleira", "supermarket shelves products", "Verba de propaganda", big(("FORNECEDOR PAGA", W, 110), ("PRA APARECER", G, 150)))),
        S("O problema: segundo a própria empresa, foram lançados vinte e um bilhões e setecentos milhões em contratos desse tipo. Dinheiro que nunca entrou no caixa.", {"type": "counter", "value": 21, "prefix": "R$ ", "suffix": ",7 BI", "over": "VERBAS QUE NUNCA ENTRARAM", "label": "SEGUNDO A AMERICANAS", "color": R, "size": 220}),
        S("Era lucro de mentira, inflando o resultado.", big(("LUCRO", W, 170), ("DE MENTIRA", R, 170))),
        S("E por que alguém faria isso? Uma empresa com menos dívida e mais lucro vale mais na bolsa e consegue crédito mais barato.", {"type": "flow", "a": "MENOS DÍVIDA", "a_sub": "mais lucro no papel", "b": "VALE MAIS", "b_sub": "crédito mais barato", "caption": "POR QUE ESCONDER?"}),
        S("A Polícia Federal também passou a investigar se ex-diretores venderam ações sabendo do problema antes de todo mundo. Eles negam.", big(("VENDERAM ANTES?", W, 130), ("INVESTIGAÇÃO DA PF", M, 90), ("ELES NEGAM", M, 110))),
        S("Em junho de dois mil e vinte e três, a Americanas disse oficialmente que foi fraude, e apontou a diretoria anterior.", {"type": "stamp", "org": "FATO RELEVANTE · JUN 2023", "title": "A DIRETORIA ANTERIOR", "stamp": "FRAUDE", "stamp_at": 0.9}),
        S("Com juros, a conta da fraude chegou a vinte e cinco bilhões de reais.", {"type": "counter", "value": 25, "prefix": "R$ ", "suffix": ",3 BI", "over": "A FRAUDE, COM JUROS", "label": "SEGUNDO A EMPRESA E ANALISTAS", "color": R, "size": 230}),
        S("Os ex-diretores apontados negam ter participado.", big(("OS APONTADOS", W, 120), ("NEGAM", M, 170))),
    ]},
    {"chapter": "A QUEDA", "sentences": [
        S("Com o buraco exposto, os bancos queriam o dinheiro de volta.", vid("banco_agencia", "bank building facade", "Os bancos cobram", big(("OS BANCOS", W, 140), ("COBRAM", R, 180)))),
        S("Oito dias depois do comunicado, a Americanas pediu recuperação judicial.", {"type": "date", "month": "JANEIRO", "day": "19", "year": "2023", "tag": "RECUPERAÇÃO JUDICIAL"}),
        S("A dívida reconhecida: quarenta e três bilhões de reais.", {"type": "counter", "value": 43, "prefix": "R$ ", "suffix": " BI", "over": "DÍVIDA RECONHECIDA", "label": "NA RECUPERAÇÃO JUDICIAL", "color": R, "size": 230}),
        S("Pra ter ideia: quem tinha mil reais em ações da Americanas na véspera, no dia seguinte tinha cerca de duzentos e trinta.", {"type": "compare", "title": "MIL REAIS EM AÇÕES", "items": [["R$ 1.000", "11 DE JANEIRO", W], ["~R$ 230", "12 DE JANEIRO", R]], "size": 170, "stagger": 1.2, "vs": False}),
        S("Recuperação judicial é quando a empresa pede pra Justiça um tempo pra renegociar tudo, sem falir.", img("tj", FOTO_RIO, "Justiça do Rio de Janeiro", {"type": "flow", "a": "EMPRESA", "a_sub": "não consegue pagar", "b": "JUSTIÇA", "b_sub": "dá tempo pra renegociar", "caption": "RECUPERAÇÃO JUDICIAL"})),
        S("Na lista de credores estavam os maiores bancos do país.", {"type": "bullets", "title": "ALGUNS CREDORES", "items": ["BRADESCO", "SANTANDER", "ITAÚ", "BTG PACTUAL", "SAFRA"], "size": 80, "last_gold": False}),
        S("Mas também milhares de fornecedores pequenos, que venderam e não receberam.", vid("galpao", "warehouse boxes logistics", "Fornecedores na fila", big(("FORNECEDORES", W, 130), ("SEM RECEBER", R, 150)))),
        S("Em um ano, a empresa que valia cerca de dez bilhões na bolsa passou a valer menos de um bilhão.", {"type": "compare", "title": "VALOR NA BOLSA", "items": [["R$ 10 BI", "ANTES", W], ["R$ 783 MI", "UM ANO DEPOIS", R]], "size": 160, "stagger": 1.2, "vs": False}),
        S("E mais de dez mil pessoas perderam o emprego.", {"type": "compare", "title": "FUNCIONÁRIOS", "items": [["44 MIL", "DEZ 2022", W], ["33,8 MIL", "NOV 2023", R]], "size": 170, "stagger": 1.2, "vs": False}),
        S("Em menos de um ano, mais de cem lojas fecharam as portas.", {"type": "compare", "title": "LOJAS", "items": [["1.882", "DEZ 2022", W], ["1.759", "NOV 2023", R]], "size": 170, "stagger": 1.2, "vs": False}),
    ]},
    {"chapter": "QUEM PAGA A CONTA", "sentences": [
        S("Aqui está o custo oculto.", {"type": "flash", "text": "O CUSTO\nOCULTO", "tint": "red", "size": 160}),
        S("Quem pagou primeiro foi quem tinha ação da Americanas.", img("b3", FOTO_B3, "Quem tinha ação", big(("QUEM TINHA", W, 140), ("AÇÃO", R, 200)))),
        S("Muita gente comum, que achava que estava investindo numa das empresas mais seguras do país, viu o dinheiro sumir em um dia.", vid("celular_queda", "stock market chart falling red", "O dinheiro sumiu em um dia", big(("SUMIU", R, 200), ("EM UM DIA", W, 130)))),
        S("Depois, os funcionários que perderam o emprego.", big(("+10 MIL", R, 200), ("EMPREGOS A MENOS", W, 100))),
        S("Os fornecedores, que entraram numa fila pra receber com desconto e prazo longo.", big(("FORNECEDORES", W, 130), ("COM DESCONTO", R, 140), ("E PRAZO LONGO", M, 90))),
        S("E até fundos de pensão e de investimento que tinham títulos da empresa.", big(("FUNDOS", W, 150), ("TAMBÉM PERDERAM", R, 130))),
        S("Muitos investidores foram à Justiça e a câmaras de arbitragem pedindo indenização. Processos que podem levar anos.", big(("INVESTIDORES", W, 130), ("NA JUSTIÇA", G, 150), ("POR ANOS", M, 100))),
        S("E teve um efeito em cadeia. Depois do caso, os bancos ficaram mais cautelosos com esse tipo de operação, e o crédito para outras varejistas ficou mais difícil.", big(("EFEITO", W, 150), ("EM CADEIA", R, 170), ("CRÉDITO MAIS DIFÍCIL", M, 90))),
        S("Ou seja: uma fraude dentro de uma empresa vira prejuízo pra milhares de pessoas que nunca viram um balanço na vida.", big(("UMA FRAUDE", W, 140), ("MILHARES", R, 180), ("DE PREJUDICADOS", W, 100))),
        S("No plano de recuperação, os três sócios bilionários se comprometeram a colocar doze bilhões de reais na empresa.", {"type": "counter", "value": 12, "prefix": "R$ ", "suffix": " BI", "over": "APORTE DOS SÓCIOS", "label": "PREVISTO NO PLANO DE RECUPERAÇÃO", "color": G, "size": 230}),
        S("Eles sempre disseram que nunca souberam da fraude.", big(("ELES DIZEM", W, 130), ("QUE NÃO SABIAM", M, 140))),
        S("E fica a pergunta que muita gente fez: como auditorias, bancos e conselheiros não viram vinte e cinco bilhões por tantos anos?", big(("COMO", W, 160), ("NINGUÉM VIU?", R, 170))),
        S("Se esse tipo de história te interessa, segue o Custo Oculto. Toda semana tem um caso novo.", {"type": "bigtext", "stagger": 0.25, "lines": [["SEGUE O CANAL", G, 150], ["TODA SEMANA, UM CASO", W, 80]]}),
    ]},
    {"chapter": "ONDE ESTÁ HOJE", "sentences": [
        S("Em junho de dois mil e vinte e quatro, a Polícia Federal fez a Operação Disclosure.", {"type": "date", "month": "JUNHO", "day": "27", "year": "2024", "tag": "OPERAÇÃO DISCLOSURE"}),
        S("Foram quinze mandados de busca e o bloqueio de mais de quinhentos milhões de reais de ex-diretores.", {"type": "compare", "title": "OPERAÇÃO DISCLOSURE", "items": [["15", "MANDADOS DE BUSCA", W], ["+R$ 500 MI", "BLOQUEADOS", R]], "size": 160, "stagger": 1.2, "vs": False}),
        S("O ex-presidente Miguel Gutierrez, que comandou a empresa por cerca de vinte anos, estava morando na Espanha.", img("madri", FOTO_MADRI, "Madri · Espanha", big(("NA ESPANHA", G, 170), ("EX-PRESIDENTE", W, 110)))),
        S("Ele foi preso em Madri no dia seguinte, e solto logo depois.", {"type": "board", "header": "MADRI · 28/06/2024", "flip_at": 0.5, "rows": [["PRESO", "SOLTO"]]}),
        S("Mais tarde, a Justiça brasileira revogou a ordem de prisão, e ele passou a responder em liberdade.", big(("RESPONDE", W, 150), ("EM LIBERDADE", G, 150))),
        S("Em dois mil e vinte e cinco, o Ministério Público Federal denunciou treze ex-executivos e ex-funcionários.", {"type": "counter", "value": 13, "suffix": " PESSOAS", "over": "DENÚNCIA DO MPF · 2025", "label": "EX-EXECUTIVOS E EX-FUNCIONÁRIOS", "color": R, "size": 220}),
        S("Três ex-diretores fizeram delação e contaram como o esquema funcionava.", big(("3 DELAÇÕES", G, 170), ("DE EX-DIRETORES", W, 100))),
        S("A defesa de Gutierrez nega tudo. Ele diz que é um bode expiatório.", big(("A DEFESA NEGA", W, 130), ("BODE EXPIATÓRIO?", M, 130))),
        S("Até a gravação deste vídeo, não há condenação definitiva no caso.", big(("SEM CONDENAÇÃO", W, 120), ("DEFINITIVA", M, 140))),
        S("E a Americanas? Ela continua aberta, menor, e em março de dois mil e vinte e seis pediu pra sair da recuperação judicial.", {"type": "date", "month": "MARÇO", "day": "25", "year": "2026", "tag": "PEDE PRA SAIR DA RECUPERAÇÃO"}),
        S("Em setembro, a Justiça ainda não tinha decidido.", big(("SET 2026", G, 160), ("SEM DECISÃO", W, 120))),
        S("O caso deixa três sinais de alerta pra quem investe.", {"type": "flash", "text": "3 SINAIS\nDE ALERTA", "color": G, "size": 150}),
        S("Primeiro: empresa grande e famosa não é sinônimo de conta certa.", {"type": "bullets", "title": "SINAIS DE ALERTA", "items": ["FAMA NÃO É GARANTIA", "DÍVIDA FORA DO LUGAR", "LUCRO QUE NÃO VIRA CAIXA"], "size": 90, "last_gold": True, "cue_offset": 0}),
        S("Segundo: dívida que aparece com outro nome no balanço.", SAME),
        S("Terceiro: lucro que nunca vira dinheiro no caixa.", SAME),
        S("A Americanas levou noventa e quatro anos pra virar uma das marcas mais conhecidas do país. E nove dias pra tudo vir à tona.", {"type": "timeline", "start": "1929", "end": "2023", "start_sub": "primeira loja", "end_sub": "o comunicado", "big": "9 DIAS"}),
        S("A lição oculta é simples.", {"type": "flash", "text": "A LIÇÃO\nOCULTA", "tint": "red", "size": 160}),
        S("Quando os números de uma empresa parecem bons demais por tempo demais, vale perguntar quem está pagando por eles.", big(("BONS DEMAIS", W, 130), ("QUEM PAGA?", G, 180))),
        S("E, quase sempre, não é quem montou os números.", {"type": "endcard", "sub": "O CASO AMERICANAS"}),
    ]},
]


def capa(faixa, linhas, recorte, foto="loja", wiki=FOTO_LOJA, selo="Americanas · 2023"):
    return {"type": "capa", "foto": foto, "wiki": wiki, "seta": False, "recorte": recorte, "faixa": faixa, "linhas": linhas, "selo": selo}


FIM = "O caso completo está no canal."
shorts = [
    {"title": "O presidente que durou 9 dias na Americanas", "sentences": [
        S("Esse presidente durou nove dias no cargo. E saiu deixando um buraco de vinte bilhões.", capa("Ele durou 9 dias", [["E ACHOU", W, 190], ["R$ 20 BI", R, 260], ["escondidos", G, 180]], "Americanas · 2023")),
        S("Em janeiro de dois mil e vinte e três, Sérgio Rial assumiu a Americanas.", {"type": "date", "month": "JANEIRO", "day": "02", "year": "2023", "tag": "RIAL ASSUME"}),
        S("Em dois dias, achou uma dívida com bancos que não aparecia direito no balanço.", big(("DÍVIDA", W, 160), ("ESCONDIDA", R, 180))),
        S("No dia onze, contou tudo ao mercado e pediu demissão.", big(("CONTOU", W, 150), ("E SAIU", R, 190))),
        S("No dia seguinte, a ação caiu setenta e sete por cento.", {"type": "counter", "value": 77, "prefix": "-", "suffix": "%", "over": "EM UM DIA", "label": "AÇÕES DA AMERICANAS", "color": R, "size": 240}),
        S("Depois, a empresa admitiu: era fraude de vinte e cinco bilhões. Os acusados negam.", {"type": "counter", "value": 25, "prefix": "R$ ", "suffix": " BI", "over": "A FRAUDE", "label": "OS ACUSADOS NEGAM", "color": R, "size": 230}),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("ESTÁ NO CANAL", G, 140))),
    ]},
    {"title": "Como a Americanas escondeu R$ 25 bilhões", "sentences": [
        S("Como uma empresa que todo mundo conhece escondeu vinte e cinco bilhões?", capa("Como esconder", [["R$ 25", G, 260], ["BILHÕES", W, 210], ["por anos", R, 180]], "Americanas · 2023")),
        S("Primeiro: dívida com banco lançada como se fosse conta com fornecedor. Isso se chama risco sacado.", {"type": "stamp", "org": "NO BALANÇO", "title": "DÍVIDA COM BANCO", "stamp": "FORNECEDOR?", "stamp_at": 0.9}),
        S("A empresa parecia menos endividada do que estava.", big(("MENOS", W, 160), ("ENDIVIDADA", G, 160))),
        S("Segundo: verbas de propaganda de fornecedores que, segundo a própria Americanas, nunca entraram no caixa.", {"type": "counter", "value": 21, "prefix": "R$ ", "suffix": ",7 BI", "over": "VERBAS QUE NUNCA ENTRARAM", "label": "SEGUNDO A AMERICANAS", "color": R, "size": 220}),
        S("Era lucro de mentira.", big(("LUCRO", W, 170), ("DE MENTIRA", R, 170))),
        S("A empresa culpou a diretoria anterior, que nega.", big(("A DIRETORIA ANTERIOR", W, 100), ("NEGA", M, 170))),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("ESTÁ NO CANAL", G, 140))),
    ]},
    {"title": "O ex-presidente da Americanas foi preso na Espanha", "sentences": [
        S("O ex-presidente da Americanas foi preso na Espanha. E solto no dia seguinte.", capa("Preso em Madri", [["E SOLTO", W, 220], ["NO DIA", W, 180], ["SEGUINTE", R, 230]], "Caso Americanas", foto="madri", wiki=FOTO_MADRI, selo="Caso Americanas · 2024")),
        S("Miguel Gutierrez comandou a empresa por cerca de vinte anos.", big(("20 ANOS", G, 200), ("NO COMANDO", W, 120))),
        S("Depois do rombo de vinte e cinco bilhões, ele foi morar na Espanha.", big(("FOI MORAR", W, 140), ("NA ESPANHA", G, 160))),
        S("Em junho de dois mil e vinte e quatro, a Polícia Federal fez uma operação, e ele foi preso em Madri.", {"type": "date", "month": "JUNHO", "day": "28", "year": "2024", "tag": "PRESO EM MADRI"}),
        S("Depois, a Justiça revogou a prisão. Ele responde em liberdade e nega tudo.", big(("RESPONDE SOLTO", W, 120), ("E NEGA", M, 160))),
        S("Treze pessoas foram denunciadas, e não há condenação definitiva.", {"type": "counter", "value": 13, "suffix": " DENUNCIADOS", "over": "MPF · 2025", "label": "SEM CONDENAÇÃO DEFINITIVA", "color": R, "size": 200}),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("ESTÁ NO CANAL", G, 140))),
    ]},
    {"title": "Quem pagou a conta da Americanas", "sentences": [
        S("A fraude da Americanas foi de vinte e cinco bilhões. Adivinha quem pagou?", capa("R$ 25 bilhões", [["QUEM", W, 230], ["PAGOU", R, 260], ["a conta?", G, 190]], "Americanas · 2023")),
        S("Quem tinha ação perdeu setenta e sete por cento em um dia.", {"type": "counter", "value": 77, "prefix": "-", "suffix": "%", "over": "QUEM TINHA AÇÃO", "label": "EM UM DIA", "color": R, "size": 240}),
        S("Mais de dez mil pessoas perderam o emprego.", big(("+10 MIL", R, 210), ("EMPREGOS", W, 130))),
        S("Fornecedores pequenos entraram na fila pra receber com desconto.", big(("FORNECEDORES", W, 130), ("NA FILA", R, 170))),
        S("E a dívida reconhecida chegou a quarenta e três bilhões.", {"type": "counter", "value": 43, "prefix": "R$ ", "suffix": " BI", "over": "DÍVIDA RECONHECIDA", "label": "RECUPERAÇÃO JUDICIAL", "color": R, "size": 230}),
        S("Os ex-diretores acusados negam, e não há condenação definitiva.", big(("ACUSADOS NEGAM", W, 120), ("SEM CONDENAÇÃO", M, 120))),
        S(FIM, big(("O CASO COMPLETO", W, 110), ("ESTÁ NO CANAL", G, 140))),
    ]},
]

tiktoks = [
    {"title": "A loja que todo mundo conhece escondeu R$ 25 bilhões",
     "caption": "A Americanas escondeu R$ 25 bilhões por anos. O presidente durou 9 dias. Os ex-diretores acusados negam e não há condenação definitiva.",
     "hashtags": ["#americanas", "#fraude", "#investimentos", "#dinheiro", "#economia"],
     "sentences": [
        S("A loja onde você comprava chocolate escondeu vinte e cinco bilhões de reais.", capa("A loja de todo mundo", [["ESCONDEU", W, 200], ["R$ 25 BI", R, 260], ["por anos", G, 180]], "Americanas · 2023")),
        S("Em janeiro de dois mil e vinte e três, a Americanas ganhou um presidente novo.", vid("loja_corredor_v", "store aisle shopping shelves", "Americanas · janeiro de 2023", big(("PRESIDENTE", W, 140), ("NOVO", G, 190)))),
        S("Nove dias depois, ele saiu, e a empresa avisou o mercado: tinha um buraco de vinte bilhões nas contas.", {"type": "counter", "value": 20, "prefix": "R$ ", "suffix": " BI", "over": "9 DIAS DEPOIS", "label": "UM BURACO NAS CONTAS", "color": R, "size": 230}),
        S("No dia seguinte, as ações caíram setenta e sete por cento.", {"type": "counter", "value": 77, "prefix": "-", "suffix": "%", "over": "EM UM DIA", "label": "AÇÕES DA AMERICANAS", "color": R, "size": 240}),
        S("Quem tinha mil reais em ações, no dia seguinte tinha uns duzentos e trinta.", {"type": "compare", "title": "MIL REAIS EM AÇÕES", "items": [["R$ 1.000", "NA VÉSPERA", W], ["~R$ 230", "NO DIA SEGUINTE", R]], "size": 170, "stagger": 1.2, "vs": False}),
        S("Funcionava assim: dívida com banco aparecia no balanço como se fosse conta com fornecedor.", {"type": "stamp", "org": "NO BALANÇO", "title": "DÍVIDA COM BANCO", "stamp": "FORNECEDOR?", "stamp_at": 0.9}),
        S("E verbas de propaganda que nunca entraram no caixa viravam lucro.", big(("LUCRO", W, 170), ("DE MENTIRA", R, 170))),
        S("Por quê? Empresa com menos dívida e mais lucro vale mais na bolsa.", big(("MENOS DÍVIDA", W, 130), ("VALE MAIS", G, 170))),
        S("Uma semana depois, a empresa pediu recuperação judicial, com quarenta e três bilhões em dívidas.", {"type": "counter", "value": 43, "prefix": "R$ ", "suffix": " BI", "over": "RECUPERAÇÃO JUDICIAL", "label": "EM DÍVIDAS", "color": R, "size": 230}),
        S("Mais de dez mil pessoas perderam o emprego.", vid("galpao_v", "warehouse boxes logistics", "+10 mil empregos a menos", big(("+10 MIL", R, 210), ("EMPREGOS", W, 130)))),
        S("Quem tinha ação viu o dinheiro sumir. Fornecedores foram pra fila.", vid("celular_queda_v", "stock market chart falling red", "O dinheiro sumiu", big(("SUMIU", R, 200), ("EM UM DIA", W, 130)))),
        S("O ex-presidente foi preso na Espanha e solto no dia seguinte. Hoje responde em liberdade.", big(("PRESO E SOLTO", W, 130), ("NA ESPANHA", G, 150))),
        S("Treze pessoas foram denunciadas. Os acusados negam, e não há condenação definitiva.", {"type": "counter", "value": 13, "suffix": " DENUNCIADOS", "over": "MPF · 2025", "label": "OS ACUSADOS NEGAM", "color": R, "size": 200}),
        S("Você tinha ação da Americanas? Conta aqui nos comentários.", big(("VOCÊ TINHA", W, 140), ("AÇÃO?", G, 180), ("COMENTA", M, 90))),
     ]},
]


# ---------- material real (fotos do caso, prints de manchete) ----------
def prt(media, url, source, fb):
    return {"type": "print", "media": media, "url": url, "source": source, "rotate": -1.0, "fallback": fb}


def foto(media, arquivo, lower, fb):
    return img(media, ["File:" + arquivo], lower, fb)


TROCAS = {
    "A loja onde quase todo brasileiro": foto("loja_rua", "Lojas Americanas - Halfeld.jpg", "Uma loja em cada esquina", big(("A LOJA", W, 140), ("DE TODO MUNDO", G, 150))),
    "O presidente, que tinha assumido fazia nove dias": foto("rial_cae", "CAE - Comissão de Assuntos Econômicos (52777184549).jpg", "Sérgio Rial · 9 dias no cargo", big(("9 DIAS", G, 220), ("NO CARGO", W, 110))),
    "Meses depois, a própria empresa admitiu": prt("print_fraude", "https://braziljournal.com/americanas-admite-fraude-de-r-25-bi-outros-r-20-bi-estavam-contabilizados-errado", "Brazil Journal · 13/06/2023",
                                                   {"type": "stamp", "org": "AMERICANAS · JUNHO 2023", "title": "INCONSISTÊNCIAS", "stamp": "FRAUDE", "stamp_at": 0.9}),
    "A ideia era simples: vender de tudo": foto("loja_curitiba", "Lojas Americanas - Centro, Curitiba.jpg", "Vender de tudo, barato", big(("DE TUDO", W, 160), ("BARATO", G, 190))),
    "A Americanas virou sinônimo de eficiência": foto("loja_barra", "Lojas Americanas - BarraShopping.jpg", "Cultura de metas", big(("METAS", G, 200), ("AGRESSIVAS", W, 140))),
    "Por fora, era uma das empresas mais sólidas": foto("loja_express", "Lojas Americanas em Cadima Shopping.jpg", "Por fora: sólida", big(("POR FORA", W, 130), ("SÓLIDA", G, 190))),
    "Sérgio Rial, um executivo vindo do Santander": foto("rial_senado", "CAE - Comissão de Assuntos Econômicos (52777342560).jpg", "Sérgio Rial · ex-Santander", big(("SÉRGIO RIAL", W, 150), ("NOVO PRESIDENTE", G, 100))),
    "E o Rial disse uma frase que assustou": prt("print_7a9", "https://mercadoeconsumo.com.br/12/01/2023/noticias-varejo/problema-na-americanas-se-arrasta-por-cerca-de-7-a-9-anos-diz-sergio-rial/", "Mercado & Consumo · 12/01/2023",
                                               big(("O PROBLEMA VINHA", W, 110), ("DE 7 A 9 ANOS", R, 160))),
    "Fornecedores pagam pra Americanas expor": foto("loja_express", "Lojas Americanas em Cadima Shopping.jpg", "Verba de propaganda", big(("FORNECEDOR PAGA", W, 110), ("PRA APARECER", G, 150))),
    "Em junho de dois mil e vinte e três, a Americanas disse oficialmente": prt("print_fraude", "https://braziljournal.com/americanas-admite-fraude-de-r-25-bi-outros-r-20-bi-estavam-contabilizados-errado", "Brazil Journal · 13/06/2023",
                                               {"type": "stamp", "org": "FATO RELEVANTE · JUN 2023", "title": "A DIRETORIA ANTERIOR", "stamp": "FRAUDE", "stamp_at": 0.9}),
    "Oito dias depois do comunicado": prt("print_rj", "https://forbes.com.br/forbes-money/2023/01/sem-acordo-com-credores-americanas-pede-recuperacao-judicial/", "Forbes Brasil · 19/01/2023",
                                          {"type": "date", "month": "JANEIRO", "day": "19", "year": "2023", "tag": "RECUPERAÇÃO JUDICIAL"}),
    "Quem pagou primeiro foi quem tinha ação": foto("bovespa", "Bovespa, São Paulo city downtown.jpg", "Bolsa de valores · São Paulo", big(("QUEM TINHA", W, 140), ("AÇÃO", R, 200))),
    "E fica a pergunta que muita gente fez": foto("cpi", "CPI Americanas - Apresentação do plano de trabalho do relator.jpg", "CPI das Americanas · Câmara dos Deputados, 2023", big(("COMO", W, 160), ("NINGUÉM VIU?", R, 170))),
    "Foram quinze mandados de busca": foto("pf_sede", "Sede da Polícia Federal (52830107256).jpg", "Polícia Federal · Operação Disclosure", {"type": "compare", "title": "OPERAÇÃO DISCLOSURE", "items": [["15", "MANDADOS DE BUSCA", W], ["+R$ 500 MI", "BLOQUEADOS", R]], "size": 160, "stagger": 1.2, "vs": False}),
    "Ele foi preso em Madri no dia seguinte": prt("print_madri", "https://www.bloomberglinea.com.br/negocios/preso-pela-interpol-em-madri-ex-ceo-da-americanas-e-protegido-por-cidadania-espanhola/", "Bloomberg Línea · 28/06/2024",
                                                 {"type": "board", "header": "MADRI · 28/06/2024", "flip_at": 0.5, "rows": [["PRESO", "SOLTO"]]}),
    "Mais tarde, a Justiça brasileira revogou": prt("print_trf2", "https://www.conjur.com.br/2024-ago-22/trf-2-revoga-ordem-de-prisao-contra-ex-ceo-das-americanas/", "Conjur · 22/08/2024", big(("RESPONDE", W, 150), ("EM LIBERDADE", G, 150))),
    "Em dois mil e vinte e cinco, o Ministério Público Federal denunciou": prt("print_mpf", "https://diariodonordeste.verdesmares.com.br/negocios/mpf-denuncia-13-pessoas-por-fraudes-nas-americanas-novo-delator-e-revelado-1.3636088", "Diário do Nordeste · 31/03/2025",
                                                 {"type": "counter", "value": 13, "suffix": " PESSOAS", "over": "DENÚNCIA DO MPF · 2025", "label": "EX-EXECUTIVOS E EX-FUNCIONÁRIOS", "color": R, "size": 220}),
    "E a Americanas? Ela continua aberta": foto("am_hoje", "Reunião Deliberativa. Diretor-Presidente - Americanas S.A., Leonardo Coelho Pereira - Bruno Spada-Câmara dos Deputados.jpg", "Leonardo Coelho, atual presidente da Americanas, na Câmara",
                                                {"type": "date", "month": "MARÇO", "day": "25", "year": "2026", "tag": "PEDE PRA SAIR DA RECUPERAÇÃO"}),
    # Shorts
    "Em janeiro de dois mil e vinte e três, Sérgio Rial assumiu": foto("rial_senado", "CAE - Comissão de Assuntos Econômicos (52777342560).jpg", "Sérgio Rial assume a Americanas", {"type": "date", "month": "JANEIRO", "day": "02", "year": "2023", "tag": "RIAL ASSUME"}),
    "No dia onze, contou tudo ao mercado": foto("rial_cae", "CAE - Comissão de Assuntos Econômicos (52777184549).jpg", "Sérgio Rial · contou e saiu", big(("CONTOU", W, 150), ("E SAIU", R, 190))),
    "Depois, a empresa admitiu: era fraude": prt("print_fraude", "https://braziljournal.com/americanas-admite-fraude-de-r-25-bi-outros-r-20-bi-estavam-contabilizados-errado", "Brazil Journal · 13/06/2023",
                                                 {"type": "counter", "value": 25, "prefix": "R$ ", "suffix": " BI", "over": "A FRAUDE", "label": "OS ACUSADOS NEGAM", "color": R, "size": 230}),
    "A empresa culpou a diretoria anterior, que nega": prt("print_fraude", "https://braziljournal.com/americanas-admite-fraude-de-r-25-bi-outros-r-20-bi-estavam-contabilizados-errado", "Brazil Journal · 13/06/2023",
                                                 big(("A DIRETORIA ANTERIOR", W, 100), ("NEGA", M, 170))),
    "Em junho de dois mil e vinte e quatro, a Polícia Federal fez uma operação": prt("print_madri", "https://www.bloomberglinea.com.br/negocios/preso-pela-interpol-em-madri-ex-ceo-da-americanas-e-protegido-por-cidadania-espanhola/", "Bloomberg Línea · 28/06/2024",
                                                 {"type": "date", "month": "JUNHO", "day": "28", "year": "2024", "tag": "PRESO EM MADRI"}),
    "Quem tinha ação perdeu setenta e sete": foto("bovespa", "Bovespa, São Paulo city downtown.jpg", "Quem tinha ação", {"type": "counter", "value": 77, "prefix": "-", "suffix": "%", "over": "QUEM TINHA AÇÃO", "label": "EM UM DIA", "color": R, "size": 240}),
    # TikTok
    "Nove dias depois, ele saiu": foto("rial_cae", "CAE - Comissão de Assuntos Econômicos (52777184549).jpg", "Sérgio Rial · 9 dias", {"type": "counter", "value": 20, "prefix": "R$ ", "suffix": " BI", "over": "9 DIAS DEPOIS", "label": "UM BURACO NAS CONTAS", "color": R, "size": 230}),
    "O ex-presidente foi preso na Espanha e solto": prt("print_madri", "https://www.bloomberglinea.com.br/negocios/preso-pela-interpol-em-madri-ex-ceo-da-americanas-e-protegido-por-cidadania-espanhola/", "Bloomberg Línea · 28/06/2024",
                                                 big(("PRESO E SOLTO", W, 130), ("NA ESPANHA", G, 150))),
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
_faltou = [k for k in TROCAS if k not in _u]
assert not _faltou, f"trocas sem frase: {_faltou}"

projeto = {
    "title": "Americanas",
    "slug": "americanas",
    "angle": "A loja que todo brasileiro conhece escondeu R$ 25 bilhões por anos. Quando o buraco apareceu, quem pagou foi quem não tinha nada a ver.",
    "voz": {"nome": "gravada", "motor": "eleven", "eleven_voz": "Will - Deep"},
    "script": {"long": {"parts": long_parts}, "shorts": shorts, "tiktoks": tiktoks},
    "serie": [
        {"partes": [1, 2], "capa": capa("Parte 1 de 4", [["A LOJA", W, 210], ["DE TODO MUNDO", G, 170], ["ESCONDEU", R, 200]], "Americanas · Parte 1", selo="Caso Americanas · Parte 1"),
         "caption": "Americanas, parte 1: a loja que todo brasileiro conhece e o comunicado que derrubou tudo em uma noite. Segue pra ver a parte 2.",
         "hashtags": ["#americanas", "#investimentos", "#dinheiro", "#economia", "#serie"]},
        {"partes": [3, 4], "capa": capa("Parte 2 de 4", [["9 DIAS", G, 260], ["E UM BURACO", W, 170], ["DE R$ 20 BI", R, 200]], "Americanas · Parte 2", selo="Caso Americanas · Parte 2"),
         "caption": "Americanas, parte 2: o presidente que durou 9 dias e como R$ 25 bilhões ficaram escondidos no balanço. Os acusados negam.",
         "hashtags": ["#americanas", "#fraude", "#contabilidade", "#dinheiro", "#serie"]},
        {"partes": [5, 6], "capa": capa("Parte 3 de 4", [["A QUEDA", R, 240], ["e quem paga", W, 160], ["a conta", G, 200]], "Americanas · Parte 3", selo="Caso Americanas · Parte 3"),
         "caption": "Americanas, parte 3: recuperação judicial, R$ 43 bilhões em dívidas e quem pagou a conta.",
         "hashtags": ["#americanas", "#economia", "#bolsadevalores", "#dinheiro", "#serie"]},
        {"partes": [7], "capa": capa("Parte 4 de 4", [["ONDE", W, 220], ["ESTÁ", W, 220], ["HOJE", G, 260]], "Americanas · Final", selo="Caso Americanas · Final"),
         "caption": "Americanas, parte final: a operação da PF, o ex-presidente na Espanha e onde o caso está hoje. Os acusados negam e não há condenação definitiva.",
         "hashtags": ["#americanas", "#fraude", "#economia", "#dinheiro", "#serie"]},
    ],
    "meta": {
        "titles": [
            "AMERICANAS: Como Sumiram R$ 25 Bilhões da Loja Que Todo Brasileiro Conhece",
            "O Que Aconteceu Com a Americanas? A Fraude de R$ 25 Bilhões",
        ],
        "description": "Em 11 de janeiro de 2023, a Americanas revelou um buraco de R$ 20 bilhões nas contas. O novo presidente, com 9 dias no cargo, saiu, e as ações caíram 77% em um dia. Meses depois, a empresa admitiu fraude de R$ 25,3 bilhões. Neste vídeo: como o risco sacado e as verbas de propaganda esconderam a dívida, a recuperação judicial de R$ 43 bilhões, quem pagou a conta e onde o caso está hoje.\n\nOs ex-executivos acusados negam e não há condenação definitiva até a publicação deste vídeo.\n\n[CAPÍTULOS]\n\nFontes: fatos relevantes da Americanas (jan/2023 e jun/2023); Bloomberg Línea; Brazil Journal (13/06/2023); Forbes Brasil (jan/2024); Polícia Federal (Operação Disclosure); MPF (denúncia, 2025); Migalhas; Capital Aberto (abr/2026).\n\n#Americanas #Fraude #RiscoSacado #CustoOculto",
        "tags": ["americanas", "fraude americanas", "o que aconteceu com a americanas", "risco sacado", "americanas recuperação judicial", "miguel gutierrez", "custo oculto"],
    },
    "thumbs_capa": [
        capa("A loja de todo mundo", [["R$ 25 BI", R, 260], ["ESCONDIDOS", W, 200], ["por anos", G, 150]], "Americanas · 2023"),
        capa("O presidente durou", [["9 DIAS", G, 280], ["e achou", W, 170], ["R$ 20 BI", R, 220]], "Americanas · 2023"),
    ],
    "thumbs": [
        {"glow": "red", "lines": [{"text": "AMERICANAS", "color": "red", "size": 120}, {"text": "R$ 25 BI", "color": "gold", "size": 190}, {"text": "ESCONDIDOS", "color": "white", "size": 130}]},
        {"glow": "gold", "lines": [{"text": "9 DIAS", "color": "gold", "size": 190}, {"text": "NO CARGO", "color": "white", "size": 130}, {"text": "AMERICANAS", "color": "green", "size": 70, "pill": True}]},
    ],
    "notes": "FATOS CHECADOS (com fonte)\n"
             "- Rial anunciado 19/08/2022, assume 02/01/2023, descobre 04/01, fato relevante e saída 11/01/2023 (Bloomberg Línea, 28/03/2023)\n"
             "- 'Problema de 7 a 9 anos' (Mercado & Consumo, 12/01/2023)\n"
             "- Queda de 77% em um dia, a maior de uma ação na B3 desde o Plano Real; valor de ~R$ 10 bi para R$ 783 mi em um ano; dívida de R$ 43 bi na RJ; aporte de R$ 12 bi do trio; lojas 1.882 → 1.759; funcionários 44 mil → 33,8 mil (Forbes Brasil, jan/2024)\n"
             "- Fato relevante 13/06/2023: fraude; VPC R$ 21,7 bi; risco sacado R$ 18,4 bi + capital de giro R$ 2,2 bi = R$ 20,6 bi; R$ 25,3 bi com juros (estimativa citada); aponta diretoria anterior (Brazil Journal)\n"
             "- RJ pedida 19/01/2023 (Forbes, jan/2023); Operação Disclosure 27/06/2024, 15 mandados, +R$ 500 mi bloqueados; Gutierrez preso em Madri 28/06/2024, solto no dia seguinte; diz ser bode expiatório (Bloomberg Línea; Metrópoles)\n"
             "- TRF-2 revoga prisão, responde em liberdade (Conjur, 22/08/2024)\n"
             "- MPF denuncia 13 (mar/2025); delatores Flávia Carneiro, Marcelo Nunes, Fábio Abrate (Diário do Nordeste, 31/03/2025)\n"
             "- Pedido de saída da RJ 25/03/2026; sem decisão em 08/09/2026 (Capital Aberto; Brasil em Folhas)\n"
             "- 1929 Niterói; 1982 controle pelo trio do Garantia; fusão com B2W em 2021 (conhecimento geral)\n"
             "- Neutralidade: sempre dizer que os acusados negam e que não há condenação definitiva; não dizer que os sócios sabiam.",
}

d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", "americanas")
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
json.dump(projeto, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
n = sum(len(s["text"]) for p in long_parts for s in p["sentences"])
print("tiktok:", sum(len(x["text"]) for x in tiktoks[0]["sentences"]), "caracteres;", "longo:", n, "caracteres;",
      "partes:", [sum(len(s["text"]) for s in p["sentences"]) for p in long_parts], "shorts:", [sum(len(s["text"]) for s in sh["sentences"]) for sh in shorts])

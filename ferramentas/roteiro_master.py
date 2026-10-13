"""Monta projetos/banco-master/projeto.json (roteiro do caso Banco Master)."""
import json, os

G, W, R, GR, M = "gold", "white", "red", "green", "muted"
FOTO_BC = ["Banco Central do Brasil sede", "Edifício-Sede do Banco Central do Brasil", "Banco Central do Brasil"]
FOTO_FL = ["Avenida Brigadeiro Faria Lima", "Faria Lima São Paulo"]
FOTO_BRB = ["Banco de Brasília BRB", "BRB Banco de Brasília"]
FOTO_STF = ["Supremo Tribunal Federal edifício", "Supremo Tribunal Federal Brasília"]


def big(*lines):
    return {"type": "bigtext", "stagger": 0.25, "lines": [list(l) for l in lines]}


def vid(media, en, lower, fb):
    return {"type": "video", "media": media, "search": en, "search_en": en, "start": 0.0, "dim": 0.4, "lower": lower, "fallback": fb}


def img(media, wiki, lower, fb):
    return {"type": "image", "media": media, "wiki": wiki, "lower": lower, "dim": 0.4, "fallback": fb}


def prt(media, url, source, fb):
    return {"type": "print", "media": media, "url": url, "source": source, "rotate": -1.0, "fallback": fb}


SAME = {"type": "same"}
S = lambda text, scene: {"text": text, "scene": scene}

long_parts = [
    {"chapter": "", "sentences": [
        S("Um milhão e seiscentas mil pessoas colocaram dinheiro no mesmo banco.", {"type": "counter", "value": 1, "suffix": ",6 MILHÃO", "over": "INVESTIDORES", "label": "NO MESMO BANCO", "color": G, "size": 220}),
        S("Um banco que pagava muito mais do que os outros.", vid("faria_lima", "business district skyscrapers", "Banco Master · São Paulo", big(("PAGAVA", W, 120), ("MUITO MAIS", G, 170)))),
        S("Em novembro de dois mil e vinte e cinco, ele quebrou.", {"type": "date", "month": "NOVEMBRO", "day": "18", "year": "2025", "tag": "BANCO MASTER LIQUIDADO"}),
        S("E a conta, de quarenta e um bilhões de reais, não ficou só com quem investiu.", {"type": "counter", "value": 41, "prefix": "R$ ", "suffix": " BI", "over": "A CONTA", "label": "O MAIOR RESGATE DA HISTÓRIA DO FGC", "color": R, "size": 230}),
        S("Ficou com os outros bancos, com fundos de aposentadoria de servidores públicos e, de um jeito ou de outro, com você.", {"type": "bullets", "items": ["OS OUTROS BANCOS", "APOSENTADORIA DE SERVIDORES", "VOCÊ"], "size": 100, "last_gold": True}),
        S("Essa é a história do Banco Master.", {"type": "flash", "text": "BANCO\nMASTER", "tint": "red", "size": 170}),
        S("E por que essa conta pode chegar até você, mesmo que você nunca tenha ouvido falar dele.", big(("A CONTA", W, 140), ("CHEGA EM VOCÊ", R, 150))),
    ]},
    {"chapter": "O BANCO PEQUENO", "sentences": [
        S("Até pouco tempo atrás, quase ninguém tinha ouvido falar dele.", vid("rua_sp", "city street people walking", "Um banco pequeno", big(("QUASE NINGUÉM", W, 120), ("CONHECIA", G, 150)))),
        S("O banco se chamava Banco Máxima, e em dois mil e dezesseis chegou perto de quebrar.", big(("BANCO MÁXIMA", W, 140), ("2016: QUASE QUEBRA", R, 100))),
        S("Em dois mil e dezoito, quem assumiu o comando foi um empresário mineiro: Daniel Vorcaro.", big(("2018", G, 200), ("DANIEL VORCARO", W, 120), ("ASSUME O COMANDO", M, 80))),
        S("Em dois mil e vinte e um, o banco mudou de nome.", {"type": "stamp", "org": "BANCO MÁXIMA · 2021", "title": "NOVO NOME", "stamp": "MASTER", "stamp_at": 0.8}),
        S("Nascia o Banco Master, com sede na Faria Lima, o centro financeiro de São Paulo.", img("faria_lima_foto", FOTO_FL, "Faria Lima · São Paulo", big(("FARIA LIMA", G, 170), ("SÃO PAULO", W, 100)))),
        S("E o Master tinha uma estratégia simples para crescer rápido.", {"type": "flash", "text": "A ESTRATÉGIA", "color": G, "size": 150}),
        S("Pagar mais.", big(("PAGAR", W, 150), ("MAIS", G, 230))),
        S("E funcionou.", {"type": "flash", "text": "E FUNCIONOU", "color": G, "size": 160}),
        S("Em dois mil e vinte e quatro, o Master comprou o controle do Will Bank, um banco digital com mais de seis milhões de clientes.", {"type": "counter", "value": 6, "prefix": "+", "suffix": " MILHÕES", "over": "WILL BANK · 2024", "label": "DE CLIENTES", "color": G, "size": 210}),
        S("Com isso, o grupo passou de dez milhões de clientes.", {"type": "counter", "value": 10, "suffix": ",5 MILHÕES", "over": "GRUPO MASTER", "label": "DE CLIENTES", "color": G, "size": 200}),
        S("No mesmo ano, fundos ligados ao Master entraram numa operação de um bilhão de reais na Oncoclínicas, uma das maiores redes de tratamento de câncer do país.", {"type": "counter", "value": 1, "prefix": "R$ ", "suffix": " BI", "over": "2024 · ONCOCLÍNICAS", "label": "OPERAÇÃO COM FUNDOS DO MASTER", "color": G, "size": 220}),
        S("E em outubro de dois mil e vinte e quatro, uma agência de risco chegou a melhorar a nota do banco.", {"type": "stamp", "org": "AGÊNCIA DE RISCO · OUT 2024", "title": "NOTA DO BANCO MASTER", "stamp": "MELHOROU", "stamp_at": 0.9}),
        S("Por fora, o Master parecia um sucesso.", vid("escritorio", "modern office building glass", "Por fora: um sucesso", big(("POR FORA", W, 130), ("UM SUCESSO", G, 170)))),
    ]},
    {"chapter": "O CDB BOM DEMAIS", "sentences": [
        S("Quando você investe num CDB, você está emprestando dinheiro para um banco.", vid("investindo", "person using banking app smartphone", "CDB: você empresta para o banco", big(("CDB", G, 220), ("VOCÊ EMPRESTA", W, 90), ("PARA O BANCO", W, 90)))),
        S("E o banco te devolve com juros, que normalmente acompanham o CDI, a taxa que os bancos usam entre eles.", big(("O BANCO DEVOLVE", W, 110), ("COM JUROS", G, 160), ("ATRELADOS AO CDI", M, 80))),
        S("Os grandes bancos costumam pagar perto de cem por cento do CDI.", {"type": "compare", "title": "QUANTO O CDB PAGA", "items": [["~100%", "GRANDES BANCOS", W], ["140%", "BANCO MASTER", G]], "size": 190, "stagger": 1.4, "vs": False}),
        S("O Master chegou a oferecer até cento e quarenta por cento.", SAME),
        S("Era um dos investimentos mais rentáveis das plataformas de investimento.", vid("grafico", "stock market chart rising", "Nas plataformas de investimento", big(("ENTRE OS MAIS", W, 110), ("RENTÁVEIS", G, 170)))),
        S("Muita gente colocou dinheiro ali sem nunca ter entrado numa agência do Master. Só olhando a taxa.", vid("celular_v", "scrolling smartphone app", "Só olhando a taxa", big(("SÓ OLHANDO", W, 130), ("A TAXA", G, 190)))),
        S("E tinha um argumento que convencia quase todo mundo.", {"type": "flash", "text": "MAS...", "color": W, "size": 200}),
        S("É garantido pelo FGC.", {"type": "stamp", "org": "FUNDO GARANTIDOR DE CRÉDITOS", "title": "ATÉ R$ 250 MIL POR CPF", "stamp": "GARANTIDO", "stamp_at": 0.5}),
        S("O FGC é um fundo que devolve até duzentos e cinquenta mil reais por pessoa se um banco quebrar.", SAME),
        S("Então, para o investidor, o risco parecia zero.", big(("RISCO", W, 150), ("ZERO?", R, 220))),
        S("Só que um banco que paga muito mais do que os outros precisa ganhar muito mais do que os outros.", {"type": "flow", "a": "PAGA 140%", "a_sub": "para o investidor", "b": "PRECISA GANHAR", "b_sub": "ainda mais", "caption": "DE ONDE VINHA ESSE DINHEIRO?"}),
        S("E é aqui que a conta começa a não fechar.", big(("A CONTA", W, 140), ("NÃO FECHA", R, 180))),
    ]},
    {"chapter": "O BANCO PÚBLICO", "sentences": [
        S("Segundo as investigações, o Master captava dinheiro novo para cobrir compromissos antigos.", {"type": "flow", "a": "DINHEIRO NOVO", "a_sub": "de novos investidores", "b": "PAGA O ANTIGO", "b_sub": "compromissos que venciam", "caption": "SEGUNDO A INVESTIGAÇÃO"}),
        S("E os ativos que deveriam garantir tudo isso valiam menos do que o banco dizia.", big(("OS ATIVOS", W, 130), ("VALIAM MENOS", R, 160))),
        S("Em março de dois mil e vinte e cinco, apareceu uma saída.", {"type": "date", "month": "MARÇO", "day": "28", "year": "2025", "tag": "O ANÚNCIO"}),
        S("O BRB, o Banco de Brasília, anunciou que ia comprar o controle do Master.", img("brb", FOTO_BRB, "BRB · Banco de Brasília", big(("BRB", R, 220), ("BANCO DE BRASÍLIA", W, 90)))),
        S("O detalhe: o BRB é um banco público, controlado pelo governo do Distrito Federal.", {"type": "stamp", "org": "GOVERNO DO DISTRITO FEDERAL", "title": "BRB · BANCO DE BRASÍLIA", "stamp": "BANCO PÚBLICO", "stamp_at": 0.9}),
        S("Ou seja, dinheiro público.", big(("DINHEIRO", W, 160), ("PÚBLICO", R, 210))),
        S("O negócio foi aprovado pelo CADE em junho e pela Câmara Legislativa do Distrito Federal em agosto.", {"type": "events", "row": 140, "events": [["JUN 2025", "CADE aprova a compra", G], ["AGO 2025", "Câmara Legislativa do DF aprova", G], ["???", "Falta o Banco Central", R]]}),
        S("Faltava só o Banco Central.", SAME),
        S("E, segundo a Polícia Federal, antes mesmo do negócio, o BRB já tinha repassado cerca de doze bilhões de reais ao Master.", {"type": "counter", "value": 12, "prefix": "R$ ", "suffix": ",2 BI", "over": "DEZ 2024 – MAI 2025", "label": "DO BRB PARA O MASTER", "color": R, "size": 220}),
        S("Em troca, recebeu carteiras de crédito.", vid("papeis", "stack of documents office", "Carteiras de crédito", big(("CARTEIRAS", W, 140), ("DE CRÉDITO", G, 140)))),
        S("Nas amostras que a polícia analisou, nenhum desses créditos teve lastro comprovado.", {"type": "stamp", "org": "POLÍCIA FEDERAL · AMOSTRAS", "title": "CARTEIRAS DE CRÉDITO", "stamp": "SEM LASTRO", "stamp_at": 1.0}),
        S("A polícia encontrou cento e oitenta e duas mil operações de crédito com apenas doze valores diferentes.", {"type": "counter", "value": 182, "suffix": " MIL", "over": "OPERAÇÕES DE CRÉDITO", "label": "COM SÓ 12 VALORES DIFERENTES", "color": R, "size": 220}),
        S("E mais de duzentos e noventa mil clientes que já tinham aparecido em vendas anteriores.", {"type": "counter", "value": 290, "prefix": "+", "suffix": " MIL", "over": "CLIENTES REPETIDOS", "label": "EM VENDAS ANTERIORES", "color": R, "size": 220}),
        S("Para a polícia, eram créditos fabricados para dar um fôlego artificial ao Master.", big(("CRÉDITOS", W, 140), ("FABRICADOS?", R, 170), ("SEGUNDO A PF", M, 80))),
        S("Os investigados negam qualquer irregularidade.", big(("OS INVESTIGADOS", W, 110), ("NEGAM", M, 160))),
    ]},
    {"chapter": "A QUEDA", "sentences": [
        S("Em setembro de dois mil e vinte e cinco, o Banco Central barrou a compra.", img("bc", FOTO_BC, "Banco Central do Brasil", {"type": "stamp", "org": "BANCO CENTRAL · 03/09/2025", "title": "BRB COMPRA MASTER", "stamp": "NEGADO", "stamp_at": 0.8})),
        S("Sem o BRB, o Master ficou sem saída.", big(("SEM", W, 150), ("SAÍDA", R, 210))),
        S("O dinheiro novo começou a ficar mais difícil, e os compromissos continuavam vencendo.", big(("O DINHEIRO", W, 130), ("ACABANDO", R, 170))),
        S("No dia dezessete de novembro, o grupo Fictor anunciou que ia comprar o banco por três bilhões de reais.", {"type": "date", "month": "NOVEMBRO", "day": "17", "year": "2025", "tag": "PROPOSTA DE R$ 3 BI"}),
        S("Na mesma noite, Daniel Vorcaro foi preso no aeroporto.", vid("aeroporto", "private jet airport night", "17 de novembro · à noite", big(("PRESO", R, 220), ("NO AEROPORTO", W, 110)))),
        S("Segundo a polícia, ele ia embarcar num jato particular com destino a Malta.", {"type": "board", "header": "PARTIDAS · JATO PARTICULAR", "flip_at": 0.5, "rows": [["22:00", "MALTA"]]}),
        S("A defesa nega que fosse uma fuga.", SAME),
        S("No dia seguinte, o Banco Central decretou a liquidação do Master.", {"type": "stamp", "org": "BANCO CENTRAL · 18/11/2025", "title": "BANCO MASTER S.A.", "stamp": "LIQUIDADO", "stamp_at": 0.8}),
        S("Liquidar um banco é fechar as portas, afastar os donos e colocar um liquidante para vender o que sobrou e pagar quem tem a receber.", {"type": "flow", "a": "BANCO FECHADO", "a_sub": "donos afastados", "b": "LIQUIDANTE", "b_sub": "vende o que sobrou", "caption": "O QUE É LIQUIDAÇÃO"}),
        S("E a Polícia Federal lançou a Operação Compliance Zero, que investiga um rombo estimado em doze bilhões de reais.", {"type": "counter", "value": 12, "prefix": "R$ ", "suffix": " BI", "over": "OPERAÇÃO COMPLIANCE ZERO", "label": "FRAUDE ESTIMADA PELA PF", "color": R, "size": 230}),
    ]},
    {"chapter": "QUEM PAGA A CONTA", "sentences": [
        S("Aqui está o custo oculto.", {"type": "flash", "text": "O CUSTO\nOCULTO", "tint": "red", "size": 160}),
        S("O FGC precisou cobrir cerca de quarenta e um bilhões de reais para um milhão e seiscentas mil pessoas.", {"type": "counter", "value": 41, "prefix": "R$ ", "suffix": " BI", "over": "FGC · 1,6 MILHÃO DE PESSOAS", "label": "O MAIOR RESGATE EM 30 ANOS", "color": G, "size": 230}),
        S("É mais do que o dobro do maior resgate anterior, o do Bamerindus, em mil novecentos e noventa e sete, já corrigido pela inflação.", {"type": "compare", "title": "RESGATES DO FGC (CORRIGIDOS)", "items": [["R$ 19,6 BI", "BAMERINDUS · 1997", W], ["R$ 41 BI", "MASTER · 2025", R]], "size": 150, "stagger": 1.2, "vs": False}),
        S("Antes do Master, o FGC tinha cerca de cento e sessenta e um bilhões de reais. Esse resgate sozinho levou perto de um quarto do fundo.", {"type": "compare", "title": "O FUNDO GARANTIDOR", "items": [["R$ 161 BI", "O QUE O FGC TINHA", W], ["R$ 41 BI", "SÓ O MASTER", R]], "size": 160, "stagger": 1.2, "vs": False}),
        S("E quem tinha mais de duzentos e cinquenta mil reais no banco não recebe o resto pelo FGC.", {"type": "stamp", "org": "ACIMA DE R$ 250 MIL", "title": "O QUE PASSA DO LIMITE", "stamp": "MASSA FALIDA", "stamp_at": 0.9}),
        S("Entra na fila da massa falida, num processo que pode levar anos.", big(("NA FILA", W, 150), ("POR ANOS", R, 170))),
        S("Mas o FGC não é dinheiro do governo.", big(("O FGC", W, 150), ("NÃO É DO GOVERNO", G, 100))),
        S("Ele é bancado pelos próprios bancos, com uma contribuição todo mês.", vid("banco_agencia", "bank building facade", "Quem banca o FGC", big(("BANCADO PELOS", W, 110), ("BANCOS", G, 190)))),
        S("E, depois do Master, essa contribuição dobrou a partir de junho de dois mil e vinte e seis.", {"type": "compare", "title": "CONTRIBUIÇÃO MENSAL AO FGC", "items": [["0,01%", "ANTES", W], ["0,02%", "DESDE JUN/2026", R]], "size": 190, "stagger": 1.0, "vs": False}),
        S("Custo maior para os bancos costuma virar juro maior e tarifa maior para o cliente.", big(("CUSTO DO BANCO", W, 110), ("VIRA CUSTO", R, 150), ("SEU", G, 170))),
        S("E tem uma parte que o FGC não cobre.", {"type": "flash", "text": "E TEM MAIS", "color": W, "size": 170}),
        S("Pelo menos dezoito fundos de previdência de estados e municípios investiram no Master.", {"type": "counter", "value": 18, "suffix": " FUNDOS", "over": "PREVIDÊNCIA DE SERVIDORES", "label": "INVESTIRAM NO MASTER", "color": R, "size": 210}),
        S("Juntos, pelo menos um vírgula oito bilhão de reais. Só a Rioprevidência, do estado do Rio, colocou novecentos e setenta milhões.", {"type": "compare", "title": "DINHEIRO DE APOSENTADORIA NO MASTER", "items": [["R$ 1,8 BI", "18 FUNDOS PÚBLICOS", W], ["R$ 970 MI", "SÓ A RIOPREVIDÊNCIA", R]], "size": 150, "stagger": 1.2, "vs": False}),
        S("Esse dinheiro foi para letras financeiras, que não têm garantia do FGC.", {"type": "stamp", "org": "LETRAS FINANCEIRAS", "title": "GARANTIA DO FGC", "stamp": "NÃO TEM", "stamp_at": 0.8}),
        S("Se o rombo aparecer, quem cobre é o estado ou o município. Ou seja, o contribuinte.", big(("QUEM COBRE?", W, 130), ("O CONTRIBUINTE", R, 150))),
        S("Se você está gostando de entender quem paga a conta dessas histórias, se inscreve. Toda semana tem uma nova.", {"type": "bigtext", "stagger": 0.25, "lines": [["SE INSCREVE", G, 150], ["TODA SEMANA, UM CASO", W, 80]]}),
    ]},
    {"chapter": "ONDE ESTÁ HOJE", "sentences": [
        S("Depois da prisão, Vorcaro chegou a ser solto.", big(("SOLTO", W, 180), ("NOV 2025", M, 90))),
        S("Mas em março de dois mil e vinte e seis, foi preso de novo.", {"type": "date", "month": "MARÇO", "day": "04", "year": "2026", "tag": "PRESO DE NOVO"}),
        S("Em janeiro, o Banco Central já tinha liquidado também o Will Bank, o banco digital comprado pelo Master.", {"type": "stamp", "org": "BANCO CENTRAL · 21/01/2026", "title": "WILL BANK", "stamp": "LIQUIDADO", "stamp_at": 0.8}),
        S("Em abril, o ex-presidente do BRB também foi preso.", big(("ABR 2026", G, 150), ("EX-PRESIDENTE DO BRB", W, 90), ("PRESO", R, 150))),
        S("A investigação chegou a políticos de partidos diferentes e até ao Supremo Tribunal Federal.", img("stf", FOTO_STF, "Supremo Tribunal Federal", big(("POLÍTICOS", W, 130), ("E O SUPREMO", R, 140)))),
        S("Todos negam irregularidades, e ninguém foi julgado até agora.", big(("TODOS NEGAM", W, 130), ("NINGUÉM JULGADO", M, 100))),
        S("Vorcaro também nega, e as propostas de delação dele foram recusadas.", big(("DELAÇÃO", W, 150), ("RECUSADA", R, 160))),
        S("Até setembro de dois mil e vinte e seis, ele seguia preso.", big(("SET 2026", G, 160), ("SEGUE PRESO", W, 120))),
        S("E quem tinha conta no Will Bank teve que correr atrás do FGC também.", {"type": "flow", "a": "WILL BANK", "a_sub": "liquidado em jan/2026", "b": "FGC", "b_sub": "mais uma conta", "caption": "O EFEITO DOMINÓ"}),
        S("E o caso deixa três sinais de alerta que servem para qualquer investimento.", {"type": "flash", "text": "3 SINAIS\nDE ALERTA", "color": G, "size": 150}),
        S("Primeiro: uma taxa muito acima da dos concorrentes.", {"type": "bullets", "title": "SINAIS DE ALERTA", "items": ["TAXA MUITO ACIMA", "O FGC COMO ARGUMENTO", "CRESCIMENTO RÁPIDO DEMAIS"], "size": 90, "last_gold": True, "cue_offset": 0}),
        S("Segundo: quando o principal argumento de venda é a garantia do FGC, e não a saúde do banco.", SAME),
        S("Terceiro: um banco pequeno que cresce rápido demais, comprando outras empresas.", SAME),
        S("O FGC protege o seu dinheiro até um limite. Mas ele não transforma um banco ruim num banco bom.", big(("O FGC PROTEGE", W, 120), ("ATÉ UM LIMITE", G, 140))),
        S("Do banco quase quebrado até o maior resgate da história, foram só sete anos.", {"type": "timeline", "start": "2018", "end": "2025", "start_sub": "Vorcaro assume", "end_sub": "liquidação", "big": "7 ANOS"}),
        S("A lição oculta do Master é simples.", {"type": "flash", "text": "A LIÇÃO\nOCULTA", "tint": "red", "size": 160}),
        S("Quando um investimento paga muito mais do que todos os outros, alguém está pagando essa diferença.", big(("SE PAGA MUITO MAIS", W, 100), ("ALGUÉM", G, 180), ("PAGA A DIFERENÇA", W, 100))),
        S("E, no fim, quase nunca é só quem ganhou o retorno.", {"type": "endcard", "sub": "O CASO BANCO MASTER"}),
    ]},
]


def capa(faixa, linhas, recorte, wiki, foto):
    return {"type": "capa", "foto": foto, "wiki": wiki, "seta": False, "recorte": recorte, "faixa": faixa, "linhas": linhas, "selo": "Banco Master · 2025"}


shorts = [
    {"title": "1,6 milhão de pessoas no mesmo banco. E ele quebrou.", "sentences": [
        S("Um milhão e seiscentas mil pessoas colocaram dinheiro no mesmo banco. E ele quebrou.", capa("1,6 milhão de pessoas", [["no mesmo", W, 190], ["BANCO", G, 250], ["que quebrou", R, 180]], "Banco Master · 2025", FOTO_BC, "bc")),
        S("O Banco Master pagava até cento e quarenta por cento do CDI.", {"type": "compare", "title": "QUANTO O CDB PAGAVA", "items": [["~100%", "GRANDES BANCOS", W], ["140%", "MASTER", G]], "size": 190, "stagger": 1.0, "vs": False}),
        S("Em novembro de dois mil e vinte e cinco, o Banco Central liquidou o banco.", {"type": "stamp", "org": "BANCO CENTRAL · 18/11/2025", "title": "BANCO MASTER S.A.", "stamp": "LIQUIDADO", "stamp_at": 0.8}),
        S("E o fundo que garante os investimentos teve que devolver quarenta e um bilhões de reais.", {"type": "counter", "value": 41, "prefix": "R$ ", "suffix": " BI", "over": "FGC", "label": "O MAIOR RESGATE DA HISTÓRIA", "color": R, "size": 230}),
        S("O maior resgate da história do Brasil.", vid("dinheiro_v", "money banknotes counting", "O maior resgate da história", big(("O MAIOR", W, 150), ("DA HISTÓRIA", R, 150)))),
        S("O caso completo está no canal.", {"type": "endcard", "sub": "O CASO BANCO MASTER"}),
    ]},
    {"title": "Esse CDB pagava 140% do CDI. Era bom demais.", "sentences": [
        S("Esse banco pagava cento e quarenta por cento do CDI. Parecia bom demais. E era.", capa("Esse CDB pagava", [["140%", G, 260], ["do CDI", W, 200], ["era bom demais", R, 150]], "Banco Master", FOTO_FL, "faria_lima_foto")),
        S("Quem paga muito mais precisa ganhar muito mais.", {"type": "flow", "a": "PAGA 140%", "a_sub": "para você", "b": "PRECISA GANHAR", "b_sub": "ainda mais", "caption": "DE ONDE VINHA?"}),
        S("Segundo a investigação, o dinheiro de quem entrava pagava quem já estava lá.", {"type": "flow", "a": "DINHEIRO NOVO", "a_sub": "de quem entrava", "b": "PAGA O ANTIGO", "b_sub": "de quem já estava", "caption": "SEGUNDO A INVESTIGAÇÃO"}),
        S("O banco quebrou em novembro de dois mil e vinte e cinco.", {"type": "stamp", "org": "BANCO CENTRAL · 18/11/2025", "title": "BANCO MASTER S.A.", "stamp": "LIQUIDADO", "stamp_at": 0.8}),
        S("Quando um investimento paga muito mais que os outros, alguém está pagando a diferença.", big(("ALGUÉM", G, 190), ("PAGA A DIFERENÇA", W, 110))),
        S("O caso completo está no canal.", {"type": "endcard", "sub": "O CASO BANCO MASTER"}),
    ]},
    {"title": "Preso no aeroporto no dia em que o banco ia ser vendido", "sentences": [
        S("O dono do banco foi preso no aeroporto no mesmo dia em que anunciaram a venda do banco.", capa("O dono do banco", [["PRESO", R, 260], ["no aeroporto", W, 190]], "17 de novembro de 2025", FOTO_BC, "bc")),
        S("Dezessete de novembro de dois mil e vinte e cinco. Um grupo anuncia que vai comprar o Banco Master por três bilhões de reais.", {"type": "date", "month": "NOVEMBRO", "day": "17", "year": "2025", "tag": "PROPOSTA DE R$ 3 BI"}),
        S("Na mesma noite, Daniel Vorcaro é preso, segundo a polícia, antes de embarcar num jato para Malta.", vid("aeroporto_v", "private jet airport night", "17 de novembro · à noite", {"type": "board", "header": "PARTIDAS · JATO PARTICULAR", "flip_at": 0.5, "rows": [["22:00", "MALTA"]]})),
        S("A defesa nega que fosse uma fuga.", big(("A DEFESA", W, 130), ("NEGA", M, 180))),
        S("No dia seguinte, o banco foi liquidado.", {"type": "stamp", "org": "BANCO CENTRAL · 18/11/2025", "title": "BANCO MASTER S.A.", "stamp": "LIQUIDADO", "stamp_at": 0.7}),
        S("O caso completo está no canal.", {"type": "endcard", "sub": "O CASO BANCO MASTER"}),
    ]},
    {"title": "Você pode estar pagando a conta do Banco Master", "sentences": [
        S("Você pode estar pagando a conta do Banco Master, mesmo sem nunca ter investido nele.", capa("Você pode estar", [["PAGANDO", R, 250], ["a conta", W, 200], ["do Master", G, 190]], "Banco Master", FOTO_BC, "bc")),
        S("Dezoito fundos de aposentadoria de servidores públicos colocaram dinheiro no banco.", {"type": "counter", "value": 18, "suffix": " FUNDOS", "over": "PREVIDÊNCIA DE SERVIDORES", "label": "INVESTIRAM NO MASTER", "color": R, "size": 210}),
        S("Pelo menos um vírgula oito bilhão de reais, em papéis que o FGC não garante.", {"type": "stamp", "org": "LETRAS FINANCEIRAS · R$ 1,8 BI", "title": "GARANTIA DO FGC", "stamp": "NÃO TEM", "stamp_at": 0.8}),
        S("Se faltar dinheiro, quem cobre é o estado ou o município. Ou seja, o contribuinte.", big(("QUEM COBRE?", W, 130), ("O CONTRIBUINTE", R, 150))),
        S("E os bancos passaram a pagar o dobro para o fundo garantidor. Custo que costuma chegar no cliente.", {"type": "compare", "title": "CONTRIBUIÇÃO AO FGC", "items": [["0,01%", "ANTES", W], ["0,02%", "AGORA", R]], "size": 190, "stagger": 1.0, "vs": False}),
        S("O caso completo está no canal.", {"type": "endcard", "sub": "O CASO BANCO MASTER"}),
    ]},
]

projeto = {
    "title": "Banco Master",
    "slug": "banco-master",
    "angle": "Um banco pagava muito mais que os outros. Quando quebrou, a conta de R$ 41 bilhões ficou com o sistema inteiro.",
    "voz": {"nome": "gravada"},
    "script": {"long": {"parts": long_parts}, "shorts": shorts},
    "meta": {
        "titles": [
            "BANCO MASTER: O Banco Que Quebrou e Deixou Uma Conta de R$ 41 Bilhões",
            "O Que Aconteceu Com o Banco Master? Quem Paga a Conta",
        ],
        "description": "O Banco Master pagava até 140% do CDI e atraiu 1,6 milhão de investidores. Em novembro de 2025, o Banco Central liquidou o banco, e o FGC fez o maior resgate da sua história: cerca de R$ 41 bilhões. Neste vídeo: como o banco cresceu, a tentativa de venda para o BRB, a prisão de Daniel Vorcaro, e quem paga a conta.\n\nOs investigados negam irregularidades e ninguém foi julgado até a publicação deste vídeo. Este vídeo não toma partido político.\n\n[CAPÍTULOS]\n\nFontes: Banco Central do Brasil; Polícia Federal (Operação Compliance Zero); STF; FGC; Bloomberg Línea (18/11/2025); IstoÉ Dinheiro; Poder360; Jornal de Brasília (09/01/2026).\n\n#BancoMaster #FGC #Vorcaro #CDB #CustoOculto",
        "tags": ["banco master", "o que aconteceu com o banco master", "fgc banco master", "daniel vorcaro", "cdb banco master", "brb banco master", "custo oculto"],
    },
    "thumbs": [
        {"glow": "red", "lines": [{"text": "BANCO MASTER", "color": "red", "size": 110}, {"text": "QUEM PAGA", "color": "white", "size": 150}, {"text": "R$ 41 BI?", "color": "gold", "size": 190}]},
        {"glow": "gold", "lines": [{"text": "140% DO CDI", "color": "gold", "size": 150}, {"text": "ERA BOM", "color": "white", "size": 130}, {"text": "DEMAIS", "color": "red", "size": 150}, {"text": "BANCO MASTER", "color": "green", "size": 70, "pill": True}]},
    ],
    "notes": "FATOS CHECADOS (com fonte)\n"
             "- 1,6 milhão de investidores; FGC deve cobrir ~R$ 41 bi; CDBs até 140% do CDI; PF estima fraude de ~R$ 12 bi (Bloomberg Línea, 18/11/2025)\n"
             "- Maior resgate em 30 anos de FGC; Bamerindus R$ 19,6 bi corrigido; FGC tinha ~R$ 161 bi; contribuição mensal de 0,01% para 0,02% desde 01/06/2026 (IstoÉ Dinheiro)\n"
             "- Banco Máxima; quase insolvente em 2016; Vorcaro assume em 2018; vira Master em 2021 (Wikipedia, Banco Master)\n"
             "- BRB anuncia compra 28/03/2025; BC nega 03/09/2025; Fictor R$ 3 bi em 17/11; prisão no aeroporto (jato para Malta) em 17/11; liquidação e Compliance Zero em 18/11; solto em 29/11; preso de novo 04/03/2026; Will Bank liquidado 21/01/2026; ex-presidente do BRB preso 16/04/2026; delações recusadas mai-jun/2026; segue preso até 11/09/2026 (Wikipedia, Banco Master scandal)\n"
             "- BRB repassou ~R$ 12,2 bi ao Master (dez/2024 a mai/2025) em cessões de crédito; nas amostras da PF nenhum crédito com lastro comprovado (Poder360)\n"
             "- 18 RPPS, ao menos R$ 1,8 bi em Letras Financeiras (sem FGC); Rioprevidência R$ 970 mi; entes cobrem o rombo (Jornal de Brasília, 09/01/2026)\n"
             "- Neutralidade: não citar nomes de políticos/ministros; sempre dizer que investigados negam e ninguém foi julgado.",
}

d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "projetos", "banco-master")
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
json.dump(projeto, open(os.path.join(d, "projeto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
n = sum(len(s["text"]) for p in long_parts for s in p["sentences"])
print("longo:", n, "caracteres ~", round(n / 15 / 60, 1), "min;", "shorts:", [sum(len(s["text"]) for s in sh["sentences"]) for sh in shorts])

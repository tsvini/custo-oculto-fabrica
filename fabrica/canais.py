"""Configuração por idioma/canal. O projeto escolhe com "idioma": "pt" (padrão) ou "en" no projeto.json.

pt → Custo Oculto (YT_REFRESH_TOKEN, Amazon Brasil custooculto-20)
en → Hidden Cost  (YT_REFRESH_TOKEN_EN, Amazon EUA hiddencost-20)

Links de afiliado: em projeto.json → "meta": {"afiliados": [{"titulo": "...", "asin": "B0..."} ou {"titulo": "...", "busca": "termos"}]}
"""
from urllib.parse import quote_plus

CANAIS = {
    "pt": {
        "nome": "Custo Oculto",
        "token_env": "YT_REFRESH_TOKEN",
        "yt_lang": "pt-BR",
        "legenda_nome": "Português",
        "whisper": "pt",
        "amazon": "https://www.amazon.com.br",
        "tag": "custooculto-20",
        "afiliados_titulo": "📚 Para saber mais sobre o caso:",
        "afiliados_aviso": "Como Associado da Amazon, eu ganho com compras qualificadas.",
        "shorts_desc": "A história completa está no vídeo longo do canal.",
        "serie_desc": "Série em {tot} partes. O caso completo está no canal.",
        "serie_titulo": "{titulo}: parte {n} de {tot}",
        "caso_completo": "▶ Caso completo:",
        "creditos": "Imagens de apoio:",
        "pl_todos": ("Todos os casos | Custo Oculto", "Todos os casos do Custo Oculto, um atrás do outro: fraudes, quedas e quem pagou a conta."),
        "pl_caso": ("Caso {t} | Custo Oculto", "O caso {t} completo e em partes."),
    },
    "en": {
        "nome": "Hidden Cost",
        "token_env": "YT_REFRESH_TOKEN_EN",
        "yt_lang": "en",
        "legenda_nome": "English",
        "whisper": "en",
        "amazon": "https://www.amazon.com",
        "tag": "hiddencost-20",
        "afiliados_titulo": "📚 Learn more about this case:",
        "afiliados_aviso": "As an Amazon Associate I earn from qualifying purchases.",
        "shorts_desc": "The full story is on the channel.",
        "serie_desc": "A {tot}-part series. The full case is on the channel.",
        "serie_titulo": "{titulo}: part {n} of {tot}",
        "caso_completo": "▶ Full case:",
        "creditos": "Supporting images:",
        "pl_todos": ("All cases | Hidden Cost", "Every Hidden Cost case, back to back: frauds, collapses and who paid the price."),
        "pl_caso": ("The {t} case | Hidden Cost", "The full {t} case, in parts."),
    },
}


def canal(idioma=None):
    return CANAIS.get((idioma or "pt").lower()[:2], CANAIS["pt"])


def link_amazon(item, idioma=None):
    c = canal(idioma)
    if item.get("asin"):
        return f"{c['amazon']}/dp/{item['asin']}?tag={c['tag']}"
    if item.get("url"):
        u = item["url"]
        return u if "tag=" in u else u + ("&" if "?" in u else "?") + f"tag={c['tag']}"
    return f"{c['amazon']}/s?k={quote_plus(item.get('busca') or item.get('titulo', ''))}&tag={c['tag']}"


def bloco_afiliados(meta, idioma=None):
    itens = (meta or {}).get("afiliados") or []
    if not itens:
        return ""
    c = canal(idioma)
    linhas = [c["afiliados_titulo"]] + [f"• {i.get('titulo', '').strip()}: {link_amazon(i, idioma)}" for i in itens]
    return "\n".join(linhas) + "\n" + c["afiliados_aviso"]

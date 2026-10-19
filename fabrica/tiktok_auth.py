"""Conexão da conta do TikTok com a fábrica (sem colar token em lugar nenhum).

1. Você abre https://tsvini.github.io/custo-oculto-fabrica/tiktok/ e clica em "Conectar TikTok".
2. O TikTok devolve um código de uso único na página de retorno.
3. Você cola o código no workflow "Conectar TikTok" (Actions → Run workflow).
4. Este script troca o código pelo refresh token e guarda ele CRIPTOGRAFADO em tiktok_token.enc
   (chave derivada do segredo TIKTOK_CLIENT_SECRET, que só existe no GitHub). Nada sensível aparece no log.
"""
import base64, hashlib, json, os, sys

import requests
from cryptography.fernet import Fernet

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(RAIZ, "tiktok_token.enc")
REDIRECT = "https://tsvini.github.io/custo-oculto-fabrica/tiktok/callback.html"


def _f():
    seg = os.environ.get("TIKTOK_CLIENT_SECRET", "").strip()
    if not seg:
        raise RuntimeError("sem TIKTOK_CLIENT_SECRET")
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(("custo-oculto|" + seg).encode()).digest()))


def guardar(dados):
    open(ARQ, "wb").write(_f().encrypt(json.dumps(dados).encode()))


def ler():
    if not os.path.exists(ARQ):
        return {}
    return json.loads(_f().decrypt(open(ARQ, "rb").read()))


def trocar(codigo):
    r = requests.post("https://open.tiktokapis.com/v2/oauth/token/", headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=60,
                      data={"client_key": os.environ["TIKTOK_CLIENT_KEY"].strip(), "client_secret": os.environ["TIKTOK_CLIENT_SECRET"].strip(),
                            "code": codigo.strip(), "grant_type": "authorization_code", "redirect_uri": REDIRECT})
    j = r.json()
    if "refresh_token" not in j:
        print(f"::error title=TikTok::a troca do código falhou: {j.get('error')} {j.get('error_description', '')}", flush=True)
        sys.exit(1)
    guardar({"refresh_token": j["refresh_token"], "open_id": j.get("open_id"), "scope": j.get("scope")})
    print(f"::notice title=TikTok conectado::permissões: {j.get('scope')} · o token ficou guardado criptografado", flush=True)


if __name__ == "__main__":
    trocar(sys.argv[1])

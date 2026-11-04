"""Mostra plano, saldo e data de renovação da ElevenLabs (só leitura)."""
import datetime as dt, os, requests
s = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": os.environ["ELEVENLABS_KEY"].strip()}, timeout=60).json()
r = s.get("next_character_count_reset_unix")
print(f"::notice title=ElevenLabs::plano {s.get('tier')} | usados {s.get('character_count')} de {s.get('character_limit')} | renova em {dt.datetime.fromtimestamp(r, dt.timezone(dt.timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M') if r else '?'} | status {s.get('status')} | rollover {s.get('max_credit_limit_extension') or s.get('can_extend_character_limit')}")

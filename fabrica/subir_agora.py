"""("quando": data/hora ISO agenda para esse horário; sem "quando", publica em poucos minutos)
Sobe uma versão nova de um vídeo já aprovado e publica em poucos minutos (subir_agora.json).

O vídeo antigo com o mesmo nome fica privado (renomeado para <nome>_antigo no registro). Nada é apagado.
"""
import datetime as dt, json, os, subprocess, tempfile

from .publicar import token, subir_video, REG, RAIZ, nota, BRT


def main():
    cfg = json.load(open(os.path.join(RAIZ, "subir_agora.json"), encoding="utf8"))
    if cfg.get("feito"):
        nota("Subir agora", "já feito, nada a fazer"); return
    reg = json.load(open(REG, encoding="utf8"))
    with tempfile.TemporaryDirectory() as d:
        arq = os.path.join(d, "v.mp4")
        subprocess.run(["gh", "release", "download", "videos", "-p", cfg["arquivo"], "-O", arq, "--clobber"], check=True)
        quando = dt.datetime.fromisoformat(cfg["quando"]) if cfg.get("quando") else dt.datetime.now(BRT) + dt.timedelta(minutes=cfg.get("minutos", 3))
        meta = {"titulo": cfg["titulo"][:100], "descricao": cfg["descricao"], "tags": cfg.get("tags", []), "caso": None, "idioma": "pt"}  # caso None = marca conteúdo sintético (cenas de IA)
        v = subir_video(token("pt"), arq, meta, quando)
    for r in reg:
        if r.get("nome") == cfg["nome"]:
            r["nome"] = cfg["nome"] + "_antigo"; r["substituido_por"] = v["id"]
    reg.append({"nome": cfg["nome"], "tipo": "short", "idioma": "pt", "titulo": meta["titulo"], "video_id": v["id"], "caso": cfg.get("caso"),
                "caso_titulo": cfg.get("caso_titulo"), "publishAt": quando.isoformat(), "status": "private"})
    json.dump(reg, open(REG, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    cfg["feito"] = v["id"]; json.dump(cfg, open(os.path.join(RAIZ, "subir_agora.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    nota("Subiu e vai ao ar", f"{meta['titulo']} → {quando:%d/%m %H:%M} (youtu.be/{v['id']})")


if __name__ == "__main__":
    main()

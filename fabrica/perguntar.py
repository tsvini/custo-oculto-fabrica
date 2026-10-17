"""Pergunta livre ao Gemini sobre um vídeo do release (ele assiste e escuta).
python -m fabrica.perguntar <nome_do_mp4_sem_extensao> "<pergunta>"
"""
import base64, json, os, subprocess, sys, tempfile
from .sonoplastia import _gemini


def main(nome, pergunta):
    with tempfile.TemporaryDirectory() as d:
        v = os.path.join(d, "v.mp4"); leve = os.path.join(d, "l.mp4")
        subprocess.run(["gh", "release", "download", "videos", "-p", nome + ".mp4", "-O", v, "--clobber"], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-vf", "scale=360:-2,fps=12", "-c:v", "libx264", "-b:v", "500k", "-c:a", "aac", "-b:a", "128k", leve], check=True)
        dado = base64.b64encode(open(leve, "rb").read()).decode()
    r = _gemini([{"text": pergunta + "\nResponda em JSON: {\"resposta\": \"texto completo da sua resposta, com quebras de linha\"}"},
                 {"inline_data": {"mime_type": "video/mp4", "data": dado}}])
    txt = (r or {}).get("resposta") if isinstance(r, dict) else None
    txt = txt or (json.dumps(r, ensure_ascii=False) if r else "sem resposta")
    os.makedirs("previas", exist_ok=True)
    open(os.path.join("previas", f"resposta_{nome}.md"), "w", encoding="utf8").write(f"# Pergunta\n{pergunta}\n\n# Resposta do Gemini\n{txt}\n")
    print("::notice title=Resposta do Gemini::" + txt.replace("\n", " | ")[:3500], flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

#!/bin/bash
# aula 46: um Chromium comum (com barra de endereço) abrindo a API de treino: digita jsonplaceholder.typicode.com/posts/1 e mostra o JSON
mkdir -p cg_saida
Xvfb :99 -screen 0 1920x1080x24 & sleep 2
export DISPLAY=:99
openbox & sleep 1
foto() { ffmpeg -loglevel error -y -f x11grab -video_size 1920x1080 -i :99 -frames:v 1 "cg_saida/$1.png"; }
gravar() { ffmpeg -loglevel error -y -f x11grab -framerate 30 -video_size 1920x1080 -i :99 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -g 1 "cg_saida/$1.mp4" & FF=$!; sleep 1; }
parar() { sleep 1; kill -INT $FF; wait $FF 2>/dev/null; }
CHROME=$(node -e "console.log(require('playwright').chromium.executablePath())")
"$CHROME" --no-first-run --no-default-browser-check --disable-infobars --user-data-dir=/tmp/perfil --window-position=0,0 --window-size=1920,1080 --lang=pt-BR https://jsonplaceholder.typicode.com/ > cg_saida/chrome_log.txt 2>&1 &
for i in $(seq 1 30); do W=$(xdotool search --onlyvisible --class chrom | head -1); [ -n "$W" ] && break; sleep 1; done
xdotool windowmove $W 0 0; xdotool windowsize $W 1920 1080; sleep 6
xdotool key ctrl+plus; sleep 0.3; xdotool key ctrl+plus; sleep 0.3; xdotool key ctrl+plus; sleep 1.5   # 150%: dá pra ler o JSON no vídeo
foto api46_inicio
gravar api46_abre
sleep 0.8; xdotool key ctrl+l; sleep 0.6
xdotool type --delay 95 "jsonplaceholder.typicode.com/posts/1"; sleep 0.7; xdotool key Return; sleep 4
parar
foto api46_json

#!/bin/bash
# prepara a tela virtual e abre o codegen com as janelas lado a lado (navegador 1180x1080 à esquerda, Inspector à direita)
mkdir -p cg_saida
Xvfb :99 -screen 0 1920x1080x24 & sleep 2
export DISPLAY=:99
openbox & sleep 1
npx playwright codegen https://www.saucedemo.com/ > cg_saida/cg_log.txt 2>&1 &
for i in $(seq 1 30); do B=$(xdotool search --onlyvisible --name "Swag Labs" | head -1); I=$(xdotool search --onlyvisible --name "Playwright Inspector" | head -1); [ -n "$B" ] && [ -n "$I" ] && break; sleep 1; done
xdotool windowmove $B 0 0; xdotool windowsize $B 1180 1080
xdotool windowmove $I 1180 0; xdotool windowsize $I 740 1080
sleep 7
foto() { ffmpeg -loglevel error -y -f x11grab -video_size 1920x1080 -i :99 -frames:v 1 "cg_saida/$1.png"; }

# move o mouse suave até (x,y) em n passos
mover() { local x0 y0; eval $(xdotool getmouselocation --shell); x0=$X; y0=$Y; local n=${3:-25}; for i in $(seq 1 $n); do xdotool mousemove $(( x0 + ($1 - x0) * i / n )) $(( y0 + ($2 - y0) * i / n )); sleep 0.02; done; }
gravar() { ffmpeg -loglevel error -y -f x11grab -framerate 30 -video_size 1920x1080 -i :99 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -g 1 "cg_saida/$1.mp4" & FF=$!; sleep 1; }
parar() { sleep 1; kill -INT $FF; wait $FF 2>/dev/null; }

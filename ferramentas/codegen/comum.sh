#!/bin/bash
# prepara a tela virtual e abre o codegen com as janelas lado a lado (navegador 1180x1080 à esquerda, Inspector à direita)
mkdir -p cg_saida
Xvfb :99 -screen 0 1920x1080x24 & sleep 2
export DISPLAY=:99
openbox & sleep 1
npx playwright codegen --viewport-size=1160,860 https://www.saucedemo.com/ > cg_saida/cg_log.txt 2>&1 &
for i in $(seq 1 30); do B=$(xdotool search --onlyvisible --name "Swag Labs" | head -1); I=$(xdotool search --onlyvisible --name "Playwright Inspector" | head -1); [ -n "$B" ] && [ -n "$I" ] && break; sleep 1; done
xdotool windowmove $B 0 0; xdotool windowsize $B 1180 1080
xdotool windowmove $I 1180 0; xdotool windowsize $I 740 1080
sleep 2
foto() { ffmpeg -loglevel error -y -f x11grab -video_size 1920x1080 -i :99 -frames:v 1 "cg_saida/$1.png"; }

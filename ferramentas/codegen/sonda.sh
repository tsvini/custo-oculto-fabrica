#!/bin/bash
# descobre onde as janelas do codegen aparecem na tela virtual
set -x
mkdir -p cg_saida
Xvfb :99 -screen 0 1920x1080x24 & sleep 2
export DISPLAY=:99
openbox & sleep 1
npx playwright codegen https://www.saucedemo.com/ > cg_saida/cg_log.txt 2>&1 &
sleep 12
xdotool search --onlyvisible --name "." 2>/dev/null | while read w; do echo "$w | $(xdotool getwindowname $w) | $(xdotool getwindowgeometry $w | tr '\n' ' ')"; done > cg_saida/cg_janelas.txt
cat cg_saida/cg_janelas.txt
ffmpeg -loglevel error -y -f x11grab -video_size 1920x1080 -i :99 -frames:v 1 cg_saida/cg_tela1.png

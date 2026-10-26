#!/bin/bash
source ../../ferramentas/codegen/comum.sh
foto cg_tela2
xdotool search --onlyvisible --name "." | while read w; do echo "$w | $(xdotool getwindowname $w) | $(xdotool getwindowgeometry $w | tr '\n' ' ')"; done > cg_saida/cg_janelas.txt

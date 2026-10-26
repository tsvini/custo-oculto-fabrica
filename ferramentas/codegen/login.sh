#!/bin/bash
# aula 19: o codegen gravando de verdade o login e um "Assert text" no título Products
source ../../ferramentas/codegen/comum.sh
foto cg_p0
gravar cg_login
mover 590 262; sleep 0.4; xdotool click 1; sleep 0.5; xdotool type --delay 110 "standard_user"; sleep 0.8
mover 590 316; sleep 0.4; xdotool click 1; sleep 0.5; xdotool type --delay 110 "secret_sauce"; sleep 0.8
mover 590 414; sleep 0.5; xdotool click 1; sleep 3
foto cg_p1
parar

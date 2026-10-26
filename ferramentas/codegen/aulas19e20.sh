#!/bin/bash
# gravações reais do codegen para as aulas 19 e 20 (um vídeo por trecho de narração)
source ../../ferramentas/codegen/comum.sh
foto cg_abre
# ---- aula 19 ----
gravar cg19_usuario
mover 590 262; sleep 0.4; xdotool click 1; sleep 0.6; xdotool type --delay 120 "standard_user"; sleep 1.2
parar
gravar cg19_senha
mover 590 316; sleep 0.4; xdotool click 1; sleep 0.5; xdotool type --delay 110 "secret_sauce"; sleep 0.8
mover 590 414; sleep 0.5; xdotool click 1; sleep 2.5
parar
gravar cg19_assert
mover 672 103; sleep 0.6; xdotool click 1; sleep 0.8
mover 62 172; sleep 0.8; xdotool click 1; sleep 1.2
foto cg19_assert_dialogo
mover 380 214; sleep 0.6; xdotool click 1; sleep 1.8
parar
foto cg19_fim
# ---- aula 20 ----
gravar cg20_pick
mover 608 103; sleep 0.6; xdotool click 1; sleep 1.5
parar
gravar cg20_passa
mover 62 172; sleep 1.6; mover 496 442; sleep 1.6; mover 34 116; sleep 1.6; mover 1050 172; sleep 1.6
parar
foto cg20_passa
mover 608 103; sleep 0.4; xdotool click 1; sleep 0.8   # desliga o Pick locator (tira o destaque antigo)
mover 608 62 8; mover 1300 62 20; mover 1300 1000 15; sleep 0.3   # sai pela barra de endereço (fora da página), sem passar por cima de nenhum elemento
gravar cg20_um
mover 1209 916 10; sleep 0.5; xdotool click 1; sleep 0.8
mover 1500 960; sleep 0.3; xdotool click 1; sleep 0.4
xdotool type --delay 70 "getByRole('button', { name: 'Open Menu' })"; sleep 2.5
parar
foto cg20_um
gravar cg20_varios
xdotool key ctrl+a; sleep 0.3; xdotool type --delay 70 "getByRole('button', { name: 'Add to cart' })"; sleep 3
xdotool key ctrl+a; sleep 0.3; xdotool type --delay 70 "getByText('Mochila')"; sleep 3
parar
foto cg20_nenhum

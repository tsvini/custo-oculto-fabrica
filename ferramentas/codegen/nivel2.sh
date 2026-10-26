#!/bin/bash
# gravações reais do nível 2 (Chromium com a janela de verdade, numa tela virtual)
mkdir -p cg_saida
Xvfb :99 -screen 0 1920x1080x24 & sleep 2
export DISPLAY=:99
openbox & sleep 1
sudo sysctl -q -w kernel.apparmor_restrict_unprivileged_userns=0 || true
node ../../ferramentas/codegen/nivel2_gravar.js
ls -la cg_saida

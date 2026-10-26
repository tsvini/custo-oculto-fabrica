#!/bin/bash
# gravações reais do nível 2 (Chromium com a janela de verdade, numa tela virtual)
mkdir -p cg_saida
Xvfb :99 -screen 0 1920x1080x24 & sleep 2
export DISPLAY=:99
openbox & sleep 1
sudo sysctl -q -w kernel.apparmor_restrict_unprivileged_userns=0 || true
export NODE_PATH="$(pwd)/node_modules"  # o script mora em ferramentas/: sem isso o require('@playwright/test') não acha o pacote
node ../../ferramentas/codegen/nivel2_gravar.js > cg_saida/nivel2_log.txt 2>&1; echo "saiu com $?" >> cg_saida/nivel2_log.txt
ls -la cg_saida

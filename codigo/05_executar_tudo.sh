#!/bin/bash
# Reproduz base, testes, amostragem e planilhas (semente = matrícula 241021515)
set -e; cd "$(dirname "$0")"
python3 01_gerar_base.py && python3 02_testes_auditoria.py && python3 03_amostragem_mus.py && python3 04_gerar_planilhas.py

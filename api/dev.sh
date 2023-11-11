#!/bin/bash
source .venv/bin/activate
python3 -m flask --app src/app run --debug

# Vivo me esquecendo de usar o venv quando abro terminais novos

#!/bin/bash
mkdir Pyz-Env
cp main.py Pyz-Env/__main__.py
pip install -r requirements.txt --target ./Pyz-Env
python -m zipapp Pyz-Env -p "/usr/bin/env python3" -o Torned.pyz -c
rm -r Pyz-Env
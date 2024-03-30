#!/bin/bash
mkdir Pyz-Env
cp main.py Pyz-Env/__main__.py
cp Functions.py Classes.py Pyz-Env/ 
pip install -r requirements.txt --target ./Pyz-Env
python -m zipapp Pyz-Env -p "/usr/bin/env python3" -o Torned.pyz -c
rm -r Pyz-Env

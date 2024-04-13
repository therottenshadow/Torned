#!/bin/bash
mkdir Pyz-Env
cp -r ./src/* Pyz-Env/
pip install --isolated --python "/usr/bin/env python3" -r requirements.txt --target ./Pyz-Env
python -m zipapp Pyz-Env -p "/usr/bin/env python3" -o Torned.pyz -c
rm -r Pyz-Env

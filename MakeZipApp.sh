#!/bin/bash
mkdir --parents Pyz-Env/cogs
cp -r ./src/*.py ./src/resources Pyz-Env/
cp ./src/cogs/*.py Pyz-Env/cogs
pip install --isolated -r requirements.txt --target ./Pyz-Env
python -m zipapp Pyz-Env -p "/usr/bin/env python3" -o Torned.pyz -c
rm -r Pyz-Env

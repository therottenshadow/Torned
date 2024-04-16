#!/bin/bash
mkdir -v --parents Pyz-Env/cogs
cp -v LICENSE README.md Pyz-Env/
cp -v ./src/*.py Pyz-Env/
cp -vr ./src/resources Pyz-Env
cp  -v ./src/cogs/*.py Pyz-Env/cogs
pip install --isolated -r requirements.txt --target ./Pyz-Env
python -m zipapp Pyz-Env -m "main:main" -p "/usr/bin/env python3" -o Torned.pyz -c
rm -vr Pyz-Env
#!/bin/bash
if [ -d ./src/.venv ]; then
  source ./src/.venv/bin/activate
  pip --disable-pip-version-check list --outdated --format=json | python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 pip install -U
  pip install -r ./requirements.txt
  python -m zipapp src --python="./src/.venv/bin/python3" --output="./Torned.pyz"
else
  python -m venv ./src/.venv
  sleep 5
  source ./src/.venv/bin/activate
  pip --disable-pip-version-check list --outdated --format=json | python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 pip install -U
  pip install -r ./requirements.txt
  python -m zipapp src --python="./src/.venv/bin/python3" --output="./Torned.pyz"
fi


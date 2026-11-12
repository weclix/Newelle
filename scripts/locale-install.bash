#!/bin/bash
cd ..

python -m build --wheel
cd dist

pip install --break-system-packages --force-reinstall newelle-1.6.1-py3-none-any.whl

#!/usr/bin/env bash
# Build the wheel and install Newelle for the current user.
# The app goes into its own venv; the launcher, desktop file and icons are
# linked into ~/.local so the desktop finds them.
set -euo pipefail

cd "$(dirname "$0")/.."
venv="${NEWELLE_VENV:-$HOME/.local/share/newelle-venv}"
share="$HOME/.local/share"

rm -rf build dist
python3 -m venv --system-site-packages "$venv"
"$venv/bin/pip" install --quiet build
"$venv/bin/python" -m build --wheel
"$venv/bin/pip" install --force-reinstall --no-deps dist/newelle-*.whl

mkdir -p "$HOME/.local/bin" "$share/applications" \
         "$share/icons/hicolor/scalable/apps" "$share/icons/hicolor/symbolic/apps"
ln -sf "$venv/bin/newelle" "$HOME/.local/bin/newelle"
ln -sf "$venv/share/applications/io.github.qwersyk.Newelle.desktop" "$share/applications/"
ln -sf "$venv/share/icons/hicolor/scalable/apps/io.github.qwersyk.Newelle.svg" \
       "$share/icons/hicolor/scalable/apps/"
ln -sf "$venv/share/icons/hicolor/symbolic/apps/io.github.qwersyk.Newelle-symbolic.svg" \
       "$share/icons/hicolor/symbolic/apps/"
update-desktop-database "$share/applications" 2>/dev/null || true
gtk-update-icon-cache -q -t -f "$share/icons/hicolor" 2>/dev/null || true

#!/bin/bash
meson setup --prefix="$HOME/.local" _build
ninja -C _build install

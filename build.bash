#!/bin/bash
meson setup --prefix="/usr/local" _build
ninja -C _build install

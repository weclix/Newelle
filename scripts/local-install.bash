cd ..
rm -rf _build
meson setup _build  --prefix=~/.local --buildtype=release
meson compile -C _build
meson install -C _build 

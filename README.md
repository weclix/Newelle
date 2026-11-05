<h1 align="center">
  <img src="https://raw.githubusercontent.com/qwersyk/Newelle/master/data/icons/hicolor/scalable/apps/io.github.qwersyk.Newelle.svg" alt="Newelle" width="192" height="192"/>
  <br>
  Newelle
</h1>

<p align="center">A GTK4 desktop AI assistant for Linux, packaged as a Python wheel.</p>

This is a trimmed-down fork of [qwersyk/Newelle](https://github.com/qwersyk/Newelle). It keeps the chat,
agent and tooling features, talks to models through a single OpenAI-compatible provider, and runs directly
on the host instead of inside Flatpak.

<picture>
  <source srcset="https://raw.githubusercontent.com/qwersyk/Newelle/master/screenshots/7.png" media="(prefers-color-scheme: light)">
  <source srcset="https://raw.githubusercontent.com/qwersyk/Newelle/master/screenshots/7b.png" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/qwersyk/Newelle/master/screenshots/7.png" alt="Newelle main window">
</picture>

## Differences from upstream

| Area | This fork |
|------|-----------|
| LLM, embeddings, image generation | OpenAI-compatible API only (set the endpoint to use any compatible server) |
| Voice | No text-to-speech. Speech-to-text is only used for wake words; dictation requires *Direct audio input* with an audio-capable model |
| Web search | SearXNG only |
| Removed | Interfaces (Telegram, API, MCP server), built-in browser and file manager tabs, thread editing, Semantic (LlamaIndex) memory, runtime pip installer |
| Packaging | setuptools wheel instead of meson; no Flatpak, Flathub or nix builds |

## Features

- 💻 **Terminal command execution**: run commands suggested by the AI, with file permission prompts
- 🛠 **Tools and MCP**: add tools through MCP servers or extensions, with tool search
- ✨ **Skills**: compatible with Claude and Codex skill folders
- 🧩 **Extensions**: add your own features and tools
- 🤖 **Subagents and scheduled tasks**: delegate work and run tasks in the background
- 🗣 **Voice and call mode**: talk to audio-capable models, with wake word support
- 🧠 **Memory**: long-term memory, user summary and agentic memory
- 💼 **Chat with documents**: RAG over your own files
- 🔎 **Web search and website reading**: prefix a URL with `#` in the prompt to read it
- 🖼 **Image generation** through OpenAI-compatible image APIs
- 🖍 **Context management**: summarize and drop old messages to fit the context window
- 👤 **Profiles and workspaces**: switch settings sets and project folders
- 💬 **Multichat, branching, folders and editing**: run chats side by side, branch from any message, organize and edit them
- 📝 **Rich formatting**: Markdown, LaTeX and Mermaid
## Installation

### Requirements

- Python 3.14 or newer
- From your distribution: GTK 4, libadwaita, GtkSourceView 5, VTE (GTK 4), WebKitGTK 6.0, librsvg,
  PyGObject and pycairo, including their GObject Introspection typelibs. pip cannot install these.
- Build tools: `glib-compile-resources`, `glib-compile-schemas` (glib2) and `msgfmt` (gettext)
- Optional: GStreamer for screen recording, gtk4-layer-shell for Voice Mode positioning on Wayland

On Arch Linux:

```sh
sudo pacman -S python python-gobject python-cairo gtk4 libadwaita gtksourceview5 vte4 \
    webkitgtk-6.0 librsvg glib2 gettext portaudio
```

### Install for the current user

```sh
git clone https://github.com/weclix/Newelle.git
cd Newelle
bash scripts/locale-install.bash
```

The script builds a wheel and installs it into `~/.local/share/newelle-venv` (created with
`--system-site-packages` so it can see the system GTK bindings). It then links the `newelle` launcher into
`~/.local/bin` and the desktop file and icons into `~/.local/share`. Set `NEWELLE_VENV` to use a different
venv path. Run the script again to update.

### Arch Linux package

`scripts/PKGBUILD` builds the current `master` branch as the `com.tritium.newelle` package:

```sh
cd scripts
makepkg -si
```

`newspaper4k` (website reading) is not in the official repositories; install it from the AUR or with pip.

### Build packages only

```sh
python -m build
```

The sdist and wheel are written to `dist/`. If you install the wheel into your own venv, create it with
`--system-site-packages`.

## Getting started

1. Open **Settings** and select the OpenAI provider.
2. Enter your API key, and change **API Endpoint** if you use another OpenAI-compatible server
   (for example a local llama.cpp, vLLM or Ollama server).
3. Pick a model and start chatting.

For voice input, enable **Direct audio input** in the voice settings and use a model that accepts audio.

## Usage

### Command line

| Option | Description |
|--------|-------------|
| `newelle --mini` | Start in mini window mode |
| `newelle --voice` | Toggle one-shot Voice Mode (reuses a running instance) |
| `newelle --run-action ACTION` | Run an application action, for example `new_chat` |

The mini window and Voice Mode are also available as actions in the desktop launcher.

### Mini window

A lightweight window you can bind to a global shortcut. In your desktop environment, bind a key
(for example `Ctrl+Space`) to `newelle --mini`. On GNOME you may also want new windows to open centered:

```sh
gsettings set org.gnome.mutter center-new-windows true
```

### Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | New chat |
| `Ctrl+L` | Focus the message box |
| `Ctrl+G` | Start/stop recording |
| `Ctrl+I` | Toggle Voice Mode |
| `Ctrl+D` | Toggle mini window |
| `Ctrl+Q` | Stop generation |
| `Ctrl+R` | Reload chat |
| `Ctrl++` / `Ctrl+-` | Zoom in / out |

### Extensions

Newelle can load [community extensions](https://github.com/topics/newelle-extension). Extensions written for
upstream that add TTS handlers or interfaces will have those parts ignored.

## Files and settings

| Path | Contents |
|------|----------|
| `~/.config/Newelle/` | Chats, profiles, extensions, skills, MCP servers, models, memory |
| `~/.cache/Newelle/` | Caches |
| dconf `/io/github/qwersyk/Newelle/` | Application settings |

## Security

Newelle runs without a sandbox. The AI can run terminal commands and read or edit files with your user's
permissions, subject to the file permission settings. Review commands before running them, and be careful
about what you share with third-party model providers.

## Credits

Newelle is developed by [qwersyk](https://github.com/qwersyk) and
[FrancescoCaracciolo](https://github.com/FrancescoCaracciolo) and contributors. See also
[Nyarch Assistant](https://github.com/NyarchLinux/NyarchAssistant), another Newelle fork.

## License

GPL-3.0-or-later. See [COPYING](COPYING).

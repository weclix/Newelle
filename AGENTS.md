# Newelle 项目说明

## 项目概述

Newelle 是一个 Linux 桌面 AI 助手应用，使用 Python + GTK4 开发，以 Python 包（wheel）形式构建。

- **构建系统**：setuptools（`pyproject.toml` + `setup.py`），不使用 meson
- **源码目录**：`src/`（打包为 `newelle` 包，`package_dir={"newelle": "src"}`）
- **核心模块**：`controller.py`、`main.py`、`window.py`、`modes.py`、`skills.py`、`tools.py`、`extensions.py`、`ui_controller.py`

## 当前变更记录（2026-11-04）

### 变更主题：合并上游 `qwersyk/Newelle` 至 `8420fcd6`

合入上游 13 个提交（多数为本地已有的 cherry-pick），实际新增：

- `controller.move_chat_to_top_level` 及 `window.py` 拖放调用：把分支聊天拖出后变为顶层聊天
- `main.py` About 窗口鸣谢更新
- `data/mcp_servers.json` 新增 Parallel Search、Sem 条目，appdata、图标更新

冲突处理：

| 文件 | 处理 |
|------|------|
| `meson.build`、`src/meson.build` | 保持删除（meson 已剥离） |
| `modules/*.json`（10 个） | 保持删除（Flatpak 已剥离） |
| `src/constants.py` | 保留本地剥离状态；新增的 Outcrawl 导入与 `AVAILABLE_WEBSEARCH` 条目注释保留 |
| `src/handlers/websearch/__init__.py` | 保留本地；Outcrawl 导入与 `__all__` 注释保留 |
| `src/handlers/websearch/outcrawl_handler.py` | 已删除（`# 已剥离：Outcrawl 网页搜索`） |

- 上游的 `deepseek_handler.py` 本地早已删除，未恢复；`AVAILABLE_WEBSEARCH` 仍只有 `searxng`
- `po/en.po` 合入了 Outcrawl 的翻译条目，属自动生成内容，未处理
- 上游 HTTPS 地址在本机连接超时，使用 `ssh://git@ssh.github.com:443/qwersyk/Newelle.git` 拉取

### 变更主题：TTS 组件剥离与 STT 听写功能收窄

剥离 TTS 全部组件，并把 STT 收窄为"仅供唤醒词使用"。保留 direct audio input 与语音唤醒。功能文件直接删除，引用按既定剥离模式注释保留（`# 已剥离：TTS 组件` / `# 已剥离：STT 自动听写`）。

#### 已删除的功能文件（3 个）

| 文件 | 说明 |
|------|------|
| `src/handlers/tts/__init__.py`、`tts.py` | `TTSHandler` 基类及包导出 |
| `src/handlers/tts/custom_openai_tts.py` | `CustomOpenAITTSHandler` |

#### 已修改的文件

| 文件 | 变更内容 |
|------|----------|
| `src/constants.py` | 注释 TTS 导入、`AVAILABLE_TTS`、`DEFAULT_AVAILABLE_TTS`、`restore_handlers` 中的 TTS 行、`SETTINGS_GROUPS["TTS"]`；STT 组移除 `automatic-stt` |
| `src/controller.py` | 注释 `TTSHandler` 导入、`ReloadType.TTS`、`tts_enabled/tts_program/tts_voice`、`self.tts`、各处 `AVAILABLE_TTS` 分支；`automatic_stt` 相关读取与比较；`set_handlers`/`add_handlers` 调用去掉 tts 参数 |
| `src/extensions.py` | `set_handlers`/`add_handlers`/`remove_handlers` 去掉 tts 参数；注释 `get_tts_handlers`；`self.tts` 固定为 `None` 以兼容旧扩展 |
| `src/window.py` | 注释静音按钮、`mute_tts` 及 TTS 生命周期方法、`tts_enabled/tts` 赋值、`automatic_stt_status`；非 direct audio 的录音不再走 STT，改为提示开启 Direct audio input |
| `src/ui/voice_mode.py` | 注释全部 TTS 播报逻辑；最终回复只显示文字，经 `_complete_without_tts` 结束本轮；非 direct audio 时报错提示 |
| `src/ui/widgets/call.py` | 注释 TTS 播放、打断（`can_barge_in` 固定 False）、"播报时监听"按钮；非 direct audio 时提示 |
| `src/ui/widgets/chat_tab.py` | 注释 TTS 快捷开关、`tts`/`tts_enabled` 属性、回复后的播报与自动重启录音 |
| `src/ui/settings.py` | 注释 TTS 设置行与 `AVAILABLE_TTS` 分支；"Automatic Speech To Text" 开关去掉，保留静音检测参数 |
| `src/integrations/default_tools.py` | 注释 `speech_to_text`、`text_to_speech` 两个工具 |
| `src/main.py`、`src/ui/shortcuts.py`、`src/ui/widgets/chat_history.py`、`src/ui_controller.py` | 注释 `stop_tts` 动作、快捷键说明、TTS 提示卡片、`window.tts` 赋值 |
| `data/io.github.qwersyk.Newelle.gschema.xml` | XML 注释 `tts-on`/`tts`/`tts-voice`/`automatic-stt` |
| `po/POTFILES` | 注释 `src/handlers/tts/*` 条目 |

#### 保留的内容

- `clean_message_tts()`（`utility/strings.py`）仍被 voice mode、call 面板用于文本清理
- `AVAILABLE_STT` 仍为 `openai_sr`、`custom_command`，供唤醒词的主/副 STT 使用
- `audio-transcribe`、`audio-transcription-timing` 以及 `audio_input.py` 中的 STT 回退保留：纯文本模型收到录音时仍会用 STT 转写

#### 已知行为变化

- `direct-audio-input` 关闭时，聊天输入框麦克风、voice mode、call 面板均不可用（会提示开启），不再有普通听写
- 之前选了 `custom_openai_tts` 的用户，`tts-*` 设置值留在 dconf 中不再被读取
- 外部扩展若实现了 `get_tts_handlers` 将被忽略

#### 验证结果

- ✅ `python3 -m compileall src` 通过
- ✅ `glib-compile-schemas --strict --dry-run data` 通过
- ✅ 通过临时 `newelle` 包路径导入 constants、extensions、controller、window、voice_mode、call、chat_tab 成功，`ReloadType` 无 `TTS`
- ❌ 未启动 GUI 实测，唤醒词到 direct audio 的完整链路未运行验证

### 变更主题：STT 引擎 WitAIHandler 剥离

剥离 `witai` STT 引擎，引用按既定剥离模式注释保留。

| 文件 | 变更内容 |
|------|----------|
| `src/handlers/stt/witai_handler.py` | 已删除（`WitAIHandler`） |
| `src/handlers/stt/__init__.py` | 注释掉导入及 `__all__` 条目 |
| `src/constants.py` | 导入行改为不含 `WitAIHandler`；`AVAILABLE_STT` 注释掉 `witai` 条目 |
| `po/POTFILES` | 注释掉 `src/handlers/stt/witai_handler.py` |

- 当前 `AVAILABLE_STT` 仅保留：`openai_sr`、`custom_command`
- gschema 的 `stt-engine` 默认值 `whisper` 本就不在 `AVAILABLE_STT` 中（既有状态），`secondary-stt-engine` 默认 `custom_command` 仍有效；已选 `witai` 的用户由 `controller.py` 中 `not in AVAILABLE_STT` 的回退逻辑切换
- `pyproject.toml` 中无 `speechrecognition` 依赖，无需改动

### 变更主题：meson 构建系统剥离

改用 setuptools 构建 sdist/wheel，并删除全部 meson 构建文件。与其他剥离不同，meson 文件直接删除，未注释保留；恢复需从 git 历史（`HEAD`）取回。

#### 已删除的文件（7 个）

| 文件 | 说明 |
|------|------|
| `meson.build`、`meson_options.txt` | 顶层构建定义与 `profile` 选项 |
| `src/meson.build` | 源码安装清单、gresource 编译、启动脚本配置（工作区中的未提交剥离注释一并删除） |
| `data/meson.build`、`data/icons/meson.build` | desktop/appdata 翻译合并、schema 与图标安装 |
| `po/meson.build` | `i18n.gettext` 翻译编译与 `newelle-pot`/`newelle-update-po` 目标 |
| `src/newelle.in` | meson 配置生成的启动脚本 |

同时删除了 `_build/` 构建目录。

#### 新增的文件（4 个）

| 文件 | 说明 |
|------|------|
| `pyproject.toml` | 项目元数据、必需依赖、可选依赖组、`newelle` 入口 |
| `setup.py` | `build_data` 步骤生成 gresource、编译 schema、`.mo` 翻译、desktop/appdata；`EXCLUDED_MODULES` 排除不打包的模块 |
| `MANIFEST.in` | sdist 内容（含 `data/`、`po/`，排除截图） |
| `src/__main__.py` | 启动入口，取代 `newelle.in` |

#### 已修改的文件

| 文件 | 变更内容 |
|------|----------|
| `scripts/PKGBUILD` | 改为 `python -m build --wheel --no-isolation` + `python -m installer`；`arch=any`；补全运行依赖 |
| `scripts/locale-install.bash` | 改为构建 wheel 并安装到 `~/.local/share/newelle-venv`，链接启动器、desktop 文件、图标到 `~/.local` |
| `README.md` | 安装说明中的 GNOME Builder/`install.sh` 改为源码构建步骤 |
| `.gitignore` | 新增 `build/`、`dist/`、`*.egg-info/` |

#### 已知行为变化

- 版本号只在 `pyproject.toml` 维护；不再有 `profile=development` 的 git 短哈希版本后缀
- 翻译模板更新（原 meson 的 `newelle-pot`/`newelle-update-po` 目标）没有替代，需要时手动运行 `xgettext`/`msgmerge`。`po/POTFILES` 仍保留，但其中有 11 个条目指向已删除的文件
- schema 不再装到系统目录，由启动器通过 `GSETTINGS_SCHEMA_DIR` 指向包内副本，因此 `~/.local/share/glib-2.0/schemas` 中旧 meson 安装留下的 schema 不会覆盖它
- 旧 meson 安装（`~/.local/bin/newelle`、`~/.local/share/newelle/newelle`、`~/.local/share/newelle/newelle.gresource`、`~/.local/share/glib-2.0/schemas/io.github.qwersyk.Newelle.gschema.xml`）不会被自动清理；`~/.local/share/newelle/storage` 是用户数据，不要删除

#### 验证结果

- ✅ `python -m build` 生成 sdist 与 wheel；wheel 中的 `.py` 文件与 `src/meson.build` 原清单一致（另加 `__main__.py`）
- ✅ wheel 内含 gresource、编译好的 schema（123 个键）、25 种语言的 `.mo`；desktop/appdata 已合并翻译
- ✅ 用临时 HOME 运行 `scripts/locale-install.bash` 成功，安装后的 `newelle` 启动 20 秒无报错（仅既有 GTK 警告）
- ✅ 在 `XDG_DATA_HOME` 放入缺键的旧 schema 时，启动器仍使用包内 schema
- ✅ 模拟 PKGBUILD 的 `--no-isolation` 构建与 `installer --destdir` 安装成功

## 变更记录（2026-11-03）

### 变更主题：LlamaIndex 长期记忆剥离

剥离长期记忆组件 `LlamaIndexMemoryHandler`（设置中显示为 "Semantic Memory"）。所有引用均按既定剥离模式注释保留（`# 已剥离：LlamaIndex 长期记忆`），保证可逆性。

#### 已删除的功能文件（1 个）

| 文件 | 说明 |
|------|------|
| `src/handlers/memory/llamaindex_memory_handler.py` | LlamaIndex 长期记忆 `LlamaIndexMemoryHandler`（同日运行模块安装器剥离中曾修改过此文件，现已删除） |

#### 已修改的文件（3 个）

| 文件 | 变更内容 |
|------|----------|
| `src/handlers/memory/__init__.py` | 注释掉 `LlamaIndexMemoryHandler` 导入及 `__all__` 条目 |
| `src/constants.py` | 注释掉 import 中的 `LlamaIndexMemoryHandler`；`AVAILABLE_MEMORIES` 注释掉 `llamaindex` 条目 |
| `src/meson.build` | 注释掉 `memory_sources` 中的 `handlers/memory/llamaindex_memory_handler.py` |

#### 当前记忆模块状态

`AVAILABLE_MEMORIES` 保留：`long_term_memory`、`user-summary`、`agentic_memory_handler`。

- gschema 中 `memory-model` 默认值本就是 `long_term_memory`，无需修改
- 已选择 `llamaindex` 记忆的用户，会由 `controller.py` 中 `memory_model not in AVAILABLE_MEMORIES` 的回退逻辑切换到第一个可用记忆（`long_term_memory`）
- RAG 组件 `LlamaIndexHanlder`（`src/handlers/rag/llamaindex_handler.py`）与本次剥离无关，保留；gschema 中 `rag-model` 的 `"llamaindex"` 指向的是该 RAG 组件

#### 验证结果

- ✅ `python3 -m py_compile src/constants.py src/handlers/memory/__init__.py` 通过
- ✅ `src.handlers.memory.__all__` 为 `['MemoryHandler', 'UserSummaryHandler', 'AgenticMemoryHandler', 'LongTermMemoryHandler']`
- ✅ `AVAILABLE_MEMORIES` 键为 `['long_term_memory', 'user-summary', 'agentic_memory_handler']`
- ✅ `src/` 下无残留的非注释引用；`po/POTFILES` 本就不含该文件
- ✅ 已清理 `__pycache__` 中的过期 `.pyc`

### 变更主题：运行模块安装器剥离

对运行时 pip 依赖安装器进行了剥离，应用不再在运行时安装 Python 依赖。所有引用均按既定剥离模式注释保留（`# 已剥离：运行模块安装器`），保证可逆性。

#### 已删除的功能文件（1 个）

| 文件 | 说明 |
|------|------|
| `src/utility/pip.py` | 运行时 pip 安装器（`install_module`/`find_module`/`PipProgressParser` 等） |

#### 已修改的文件（10 个）

| 文件 | 变更内容 |
|------|----------|
| `src/handlers/handler.py` | 注释 `pip` 导入与 `Handler.install()` 中的安装循环；新增仅检测的 `find_module`（基于 `importlib.util.find_spec`），供 `is_installed()` 及子类使用 |
| `src/controller.py` | 注释 `install_module` 导入、pip 目录不存在时的后台初始化线程及 `init_pip_path` 方法（pip 目录存在时仍加入 `python_path`） |
| `src/ui/settings.py` | 注释 `install_module` 导入、开发者设置中的 "Delete pip path"/"Install pip module" 两行及 `delete_pip_path` 方法 |
| `src/handlers/stt/stt.py`、`stt/whisper_handler.py` | `find_module` 改从 `handlers.handler` 导入 |
| `src/handlers/tts/custom_openai_tts.py` | 注释 `install_module("openai")`，`find_module` 改从 `handlers.handler` 导入 |
| `src/handlers/rag/llamaindex_handler.py` | 注释 `install()` 中的安装逻辑，`find_module` 改从 `handlers.handler` 导入 |
| `src/handlers/memory/llamaindex_memory_handler.py` | 同上 |
| `src/handlers/memory/agentic_memory_handler.py` | 注释未使用的 pip 导入 |
| `src/meson.build` | 注释掉 `utility_sources` 中的 `utility/pip.py` |

#### 保留的通用逻辑

- `controller.pip_path` 与 `python_path` 追加逻辑保留：已存在的 pip 目录仍可提供已装依赖
- `Handler.install()`/`install_with_progress()`/`is_installed()` 接口保留（`install()` 现在只重置安装缓存）
- `download_manager.py` 与 pip 无耦合，不受影响

#### 已知行为变化

- 依赖缺失时 `is_installed()` 仍返回 False，但不会再自动安装；`install_missing_handlers()` 会在 `install_with_progress` 中抛出 "did not finish installing"（已被调用处捕获并打印），需用户自行安装依赖

#### 验证结果

- ✅ `python3 -m py_compile` 对全部 9 个修改的 Python 文件通过
- ✅ whisper、custom_openai_tts、llamaindex RAG/记忆、agentic 记忆 handler 均可正常导入
- ✅ `src/` 下无残留的非注释 pip 工具引用（仅剩两处文档字符串提及）
- ✅ `po/POTFILES` 本就不含 `pip.py`，无需改动

## 当前变更记录（2026-10-23）

### 变更主题：线程编辑功能剥离

对线程编辑功能进行了完全剥离，移除了线程编辑窗口及相关功能。所有引用均按既定剥离模式注释保留，保证可逆性。

#### 已删除的功能文件（1 个）

| 文件 | 说明 |
|------|------|
| `src/ui/thread_editing.py` | 线程编辑窗口 `ThreadEditing` |

#### 已修改的文件（5 个）

| 文件 | 变更内容 |
|------|----------|
| `src/main.py` | 注释掉 `ThreadEditing` 导入、`thread_editing` action 注册、`thread_editing_action` 方法 |
| `src/window.py` | 注释掉菜单项 `menu.append(_("Thread editing"), "app.thread_editing")` |
| `src/ui/widgets/chat_history.py` | 注释掉占位提示项 `{"title": _("Thread Editing"), ...}` |
| `src/meson.build` | 注释掉 `ui_sources` 中的 `ui/thread_editing.py` |
| `po/POTFILES` | 注释掉 `src/ui/thread_editing.py` 条目 |

#### 当前线程编辑状态

剥离后，`src/ui/thread_editing.py` 已删除，项目中不再包含线程编辑功能。

#### 验证结果

- ✅ `python -m py_compile` 对全部 3 个修改的 Python 文件语法检查通过
- ✅ `src/` 下 grep 确认无残留的非注释线程编辑引用

## 当前变更记录（2026-10-21）

### 变更主题：内置文件管理器剥离

对内置文件管理器（ExplorerPanel）进行了完全剥离，移除了画布中的 Explorer 标签页功能。所有引用均按既定剥离模式注释保留（`# 已剥离：内置文件管理器`），保证可逆性。

#### 已删除的功能文件（1 个）

| 文件 | 说明 |
|------|------|
| `src/ui/explorer.py` | 文件管理器面板 `ExplorerPanel`（约 730 行） |

#### 已修改的文件（7 个）

| 文件 | 变更内容 |
|------|----------|
| `src/window.py` | 注释掉 `ExplorerPanel` 导入、`canvas_overview.connect`（新建标签页信号）、`add_explorer_tab` 初始化调用、`menu_entries` 中的 "Explorer Tab" 条目、`run_command` 中 `cd` 命令的 explorer 路径解析、命令执行后的 explorer 路径同步、`update_explorer_panels`/`get_current_explorer_panel`/`add_explorer_tab`/`update_path` 方法 |
| `src/ui_controller.py` | 注释掉 `workspace_action("path")` 中的 explorer 面板路径同步、`new_explorer_tab` 方法、stub 类中的 `newiexplorer_tab` |
| `src/ui/voice_mode.py` | 注释掉 `VoiceOverlay` 中的 `new_explorer_tab` 转发方法 |
| `src/ui/workspaces.py` | 注释掉工作区切换时的 explorer 面板路径同步块 |
| `src/ui/widgets/chat_history.py` | 注释掉目录点击时 `new_explorer_tab` 调用，改为统一走 `gio open` |
| `src/meson.build` | 注释掉 `ui_sources` 中的 `ui/explorer.py` |
| `po/POTFILES` | 注释掉 `src/ui/explorer.py` 条目 |

#### 保留的通用逻辑

- `window.py` 中 `on_tab_switched` 的 `hasattr(child, "main_path")` 检查为通用逻辑（终端标签页也使用 `main_path`），予以保留
- `self.main_path` 在 `window.py:141` 从 `newelle_settings.main_path` 初始化，与 explorer 无关，不受影响

#### 当前文件管理器状态

剥离后，画布标签页仅保留：Chat、Terminal、Browser、Image Generator、Code Editor。目录点击行为统一为系统文件管理器打开（`gio open`）。

#### 验证结果

- ✅ `python -m py_compile` 对全部 5 个修改的 Python 文件语法检查通过
- ✅ `src/` 下 grep 确认无残留的非注释 explorer 引用
- ✅ `main.py:719` 的 `self.win.update_folder()` 为既有问题（改动前 `window.py` 即无此方法定义），与本次剥离无关，未处理

### 变更主题：内置浏览器剥离

对内置浏览器（BrowserWidget）进行了完全剥离，移除了画布中的 Browser 标签页功能。所有引用均按既定剥离模式注释保留（`# 已剥离：内置浏览器`），保证可逆性。链接打开行为统一改为外部浏览器（`open_website` / `Gio.AppInfo.launch_default_for_uri`）。

#### 已删除的功能文件（1 个）

| 文件 | 说明 |
|------|------|
| `src/ui/widgets/browser.py` | 浏览器面板 `BrowserWidget` |

#### 已修改的文件（10 个）

| 文件 | 变更内容 |
|------|----------|
| `src/window.py` | 注释掉 `BrowserWidget` 导入、`menu_entries` 中的 "Browser Tab" 条目、`get_current_browser_panel`/`add_browser_tab`/`_on_attach_clicked` 方法 |
| `src/ui_controller.py` | 注释掉 `new_browser_tab`/`open_link` 方法、stub 类中的对应方法、`open_website` 导入 |
| `src/ui/voice_mode.py` | 注释掉 `VoiceOverlay` 中的 `new_browser_tab`/`open_link` 转发方法 |
| `src/ui/settings.py` | 注释掉 `build_browser_settings()` 调用及 `build_browser_settings`/`delete_browser_session` 方法 |
| `src/constants.py` | 从 `settings` 列表移除 `initial-browser-page`/`external-browser`/`browser-search-string`/`browser-session-persist` |
| `src/controller.py` | 注释掉 `external_browser`/`initial_browser_page`/`browser_search_string`/`browser_session_persist` 设置读取 |
| `src/ui/widgets/__init__.py` | 注释掉 `BrowserWidget` 导入及 `__all__` 条目 |
| `src/ui/widgets/message.py` | 引用点击与本地服务打开改为外部浏览器（`Gio.AppInfo.launch_default_for_uri`） |
| `src/integrations/websearch.py` | `website-clicked` 改为 `open_website(link)` 外部打开 |
| `src/integrations/website_reader.py` | `open_website` 方法改为调用 `open_website(button.url)` 外部打开 |
| `src/meson.build` | 注释掉 `ui_sources` 中的 `ui/widgets/browser.py` |
| `po/POTFILES` | 注释掉 `src/ui/widgets/browser.py` 条目 |
| `data/io.github.qwersyk.Newelle.gschema.xml` | 注释掉 `external-browser`/`initial-browser-page`/`browser-search-string`/`browser-session-persist` 键 |

#### 保留的通用逻辑

- WebKit 依赖仍被其他组件使用（`extensions_catalog.py`、`mermaid.py`、`divergence.py`），故 `meson.build` 中的 WebKit 依赖保留
- `modes.py:142`、`window.py:2757/2762` 的 `help-browser-symbolic`/`web-browser-symbolic` 为图标名称列表，与浏览器组件无关，予以保留
- `mcp_oauth.py` 的 `webbrowser.open` 为 OAuth 外部浏览器认证，与内置浏览器无关，予以保留

#### 当前浏览器状态

剥离后，画布标签页仅保留：Chat、Terminal、Image Generator、Code Editor。链接打开行为统一为系统默认浏览器打开。

#### 验证结果

- ✅ `python -m py_compile` 对全部 10 个修改的 Python 文件语法检查通过
- ✅ `data/io.github.qwersyk.Newelle.gschema.xml` XML 解析通过
- ✅ `src/` 下 grep 确认无残留的非注释浏览器引用

## 变更记录（2026-10-12）

### 变更主题：LLM 提供商剥离

对 LLM 模块进行了大规模精简，将 LLM 提供商从 14 个减少至 1 个（仅保留 OpenAI）。

#### 已删除的功能文件（13 个）

以下 LLM 提供商处理器文件已从项目中删除：

| 提供商 | 文件 |
|--------|------|
| claude | `src/handlers/llm/claude_handler.py` |
| custom | `src/handlers/llm/custom_handler.py` |
| deepseek | `src/handlers/llm/deepseek_handler.py` |
| gpt4free | `src/handlers/llm/g4f_handler.py` |
| gemini | `src/handlers/llm/gemini_handler.py` |
| gpt3any | `src/handlers/llm/gpt3any_handler.py` |
| groq | `src/handlers/llm/groq_handler.py` |
| llama_cpp | `src/handlers/llm/llama_cpp_handler.py` |
| mistral | `src/handlers/llm/mistral_handler.py` |
| newelle | `src/handlers/llm/newelle_handler.py` |
| ollama_cloud | `src/handlers/llm/ollama_cloud_handler.py` |
| ollama | `src/handlers/llm/ollama_handler.py` |
| openrouter | `src/handlers/llm/openrouter_handler.py` |

#### 已修改的文件（5 个）

| 文件 | 变更内容 |
|------|----------|
| `src/constants.py` | 注释掉 `AVAILABLE_LLMS` 中所有被剥离提供商的条目及 import 行 |
| `src/handlers/llm/__init__.py` | 注释掉被剥离提供商的 import 及 `__all__` 列表条目 |
| `src/meson.build` | 注释掉 `llm_sources` 中被剥离提供商的源文件引用 |
| `po/POTFILES` | 移除已删除的 LLM 处理器文件条目 |
| `build_locale.sh` | 将 locale 构建脚本改为 meson 构建（与本次剥离无关的独立变更） |

#### 当前 LLM 模块状态

剥离后，`src/handlers/llm/` 目录仅保留以下文件：

- `__init__.py`
- `llm.py`（基类 `LLMHandler`、`LLMResponse`）
- `openai_handler.py`（`OpenAIHandler`）

`AVAILABLE_LLMS` 中仅保留 `openai` 一个提供商。

#### 验证结果

- ✅ `src.handlers.llm` 可正常导入，无 ImportError
- ✅ `__all__` 为 `['LLMHandler', 'LLMResponse', 'OpenAIHandler']`
- ✅ 全项目搜索确认无残留的未注释引用

### 变更主题：Embedding 模型剥离

对 Embedding 模块进行了精简，将 Embedding 模型从 6 个减少至 1 个（仅保留 OpenAI）。

#### 已删除的功能文件（5 个）

以下 Embedding 处理器文件已从项目中删除：

| 模型 | 文件 |
|------|------|
| gemini | `src/handlers/embeddings/gemini_handler.py` |
| ollama | `src/handlers/embeddings/ollama_handler.py` |
| wordllama | `src/handlers/embeddings/wordllama_handler.py` |
| llama_cpp | `src/handlers/embeddings/llama_cpp_handler.py` |
| model2vec | `src/handlers/embeddings/model2vec.py` |

#### 已修改的文件（3 个）

| 文件 | 变更内容 |
|------|----------|
| `src/handlers/embeddings/__init__.py` | 注释掉被剥离模型的 import 及 `__all__` 列表条目 |
| `src/constants.py` | 注释掉 `AVAILABLE_EMBEDDINGS` 中被剥离模型的条目及 import 行 |
| `src/ui/model_library.py` | 注释掉 `llamacppembedding` 相关的后端检测引用 |
| `src/meson.build` | 注释掉 `embedding_sources` 中被剥离模型的文件路径 |

#### 当前 Embedding 模块状态

剥离后，`src/handlers/embeddings/` 目录仅保留以下文件：

- `__init__.py`
- `embedding.py`（基类 `EmbeddingHandler`、`EmbeddingPurpose`）
- `openai_handler.py`（`OpenAIEmbeddingHandler`）

`AVAILABLE_EMBEDDINGS` 中仅保留 `openaiembedding` 一个模型。

#### 验证结果

- ✅ `src.handlers.embeddings` 可正常导入，无 ImportError
- ✅ `__all__` 为 `['EmbeddingHandler', 'EmbeddingPurpose', 'OpenAIEmbeddingHandler']`
- ✅ 全项目搜索确认无残留的未注释引用
- ✅ `python -m py_compile` 语法检查通过

## 当前变更记录（2026-10-13）

### 变更主题：Interfaces 模块剥离

对 Interfaces 模块进行了完全剥离，移除了所有接口处理器（API、Telegram、GUI API 等）及相关设置页面。

#### 已删除的功能文件（7 个）

以下接口处理器及设置页面文件已从项目中删除：

| 文件 | 说明 |
|------|------|
| `src/handlers/interfaces/__init__.py` | 接口处理器包初始化 |
| `src/handlers/interfaces/interface.py` | 接口基类 `Interface` |
| `src/handlers/interfaces/chat_interface.py` | 聊天接口处理器 |
| `src/handlers/interfaces/api_handler.py` | API 接口处理器 `APIInterface` |
| `src/handlers/interfaces/gui_api_handler.py` | GUI API 接口处理器 `GUIAPIInterface` |
| `src/handlers/interfaces/telegram_handler.py` | Telegram 接口处理器 `TelegramInterface` |
| `src/ui/interfaces.py` | Interfaces 设置页面 |

#### 已修改的文件（7 个）

| 文件 | 变更内容 |
|------|----------|
| `src/constants.py` | 注释掉 `Interface`/`APIInterface`/`GUIAPIInterface`/`TelegramInterface` 的 import 行、`AVAILABLE_INTERFACES` 及 `DEFAULT_AVAILABLE_INTERFACES` 定义；从 "interface" 设置组的 settings 列表移除 `interfaces-settings` |
| `src/controller.py` | 注释掉 `Interface` 导入、`self.interfaces` 字典、`refresh_interfaces()` 方法、`interface.stop()` 调用、`skip_auto_start_interfaces` 相关引用及 `_get_message_interfaces` |
| `src/extensions.py` | 注释掉 `get_interface_handlers` 方法、`"interface": "get_interface_handlers"` 映射、`handler_contributions["interface"]` 检查、`AVAILABLE_INTERFACES` 文档字符串及 `extension.get_interface_handlers()` 调用 |
| `src/main.py` | 注释掉 `interfaces` 动作注册、`interfaces_action` 方法、`run_headless` 函数及 `HeadlessController` 导入 |
| `src/meson.build` | 从 `ui_sources` 移除 `ui/interfaces.py`；删除 `interface_sources` 列表及 `install_data(interface_sources, ...)` 指令 |
| `src/newelle.in` | 注释掉 `--interface`/`--list-interfaces` CLI 参数及 headless 接口启动代码块 |
| `src/ui/settings.py` | 注释掉 `InterfacesPage` 导入、导航页面条目及 `"Interfaces": ["interface"]` 页面映射 |

#### 当前 Interfaces 模块状态

剥离后，`src/handlers/interfaces/` 目录已完全移除，`src/ui/interfaces.py` 已删除。

`AVAILABLE_INTERFACES` 及相关引用均已注释保留（`#` 前缀），便于后续恢复。

#### 验证结果

- ✅ `python3 -m py_compile src/main.py src/ui/settings.py` 语法检查通过
- ✅ 全项目搜索确认无残留的未注释引用（`interfaces_action`、`settings_action_paged("Interfaces")`、`AVAILABLE_INTERFACES`、`run_headless` 等均已注释）
- ✅ `src/handlers/interfaces/` 目录已不存在

### 变更主题：TTS 引擎剥离

对 TTS（语音合成）模块进行了精简，将 TTS 引擎从 10 个减少至 1 个（仅保留 Custom OpenAI TTS）。

#### 已删除的功能文件（9 个）

以下 TTS 引擎处理器文件已从项目中删除：

| 引擎 | 文件 |
|------|------|
| gtts | `src/handlers/tts/gtts_handler.py` |
| kokoro | `src/handlers/tts/kokoro_handler.py` |
| groq | `src/handlers/tts/groq_tts_handler.py` |
| espeak | `src/handlers/tts/espeak_handler.py` |
| elevenlabs | `src/handlers/tts/elevenlabs_handler.py` |
| edge | `src/handlers/tts/edge_handler.py` |
| mistral | `src/handlers/tts/mistral_tts_handler.py` |
| custom_command | `src/handlers/tts/custom_handler.py` |
| openai_tts | `src/handlers/tts/openai_tts_handler.py` |

#### 已修改的文件（5 个）

| 文件 | 变更内容 |
|------|----------|
| `src/handlers/tts/__init__.py` | 注释掉被剥离引擎的 import 及 `__all__` 列表条目，仅保留 `TTSHandler` 和 `CustomOpenAITTSHandler` |
| `src/constants.py` | 注释掉被剥离引擎的 import 行；`AVAILABLE_TTS` 字典仅保留 `custom_openai_tts` 条目 |
| `src/meson.build` | 注释掉 `tts_sources` 中被剥离引擎的源文件引用 |
| `data/io.github.qwersyk.Newelle.gschema.xml` | 将 `tts` 键默认值从 `"gtts"` 改为 `"custom_openai_tts"` |
| `io.github.qwersyk.Newelle.json` | 注释掉 `modules/python3-gtts.json` 依赖（gTTS 引擎已移除） |

#### 当前 TTS 模块状态

剥离后，`src/handlers/tts/` 目录仅保留以下文件：

- `__init__.py`
- `tts.py`（基类 `TTSHandler`）
- `custom_openai_tts.py`（`CustomOpenAITTSHandler`）

`AVAILABLE_TTS` 中仅保留 `custom_openai_tts` 一个引擎。

#### 验证结果

- ✅ `src.handlers.tts` 可正常导入，无 ImportError
- ✅ `__all__` 为 `['TTSHandler', 'CustomOpenAITTSHandler']`
- ✅ `AVAILABLE_TTS` 键为 `['custom_openai_tts']`
- ✅ 全项目搜索确认无残留的未注释引用（`controller.py`/`window.py` 无硬编码特定引擎引用）
- ✅ 搜索到的 `custom_command` 引用属于 STT 模块，与 TTS 无关，保留正确
- ✅ `python3-openai.json` 依赖已保留（`custom_openai_tts` 引擎及 OpenAI LLM 均需使用）

### 变更主题：STT 引擎剥离

对 STT（语音识别）模块进行了精简，剥离了 `whisper_cpp`（WhisperCPPHandler）和 `openwakeword`（OpenWakeWordHandler）两个引擎。

#### 已删除的功能文件（2 个）

以下 STT 引擎处理器文件已从项目中删除：

| 引擎 | 文件 |
|------|------|
| whisper_cpp | `src/handlers/stt/whispercpp_handler.py` |
| openwakeword | `src/handlers/stt/openwakeword_handler.py` |

#### 已修改的文件（7 个）

| 文件 | 变更内容 |
|------|----------|
| `src/handlers/stt/__init__.py` | 注释掉 `WhisperCPPHandler`/`OpenWakeWordHandler` 的 import 及 `__all__` 列表条目 |
| `src/constants.py` | 注释掉被剥离引擎的 import 行；`AVAILABLE_STT` 中注释掉 `whispercpp`/`openwakeword` 条目 |
| `src/meson.build` | 注释掉 `stt_sources` 中被剥离引擎的源文件引用 |
| `po/POTFILES` | 注释掉 `src/handlers/stt/whispercpp_handler.py` 引用 |
| `data/io.github.qwersyk.Newelle.gschema.xml` | 将 `secondary-stt-engine` 键默认值从 `"whispercpp"` 改为 `"custom_command"` |
| `src/ui/model_library.py` | 注释掉 `whispercpp` 相关引用（`_backend_from_cmake_cache` 的 `source_dir` 映射、两处 `if key not in (...)` 条件、一处 `if key in (...)` 条件） |
| `io.github.qwersyk.Newelle.json` | 注释掉 `modules/python3-openwakeword.json` 依赖（openwakeword 引擎已移除） |

#### 当前 STT 模块状态

剥离后，`src/handlers/stt/` 目录保留以下文件：

- `__init__.py`
- `stt.py`（基类 `STTHandler`）
- `custom_handler.py`（`CustomSRHandler`）
- `openaisr_handler.py`（`OpenAISRHandler`）
- `whisper_handler.py`（`WhisperHandler`）
- `witai_handler.py`（`WitAIHandler`）

`AVAILABLE_STT` 中保留的引擎为：`witai`、`openai_sr`、`custom_command`。

#### 验证结果

- ✅ `python3 -m py_compile src/handlers/stt/__init__.py src/constants.py src/ui/model_library.py src/ui/settings.py` 语法检查通过
- ✅ 全项目搜索确认无残留的未注释引用（`WhisperCPPHandler`、`OpenWakeWordHandler`、`whispercpp_handler`、`openwakeword_handler` 均已注释或删除）
- ✅ `src/handlers/stt/whispercpp_handler.py`、`src/handlers/stt/openwakeword_handler.py` 已不存在
- ✅ `_build/` 下 meson 构建产物仍含陈旧引用，重新构建时会自动刷新

### 变更主题：图片生成引擎剥离

对图片生成模块进行了精简，将图片生成引擎从 4 个减少至 1 个（仅保留 OpenAI Compatible）。

#### 已删除的功能文件（3 个）

以下图片生成引擎处理器文件已从项目中删除：

| 引擎 | 文件 |
|------|------|
| pollinations | `src/handlers/image_generator/pollinations_handler.py` |
| stablediffusion_cpp | `src/handlers/image_generator/stablediffusion_cpp_handler.py` |
| openrouter_image | `src/handlers/image_generator/openrouter_image_handler.py` |

#### 已修改的文件（5 个）

| 文件 | 变更内容 |
|------|----------|
| `src/handlers/image_generator/__init__.py` | 注释掉被剥离引擎的 import 及 `__all__` 列表条目，仅保留 `ImageGeneratorHandler` 和 `OpenAIImageHandler` |
| `src/constants.py` | 注释掉被剥离引擎的 import 行；`AVAILABLE_IMAGE_GENERATORS` 字典仅保留 `openai-image` 条目 |
| `src/meson.build` | 注释掉 `image_generator_sources` 中被剥离引擎的源文件引用 |
| `data/io.github.qwersyk.Newelle.gschema.xml` | 将 `image-generator` 键默认值从 `"pollinations"` 改为 `"openai-image"` |
| `src/ui/model_library.py` | 注释掉 `stablediffusioncpp` 相关引用（`_backend_from_cmake_cache` 的 `source_dir` 映射、`get_local_backend` 的 key 检查与分支、`_installed_backend` 的 key 检查与 `use_system_sd` 分支） |

#### 当前图片生成模块状态

剥离后，`src/handlers/image_generator/` 目录仅保留以下文件：

- `__init__.py`
- `image_generator.py`（基类 `ImageGeneratorHandler`）
- `openai_image_handler.py`（`OpenAIImageHandler`）

`AVAILABLE_IMAGE_GENERATORS` 中仅保留 `openai-image` 一个引擎。

#### 验证结果

- ✅ `python3 -m py_compile src/handlers/image_generator/__init__.py src/constants.py src/ui/model_library.py` 语法检查通过
- ✅ 全项目搜索确认无残留的未注释引用（`PollinationsHandler`、`StableDiffusionCPPHandler`、`OpenRouterImageHandler` 均已注释或删除）
- ✅ `src/handlers/image_generator/pollinations_handler.py`、`stablediffusion_cpp_handler.py`、`openrouter_image_handler.py` 已不存在
- ✅ 已清理 `__pycache__` 中 3 个引擎的过期 `.pyc` 文件
- ✅ `_build/` 下 meson 构建产物仍含陈旧引用，重新构建时会自动刷新

## 当前变更记录（2026-10-14）

### 变更主题：Flatpak 支持剥离

对 Flatpak 支持进行了完全剥离，移除了所有 Flatpak 相关函数、沙箱检查及警告 UI。

#### 已删除的功能函数（`src/utility/system.py`）

以下 Flatpak 相关函数已从 `src/utility/system.py` 中删除：

| 函数 | 说明 |
|------|------|
| `is_flatpak()` | 检查是否运行在 Flatpak 沙箱中 |
| `get_flatpak_x11_override_command()` | 获取 Flatpak X11 覆盖命令 |
| `_flatpak_sockets()` | 获取 Flatpak sockets |
| `has_flatpak_x11_permission()` | 检查 Flatpak X11 权限 |
| `needs_voice_mode_x11_override()` | 检查是否需要 voice mode X11 覆盖 |
| `can_escape_sandbox()` | 检查是否能逃逸沙箱 |
| `get_spawn_command()` | 获取 spawn 命令（含 flatpak-spawn 前缀） |

同时更新了 `has_backend()`/`detect_cuda_version()` 中对 `get_spawn_command` 的调用。

#### 已修改的文件（15 个）

| 文件 | 变更内容 |
|------|----------|
| `src/utility/system.py` | 删除 7 个 Flatpak 函数；更新 `has_backend`/`detect_cuda_version` 调用 |
| `src/integrations/mcp.py` | 注释 `is_flatpak`/`get_spawn_command` 引用，更新文档字符串 |
| `src/integrations/default_tools.py` | 注释 `is_flatpak`/`get_spawn_command` 引用 |
| `src/utility/build_dependencies.py` | 注释 `is_flatpak`/`get_spawn_command` 引用 |
| `src/utility/replacehelper.py` | 注释 `is_flatpak`/`get_spawn_command` 引用 |
| `src/ui/widgets/message.py` | 注释 `is_flatpak`/`get_spawn_command` 引用 |
| `src/ui/widgets/chat_tab.py` | 注释 `is_flatpak`/`get_spawn_command` 引用 |
| `src/utility/file_search.py` | 注释 flatpak-spawn 用法 |
| `src/ui/mcp_catalog.py` | 注释 `_FLATPAK_GIMP_PLUGIN_INSTALLER` 常量和 flatpak-spawn 检查 |
| `src/ui/extension.py` | 注释 `add_flatpak_warning_button`/`show_flatpak_sandbox_notice` 方法；`self.sandbox` 改为 `False` |
| `src/ui/presentation.py` | 注释 flatpak 命令 CopyBox |
| `src/ui/settings.py` | 注释 `add_flatpak_waning_button`/`show_flatpak_sandbox_notice` 方法；`self.sandbox` 改为 `False`；`_handler_selection_blocked` 移除沙箱检查 |
| `src/handlers/handler.py` | 注释 `requires_sandbox_escape()` 方法 |
| `src/handlers/stt/custom_handler.py` | 注释 `requires_sandbox_escape()` 方法 |
| `src/utility/background_process.py` | 更新文档字符串 |

#### 当前 Flatpak 支持状态

剥离后，项目中不再包含任何 Flatpak 相关功能：

- `src/utility/system.py` 中无 Flatpak 函数
- 所有 Flatpak 引用均以注释形式保留（`#` 前缀），便于后续恢复
- `self.sandbox` 属性改为 `False`（应用不再运行在沙箱中）
- `requires_sandbox_escape()` 方法已注释（不再需要沙箱逃逸检查）

#### 验证结果

- ✅ `python3 -m py_compile` 语法检查通过（所有修改文件）
- ✅ 全项目搜索确认无残留的未注释 Flatpak 引用（`is_flatpak`、`get_spawn_command`、`flatpak-spawn`、`requires_sandbox_escape` 等均已注释或删除）
- ✅ meson 构建脚本（`meson.build`、`src/meson.build`、`data/meson.build`、`meson_options.txt`）无 Flatpak 相关引用
- ✅ 项目根目录无 Flatpak manifest 文件（`io.github.qwersyk.Newelle.json` 等）

### 变更主题：MCP 接口合并与剥离（2026-10-14）

合并上游 `FrancescoCaracciolo/Newelle` 新增的 MCP 接口（`MCPInterface`），随后将其完全剥离。

#### 合并内容

上游新增 2 个提交：
- `0cbdb0e` **Add MCP interface** — 新增 MCP 服务器接口
- `feef987` **Make settings window resizable** — 设置窗口可调整大小

合并时恢复了以下文件以支持 MCP 接口：
- `src/handlers/interfaces/interface.py`（接口基类 `Interface`）
- `src/handlers/interfaces/mcp_interface.py`（`MCPInterface`）
- `src/handlers/interfaces/__init__.py`（包导出）

#### 已删除的功能文件（3 个）

| 文件 | 说明 |
|------|------|
| `src/handlers/interfaces/__init__.py` | 接口处理器包初始化 |
| `src/handlers/interfaces/interface.py` | 接口基类 `Interface` |
| `src/handlers/interfaces/mcp_interface.py` | MCP 接口处理器 `MCPInterface` |

#### 已修改的文件（2 个）

| 文件 | 变更内容 |
|------|----------|
| `src/constants.py` | 注释掉 `MCPInterface` 的 import 行及 `AVAILABLE_INTERFACES` 定义 |
| `src/meson.build` | 注释掉 `interface_sources` 列表 |

#### 当前 Interfaces 模块状态

剥离后，`src/handlers/interfaces/` 目录已完全移除。

`AVAILABLE_INTERFACES` 及相关引用均已注释保留（`#` 前缀），便于后续恢复。

#### 验证结果

- ✅ `python3 -m py_compile src/constants.py` 语法检查通过
- ✅ `constants.py` 导入成功，`AVAILABLE_INTERFACES` 已不存在
- ✅ 全项目搜索确认无残留的未注释引用（`MCPInterface`、`AVAILABLE_INTERFACES`、`interface_sources` 等均已注释）
- ✅ `src/handlers/interfaces/` 目录已不存在

### 其他变更（与 Interfaces 剥离无关）

- `data/io.github.qwersyk.Newelle.desktop.in`：将 `Exec=newelle` 改为 `Exec=env DRI_PRIME=1 newelle`（含 mini-window/voice-mode 动作），用于强制使用独立显卡渲染

## 构建说明

使用 setuptools 构建（`pyproject.toml` + `setup.py`）。构建时需要系统提供 `glib-compile-resources`、`glib-compile-schemas`、`msgfmt`。

```bash
# 本地安装：构建 wheel，装入 ~/.local/share/newelle-venv，并链接到 ~/.local/bin
bash scripts/locale-install.bash

# 只构建 sdist 与 wheel（输出到 dist/）
python -m build
```

- GTK4/libadwaita 等 GI 库来自系统，自行安装 wheel 时 venv 需带 `--system-site-packages`
- 入口为 `src/__main__.py`（`newelle.__main__:main`）：用 `GSETTINGS_SCHEMA_DIR` 指向包内 schema，把包内 `newelle/_data/share` 加到 `XDG_DATA_DIRS` 前面（图标），并从包内加载 gresource 与翻译
- `setup.py` 的 `build_data` 步骤在 `build/newelle-data/` 生成 gresource、编译好的 schema、`.mo` 翻译、已翻译的 desktop/appdata 文件
- `setup.py` 的 `EXCLUDED_MODULES` 排除不打包的模块（`divergence.py`、`vision.py`、`llamaindex_memory_handler.py`）。新增或剥离模块时，若不想打包需同步更新该集合；剥离模块不再需要改 `meson.build`
- 依赖：必需依赖写在 `pyproject.toml` 的 `dependencies`，按需加载的写在 `optional-dependencies`（`web`、`mcp`、`rag`、`stt`、`models`）
- 新增 gresource 资源需改 `src/newelle.gresource.xml`；新增语言需改 `po/LINGUAS`

## 注意事项

- 被剥离的 LLM 提供商引用均以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的 Embedding 模型引用同样以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的 Interfaces 引用同样以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的 TTS 引擎引用同样以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的 STT 引擎引用同样以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的图片生成引擎引用同样以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的 Flatpak 引用同样以注释形式保留（`#` 前缀），便于后续恢复
- `po/` 目录下的 `.po` 翻译文件仍可能包含已删除文件的路径引用，这些是自动生成文件，重新构建时会更新
- 若需恢复某个提供商/模型/引擎，需同时恢复其功能文件、`constants.py` 条目及 `__init__.py` 导入（meson 已剥离，无需再改 `meson.build`；若该文件在 `setup.py` 的 `EXCLUDED_MODULES` 中需移除）

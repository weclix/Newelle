# Newelle 项目说明

## 项目概述

Newelle 是一个 Linux 桌面 AI 助手应用，使用 Python + GTK4 开发，采用 meson 构建系统。

- **构建系统**：meson（`meson_version >= 0.62.0`）
- **源码目录**：`src/`
- **核心模块**：`controller.py`、`main.py`、`window.py`、`modes.py`、`skills.py`、`tools.py`、`extensions.py`、`ui_controller.py`

## 当前变更记录（2026-10-12）

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

### 其他变更（与 Interfaces 剥离无关）

- `data/io.github.qwersyk.Newelle.desktop.in`：将 `Exec=newelle` 改为 `Exec=env DRI_PRIME=1 newelle`（含 mini-window/voice-mode 动作），用于强制使用独立显卡渲染

## 构建说明

```bash
# 配置构建
meson setup _build --prefix=~/.local --buildtype=release

# 编译
meson compile -C _build

# 安装
meson install -C _build
```

## 注意事项

- 被剥离的 LLM 提供商引用均以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的 Embedding 模型引用同样以注释形式保留（`#` 前缀），便于后续恢复
- 被剥离的 Interfaces 引用同样以注释形式保留（`#` 前缀），便于后续恢复
- `po/` 目录下的 `.po` 翻译文件仍可能包含已删除文件的路径引用，这些是自动生成文件，重新构建时会更新
- 若需恢复某个提供商/模型，需同时恢复其功能文件、`constants.py` 条目、`__init__.py` 导入及 `meson.build` 引用

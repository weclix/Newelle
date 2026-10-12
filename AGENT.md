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
- `po/` 目录下的 `.po` 翻译文件仍可能包含已删除文件的路径引用，这些是自动生成文件，重新构建时会更新
- 若需恢复某个提供商/模型，需同时恢复其功能文件、`constants.py` 条目、`__init__.py` 导入及 `meson.build` 引用

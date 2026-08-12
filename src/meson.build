pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'newelle')
gnome = import('gnome')

gnome.compile_resources('newelle',
  'newelle.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')
conf = configuration_data() 
conf.set('PYTHON', python.find_installation('python3').path())
profile = get_option('profile')
version_full = meson.project_version()
if profile == 'development'
  version_full += '-' + run_command('git', 'rev-parse', '--short', 'HEAD').stdout().strip()
endif
conf.set('VERSION', version_full)
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'newelle.in',
  output: 'newelle',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

newelle_sources = [
  '__init__.py',
  'main.py',
  'constants.py',
  'window.py',
  'extensions.py',
  'controller.py',
  'ui_controller.py',
  'tools.py',
  'skills.py',
  'modes.py'
]

integrations_sources = [
  'integrations/__init__.py',
  'integrations/website_reader.py',
  'integrations/websearch.py',
  'integrations/mermaid.py',
  'integrations/mcp.py',
  'integrations/mcp_oauth.py',
  'integrations/default_tools.py',
  'integrations/skills.py',
  'integrations/skill_editor.py',
  'integrations/agent_tools.py',
  'integrations/file_editing.py',
  'integrations/todo_list.py',
]

ui_sources = [
  'ui/__init__.py',
  'ui/profile.py',
  'ui/extension.py',
  'ui/settings.py',
  'ui/presentation.py',
  'ui/thread_editing.py',
  'ui/scheduled_tasks.py',
  'ui/shortcuts.py',
  'ui/mini_window.py',
  'ui/stdout_monitor.py',
  'ui/model_library.py',
  'ui/mcp_catalog.py',
  'ui/skills_catalog.py',
  'ui/skill_creator.py',
  'ui/extensions_catalog.py',
  'ui/extra_settings.py',
]

widgets_sources = [
  'ui/widgets/__init__.py',
  'ui/widgets/multiline.py',
  'ui/widgets/profilerow.py',
  'ui/widgets/barchart.py',
  'ui/widgets/comborow.py',
  'ui/widgets/copybox.py',
  'ui/widgets/command_session_action.py',
  'ui/widgets/file.py',
  'ui/widgets/file_read.py',
  'ui/widgets/file_edit.py',
  'ui/widgets/file_permission_confirm.py',
  'ui/widgets/glob.py',
  'ui/widgets/grep.py',
  'ui/widgets/list_directory.py',
  'ui/widgets/context_indicator.py',
  'ui/widgets/folderrow.py',
  'ui/widgets/latex.py',
  'ui/widgets/mermaid.py',
  'ui/widgets/terminal_dialog.py',
  'ui/widgets/markuptextview.py',
  'ui/widgets/website.py',
  'ui/widgets/sources.py',
  'ui/widgets/websearch.py',
  'ui/widgets/thinking.py',
  'ui/widgets/documents_reader.py',
  'ui/widgets/tipscarousel.py',
  'ui/widgets/code_editor.py',
  'ui/widgets/tool.py',
  'ui/widgets/skill.py',
  'ui/widgets/skill_editor_mini_app.py',
  'ui/widgets/subagent.py',
  'ui/widgets/scheduled_task.py',
  'ui/widgets/message.py',
  'ui/widgets/chatrow.py',
  'ui/widgets/chat_history.py',
  'ui/widgets/chat_tab.py',
  'ui/widgets/mode_switcher.py',
  'ui/widgets/mode_editor.py',
  'ui/widgets/status.py',
  'ui/widgets/question.py',
]

handler_sources = [
  'handlers/__init__.py',
  'handlers/handler.py',
  'handlers/extra_settings.py',
  'handlers/descriptors.py',
]

llm_sources = [
  'handlers/llm/__init__.py',
  'handlers/llm/llm.py',
  'handlers/llm/newelle_handler.py',
  'handlers/llm/openai_handler.py',
]

embedding_sources = [  
  'handlers/embeddings/__init__.py',
  'handlers/embeddings/embedding.py',
  'handlers/embeddings/openai_handler.py',
]

memory_sources = [  
  'handlers/memory/__init__.py',
  'handlers/memory/memory_handler.py',
  'handlers/memory/memoripy_handler.py',
  'handlers/memory/summary_memoripy_handler.py',
  'handlers/memory/user_summary_handler.py',
  'handlers/memory/llamaindex_memory_handler.py',
  'handlers/memory/agentic_memory_handler.py'
]

rag_sources = [  
  'handlers/rag/__init__.py',
  'handlers/rag/rag_handler.py',
  'handlers/rag/llamaindex_handler.py',
]

websearch_sources = [
  'handlers/websearch/__init__.py',
  'handlers/websearch/websearch.py',
  'handlers/websearch/searxng.py',
]

utility_sources = [
  'utility/__init__.py',
  'utility/media.py',
  'utility/pip.py',
  'utility/replacehelper.py',
  'utility/strings.py',
  'utility/system.py',
  'utility/util.py',
  'utility/profile_settings.py',
  'utility/message_chunk.py',
  'utility/website_scraper.py',
  'utility/stdout_capture.py',
  'utility/force_sync.py',
  'utility/file_search.py',
  'utility/context_manager.py',
  'utility/source_attribution.py',
  'utility/command_permissions.py',
  'utility/command_runner.py',
  'utility/command_sessions.py',
  'utility/background_process.py',
  'utility/tool_call_group.py',
]

install_data(newelle_sources, install_dir: moduledir)
install_data(ui_sources, install_dir: moduledir / 'ui')
install_data(widgets_sources, install_dir: moduledir / 'ui' / 'widgets')
install_data(handler_sources, install_dir: moduledir / 'handlers')
install_data(llm_sources, install_dir: moduledir / 'handlers' / 'llm')
install_data(memory_sources, install_dir: moduledir / 'handlers' / 'memory')
install_data(rag_sources, install_dir: moduledir / 'handlers' / 'rag')
install_data(embedding_sources, install_dir: moduledir / 'handlers' / 'embeddings')
install_data(memory_sources, install_dir: moduledir / 'handlers' / 'memory')
install_data(rag_sources, install_dir: moduledir / 'handlers' / 'rag')
install_data(websearch_sources, install_dir: moduledir / 'handlers' / 'websearch')
install_data(utility_sources, install_dir: moduledir / 'utility')
install_data(integrations_sources, install_dir: moduledir / 'integrations')

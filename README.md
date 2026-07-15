# Hermes AI Assistant Suite

A collection of AI-powered assistants built for the Hermes Agent framework, featuring conversational AI, code assistance, system diagnostics, file operations, and data analysis capabilities.

## 📋 Overview

This repository contains multiple Python scripts that implement various AI assistants with different specializations:

- **JAVIS** (`javis.py`) - Just A Very Intelligent System (your requested assistant)
- **Hermes Universal AI** (`hermes_universal_ai.py`) - Combines features of modern AI coding agents
- **Hermes Assistant** (`hermes_assistant.py`) - Advanced, user-friendly AI chatbot
- **Hermes BigData AI** (`hermes_bigdata_ai.py`) - Specialized for large file processing
- **Hermes ChatBot** (`hermes_chatbot.py`) - Interactive terminal chatbot
- **Hermes AI Advanced** (`hermes_ai_advanced.py`) - Feature-rich AI assistant
- **Hermes Lite** (`hermes_lite.py`) - Simple prototype
- **Hermes Demo** (`hermes_demo.py`) - Demonstration version
- **DataSage AI** (`datasage_ai.py`) - Data science focused assistant
- **Poem Display** (`display_poem.py`) - Shows the AI-generated poem "Silicon Satori"

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Git Bash / MSYS / Windows Terminal (for best experience)
- Optional: NVIDIA GPU for hardware acceleration detection

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/salmonA001/hermes-ai-assistant-suite.git
   cd hermes-ai-assistant-suite
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Run any assistant:
   ```bash
   python javis.py          # Your requested JAVIS assistant
   python hermes_chatbot.py # Interactive chatbot
   python hermes_bigdata_ai.py # Big data processing demo
   ```

## 🛠️ Using the Assistants

### JAVIS (Just A Very Intelligent System)
Your requested assistant combining features of Claude Code, Codex, Cursor, Gemini, ChatGPT, NVIDIA tools, and Antigravity-IDE.

```bash
python javis.py
```

**Features:**
- Natural language conversation
- Code assistance (`code <file> <instruction>`)
- Safe code execution (`run <code_snippet>`)
- Code explanation (`explain <code>`)
- System & GPU information (`gpu`)
- Mathematical calculations (`calc <expression>`)
- File operations (`read`, `write`, `files`)
- Data analysis (`stats <dataset>`)
- Conversation history

**Example Commands:**
```
> Hello!
> What is machine learning?
> gpu
> calc 25% of 2000
> code example.py "add a function to calculate factorial"
> run "print('Hello from JAVIS!')"
> Thanks!
> Bye
```

### Hermes ChatBot
Interactive terminal-based chatbot with helpful commands.

```bash
python hermes_chatbot.py
```

**Available Commands:**
- `help` - Show all commands
- `time` / `date` - Current time/date
- `system` / `gpu` - System information
- `files` / `read <file>` / `write <file> <content>` - File operations
- `calc <expression>` - Mathematical calculations
- `code <file> <instruction>` - Code suggestions
- `run <code>` - Safe code execution
- `stats <dataset>` - Analyze sample datasets
- `history` - Conversation history
- `exit` / `quit` - Leave chat

### Hermes BigData AI
Specialized for processing large files efficiently using streaming and chunking techniques.

```bash
python hermes_bigdata_ai.py
```

**Features:**
- Efficient line/word counting for huge files
- CSV analysis without loading entire file
- Map-reduce word count implementation
- Memory-friendly processing

### Other Assistants
Each script follows similar patterns - simply run with `python <script_name>.py` and follow the on-screen prompts or use command-line arguments where applicable.

## 🧠 Skills Usage

While this implementation focuses on standalone scripts, the Hermes Agent framework supports **skills** for extending functionality. To create custom skills:

1. Create a directory under `~/.hermes/skills/` (or project-specific skills folder)
2. Add a `SKILL.md` file with:
   - Frontmatter (name, description, etc.)
   - Detailed usage instructions
   - Optional reference files, templates, and scripts
3. Skills can be loaded automatically or invoked via the Hermes framework

For more information on skill creation, see the [Hermes Agent Skill Authoring](https://hermes-agent.nousresearch.com/docs/skills) documentation.

## 🗺️ Roadmap

### Planned Enhancements
- [ ] **Web Interface**: Add optional Gradio/Streamlit UI for easier interaction
- [ ] **Skill Marketplace**: Community-shared skills repository
- [ ] **Memory Persistence**: Long-term conversation memory across sessions
- [ ] **Multi-model Support**: Switch between different LLM backends
- [ ] **Voice Integration**: Speech-to-text and text-to-speech capabilities
- [ ] **Agent Collaboration**: Enable multiple assistants to work together
- [ ] **Document Processing**: PDF, Word, Excel analysis capabilities
- [ ] **Code Execution Sandbox**: Enhanced security for code execution
- [ ] **Integration Hooks**: Connect to IDEs, editors, and development tools

### Current Development Focus
- Improving code suggestion accuracy with better rule-based systems
- Adding more sample datasets for demonstration
- Enhancing GPU detection and utilization features
- Refining conversational flow and context retention
- Expanding knowledge base with more technical domains

## 📝 License

This project is provided as-is for educational and personal use. Feel free to modify and extend for your own needs.

## 🙏 Acknowledgments

- Built with the Hermes Agent framework by Nous Research
- Inspired by: Claude Code, Codex, Cursor, Gemini, ChatGPT, NVIDIA tools
- Special thanks to the open-source AI community

---

**Happy coding with your AI assistants!** 🤖
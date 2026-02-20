# CodeMind — Local AI Coding Assistant

> A fully local, privacy-first AI coding assistant built with Streamlit and Ollama.  
> No API keys. No cloud. No data leaves your machine.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-local%20inference-black?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Screenshot

<!-- Replace this with a real screenshot after your first run -->
> Dark-themed UI with sidebar controls, streaming responses, selectable template cards, and persistent conversation history.

---

## Features

- **100% local inference** via [Ollama](https://ollama.com) — no internet required after setup
- **Smooth token streaming** — responses appear word-by-word with a live blinking cursor
- **Selectable prebuilt templates** — click to select, then hit one button to generate
- **Auto-save on every reply** — chats are saved to JSON automatically, no manual steps
- **Named conversations** — manually name or auto-name from your first message
- **Conversation history sidebar** — browse, reload, and delete past sessions
- **Configurable inference** — adjust temperature, top-p, and context window in real time
- **Dark professional UI** — JetBrains Mono + Geist fonts, fully custom CSS

---

## Models Included

| Model | Approx. Size | Best For |
|---|---|---|
| `Qwen2.5-Coder-3B-Instruct` Q5_K_M | ~2.5 GB | General coding, explanations, debugging |
| `CodeGemma-2B` Q5_K_M | ~1.6 GB | Lightweight, fast completions |

> You can add any Ollama-compatible model by editing the `MODEL_DISPLAY` dict in `app.py`.

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- 4 GB RAM minimum — 8 GB recommended

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/codemind.git
cd codemind
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit ollama
```

### 4. Install and start Ollama

Download from [ollama.com](https://ollama.com), then start the server:

```bash
ollama serve
```

### 5. Pull the models

```bash
# Primary model — Qwen2.5 Coder 3B
ollama pull hf.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF:Q5_K_M

# Optional — CodeGemma 2B
ollama pull hf.co/MaziyarPanahi/codegemma-2b-GGUF:Q5_K_M
```

### 6. Run the app

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## Project Structure

```
codemind/
├── app.py                        # Main Streamlit application
├── README.md                     # This file
└── codemind_conversations/       # Auto-created on first run
    ├── my_fastapi_app_20250220_143012.json
    └── aes_cipher_fix_20250220_151234.json
```

> `codemind_conversations/` is created automatically. Add it to `.gitignore` if you don't want to commit your chat history.

---

## Usage Guide

### Chatting
Type any coding question into the input bar at the bottom. For best results:
- Mention the language and version upfront
- Paste error messages verbatim
- Ask for step-by-step explanations when needed

### Prebuilt Templates
1. On the home screen, click a template card to **select** it — it highlights in purple
2. Press **▶ Use Template** to fire the full detailed prompt instantly
3. Click the same card again to deselect it

Available templates out of the box:
- 🐍 **REST API Client** — Python HTTP client with retries, Bearer auth, and custom exceptions
- ⚡ **CLI File Organiser** — Argparse CLI with dry-run mode and colourised output
- 🌐 **FastAPI CRUD App** — Full CRUD API with SQLite, SQLAlchemy ORM, and Pydantic schemas

### Conversation Persistence
- **Auto-save** — every assistant reply is saved automatically to a JSON file
- **New chats** are auto-named from the first 50 characters of your opening message
- **Manual naming** — type a custom name in the Save field and click 💾 Save
- **Reload** any past conversation from the History list in the sidebar
- **Delete** conversations with the 🗑 button next to each history item

---

## Configuration

All inference options are adjustable live in the sidebar:

| Setting | Default | Description |
|---|---|---|
| Temperature | `0.2` | Lower = more deterministic, higher = more creative |
| Top-P | `0.9` | Nucleus sampling threshold |
| Context Window | `2048` | Max token context (higher = more RAM usage) |

To tune threading or batch size, edit the `options` block in `app.py`:

```python
options={
    "num_thread":  6,     # Set to your CPU core count
    "num_ctx":     2048,  # Context window
    "num_batch":   128,   # Batch size — lower if RAM is limited
    "temperature": 0.2,
    "top_p":       0.9,
    "use_mlock":   True,  # Pin model in RAM to avoid swapping
}
```

---

## Adding Your Own Models

Edit the `MODEL_DISPLAY` dictionary near the top of `app.py`:

```python
MODEL_DISPLAY = {
    "hf.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF:Q5_K_M": "Qwen2.5-Coder 3B · Q5_K_M",
    "hf.co/MaziyarPanahi/codegemma-2b-GGUF:Q5_K_M":      "CodeGemma 2B · Q5_K_M",
    "your-ollama-model-id":                               "Your Display Name",  # ← add here
}
```

Any model you can run with `ollama pull` will work.

---

## Recommended `.gitignore`

```gitignore
.venv/
__pycache__/
*.pyc
*.pyo
codemind_conversations/
.streamlit/secrets.toml
```

---

## Troubleshooting

**`Connection refused` — Ollama not responding**
```bash
ollama serve
```

**`Model not found` error**
```bash
ollama pull hf.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF:Q5_K_M
```

**Responses are very slow**
- Lower the Context Window slider to `1024`
- Reduce `num_batch` to `64` in `app.py`
- Switch to the smaller CodeGemma 2B model

**`StreamlitAPIException: Failed to load avatar`**
Upgrade Streamlit: `pip install --upgrade streamlit`

**Home screen and chat appear together on first message**
Make sure you're using the latest `app.py` from this repo — this was a known bug that has been patched.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | [Streamlit](https://streamlit.io) |
| LLM Inference | [Ollama](https://ollama.com) |
| Models | Qwen2.5-Coder 3B, CodeGemma 2B (GGUF) |
| Storage | JSON files on local filesystem |
| Fonts | JetBrains Mono, Geist (Google Fonts) |
| Language | Python 3.10+ |

---

## License

MIT License — free to use, modify, and distribute.

---

## Acknowledgements

- [Ollama](https://ollama.com) for making local LLM inference accessible
- [Qwen Team @ Alibaba](https://huggingface.co/Qwen) for Qwen2.5-Coder
- [Google DeepMind](https://huggingface.co/google/codegemma-2b) for CodeGemma
- [Streamlit](https://streamlit.io) for the rapid prototyping framework

---

<p align="center">Built for developers who value clean code and local privacy.</p>

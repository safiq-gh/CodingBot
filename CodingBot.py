import streamlit as st
import ollama
import json
import os
import re
from datetime import datetime
from pathlib import Path

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodeMind",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Styles ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Geist:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg-0:        #0a0a0b;
    --bg-1:        #111113;
    --bg-2:        #18181b;
    --bg-3:        #1e1e21;
    --bg-4:        #27272a;
    --border:      #2e2e33;
    --border-hi:   #3f3f46;
    --text-0:      #fafafa;
    --text-1:      #d4d4d8;
    --text-2:      #a1a1aa;
    --text-3:      #71717a;
    --accent:      #22d3ee;
    --accent-dim:  rgba(34,211,238,.12);
    --accent-glow: rgba(34,211,238,.25);
    --green:       #4ade80;
    --red:         #f87171;
    --purple:      #818cf8;
    --purple-dim:  rgba(129,140,248,.15);
    --purple-glow: rgba(129,140,248,.30);
    --code-bg:     #0d0d0f;
    --mono:        'JetBrains Mono', monospace;
    --sans:        'Geist', 'Segoe UI', sans-serif;
}

html, body, .main,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background-color: var(--bg-0) !important;
    font-family: var(--sans);
    color: var(--text-1);
}
.main .block-container { padding-top: 0 !important; padding-bottom: 120px; max-width: 900px; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-1); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 2px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background-color: var(--bg-1) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] > div:first-child { padding: 20px 16px 24px; }
.sidebar-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }
.sidebar-logo-icon { width: 30px; height: 30px; background: linear-gradient(135deg, var(--accent), var(--purple)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.sidebar-logo-text { font-family: var(--mono); font-size: 1rem; font-weight: 600; color: var(--text-0); letter-spacing: -0.5px; }
.sidebar-logo-version { font-family: var(--mono); font-size: 0.6rem; color: var(--accent); background: var(--accent-dim); padding: 1px 5px; border-radius: 4px; }
.sidebar-section { font-family: var(--mono); font-size: 0.6rem; font-weight: 500; color: var(--text-3); letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px; margin-top: 2px; }
[data-testid="stSidebar"] label { font-family: var(--sans) !important; font-size: 0.78rem !important; font-weight: 500 !important; color: var(--text-2) !important; margin-bottom: 5px !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background-color: var(--bg-3) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; color: var(--text-1) !important; font-family: var(--mono) !important; font-size: 0.76rem !important; }
[data-testid="stSidebar"] .stSelectbox > div > div:hover { border-color: var(--border-hi) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 2px var(--accent-dim) !important; }
[data-testid="stSidebar"] input[type="number"] { background-color: var(--bg-3) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; color: var(--text-0) !important; font-family: var(--mono) !important; font-size: 0.8rem !important; padding: 7px 9px !important; }
[data-testid="stSidebar"] input[type="number"]:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px var(--accent-dim) !important; outline: none !important; }
[data-testid="stSidebar"] input[type="text"] { background-color: var(--bg-3) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; color: var(--text-0) !important; font-family: var(--mono) !important; font-size: 0.8rem !important; padding: 7px 9px !important; }
[data-testid="stSidebar"] input[type="text"]:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px var(--accent-dim) !important; outline: none !important; }
[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] { background-color: var(--accent) !important; box-shadow: 0 0 8px var(--accent-glow) !important; }
[data-testid="stSidebar"] [data-baseweb="slider"] [data-testid="stThumbValue"] { background: var(--bg-3) !important; color: var(--accent) !important; font-family: var(--mono) !important; font-size: 0.7rem !important; border: 1px solid var(--border-hi) !important; }
hr, [data-testid="stDivider"] { border-color: var(--border) !important; margin: 12px 0 !important; }
.model-badge { display: inline-flex; align-items: center; gap: 5px; background: var(--accent-dim); border: 1px solid rgba(34,211,238,0.2); border-radius: 4px; padding: 2px 8px; font-family: var(--mono); font-size: 0.62rem; color: var(--accent); margin-bottom: 10px; }

/* ── Conversation History Cards ── */
.conv-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.conv-header-label { font-family: var(--mono); font-size: 0.6rem; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-3); }
.conv-count { font-family: var(--mono); font-size: 0.6rem; color: var(--text-3); background: var(--bg-3); border: 1px solid var(--border); border-radius: 10px; padding: 1px 7px; }
.conv-list { display: flex; flex-direction: column; gap: 4px; max-height: 280px; overflow-y: auto; padding-right: 2px; margin-bottom: 10px; }
.conv-item { background: var(--bg-2); border: 1px solid var(--border); border-radius: 7px; padding: 9px 11px; cursor: pointer; transition: all 0.15s; }
.conv-item:hover { border-color: var(--border-hi); background: var(--bg-3); }
.conv-item.active { border-color: var(--accent); background: var(--accent-dim); }
.conv-item-name { font-family: var(--sans); font-size: 0.78rem; font-weight: 500; color: var(--text-0); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 3px; }
.conv-item-meta { font-family: var(--mono); font-size: 0.62rem; color: var(--text-3); display: flex; align-items: center; gap: 6px; }
.conv-item-dot { width: 4px; height: 4px; border-radius: 50%; background: var(--border-hi); display: inline-block; }
.conv-empty { font-family: var(--mono); font-size: 0.72rem; color: var(--text-3); text-align: center; padding: 16px 8px; background: var(--bg-2); border: 1px dashed var(--border); border-radius: 7px; }

/* ── Tips ── */
.tips-box { background: var(--bg-2); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; margin-top: 4px; }
.tips-box-title { font-family: var(--mono); font-size: 0.68rem; font-weight: 600; color: var(--text-3); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 9px; }
.tip-row { display: flex; align-items: flex-start; gap: 7px; margin-bottom: 6px; font-size: 0.75rem; color: var(--text-2); line-height: 1.4; }
.tip-icon { color: var(--accent); font-size: 0.68rem; flex-shrink: 0; margin-top: 2px; font-family: var(--mono); }

/* ── All Buttons ── */
.stButton > button { background-color: var(--bg-4) !important; color: var(--text-1) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; font-family: var(--sans) !important; font-size: 0.78rem !important; font-weight: 500 !important; padding: 7px 10px !important; width: 100% !important; transition: all 0.15s !important; }
.stButton > button:hover { background-color: var(--bg-3) !important; border-color: var(--border-hi) !important; color: var(--text-0) !important; }
.stButton > button:active { transform: translateY(1px) !important; }

/* ── Template selector buttons ── */
.tpl-btn .stButton > button { background: var(--bg-2) !important; border: 1.5px solid var(--border) !important; border-radius: 12px !important; padding: 16px 14px !important; text-align: left !important; height: auto !important; min-height: 110px !important; white-space: normal !important; line-height: 1.5 !important; color: var(--text-1) !important; }
.tpl-btn .stButton > button:hover { border-color: var(--border-hi) !important; background: var(--bg-3) !important; transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(0,0,0,0.35) !important; }
.tpl-btn-selected .stButton > button { background: var(--purple-dim) !important; border: 1.5px solid var(--purple) !important; border-radius: 12px !important; padding: 16px 14px !important; text-align: left !important; height: auto !important; min-height: 110px !important; white-space: normal !important; line-height: 1.5 !important; color: var(--text-0) !important; box-shadow: 0 0 20px var(--purple-glow) !important; transform: translateY(-2px) !important; }

/* ── Use Template CTA ── */
.use-tpl-btn .stButton > button { background: linear-gradient(135deg, var(--accent), var(--purple)) !important; color: #000 !important; border: none !important; border-radius: 10px !important; font-size: 0.88rem !important; font-weight: 700 !important; padding: 13px 20px !important; box-shadow: 0 4px 20px var(--accent-glow) !important; }
.use-tpl-btn .stButton > button:hover { opacity: 0.9 !important; box-shadow: 0 6px 28px var(--purple-glow) !important; transform: translateY(-1px) !important; }
.use-tpl-btn .stButton > button:disabled { background: var(--bg-4) !important; color: var(--text-3) !important; box-shadow: none !important; transform: none !important; border: 1px solid var(--border) !important; }

/* ── Page Header ── */
.page-header { display: flex; align-items: center; gap: 14px; padding: 24px 0 18px; border-bottom: 1px solid var(--border); margin-bottom: 8px; }
.page-header-icon { width: 38px; height: 38px; background: linear-gradient(135deg, var(--accent), var(--purple)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; box-shadow: 0 0 18px var(--accent-glow); }
.page-header-title { font-family: var(--mono); font-size: 1.2rem; font-weight: 600; color: var(--text-0); letter-spacing: -0.5px; }
.page-header-sub { font-size: 0.76rem; color: var(--text-3); margin-top: 2px; font-family: var(--mono); }
.conv-name-badge { display: inline-flex; align-items: center; gap: 5px; background: var(--purple-dim); border: 1px solid rgba(129,140,248,0.25); border-radius: 4px; padding: 1px 8px; font-family: var(--mono); font-size: 0.65rem; color: var(--purple); margin-left: 6px; vertical-align: middle; }
.status-dot { width: 6px; height: 6px; background: var(--green); border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 5px var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

/* ── Chat ── */
[data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 0 !important; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { color: var(--text-1); font-size: 0.88rem; line-height: 1.65; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background: var(--bg-2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: 12px 16px !important; margin: 6px 0 !important; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { background: transparent !important; border-left: 2px solid var(--accent) !important; border-radius: 0 !important; padding: 10px 16px !important; margin: 6px 0 !important; }
.stMarkdown pre { background-color: var(--code-bg) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; padding: 16px !important; font-family: var(--mono) !important; font-size: 0.8rem !important; line-height: 1.6 !important; overflow-x: auto !important; }
.stMarkdown pre::before { content: '● ● ●'; display: block; color: var(--border-hi); font-size: 0.58rem; letter-spacing: 4px; margin-bottom: 12px; }
.stMarkdown code { font-family: var(--mono) !important; font-size: 0.8em !important; color: var(--accent) !important; background: var(--accent-dim) !important; padding: 2px 5px !important; border-radius: 4px !important; }
.stMarkdown pre code { color: var(--text-1) !important; background: transparent !important; padding: 0 !important; }

/* ── Chat Input ── */
[data-testid="stChatInput"] { background-color: var(--bg-2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; color: var(--text-0) !important; font-family: var(--sans) !important; font-size: 0.88rem !important; }
[data-testid="stChatInput"]:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-dim) !important; }
[data-testid="stChatInput"] textarea { background: transparent !important; color: var(--text-0) !important; }
[data-testid="stChatInput"] button { background: var(--accent) !important; border-radius: 6px !important; color: #000 !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 8px !important; font-size: 0.82rem !important; font-family: var(--mono) !important; }
[data-testid="stToast"] { background: var(--bg-3) !important; border: 1px solid var(--border-hi) !important; color: var(--text-0) !important; border-radius: 8px !important; }

/* ── Empty State ── */
.empty-state { text-align: center; padding: 36px 20px 20px; }
.empty-state-icon { font-size: 2rem; margin-bottom: 12px; opacity: 0.45; }
.empty-state-title { font-family: var(--mono); font-size: 0.95rem; font-weight: 500; color: var(--text-2); margin-bottom: 7px; }
.empty-state-sub { font-size: 0.8rem; color: var(--text-3); line-height: 1.6; max-width: 340px; margin: 0 auto 22px; }

/* ── Starter chips ── */
.starter-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; max-width: 520px; margin: 0 auto 28px; }
.starter-card { background: var(--bg-2); border: 1px solid var(--border); border-radius: 8px; padding: 11px 13px; transition: all 0.15s; }
.starter-card:hover { border-color: var(--accent); background: var(--bg-3); box-shadow: 0 0 10px var(--accent-glow); }
.starter-icon { font-size: 0.95rem; margin-bottom: 5px; display: block; }
.starter-text { font-size: 0.74rem; color: var(--text-2); line-height: 1.4; }

/* ── Template section ── */
.section-label { font-family: var(--mono); font-size: 0.62rem; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-3); display: flex; align-items: center; gap: 10px; margin: 4px 0 14px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.select-hint { font-family: var(--mono); font-size: 0.7rem; color: var(--text-3); text-align: center; margin: 8px 0 14px; letter-spacing: 0.3px; }
.select-hint span { color: var(--purple); }

/* ── Dropdown ── */
[data-baseweb="popover"] { background: var(--bg-3) !important; border: 1px solid var(--border-hi) !important; border-radius: 8px !important; }
[data-baseweb="menu"] { background: var(--bg-3) !important; }
[data-baseweb="menu"] [role="option"] { color: var(--text-1) !important; font-family: var(--mono) !important; font-size: 0.76rem !important; }
[data-baseweb="menu"] [role="option"]:hover { background: var(--bg-4) !important; }

/* ── Chat Markdown ── */
[data-testid="stChatMessage"] h1,[data-testid="stChatMessage"] h2,[data-testid="stChatMessage"] h3 { color: var(--text-0) !important; font-weight: 600; margin-top: 12px; margin-bottom: 5px; }
[data-testid="stChatMessage"] p { color: var(--text-1) !important; margin-bottom: 7px; }
[data-testid="stChatMessage"] ul,[data-testid="stChatMessage"] ol { color: var(--text-1) !important; padding-left: 18px; margin-bottom: 7px; }
[data-testid="stChatMessage"] li { margin-bottom: 3px; }

/* ── Footer ── */
.footer-bar { text-align: center; padding: 14px 0 6px; font-family: var(--mono); font-size: 0.65rem; color: var(--text-3); border-top: 1px solid var(--border); margin-top: 14px; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are CodeMind, an expert software engineering assistant.

CORE PRINCIPLES:
- Write correct, minimal, executable code
- Never invent APIs or frameworks that do not exist
- Break complex problems into clear steps before coding
- Handle edge cases and error conditions
- Prefer simple, readable, deterministic solutions over clever ones

RESPONSE FORMAT:
- Begin with a concise explanation of your approach
- Provide well-commented, production-ready code
- List any dependencies or prerequisites
- Note important assumptions or limitations
- Use markdown formatting with proper language tags in code fences"""

MODEL_DISPLAY = {
    "hf.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF:Q5_K_M": "Qwen2.5-Coder 3B · Q5_K_M",
    "hf.co/MaziyarPanahi/codegemma-2b-GGUF:Q5_K_M":      "CodeGemma 2B · Q5_K_M",
}

TEMPLATES = [
    {
        "icon": "🐍", "tag": "Python", "title": "REST API Client",
        "desc": "HTTP client class with retries, Bearer auth, custom exceptions & type hints",
        "prompt": (
            "Write a production-ready Python REST API client class with:\n"
            "- Base URL + Bearer token auth header support\n"
            "- GET, POST, PUT, DELETE methods\n"
            "- Automatic retries (3x) with exponential back-off using `tenacity`\n"
            "- Structured error handling with custom exceptions\n"
            "- Type hints and docstrings throughout\n"
            "- A usage example at the bottom"
        ),
    },
    {
        "icon": "⚡", "tag": "CLI Tool", "title": "CLI File Organiser",
        "desc": "Argparse CLI that sorts files by extension with dry-run mode & coloured output",
        "prompt": (
            "Write a Python CLI tool using `argparse` that organises files in a directory:\n"
            "- Accepts --source and --dest path arguments\n"
            "- Moves files into sub-folders named by extension (e.g. /images, /docs)\n"
            "- --dry-run flag to preview without moving anything\n"
            "- Colourised terminal output using `colorama`\n"
            "- Handles permission errors and missing paths gracefully\n"
            "- Include a __main__ entry point"
        ),
    },
    {
        "icon": "🌐", "tag": "FastAPI", "title": "FastAPI CRUD App",
        "desc": "Full CRUD API with SQLite, SQLAlchemy ORM, Pydantic schemas & uvicorn setup",
        "prompt": (
            "Build a complete FastAPI application with:\n"
            "- SQLite database via SQLAlchemy ORM\n"
            "- A Task model with id, title, description, status, created_at fields\n"
            "- Full CRUD endpoints: POST /tasks, GET /tasks, GET /tasks/{id}, PUT /tasks/{id}, DELETE /tasks/{id}\n"
            "- Pydantic request/response schemas with validation\n"
            "- HTTPException error responses with proper status codes\n"
            "- Dependency injection for DB session\n"
            "- Instructions to run with uvicorn"
        ),
    },
]

# ─── Storage helpers ──────────────────────────────────────────────────────────
# Conversations saved as JSON files in ./codemind_conversations/ next to app.py
CONV_DIR = Path(__file__).parent / "codemind_conversations"
CONV_DIR.mkdir(exist_ok=True)

def _safe_filename(name: str) -> str:
    """Slugify a conversation name to a safe filename."""
    slug = re.sub(r"[^\w\s-]", "", name).strip()
    slug = re.sub(r"[\s]+", "_", slug)
    return slug[:60] or "untitled"

def list_conversations() -> list[dict]:
    """Return all saved conversations sorted newest first."""
    convs = []
    for f in CONV_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            convs.append({
                "id":       f.stem,
                "name":     data.get("name", f.stem),
                "saved_at": data.get("saved_at", ""),
                "msg_count": len([m for m in data.get("messages", []) if m["role"] != "system"]),
                "path":     f,
            })
        except Exception:
            pass
    return sorted(convs, key=lambda x: x["saved_at"], reverse=True)

def save_conversation(name: str, messages: list[dict]) -> str:
    """Save messages to a JSON file. Returns the file stem (id)."""
    slug     = _safe_filename(name)
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id  = f"{slug}_{ts}"
    payload  = {
        "name":     name,
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "messages": messages,
    }
    path = CONV_DIR / f"{file_id}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return file_id

def load_conversation(file_id: str) -> tuple[str, list[dict]]:
    """Load a conversation by its file stem. Returns (name, messages)."""
    path = CONV_DIR / f"{file_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["name"], data["messages"]

def delete_conversation(file_id: str) -> None:
    path = CONV_DIR / f"{file_id}.json"
    if path.exists():
        path.unlink()

# ─── Session State ────────────────────────────────────────────────────────────
if "messages"          not in st.session_state:
    st.session_state.messages          = [{"role": "system", "content": SYSTEM_PROMPT}]
if "pending_prompt"    not in st.session_state:
    st.session_state.pending_prompt    = None
if "selected_template" not in st.session_state:
    st.session_state.selected_template = None
if "active_conv_id"    not in st.session_state:
    st.session_state.active_conv_id    = None   # file stem of loaded conversation
if "active_conv_name"  not in st.session_state:
    st.session_state.active_conv_name  = None
if "save_name_input"   not in st.session_state:
    st.session_state.save_name_input   = ""

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">💻</div>
        <div><div class="sidebar-logo-text">CodeMind</div></div>
        <div class="sidebar-logo-version">v1.0</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Model ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Model</div>', unsafe_allow_html=True)
    model_key = st.selectbox(
        "model", list(MODEL_DISPLAY.keys()),
        format_func=lambda k: MODEL_DISPLAY[k],
        label_visibility="collapsed"
    )
    st.markdown(f'<div class="model-badge">◆ {MODEL_DISPLAY[model_key]}</div>', unsafe_allow_html=True)

    # ── Inference ──────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Inference</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        temperature = st.number_input("Temp",  min_value=0.0, max_value=1.0, value=0.2, step=0.05, format="%.2f")
    with c2:
        top_p       = st.number_input("Top-P", min_value=0.0, max_value=1.0, value=0.9, step=0.05, format="%.2f")
    num_ctx = st.slider("Context Window", min_value=512, max_value=4096, value=2048, step=256)

    st.divider()

    # ── Actions ────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Actions</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✦ New Chat", use_container_width=True):
            st.session_state.messages          = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.session_state.pending_prompt    = None
            st.session_state.selected_template = None
            st.session_state.active_conv_id    = None
            st.session_state.active_conv_name  = None
            st.rerun()
    with c2:
        msg_count = max(0, len(st.session_state.messages) - 1)
        st.button(f"↓ {msg_count} msgs", use_container_width=True, disabled=True)

    st.divider()

    # ── Save Conversation ──────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Save Conversation</div>', unsafe_allow_html=True)

    has_msgs = len([m for m in st.session_state.messages if m["role"] == "user"]) > 0

    # Default name from first user message
    default_name = st.session_state.active_conv_name or ""
    if not default_name and has_msgs:
        first_user = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "")
        default_name = first_user[:40].replace("\n", " ")

    save_name = st.text_input(
        "Conversation name",
        value=default_name,
        placeholder="Name this conversation…",
        label_visibility="collapsed",
        disabled=not has_msgs,
    )

    if st.button(
        "💾  Save" if not st.session_state.active_conv_id else "💾  Overwrite",
        use_container_width=True,
        disabled=not has_msgs or not save_name.strip(),
    ):
        # If overwriting, delete old file first
        if st.session_state.active_conv_id:
            delete_conversation(st.session_state.active_conv_id)

        new_id = save_conversation(save_name.strip(), st.session_state.messages)
        st.session_state.active_conv_id   = new_id
        st.session_state.active_conv_name = save_name.strip()
        st.toast(f'✅ Saved "{save_name.strip()}"', icon="✅")
        st.rerun()

    st.divider()

    # ── Conversation History ───────────────────────────────────────────────
    all_convs = list_conversations()

    st.markdown(f"""
    <div class="conv-header">
        <span class="conv-header-label">History</span>
        <span class="conv-count">{len(all_convs)}</span>
    </div>
    """, unsafe_allow_html=True)

    if not all_convs:
        st.markdown('<div class="conv-empty">No saved conversations yet</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="conv-list">', unsafe_allow_html=True)
        for conv in all_convs:
            is_active  = conv["id"] == st.session_state.active_conv_id
            active_cls = "active" if is_active else ""
            dt_str     = conv["saved_at"][:16].replace("T", " ") if conv["saved_at"] else "—"

            st.markdown(f"""
            <div class="conv-item {active_cls}">
                <div class="conv-item-name">{'◆ ' if is_active else ''}{conv['name']}</div>
                <div class="conv-item-meta">
                    <span>{conv['msg_count']} msg{"s" if conv['msg_count'] != 1 else ""}</span>
                    <span class="conv-item-dot"></span>
                    <span>{dt_str}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Load / delete buttons per item
            bc1, bc2 = st.columns([3, 1])
            with bc1:
                if st.button(f"Load", key=f"load_{conv['id']}", use_container_width=True):
                    name, msgs = load_conversation(conv["id"])
                    st.session_state.messages          = msgs
                    st.session_state.active_conv_id    = conv["id"]
                    st.session_state.active_conv_name  = name
                    st.session_state.selected_template = None
                    st.session_state.pending_prompt    = None
                    st.toast(f'📂 Loaded "{name}"')
                    st.rerun()
            with bc2:
                if st.button("🗑", key=f"del_{conv['id']}", use_container_width=True):
                    delete_conversation(conv["id"])
                    if st.session_state.active_conv_id == conv["id"]:
                        st.session_state.active_conv_id   = None
                        st.session_state.active_conv_name = None
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Tips ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="tips-box">
        <div class="tips-box-title">Prompt tips</div>
        <div class="tip-row"><span class="tip-icon">→</span> State language &amp; version upfront</div>
        <div class="tip-row"><span class="tip-icon">→</span> Share error messages verbatim</div>
        <div class="tip-row"><span class="tip-icon">→</span> Ask for step-by-step explanations</div>
        <div class="tip-row"><span class="tip-icon">→</span> Mention performance constraints</div>
        <div class="tip-row"><span class="tip-icon">→</span> Request tests alongside code</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Page Header ─────────────────────────────────────────────────────────────
user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
conv_badge = ""
if st.session_state.active_conv_name:
    conv_badge = f'<span class="conv-name-badge">📁 {st.session_state.active_conv_name}</span>'

st.markdown(f"""
<div class="page-header">
    <div class="page-header-icon">💻</div>
    <div>
        <div class="page-header-title">CodeMind {conv_badge}</div>
        <div class="page-header-sub">
            <span class="status-dot"></span>
            {MODEL_DISPLAY[model_key]} &nbsp;·&nbsp; {len(user_msgs)} message{"s" if len(user_msgs) != 1 else ""}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Chat Area ────────────────────────────────────────────────────────────────
chat_area = st.container()

with chat_area:
    visible = [m for m in st.session_state.messages if m["role"] != "system"]

    if not visible:
        # ── Home ──────────────────────────────────────────────────────────
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">💻</div>
            <div class="empty-state-title">Ready to assist</div>
            <div class="empty-state-sub">
                Ask me to write, debug, review, or explain code.
                I specialise in clean, production-ready solutions.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="starter-grid">
            <div class="starter-card"><span class="starter-icon">🛠</span><div class="starter-text">Write a Python function to parse and validate JSON configs</div></div>
            <div class="starter-card"><span class="starter-icon">🔍</span><div class="starter-text">Review my code for bugs and performance issues</div></div>
            <div class="starter-card"><span class="starter-icon">🧪</span><div class="starter-text">Generate unit tests with pytest for my module</div></div>
            <div class="starter-card"><span class="starter-icon">⚙️</span><div class="starter-text">Explain the time complexity of this algorithm</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Templates ─────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Prebuilt Templates</div>', unsafe_allow_html=True)

        sel = st.session_state.selected_template
        if sel is None:
            st.markdown('<div class="select-hint">Click a template to select it, then hit <span>Use Template</span></div>', unsafe_allow_html=True)
        else:
            t = TEMPLATES[sel]
            st.markdown(f'<div class="select-hint"><span>{t["icon"]} {t["title"]}</span> selected — ready to generate</div>', unsafe_allow_html=True)

        cols = st.columns(3, gap="small")
        for i, t in enumerate(TEMPLATES):
            with cols[i]:
                is_sel    = (sel == i)
                css_class = "tpl-btn-selected" if is_sel else "tpl-btn"
                check     = "✦ " if is_sel else ""
                label     = f"{check}{t['icon']}  {t['title']}\n\n**{t['tag']}**\n\n{t['desc']}"
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                if st.button(label, key=f"tpl_card_{i}", use_container_width=True):
                    st.session_state.selected_template = i if sel != i else None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        cta_col = st.columns([1, 2, 1])[1]
        with cta_col:
            st.markdown('<div class="use-tpl-btn">', unsafe_allow_html=True)
            cta_label = (
                f"▶  Use Template  ·  {TEMPLATES[sel]['title']}"
                if sel is not None else "▶  Use Template"
            )
            if st.button(cta_label, key="use_tpl", use_container_width=True, disabled=(sel is None)):
                st.session_state.pending_prompt    = TEMPLATES[sel]["prompt"]
                st.session_state.selected_template = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # ── Render History ────────────────────────────────────────────────
        for msg in visible:
            avatar = "👤" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

# ─── Chat Input ───────────────────────────────────────────────────────────────
user_input = st.chat_input("Write a function, debug code, explain a concept…")
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# ─── Streaming Response ───────────────────────────────────────────────────────
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with chat_area:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

    with chat_area:
        with st.chat_message("assistant", avatar="🤖"):
            placeholder   = st.empty()
            streamed_text = ""

            try:
                trimmed = [st.session_state.messages[0]] + st.session_state.messages[-10:]

                stream = ollama.chat(
                    model=model_key,
                    messages=trimmed,
                    stream=True,
                    options={
                        "num_thread":  6,
                        "num_ctx":     num_ctx,
                        "num_batch":   128,
                        "temperature": temperature,
                        "top_p":       top_p,
                        "use_mlock":   True,
                    }
                )

                for chunk in stream:
                    token          = chunk["message"]["content"]
                    streamed_text += token
                    placeholder.markdown(streamed_text + " ▍")

                placeholder.markdown(streamed_text)
                st.session_state.messages.append({"role": "assistant", "content": streamed_text})

                # ── Auto-save after EVERY reply (new or existing chat) ─────
                # For brand-new conversations, auto-generate a name from the
                # first user message so nothing is ever lost.
                if not st.session_state.active_conv_name:
                    first_user = next(
                        (m["content"] for m in st.session_state.messages if m["role"] == "user"),
                        "Untitled"
                    )
                    st.session_state.active_conv_name = first_user[:50].replace("\n", " ").strip()

                # Overwrite the existing file (or create a new one)
                if st.session_state.active_conv_id:
                    delete_conversation(st.session_state.active_conv_id)

                new_id = save_conversation(
                    st.session_state.active_conv_name,
                    st.session_state.messages
                )
                st.session_state.active_conv_id = new_id

                # Rerun so the home-screen / template panel is replaced by
                # the clean chat view on the very first message.
                st.rerun()

            except Exception as err:
                st.error(f"**Error:** {err}")
                st.info(
                    "Make sure Ollama is running:  `ollama serve`\n\n"
                    "Then pull a model:\n"
                    "```\nollama pull hf.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF:Q5_K_M\n```"
                )

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    CodeMind · local inference via Ollama · conversations saved to ./codemind_conversations/
</div>
""", unsafe_allow_html=True)
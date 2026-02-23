# 🤠 Prompt Cowboy Agentic AI

A local Gradio app with a **3-agent pipeline** powered by `gpt-4o-mini`:

```
Your Goal → [Agent 1: Prompt Cowboy] → [Agent 2: Code Generator] → [Agent 3: Reviewer] → Final Code
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install gradio openai
```

### 2. Set your OpenAI API key
Either edit `config.py`:
```python
OPENAI_API_KEY = "sk-your-actual-key-here"
```
Or set an environment variable (recommended):
```bash
export OPENAI_API_KEY="sk-your-actual-key-here"
```

### 3. Run the app
```bash
python app.py
```
Open your browser at: **http://localhost:7860**

---

## 🔄 Agent Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│              "What do you want to build?"                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  🤠  AGENT 1 — Prompt Cowboy                                    │
│                                                                 │
│  INPUT : Vague user goal                                        │
│  ACTION: Applies Prompt Cowboy formula:                         │
│          Role → Context → Task → Requirements → Output Format   │
│  OUTPUT: Precision-engineered prompt (copy to Claude.ai!)       │
└────────────────────────────┬────────────────────────────────────┘
                             │  optimized prompt
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  ⚙️  AGENT 2 — Code Generator                                   │
│                                                                 │
│  INPUT : Optimized prompt from Agent 1                          │
│  ACTION: Sends prompt to gpt-4o-mini with strict code-only      │
│          system rules (type hints, docstrings, error handling)  │
│  OUTPUT: Raw working code                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │  raw code + original goal
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  ✅  AGENT 3 — Reviewer                                         │
│                                                                 │
│  INPUT : Raw code + original user goal                          │
│  ACTION: Cross-checks goal vs code, fixes bugs, adds            │
│          HOW TO RUN block + DEPENDENCIES comment                │
│  OUTPUT: Final polished, documented, ready-to-run code          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GRADIO UI TABS                             │
│  📝 Optimized Prompt  |  💻 Final Code  |  🔍 Pipeline Log     │
└─────────────────────────────────────────────────────────────────┘
```

**Orchestration** is handled by `app.py` — it calls each agent sequentially, passing the output of one as the input to the next. No agent talks to another directly; the orchestrator owns the data flow.

---

## 🧠 Agent Reference

| Agent | Role | Model |
|-------|------|-------|
| 🤠 Prompt Cowboy Agent | Rewrites your vague goal into a precision prompt | gpt-4o-mini |
| ⚙️ Code Generator Agent | Generates code from the optimized prompt | gpt-4o-mini |
| ✅ Reviewer Agent | Reviews, fixes, and documents the code | gpt-4o-mini |

---

## 💡 Using Free Claude Queries Wisely

Claude.ai gives you **~5 free messages per day** on the web UI. Here's how to make the most of them:

1. Run this app to generate the **Optimized Prompt** (Agent 1 output)
2. Copy the prompt from the **"📝 Optimized Prompt"** tab
3. Paste it directly into [Claude.ai](https://claude.ai) — Claude will produce better code than gpt-4o-mini for complex tasks
4. Use the **Code Generator** tab output as a draft to refine with Claude

**Pro tip**: Use `gpt-4o-mini` for fast iteration/testing, save Claude's free queries for your most important/complex tasks.

---

## 📁 File Structure

```
prompt_cowboy_agent/
├── app.py          # Main Gradio app + orchestrator
├── agents.py       # Three agent classes
├── config.py       # API key & model config
├── requirements.txt
└── README.md
```

---

## 🔧 Customization

- **Change model**: Edit `MODEL` in `config.py` (e.g. `"gpt-4o"` for stronger results)
- **Add agents**: Subclass `BaseAgent` in `agents.py`
- **Modify prompts**: Edit the `*_SYSTEM` strings in `agents.py`
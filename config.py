"""
config.py — Configuration for Prompt Cowboy Agent
Set your OpenAI API key here or via environment variable.
"""

import os
from dotenv import load_dotenv
# ── OpenAI Settings ──────────────────────────────────────────────────────────
# Option 1: Set directly here (not recommended for production)
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Using gpt-4o-mini as requested (cost-efficient, fast)
MODEL = "gpt-4o-mini"

# ── App Settings ─────────────────────────────────────────────────────────────
APP_HOST = "0.0.0.0"
APP_PORT = 7860

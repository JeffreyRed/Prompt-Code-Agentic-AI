"""
agents.py — Three specialized AI agents
Each agent wraps an OpenAI chat call with a focused system prompt.
"""

from openai import OpenAI


class BaseAgent:
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def chat(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()


# ─── Agent 1: Prompt Cowboy ───────────────────────────────────────────────────

PROMPT_COWBOY_SYSTEM = """
You are the Prompt Cowboy — the #1 prompt engineer on the internet.
Your job is to take a vague user goal and transform it into a laser-precise,
production-grade prompt that will make any LLM (especially Claude) produce
excellent, clean, well-structured code.

Follow this Prompt Cowboy formula:
1. ROLE — Define an expert persona for the AI
2. CONTEXT — State the exact problem domain and constraints  
3. TASK — One clear, unambiguous instruction
4. REQUIREMENTS — Bullet list: language, style, edge cases, error handling
5. OUTPUT FORMAT — Exactly how the code should be structured
6. EXAMPLE (optional) — A quick sketch of the expected result

Rules:
- Be specific, not generic
- Include error handling requirements
- Specify coding style (PEP8, type hints, docstrings, etc.)
- Keep it under 400 words but pack maximum information density
- Write the prompt in second person ("You are...", "Your task is...")
- End with: "Produce only the final code. No explanations unless inside comments."
"""


class PromptCowboyAgent(BaseAgent):
    def run(self, user_goal: str) -> str:
        return self.chat(
            system=PROMPT_COWBOY_SYSTEM,
            user=f"Transform this user goal into a Prompt Cowboy optimized prompt:\n\n{user_goal}",
        )


# ─── Agent 2: Code Generator ──────────────────────────────────────────────────

CODE_GEN_SYSTEM = """
You are an elite software engineer. You receive a carefully engineered prompt
and your only job is to produce clean, working, production-grade code.

Rules:
- Follow the prompt's requirements exactly
- Write clean, well-commented code
- Include proper error handling
- Use type hints where applicable (Python)
- Add a brief docstring to every function/class
- If the task requires multiple files, clearly label each with: # === filename.py ===
- Produce ONLY code — no markdown fences, no prose explanations outside comments
"""


class CodeGeneratorAgent(BaseAgent):
    def run(self, optimized_prompt: str) -> str:
        return self.chat(
            system=CODE_GEN_SYSTEM,
            user=optimized_prompt,
        )


# ─── Agent 3: Reviewer ────────────────────────────────────────────────────────

REVIEWER_SYSTEM = """
You are a senior code reviewer and technical writer.
You receive generated code and the original user goal.

Your tasks:
1. Check the code solves the original goal
2. Fix any obvious bugs or missing imports
3. Add a clear # HOW TO RUN comment block at the top
4. Add a # DEPENDENCIES line listing pip install commands
5. If the code is good, return it with those additions
6. If there are problems, fix them inline

Output format:
- Start with: # ✅ REVIEWED BY AGENT 3
- Then the HOW TO RUN block
- Then the DEPENDENCIES line  
- Then the complete corrected code
- End with a short 2-3 line summary comment explaining what the code does
"""


class ReviewerAgent(BaseAgent):
    def run(self, code: str, original_goal: str) -> str:
        return self.chat(
            system=REVIEWER_SYSTEM,
            user=f"Original goal: {original_goal}\n\nCode to review:\n{code}",
        )
"""
🤠 Prompt Cowboy Agentic AI — Local Gradio App
Uses gpt-4o-mini with a multi-agent pipeline:
  Agent 1: Prompt Engineer (Prompt Cowboy style)
  Agent 2: Code Generator (Claude-optimized prompts)
  Agent 3: Code Reviewer / Output Formatter
"""

import gradio as gr
from agents import PromptCowboyAgent, CodeGeneratorAgent, ReviewerAgent
from config import OPENAI_API_KEY, MODEL

# ─── Orchestrator ────────────────────────────────────────────────────────────

def run_pipeline(user_goal: str, show_steps: bool):
    """
    Main agentic pipeline:
      1. PromptCowboyAgent → crafts optimized prompt
      2. CodeGeneratorAgent → generates code using that prompt
      3. ReviewerAgent → reviews & formats the final output
    """
    steps = []

    # Agent 1: Prompt Engineer
    prompt_agent = PromptCowboyAgent(model=MODEL, api_key=OPENAI_API_KEY)
    optimized_prompt = prompt_agent.run(user_goal)
    steps.append(("🤠 Prompt Cowboy Agent", optimized_prompt))

    # Agent 2: Code Generator
    code_agent = CodeGeneratorAgent(model=MODEL, api_key=OPENAI_API_KEY)
    raw_code = code_agent.run(optimized_prompt)
    steps.append(("⚙️ Code Generator Agent", raw_code))

    # Agent 3: Reviewer
    reviewer = ReviewerAgent(model=MODEL, api_key=OPENAI_API_KEY)
    final_output = reviewer.run(raw_code, user_goal)
    steps.append(("✅ Reviewer Agent", final_output))

    # Build display
    if show_steps:
        log = ""
        for name, content in steps:
            log += f"\n{'='*60}\n{name}\n{'='*60}\n{content}\n"
        return optimized_prompt, final_output, log
    else:
        return optimized_prompt, final_output, "Enable 'Show agent steps' to see the pipeline."


# ─── Gradio UI ────────────────────────────────────────────────────────────────

THEME = gr.themes.Base(
    primary_hue="amber",
    secondary_hue="orange",
    neutral_hue="stone",
    font=[gr.themes.GoogleFont("Syne"), gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
)

CSS = """
body { background: #0f0e0c; }
.gradio-container { max-width: 1100px; margin: auto; }
#title { text-align: center; padding: 2rem 0 0.5rem; }
#title h1 { font-size: 3rem; background: linear-gradient(135deg, #f59e0b, #ef4444); 
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
#title p  { color: #a8a29e; font-size: 1rem; }
.tab-nav button { font-family: 'Syne', sans-serif; font-weight: 700; }
"""

with gr.Blocks(theme=THEME, css=CSS, title="🤠 Prompt Cowboy Agent") as demo:

    gr.HTML("""
    <div id="title">
      <h1>🤠 Prompt Cowboy Agent</h1>
      <p>Multi-agent AI · Prompt Engineer → Code Generator → Reviewer · Powered by gpt-4o-mini</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=2):
            user_goal = gr.Textbox(
                label="What do you want to build?",
                placeholder="e.g. A Python script that scrapes job listings from LinkedIn and saves them to CSV...",
                lines=4,
            )
            show_steps = gr.Checkbox(label="Show agent steps (pipeline log)", value=True)
            run_btn = gr.Button("🚀 Run Agent Pipeline", variant="primary", size="lg")

        with gr.Column(scale=1):
            gr.Markdown("""
### How it works
1. **Prompt Cowboy Agent** rewrites your idea into a precision-engineered prompt
2. **Code Generator Agent** sends that prompt to `gpt-4o-mini` and gets code back
3. **Reviewer Agent** polishes the output and adds usage notes

> 💡 **Free Claude queries**: Claude.ai offers ~5 free messages/day on the web UI. 
> To maximize them, copy the **Optimized Prompt** tab output and paste it directly into Claude.ai for best results!
            """)

    with gr.Tabs():
        with gr.TabItem("📝 Optimized Prompt"):
            optimized_prompt_out = gr.Textbox(
                label="Prompt Cowboy Output (copy this to Claude.ai!)",
                lines=12,
                show_copy_button=True,
            )
        with gr.TabItem("💻 Generated Code"):
            code_out = gr.Code(
                label="Final Code",
                language="python",
                lines=30,
            )
        with gr.TabItem("🔍 Agent Pipeline Log"):
            pipeline_log = gr.Textbox(
                label="Step-by-step agent reasoning",
                lines=30,
            )

    run_btn.click(
        fn=run_pipeline,
        inputs=[user_goal, show_steps],
        outputs=[optimized_prompt_out, code_out, pipeline_log],
    )

    gr.Markdown("""
---
**Model**: `gpt-4o-mini` &nbsp;|&nbsp; **Framework**: Gradio + OpenAI SDK &nbsp;|&nbsp; 
**Tip**: Use the optimized prompt on [Claude.ai](https://claude.ai) free tier for best code quality!
    """)

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
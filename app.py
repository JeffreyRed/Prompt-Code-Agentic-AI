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
import os, re, datetime

# ─── Orchestrator ────────────────────────────────────────────────────────────
def save_output_files(user_goal: str, optimized_prompt: str, final_code: str):
    """Save prompt and generated code to output/project_name/"""
    # Create a slug from the goal for the folder name
    slug = re.sub(r'[^a-z0-9]+', '_', user_goal.lower())[:40].strip('_')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join("output", f"{slug}_{timestamp}")
    os.makedirs(folder, exist_ok=True)

    # Save the optimized prompt
    with open(os.path.join(folder, "optimized_prompt.md"), "w", encoding="utf-8") as f:
        f.write(optimized_prompt)

    # Detect multi-file output (Agent 2 labels them: # === filename.py ===)
    file_blocks = re.split(r'#\s*={3,}\s*([\w./]+)\s*={3,}', final_code)
    if len(file_blocks) > 1:
        # Odd indexes are filenames, even indexes are code blocks
        it = iter(file_blocks[1:])
        for filename, code in zip(it, it):
            filepath = os.path.join(folder, filename.strip())
            os.makedirs(os.path.dirname(filepath) or folder, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code.strip())
    else:
        # Single file — save as main.py
        with open(os.path.join(folder, "main.py"), "w", encoding="utf-8") as f:
            f.write(final_code)

    return folder

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

    saved_folder = save_output_files(user_goal, optimized_prompt, final_output)
    print(f"[OK] Files saved to: {saved_folder}")
    # Build display
    if show_steps:
        log = f"📁 Saved to: {saved_folder}\n"
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
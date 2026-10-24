"""Responsive Digital Twin portfolio UI for Gradio.

Use with an existing chat(message, history) callable:
    from digital_twin_portfolio import create_portfolio
    demo = create_portfolio(chat)
    demo.launch(theme=gr.themes.Base(), css=CSS)

The UI does not replace the chatbot backend or its OpenAI/Telegram tools.
"""

from __future__ import annotations

import base64
import inspect
import logging
from pathlib import Path
from typing import Callable

import gradio as gr

LOGGER = logging.getLogger(__name__)

GOLD = "#f1b746"
BLUE = "#4ca9ec"
PURPLE = "#a286ff"
EXAMPLES = [
    "Tell me about your background and experience.",
    "What AI projects have you worked on?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

ROOT = Path(__file__).resolve().parent
BACKGROUND = ROOT / "digital_twin_background.webp"
PROFILE_PHOTO = ROOT / "profile.jpg"
EMBEDDED_BACKGROUND = "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"


def _background_data_uri() -> str:
    if BACKGROUND.exists():
        data = base64.b64encode(BACKGROUND.read_bytes()).decode("ascii")
        return f'url("data:image/webp;base64,{data}")'
    return f'url("data:image/webp;base64,{EMBEDDED_BACKGROUND}")'


def _avatar_html() -> str:
    if PROFILE_PHOTO.exists():
        suffix = PROFILE_PHOTO.suffix.lower()
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        image = base64.b64encode(PROFILE_PHOTO.read_bytes()).decode("ascii")
        return f'<img src="data:{mime};base64,{image}" alt="Profile photo" />'
    return '<span aria-label="AS initials">AS</span>'


CSS = r"""
:root, body, body.dark {
  color-scheme: dark;
  --dt-navy: #08172d;
  --dt-gold: #f1b746;
  --dt-blue: #73bfff;
  --dt-text: #eef5ff;
  --dt-muted: #a5b6d4;
  --dt-border: rgba(165, 193, 239, .23);
  --dt-surface: rgba(18, 35, 61, .76);
  --dt-surface-strong: rgba(10, 25, 49, .89);
}
html, body, gradio-app {
  background-color: #08172d !important;
  background-image: linear-gradient(110deg, rgba(2,9,22,.65), rgba(8,22,43,.54) 54%, rgba(10,19,44,.41)), __BACKGROUND__;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}
.gradio-container, .gradio-container .main, .gradio-container .contain {
  background: transparent !important;
  color: var(--dt-text) !important;
}
.gradio-container {
  max-width: 1500px !important;
  padding: 28px 34px 48px !important;
  font-family: Inter, ui-sans-serif, system-ui, 'Segoe UI', sans-serif !important;
}
.gradio-container * { box-sizing: border-box; min-width: 0; }
.gradio-container footer, .gradio-container .built-with, .gradio-container .show-api {display:none !important;}

/* Site header */
.dt-brand { display: flex; gap: 14px; align-items: flex-start; margin: 2px 0 26px; }
.dt-brand-mark { width: 20px; height: 20px; margin-top: 13px; flex:0 0 20px; border-radius: 50%;
  background:var(--dt-gold); border: 5px solid #26394e; box-shadow: 0 0 0 2px rgba(241,183,70,.20), 0 0 24px rgba(241,183,70,.24); }
.dt-brand h1 {margin: 0 !important; font-weight: 800 !important; font-size: clamp(31px,3vw,44px) !important; line-height:1.1; letter-spacing:-.05em; color:#f5f8ff !important;}
.dt-brand p {margin: 9px 0 0; color:#bccbe4; font-size:15px;}

/* Two-column layout */
#dt-layout { gap: 32px !important; align-items: flex-start !important; }
#dt-sidebar { max-width: 310px !important; padding: 4px 8px 0 4px; }
#dt-main { min-width:0 !important; }
.dt-profile {color:#e6eeff; padding-top:8px;}
.dt-avatar { height: 156px; width: 156px; display:flex; align-items:center; justify-content:center;
  overflow:hidden; border-radius:100%; border:3px solid rgba(161,187,255,.83);
  box-shadow: 0 0 0 8px rgba(21,40,75,.58), 0 0 35px rgba(65,140,235,.22);
  margin: 12px 0 26px 12px; background: linear-gradient(145deg,#1b4874,#403878); }
.dt-avatar img { height:100%; width:100%; object-fit:cover; }
.dt-avatar span { font-size:60px; color:#fff; letter-spacing:-.07em; font-weight:750; }
.dt-profile h2 { font-size:29px; font-weight:760; letter-spacing:-.045em; margin:0 0 2px; color:#f6f8ff; }
.dt-profile .dt-role {font-size:15px; font-weight:680; color:#bfd4f4; margin:0;}
.dt-profile .dt-degree {font-size:13px; color:#9fb1cf; line-height:1.65; margin:9px 0 19px;}
.dt-profile .dt-bio {font-size:14px; color:#b5c6e2; line-height:1.75; margin:0 0 20px;}
.dt-profile hr {border:0; border-top:1px solid rgba(170,199,242,.28);margin:17px 0 21px;}
.dt-fact {display:flex;align-items:flex-start;gap:13px;margin-bottom:19px;}
.dt-fact .dt-fact-icon {display:grid;place-items:center;width:29px;height:29px;flex:0 0 29px;border-radius:9px;background:rgba(100,158,239,.12);color:#9fceff;font-size:17px;}
.dt-fact b {display:block;font-size:12px;font-weight:650;color:#e2ecfd;}
.dt-fact small {display:block;font-size:11px;color:#91a5c7;line-height:1.5;margin-top:3px;}
.dt-profile-links {display:flex;gap:9px;flex-wrap:wrap;padding-top:3px;}
.dt-profile-links a,.dt-link {border:1px solid var(--dt-border);border-radius:100px;padding:9px 13px;
  color:#c9dfff !important;text-decoration:none !important;font-size:12px;font-weight:580;background:rgba(16,35,62,.55);transition:.2s;}
.dt-profile-links a:hover,.dt-link:hover{border-color:var(--dt-gold);color:var(--dt-gold)!important;transform:translateY(-1px);}

/* Navigation tabs */
#dt-tabs .tab-nav {background:transparent!important;border:0!important;gap:9px!important;justify-content:flex-end!important;
  margin:0 0 24px!important; padding:0 0 5px!important;}
#dt-tabs .tab-nav button {background:transparent!important;border:0!important;border-bottom:3px solid transparent!important;
  color:#a6bbdc!important;border-radius:0!important;font-weight:600!important;padding:12px 14px!important;
  font-size:14px!important;box-shadow:none!important;}
#dt-tabs .tab-nav button:hover{color:#fff!important;}
#dt-tabs .tab-nav button.selected, #dt-tabs .tab-nav button[aria-selected="true"] {color:#fff!important;border-bottom-color:var(--dt-gold)!important;}
#dt-tabs .tabitem {background:transparent!important;border:0!important;padding:0!important;}

/* Chat shell */
.dt-chat-shell{border:1px solid rgba(165,193,239,.34);border-radius:23px 23px 0 0;
  padding:27px 27px 11px;background:linear-gradient(136deg,rgba(25,46,79,.87),rgba(25,39,75,.74) 55%,rgba(41,38,75,.82));
  box-shadow:0 20px 60px rgba(3,12,28,.32);backdrop-filter:blur(18px);}
.dt-chat-heading{display:flex;gap:17px;align-items:flex-start;padding-bottom:18px;}
.dt-chat-heading .dt-chat-icon{font-size:32px;line-height:1;color:#8cccff;}
.dt-chat-heading h2{font-size:25px;font-weight:730;letter-spacing:-.035em;color:#f5f8ff;margin:0 0 6px;}
.dt-chat-heading p{color:#b3c3df;font-size:14px;margin:0;line-height:1.5;}
.dt-welcome{min-height:365px;border-radius:19px;background:rgba(3,13,30,.32);padding:45px 27px;
  display:flex;align-items:center;justify-content:center;text-align:center;}
.dt-welcome-inner{max-width:560px;}
.dt-welcome-mark{font-size:35px;width:64px;height:64px;display:grid;place-items:center;margin:0 auto 16px;
  border:1px solid rgba(151,180,255,.4);border-radius:18px;background:rgba(101,92,202,.19);}
.dt-welcome h3{margin:0 0 10px;color:#f4f8ff;font-size:23px;font-weight:700;}
.dt-welcome p{margin:0;color:#b8c7df;font-size:14px;line-height:1.7;}

/* Chatbot is a single framed conversation, not nested colored boxes */
#dt-chatbot{background:rgba(4,14,30,.35)!important;border:0!important;border-radius:18px!important;
  padding:10px!important;box-shadow:none!important;}
#dt-chatbot .message-row {background:transparent!important;border:0!important;box-shadow:none!important;}
#dt-chatbot .message-row.user-row .message,
#dt-chatbot .message-row.user-row .bubble,
#dt-chatbot .message-row.user-row .message-bubble,
#dt-chatbot .message-row[data-role="user"] .message {
  background:linear-gradient(115deg,#236fba,#334dae)!important;
  color:#fff!important;border:1px solid rgba(130,185,255,.24)!important;
  border-radius:18px 18px 5px 18px!important;box-shadow:none!important;
}
#dt-chatbot .message-row.bot-row .message,
#dt-chatbot .message-row.bot-row .bubble,
#dt-chatbot .message-row.bot-row .message-bubble,
#dt-chatbot .message-row[data-role="assistant"] .message {
  background:rgba(22,37,63,.90)!important;color:#e8efff!important;
  border:1px solid rgba(155,181,225,.24)!important;border-radius:18px 18px 18px 5px!important;box-shadow:none!important;
}
#dt-chatbot .message p, #dt-chatbot .message-bubble p, #dt-chatbot .bubble p {line-height:1.65!important; font-size:14px!important;}
#dt-chatbot .message-row .message .message {background:transparent!important;border:0!important;}

/* Prompt chips */
.dt-prompt-title {font-size:11px;color:#8ca1c1;text-transform:uppercase;font-weight:700;letter-spacing:.12em;
 margin:15px 1px 8px;}
#dt-prompts{gap:9px!important;margin:12px 0 18px!important;}
#dt-prompts button{background:rgba(15,34,65,.71)!important;color:#d2e1fc!important;
 border:1px solid rgba(150,177,224,.42)!important;border-radius:30px!important;
 padding:10px 17px!important;min-height:41px!important;font-size:12px!important;
 font-weight:550!important;line-height:1.35!important;transition:all .2s ease!important;}
#dt-prompts button:hover{border-color:#efb948!important;background:rgba(39,53,84,.9)!important;transform:translateY(-2px);color:#fff!important;}

/* Input composer */
#dt-composer{padding:10px!important;background:rgba(13,30,58,.87)!important;
 border:1px solid rgba(145,180,240,.62)!important;border-radius:18px!important;
 align-items:stretch!important;gap:10px!important;box-shadow:0 15px 35px rgba(0,8,27,.2);backdrop-filter:blur(16px);}
#dt-message{background:transparent!important;border:0!important;box-shadow:none!important;}
#dt-message textarea,#dt-message input{background:transparent!important;color:#f2f7ff!important;
 font-size:14px!important;padding:11px 10px!important;line-height:1.5!important;outline:none!important;box-shadow:none!important;
 border:0!important;}
#dt-message textarea::placeholder,#dt-message input::placeholder{color:#899ebd!important;}
#dt-send {background:var(--dt-gold)!important;color:#13213b!important;border:0!important;border-radius:12px!important;
 min-width:54px!important;max-width:54px!important;font-size:24px!important;font-weight:600!important;transition:transform .2s!important;}
#dt-send:hover{transform:translateY(-1px) scale(1.025)!important;filter:brightness(1.08);}
.dt-disclaimer{text-align:center;color:#7e95b8;font-size:11px;padding:12px 0 0;}

/* Secondary tab panels */
.dt-section{background:rgba(13,29,54,.83);border:1px solid var(--dt-border);border-radius:20px;
  padding:28px 30px;min-height:515px;backdrop-filter:blur(20px);}
.dt-section h2{font-size:27px;margin:0 0 10px;color:#f4f8ff;}
.dt-section .dt-section-lead{font-size:14px;color:#a9bfdf;line-height:1.7;margin:0 0 22px;}
.dt-info-card{border:1px solid rgba(157,188,236,.2);background:rgba(17,39,72,.65);
 border-radius:15px;padding:18px 20px;margin:12px 0;}
.dt-info-card h3{font-size:16px;color:#e9f3ff;margin:0 0 7px;}
.dt-info-card p{font-size:13px;color:#b5c6e1;line-height:1.65;margin:0;}
.dt-tagline{font-size:12px;color:#e8c679;margin-top:8px;}
.dt-pills {display:flex;flex-wrap:wrap;gap:9px;}
.dt-pills span {border:1px solid rgba(140,176,236,.31);padding:10px 14px;border-radius:24px;
 background:rgba(52,76,121,.22);font-size:13px;color:#dce8fb;}

@media(max-width:1000px){
 .gradio-container{padding:22px 18px 38px!important;}
 #dt-layout{gap:20px!important;}
 #dt-sidebar{max-width:250px!important;}
 .dt-avatar{width:120px;height:120px;}
 .dt-profile h2{font-size:24px;}
 #dt-tabs .tab-nav button{font-size:12px!important;padding:10px 8px!important;}
}
@media(max-width:760px){
 .gradio-container{padding:17px 12px 30px!important;}
 #dt-layout{flex-direction:column!important;}
 #dt-sidebar{width:100%!important;max-width:none!important;}
 .dt-profile{display:grid;grid-template-columns:88px 1fr;column-gap:20px;align-items:start;padding:6px 4px 8px;}
 .dt-avatar{width:80px;height:80px;margin:5px 0;grid-row:span 3;border-width:2px;box-shadow:0 0 0 4px rgba(21,40,75,.58);}
 .dt-avatar span{font-size:34px;}
 .dt-profile h2{font-size:23px;align-self:end;}
 .dt-role,.dt-degree{grid-column:2;}
 .dt-profile .dt-bio,.dt-profile hr,.dt-profile .dt-facts{display:none;}
 .dt-profile-links{grid-column:2;}
 #dt-main{width:100%!important;}
 #dt-tabs .tab-nav{justify-content:flex-start!important;overflow-x:auto!important;flex-wrap:nowrap!important;}
 #dt-tabs .tab-nav button{white-space:nowrap!important;}
 .dt-chat-shell{padding:16px 13px 10px;border-radius:17px 17px 0 0;}
 .dt-chat-heading h2{font-size:21px;}
 .dt-chat-heading p{font-size:12px;}
 .dt-welcome{min-height:305px;padding:28px 18px;}
 #dt-composer{padding:8px!important;}
 .dt-section{padding:22px 17px;min-height:350px;}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important;}}
""".replace("__BACKGROUND__", _background_data_uri())


def _sidebar_html() -> str:
    return f"""
    <div class="dt-profile">
      <div class="dt-avatar">{_avatar_html()}</div>
      <h2>Aram Salehi</h2>
      <p class="dt-role">AI &amp; Medical Imaging Engineer</p>
      <p class="dt-degree">PhD research completed · defense pending<br>Radboudumc &amp; LUMC</p>
      <p class="dt-bio">I work at the intersection of artificial intelligence,
        machine learning, and MRI—building practical, reproducible solutions for research and real-world use.</p>
      <hr>
      <div class="dt-facts">
        <div class="dt-fact"><span class="dt-fact-icon">🎓</span><div><b>PhD research</b><small>Radboudumc · LUMC</small></div></div>
        <div class="dt-fact"><span class="dt-fact-icon">◉</span><div><b>AI for medical imaging</b><small>Deep learning · MRI · Harmonization</small></div></div>
        <div class="dt-fact"><span class="dt-fact-icon">▤</span><div><b>Research &amp; publications</b><small>Scientific ML · Segmentation · Reconstruction</small></div></div>
        <div class="dt-fact"><span class="dt-fact-icon">⌘</span><div><b>From research to practice</b><small>Python · PyTorch · Docker</small></div></div>
      </div>
      <div class="dt-profile-links">
        <a href="https://github.com/AramSalehi" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
        <a href="https://www.linkedin.com/in/aram-salehi/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
      </div>
    </div>
    """


WELCOME = """
<div class="dt-welcome"><div class="dt-welcome-inner">
  <div class="dt-welcome-mark">✦</div>
  <h3>Welcome to my digital twin</h3>
  <p>Ask me about my research, AI and machine learning projects, technical
     skills, academic experience, or how we might collaborate.</p>
</div></div>
"""

RESEARCH = """
<div class="dt-section"><h2>Research &amp; publications</h2>
<p class="dt-section-lead">My research focuses on machine learning methods for MRI, with an emphasis on practical validation and reproducibility.</p>
<div class="dt-info-card"><h3>Low-field MRI enhancement</h3><p>Developing deep learning approaches to improve low-field MRI image quality, including denoising and reconstruction.</p></div>
<div class="dt-info-card"><h3>Cross-field MRI harmonization</h3><p>Working on conditional models for MRI harmonization across field strengths and image contrasts.</p></div>
<div class="dt-info-card"><h3>Automated medical-image segmentation</h3><p>Applying 3D transformer architectures to brain MRI analysis and anatomical measurements.</p></div>
<p class="dt-tagline">Ask the chatbot for details about my publications and methods.</p>
</div>"""

PROJECTS = """
<div class="dt-section"><h2>Selected projects</h2>
<p class="dt-section-lead">A selection of research and software work—from experiments to reproducible pipelines.</p>
<div class="dt-info-card"><h3>Low-field MRI enhancement</h3><p>Image enhancement and reconstruction using deep learning, including transformer-based architectures.</p></div>
<div class="dt-info-card"><h3>MRI field-strength harmonization</h3><p>Developing unified conditional models for translating between MRI domains.</p></div>
<div class="dt-info-card"><h3>ROI-guided anatomical segmentation</h3><p>Automating anterior commissure area measurement from brain MRI.</p></div>
<div class="dt-info-card"><h3>Retrieval-augmented chatbot prototypes</h3><p>Building RAG applications with LangChain, vector databases, and local language models.</p></div>
<a class="dt-link" href="https://github.com/AramSalehi" target="_blank" rel="noopener noreferrer">View GitHub projects ↗</a>
</div>"""

SKILLS = """
<div class="dt-section"><h2>Technical skills</h2>
<p class="dt-section-lead">A blend of applied machine learning, imaging research, and software engineering.</p>
<div class="dt-info-card"><h3>AI &amp; machine learning</h3><div class="dt-pills"><span>PyTorch</span><span>Deep learning</span><span>Transformers</span><span>Computer vision</span><span>Segmentation</span><span>Generative AI</span></div></div>
<div class="dt-info-card"><h3>Medical imaging</h3><div class="dt-pills"><span>MRI</span><span>Image reconstruction</span><span>Harmonization</span><span>Validation</span><span>Image processing</span></div></div>
<div class="dt-info-card"><h3>Engineering</h3><div class="dt-pills"><span>Python</span><span>Git</span><span>Docker</span><span>SQL</span><span>GPU computing</span><span>LangChain / RAG</span></div></div>
</div>"""

CONTACT = """
<div class="dt-section"><h2>Let's connect</h2>
<p class="dt-section-lead">Interested in applied AI, machine learning, medical imaging, or research collaboration? Let's talk.</p>
<div class="dt-info-card"><h3>Professional networking</h3><p>Reach out through LinkedIn for collaboration opportunities, technical discussions, and roles.</p></div>
<div class="dt-info-card"><h3>Projects &amp; code</h3><p>Explore my public repositories on GitHub.</p></div>
<div class="dt-profile-links" style="margin-top:18px">
<a href="https://www.linkedin.com/in/aram-salehi/" target="_blank" rel="noopener noreferrer">Connect on LinkedIn ↗</a>
<a href="https://github.com/AramSalehi" target="_blank" rel="noopener noreferrer">Explore GitHub ↗</a>
</div><p class="dt-tagline">You can also ask the assistant how to get in touch.</p>
</div>"""


def create_portfolio(chat_fn: Callable[[str, list], str]):
    """Build a Gradio Blocks UI around an existing chat(message, history) function.

    chat_fn should accept a user message and prior history in the same format
    supplied by gr.ChatInterface(type='messages'). No OpenAI logic is rewritten.
    """
    with gr.Blocks(title="Digital Twin | Aram Salehi") as demo:
        gr.HTML("""<header class="dt-brand">
          <div class="dt-brand-mark"></div><div>
          <h1>Digital Twin</h1><p>AI assistant about my career, research and projects</p>
          </div></header>""")
        with gr.Row(elem_id="dt-layout"):
            with gr.Column(scale=1, min_width=250, elem_id="dt-sidebar"):
                gr.HTML(_sidebar_html())
            with gr.Column(scale=3, min_width=330, elem_id="dt-main"):
                with gr.Tabs(elem_id="dt-tabs"):
                    with gr.Tab("Chat", id="chat"):
                        with gr.Column(elem_classes=["dt-chat-shell"]):
                            gr.HTML("""<div class="dt-chat-heading"><div class="dt-chat-icon">▢</div>
                              <div><h2>Chat with my AI twin</h2>
                              <p>Ask about my background, research, projects, technical skills, or anything else.</p>
                              </div></div>""")
                            welcome = gr.HTML(WELCOME, visible=True)
                            chatbot = gr.Chatbot(
                                value=[],
                                label="Conversation", show_label=False, height=405,
                                visible=False, elem_id="dt-chatbot", layout="bubble",
                                buttons=["copy"],
                            )
                        gr.HTML('<div class="dt-prompt-title">Explore a topic</div>')
                        with gr.Row(elem_id="dt-prompts"):
                            prompt_buttons = [gr.Button(q, size="sm", scale=1, min_width=185)
                                              for q in EXAMPLES]
                        with gr.Row(elem_id="dt-composer"):
                            question = gr.Textbox(
                                placeholder="Ask me anything...", show_label=False,
                                lines=1, max_lines=4, scale=12, elem_id="dt-message",
                                container=False,
                            )
                            send = gr.Button("➤", variant="primary", scale=0, elem_id="dt-send")
                        gr.HTML('<div class="dt-disclaimer">Powered by AI · Responses may contain inaccuracies</div>')

                    with gr.Tab("Research", id="research"):
                        gr.HTML(RESEARCH)
                    with gr.Tab("Projects", id="projects"):
                        gr.HTML(PROJECTS)
                    with gr.Tab("Skills", id="skills"):
                        gr.HTML(SKILLS)
                    with gr.Tab("Contact", id="contact"):
                        gr.HTML(CONTACT)

        def add_question(message, history):
            history = list(history or [])
            if not isinstance(message, str) or not message.strip():
                return gr.update(value=history), message, gr.update()
            history.append({"role": "user", "content": message.strip()})
            return gr.update(value=history, visible=True), "", gr.update(visible=False)

        def generate_answer(history):
            history = list(history or [])
            if not history or history[-1].get("role") != "user":
                return history
            message = history[-1]["content"]
            previous_history = history[:-1]
            try:
                answer = chat_fn(message, previous_history)
                if inspect.isgenerator(answer):
                    # Original ChatInterface functions may stream partial strings.
                    # We show the final assembled response rather than replacing
                    # the Gradio state with iterator objects.
                    last = ""
                    for chunk in answer:
                        if chunk is not None:
                            last = str(chunk)
                    answer = last
                elif inspect.isawaitable(answer):
                    raise TypeError("Async chat functions need an async adapter.")
            except Exception:
                LOGGER.exception("Digital Twin chat backend failed")
                answer = "Sorry, something went wrong while generating a reply. Please try again."
            history.append({"role": "assistant", "content": str(answer or "")})
            return history

        triggers = [question.submit, send.click]
        event = gr.on(triggers=triggers, fn=add_question,
                      inputs=[question, chatbot],
                      outputs=[chatbot, question, welcome],
                      show_progress="hidden")
        event.then(fn=generate_answer, inputs=[chatbot], outputs=[chatbot],
                   show_progress="minimal")

        for prompt_button, prompt in zip(prompt_buttons, EXAMPLES):
            prompt_button.click(
                fn=lambda q=prompt: q,
                inputs=None,
                outputs=[question], show_progress="hidden"
            ).then(
                fn=add_question, inputs=[question, chatbot],
                outputs=[chatbot, question, welcome], show_progress="hidden"
            ).then(
                fn=generate_answer, inputs=[chatbot], outputs=[chatbot],
                show_progress="minimal"
            )

    return demo


if __name__ == "__main__":
    # Standalone demonstration. This does NOT call OpenAI.
    def demo_chat(message, history):
        return ("This is a UI preview. Your real OpenAI assistant will answer "
                "once you connect your existing chat function. You asked: " + message)

    create_portfolio(demo_chat).launch(
        css=CSS,
        theme=gr.themes.Base(primary_hue="amber", neutral_hue="slate"),
        footer_links=[],
    )

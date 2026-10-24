"""Professional Gradio Digital Twin theme with clean, non-nested chat bubbles."""

GOLD = "#ecad0a"
BLUE = "#209dd7"
PURPLE = "#753991"

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

CSS = r"""
/* Scope palette to Gradio, while supporting either color scheme. */
:root, body.dark {
  --twin-bg: #0b111c;
  --twin-card: #131e2d;
  --twin-message: #1c2a3d;
  --twin-border: #304054;
  --twin-text: #edf2fa;
  --twin-muted: #a2b0c3;
  --twin-accent: #e6aa21;
  --twin-blue: #267caf;
  --twin-link: #79c5f2;
  --twin-shadow: 0 18px 48px rgba(0, 0, 0, .22);
}
body:not(.dark) {
  --twin-bg: #f5f7fb;
  --twin-card: #fff;
  --twin-message: #f0f4f9;
  --twin-border: #dfe7f0;
  --twin-text: #1b293d;
  --twin-muted: #64748b;
  --twin-accent: #e6aa21;
  --twin-blue: #176991;
  --twin-link: #176991;
  --twin-shadow: 0 14px 42px rgba(28, 47, 75, .055);
}
html, body, gradio-app { background: var(--twin-bg) !important; }
.gradio-container {
  background: transparent !important;
  color: var(--twin-text) !important;
  width: 100% !important;
  max-width: 960px !important;
  margin: 0 auto !important;
  padding: 28px 22px 48px !important;
  font-family: Inter, ui-sans-serif, system-ui, 'Segoe UI', sans-serif !important;
}
.gradio-container * { box-sizing: border-box; min-width: 0; }
.gradio-container :is(.main, .contain, .wrap) { max-width: 100% !important; }

/* Heading */
.gradio-container h1 {
  color: var(--twin-text) !important;
  font-size: clamp(26px, 3vw, 35px) !important;
  font-weight: 750 !important;
  letter-spacing: -.04em !important;
  line-height: 1.2 !important;
  text-align: left !important;
  margin: 0 0 10px !important;
}
.gradio-container h1::before {
  content: '';
  display: inline-block;
  width: 9px;
  height: 9px;
  margin-right: 12px;
  vertical-align: middle;
  background: var(--twin-accent);
  border-radius: 50%;
  box-shadow: 0 0 0 5px rgba(230, 170, 33, .12);
}

/* One frame for the conversation. Avoid styling all .block children. */
.gradio-container .chatbot,
.gradio-container .chatbot.block {
  background: var(--twin-card) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 16px !important;
  box-shadow: var(--twin-shadow) !important;
  min-height: 460px !important;
  overflow: hidden;
}
.gradio-container .chatbot > :is(.block-label, .label-container),
.gradio-container .chatbot > label { display: none !important; }
.gradio-container .chatbot .placeholder { color: var(--twin-muted) !important; }
.gradio-container :is(.message-row, .message-wrap, .bubble-wrap) {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Reset ALL bubble layers first. Gradio can render .message inside .bubble
   or vice versa; styling each produces the nested cards seen in the screenshot. */
.gradio-container .message-row :is(.message, .message-bubble, .bubble) {
  background: transparent !important;
  border: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  color: inherit !important;
}

/* Style ONLY the outermost bubble-like element, never nested ones. */
.gradio-container .message-row :is(.message, .message-bubble, .bubble):not(
  :is(.message, .message-bubble, .bubble) :is(.message, .message-bubble, .bubble)
) {
  padding: 13px 17px !important;
  border-radius: 15px !important;
  max-width: min(100%, 740px);
  font-size: 14px !important;
  line-height: 1.65 !important;
}
.gradio-container :is(.user-row, .message-row[data-role="user"])
  :is(.message, .message-bubble, .bubble):not(
    :is(.message, .message-bubble, .bubble) :is(.message, .message-bubble, .bubble)
  ) {
  background: var(--twin-blue) !important;
  color: #fff !important;
  border-radius: 15px 15px 5px 15px !important;
}
.gradio-container :is(.bot-row, .message-row[data-role="assistant"])
  :is(.message, .message-bubble, .bubble):not(
    :is(.message, .message-bubble, .bubble) :is(.message, .message-bubble, .bubble)
  ) {
  background: var(--twin-message) !important;
  color: var(--twin-text) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 15px 15px 15px 5px !important;
}

/* Preserve Markdown formatting; avoid adding backgrounds to prose wrappers. */
.gradio-container .message-row :is(.prose, .markdown, .message-content) {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}
.gradio-container .message-row :is(.prose p, .message p, .message-bubble p, .bubble p) {
  color: inherit !important;
  font-size: 14px !important;
  line-height: 1.65 !important;
  margin: 0 0 10px !important;
}
.gradio-container .message-row p:last-child { margin-bottom: 0 !important; }
.gradio-container .message-row a { color: var(--twin-link) !important; }
.gradio-container .user-row a { color: #fff !important; }
.gradio-container .message-row pre {
  overflow-x: auto;
  border-radius: 9px;
  padding: 12px;
}

/* Input: restrained focus treatment */
.gradio-container :is(textarea, input[type="text"]) {
  color: var(--twin-text) !important;
  background: var(--twin-card) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 12px !important;
  padding: 12px 14px !important;
  min-height: 48px !important;
  font-family: inherit !important;
  font-size: 14px !important;
  box-shadow: none !important;
  transition: border-color .18s ease, box-shadow .18s ease;
}
.gradio-container :is(textarea, input[type="text"]):focus {
  border-color: var(--twin-accent) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(230, 170, 33, .14) !important;
}
.gradio-container textarea::placeholder { color: var(--twin-muted) !important; }

/* Do not style every button: Gradio's copy/share/clear toolbar is separate. */
.gradio-container button.primary,
.gradio-container button[variant="primary"],
.gradio-container button.submit,
.gradio-container button.submit-button {
  background: var(--twin-accent) !important;
  border: 1px solid var(--twin-accent) !important;
  color: #1a1b20 !important;
  border-radius: 11px !important;
  min-height: 46px !important;
  box-shadow: none !important;
}
.gradio-container :is(.chatbot .icon-button, .chatbot button[title]) {
  background: transparent !important;
  color: var(--twin-muted) !important;
  border: none !important;
  padding: 5px !important;
  min-height: 0 !important;
  box-shadow: none !important;
}

/* Suggested questions */
.gradio-container :is(.examples, .examples-holder, [data-testid="examples"]) {
  background: transparent !important;
  margin-top: 13px !important;
  padding: 0 !important;
}
.gradio-container :is(.examples button, .example, [data-testid="examples"] button) {
  color: var(--twin-text) !important;
  background: var(--twin-card) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 10px !important;
  padding: 10px 13px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  text-align: left !important;
  min-height: 0 !important;
  transition: border-color .18s ease, background .18s ease;
}
.gradio-container :is(.examples button, .example, [data-testid="examples"] button):hover {
  border-color: var(--twin-blue) !important;
  background: var(--twin-message) !important;
}
.gradio-container ::-webkit-scrollbar { width: 8px; }
.gradio-container ::-webkit-scrollbar-thumb {
  background: var(--twin-border);
  border-radius: 8px;
}
@media (max-width: 640px) {
  .gradio-container { padding: 18px 12px 28px !important; }
  .gradio-container .chatbot { min-height: 380px !important; }
  .gradio-container .message-row :is(.message, .message-bubble, .bubble):not(
    :is(.message, .message-bubble, .bubble) :is(.message, .message-bubble, .bubble)
  ) { padding: 11px 13px !important; }
}
@media (prefers-reduced-motion: reduce) {
  .gradio-container *, .gradio-container *::before, .gradio-container *::after {
    animation-duration: .01ms !important;
    transition-duration: .01ms !important;
  }
}
"""

JS = r"""
() => {
  document.title = 'Digital Twin | AI Portfolio Assistant';
  const watch = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };
  const scan = () => document.querySelectorAll('textarea').forEach(watch);
  scan();
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""

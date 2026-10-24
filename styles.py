"""Professional responsive styling for the Gradio Digital Twin application."""

GOLD = "#ecad0a"
BLUE = "#209dd7"
PURPLE = "#753991"

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

CSS = """
/* Brand and theme tokens */
:root, body.dark {
  --twin-gold: #ecad0a;
  --twin-blue: #209dd7;
  --twin-purple: #a78bfa;
  --twin-bg: #0b1019;
  --twin-surface: #121b2a;
  --twin-surface-2: #1b283a;
  --twin-border: #2a384b;
  --twin-text: #edf2f9;
  --twin-muted: #a0adbf;
  --twin-shadow: 0 14px 48px rgba(0,0,0,.22);
}
body:not(.dark) {
  --twin-bg: #f5f7fb;
  --twin-surface: #ffffff;
  --twin-surface-2: #edf2f8;
  --twin-border: #dce4ee;
  --twin-text: #172234;
  --twin-muted: #627187;
  --twin-shadow: 0 12px 36px rgba(32,52,80,.07);
}
html, body, gradio-app { background: var(--twin-bg) !important; }
footer, .built-with, .show-api, .api-docs { display: none !important; }
.gradio-container {
  width: 100% !important;
  max-width: 980px !important;
  margin: 0 auto !important;
  padding: 38px 28px 56px !important;
  background: transparent !important;
  color: var(--twin-text) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif !important;
}
.gradio-container *, .gradio-container *::before, .gradio-container *::after {
  box-sizing: border-box;
}
.gradio-container h1 {
  color: var(--twin-text) !important;
  font-size: clamp(25px, 3vw, 36px) !important;
  line-height: 1.18 !important;
  letter-spacing: -.045em !important;
  font-weight: 750 !important;
  margin: 4px 0 14px !important;
}
.gradio-container h1::before {
  content: ''; display: inline-block; width: 9px; height: 9px;
  border-radius: 50%; background: var(--twin-gold);
  margin-right: 12px; vertical-align: middle;
  box-shadow: 0 0 0 5px rgba(236,173,10,.10);
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  max-width: 100% !important; min-width: 0 !important;
}
.gradio-container .block, .gradio-container .form {
  box-shadow: none !important;
}
/* Conversation surface */
.gradio-container .chatbot,
.gradio-container .chatbot.block {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 20px !important;
  min-height: 460px !important;
  box-shadow: var(--twin-shadow) !important;
  overflow: hidden;
}
.gradio-container .chatbot > .block-label,
.gradio-container .chatbot > label,
.gradio-container .chatbot .label-wrap,
.gradio-container .chatbot .block-label,
.gradio-container .chatbot > .label-container { display: none !important; }
.gradio-container .chatbot .placeholder,
.gradio-container .chatbot .placeholder * { color: var(--twin-muted) !important; }
/* Message styling: keep markdown, code and links intact */
.gradio-container .message-row,
.gradio-container .message-wrap,
.gradio-container .bubble-wrap {
  background: transparent !important;
  box-shadow: none !important;
}
.gradio-container .message-row .message,
.gradio-container .message-row .message-bubble,
.gradio-container .message-row .bubble {
  font-size: 14px !important;
  line-height: 1.65 !important;
  padding: 12px 16px !important;
  border-radius: 16px !important;
  box-shadow: none !important;
  max-width: 100%;
}
.gradio-container .message-row.user-row .message,
.gradio-container .message-row.user-row .message-bubble,
.gradio-container .message-row.user-row .bubble,
.gradio-container .message-row[data-role="user"] .message,
.gradio-container .message-row[data-role="user"] .message-bubble {
  background: #246b9a !important;
  color: #fff !important;
  border: 1px solid #367da9 !important;
  border-bottom-right-radius: 5px !important;
}
.gradio-container .message-row.bot-row .message,
.gradio-container .message-row.bot-row .message-bubble,
.gradio-container .message-row.bot-row .bubble,
.gradio-container .message-row[data-role="assistant"] .message,
.gradio-container .message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  color: var(--twin-text) !important;
  border: 1px solid var(--twin-border) !important;
  border-bottom-left-radius: 5px !important;
}
.gradio-container .message-row .prose p,
.gradio-container .message-row .message p,
.gradio-container .message-row .message-bubble p {
  font-size: 14px !important;
  line-height: 1.65 !important;
  margin: 0 0 10px !important;
  color: inherit !important;
}
.gradio-container .message-row .prose p:last-child,
.gradio-container .message-row .message p:last-child,
.gradio-container .message-row .message-bubble p:last-child { margin-bottom: 0 !important; }
.gradio-container .message-row a { color: var(--twin-blue) !important; text-underline-offset: 3px; }
.gradio-container .message-row.user-row a,
.gradio-container .message-row[data-role="user"] a { color: #fff !important; }
.gradio-container .message-row pre {
  overflow-x: auto; border-radius: 10px; padding: 12px;
}
/* Composer */
.gradio-container textarea,
.gradio-container input[type="text"] {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 14px !important;
  color: var(--twin-text) !important;
  font: 14px/1.5 Inter, ui-sans-serif, system-ui, sans-serif !important;
  padding: 13px 15px !important;
  min-height: 50px !important;
  transition: border-color .2s ease, box-shadow .2s ease;
}
.gradio-container textarea:focus,
.gradio-container input[type="text"]:focus {
  border-color: var(--twin-blue) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(32,157,215,.15) !important;
}
.gradio-container textarea::placeholder,
.gradio-container input::placeholder { color: var(--twin-muted) !important; }
/* Buttons */
.gradio-container button {
  border-radius: 12px !important;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  transition: background .18s ease, border-color .18s ease, transform .18s ease !important;
}
.gradio-container button:hover { transform: translateY(-1px); }
.gradio-container button.primary,
.gradio-container button[variant="primary"],
.gradio-container button.submit,
.gradio-container button.submit-button {
  background: var(--twin-gold) !important;
  color: #131820 !important;
  border: 1px solid var(--twin-gold) !important;
  min-height: 48px !important;
}
.gradio-container button.primary:hover,
.gradio-container button.submit:hover { background: #ffc329 !important; }
.gradio-container .icon-button,
.gradio-container .chatbot .icon-button {
  min-height: 0 !important;
  padding: 5px !important;
  background: transparent !important;
  border: 0 !important;
  color: var(--twin-muted) !important;
  transform: none !important;
}
/* Suggestions */
.gradio-container .examples,
.gradio-container .examples-holder,
.gradio-container [data-testid="examples"] {
  background: transparent !important;
  margin-top: 16px !important;
  padding: 0 !important;
}
.gradio-container .examples table,
.gradio-container .examples-table { border: 0 !important; background: transparent !important; }
.gradio-container .examples button,
.gradio-container .example,
.gradio-container .examples td button,
.gradio-container [data-testid="examples"] button {
  display: inline-block !important;
  background: var(--twin-surface) !important;
  color: var(--twin-text) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 12px !important;
  padding: 12px 15px !important;
  font-weight: 500 !important;
  text-align: left !important;
  min-height: 0 !important;
  box-shadow: 0 3px 12px rgba(0,0,0,.03);
}
.gradio-container .examples button:hover,
.gradio-container .example:hover,
.gradio-container [data-testid="examples"] button:hover {
  border-color: var(--twin-blue) !important;
  background: var(--twin-surface-2) !important;
}
/* Scrollbars and accessibility */
.gradio-container ::-webkit-scrollbar { width: 8px; height: 8px; }
.gradio-container ::-webkit-scrollbar-thumb { background: var(--twin-border); border-radius: 8px; }
.gradio-container :focus-visible { outline: 2px solid var(--twin-blue); outline-offset: 2px; }
@media (max-width: 640px) {
  .gradio-container { padding: 20px 12px 32px !important; }
  .gradio-container .chatbot { min-height: 390px !important; border-radius: 14px !important; }
  .gradio-container .message-row .message,
  .gradio-container .message-row .message-bubble,
  .gradio-container .message-row .bubble { padding: 10px 12px !important; }
}
@media (prefers-reduced-motion: reduce) {
  .gradio-container *, .gradio-container *::before, .gradio-container *::after {
    transition-duration: .01ms !important; animation-duration: .01ms !important;
  }
}
"""

JS = """
() => {
  document.title = 'Digital Twin | AI Portfolio Assistant';
  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };
  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  scan();
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""

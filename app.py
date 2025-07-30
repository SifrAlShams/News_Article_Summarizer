import streamlit as st
import requests
from urllib.parse import urlparse
from datetime import datetime

# ---------- Page & basic styling ----------
st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="centered",
)

CUSTOM_CSS = """
<style>
/* Tighter top spacing */
.block-container { padding-top: 2rem; }

/* Title gradient */
h1 .title-gradient {
  background: linear-gradient(90deg, #4f46e5, #06b6d4 45%, #10b981);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}

/* Chips */
.chips { margin-top: .25rem; }
.chip {
  display:inline-block; padding: 4px 10px; margin: 2px 6px 2px 0;
  border-radius: 999px; font-size: 0.85rem;
  border: 1px solid rgba(0,0,0,.08);
}

/* Card */
.card {
  padding: 1rem 1.25rem; border-radius: 14px;
  border: 1px solid rgba(0,0,0,.06);
  box-shadow: 0 4px 18px rgba(0,0,0,.06);
  background: rgba(255,255,255,.65);
}
[data-theme="dark"] .card {
  background: rgba(33,33,33,.35);
  border-color: rgba(255,255,255,.08);
}

/* Monospace URL */
.url {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .9rem; opacity: .85;
  word-break: break-all;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------- Config ----------
DEFAULT_API_BASE_URL = "http://localhost:8000/"
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {url, summary, ts}

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    API_BASE_URL = st.text_input("API Base URL", value=DEFAULT_API_BASE_URL)
    st.divider()
    st.subheader("🧪 Examples")
    examples = [
        "https://www.bbc.com/news",
        "https://edition.cnn.com/",
        "https://www.dawn.com/",
        "https://medium.com/some-article",
        "https://blog.langchain.dev/some-post"
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.prefill_url = ex

# Header
st.markdown(
    "<h1>AI News <span class='title-gradient'>Summarizer</span></h1>",
    unsafe_allow_html=True,
)
st.caption("Summarize articles from: DAWN, The News, Express Tribune, Radio Pakistan, BBC, CNN, Medium, LangChain (and more).")

st.markdown(
    """
<div class="chips">
  <span class="chip">DAWN</span>
  <span class="chip">The News</span>
  <span class="chip">Express Tribune</span>
  <span class="chip">Radio Pakistan</span>
  <span class="chip">BBC</span>
  <span class="chip">CNN</span>
  <span class="chip">Medium</span>
  <span class="chip">LangChain</span>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Helpers ----------
def is_valid_url(u: str) -> bool:
    try:
        p = urlparse(u.strip())
        return p.scheme in {"http", "https"} and bool(p.netloc)
    except Exception:
        return False

def save_to_history(url: str, summary: str):
    st.session_state.history.insert(0, {
        "url": url,
        "summary": summary,
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    # Keep only last 8
    st.session_state.history = st.session_state.history[:8]

# ---------- Form ----------
with st.form("summarize_form", clear_on_submit=False):
    url_prefill = st.session_state.get("prefill_url", "")
    url = st.text_input(
        "Article URL",
        value=url_prefill,
        placeholder="https://www.example.com/news/article-123",
    )

    colA, colB, colC = st.columns([1.3, 1, 1])
    output_style = colA.selectbox("Output style", ["Bulleted", "Paragraph"], index=0)
    show_url_in_card = colB.checkbox("Show URL", value=True)
    wrap_in_expander = colC.checkbox("Compact view", value=False)

    submit = st.form_submit_button("Summarize", use_container_width=True)

# Clear the prefill once shown
if "prefill_url" in st.session_state:
    del st.session_state["prefill_url"]

# ---------- Action ----------
if submit:
    if not url or not is_valid_url(url):
        st.error("Please enter a valid URL (must start with http:// or https://).")
    else:
        with st.status("Sending to summarizer...", expanded=False) as status:
            try:
                resp = requests.post(
                    f"{API_BASE_URL.rstrip('/')}/summarize/",
                    json={"url": url},
                    timeout=60
                )
                if resp.status_code == 200:
                    summary = resp.json().get("summary", "").strip()
                    if not summary:
                        st.warning("The API returned no summary text.")
                    else:
                        # Optional formatting tweak
                        if output_style == "Bulleted" and "\n" not in summary:
                            # If single paragraph returned, make simple bullets by splitting sentences.
                            parts = [p.strip() for p in summary.replace("•", "").split(". ") if p.strip()]
                            summary = "\n".join([f"- {p.rstrip('.')}" for p in parts])

                        status.update(label="Done", state="complete")
                        # Card display
                        card_md = "<div class='card'>"
                        if show_url_in_card:
                            card_md += f"<div class='url'>{url}</div><br/>"
                        card_md += f"<div><strong>Summary</strong></div>"
                        card_md += "</div>"
                        st.markdown(card_md, unsafe_allow_html=True)

                        if wrap_in_expander:
                            with st.expander("Show summary"):
                                st.markdown(summary)
                        else:
                            st.markdown(summary)

                        # Download
                        st.download_button(
                            "Download summary (.txt)",
                            data=summary,
                            file_name="summary.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )

                        save_to_history(url, summary)
                        st.toast("Summary added to history.")
                else:
                    status.update(label="API error", state="error")
                    st.error(f"Request failed (status {resp.status_code}). Try again or check the API.")
            except requests.exceptions.RequestException as e:
                status.update(label="Connection error", state="error")
                st.error(f"Could not reach the API: {e}")

# ---------- History ----------
if st.session_state.history:
    st.subheader("🕘 Recent summaries")
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"{item['ts']} — {item['url']}", expanded=False):
            st.markdown(item["summary"])
            st.download_button(
                "Download",
                data=item["summary"],
                file_name=f"summary_{i+1}.txt",
                mime="text/plain",
                key=f"dl_{i}",
            )

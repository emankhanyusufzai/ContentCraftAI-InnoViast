# app.py
# ContentCraft AI - Main Streamlit Application
# Your AI-Powered Content Writing Studio

import time
import json
import streamlit as st
from utils.templates import (
    get_template_names,
    get_template_info,
    build_prompt,
    TONES,
    LENGTHS,
    AUDIENCES,
    OUTPUT_FORMATS,
    LANGUAGES,
)
from utils.content_generator import generate_content
from utils.error_handler import validate_input
from utils.exporters import generate_pdf_bytes

# ---------------------------------------------------------
# CONFIG — update this with your actual repo link
# ---------------------------------------------------------
GITHUB_REPO_URL = "https://github.com/emankhanyusufzai/ContentCraftAI-InnoViast"

st.set_page_config(
    page_title="ContentCraft AI",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
defaults = {
    "theme": "dark",
    "view": "gallery",
    "selected_template": get_template_names()[0],
    "generated_content": "",
    "edited_content": "",
    "history": [],
    "last_params": None,  # stores (topic, tone, length, audience, format, lang, seo) for Regenerate
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"


def render_html(html: str):
    """
    Renders an HTML block safely.
    Streamlit's markdown parser treats any line indented by 4+ spaces as a
    code block, which caused raw HTML to appear as visible text. Stripping
    leading whitespace from every line (while keeping the tags themselves
    intact) prevents that misinterpretation.
    """
    cleaned = "\n".join(line.strip() for line in html.strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def open_generator(template_name):
    st.session_state.selected_template = template_name
    st.session_state.view = "generator"
    st.session_state.generated_content = ""
    st.session_state.edited_content = ""


def back_to_gallery():
    st.session_state.view = "gallery"


def load_history_item(item):
    st.session_state.selected_template = item["template"]
    st.session_state.view = "generator"
    st.session_state.generated_content = item["content"]
    st.session_state.edited_content = item["content"]


def run_generation(template_name, topic, tone, length, audience, output_format, language, include_seo, animate=True):
    """Shared generation logic used by both Generate and Regenerate."""
    with st.spinner("Crafting your content..."):
        success, result = generate_content(
            template_name, topic, tone, length, audience, output_format,
            language=language, include_seo=include_seo,
        )

    if not success:
        st.error(result)
        return

    if animate:
        placeholder = st.empty()
        displayed = ""
        step = max(1, len(result) // 150)
        for i in range(0, len(result), step):
            displayed = result[: i + step]
            placeholder.markdown(
                f"<div class='cc-result'>{displayed}▌</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.008)

    st.session_state.generated_content = result
    st.session_state.edited_content = result
    st.session_state.last_params = {
        "topic": topic, "tone": tone, "length": length, "audience": audience,
        "output_format": output_format, "language": language, "include_seo": include_seo,
    }
    st.session_state.history.append({"template": template_name, "topic": topic, "content": result})
    st.rerun()


# ---------------------------------------------------------
# THEME PALETTE
# ---------------------------------------------------------
if st.session_state.theme == "dark":
    bg = "#0b0c14"
    surface = "#151621"
    surface_alt = "#1d1e2c"
    border = "#292a3d"
    text = "#eceaf5"
    subtext = "#8c8ba3"
else:
    bg = "#f4f4fa"
    surface = "#ffffff"
    surface_alt = "#eceaf7"
    border = "#e2e1f0"
    text = "#181828"
    subtext = "#6b6a80"

grad = "linear-gradient(120deg, #3b5bfd 0%, #8b3ef0 100%)"
grad_soft = "linear-gradient(120deg, rgba(59,91,253,0.15) 0%, rgba(139,62,240,0.15) 100%)"

ACCENTS = {
    "Blog Post": "#3b82f6",
    "Social Media Caption": "#f472b6",
    "Ad Copy": "#f59e0b",
    "Email": "#22c55e",
    "Product Description": "#a855f7",
    "LinkedIn Post": "#06b6d4",
}

POPULAR = {"Blog Post", "Social Media Caption"}

# Original abstract SVG logo — brain + pen-nib fusion, not a stock emoji/icon
LOGO_SVG = (
    '<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="ccGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
    '<stop offset="0%" stop-color="#3b5bfd"/>'
    '<stop offset="100%" stop-color="#8b3ef0"/>'
    '</linearGradient></defs>'
    '<rect width="40" height="40" rx="11" fill="url(#ccGrad)"/>'
    '<path d="M12 26 L20 10 L20 18 L28 14 L20 30 L20 22 Z" fill="white" opacity="0.95"/>'
    '<circle cx="12" cy="26" r="2" fill="white"/>'
    '<circle cx="28" cy="14" r="2" fill="white"/>'
    '</svg>'
)

# ---------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------
render_html(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            overflow-x: hidden !important;
        }}

        .stApp {{
            background-color: {bg};
            color: {text};
            overflow-x: hidden;
        }}

        #MainMenu, header, footer {{visibility: hidden;}}

        .cc-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .cc-brand-name {{
            font-family: 'Poppins', sans-serif;
            font-size: 19px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }}

        .cc-brand-tag {{
            font-size: 11px;
            color: {subtext};
            margin-top: -2px;
        }}

        .cc-hero {{
            padding: 28px 32px;
            border-radius: 20px;
            background: {surface};
            border: 1px solid {border};
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }}

        .cc-hero::before {{
            content: "";
            position: absolute;
            top: -60px;
            right: -60px;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: {grad_soft};
            animation: ccPulse 6s ease-in-out infinite;
        }}

        @keyframes ccPulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.15); opacity: 1; }}
        }}

        .cc-hero h1 {{
            font-family: 'Poppins', sans-serif;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 6px 0;
            position: relative;
        }}

        .cc-hero h1 a, a.anchor-link {{
            display: none !important;
        }}

        .cc-hero p {{
            color: {subtext};
            margin: 0;
            font-size: 14px;
            position: relative;
        }}

        .cc-hero-stats {{
            display: flex;
            gap: 18px;
            margin-top: 14px;
            position: relative;
            flex-wrap: wrap;
        }}

        .cc-hero-stat {{
            font-size: 11.5px;
            color: {subtext};
            background: {surface_alt};
            border: 1px solid {border};
            padding: 4px 12px;
            border-radius: 20px;
        }}

        .cc-card {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 22px 20px 18px 20px;
            height: 100%;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }}

        .cc-card:hover {{
            transform: translateY(-6px);
            box-shadow: 0 12px 30px rgba(59,91,253,0.18);
            border-color: #8b3ef0;
        }}

        .cc-popular-badge {{
            position: absolute;
            top: 16px;
            right: 16px;
            background: {grad};
            color: white;
            font-size: 10px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            letter-spacing: 0.3px;
        }}

        .cc-icon-box {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-bottom: 14px;
        }}

        .cc-card-title {{
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .cc-card-desc {{
            font-size: 12.5px;
            color: {subtext};
            margin-bottom: 14px;
            line-height: 1.4;
            min-height: 34px;
        }}

        div.stButton > button {{
            background: {grad};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 8px 18px;
            font-weight: 600;
            font-size: 13px;
            width: 100%;
        }}

        div.stButton > button:hover {{
            filter: brightness(1.08);
        }}

        .cc-ghost-btn button {{
            background: {surface_alt} !important;
            color: {text} !important;
            border: 1px solid {border} !important;
        }}

        .cc-panel {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 22px;
        }}

        .cc-result {{
            background: {surface_alt};
            border: 1px solid {border};
            border-radius: 14px;
            padding: 22px;
            white-space: pre-wrap;
            line-height: 1.65;
            font-size: 14.5px;
        }}

        .cc-pill {{
            display: inline-block;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: white;
        }}

        .cc-stats-row {{
            display: flex;
            gap: 22px;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid {border};
            flex-wrap: wrap;
        }}

        .cc-stat {{
            font-size: 12.5px;
            color: {subtext};
        }}

        .cc-stat b {{
            color: {text};
            font-size: 14px;
            display: block;
        }}

        .cc-empty-state {{
            text-align: center;
            padding: 50px 20px;
            color: {subtext};
        }}

        .cc-empty-state .cc-empty-icon {{
            font-size: 40px;
            margin-bottom: 10px;
        }}

        .cc-footer {{
            text-align: center;
            padding: 30px 0 10px 0;
            color: {subtext};
            font-size: 12.5px;
            border-top: 1px solid {border};
            margin-top: 36px;
        }}

        .cc-history-item {{
            background: {surface_alt};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 8px;
        }}

        .cc-history-title {{
            font-weight: 600;
            font-size: 13.5px;
        }}

        .cc-history-sub {{
            font-size: 11.5px;
            color: {subtext};
        }}

        .cc-counter-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: -8px;
            margin-bottom: 12px;
        }}

        .cc-counter-text {{
            font-size: 12px;
        }}

        /* ---------- RESPONSIVE BREAKPOINTS ---------- */
        @media (max-width: 1024px) {{
            div[data-testid="column"] {{
                width: 50% !important;
                flex: 1 1 50% !important;
                min-width: 50% !important;
            }}
        }}

        @media (max-width: 768px) {{
            .cc-hero {{ padding: 20px 18px; }}
            .cc-hero h1 {{ font-size: 21px; }}
            .cc-hero p {{ font-size: 13px; }}
            .cc-panel {{ padding: 16px; }}
            div.stButton > button {{ width: 100%; padding: 10px 14px; }}
        }}

        @media (max-width: 425px) {{
            div[data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }}
            .cc-brand-name {{ font-size: 15px; }}
            .cc-brand-tag {{ font-size: 10px; }}
            .cc-hero h1 {{ font-size: 18px; }}
            .cc-card {{ padding: 16px 14px; }}
        }}

        @media (max-width: 375px), (max-width: 320px) {{
            .cc-hero {{ padding: 16px 14px; }}
            .cc-hero h1 {{ font-size: 16px; }}
            .cc-hero p {{ font-size: 12px; }}
        }}
    </style>
    """
)

# ---------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------
top_left, top_right = st.columns([5, 1.6])
with top_left:
    render_html(
        f"""
        <div class="cc-brand">
            {LOGO_SVG}
            <div>
                <div class="cc-brand-name">ContentCraft AI</div>
                <div class="cc-brand-tag">Your AI-Powered Content Writing Studio</div>
            </div>
        </div>
        """
    )
with top_right:
    theme_icon = "☀️ Light" if st.session_state.theme == "dark" else "🌙 Dark"
    icon_col1, icon_col2 = st.columns([1, 1.5])
    with icon_col1:
        st.link_button("🔗 GitHub", GITHUB_REPO_URL, use_container_width=True)
    with icon_col2:
        st.markdown('<div class="cc-ghost-btn">', unsafe_allow_html=True)
        st.button(theme_icon, on_click=toggle_theme, key="theme_btn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================
# VIEW: GALLERY
# ===========================================================
if st.session_state.view == "gallery":

    render_html(
        f"""
        <div class="cc-hero">
            <h1>Create High-Quality AI Content in Seconds</h1>
            <p>Generate blogs, LinkedIn posts, emails, captions, ads and product descriptions using AI.</p>
            <div class="cc-hero-stats">
                <span class="cc-hero-stat">✨ 6 Templates</span>
                <span class="cc-hero-stat">🌐 2 Languages</span>
                <span class="cc-hero-stat">♾️ Unlimited Generations</span>
            </div>
        </div>
        """
    )

    names = get_template_names()
    cols = st.columns(3)

    for i, name in enumerate(names):
        info = get_template_info(name)
        accent = ACCENTS.get(name, "#3b5bfd")
        badge_html = '<div class="cc-popular-badge">POPULAR</div>' if name in POPULAR else ""
        with cols[i % 3]:
            render_html(
                f"""
                <div class="cc-card">
                    {badge_html}
                    <div class="cc-icon-box" style="background:{accent}22; color:{accent};">
                        {info['icon']}
                    </div>
                    <div class="cc-card-title">{name}</div>
                    <div class="cc-card-desc">{info['description']}</div>
                </div>
                """
            )
            st.button(
                "🚀 Start Writing",
                key=f"create_{name}",
                on_click=open_generator,
                args=(name,),
                use_container_width=True,
            )
            st.write("")

    # History section — clickable to reload past content
    if st.session_state.history:
        with st.expander(f"🕘 History ({len(st.session_state.history)})"):
            for idx, item in enumerate(reversed(st.session_state.history[-10:])):
                hcol1, hcol2 = st.columns([4, 1])
                with hcol1:
                    render_html(
                        f"""
                        <div class="cc-history-item">
                            <div class="cc-history-title">{item['template']}</div>
                            <div class="cc-history-sub">{item['topic'][:80]}</div>
                        </div>
                        """
                    )
                with hcol2:
                    st.button(
                        "View →",
                        key=f"hist_{idx}",
                        on_click=load_history_item,
                        args=(item,),
                        use_container_width=True,
                    )

    render_html(
        """
        <div class="cc-footer">
            © 2026 ContentCraft AI · Built with Streamlit + Google Gemini
        </div>
        """
    )

# ===========================================================
# VIEW: GENERATOR
# ===========================================================
else:
    selected = st.session_state.selected_template
    info = get_template_info(selected)
    accent = ACCENTS.get(selected, "#3b5bfd")

    st.markdown('<div class="cc-ghost-btn">', unsafe_allow_html=True)
    st.button("← Back to templates", on_click=back_to_gallery, key="back_btn")
    st.markdown("</div>", unsafe_allow_html=True)

    render_html(
        f"""
        <div class="cc-hero">
            <span class="cc-pill" style="background:{accent};">{info['icon']} {selected}</span>
            <h1 style="margin-top:14px;">{selected}</h1>
            <p>{info['description']}</p>
        </div>
        """
    )

    col_main, col_settings = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="cc-panel">', unsafe_allow_html=True)
        st.markdown("**What's it about?**")
        topic = st.text_area(
            "Topic",
            placeholder=info["placeholder"],
            height=130,
            label_visibility="collapsed",
            max_chars=500,
            key=f"topic_input_{selected}",
        )

        # Real-time word/character counter with color-coded limit warning
        char_count = len(topic)
        word_count = len(topic.split()) if topic.strip() else 0
        pct = char_count / 500
        bar_color = "#22c55e" if pct < 0.7 else ("#f59e0b" if pct < 0.9 else "#ef4444")

        render_html(
            f"""
            <div class="cc-counter-row">
                <span class="cc-counter-text" style="color:{subtext};">{word_count} words</span>
                <span class="cc-counter-text" style="color:{bar_color}; font-weight:600;">{char_count}/500 characters</span>
            </div>
            """
        )

        generate_clicked = st.button("✨ Generate")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_settings:
        st.markdown('<div class="cc-panel">', unsafe_allow_html=True)
        st.markdown("**Customize**")
        tone = st.selectbox("Tone", TONES)
        length = st.selectbox("Length", LENGTHS, index=1)
        audience = st.selectbox("Audience", AUDIENCES)
        output_format = st.selectbox("Format", OUTPUT_FORMATS)
        language = st.selectbox("🌐 Language", LANGUAGES)
        include_seo = st.checkbox("🏷️ Include SEO Keywords")
        st.markdown("</div>", unsafe_allow_html=True)

        # Prompt Preview — shows mentor exactly what's sent to Gemini
        with st.expander("🔍 Prompt Strategy (for mentor review)"):
            preview_prompt = build_prompt(
                selected,
                topic if topic else info["placeholder"],
                tone, length, audience, output_format,
                language=language, include_seo=include_seo,
            )
            st.code(preview_prompt, language="text")

    # -------------------------------------------------------
    # GENERATE
    # -------------------------------------------------------
    if generate_clicked:
        is_valid, error_msg = validate_input(topic)
        if not is_valid:
            st.warning(error_msg)
        else:
            run_generation(selected, topic, tone, length, audience, output_format, language, include_seo)

    # -------------------------------------------------------
    # RESULT DISPLAY — editable, with regenerate + exports
    # -------------------------------------------------------
    if st.session_state.generated_content:
        content = st.session_state.generated_content

        st.write("")
        result_col, regen_col = st.columns([4, 1])
        with result_col:
            st.markdown("**📄 Result** — edit freely before downloading")
        with regen_col:
            regen_clicked = st.button("🔄 Regenerate", use_container_width=True)

        if regen_clicked and st.session_state.last_params:
            p = st.session_state.last_params
            run_generation(
                selected, p["topic"], p["tone"], p["length"], p["audience"],
                p["output_format"], p["language"], p["include_seo"], animate=True,
            )

        edited = st.text_area(
            "Edit content",
            value=st.session_state.edited_content or content,
            height=260,
            label_visibility="collapsed",
            key="editable_result",
        )
        st.session_state.edited_content = edited

        words = len(edited.split())
        chars = len(edited)
        reading_time = max(1, round(words / 200))

        render_html(
            f"""
            <div class="cc-stats-row">
                <div class="cc-stat"><b>{words}</b>Words</div>
                <div class="cc-stat"><b>{chars}</b>Characters</div>
                <div class="cc-stat"><b>{reading_time} min</b>Reading time</div>
            </div>
            """
        )

        st.write("")

        copy_col, dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 1, 1])

        with copy_col:
            safe_content = json.dumps(edited)
            st.components.v1.html(
                f"""
                <button id="copyBtn" style="width:100%; padding:8px 14px; border-radius:10px; border:none;
                    background:linear-gradient(120deg,#3b5bfd,#8b3ef0); color:white;
                    font-weight:600; font-size:13px; cursor:pointer; font-family:Inter,sans-serif;">
                    📋 Copy
                </button>
                <script>
                const textToCopy = {safe_content};
                document.getElementById('copyBtn').addEventListener('click', function() {{
                    navigator.clipboard.writeText(textToCopy);
                    this.innerText = '✅ Copied!';
                    setTimeout(() => this.innerText = '📋 Copy', 1500);
                }});
                </script>
                """,
                height=42,
            )

        with dl_col1:
            st.download_button(
                "⬇️ .txt",
                data=edited,
                file_name=f"{selected.replace(' ', '_').lower()}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with dl_col2:
            md_content = f"# {selected}\n\n{edited}"
            st.download_button(
                "⬇️ .md",
                data=md_content,
                file_name=f"{selected.replace(' ', '_').lower()}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with dl_col3:
            try:
                pdf_bytes = generate_pdf_bytes(selected, edited)
                st.download_button(
                    "⬇️ .pdf",
                    data=pdf_bytes,
                    file_name=f"{selected.replace(' ', '_').lower()}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except ModuleNotFoundError:
                st.caption("PDF export unavailable — run: pip install fpdf2")
            except Exception as e:
                st.caption(f"⚠️ PDF error: {type(e).__name__}: {e}")

    else:
        render_html(
            """
            <div class="cc-empty-state">
                <div class="cc-empty-icon">✨</div>
                <div>Generate your first content to see it here.</div>
            </div>
            """
        )

    render_html(
        """
        <div class="cc-footer">
            © 2026 ContentCraft AI · Built with Streamlit + Google Gemini
        </div>
        """
    )
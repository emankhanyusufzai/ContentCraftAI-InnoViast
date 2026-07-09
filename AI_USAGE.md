# AI_USAGE.md

This document records how AI tools were used during the development of **ContentCraft AI**, as required by the InnoViast Assignment 2 guidelines.

---

## AI Tools Used

- **Claude (Anthropic)** — used for architecture planning, writing Python/Streamlit code, debugging runtime errors, and fixing UI rendering issues.
- **Google Gemini API (`gemini-2.5-flash`)** — the core AI model powering the app itself (content generation for all 6 templates).

---

## How AI Was Used

### 1. Project Scaffolding
Asked Claude to design the folder structure and initial file breakdown (`app.py`, `utils/content_generator.py`, `utils/templates.py`, `utils/error_handler.py`) based on the assignment's required scope: 6 content templates with tone/length/audience/format controls.

### 2. UI Design
Requested an **original** premium SaaS-style interface — explicitly instructed the AI *not* to copy any reference UI, but to use it only as inspiration. Specified requirements: dark theme by default with a light toggle, a custom AI Brain + Pen Nib logo (SVG, not a stock icon), and a blue-to-purple gradient as the primary accent. Later iterations added an animated gradient hero, hover-lift card effects, and "Popular" badges to make the interface feel less static.

### 3. Gemini API Integration
Had Claude write `content_generator.py` to connect to the Gemini API, build prompts from user inputs (topic, tone, length, audience, format), and return generated text with error handling.

### 4. Prompt Strategy Iteration
The prompt sent to Gemini is dynamically built in `templates.py` from seven variables (template type, topic, tone, length, audience, format, language) plus an optional SEO-keywords instruction — rather than being a single static string. This was an iteration on an early version that used one fixed prompt per template — the parameterized version was chosen so every control actually changes the output instead of just the UI state. A **"Prompt Strategy" expander** was added to the generator page so the exact prompt sent to Gemini is visible for review at any time.

### 5. Feature Expansion (second development pass)
After the core generator was working, Claude was used to add a second layer of functionality on top of the base app:
- **Regenerate button** — reruns generation with the last-used settings without re-entering the topic.
- **Editable output** — the AI result is shown in an editable text area, so downloads/copy reflect the user's edits, not just the raw AI output.
- **History with reload** — the last 10 generations are stored in session state, each with a "View →" button that reloads that content back into the generator.
- **Language selector** — English / Roman Urdu, implemented by adding a language instruction to the prompt builder.
- **Optional SEO Keywords** — a checkbox that appends an instruction asking Gemini to include a keywords section at the end of the output.
- **Real-time word/character counter** with a color-coded (green → orange → red) limit warning as the user approaches the 500-character cap.
- **Multi-format export** — Copy to clipboard (via JavaScript), and download as `.txt`, `.md`, and `.pdf`.

### 6. Debugging (major iteration cycles)

- **Bug: Raw HTML rendering as visible text.**
  Custom HTML (logo, headers, cards) was rendering as literal text instead of formatted HTML.
  **Diagnosis:** Streamlit's Markdown parser interprets any line indented 4+ spaces as a code block. `textwrap.dedent()` only strips *common* leading whitespace, so nested `<div>` tags still had leftover indentation that triggered this behavior.
  **Fix:** Added a `render_html()` helper that strips *all* leading whitespace from every line before rendering, used consistently across the app.

- **Bug: Generic "Something went wrong" on every generation attempt.**
  **Diagnosis:** Traced the real exception in the terminal — Gemini's `gemini-1.5-flash` model had been fully deprecated/shut down (all Gemini 1.0/1.5 models return 404 as of mid-2026), and the broad `except Exception` handler was masking the real cause behind one generic message.
  **Fix:** Updated the model to `gemini-2.5-flash`, and later made the error handler surface the actual exception type/message during debugging rather than always showing the same static caption.

- **Bug: `google.generativeai` package fully deprecated.**
  The terminal began showing a deprecation notice: all support for the `google-generativeai` package had ended, in favor of the unified `google-genai` SDK.
  **Fix:** Migrated `content_generator.py` from the old `genai.GenerativeModel(...)` pattern to the new client-based `genai.Client()` / `client.models.generate_content(...)` API, and updated `requirements.txt` accordingly.

- **Bug: Copy-to-clipboard button rendered as raw HTML/JS text.**
  **Diagnosis:** The `onclick="..."` attribute was double-quoted, and the JSON-encoded content (`json.dumps`) also starts with a double quote — the browser parsed the attribute as ending early, breaking the tag.
  **Fix:** Rewrote the component to attach the click handler via `addEventListener` inside a `<script>` tag instead of inline `onclick`, so the JSON string never collides with an HTML attribute boundary.

- **Bug: PDF export failing with `FPDFException: Not enough horizontal space to render a single character`.**
  **Diagnosis:** Isolated the failure locally by reproducing the exact PDF generation call outside Streamlit and printing the cursor's x/y position before each `multi_cell()` call. This showed that `fpdf2` sometimes leaves the text cursor at the right edge of the page after a call instead of resetting it to the left margin — so the *next* line had almost no horizontal space left to render into. A separate, smaller bug was that calling `multi_cell()` with an empty string (for blank lines between paragraphs) also raised the same exception.
  **Fix:** Passed explicit `new_x=XPos.LMARGIN, new_y=YPos.NEXT` to every `multi_cell()` call to force the cursor back to the left margin on a new line, and replaced blank-line handling with `pdf.ln()` instead of calling `multi_cell()` on an empty string.

### 7. Deployment Support
Used Claude to walk through Git/GitHub setup, `.gitignore` configuration (excluding `.env` and `__pycache__`), resolving a GitHub push-protection block after `.env` was accidentally committed once (fixed via `git rm --cached .env` and `git commit --amend`), and Streamlit Community Cloud deployment — including rebooting the deployed app after dependency changes so the new `google-genai` package and PDF fixes took effect in production.

### 8. Documentation
Used Claude to draft `README.md` and this `AI_USAGE.md` file, based on the actual features and fixes implemented during development, and to keep both updated as new features were added in later iterations.

---

## What Was Not AI-Generated
- The actual topics/content typed into the app during testing (e.g. "Benefits of Artificial Intelligence for Students") were provided by the developer, not the AI.
- Final review, testing, and verification of every fix (screenshots, manual testing of Copy/Download/History/Regenerate/Error handling, and live testing on the deployed Streamlit Cloud app) were performed manually by the developer before accepting any change.

---

## Reflection
AI tools significantly sped up scaffolding, feature iteration, and debugging — especially diagnosing the Streamlit-specific HTML/Markdown rendering issue, the Gemini model/SDK deprecation, and the `fpdf2` cursor-positioning bug, all of which required tracing the actual runtime error rather than guessing. Every suggested fix was tested locally (and where relevant, in an isolated reproduction script) before being committed, and the developer verified functionality end-to-end — including on the live deployed app after each reboot — rather than accepting code changes blindly.
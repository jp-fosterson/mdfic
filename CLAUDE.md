# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

`mdfic` is a Python CLI toolkit that converts Markdown fiction (with YAML front matter) into manuscript formats: DOCX, LaTeX/PDF, HTML, EPUB. It also generates per-story Makefiles, CSS, .gitignore files, tweet-sized text chunks, and runs AI copyedits via OpenAI. Installed by `pip install mdfic`; the CLI entry point is `mdfic.cli:cli`.

This repo is its own git repository, separate from the parent `writing/` workspace that consumes it.

## Environment

The project is managed by `uv` with a virtualenv at `.venv/`. Do not install into the system Python. Use `uv` for everything:

```bash
uv sync                # install/update deps from uv.lock
uv run mdfic --help    # run the CLI
uv run python -m ...   # run any python
uv pip install -e .    # editable install inside the uv venv
```

There is no test suite, lint config, or formatter wired up — don't invent commands. To smoke-test a change, run the relevant `mdfic` subcommand against a story file (examples live in `../../pub/`).

## Architecture

Single Click CLI (`mdfic/cli.py`) with each subcommand thinly wrapping a module. Imports inside command functions are deliberate — they keep `mdfic --help` fast and avoid loading LangChain/keyring unless `copyedit` is actually invoked.

| Module | Role |
|---|---|
| `cli.py` | Click group `cli` and all subcommands. Lazy-imports per command. |
| `utils.py` | YAML front matter parsing (`split_metadata_and_text`, `parse_metadata`), pandoc subprocess wrapper, AppleScript runner, `int_to_roman`, `get_in` nested-dict lookup. |
| `docx.py` | `HTML2DOCX` — an `HTMLParser` subclass that consumes pandoc's HTML output and emits a `python-docx` document. SFFMS mode rewrites styles (Courier, double-spaced, 1" margins) and injects a custom `word/header*.xml` via direct zip manipulation. |
| `latex.py` | `SFFMSStory` / `ArticleStory` / `BookStory` classes that wrap pandoc-generated LaTeX with the appropriate documentclass header and metadata. |
| `makefile.py` | String templates (`SINGLE_TEMPLATE`, `MULTI_TEMPLATE`) for per-story Makefiles. PDF target swaps between `pdflatex` and `mdfic pages-to-pdf` based on `--latex` flag. |
| `css.py` | Single `CSS` constant used by `mdfic css`. |
| `tweets.py` | Splits text into max-length chunks, preserving paragraph and sentence boundaries. Reused by `copyedit.py` for chunking long manuscripts before sending to the API. |
| `copyedit.py` | LangChain `ChatOpenAI` chain with a fixed copyediting prompt. Module-level init reads `OPENAI_USER` env var and pulls the API key from the system keyring (`api.openai.com`). |

### Story format conventions

- Markdown with optional YAML front matter delimited `---` ... `...` (or `---` ... `---`).
- `---` on its own line inside the body is a scene break (becomes `<hr />` in pandoc HTML, then transformed to `• • •` or numbered scene markers).
- Recognized metadata: `title`, `author`, `address` (list, joined with newlines), `email`, plus `mdfic.number_scenes` (`true` or `'roman'`) and `mdfic.latex.extra_headers` (list of raw LaTeX lines).
- `address` arriving as a YAML list is joined by `parse_metadata` using the caller's `join` separator — this is how multi-line addresses survive into LaTeX/DOCX templates.

### External tool dependencies

Pandoc is required for every format-conversion command (invoked via `utils.pandoc`, which shells out). LaTeX (`pdflatex`) is required only when the generated Makefile uses the latex PDF target. `mdfic pages-to-pdf` is macOS-only — it drives Apple Pages via AppleScript.

## Copyedit gotchas

- `copyedit.py` initializes `ChatOpenAI` at module import time. If `OPENAI_USER` is unset or no key is in the keyring, `OPENAI_API_KEY` becomes `None` and the model object is constructed anyway — failures surface only when the chain is invoked.
- Default model is `gpt-5-mini` (override with `MDFIC_MODEL_NAME`). Default chunk size is 80,000 words (override with `MDFIC_MAX_WORDS`); chunks are computed as `MAX_WORDS * 6` characters via `tweets.generate`.
- The prompt forbids editing dialogue, sanitizing profanity, or changing whitespace, and asks for `[TKTK: ...]` inline suggestions. Preserve these constraints if you touch `editprompt`.
- After editing, `copyedit()` reassembles output as `---\n{metadata}\n...\n\n{story}` — the original metadata block is re-emitted verbatim, not re-parsed.

## Known rough edges

- `cli.gitignore` declares `latex` in its function signature but no corresponding Click option — passing `--multi` works, but the function will `TypeError` if Click ever supplies a `latex` kwarg. Don't "fix" by adding the option without checking callers.
- `pyproject.toml` still uses `setuptools` as the build backend even though dev workflow is `uv`-driven; both coexist intentionally.

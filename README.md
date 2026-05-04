# MDFIC - Markdown Fiction Toolkit

**MDFIC** is a Python toolkit designed specifically for fiction writers who want to work with their manuscripts like code. It transforms Markdown-formatted short stories and novelettes into professional manuscript formats including DOCX, PDF, EPUB, HTML, and LaTeX, following industry-standard formatting guidelines like SFFMS (Standard Format for Fiction Manuscripts).

## Philosophy

MDFIC enables fiction writers to:
- Write stories in clean, distraction-free Markdown
- Manage story projects with Git version control
- Use Makefiles for automated builds and publishing workflows
- Generate multiple output formats from a single source
- Follow professional manuscript formatting standards
- Work with both single-file and multi-part stories

## Key Features

### Professional Manuscript Formatting
- **SFFMS Format**: Industry-standard manuscript format with proper headers, spacing, and typography
- **DOCX Output**: Microsoft Word documents ready for submission to publishers
- **LaTeX/PDF**: High-quality typeset documents using LaTeX
- **HTML/CSS**: Web-ready versions with customizable styling
- **EPUB**: E-book format for digital distribution

### Story Project Management
- **Makefile Generation**: Automated build systems for your story projects
- **Multi-part Stories**: Support for novelettes and longer works split across multiple files
- **Metadata Handling**: YAML front matter for title, author, contact info, and story settings
- **Git Integration**: `.gitignore` generation for clean version control

### Writer-Friendly Tools
- **Word Counting**: Accurate word counts and reading time estimates
- **Progress Tracking**: Git-based progress monitoring since specific dates
- **Copyediting**: Automated copyediting with configurable strength levels
- **Scene Management**: Automatic scene break formatting and numbering
- **Tweet Generation**: Break stories into social media-friendly segments

## Installation

### Install MDFIC

```bash
pip install mdfic
```

### External Dependencies

MDFIC requires several external tools for full functionality:

**Required:**
- **[Pandoc](https://pandoc.org/)**: Universal document converter (required for all format conversions)
  ```bash
  # macOS
  brew install pandoc
  
  # Ubuntu/Debian
  sudo apt-get install pandoc
  
  # Windows: Download from https://pandoc.org/installing.html
  ```

**Optional (for specific features):**
- **LaTeX Distribution**: For PDF generation via LaTeX
  ```bash
  # macOS
  brew install --cask mactex
  
  # Ubuntu/Debian
  sudo apt-get install texlive-full
  
  # Windows: Install MiKTeX or TeX Live
  ```

- **Apple Pages** (macOS only): Alternative PDF generation method
  - Install from Mac App Store
  - Used by `mdfic pages-to-pdf` command

**Note**: Without LaTeX, you can still generate PDFs using the Pages method on macOS, or convert DOCX files to PDF using other tools.

## Quick Start

### 1. Create a New Story Project

```bash
# Generate a Makefile for your story
mdfic makefile --name "my-story" --output Makefile

# Generate a .gitignore file
mdfic gitignore --name "my-story" --output .gitignore
```

### 2. Write Your Story

Create `my-story.md` with YAML metadata:

```markdown
---
title: My Amazing Story
author: Your Name
address: 
  - Your Name
  - Your Address
  - City, State ZIP
  - Phone Number
email: your.email@example.com
---

Your story begins here...

---

Scene breaks are created with horizontal rules.

More story content...
```

### 3. Build Your Manuscripts

```bash
# Build all formats
make

# Or build specific formats
make docx    # Word documents (plain and SFFMS format)
make pdf     # PDF via LaTeX
make html    # HTML with CSS styling
make epub    # E-book format
```

> Note: `make epub` (and `make mobi`) shell out to pandoc directly from the
> generated Makefile; mdfic does not currently produce EPUB through a
> dedicated subcommand.

## Story Project Structure

A typical mdfic story project looks like this:

```
my-story/
├── my-story.md          # Your story in Markdown
├── metadata.yaml        # Story metadata (optional)
├── Makefile            # Build automation
├── .gitignore          # Git ignore rules
└── out/                # Generated output files
    ├── my-story-sffms.docx
    ├── my-story-plain.docx
    ├── my-story-sffms.pdf
    ├── my-story.html
    └── my-story.epub
```

For multi-part stories:
```
my-novelette/
├── my-novelette-part-1.md
├── my-novelette-part-2.md
├── my-novelette-part-3.md
├── my-novelette.md      # Auto-generated from parts
├── metadata.yaml
├── Makefile
└── out/
```

## Command Reference

### Core Commands

**Generate manuscript formats:**
```bash
# DOCX manuscripts (SFFMS or plain)
mdfic docx --sffms --output story.docx story.md

# LaTeX/PDF (requires LaTeX installation)
mdfic latex --documentclass sffms --output story.tex story.md

# HTML with styling
mdfic html --output story.html --css style.css story.md
```

The `docx` command also accepts `--pspaces N` (number of spaces after a
period, default `1`) and `--date / --no-date` (default on — appends a
DRAFT tag and today's date to the title).

**Project setup:**
```bash
# Create Makefile
mdfic makefile --name story-name [--multi] [--latex]

# Create .gitignore
mdfic gitignore --name story-name [--multi]

# Generate CSS for HTML output
mdfic css --output style.css
```

**Writer tools:**
```bash
# Word count and reading time
mdfic wc story.md --wpm 250

# Track writing progress
mdfic progress --since 2024-01-01 story.md

# Copyedit text
mdfic copyedit --strength medium --output edited.md story.md

# Generate tweets from story
mdfic tweet --maxlen 280 --output tweets.txt story.md
```

**Utility commands:**
```bash
# Replace <hr /> in pandoc HTML output with custom scene-break markup
mdfic hrrepl --withtxt "<center>• • •</center>" --output out.html story.html

# Convert legacy 90s-era Mac Word documents to markdown-editable text
mdfic strip-word-doc --output story.md old-mac-word.doc
```

### Copyedit Configuration

The `mdfic copyedit` command runs an AI-assisted copyedit using OpenAI's language models. The strength flag and model are passed through to a single fixed prompt; results vary with the model you choose.

**Prerequisites:**
- OpenAI API account and API key
- Python `keyring` library (installed with mdfic)

**Setup:**
1. Set your OpenAI username in environment:
   ```bash
   export OPENAI_USER="your-openai-email@example.com"
   ```

2. Store your API key in the system keyring:
   ```python
   import keyring
   keyring.set_password("api.openai.com", "your-openai-email@example.com", "your-api-key")
   ```

**Configuration Options:**

| Variable | Purpose | Default |
|---|---|---|
| `OPENAI_USER` | Keyring username used to look up the API key | (required) |
| `MDFIC_MODEL_NAME` | OpenAI model to use | `gpt-5-mini` |
| `MDFIC_MAX_WORDS` | Maximum words per API request chunk | `80000` |

**Strength Levels:**

The `--strength` value is interpolated into the prompt as a hint to the model — there is no per-level branching in the code. Common values are `light`, `medium`, and `heavy`; the model interprets these on its own and the actual edits depend on the model. You can pass any string the model can sensibly act on.

**Model Selection:**

Any chat-completions model your account can access will work. `gpt-5-mini` (the default) is fast and cheap; larger models such as `gpt-4o` or `gpt-4-turbo` typically give more thorough edits at higher cost.

**Processing:**

Large manuscripts are automatically chunked based on `MDFIC_MAX_WORDS` to stay within API context limits. Each chunk is processed separately and reassembled with the original front matter preserved verbatim.

**Usage Examples:**
```bash
# Default copyedit
mdfic copyedit story.md

# Medium strength edit to new file
mdfic copyedit --strength medium --output edited.md story.md

# Heavy edit of multiple chapters
mdfic copyedit --strength heavy chapter*.md > full-edit.md
```

### Advanced Features

**Scene numbering:**
Add to your metadata YAML:
```yaml
mdfic:
  number_scenes: true      # Use numbers (1, 2, 3...)
  # number_scenes: roman   # Use Roman numerals (I, II, III...)
```

**Custom LaTeX headers:**
```yaml
mdfic:
  latex:
    extra_headers:
      - "\\usepackage{custom-package}"
      - "\\newcommand{\\mycommand}{text}"
```

## Manuscript Format Standards

MDFIC follows professional manuscript formatting guidelines:

- **SFFMS Format**: Based on the Science Fiction & Fantasy Manuscripts Standard
- **Proper Typography**: Courier font, double-spacing, 1-inch margins
- **Headers**: Author name, title, and page numbers on each page
- **Word Count**: Rounded to nearest 50 words on title page
- **Scene Breaks**: Render as `• • •` (HTML), a centered rule (LaTeX/SFFMS), or sequential Arabic/Roman numerals when `mdfic.number_scenes` is set in metadata
- **End Marker**: `# # # # #` (DOCX), `END` (HTML), or sffms-style end-of-story marker (LaTeX)

## Dependencies

- **Python 3.11+**
- **Pandoc**: For format conversions
- **LaTeX** (optional): For PDF generation via LaTeX
- **Apple Pages** (macOS only): Alternative PDF generation

## Development

Day-to-day development uses [`uv`](https://docs.astral.sh/uv/) with a
project-local virtualenv at `.venv/`.

```bash
# Install dependencies (creates .venv/ if needed)
uv sync

# Run the CLI from the dev checkout
uv run mdfic --help

# Run the test suite
uv run pytest
```

The test suite registers four pytest markers — `pandoc`, `darwin`,
`network`, and `git` — and skips tests automatically when the
corresponding tool or platform is unavailable, so a clean machine
without pandoc or LaTeX installed will still see most tests pass.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 JP Fosterson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Author

JP Fosterson

---

*MDFIC helps fiction writers focus on their craft while maintaining professional manuscript standards. Write in Markdown, build like code, publish like a pro.*
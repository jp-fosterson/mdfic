# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial pytest test suite with 100 tests covering pure-logic functions in
  `utils`, `tweets`, `makefile`, `latex`, and `docx`, plus end-to-end tests
  for the seven pure-text CLI commands (`wc`, `gitignore`, `makefile`,
  `tweet`, `css`, `hrrepl`, `strip-word-doc`), the three pandoc-required
  CLI commands (`latex`, `docx`, `html`), and the three external-dependency
  CLI commands (`copyedit`, `pages-to-pdf`, `progress`).
- Two lorem-ipsum asset stories under `tests/assets/` (single-file and
  multi-file matching the `MULTI_TEMPLATE` `metadata.yaml` + `STORY-NN.md`
  convention) plus shared fixtures in `tests/conftest.py`.
- `[dependency-groups] dev` in `pyproject.toml` with `pytest`, and
  `[tool.pytest.ini_options]` registering `pandoc`, `darwin`, `network`,
  and `git` markers for integration tests.
- Pandoc availability hook in `tests/conftest.py` that auto-skips
  `@pytest.mark.pandoc` tests when pandoc isn't on PATH. DOCX tests
  read back via `python-docx` and `zipfile` to verify SFFMS header
  injection; LaTeX/HTML tests use substring assertions on key tokens.
- `tmp_git_repo` fixture in `tests/conftest.py` that initializes an
  isolated repo (with per-repo identity) and `chdir`s into it, used by
  the `progress` tests to drive real `git diff` without touching global
  state.
- `copyedit` CLI tests mock `mdfic.copyedit.copy_editor_chain` at the LCEL
  pipeline boundary; an autouse fixture stubs `keyring.get_password` so
  the module-level keyring lookup never prompts the keychain on dev
  machines where `OPENAI_USER` is set.
- `pages-to-pdf` CLI tests mock `mdfic.utils.oascript` and assert the
  AppleScript was constructed with the correct absolute input/output
  paths.

### Fixed
- `mdfic/docx.py` `prettyxml` referenced an undefined `xml_fname` and was
  dead-on-call; now uses the function's `xml` parameter.
- `mdfic gitignore` raised `TypeError` on every invocation because the
  callback declared an unused `latex` parameter with no corresponding
  Click option; the parameter has been removed.
- `mdfic html` raised `UnboundLocalError` for `cssargs` whenever `--css`
  was omitted; `cssargs` is now initialized before the conditional.

## [1.0.0] - 2025-09-06

### Added
- MIT License with full license text and copyright notice
- License information added to CLI help output
- Modern Python packaging with pyproject.toml configuration
- Comprehensive README.md with detailed documentation including:
  - Philosophy and key features
  - Installation instructions with external dependencies
  - Quick start guide
  - Command reference with examples
  - Professional manuscript formatting standards
  - Project structure examples
- Enhanced copyediting functionality with configurable strength levels
- Improved CLI interface with additional commands and options
- Enhanced Makefile generation with better multi-part story support
- Tweet generation improvements for social media sharing
- Better utility functions for story processing

### Changed
- Migrated from setup.py to modern pyproject.toml build system
- Updated project metadata and dependencies
- Enhanced CLI help and documentation
- Improved error handling and user experience

### Technical Details
- Python 3.6+ support with compatibility for Python 3.12
- Dependencies: click, markdown, python-docx, PyYAML
- Development status: Stable
- Full MIT License compliance

## [0.1.0] - 2023-05-15

### Added
- Initial release of MDFIC (Markdown Fiction Toolkit)
- Core functionality for converting Markdown fiction to multiple formats:
  - DOCX manuscript generation with SFFMS formatting
  - LaTeX/PDF output with professional typography
  - HTML generation with CSS styling
  - CSS stylesheet generation
- Story project management tools:
  - Makefile generation for automated builds
  - Git integration with .gitignore generation
- Writer-focused utilities:
  - Word counting and reading time estimation
  - Progress tracking with Git integration
  - Tweet generation for social media
- Professional manuscript formatting following SFFMS standards
- Support for both single-file and multi-part stories
- YAML metadata handling for story information
- Scene break management and numbering
- Command-line interface with comprehensive options

### Technical Implementation
- Modular Python architecture with separate modules for:
  - CLI interface ([`cli.py`](mdfic/cli.py))
  - DOCX generation ([`docx.py`](mdfic/docx.py))
  - LaTeX processing ([`latex.py`](mdfic/latex.py))
  - CSS styling ([`css.py`](mdfic/css.py))
  - Makefile generation ([`makefile.py`](mdfic/makefile.py))
  - Tweet processing ([`tweets.py`](mdfic/tweets.py))
  - Utility functions ([`utils.py`](mdfic/utils.py))
- Integration with Pandoc for document conversion
- Support for external LaTeX and Apple Pages workflows

---

*MDFIC helps fiction writers focus on their craft while maintaining professional manuscript standards. Write in Markdown, build like code, publish like a pro.*
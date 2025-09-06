# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
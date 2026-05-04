from mdfic.cli import cli


# wc -------------------------------------------------------

def test_wc(cli_runner, tmp_path):
    inp = tmp_path / "story.md"
    inp.write_text("one two three four five")
    result = cli_runner.invoke(cli, ["wc", str(inp)])
    assert result.exit_code == 0, result.output
    assert "5 words" in result.output
    assert "TOTAL: 5 words" in result.output


def test_wc_uses_asset(cli_runner, single_story):
    result = cli_runner.invoke(cli, ["wc", str(single_story)])
    assert result.exit_code == 0, result.output
    assert "words" in result.output
    assert "TOTAL" in result.output


# gitignore ------------------------------------------------

def test_gitignore_default(cli_runner):
    result = cli_runner.invoke(cli, ["gitignore", "--name", "mystory"])
    assert result.exit_code == 0, result.output
    assert "mystory.tex" in result.output
    assert "images/" in result.output
    assert "out/" in result.output


def test_gitignore_multi_adds_md(cli_runner):
    result = cli_runner.invoke(cli, ["gitignore", "--name", "mystory", "--multi"])
    assert result.exit_code == 0, result.output
    assert "mystory.md" in result.output


def test_gitignore_no_multi_omits_bare_md(cli_runner):
    result = cli_runner.invoke(cli, ["gitignore", "--name", "mystory"])
    assert result.exit_code == 0, result.output
    assert "\nmystory.md\n" not in result.output


# makefile -------------------------------------------------

def test_makefile_cli_single(cli_runner):
    result = cli_runner.invoke(cli, ["makefile", "--name", "foo"])
    assert result.exit_code == 0, result.output
    assert "STORY=foo" in result.output
    assert "mdfic pages-to-pdf" in result.output


def test_makefile_cli_multi_latex(cli_runner):
    result = cli_runner.invoke(cli, ["makefile", "--name", "foo", "--multi", "--latex"])
    assert result.exit_code == 0, result.output
    assert "STORY=foo" in result.output
    assert "$(STORY)-*.md" in result.output
    assert "pdflatex" in result.output


# tweet ----------------------------------------------------

def test_tweet(cli_runner, tmp_path):
    inp = tmp_path / "in.md"
    inp.write_text("Lorem ipsum dolor sit amet.\n\nConsectetur adipiscing elit.")
    result = cli_runner.invoke(cli, ["tweet", "--maxlen", "100", str(inp)])
    assert result.exit_code == 0, result.output
    assert "####" in result.output
    assert "1 |" in result.output


# css ------------------------------------------------------

def test_css(cli_runner):
    from mdfic.css import CSS
    result = cli_runner.invoke(cli, ["css"])
    assert result.exit_code == 0, result.output
    assert result.output == CSS


# hrrepl ---------------------------------------------------

def test_hrrepl_default(cli_runner, tmp_path):
    inp = tmp_path / "in.html"
    inp.write_text("before<hr />after")
    result = cli_runner.invoke(cli, ["hrrepl", str(inp)])
    assert result.exit_code == 0, result.output
    assert "<hr />" not in result.output
    assert "•" in result.output
    assert "before" in result.output
    assert "after" in result.output


def test_hrrepl_custom_text(cli_runner, tmp_path):
    inp = tmp_path / "in.html"
    inp.write_text("a<hr />b")
    result = cli_runner.invoke(cli, ["hrrepl", "--withtxt", "[break]", str(inp)])
    assert result.exit_code == 0, result.output
    assert "[break]" in result.output


# strip-word-doc -------------------------------------------

def test_strip_word_doc(cli_runner, tmp_path):
    inp = tmp_path / "in.bin"
    inp.write_bytes(b"hello\xd2world\xd3\r")
    result = cli_runner.invoke(cli, ["strip-word-doc", str(inp)])
    assert result.exit_code == 0, result.output
    assert result.output == 'hello"world"\n\n'

from mdfic.makefile import makefile


def test_makefile_single_pages():
    out = makefile(name="foo")
    assert "STORY=foo" in out
    assert "mdfic pages-to-pdf" in out
    assert "pdflatex" not in out


def test_makefile_single_latex():
    out = makefile(name="foo", latex=True)
    assert "STORY=foo" in out
    assert "pdflatex" in out
    assert "mdfic pages-to-pdf" not in out


def test_makefile_multi_pages():
    out = makefile(name="foo", multi=True)
    assert "STORY=foo" in out
    assert "$(STORY)-*.md" in out
    assert "mdfic pages-to-pdf" in out


def test_makefile_multi_latex():
    out = makefile(name="foo", multi=True, latex=True)
    assert "STORY=foo" in out
    assert "$(STORY)-*.md" in out
    assert "pdflatex" in out


def test_makefile_substitutes_arbitrary_name():
    out = makefile(name="my-special-story")
    assert "STORY=my-special-story" in out

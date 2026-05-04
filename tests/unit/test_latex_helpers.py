from mdfic.latex import (
    SCENE_HR_TEX,
    convert_newscenes_to_numbers,
    get_packages,
    replace_newscene,
    replace_section,
)


# replace_section ------------------------------------------

def test_replace_section_basic():
    assert replace_section("\\section{Heading}") == "\\textbf{Heading}"


def test_replace_section_multiple():
    out = replace_section("\\section{One}\n\\section{Two}")
    assert "\\section" not in out
    assert out.count("\\textbf{") == 2


def test_replace_section_no_match_unchanged():
    assert replace_section("no sections here") == "no sections here"


# replace_newscene -----------------------------------------

def test_replace_newscene_substitutes_marker():
    out = replace_newscene(f"before {SCENE_HR_TEX} after")
    assert "\\newscene" in out
    assert SCENE_HR_TEX not in out


def test_replace_newscene_no_match_unchanged():
    assert replace_newscene("no scene markers") == "no scene markers"


# get_packages ---------------------------------------------

def test_get_packages_present():
    meta = {"mdfic": {"latexpackages": ["microtype", "geometry"]}}
    assert get_packages(meta) == ["microtype", "geometry"]


def test_get_packages_missing_top_level():
    assert get_packages({}) == []


def test_get_packages_missing_nested():
    assert get_packages({"mdfic": {}}) == []


# convert_newscenes_to_numbers -----------------------------

def test_convert_newscenes_arabic():
    out = convert_newscenes_to_numbers(f"first scene{SCENE_HR_TEX}second scene", style="arabic")
    assert "\\textbf{1}" in out
    assert "\\textbf{2}" in out
    assert "first scene" in out
    assert "second scene" in out
    assert SCENE_HR_TEX not in out


def test_convert_newscenes_roman():
    out = convert_newscenes_to_numbers(f"a{SCENE_HR_TEX}b{SCENE_HR_TEX}c", style="roman")
    assert "\\textbf{I}" in out
    assert "\\textbf{II}" in out
    assert "\\textbf{III}" in out


def test_convert_newscenes_default_arabic():
    out = convert_newscenes_to_numbers(f"a{SCENE_HR_TEX}b")
    assert "\\textbf{1}" in out
    assert "\\textbf{2}" in out


def test_convert_newscenes_no_breaks_still_numbers_first():
    out = convert_newscenes_to_numbers("just text")
    assert "\\textbf{1}" in out
    assert "just text" in out

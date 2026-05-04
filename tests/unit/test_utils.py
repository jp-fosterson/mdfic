import pytest

from mdfic.utils import (
    fix_sentence_spacing,
    split_metadata_and_text,
    parse_metadata,
    get_in,
    int_to_roman,
)


# fix_sentence_spacing -------------------------------------

def test_fix_sentence_spacing_collapses_to_one():
    assert fix_sentence_spacing("Hi.  There.   Friend.") == "Hi. There. Friend."


def test_fix_sentence_spacing_expands_to_two():
    assert fix_sentence_spacing("Hi. There.", N=2) == "Hi.  There."


def test_fix_sentence_spacing_no_periods_unchanged():
    assert fix_sentence_spacing("hello world") == "hello world"


def test_fix_sentence_spacing_zero_strips():
    assert fix_sentence_spacing("Hi.  There.", N=0) == "Hi.There."


# split_metadata_and_text ----------------------------------

def test_split_metadata_with_dot_terminator():
    md, text = split_metadata_and_text("---\ntitle: T\n...\nbody")
    assert "title: T" in md
    assert "body" in text


def test_split_metadata_with_dash_terminator():
    md, text = split_metadata_and_text("---\ntitle: T\n---\nbody")
    assert "title: T" in md
    assert "body" in text


def test_split_metadata_no_metadata():
    md, text = split_metadata_and_text("just a body")
    assert md is None
    assert text == "just a body"


def test_split_metadata_malformed_raises():
    with pytest.raises(ValueError):
        split_metadata_and_text("---\ntitle: T\nno_close")


# parse_metadata -------------------------------------------

def test_parse_metadata_returns_empty_when_no_yaml():
    assert parse_metadata("body only") == {}


def test_parse_metadata_joins_top_level_lists():
    doc = "---\naddress:\n  - line1\n  - line2\n...\nbody"
    meta = parse_metadata(doc)
    assert meta["address"] == "line1\nline2"


def test_parse_metadata_custom_join():
    doc = "---\naddress:\n  - line1\n  - line2\n...\nbody"
    meta = parse_metadata(doc, join="\\\\")
    assert meta["address"] == "line1\\\\line2"


def test_parse_metadata_includes_yaml_length():
    meta = parse_metadata("---\ntitle: T\n...\nbody")
    assert isinstance(meta["metadata_yaml_length"], int)
    assert meta["metadata_yaml_length"] > 0


def test_parse_metadata_does_not_join_nested_lists():
    doc = (
        "---\n"
        "mdfic:\n"
        "  latex:\n"
        "    extra_headers:\n"
        "      - line1\n"
        "      - line2\n"
        "...\n"
        "body"
    )
    meta = parse_metadata(doc)
    assert meta["mdfic"]["latex"]["extra_headers"] == ["line1", "line2"]


# get_in ---------------------------------------------------

def test_get_in_top_level():
    assert get_in({"a": 1}, ["a"], None) == 1


def test_get_in_nested():
    assert get_in({"a": {"b": {"c": 42}}}, ["a", "b", "c"], None) == 42


def test_get_in_missing_returns_default():
    assert get_in({"a": 1}, ["b"], "default") == "default"


def test_get_in_missing_nested_returns_default():
    assert get_in({"a": {"b": 1}}, ["a", "x"], "default") == "default"


def test_get_in_typeerror_returns_default():
    assert get_in({"a": 1}, ["a", "b"], "default") == "default"


# int_to_roman ---------------------------------------------

@pytest.mark.parametrize(
    "n,expected",
    [
        (1, "I"),
        (4, "IV"),
        (9, "IX"),
        (40, "XL"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (1994, "MCMXCIV"),
        (3999, "MMMCMXCIX"),
    ],
)
def test_int_to_roman_known_values(n, expected):
    assert int_to_roman(n) == expected


def test_int_to_roman_zero_raises():
    with pytest.raises(ValueError):
        int_to_roman(0)


def test_int_to_roman_too_large_raises():
    with pytest.raises(ValueError):
        int_to_roman(4000)


def test_int_to_roman_non_int_raises():
    with pytest.raises(TypeError):
        int_to_roman("five")

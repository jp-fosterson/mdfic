import re

from mdfic.tweets import (
    SENTENCE_DELIM,
    argmin,
    generate,
    split_paragraphs,
    split_tweets,
)


# argmin ---------------------------------------------------

def test_argmin_simple():
    assert argmin([3, 1, 2], lambda x: x) == 1


def test_argmin_single_element():
    assert argmin([42], lambda x: x) == 42


def test_argmin_finds_closest_to_target():
    assert argmin([1, 5, 10], lambda x: abs(x - 4)) == 5


# split_paragraphs -----------------------------------------

def test_split_paragraphs_filters_empty_lines():
    assert split_paragraphs("a\n\nb\n\n\nc") == ["a", "b", "c"]


def test_split_paragraphs_empty_input():
    assert split_paragraphs("") == []


# split_tweets ---------------------------------------------

def test_split_tweets_short_returns_unchanged():
    assert split_tweets("short text", SENTENCE_DELIM, maxlen=280) == ["short text"]


def test_split_tweets_splits_long_text():
    para = "first sentence. second sentence. third sentence. fourth sentence."
    chunks = split_tweets(para, SENTENCE_DELIM, maxlen=25)
    assert len(chunks) > 1
    assert all(c for c in chunks)


def test_split_tweets_no_delim_gives_up():
    para = "a" * 500
    assert split_tweets(para, SENTENCE_DELIM, maxlen=100) == [para]


# generate -------------------------------------------------

def test_generate_yields_length_and_content():
    tweets = list(generate("Lorem ipsum dolor sit amet.", maxlen=280, add_counter=False))
    assert len(tweets) >= 1
    for length, content in tweets:
        assert length == len(content)


def test_generate_strips_metadata_block():
    text = "---\ntitle: T\n...\nbody text here."
    joined = "".join(t for _, t in generate(text, maxlen=280, add_counter=False))
    assert "title: T" not in joined
    assert "body text here" in joined


def test_generate_includes_counter_when_requested():
    tweets = list(generate("Lorem ipsum dolor sit amet.", maxlen=280, add_counter=True))
    assert tweets
    for _, content in tweets:
        assert re.search(r"\n\d+/\d+", content)


def test_generate_omits_counter_when_disabled():
    tweets = list(generate("Lorem ipsum dolor sit amet.", maxlen=280, add_counter=False))
    assert tweets
    for _, content in tweets:
        assert not re.search(r"\n\d+/\d+", content)

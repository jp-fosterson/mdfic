from xml.dom import minidom

from mdfic.docx import (
    isemphasis,
    isstrong,
    prettyxml,
    xml_get_rel_ids,
    xml_rel_nums,
    xml_traverse,
)


# isstrong / isemphasis ------------------------------------

def test_isstrong_recognizes_b_and_strong():
    assert isstrong("b")
    assert isstrong("strong")


def test_isstrong_rejects_others():
    assert not isstrong("i")
    assert not isstrong("em")
    assert not isstrong("p")


def test_isemphasis_recognizes_i_and_em():
    assert isemphasis("i")
    assert isemphasis("em")


def test_isemphasis_rejects_others():
    assert not isemphasis("b")
    assert not isemphasis("strong")
    assert not isemphasis("p")


# prettyxml (locks in xml_fname -> xml fix) ----------------

def test_prettyxml_returns_pretty_string():
    out = prettyxml("<root><child>text</child></root>")
    assert "<root>" in out
    assert "<child>" in out
    assert "text" in out


# xml_traverse ---------------------------------------------

def test_xml_traverse_yields_all_elements_in_order():
    doc = minidom.parseString("<a><b/><c/></a>")
    tags = [n.tagName for n in xml_traverse(doc) if n.nodeType == n.ELEMENT_NODE]
    assert tags == ["a", "b", "c"]


# xml_get_rel_ids ------------------------------------------

def test_xml_get_rel_ids_finds_ids():
    doc = minidom.parseString(
        '<Relationships>'
        '<Relationship Id="rId1" Target="x"/>'
        '<Relationship Id="rId2" Target="y"/>'
        '</Relationships>'
    )
    assert xml_get_rel_ids(doc) == ["rId1", "rId2"]


def test_xml_get_rel_ids_empty_when_no_ids():
    doc = minidom.parseString("<root/>")
    assert xml_get_rel_ids(doc) == []


# xml_rel_nums ---------------------------------------------

def test_xml_rel_nums_extracts_numeric_suffixes():
    doc = minidom.parseString(
        '<Relationships>'
        '<Relationship Id="rId1"/>'
        '<Relationship Id="rId42"/>'
        '</Relationships>'
    )
    assert xml_rel_nums(doc) == [1, 42]

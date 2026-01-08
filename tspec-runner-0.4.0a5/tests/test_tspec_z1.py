from tspec.tspec_z1 import decode_z1_text, decompile_z1_text, expand_z1_sections


def test_decode_z1_parses_dictionary_and_sections():
    raw = "Z1|D{p=path;sc=scope}P{SCOPE:@sc=@p\\|x|FILES:#a\\}b}"
    doc = decode_z1_text(raw)
    assert doc.dictionary == {"p": "path", "sc": "scope"}
    assert len(doc.sections) == 2
    assert doc.sections[0].tag == "SCOPE"
    assert doc.sections[0].body == "@sc=@p|x"
    assert doc.sections[1].tag == "FILES"
    assert doc.sections[1].body == "#a}b"


def test_decompile_expands_refs():
    raw = "Z1|D{p=path;sc=scope}P{SCOPE:@sc=@p}"
    text = decompile_z1_text(raw)
    assert "TSPEC-Z1 DECOMPILED" in text
    assert "scope=path" in text


def test_expand_z1_sections():
    raw = "Z1|D{p=path}P{SCOPE:@p}"
    doc = decode_z1_text(raw)
    expanded = expand_z1_sections(doc)
    assert expanded[0].body == "path"

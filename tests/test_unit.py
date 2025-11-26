from app.main import sanitize

def test_replaces_case_insensitive_keep_first_last():
    assert sanitize("Foo foo FOO", ["foo"]) == "F*o f*o F*O"

def test_multiple_words():
    assert sanitize("foo and bar", ["foo", "bar"]) == "f*o and b*r"

def test_substring_replaced_too():
    assert sanitize("football", ["foo"]) == "f*otball"

from quotes import clean


def test_clean():
    assert clean("“Hello”") == "Hello"

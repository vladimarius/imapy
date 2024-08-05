from imapy import utils


def test_utf7_to_unicode():
    assert utils.utf7_to_unicode(b"&APY-") == "ö"
    assert utils.utf7_to_unicode(b"Hello &APY-") == "Hello ö"
    assert utils.utf7_to_unicode(b"&APY-&APY-") == "öö"
    assert utils.utf7_to_unicode(b"&BD8EQAQ4BDIENQRC-") == "привет"


def test_str_to_utf7():
    assert utils.str_to_utf7("привет") == b"&BD8EQAQ4BDIENQRC-"
    assert utils.str_to_utf7("Hello ö") == b"Hello &APY-"


def test_u():
    assert utils.u("test") == "test"
    assert utils.u("テスト") == "テスト"


def test_to_unescaped_str():
    assert utils.to_unescaped_str("test\\ntest") == "test\ntest"
    assert utils.to_unescaped_str("test\\ttest") == "test\ttest"


def test_b_to_str():
    assert utils.b_to_str(b"test") == "test"
    assert utils.b_to_str(b"\xc3\xa4") == "ä"


def test_str_to_b():
    assert utils.str_to_b("test") == b"test"
    assert utils.str_to_b("ä") == b"\xc3\xa4"

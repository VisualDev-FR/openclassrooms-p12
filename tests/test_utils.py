from controller import utils


def test_email_is_valid():
    assert utils.email_is_valid("dummy.client@example.co")
    assert utils.email_is_valid("dumm21Ay.cl154Aient@ex2545Aample.co")
    assert utils.email_is_valid("client@example.co")

    assert not utils.email_is_valid("dummy.client@co")
    assert not utils.email_is_valid("invalid_email")


def test_drop_none_from_dict():
    assert utils.drop_none_from_dict({"key1": None, "key2": None}) == {}

    assert utils.drop_none_from_dict({"key1": "value1", "key2": None}) == {
        "key1": "value1"
    }

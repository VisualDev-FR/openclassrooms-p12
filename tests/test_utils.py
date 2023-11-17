import pytest

from controller import utils


def test_email_validator():

    email = "dummy.client@example.co"
    assert utils.validate_email(email) == email

    email = "dumm21Ay.cl154Aient@ex2545Aample.co"
    assert utils.validate_email(email) == email

    email = "client@example.co"
    assert utils.validate_email(email) == email

    with pytest.raises(ValueError):
        utils.validate_email("dummy.client@co")

    with pytest.raises(ValueError):
        utils.validate_email("invalid_email")


def test_phone_validator():

    phone = "06 07 08 09 10"
    assert utils.validate_phone(phone) == phone

    phone = "0607080910"
    assert utils.validate_phone(phone) == phone

    phone = "+33607080910"
    assert utils.validate_phone(phone) == phone

    phone = "+33 6 07 08 09 10"
    assert utils.validate_phone(phone) == phone

    phone = "06-07-08-09-10"
    assert utils.validate_phone(phone) == phone

    phone = "123-456-7890"
    assert utils.validate_phone(phone) == phone

    phone = "123 456 7890"
    assert utils.validate_phone(phone) == phone

    phone = "1234567890"
    assert utils.validate_phone(phone) == phone

    with pytest.raises(ValueError):
        utils.validate_phone("invalid_phone")


def test_drop_dict_none_values():
    assert utils.drop_dict_none_values({"key1": None, "key2": None}) == {}

    assert utils.drop_dict_none_values({"key1": "value1", "key2": None}) == {
        "key1": "value1"
    }

    assert utils.drop_dict_none_values({"key1": "value1", "key2": "value2"}) == {
        "key1": "value1", "key2": "value2"
    }

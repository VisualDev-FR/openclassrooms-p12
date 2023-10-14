from unittest.mock import patch
from pathlib import Path
import pytest

from authentification.login import login, sign_up, logout
from authentification.token import (
    store_token,
    retreive_token,
    create_token,
    decode_token,
    clear_token
)

__TOKEN_PATH_TEMP = Path("tests/ignore/token.txt")
__TOKEN_TEMP = create_token(user_id=1)


@pytest.fixture
def token_path_mock():
    return patch("authentification.token.__get_token_path", lambda: __TOKEN_PATH_TEMP)


@pytest.fixture
def token_temp() -> str:
    with open(__TOKEN_PATH_TEMP, "w") as writer:
        writer.write(__TOKEN_TEMP)

    return __TOKEN_TEMP


def test_store_token(token_path_mock):
    with token_path_mock:
        store_token("mytoken")

    with open(__TOKEN_PATH_TEMP, "r") as reader:
        assert reader.read() == "mytoken"


def test_retreive_token(token_temp, token_path_mock):
    with token_path_mock:
        token = retreive_token()

    assert token == __TOKEN_TEMP


def test_decode_token():
    decoded_token = decode_token(__TOKEN_TEMP)
    assert decoded_token["user_id"] == 1

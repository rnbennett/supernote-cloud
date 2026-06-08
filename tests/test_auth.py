"""Password login flow: success, identity-verification (E1760), and failure."""

import pytest

from supernote_cloud import endpoints
from supernote_cloud.api import calc_md5, calc_sha256
from supernote_cloud.exceptions import AuthenticationError

from .conftest import FakeAPI, make_client


def _random_code_ok(payload):
    return {"success": True, "randomCode": "RC123", "timestamp": "1700000000"}


def test_login_success_sets_token_and_signs_password():
    client = make_client(token=None)
    fake = FakeAPI(
        {
            endpoints.code: _random_code_ok,
            endpoints.login: {"success": True, "token": "TOK-XYZ"},
        }
    )
    client._api_call = fake

    assert client.login("user@example.com", "hunter2") == "TOK-XYZ"
    assert client._access_token == "TOK-XYZ"

    sent = fake.payload_for(endpoints.login)
    assert sent["account"] == "user@example.com"
    # Password is sha256(md5(password) + randomCode) — guard the formula.
    assert sent["password"] == calc_sha256(calc_md5("hunter2") + "RC123")


def test_login_identity_verification_raises_e1760_sentinel():
    client = make_client(token=None)
    client._api_call = FakeAPI(
        {
            endpoints.code: _random_code_ok,
            endpoints.login: {"success": False, "errorCode": "E1760"},
        }
    )
    with pytest.raises(AuthenticationError) as exc:
        client.login("user@example.com", "hunter2")
    assert str(exc.value).startswith("__E1760__:")


def test_login_failure_surfaces_error_message():
    client = make_client(token=None)
    client._api_call = FakeAPI(
        {
            endpoints.code: _random_code_ok,
            endpoints.login: {
                "success": False,
                "errorCode": "E0001",
                "errorMsg": "Invalid credentials",
            },
        }
    )
    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        client.login("user@example.com", "wrong")

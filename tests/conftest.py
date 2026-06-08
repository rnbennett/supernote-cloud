"""Shared test fixtures and fakes.

Tests never touch the network: we build an ``SNClient`` without running its
``__init__`` (which would fetch a CSRF token) and replace ``_api_call`` with a
recording fake that returns canned responses per endpoint.
"""

import pytest

from supernote_cloud.api import SNClient
from supernote_cloud.models import Directory, File


def make_client(token="test-token"):
    """Build an SNClient with no network call in __init__."""
    client = SNClient.__new__(SNClient)
    client._client = None  # download/upload paths aren't exercised here
    client._access_token = token
    client._csrf_token = "csrf"
    return client


class FakeAPI:
    """Stand-in for SNClient._api_call.

    Records every (endpoint, payload) call and returns a canned response keyed
    by endpoint. A response may be a dict or a callable(payload) -> dict.
    Unmapped endpoints return ``default`` (a generic success).
    """

    def __init__(self, responses=None, default=None):
        self.calls = []
        self.responses = responses or {}
        self.default = {"success": True} if default is None else default

    def __call__(self, endpoint, payload):
        self.calls.append((endpoint, payload))
        resp = self.responses.get(endpoint, self.default)
        return resp(payload) if callable(resp) else resp

    def payload_for(self, endpoint):
        """Return the payload of the first call made to ``endpoint``."""
        for called_endpoint, payload in self.calls:
            if called_endpoint == endpoint:
                return payload
        raise AssertionError(f"no call recorded for endpoint {endpoint!r}")


def item_dict(id, name, is_folder, directory_id=0):
    """Build a raw API item dict (alias keys) for File/Directory construction."""
    return {
        "id": id,
        "directoryId": directory_id,
        "fileName": name,
        "size": 123,
        "md5": "deadbeef",
        "isFolder": is_folder,
        "createTime": 1700000000000,
        "updateTime": 1700000000000,
    }


def make_file(id, name, directory_id=0):
    return File(**item_dict(id, name, "N", directory_id))


def make_dir(id, name, directory_id=0):
    return Directory(**item_dict(id, name, "Y", directory_id))


@pytest.fixture
def client():
    """Authenticated client with a recording FakeAPI installed."""
    c = make_client()
    c._api_call = FakeAPI()
    return c


@pytest.fixture
def anon_client():
    """Client with no access token (every guarded call should refuse)."""
    return make_client(token=None)

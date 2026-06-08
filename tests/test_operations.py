"""File operations: ls parsing plus rename/move/copy/delete/mkdir payloads & errors."""

import pytest

from supernote_cloud import endpoints
from supernote_cloud.exceptions import ApiError, AuthenticationError
from supernote_cloud.models import Directory, File

from .conftest import FakeAPI, item_dict, make_dir, make_file

# --- ls -------------------------------------------------------------------

def test_ls_parses_folders_and_files(client):
    client._api_call = FakeAPI(
        {
            endpoints.ls: {
                "userFileVOList": [
                    item_dict(1, "Notes", "Y"),
                    item_dict(2, "a.note", "N"),
                ]
            }
        }
    )
    result = client.ls()
    assert isinstance(result[0], Directory) and result[0].file_name == "Notes"
    assert isinstance(result[1], File) and result[1].file_name == "a.note"


def test_ls_requires_authentication(anon_client):
    with pytest.raises(AuthenticationError):
        anon_client.ls()


# --- rename ---------------------------------------------------------------

def test_rename_sends_id_and_new_name(client):
    fake = FakeAPI({endpoints.rename: {"success": True}})
    client._api_call = fake
    assert client.rename(make_file(10, "old.note"), "new.note") == "new.note"
    assert fake.payload_for(endpoints.rename) == {"id": 10, "newName": "new.note"}


def test_rename_failure_raises_apierror(client):
    client._api_call = FakeAPI(
        {endpoints.rename: {"success": False, "errorMsg": "nope"}}
    )
    with pytest.raises(ApiError, match="nope"):
        client.rename(make_file(10, "old.note"), "new.note")


def test_rename_requires_authentication(anon_client):
    with pytest.raises(AuthenticationError):
        anon_client.rename(make_file(10, "old.note"), "new.note")


# --- move / copy ----------------------------------------------------------

@pytest.mark.parametrize(
    "method, endpoint",
    [("move", endpoints.move), ("copy", endpoints.copy)],
)
def test_move_copy_payload_and_return(client, method, endpoint):
    fake = FakeAPI({endpoint: {"success": True}})
    client._api_call = fake
    src = make_file(10, "a.note", directory_id=5)
    dest = make_dir(99, "Archive")

    result = getattr(client, method)(src, dest)

    assert result == "a.note"
    assert fake.payload_for(endpoint) == {
        "directoryId": 5,
        "goDirectoryId": 99,
        "idList": [10],
    }


def test_move_accepts_a_list(client):
    fake = FakeAPI({endpoints.move: {"success": True}})
    client._api_call = fake
    items = [make_file(10, "a.note", directory_id=5), make_file(11, "b.note", directory_id=5)]
    result = client.move(items, make_dir(99, "Archive"))
    assert result == "a.note, b.note"
    assert fake.payload_for(endpoints.move)["idList"] == [10, 11]


# --- delete ---------------------------------------------------------------

def test_delete_sends_directory_and_ids(client):
    fake = FakeAPI({endpoints.delete: {"success": True}})
    client._api_call = fake
    assert client.delete(make_file(10, "a.note", directory_id=5)) == "a.note"
    assert fake.payload_for(endpoints.delete) == {"directoryId": 5, "idList": [10]}


def test_delete_failure_raises_apierror(client):
    client._api_call = FakeAPI(
        {endpoints.delete: {"success": False, "errorMsg": "gone"}}
    )
    with pytest.raises(ApiError, match="gone"):
        client.delete(make_file(10, "a.note", directory_id=5))


# --- mkdir ----------------------------------------------------------------

def test_mkdir_at_root(client):
    fake = FakeAPI({endpoints.mkdir: {"success": True}})
    client._api_call = fake
    assert client.mkdir("NewFolder") == "NewFolder"
    assert fake.payload_for(endpoints.mkdir) == {
        "directoryId": 0,
        "fileName": "NewFolder",
    }


def test_mkdir_failure_raises_apierror(client):
    client._api_call = FakeAPI(
        {endpoints.mkdir: {"success": False, "errorMsg": "exists"}}
    )
    with pytest.raises(ApiError, match="exists"):
        client.mkdir("NewFolder")

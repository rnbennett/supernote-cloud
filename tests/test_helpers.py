"""Pure helpers and path/key resolution that need no network."""

import pytest

from supernote_cloud.api import SNClient, calc_md5, calc_sha256

from .conftest import make_client


def test_calc_sha256_known_vector():
    # Well-known SHA-256 of "abc"
    assert calc_sha256("abc") == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_calc_md5_str_known_vector():
    assert calc_md5("abc") == "900150983cd24fb0d6963f7d28e17f72"


def test_calc_md5_bytes_matches_str():
    assert calc_md5(b"abc") == calc_md5("abc")


def test_calc_md5_rejects_other_types():
    with pytest.raises(TypeError):
        calc_md5(12345)


@pytest.mark.parametrize("value", [None, 0, "/"])
def test_get_directory_id_root_aliases(value):
    client = make_client()
    assert client._get_directory_id(value) == 0


def test_get_directory_id_passthrough_int():
    client = make_client()
    assert client._get_directory_id(42) == 42


def test_get_directory_id_from_directory_object():
    from .conftest import make_dir

    client = make_client()
    assert client._get_directory_id(make_dir(7, "Archive")) == 7


def test_get_directory_id_invalid_type():
    client = make_client()
    with pytest.raises(ValueError):
        client._get_directory_id(3.14)


def test_extract_real_key_uses_last_char_as_index():
    # Last char "2" indexes into the dash-split parts -> "z".
    client = make_client()
    assert client._extract_real_key("x-y-z-2") == "z"
    assert SNClient._extract_real_key(client, "a-b-0") == "a"

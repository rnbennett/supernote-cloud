"""Recursive walk() traversal, driven by a stubbed ls()."""

import pytest

from supernote_cloud.exceptions import AuthenticationError

from .conftest import make_client, make_dir, make_file


def _tree_ls():
    """A 3-level tree:  /  ->  A(1), r.note   |  A -> B(2), a.note  |  B -> b.note."""
    root = [make_dir(1, "A"), make_file(10, "r.note")]
    a = [make_dir(2, "B", directory_id=1), make_file(11, "a.note", directory_id=1)]
    b = [make_file(12, "b.note", directory_id=2)]

    def ls(directory=None):
        if directory is None:
            return root
        return {1: a, 2: b}[directory.id]

    return ls


def test_walk_visits_every_directory_depth_first():
    client = make_client()
    client.ls = _tree_ls()  # instance attr shadows the bound method

    visited = list(client.walk())

    paths = [path for path, _dirs, _files in visited]
    assert paths == ["/", "/A", "/A/B"]

    # Files surfaced at each level
    files_by_path = {path: [f.file_name for f in files] for path, _dirs, files in visited}
    assert files_by_path == {
        "/": ["r.note"],
        "/A": ["a.note"],
        "/A/B": ["b.note"],
    }


def test_walk_requires_authentication():
    client = make_client(token=None)
    with pytest.raises(AuthenticationError):
        list(client.walk())

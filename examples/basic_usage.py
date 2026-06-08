"""Minimal example: log in, list the root folder, download the first file.

Set credentials in the environment first:

    export SUPERNOTE_EMAIL=you@example.com
    export SUPERNOTE_PASSWORD=...

Then:  python examples/basic_usage.py
"""

import os
from pathlib import Path

from supernote_cloud import SNClient


def main() -> None:
    client = SNClient()
    client.login(os.environ["SUPERNOTE_EMAIL"], os.environ["SUPERNOTE_PASSWORD"])

    items = client.ls()
    print(f"{len(items)} item(s) in the root folder:")
    for item in items:
        kind = "dir " if item.is_folder == "Y" else "file"
        print(f"  [{kind}] {item.file_name}")

    files = [i for i in items if i.is_folder == "N"]
    if files:
        saved_to = client.get(files[0], Path("."))
        print(f"Downloaded {files[0].file_name} -> {saved_to}")


if __name__ == "__main__":
    main()

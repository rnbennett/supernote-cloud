"""Back up an entire Supernote folder tree to a local directory, preserving structure.

Usage:
    python examples/sync_folder.py [REMOTE_PATH] [LOCAL_DIR]

Defaults: REMOTE_PATH="/", LOCAL_DIR="supernote-backup".
Credentials come from SUPERNOTE_EMAIL / SUPERNOTE_PASSWORD.
"""

import os
import sys
from pathlib import Path

from supernote_cloud import SNClient


def main() -> None:
    remote_root = sys.argv[1] if len(sys.argv) > 1 else "/"
    local_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("supernote-backup")

    client = SNClient()
    client.login(os.environ["SUPERNOTE_EMAIL"], os.environ["SUPERNOTE_PASSWORD"])

    for dirpath, _dirs, files in client.walk(remote_root):
        target = local_root / dirpath.lstrip("/")
        target.mkdir(parents=True, exist_ok=True)
        for f in files:
            client.get(f, target)
            print(f"  saved {dirpath.rstrip('/')}/{f.file_name}")

    print(f"Backup complete -> {local_root}")


if __name__ == "__main__":
    main()

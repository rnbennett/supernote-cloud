"""Batch-export every .note file under a folder to PDF.

Usage:
    python examples/export_notes_pdf.py [REMOTE_PATH] [OUTPUT_DIR]

Defaults: REMOTE_PATH="/", OUTPUT_DIR="pdf-export".
Credentials come from SUPERNOTE_EMAIL / SUPERNOTE_PASSWORD.
"""

import os
import sys
from pathlib import Path

from supernote_cloud import SNClient


def main() -> None:
    remote_root = sys.argv[1] if len(sys.argv) > 1 else "/"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("pdf-export")
    out_dir.mkdir(parents=True, exist_ok=True)

    client = SNClient()
    client.login(os.environ["SUPERNOTE_EMAIL"], os.environ["SUPERNOTE_PASSWORD"])

    exported = 0
    for _dirpath, _dirs, files in client.walk(remote_root):
        for f in files:
            if f.file_name.endswith(".note"):
                client.get_pdf(f, out_dir)
                exported += 1
                print(f"  exported {f.file_name}")

    print(f"Done: {exported} note(s) exported to {out_dir}")


if __name__ == "__main__":
    main()

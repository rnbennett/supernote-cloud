"""Folder management demo: create a folder, then move / copy / rename items.

The paths below are illustrative — edit them to match your own Supernote Cloud
layout before running. Credentials come from SUPERNOTE_EMAIL / SUPERNOTE_PASSWORD.

Usage:
    python examples/organize.py
"""

import os

from supernote_cloud import SNClient


def main() -> None:
    client = SNClient()
    client.login(os.environ["SUPERNOTE_EMAIL"], os.environ["SUPERNOTE_PASSWORD"])

    # Create an Archive folder at the root.
    client.mkdir("Archive")

    # Move one note into Archive, copy a template alongside it, then rename
    # the moved note. move()/copy() also accept a list of paths.
    client.move("/Notes/old-meeting.note", "/Archive")
    client.copy("/Notes/template.note", "/Archive")
    client.rename("/Archive/old-meeting.note", "2024-meeting.note")

    print("Reorganized: moved + copied into /Archive, renamed the moved note.")


if __name__ == "__main__":
    main()

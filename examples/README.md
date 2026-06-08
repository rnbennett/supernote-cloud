# Examples

Runnable scripts showing common `supernote-cloud` workflows. Each reads
credentials from the environment:

```bash
export SUPERNOTE_EMAIL=you@example.com
export SUPERNOTE_PASSWORD=...
```

| Script | What it does |
|---|---|
| [`basic_usage.py`](basic_usage.py) | Log in, list the root folder, download the first file |
| [`sync_folder.py`](sync_folder.py) | Back up a whole folder tree locally, preserving structure (via `walk`) |
| [`export_notes_pdf.py`](export_notes_pdf.py) | Batch-export every `.note` under a folder to PDF |
| [`organize.py`](organize.py) | Create a folder, then `move` / `copy` / `rename` items |

Run any of them with, e.g.:

```bash
python examples/sync_folder.py /Notes ./backup
```

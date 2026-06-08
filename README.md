# Supernote Cloud API Client for Python

Unofficial Python API client that allows you to access your Supernote files through the Supernote Cloud.

> This is a maintained continuation of [julianprester/sncloud](https://github.com/julianprester/sncloud), carrying fixes for the Supernote Cloud API. It is published to PyPI as `supernote-cloud` and imported as `supernote_cloud`. Licensed under Apache-2.0; original work © Julian Prester.

`supernote-cloud` makes Supernote Cloud files programmatically accessible, so notes captured on a Supernote device can flow into the applications, automations, and workflows that rely on them. Supernote syncs to several cloud providers, but only Supernote Cloud offers automatic sync — making it the integration point that keeps that data current without manual exports.

The library focuses on the operations teams reach for most — listing, downloading, uploading, and managing files — rather than exhaustively wrapping the service. Need an endpoint it doesn't cover yet? Open an issue or a pull request.

## Core Features

- 🔑 **Login** to the Supernote Cloud
- 🔍 **List** the files and folders for a parent directory
- 💾 **Get** a file and save it locally
- 📄 **Get** a note file and convert it to PDF
- 🖼 **Get** a note file and convert it to PNG
- 🔼 **Put** a file and upload it to the cloud
- 📂 **Make a directory** on the cloud
- 🗑 **Delete** a file or folder
- ✏️ **Rename** a file or folder
- 📦 **Move** files/folders to a new directory
- 📋 **Copy** files/folders to a new directory
- 🔍 **Walk** the directory tree recursively

## Installation

`pip install supernote-cloud`

## Usage

### Python API

```python
from supernote_cloud import SNClient

client = SNClient()
client.login("test@example.com", "1234") # login with email and password
files = client.ls() # returns a list of the files/directories on the Supernote
print(files)
client.get("/Note/notes.note") # downloads the file with the given path
```

### Command Line Interface

The package also provides a command line interface:

```bash
# Login to your Supernote Cloud account
supernote-cloud login

# List files in the root directory
supernote-cloud ls

# List files in a specific directory
supernote-cloud ls /Notes

# Download a file
supernote-cloud get /Notes/document.note

# Download a note as PDF
supernote-cloud get /Notes/document.note --pdf

# Download a note as PNG
supernote-cloud get /Notes/document.note --png

# Download specific pages (works with both PDF and PNG)
supernote-cloud get /Notes/document.note --pdf --pages "1,3,5"

# Set output directory
supernote-cloud get /Notes/document.note --output /path/to/directory

# Create a new folder
supernote-cloud mkdir NewFolder --parent /Notes

# Upload a file
supernote-cloud put /path/to/file.txt --parent /Notes

# Delete a file
supernote-cloud rm /Notes/document.note

# Rename a file or folder
supernote-cloud rename /Notes/old-name.note new-name.note

# Move a file to another directory
supernote-cloud mv /Notes/document.note --destination /Archive

# Move multiple files
supernote-cloud mv /Notes/a.note /Notes/b.note --destination /Archive

# Copy a file to another directory
supernote-cloud cp /Notes/document.note --destination /Backup

# Recursively list all files and folders
supernote-cloud walk
supernote-cloud walk /Notes
```

The CLI will store your access token in `~/.config/supernote-cloud/config.json` and automatically refresh it when needed.

## Roadmap

- [x] CLI / shell commands
- [ ] Example scripts — common workflows (sync a folder, batch-export notes to PDF)
- [ ] Advanced file operations — move, rename, copy, and recursive walk
- [ ] Broader endpoint coverage as use cases come up
- [ ] Docker image — likely only if a sync/daemon mode lands

## Contributing

PRs are welcome. For anything beyond a small fix, open an issue first so we can make sure it fits the direction of the library before you put in the work.

## Acknowledgements

- Original [`sncloud`](https://github.com/julianprester/sncloud) library by [Julian Prester](https://github.com/julianprester), on which this project is based
- General idea for a Supernote Cloud library taken from the amazing [rmapi](https://github.com/juruen/rmapi) project for the reMarkable cloud
- Help to identify API endpoints from [NYT crossword puzzle to Supernote script](https://github.com/bwhitman/supernote-cloud-python)

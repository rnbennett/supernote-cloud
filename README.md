# Supernote Cloud API Client for Python

Unofficial Python API client that allows you to access your Supernote files through the Supernote Cloud.

> This is a maintained continuation of [julianprester/sncloud](https://github.com/julianprester/sncloud), carrying fixes for the Supernote Cloud API. It is published to PyPI as `supernote-cloud` and imported as `supernote_cloud`. Licensed under Apache-2.0; original work © Julian Prester.

`supernote-cloud` is intended for integrating your Supernote Cloud files into other apps. Yes, there are other cloud providers integrated into the Supernote which are easier to develop for, but only the Supernote Cloud offer "auto sync" at the moment. The Supernote APIs are extensive but this library only covers the subset that most developers will need for common filesystem actions such as list, download and upload files.

So while it doesn't currently cover every endpoint (for example you cannot move or rename files) it will likely work for you. That said, PRs are welcome.

## Core Features

- 🔑 **Login** to the Supernote Cloud
- 🔍 **List** the files and folders for a parent directory
- 💾 **Get** a file and save it locally
- 📄 **Get** a note file and convert it to PDF
- 🖼 **Get** a note file and convert it to PNG
- 🔼 **Put** a file and upload it to the cloud
- 📂 **Make a directory** on the cloud
- 🗑 **Delete** a file or folder

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
```

The CLI will store your access token in `~/.config/supernote-cloud/config.json` and automatically refresh it when needed.

## Roadmap

- [x] CLI/SHELL script
- [ ] Example scripts
- [ ] Advanced API calls
- [ ] Get Supernote Cloud API complete
- [ ] Docker container

## Want to contribute?

PRs are welcome. But please open an issue first to see if the proposed feature fits with the direction of this library.

## Acknowledgements

- Original [`sncloud`](https://github.com/julianprester/sncloud) library by [Julian Prester](https://github.com/julianprester), on which this project is based
- General idea for a Supernote Cloud library taken from the amazing [rmapi](https://github.com/juruen/rmapi) project for the reMarkable cloud
- Help to identify API endpoints from [NYT crossword puzzle to Supernote script](https://github.com/bwhitman/supernote-cloud-python)

import click
import json
import os
from pathlib import Path
from typing import Optional

from supernote_cloud.api import SNClient
from supernote_cloud.exceptions import AuthenticationError, ApiError

CONFIG_DIR = Path.home() / ".config" / "supernote-cloud"
CONFIG_PATH = CONFIG_DIR / "config.json"


def load_config():
    """Load configuration from config file."""
    if not CONFIG_PATH.exists():
        return {}
    
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_config(config):
    """Save configuration to config file."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)


def get_client():
    """Get an authenticated SNClient instance."""
    client = SNClient()
    
    config = load_config()
    token = config.get("access_token")
    
    if token:
        client._access_token = token
        # Validate token by making a quick ls call
        try:
            client.ls()
            return client
        except (AuthenticationError, ApiError):
            # Token is invalid or expired
            pass
    
    # Token doesn't exist or is invalid
    click.echo("Authentication required. Please login.")
    return None


def ensure_authenticated(client):
    """Ensure the client is authenticated, prompt for login if not."""
    if not client or not client._access_token:
        email = click.prompt("Email")
        password = click.prompt("Password", hide_input=True)
        
        if not client:
            client = SNClient()
        
        try:
            token = client.login(email, password)
            # Save token
            config = {
                "access_token": token
            }
            save_config(config)
        except AuthenticationError as e:
            click.echo(f"Authentication failed: {str(e)}")
            exit(1)
    
    return client


@click.group()
@click.version_option()
def cli():
    """Supernote Cloud CLI."""
    pass


@cli.command()
def login():
    """Login to Supernote Cloud and save access token."""
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True)

    client = SNClient()
    try:
        token = client.login(email, password)
        save_config({"access_token": token})
        click.echo("Login successful")
        return
    except AuthenticationError as e:
        msg = str(e)
        if not msg.startswith("__E1760__:"):
            click.echo(f"Login failed: {msg}")
            exit(1)
        timestamp = msg.split(":", 1)[1]

    # Identity verification loop — server has a ~120s OTP window.
    # If sms/login returns E1760, the code expired; loop with new timestamp.
    for attempt in range(3):
        click.echo("Verification required. Sending code to your email...")
        try:
            valid_code_key = client.send_verification_code(email, timestamp)
            otp = click.prompt("Enter the 6-digit verification code (enter within 2 minutes)")
            token = client.verify_otp(email, otp, valid_code_key, timestamp)
        except AuthenticationError as ve:
            ve_msg = str(ve)
            if ve_msg.startswith("__E1760__:"):
                timestamp = ve_msg.split(":", 1)[1]
                click.echo("Code expired. Requesting a new one...")
                continue
            click.echo(f"Verification failed: {ve_msg}")
            exit(1)

        save_config({"access_token": token})
        click.echo("Login successful")
        return

    click.echo("Too many failed verification attempts")
    exit(1)


@cli.command()
@click.argument("directory", required=False)
def ls(directory: Optional[str] = None):
    """List files and folders in the specified directory."""
    client = get_client()
    client = ensure_authenticated(client)
    
    try:
        items = client.ls(directory)
        for item in items:
            icon = "📁 " if hasattr(item, "is_folder") and item.is_folder == "Y" else "📄 "
            click.echo(f"{icon}{item.file_name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("file_path")
@click.option("--output", "-o", type=click.Path(), help="Output directory")
@click.option("--pdf", is_flag=True, help="Download as PDF")
@click.option("--png", is_flag=True, help="Download as PNG")
@click.option("--pages", help="Page numbers to include (comma-separated)")
def get(file_path: str, output: Optional[str] = None, pdf: bool = False, 
        png: bool = False, pages: Optional[str] = None):
    """Download a file from Supernote Cloud."""
    client = get_client()
    client = ensure_authenticated(client)
    
    output_path = Path(output) if output else Path(".")
    
    # Parse page numbers if provided
    page_numbers = []
    if pages:
        try:
            page_numbers = [int(p.strip()) for p in pages.split(",")]
        except ValueError:
            click.echo("Error: Pages must be comma-separated integers")
            exit(1)
    
    try:
        if pdf:
            result = client.get_pdf(file_path, output_path, page_numbers)
            click.echo(f"Downloaded PDF to {result}")
        elif png:
            result = client.get_png(file_path, output_path, page_numbers)
            click.echo(f"Downloaded PNG to {result}")
        else:
            result = client.get(file_path, output_path)
            click.echo(f"Downloaded file to {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("folder_name")
@click.option("--parent", "-p", help="Parent directory")
def mkdir(folder_name: str, parent: Optional[str] = None):
    """Create a new folder in Supernote Cloud."""
    client = get_client()
    client = ensure_authenticated(client)
    
    try:
        result = client.mkdir(folder_name, parent)
        click.echo(f"Created folder: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--parent", "-p", help="Parent directory")
def put(file_path: str, parent: Optional[str] = None):
    """Upload a file to Supernote Cloud."""
    client = get_client()
    client = ensure_authenticated(client)
    
    try:
        result = client.put(Path(file_path), parent)
        click.echo(f"Uploaded file: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("file_path")
@click.argument("new_name")
def rename(file_path: str, new_name: str):
    """Rename a file or folder on Supernote Cloud."""
    client = get_client()
    client = ensure_authenticated(client)

    try:
        result = client.rename(file_path, new_name)
        click.echo(f"Renamed to: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("file_path", nargs=-1, required=True)
@click.option("--destination", "-d", required=True, help="Destination directory")
def mv(file_path, destination: str):
    """Move one or more files/folders to a destination directory."""
    client = get_client()
    client = ensure_authenticated(client)

    try:
        items = list(file_path)
        result = client.move(items if len(items) > 1 else items[0], destination)
        click.echo(f"Moved: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("file_path", nargs=-1, required=True)
@click.option("--destination", "-d", required=True, help="Destination directory")
def cp(file_path, destination: str):
    """Copy one or more files/folders to a destination directory."""
    client = get_client()
    client = ensure_authenticated(client)

    try:
        items = list(file_path)
        result = client.copy(items if len(items) > 1 else items[0], destination)
        click.echo(f"Copied: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("directory", required=False)
def walk(directory: Optional[str] = None):
    """Recursively list all files and folders."""
    client = get_client()
    client = ensure_authenticated(client)

    try:
        for dirpath, dirs, files in client.walk(directory):
            click.echo(f"\n{dirpath}")
            for d in dirs:
                click.echo(f"  📁 {d.file_name}")
            for f in files:
                click.echo(f"  📄 {f.file_name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(), nargs=-1)
def rm(file_path):
    """Delete a file from Supernote Cloud."""
    client = get_client()
    client = ensure_authenticated(client)
    
    try:
        result = client.delete(list(file_path))
        click.echo(f"Deleted file: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    cli()
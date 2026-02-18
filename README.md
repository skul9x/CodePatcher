# TCO Patch Applier v3.1 - Vietnamese Edition

**TCO Patch Applier** is a specialized tool designed to help users manage code patches and synchronize with GitHub repositories efficiently and securely.

## Features

- **Git Integration**:
  - **Auto Sync**: Pull, Merge, and Push code changes with a single click.
  - **Branch Management**: Create, switch, and delete remote branches.
  - **Rollback**: Quickly revert the last push if something goes wrong.
  - **Smart Ignore**: Automatically manages `.gitignore` to prevent sensitive or temporary files (like `__pycache__`) from being leaked.

- **Security**:
  - **Token Encryption**: GitHub tokens are encrypted before storage.
  - **Path Safety**: Prevents unauthorized file access via directory traversal checks.

- **User Interface**:
  - Modern GUI built with Python (PyQt/PySide implied).
  - Dedicated tabs for different functionalities (GitHub, Patching).
  - Vietnamese language support.

## Installation

1.  Ensure you have Python installed.
2.  Install dependencies (if a `requirements.txt` is present, run `pip install -r requirements.txt`).
    - *Note: This project likely requires `GitPython` and a UI library like `PyQt6` or `PySide6`.*
3.  Run the application:
    ```bash
    python -m app.main  # or whichever entry point is defined
    ```

## Usage

1.  **GitHub Tab**:
    - Enter your GitHub Token (it will be encrypted).
    - Connect to your repository.
    - Use the "Pull & Merge & Push" button to sync your local code with the remote.
    - Manage branches using the dropdown and action buttons.

2.  **Patching** (Implied):
    - The tool listens for patch formats (regex defined in `constants.py`) to apply code changes safely.

## Project Structure

See [structure.md](structure.md) for a detailed breakdown of the codebase.

# Project Structure

This document outlines the file structure of the **TCO Patch Applier** application.

## Directory Tree

```
app/
├── constants.py       # Global constants and configuration (App title, fonts, regex)
├── git_core.py        # GitManager class for handling Git operations (Pull, Push, Merge, Rollback)
├── styles.py          # UI styling definitions
├── utils.py           # Utility functions (Token encryption, path safety check, syntax check)
├── __init__.py        # Package initialization
└── ui/                # User Interface components
    ├── __init__.py
    ├── dialogs.py     # Custom dialog classes
    ├── github_tab.py  # GitHub integration tab UI and logic
    └── main_window.py # Main application window setup
```

## Key Files Description

- **`git_core.py`**: The core logic for interacting with Git. It handles authentication, remote management, and safe execution of git commands including the custom `_ensure_gitignore` logic.
- **`ui/main_window.py`**: The entry point for the GUI, assembling different tabs and components.
- **`ui/github_tab.py`**: Contains the specific logic for the GitHub management interface, allowing users to sync code, switch branches, and manage tokens.
- **`utils.py`**: Provides security helpers like `TokenCipher` for encrypting sensitive data and `is_safe_path` to prevent directory traversal attacks.

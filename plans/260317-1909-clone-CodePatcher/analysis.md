# CodePatcher Analysis

- **Source Project**: `/home/skul9x/Desktop/Test_code/CodePatcher-main`
- **Target Project**: `/home/skul9x/Desktop/Test_code/CodePatcher-Go`
- **Backend Target**: Go (Wails v2)
- **Frontend Target**: React/Vite (đề xuất cho Wails v2 vì hệ sinh thái phong phú và dễ làm UI phức tạp như TreeView).

## Original Stack
- **Language**: Python 3
- **GUI Framework**: PySide6 (Qt)
- **Architecture**: Monolithic Desktop App (MVC-like with UI and Core logic separated)
- **Dependencies**: `GitPython` (implicit from git_core.py), `PySide6`

## Core Modules Detected
- `app/main.py`: Entry point, setup theme.
- `app/ui/main_window.py`: Window layout, Code Patcher tab (Splitter with Input/Preview and History).
- `app/ui/github_tab.py`: GitHub Sync tab.
- `app/git_core.py`: Git operations (Pull, Merge, Push, Branch management).
- `app/utils.py`: Security (is_safe_path, TokenCipher), Syntax checking.
- `app/constants.py`: Regex patterns, Themes, Configs.

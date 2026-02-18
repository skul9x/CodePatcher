from app.constants import APP_FONT_FAMILY, APP_FONT_SIZE

# --- NORD PALETTE CONSTANTS ---
NORD0 = "#2E3440"  # Polar Night 0 (Main BG)
NORD1 = "#3B4252"  # Polar Night 1 (Surface)
NORD2 = "#434C5E"  # Polar Night 2 (Surface Highlight)
NORD3 = "#4C566A"  # Polar Night 3 (Border Muted)
NORD4 = "#D8DEE9"  # Snow Storm 0 (Muted Text)
NORD5 = "#E5E9F0"  # Snow Storm 1
NORD6 = "#ECEFF4"  # Snow Storm 2 (Primary Text)
NORD7 = "#8FBCBB"  # Frost 0
NORD8 = "#88C0D0"  # Frost 1 (Neon Cyan Accent)
NORD9 = "#81A1C1"  # Frost 2
NORD10 = "#5E81AC" # Frost 3
NORD11 = "#BF616A" # Aurora 0 (Danger Red)
NORD12 = "#D08770" # Aurora 1
NORD13 = "#EBCB8B" # Aurora 2 (Warning Yellow)
NORD14 = "#A3BE8C" # Aurora 3 (Success Green)
NORD15 = "#B48EAD" # Aurora 4 (Neon Purple Accent)

HEADER_FONT_SIZE = APP_FONT_SIZE + 4

DARK_STYLESHEET = f"""
    /* --- GLOBAL RESET --- */
    * {{
        font-family: "{APP_FONT_FAMILY}";
        font-size: {APP_FONT_SIZE}pt;
        color: {NORD6};
        outline: none;
    }}

    /* --- WINDOW & CONTAINER --- */
    QMainWindow, QDialog, QTabWidget::pane {{
        background-color: {NORD0};
        border: none;
    }}

    /* --- SIDEBAR CUSTOM STYLES --- */
    QFrame#Sidebar {{
        background-color: {NORD1};
        border-right: 1px solid {NORD3};
        min-width: 200px;
    }}

    QPushButton#SidebarBtn {{
        background-color: transparent;
        border: none;
        border-left: 4px solid transparent;
        padding: 12px 20px;
        text-align: left;
        font-weight: 500;
        color: {NORD4};
    }}

    QPushButton#SidebarBtn:hover {{
        background-color: {NORD2};
        color: {NORD6};
    }}

    QPushButton#SidebarBtn[active="true"] {{
        background-color: {NORD2};
        color: {NORD8};
        border-left: 4px solid {NORD8};
        font-weight: bold;
    }}

    /* --- CARDS & PANELS --- */
    QFrame#Card {{
        background-color: {NORD1};
        border: 1px solid {NORD3};
        border-radius: 4px;
    }}

    /* --- TYPOGRAPHY --- */
    QLabel {{
        background: transparent;
    }}
    
    QLabel#HeaderLabel {{
        font-size: {HEADER_FONT_SIZE}pt;
        font-weight: bold;
        color: {NORD8};
        padding-bottom: 4px;
        letter-spacing: 1px;
    }}

    QLabel#SubHeader {{
        font-size: {APP_FONT_SIZE}pt;
        font-weight: bold;
        color: {NORD6};
    }}

    /* --- INPUTS --- */
    QLineEdit, QPlainTextEdit, QTextEdit, QComboBox {{
        background-color: {NORD0};
        border: 1px solid {NORD3};
        border-radius: 2px;
        padding: 8px 12px;
        color: {NORD6};
        selection-background-color: {NORD10};
    }}
    
    QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 1px solid {NORD8};
    }}
    
    /* --- LISTS & TREES --- */
    QTreeWidget, QListWidget {{
        background-color: {NORD0};
        border: 1px solid {NORD3};
        border-radius: 2px;
        padding: 4px;
    }}
    
    QHeaderView::section {{
        background-color: {NORD1};
        color: {NORD8};
        padding: 8px;
        border: none;
        border-bottom: 2px solid {NORD3};
        font-weight: bold;
    }}

    /* --- BUTTONS --- */
    QPushButton {{
        background-color: {NORD3};
        border: none;
        border-radius: 2px;
        padding: 8px 16px;
        font-weight: 600;
        min-height: 32px;
    }}

    QPushButton:hover {{
        background-color: {NORD2};
    }}

    QPushButton:pressed {{
        background-color: {NORD1};
    }}
    
    QPushButton:disabled {{
        background-color: {NORD1};
        color: {NORD3};
    }}

    /* Primary Accent (Cyan) */
    QPushButton[class="PrimaryButton"] {{
        background-color: {NORD8};
        color: {NORD0};
    }}
    QPushButton[class="PrimaryButton"]:hover {{
        background-color: {NORD7};
    }}

    /* Secondary Accent (Purple) */
    QPushButton[class="SecondaryButton"] {{
        background-color: {NORD15};
        color: {NORD0};
    }}

    /* Danger (Red) */
    QPushButton[class="DangerButton"] {{
        background-color: {NORD11};
        color: {NORD6};
    }}

    /* --- SCROLLBARS --- */
    QScrollBar:vertical {{
        background: {NORD0};
        width: 10px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: {NORD3};
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    /* --- MISC --- */
    QProgressBar {{
        border: 1px solid {NORD3};
        border-radius: 2px;
        text-align: center;
        background-color: {NORD0};
    }}
    QProgressBar::chunk {{
        background-color: {NORD8};
    }}
"""
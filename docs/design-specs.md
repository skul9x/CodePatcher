# Design Specifications: CyberNord Theme

## 🎨 Color Palette (Nord + Cyberpunk)

| Name | Hex | Usage |
|------|-----|-------|
| **Background** | `#2E3440` | Main Window Background (Nord Polarnight 0) |
| **Surface** | `#3B4252` | Cards, Sidebar, Inputs (Nord Polarnight 1) |
| **Surface Highlight** | `#434C5E` | Hover states, Active rows (Nord Polarnight 2) |
| **Border Muted** | `#4C566A` | Inactive borders, dividers (Nord Polarnight 3) |
| **Primary/Neon** | `#88C0D0` | **Main Accent** (Cyan), Active states, Glowing borders (Nord Frost 2) |
| **Secondary/Neon** | `#B48EAD` | **Secondary Accent** (Purple), Special actions (Nord Aurora 5) |
| **Success** | `#A3BE8C` | Success messages, 'Safe' status (Nord Aurora 4) |
| **Danger** | `#BF616A` | Error messages, Delete actions (Nord Aurora 1) |
| **Warning** | `#EBCB8B` | Warning messages (Nord Aurora 3) |
| **Text Primary** | `#ECEFF4` | Main text (Nord Snow Storm 2) |
| **Text Secondary** | `#D8DEE9` | Muted text, placeholders (Nord Snow Storm 0) |

## 📝 Typography

*   **Font Family (UI):** `Inter` or `Segoe UI` (System default, providing clean readability).
*   **Font Family (Code/Logs):** `JetBrains Mono`, `Fira Code`, or `Consolas` (Monospace is critical for the "Hacker" vibe).

| Element | Size | Weight | Color | Style |
|---------|------|--------|-------|-------|
| **H1 (Page Title)** | 24px | Bold (700) | `#88C0D0` | Uppercase, Letter-spacing +1px |
| **H2 (Section Header)**| 18px | SemiBold (600)| `#ECEFF4` | |
| **Body** | 14px | Regular (400)| `#ECEFF4` | |
| **Label/Muted** | 12px | Regular (400)| `#D8DEE9` | |
| **Code/Terminal** | 13px | Medium (500) | `#E5E9F0` | Monospace |

## 📐 Layout & Spacing

*   **Navigation:** Left Sidebar (Width: 240px). Fixed position.
    *   *Why?* Clears up vertical space for code/logs and follows "Pro App" standard.
*   **Content Area:** Card-based layout with "Tech" borders.
*   **Spacing scale:**
    *   `xs`: 4px
    *   `sm`: 8px
    *   `md`: 16px
    *   `lg`: 24px

## 🔲 Shape & Effects (The "Cyber" Feel)

*   **Corner Radius:** `2px` or `4px` (Sharp, avoiding the "bubbly" mobile look).
*   **Borders:** Thin (`1px`), crisp.
*   **Active States:**
    *   Input Focus: `1px solid #88C0D0` + `box-shadow: 0 0 8px rgba(136, 192, 208, 0.4)` (Neon Glow).
    *   Button Hover: Brightness + 10%, slight translation up (`-1px`).
*   **Glassmorphism:** Subtle use on the Sidebar background (`opacity: 0.95`).

## 🖼️ Component Specs

### Buttons
*   **Primary Button (Cyan):**
    *   Bg: `#88C0D0` (Gradient to `#81A1C1` optional)
    *   Text: `#2E3440` (Dark text on bright bg for contrast)
    *   Border: None
    *   Font-weight: Bold
*   **Secondary Button (Outline):**
    *   Bg: Transparent
    *   Border: `1px solid #88C0D0`
    *   Text: `#88C0D0`

### Input Fields
*   Background: `#2E3440` (Darker than surface)
*   Border: `1px solid #4C566A`
*   Padding: `8px 12px`
*   Font: Monospace for paths/tokens/code.

### Cards (Containers)
*   Background: `#3B4252`
*   Border: `1px solid #4C566A`
*   Box Shadow: `0 4px 6px rgba(0,0,0,0.3)`

### Sidebar
*   Background: `#2E3440`
*   Item Height: `40px`
*   **Active Item:**
    *   Bg: `rgba(136, 192, 208, 0.1)` (10% Cyan)
    *   Left Border: `3px solid #88C0D0`
    *   Text: `#88C0D0`

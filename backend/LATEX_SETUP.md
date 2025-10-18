# LaTeX Setup for Manim

## The Issue
Manim uses LaTeX to render mathematical expressions (MathTex, Tex, Matrix objects). If LaTeX is not installed on your system, these will fail.

## Quick Fix: Avoid LaTeX When Possible
The system is now configured to prefer `Text()` and `MarkupText()` objects which don't require LaTeX. For simple math, use Unicode symbols: ² ³ α β γ δ ∑ ∫ √ ± × ÷ ≠ ≤ ≥

## Installing LaTeX (if needed for complex math)

### macOS
```bash
# Option 1: Install MacTeX (large, ~4GB)
brew install --cask mactex

# Option 2: Install BasicTeX (smaller, ~100MB)
brew install --cask basictex
# Then install required packages:
sudo tlmgr update --self
sudo tlmgr install standalone preview doublestroke ms setspace rsfs relsize ragged2e fundus-calligra microtype wasysym physics dvisvgm jknapltx wasy cm-super
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science texlive-fonts-extra dvisvgm
```

### Windows
1. Download and install MiKTeX from https://miktex.org/download
2. During installation, choose "Always install missing packages on-the-fly"
3. Install dvisvgm separately if needed

## Verify Installation
```bash
# Check if LaTeX is installed
latex --version

# Check if dvisvgm is installed (required by Manim)
dvisvgm --version
```

## Current Configuration
The system is configured in `manim.cfg` to:
- Use Pango text renderer for Text() objects (no LaTeX needed)
- Automatically find LaTeX binaries when needed
- Provide helpful error messages when LaTeX is missing

## For Development
If you don't need complex mathematical expressions, you can avoid installing LaTeX entirely by:
1. Using `Text()` instead of `MathTex()` or `Tex()`
2. Using Unicode math symbols instead of LaTeX notation
3. Using `MarkupText()` for styled text

The AI prompt has been updated to prefer non-LaTeX options whenever possible.


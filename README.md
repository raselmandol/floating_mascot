# floating-mascot

![GUI Preview](https://raw.githubusercontent.com/raselmandol/floating_mascot/refs/heads/main/assets/floating_mascot.gif)


`floating_mascot` is a simple floating character mascot application for your desktop, made with PyQt6. It supports animated GIFs/images, 3D models(.glb), and some extendable built-in animations like bouncing balls and snakes. You can also add your own custom character or animation.


---

[![GitHub release](https://img.shields.io/github/v/release/raselmandol/floating_mascot)](#) [![GitHub release date](https://img.shields.io/github/release-date/raselmandol/floating_mascot)](#) [![GitHub last commit](https://img.shields.io/github/last-commit/raselmandol/floating_mascot)](#)


## Features

- Load and display a **GIF** or **PNG** character.
- Make the mascot draggable around your desktop.
- Transparent background (no window frame).
- Built-in full-screen animations (bouncing balls, snake, twinkling stars).
- Simple settings window.


---

## Screenshots

![GUI Preview](https://raw.githubusercontent.com/raselmandol/floating_mascot/refs/heads/main/assets/screenshot_1.png)

![GUI Preview](https://raw.githubusercontent.com/raselmandol/floating_mascot/refs/heads/main/assets/screenshot_2.png)

---

## Installation

Follow these steps to set up the project:

### Clone the Repository

```bash
git clone https://github.com/raselmandol/floating_mascot.git
cd floating_mascot
```

## Virtual Environment Setup

Create and activate a virtual environment called `mascot`:

### Windows

```bash
python -m venv mascot
mascot\Scripts\activate
```

---

##  Install Dependencies

After activating the virtual environment:

```bash
pip install -r requirements.txt
```

---
## Usage

Make sure you're in the project folder, then run:

```bash
python main.py
```

---


##  Requirements

- Python 3.9+
- PyQt6
- PyOpenGL
- Pillow (for GIF/image handling)

---

##  Build Executable (Windows)

if you want to create an `.exe`:

### Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

> **Note:** Already added in `requirements.txt`. (If you want to ignore it, make sure to remove it from `requirements.txt`.)


Convert your PNG icon to ICO.

### Run:
   ```bash
   pyinstaller --name mascot-launcher --onefile --windowed --icon=icon.ico main.py
   ```

---

## Keyboard Shortcut

You can **toggle the floating mascot** (hide/show), and **toggle background music** (pause/unpause) using the keyboard shortcut:

Floating mascot:
```
Ctrl + Alt + M
```
Background music:
```
Ctrl + Alt + S
```


This makes it easy to hide the window when you're working, bring it back anytime, and pause/unpause the audio anytime.

### Requirements

Make sure you have the `keyboard` module installed:

```bash
pip install -r requirements.txt
```
(already added -> requirements.txt)

> Note: The `keyboard` module may require administrator/root permissions on some systems.

### Change the Shortcut

To use a different shortcut, open `floating_window.py` and find this line:

```python
keyboard.add_hotkey('ctrl+alt+m', self.toggle_visibility)
```
Change `'ctrl+alt+m'` to any other key combination, like `'ctrl+shift+z'` or `'f12'`.

To use a different shortcut (music), open `settings_window.py` and find this line:

```python
keyboard.add_hotkey('ctrl+alt+s', self._toggle_music)
```

Change `'ctrl+alt+s'` to any other key combination, like `'ctrl+shift+z'` or `'f12'`.

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.

---

## To-Do

- [ ]  Enhance error handling  
- [ ]  Improve documentation with more examples  
- [ ]  Add more configuration options  
- [ ]  Minimize to system tray  
- [ ]  Include more default animations  
- [ ]  Add proper 3D model support  
- [ ]  Load from URL  
- [ ]  Add autostart on system startup  
- [x]  Implement proper drag functionality  
- [ ]  Create animation builder/editor  
- [x]  Draggable Label
- [x]  Keyboard Shortcuts
- [x]  Background Music 
- [ ]  Multiple GIFs option
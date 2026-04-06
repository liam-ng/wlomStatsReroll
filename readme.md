# Wonderland Online Mobile Stats Reroll

A simple script to reroll pet's reincarnated stats until getting the desired value.
Uses Tesseract OCR to read the game screen and extract the value gain in (+##) pattern.


>[!Warning] AI code generation is used to create this application.
> Use at your own risk.

# Install

Only tested in Windows 11:
1. Download the `Wlom Stats Reroll.exe` from release page.
2. Open the `Wlom Stats Reroll.exe`.

Note: it will populate a `wlo_config.json` at your exe path after launch. The `wlo_config.json` will store the last used coordinates.

# How to Use

1. Click `Set 'Redistribute' Location` on stat roller.
2. Click the Redistribute button in game.
3. Click `Set 'Bonus' Area` on stat roller.
4. Click on the top left of one of stat you want the script to watch, say CON.
5. Click on the bottom right of the same stat you picked.
6. Set `Target Gain` to desired value.
7. Set `Interval` to speed up or down if your system allowed.
8. Make sure the game window is at the top and values are visible.
9. Press F9 to start/stop.


## Build
pip install pyinstaller
pyinstaller --onefile --windowed --add-binary "C:/Program Files/Tesseract-OCR;Tesseract-OCR" main.py
# Wonderland Online Mobile Stats Reroll (飄流幻境M 夥伴轉生自動亂數分配)

A simple script to reroll pet's reincarnated stats until getting the desired value.

Uses Tesseract OCR to read the in-game screen and extract the value gain in (+##) pattern.

<img alt="{3A8B4DA5-1965-455B-9E25-546A55362A1C}" src="https://github.com/user-attachments/assets/42ed8aa1-34cb-46a8-a7ea-1f4342bcace9" style="width:20%; height:auto;" />

# Install

Only tested in Windows 11.

## Lite Version
1. Download and Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki). Additional [guide](https://docs.coro.net/featured/agent/install-tesseract-windows) on Tesseract installation.
2. Download the `Wlom Stats Reroll Lite.exe` from the release page.
3. Run the `Wlom Stats Reroll Lite.exe`.

## All-in-one Bundled Version
1. Download the `WLOM Stats Reroller Bundled.zip` from available link(s) in release page.
2. Extract and Open the `WLOM Stats Reroller Bundled.exe`.

Note: it will populate a `wlo_config.json` at your exe path after launch. The `wlo_config.json` stores the last used coordinates.

# How to Use

1. Click `Set 'Redistribute' Location` on stat roller.
2. Click the Redistribute button in game.
3. Click `Set 'Bonus' Area` on stat roller.
4. Click on the top left of one of stat you want the script to watch, say CON.
5. Click on the bottom right of the same stat you picked.
6. Set `Target Gain` to desired value.
7. Set `Interval` to speed up or down if your system allowed.

   Note: do not set `Interval` too low or it might skip.
9. Make sure the game window is at the top and values are visible.
10. Press F9 to start/stop.

<img style="width:80%; height:auto;" alt="image" src="https://github.com/user-attachments/assets/5423050a-9e59-466a-9503-4ee95ab21b1b" />

# 使用教學

1. 點擊洗點工具上的 Set 'Redistribute' Location。
2. 到遊戲畫面中，點擊一次 「亂數分配」 按鈕所在位置。
3. 點擊洗點工具上的 Set 'Bonus' Area。
4. 點擊你想監控的屬性（例如：CON）紅字部分的左上角。
5. 接著點擊同一屬性紅字部分的右下角（框選出紅字區域）。
6. 在 Target Gain（目標數值）欄位輸入你想要的目標值（例如：90）。
7. 根據順暢度調整 Interval（間隔時間）來加快或減慢速度。
8. 確保遊戲視窗位於最上層，且屬性數值清晰可見。
9. 按下 F9 鍵即可開始或停止自動執行。

## VirusTotal
[VirusTotal](https://www.virustotal.com/gui/file/c50c66d2c35efa33b2ff0a3ce1ae6d7beac355a52091ca727737c4b1c1541cf1/detection) 

Use at your own risk. In case your security software flag the exe as malicious, I recommend AGAINST executing the exe. 

If you have the technical know-how, follow `Run as a Script` instead. 

<img style="width:40%; height:auto;" alt="{14A01915-283E-4E03-BDA8-3E04C2AD3B0A}" src="https://github.com/user-attachments/assets/22eea89c-1c3f-42a4-bb8d-b2b75106215d" />

# Run as a Script
```
python venv .venv-wlom
./.venv-wlom/Scripts/Activate.ps1

python -m pip install -r requirements.txt

# You need to manually install Tesseract in your system for the script to work
# You may find prebuilt .exe from Coro doc

python main.py
```

# Build
```
pip install pyinstaller

# Lite
pyinstaller --onefile --windowed main.py

# All-in-one
pyinstaller --onefile --windowed --add-binary "C:/Program Files/Tesseract-OCR;Tesseract-OCR" main.py
```

# Disclaimer

This tool is for educational purposes only. The author is not responsible for any consequences resulting from the use of this software, including game bans or data loss. Use of third-party automation is a violation of most game's terms of service. Use at your own discretion.

Use at your own risk. 

Use at your own risk. 

Use at your own risk. 

AI code generation is used to create this application. This software is provided "as is" and "with all faults," without any warranty of any kind, express or implied. The developers make no representations or warranties regarding the accuracy, reliability, or completeness of the application.

The use of automation tools may violate the Terms of Service (ToS) of "Wonderland Online Mobile" or its related platforms. By using this software, you acknowledge that you are doing so at your own risk. This includes, but is not limited to, the risk of game account suspension, permanent bans, or loss of in-game data.

In no event shall the developers or contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, account bans, software conflicts, or system failures) however caused and on any theory of liability, whether in contract, strict liability, or tort arising in any way out of the use of this software.

This application is an independent third-party tool and is not affiliated with, authorized, maintained, sponsored, or endorsed by the official game developers or publishers of Wonderland Online Mobile.

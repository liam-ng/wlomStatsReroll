import keyboard
import mouse
import json
import os
import time
import tkinter as tk
from tkinter import messagebox
import threading
import re

import pyautogui
import pytesseract
from PIL import Image
import hashlib

# Require Tesseract OCR to be installed in your system
# Require Tesseract OCR to be installed in your system
# Require Tesseract OCR to be installed in your system

# Configuration file name
CONFIG_FILE = "wlo_config.json"

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WLOM Stats Roller Lite v1.1.0")
        self.root.geometry("320x480")
        self.root.attributes("-topmost", True)

        self.is_running = False
        
        # --- Default Coordinates ---
        self.redist_pos = (2111, 1085)
        self.con_region = (1987, 1145, 254, 38)
        
        # --- UI Elements ---
        # Dynamic Instruction Label
        self.instr_label = tk.Label(root, text="", 
                                    font=("Arial", 11, "bold"), fg="black", wraplength=300)
        self.instr_label.pack(pady=5)
        
        # Step 1: Setup Coordinates
        tk.Label(root, text="Step 1: Setup Coordinates", font=("Arial", 10, "bold")).pack(pady=1)

        self.btn_pos_label = tk.Label(root, text=f"Button: {self.redist_pos}", fg="green")
        self.btn_pos_label.pack()
        tk.Button(root, text="Set 'Redistribute' Location", command=self.select_button).pack(pady=2)

        self.region_pos_label = tk.Label(root, text=f"Region: {self.con_region[2]}x{self.con_region[3]} set", fg="green")
        self.region_pos_label.pack()
        tk.Button(root, text="Set Stat Bonus Area", command=self.select_region).pack(pady=2)

        # Step 2: Set Target Gain (+XX)
        tk.Label(root, text="", font=("Arial", 6)).pack()
        tk.Label(root, text="Step 2. Set Target Gain (+XX)", font=("Arial", 10, "bold")).pack(pady=2)
        tk.Label(root, text="Target Gain:", font=("Arial", 10, "bold")).pack(pady=1)
        self.target_entry = tk.Entry(root, justify='center', font=("Arial", 12))
        self.target_entry.insert(0, "90")
        self.target_entry.pack(pady=5)

        # Step 3: Start Script by pressing F9
        tk.Label(root, text="", font=("Arial", 6)).pack()
        tk.Label(root, text="Step 3. Start Script by pressing F9", font=("Arial", 10, "bold")).pack(pady=1)
        self.status_label = tk.Label(root, text="Status: IDLE (Press F9)", fg="gray")
        self.status_label.pack(pady=2)
        tk.Label(root, text="Interval (in seconds):", font=("Arial", 10, "bold")).pack(pady=1)
        self.interval_entry = tk.Entry(root, justify='center', font=("Arial", 12))
        self.interval_entry.insert(0, "0.2")
        self.interval_entry.pack(pady=5)

        # Start Script Button
        tk.Label(root, text="", font=("Arial", 6)).pack()
        self.start_btn = tk.Button(root, text="START SCRIPT", command=self.toggle_script, bg="#4CAF50", fg="white", font=("Arial", 10,"bold"), width=20)
        self.start_btn.pack(pady=5)

        # Load saved data on startup
        self.load_config()

        keyboard.add_hotkey('F9', self.toggle_script)

    def update_instr(self, msg, color="blue"):
        self.instr_label.config(text=msg, fg=color)
        self.root.update()

    def save_config(self):
        data = {
            "redist_pos": self.redist_pos,
            "con_region": self.con_region
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    saved_btn = data.get("redist_pos")
                    saved_reg = data.get("con_region")
                    
                    if saved_btn:
                        self.redist_pos = saved_btn
                        self.btn_pos_label.config(text=f"Button: {self.redist_pos}", fg="green")
                    if saved_reg:
                        self.con_region = saved_reg
                        self.region_pos_label.config(text=f"Region: {self.con_region[2]}x{self.con_region[3]} loaded", fg="green")
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def select_button(self):
        self.update_instr("ACTION: Left-Click the 'Redistribute' button...", "orange")
        x, y = self.get_click_location()
        self.update_instr("", "black")
        self.redist_pos = (x, y)
        self.btn_pos_label.config(text=f"Button: {x}, {y}", fg="green")
        self.save_config()

    def select_region(self):
        self.update_instr("ACTION: Left-Click TOP-LEFT of stat row...", "orange")
        x1, y1 = self.get_click_location()
        pyautogui.sleep(0.3) 
        self.update_instr("ACTION: Left-Click BOTTOM-RIGHT of stat row...", "orange")
        x2, y2 = self.get_click_location()
        self.update_instr("", "black")
        
        width, height = abs(x2 - x1), abs(y2 - y1)
        self.con_region = (min(x1, x2), min(y1, y2), width, height)
        self.region_pos_label.config(text=f"Region: {width}x{height} at {x1},{y1} set", fg="green")
        self.save_config()

    def get_click_location(self):
        while not mouse.is_pressed(button='left'):
            pyautogui.sleep(0.01)
        pos = pyautogui.position()
        while mouse.is_pressed(button='left'): 
            pyautogui.sleep(0.01)
        return pos.x, pos.y

    def get_con_value(self):
        if not self.con_region: return 0

        screenshot = pyautogui.screenshot(region=self.con_region)
        screenshot = screenshot.resize((screenshot.width * 4, screenshot.height * 4), Image.LANCZOS)

        text = pytesseract.image_to_string(screenshot, config='--psm 6 -c tessedit_char_whitelist=0123456789+')
        matches = re.findall(r'\+(\d{1,3})', text)

        if matches:
            stat_values = [int(m) for m in matches]
            
            self.status_label.config(text=f"Last Read: +{stat_values}", fg="blue")
            
            return max(stat_values)
        return 0

    
    def wait_for_pixel_change(self, region, timeout=1.5):
        """
        Captures a small snapshot and waits for the pixels to differ 
        from the initial state.
        """
        initial_img = pyautogui.screenshot(region=region)
        initial_hash = hashlib.md5(initial_img.tobytes()).hexdigest()
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.is_running:
                return False
                
            current_img = pyautogui.screenshot(region=region)
            current_hash = hashlib.md5(current_img.tobytes()).hexdigest()
            
            if current_hash != initial_hash:
                self.update_instr("Update detected, reading stats...", "green")
                time.sleep(0.05) 
                return True
                
            self.update_instr("Warning: No value changes detected!", "orange")
            time.sleep(0.02) 
        return False # Timeout
    
    def validate_int(self, input):
        if input.isdigit() and int(input) > 0:
            self.update_instr("")
            return True
        self.update_instr("Invalid Target: Must be a positive integer!", "red")
        return False
    
    def validate_float(self, input):
        if input.replace('.', '', 1).isdigit() and float(input) > 0:
            self.update_instr("")
            return True
        self.update_instr("Invalid Interval: Must be a positive number!", "red")
        return False
    
    def run_loop(self):
        try:
            target = int(self.target_entry.get())
            inter = float(self.interval_entry.get())
        except ValueError:
            self.update_instr("ERROR: Invalid Target!", "red")
            self.is_running = False
            return

        while self.is_running:
            pyautogui.click(self.redist_pos)
            # Wait for the pixel to change (Pixel-Hash Wait)
            if not self.wait_for_pixel_change(self.con_region):
                continue
                
            val = self.get_con_value()

            if val >= target:
                self.is_running = False
                self.status_label.config(text=f"TARGET REACHED! {val}", fg="green")
                messagebox.showinfo("Success", f"Target met! Found +{val}")
                break
            # else:
            #     pyautogui.click(self.redist_pos)
            
            pyautogui.sleep(inter)

    def toggle_script(self):
        if not self.is_running:
            if not self.validate_int(self.target_entry.get()):
                return
            if not self.validate_float(self.interval_entry.get()):
                return
            self.is_running = True
            self.status_label.config(text="Status: RUNNING...", fg="red")
            self.start_btn.config(text="STOP (F9)", bg="#f44336")
            threading.Thread(target=self.run_loop, daemon=True).start()
        else:
            self.is_running = False
            self.status_label.config(text="Status: STOPPED", fg="gray")
            self.start_btn.config(text="START SCRIPT (F9)", bg="#4CAF50")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()
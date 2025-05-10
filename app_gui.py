import tkinter as tk
import subprocess
import sys
from tkinter import messagebox


def start_eye_controlled_mouse():
    try:
        # Run main.py
        subprocess.Popen([sys.executable, 'main.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the eye controlled mouse: {e}")

# Root window 
root = tk.Tk()


root.title("EyeMote")

root.geometry('400x400')

# Create a Canvas
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# scrollbar
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a frame to hold the content
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

# Configuring the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# update scrollbar and frame size
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Grid layout for frame 
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)


lbl_welcome = tk.Label(frame, text="Welcome to EyeMote!", font=("Helvetica", 16, 'bold'))
lbl_welcome.grid(row=0, column=0, pady=(10, 10), sticky="n")

# Description label
lbl_description = tk.Label(frame, text="Unlock a new way to interact with your computer using just your eyes!", wraplength=300, justify="center")
lbl_description.grid(row=1, column=0, pady=(0, 20), sticky="n")


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


root.mainloop()

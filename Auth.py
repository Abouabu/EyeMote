import customtkinter as ctk
from tkinter import messagebox
import json
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class EyeMouseLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("EyeMouse - Login")
        self.root.geometry("400x300")
        
        # Create data directory if not exists
        self.data_file = 'users.json'
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({}, f)

        # Create frames
        self.login_frame = ctk.CTkFrame(self.root)
        self.register_frame = ctk.CTkFrame(self.root)

        self.show_login_frame()

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Login widgets
        ctk.CTkLabel(self.login_frame, text="EyeMouse Login", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.login_user_entry = ctk.CTkEntry(self.login_frame, 
                                           placeholder_text="Username")
        self.login_user_entry.pack(pady=5)

        self.login_pass_entry = ctk.CTkEntry(self.login_frame, 
                                           show="*", placeholder_text="Password")
        self.login_pass_entry.pack(pady=5)

        ctk.CTkButton(self.login_frame, text="Login", command=self.login).pack(pady=20)

        ctk.CTkButton(self.login_frame, text="Create New Account", 
                     command=self.show_register_frame, fg_color="transparent").pack()

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Registration widgets
        ctk.CTkLabel(self.register_frame, text="Create New Account", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        self.reg_user_entry = ctk.CTkEntry(self.register_frame, 
                                         placeholder_text="Email")
        self.reg_user_entry.pack(pady=5)

        self.reg_user_entry = ctk.CTkEntry(self.register_frame, 
                                         placeholder_text="Username")
        self.reg_user_entry.pack(pady=5)

        self.reg_pass_entry = ctk.CTkEntry(self.register_frame, 
                                         show="*", placeholder_text="Password")
        self.reg_pass_entry.pack(pady=5)

        ctk.CTkButton(self.register_frame, text="Register", 
                     command=self.register).pack(pady=20)

        ctk.CTkButton(self.register_frame, text="Back to Login", 
                     command=self.show_login_frame, fg_color="transparent").pack()

    def login(self):
        username = self.login_user_entry.get()
        password = self.login_pass_entry.get()

        with open(self.data_file, 'r') as f:
            users = json.load(f)

        if username in users and users[username] == password:
            self.root.withdraw()
            SettingsWindow(self.root)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.reg_user_entry.get()
        password = self.reg_pass_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        with open(self.data_file, 'r') as f:
            users = json.load(f)

        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return

        users[username] = password

        with open(self.data_file, 'w') as f:
            json.dump(users, f)

        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_frame()

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.settings = self.load_settings()

        self.window = ctk.CTkToplevel(parent)
        self.window.title("EyeMouse Settings")
        self.window.geometry("800x600")
        
        self.create_widgets()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except:
            return {
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

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
        messagebox.showinfo("Success", "Settings saved successfully!")

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Sensitivity Settings
        sens_frame = ctk.CTkFrame(main_frame)
        sens_frame.pack(fill='x', pady=5)

        ctk.CTkLabel(sens_frame, text="Cursor Sensitivity:").pack(side='left', padx=10)
        self.sens_scale = ctk.CTkSlider(sens_frame, from_=1, to=100)
        self.sens_scale.set(self.settings["sensitivity"])
        self.sens_scale.pack(side='left', fill='x', expand=True, padx=10)
        self.sens_value = ctk.CTkLabel(sens_frame, text=str(self.settings["sensitivity"]))
        self.sens_value.pack(side='left', padx=10)
        self.sens_scale.configure(command=lambda v: self.sens_value.configure(text=f"{float(v):.0f}"))

        # Calibration Section
        cal_frame = ctk.CTkFrame(main_frame)
        cal_frame.pack(fill='x', pady=5)

        ctk.CTkButton(cal_frame, text="Start Calibration", 
                     command=self.start_calibration).pack(side='left', padx=10, pady=5)
        self.cal_status = ctk.CTkLabel(cal_frame, text="Calibrated", text_color="green")
        self.cal_status.pack(side='left', padx=20)

        # Feedback Settings
        feedback_frame = ctk.CTkFrame(main_frame)
        feedback_frame.pack(fill='x', pady=5)

        self.visual_fb = ctk.CTkCheckBox(feedback_frame, text="Visual Feedback")
        self.visual_fb.pack(side='left', padx=20, pady=5)
        self.audio_fb = ctk.CTkCheckBox(feedback_frame, text="Audio Feedback")
        self.audio_fb.pack(side='left', padx=20, pady=5)

        if self.settings["feedback"]["visual"]:
            self.visual_fb.select()
        if self.settings["feedback"]["audio"]:
            self.audio_fb.select()

        # Control Settings
        control_frame = ctk.CTkScrollableFrame(main_frame, label_text="Eye Control Settings")
        control_frame.pack(fill='both', expand=True, pady=10)

        controls = [
            ("Look at screen position to move cursor", "move_cursor", "combo", ["look", "head movement"]),
            ("Brief left eye close - Left click (ms)", "left_click", "entry"),
            ("Hold left eye closed - Right click (ms)", "right_click", "entry"),
            ("Gaze at screen edges - Scroll", "scroll", "combo", ["edges", "circular motion"]),
            ("Maintain closed eye - Drag items (ms)", "drag", "entry")
        ]

        for text, key, type_, *options in controls:
            row = ctk.CTkFrame(control_frame)
            row.pack(fill='x', pady=5)

            ctk.CTkLabel(row, text=text, width=300, anchor='w').pack(side='left', padx=10)

            if type_ == "entry":
                var = ctk.StringVar(value=str(self.settings["controls"][key]))
                entry = ctk.CTkEntry(row, textvariable=var)
                entry.pack(side='left', padx=10, fill='x', expand=True)
                setattr(self, f"{key}_var", var)
            elif type_ == "combo":
                var = ctk.StringVar(value=self.settings["controls"][key])
                combo = ctk.CTkComboBox(row, variable=var, values=options[0])
                combo.pack(side='left', padx=10, fill='x', expand=True)
                setattr(self, f"{key}_var", var)

        # Buttons
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Save", command=self.on_save).pack(side='left', padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", 
                      command=self.window.destroy, fg_color="gray40").pack(side='left', padx=10)

    def start_calibration(self):
        messagebox.showinfo("Calibration", "Please follow the on-screen instructions to calibrate")
        self.cal_status.configure(text="Calibrated", text_color="green")

    def on_save(self):
        try:
            self.settings = {
                "sensitivity": self.sens_scale.get(),
                "feedback": {
                    "visual": self.visual_fb.get() == 1,
                    "audio": self.audio_fb.get() == 1
                },
                "controls": {
                    "move_cursor": self.move_cursor_var.get(),
                    "left_click": int(self.left_click_var.get()),
                    "right_click": int(self.right_click_var.get()),
                    "scroll": self.scroll_var.get(),
                    "drag": int(self.drag_var.get())
                }
            }
            self.save_settings()
            self.window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for timing settings")

if __name__ == "__main__":
    root = ctk.CTk()
    app = EyeMouseLogin(root)
    root.mainloop()
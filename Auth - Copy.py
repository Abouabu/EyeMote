import customtkinter as ctk 
from tkinter import messagebox
import json, os


class EyeMouseLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("EyeMouse - Login")
        self.root.geometry("400x300")

        # Create data file if not exists
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
        self.login_frame.pack(expand=True, fill='both')

        for widget in self.login_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.login_frame, text="EyeMouse Login", font=('Helvetica', 18)).pack(pady=20)

        ctk.CTkLabel(self.login_frame, text="Username:").pack()
        self.login_user_entry = ctk.CTkEntry(self.login_frame)
        self.login_user_entry.pack()

        ctk.CTkLabel(self.login_frame, text="Password:").pack(pady=(10, 0))
        self.login_pass_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.login_pass_entry.pack()

        ctk.CTkButton(self.login_frame, text="Login", command=self.login).pack(pady=20)
        ctk.CTkButton(self.login_frame, text="Create New Account", command=self.show_register_frame, fg_color="transparent", text_color="blue").pack()

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(expand=True, fill='both')

        for widget in self.register_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.register_frame, text="Create New Account", font=('Helvetica', 18)).pack(pady=20)

        ctk.CTkLabel(self.register_frame, text="Username:").pack()
        self.reg_user_entry = ctk.CTkEntry(self.register_frame)
        self.reg_user_entry.pack()

        ctk.CTkLabel(self.register_frame, text="Password:").pack(pady=(10, 0))
        self.reg_pass_entry = ctk.CTkEntry(self.register_frame, show="*")
        self.reg_pass_entry.pack()

        ctk.CTkButton(self.register_frame, text="Register", command=self.register).pack(pady=20)
        ctk.CTkButton(self.register_frame, text="Back to Login", command=self.show_login_frame, fg_color="transparent", text_color="blue").pack()

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
        self.window.geometry("500x400")

        ctk.CTkLabel(self.window, text="Settings", font=('Helvetica', 20)).pack(pady=20)

        self.sens_scale = ctk.CTkSlider(self.window, from_=1, to=100)
        self.sens_scale.set(self.settings.get("sensitivity", 50))
        self.sens_scale.pack(pady=10)

        ctk.CTkButton(self.window, text="Save Settings", command=self.save_settings).pack(pady=10)
        ctk.CTkButton(self.window, text="Close", command=self.window.destroy).pack(pady=10)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except:
            return {"sensitivity": 50}

    def save_settings(self):
        settings = {"sensitivity": int(self.sens_scale.get())}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
        messagebox.showinfo("Success", "Settings saved successfully!")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = EyeMouseLogin(root)
    root.mainloop()
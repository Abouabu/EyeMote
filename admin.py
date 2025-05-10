# Admin.py
import customtkinter as ctk
from tkinter import ttk
import json
from datetime import datetime
import csv

class AdminWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("EyeMouse - Admin Dashboard")
        self.root.geometry("1200x800")
        
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Main container
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Navigation buttons
        self.nav_buttons = {
            "Users": ctk.CTkButton(self.sidebar, text="User Management", command=self.show_users),
            "Reports": ctk.CTkButton(self.sidebar, text="Reports", command=self.show_reports),
            "Logout": ctk.CTkButton(self.sidebar, text="Logout", command=self.logout)
        }
        
        for btn in self.nav_buttons.values():
            btn.pack(pady=5, fill="x")
        
        # Main content area
        self.content_area = ctk.CTkFrame(self.main_frame)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Initialize data
        self.users = self.load_users()
        self.user_activity = self.load_activity()
        
        # Initialize views
        self.current_view = None
        self.show_users()
    
    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                # Convert string passwords to user data structure
                formatted_users = {}
                for username, data in users.items():
                    if isinstance(data, str):  # If it's just a password string
                        formatted_users[username] = {
                            'password': data,
                            'last_login': 'Never',
                            'usage_count': 0
                        }
                    else:
                        formatted_users[username] = data
                return formatted_users
        except FileNotFoundError:
            return {}
    
    def load_activity(self):
        try:
            with open('activity_log.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def show_users(self):
        self.clear_content()
        self.current_view = "users"
        
        # Search bar
        search_frame = ctk.CTkFrame(self.content_area)
        search_frame.pack(fill="x", pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search users...")
        self.search_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(search_frame, text="Search", width=100).pack(side="left", padx=10)
        
        # User table
        columns = ("username", "last_login", "usage_count")
        self.user_tree = ttk.Treeview(
            self.content_area,
            columns=columns,
            show="headings",
            style="mystyle.Treeview"
        )
        
        # Configure columns
        self.user_tree.heading("username", text="Username")
        self.user_tree.heading("last_login", text="Last Login")
        self.user_tree.heading("usage_count", text="Usage Count")
        
        # Populate data
        for username, data in self.users.items():
            if isinstance(data, dict):
                last_login = data.get('last_login', 'Never')
                usage_count = data.get('usage_count', 0)
            else:
                last_login = 'Never'
                usage_count = 0
            self.user_tree.insert("", "end", values=(
                username,
                last_login,
                usage_count
            ))
        
        self.user_tree.pack(fill="both", expand=True, pady=10)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(self.content_area)
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(btn_frame, text="Edit User", command=self.edit_user).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete User", command=self.delete_user).pack(side="left", padx=5)
    
    def show_reports(self):
        self.clear_content()
        self.current_view = "reports"
        
        # Report controls
        control_frame = ctk.CTkFrame(self.content_area)
        control_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(control_frame, text="Date Range:").pack(side="left")
        self.start_date = ctk.CTkEntry(control_frame, placeholder_text="Start Date (YYYY-MM-DD)")
        self.start_date.pack(side="left", padx=5)
        self.end_date = ctk.CTkEntry(control_frame, placeholder_text="End Date (YYYY-MM-DD)")
        self.end_date.pack(side="left", padx=5)
        
        ctk.CTkButton(control_frame, text="Generate Report", command=self.generate_report).pack(side="left", padx=10)
        ctk.CTkButton(control_frame, text="Export CSV", command=self.export_csv).pack(side="left", padx=5)
        
        # Report display
        self.report_text = ctk.CTkTextbox(self.content_area)
        self.report_text.pack(fill="both", expand=True)
    
    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def edit_user(self):
        # Implement edit user functionality
        pass
    
    def delete_user(self):
        # Implement delete user functionality
        pass
    
    def generate_report(self):
        # Implement report generation
        pass
    
    def export_csv(self):
        # Implement CSV export
        pass
    
    def logout(self):
        self.root.destroy()

# Usage example
if __name__ == "__main__":
    root = ctk.CTk()
    admin = AdminWindow(root)
    root.mainloop()
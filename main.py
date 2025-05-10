import cv2
import mediapipe as mp
import pyautogui
import time
import threading
import customtkinter as ctk
from PIL import Image, ImageTk
from Auth import SettingsWindow

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class EyeControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Eye Controlled Mouse")
        self.geometry("800x600")
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
        # Initialize camera
        self.cam = cv2.VideoCapture(0)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.screen_w, self.screen_h = pyautogui.size()
        
        # State variables
        self.dragging = False
        self.wink_start_time = 0
        self.scroll_cooldown = 0
        self.last_update = 0
        self.last_action = None
        self.action_time = 0
        self.current_gaze = (0, 0)
        self.eye_closed = False
        self.scroll_margin = 0.1  # 10% of screen edges
        
        # Create UI
        self.create_widgets()
        self.update_camera()
        
    def create_widgets(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Camera preview
        self.camera_label = ctk.CTkLabel(self.main_frame, text="")
        self.camera_label.pack(fill="both", expand=True)
        
        # Instructions panel
        self.instructions_frame = ctk.CTkFrame(self.main_frame)
        self.instructions_frame.place(relx=0.05, rely=0.05)
        
        instructions = [
            "1. Look at screen position to move cursor",
            "2. Brief left eye close - Left click",
            "3. Hold left eye closed - Right click",
            "4. Gaze at screen edges - Scroll",
            "5. Maintain closed eye - Drag items"
        ]
        
        for text in instructions:
            label = ctk.CTkLabel(self.instructions_frame, text=text,
                                font=("Arial", 14), anchor="w")
            label.pack(pady=5, padx=10, fill="x")
        
        # Status bar
        self.status_label = ctk.CTkLabel(self.main_frame, text="Status: Initializing",
                                        corner_radius=10, fg_color=("gray20", "gray30"))
        self.status_label.place(relx=0.05, rely=0.9)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(self.main_frame, text="⚙ Settings",
                                         width=120, height=40, corner_radius=20,
                                         command=self.open_settings)
        self.settings_btn.place(relx=0.85, rely=0.9)
        
    def open_settings(self):
        threading.Thread(target=SettingsWindow, args=(self,)).start()
        
    def update_camera(self):
        ret, frame = self.cam.read()
        if ret:
            # Process frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = self.face_mesh.process(rgb_frame)
            self.process_landmarks(frame, output)
            
            # Update status label
            current_time = time.time()
            if self.last_action and (current_time - self.action_time < 0.5):
                action_text = {
                    'left_click': "Left Click",
                    'right_click': "Right Click",
                    'dragging': "Dragging",
                    'scroll_left': "Scrolling Left",
                    'scroll_right': "Scrolling Right",
                    'scroll_up': "Scrolling Up",
                    'scroll_down': "Scrolling Down"
                }.get(self.last_action, "")
                color = "#2FA572" if 'click' in self.last_action else "#FF2D00" if 'right' in self.last_action else "#1E90FF"
                self.status_label.configure(text=action_text, fg_color=color)
            else:
                self.status_label.configure(
                    text=f"Left Eye: {'CLOSED' if self.eye_closed else 'OPEN'}",
                    fg_color=("gray20", "gray30"))
            
            # Convert to Tkinter format
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.configure(image=imgtk)
            self.camera_label.image = imgtk
            
        self.after(10, self.update_camera)
        
    def process_landmarks(self, frame, output):
        frame_h, frame_w = frame.shape[:2]
        landmark_points = output.multi_face_landmarks
        
        if landmark_points:
            landmarks = landmark_points[0].landmark
            
            # Gaze tracking
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                color = (0, 255, 0)  # Green
                if self.dragging:
                    color = (0, 0, 255)  # Red when dragging
                cv2.circle(frame, (x, y), 3, color, -1)
                
                if id == 1:
                    screen_x = self.screen_w * landmark.x
                    screen_y = self.screen_h * landmark.y
                    self.current_gaze = (x, y)
                    
                    # Handle screen edge scrolling
                    self.handle_scrolling(screen_x, screen_y)
                    
                    if not self.dragging:
                        pyautogui.moveTo(screen_x, screen_y, _pause=False)

            # Eye state detection
            left_eye = [landmarks[145], landmarks[159]]
            self.eye_closed = (left_eye[0].y - left_eye[1].y) < 0.004
            
            # Handle eye gestures
            self.handle_gestures()
            
            # Visual feedback
            self.draw_feedback(frame)
            
    def handle_scrolling(self, screen_x, screen_y):
        scroll_margin_w = self.screen_w * self.scroll_margin
        scroll_margin_h = self.screen_h * self.scroll_margin
        current_time = time.time()
        
        if screen_x < scroll_margin_w:
            pyautogui.hscroll(10)
            self.last_action = 'scroll_left'
            self.action_time = current_time
        elif screen_x > self.screen_w - scroll_margin_w:
            pyautogui.hscroll(-10)
            self.last_action = 'scroll_right'
            self.action_time = current_time
            
        if screen_y < scroll_margin_h:
            pyautogui.scroll(10)
            self.last_action = 'scroll_up'
            self.action_time = current_time
        elif screen_y > self.screen_h - scroll_margin_h:
            pyautogui.scroll(-10)
            self.last_action = 'scroll_down'
            self.action_time = current_time
            
    def draw_feedback(self, frame):
        current_time = time.time()
        if self.last_action and (current_time - self.action_time < 0.5):
            x, y = self.current_gaze
            
            if 'click' in self.last_action:
                color = (0, 255, 0) if 'left' in self.last_action else (0, 0, 255)
                cv2.circle(frame, (x, y), 20, color, 2)
                cv2.putText(frame, self.last_action.replace('_', ' ').title(),
                           (x-60, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            if 'scroll' in self.last_action:
                color = (255, 255, 0)
                direction = self.last_action.split('_')[1]
                cv2.putText(frame, f"Scrolling {direction.title()}",
                           (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                
        if self.dragging:
            cv2.putText(frame, "Dragging", (self.current_gaze[0]-40, self.current_gaze[1]+40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
    def handle_gestures(self):
        current_time = time.time()
        
        if self.eye_closed:
            if self.wink_start_time == 0:
                self.wink_start_time = current_time
            else:
                # Check for dragging
                if current_time - self.wink_start_time > DRAG_HOLD_DURATION:
                    if not self.dragging:
                        pyautogui.mouseDown()
                        self.dragging = True
                        self.last_action = 'dragging'
                        self.action_time = current_time
        else:
            if self.wink_start_time > 0:
                wink_duration = current_time - self.wink_start_time
                if wink_duration < LONG_WINK_THRESHOLD:
                    pyautogui.click()
                    self.last_action = 'left_click'
                else:
                    pyautogui.rightClick()
                    self.last_action = 'right_click'
                self.action_time = current_time
                self.wink_start_time = 0
                
            if self.dragging:
                pyautogui.mouseUp()
                self.dragging = False
                self.last_action = None
        
    def on_closing(self):
        self.cam.release()
        self.destroy()

# Configuration constants
LONG_WINK_THRESHOLD = 0.5
DRAG_HOLD_DURATION = 1.0

if __name__ == "__main__":
    app = EyeControlApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
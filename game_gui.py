import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from game import GameEngine
from detector import ObjectDetector

class VQAAgentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VQA RL Agent - Recorder Mode")
        
        self.engine = GameEngine()
        self.detector = ObjectDetector()
        
        self.target_obj = ""
        self.cumulative_reward = 0
        self.step_count = 0
        
        # --- Recording Variables ---
        self.is_recording = False
        self.video_writer = None

        # UI Setup
        self.label_reward = tk.Label(root, text="Reward: 0", font=("Arial", 14, "bold"))
        self.label_reward.pack(pady=5)
        
        self.label_status = tk.Label(root, text="Status: IDLE", fg="orange")
        self.label_status.pack()

        self.entry = tk.Entry(root)
        self.entry.insert(0, "cup")
        self.entry.pack(pady=5)

        tk.Button(root, text="Start Search & Record", command=self.set_goal, bg="#4CAF50", fg="white").pack(pady=5)
        
        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.update_loop()

    def set_goal(self):
        self.target_obj = self.entry.get().lower()
        self.cumulative_reward = 0
        self.step_count = 0
        
        # --- Initialize Video Recording ---
        filename = f"simulation_{self.target_obj}.mp4"
        # We use 'mp4v' codec for standard MP4 files
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        # 10.0 is the FPS. (300, 300) must match the engine width/height
        self.video_writer = cv2.VideoWriter(filename, fourcc, 10.0, (300, 300))
        self.is_recording = True
        
        print(f"Goal set to: {self.target_obj}. Recording started...")

    def update_loop(self):
        # 1. Perception
        frame, _ = self.engine.get_state("Pass")
        annotated_frame, labels = self.detector.process_frame(frame)
        
        # 2. Dynamic Search Logic
        action = "Pass"
        if self.target_obj and self.target_obj not in labels:
            self.step_count += 1
            if self.step_count % 10 < 7:
                action = "RotateRight"
            else:
                action = "MoveAhead"

        # 3. Execution
        new_frame, success = self.engine.get_state(action)
        
        if not success and action == "MoveAhead":
            self.engine.get_state("RotateLeft")
            self.engine.get_state("RotateLeft")

        # 4. Recording Logic
        if self.is_recording and self.video_writer:
            # Annotated frame contains the YOLO boxes
            # We resize to ensure it fits the 300x300 video dimensions
            record_ready = cv2.resize(annotated_frame, (300, 300))
            self.video_writer.write(record_ready)

        # 5. Reward & Stopping
        is_found = self.target_obj in labels and self.target_obj != ""
        reward = 10 if is_found else -0.1
        self.cumulative_reward += reward
        self.label_reward.config(text=f"Total Reward: {round(self.cumulative_reward, 1)}")
        
        if self.target_obj:
            self.detector.log_data(self.target_obj, labels, reward)

        if is_found:
            self.label_status.config(text=f"SUCCESS: {self.target_obj} FOUND!", fg="green")
            # --- Stop Recording on Success ---
            if self.is_recording:
                self.video_writer.release()
                self.is_recording = False
                print(f"Simulation saved as simulation_{self.target_obj}.mp4")

        # 6. Render to GUI
        img = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
        self.canvas.img_tk = img_tk
        self.canvas.config(image=img_tk)

        self.root.after(300, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = VQAAgentApp(root)
    root.mainloop()
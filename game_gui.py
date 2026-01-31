import tkinter as tk
from PIL import Image, ImageTk
import cv2
from game import GameEngine
from detector import ObjectDetector

class VQAAgentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VQA RL Agent - Dynamic Explorer")
        
        self.engine = GameEngine()
        self.detector = ObjectDetector()
        
        self.target_obj = ""
        self.cumulative_reward = 0
        self.step_count = 0
        self.stuck_count = 0

        # UI Setup
        self.label_reward = tk.Label(root, text="Reward: 0", font=("Arial", 14, "bold"))
        self.label_reward.pack(pady=5)
        self.label_status = tk.Label(root, text="Status: IDLE", fg="orange")
        self.label_status.pack()

        self.entry = tk.Entry(root)
        self.entry.insert(0, "cup")
        self.entry.pack(pady=5)

        tk.Button(root, text="Start Dynamic Search", command=self.set_goal).pack(pady=5)
        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.update_loop()

    def set_goal(self):
        self.target_obj = self.entry.get().lower()
        self.cumulative_reward = 0
        self.step_count = 0
        print(f"Agent Goal: {self.target_obj}")

    def update_loop(self):
        # 1. Perception
        frame, _ = self.engine.get_state("Pass")
        annotated_frame, labels = self.detector.process_frame(frame)
        
        # 2. Dynamic Policy Logic
        action = "Pass"
        if self.target_obj and self.target_obj not in labels:
            self.step_count += 1
            
            # Pattern: Scan (Rotate 6 times) then Move
            if self.step_count % 10 < 7:
                action = "RotateRight"
                self.label_status.config(text="Scanning Area...")
            else:
                action = "MoveAhead"
                self.label_status.config(text="Moving Forward...")

        # 3. Execute and check for Collisions
        new_frame, success = self.engine.get_state(action)
        
        if not success and action == "MoveAhead":
            self.stuck_count += 1
            self.label_status.config(text="COLLISION! Re-routing...", fg="red")
            # If hitting a wall, force a large turn
            self.engine.get_state("RotateLeft")
            self.engine.get_state("RotateLeft")
        else:
            self.label_status.config(fg="black")

        # 4. Reward & Log
        is_found = self.target_obj in labels and self.target_obj != ""
        reward = 10 if is_found else -0.1
        self.cumulative_reward += reward
        self.label_reward.config(text=f"Total Reward: {round(self.cumulative_reward, 1)}")
        
        if self.target_obj:
            self.detector.log_data(self.target_obj, labels, reward)
        
        if is_found:
            self.label_status.config(text=f"SUCCESS: Found {self.target_obj}!", fg="green")

        # 5. Render
        img = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
        self.canvas.img_tk = img_tk
        self.canvas.config(image=img_tk)

        self.root.after(300, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = VQAAgentApp(root)
    root.mainloop()
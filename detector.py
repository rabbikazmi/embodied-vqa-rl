import cv2
import json
import datetime
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt") 
        
    def process_frame(self, frame):
        # Lower confidence (0.2) helps detect small objects like cups
        results = self.model.predict(frame, conf=0.2, imgsz=224, verbose=False)[0]
        labels = [self.model.names[int(box.cls[0])] for box in results.boxes]
        return results.plot(), labels

    def log_data(self, target, detected_list, reward):
        log_entry = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "goal": target,
            "seen": detected_list,
            "reward": reward,
            "success": target in detected_list
        }
        with open("agent_log.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
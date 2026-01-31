import cv2
from ai2thor.controller import Controller

class GameEngine:
    def __init__(self):
        self.controller = Controller(
            scene="FloorPlan1", 
            gridSize=0.25,
            width=300, 
            height=300,
            quality="Very Low"
        )
        # Initial tilt so we don't miss the kitchen counters
        self.controller.step(action="LookDown", degrees=30)

    def get_state(self, action_str="Pass"):
        # Execute the action
        event = self.controller.step(action=action_str)
        
        # Check if the action actually worked (Physics check)
        success = event.metadata['lastActionSuccess']
        
        # Convert frame for OpenCV
        frame = cv2.cvtColor(event.frame, cv2.COLOR_RGB2BGR)
        return frame, success
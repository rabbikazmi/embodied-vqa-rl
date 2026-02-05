# VQA Reinforcement Learning Agent

This repository contains an autonomous agent designed to navigate the AI2-THOR environment. The system integrates real-time object detection with a search policy to solve Visual Question Answering (VQA) tasks.

## Demonstration
<p align="center">
  <img src="assests/simulation_potted plant.gif" width="350">
</p>

## Project Overview
The agent is designed to locate specific objects within a 3D kitchen environment. It utilizes a YOLOv8 vision model to interpret the scene and a reinforcement learning-based reward structure to optimize search paths.

### Key Features
* **Dynamic Search Policy**: Implements a Scan-Move-Avoid algorithm to prevent the agent from getting stuck.
* **Vision-Based Navigation**: Uses YOLOv8 bounding boxes to identify and confirm target objects.
* **Automated Recording**: The GUI automatically captures and saves simulations as MP4 files.
* **Data Analytics**: Includes tools to track success rates and visualize cumulative rewards.

### System Architecture
The agent follows a modular architecture:

* **Perception Layer**: YOLOv8 detects objects and provides confidence scores.
* **Decision Layer**: If the target is not detected, the agent rotates to scan or moves forward to explore new areas.
* **Recovery Layer**: Collision detection triggers a rotation to avoid obstacles.
* **Logging Layer** : Every action, detection, and reward is stored in a JSONL buffer for post-run analysis.
## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Analysis Tools](#analysis-tools)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
* Python 3.10 or higher
* Ubuntu/WSL (Recommended for AI2-THOR compatibility)
* X11 server (for headless environments)
* At least 2GB free disk space

### Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd vqa_final
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv lvenv
   source lvenv/bin/activate  # On Windows: lvenv\Scripts\activate
   ```

3. **Install required dependencies:**
   ```bash
   pip install --upgrade pip
   pip install ai2thor==5.0.0
   pip install ultralytics
   pip install opencv-python
   pip install pillow
   pip install numpy
   pip install matplotlib
   pip install moviepy
   ```

4. **Verify YOLOv8 model:**
   The `yolov8n.pt` model file should be present in the project root. If not, it will be automatically downloaded on first run.

5. **Test the installation:**
   ```bash
   python game_gui.py
   ```

## Usage

### Running the VQA Agent

1. **Start the GUI Application:**
   ```bash
   python game_gui.py
   ```

2. **In the GUI:**
   - Enter the target object name (e.g., "apple", "potted plant", "cup")
   - Click **"Start Mission"** to begin the agent's search
   - The agent will autonomously navigate and search for the target
   - Video recording starts automatically and saves as MP4 when mission completes

3. **Agent Behavior:**
   - **Scan Phase**: Rotates 360° to detect objects
   - **Move Phase**: Advances forward to explore new areas
   - **Avoid Phase**: Backs up and rotates when collisions are detected
   - **Success**: Stops when target object is found with high confidence

### Analysis and Visualization

#### 1. Analyze Agent Performance
```bash
python analyze_logs.py
```
This generates a report showing:
- Total steps taken
- Success status and discovery time
- Objects detected during the mission
- Search efficiency metrics

#### 2. Plot Reward Curve
```bash
python plot_results.py
```
Creates `reward_curve1.png` showing the agent's learning progress over time.

#### 3. Convert Video to GIF
```bash
python gif.py
```
Converts the simulation MP4 to an optimized GIF for documentation.

## Project Structure

```
vqa_final/
│
├── game.py              # AI2-THOR environment controller
├── detector.py          # YOLOv8 object detection and logging
├── game_gui.py          # Main GUI application with recording
│
├── analyze_logs.py      # Performance analysis tool
├── plot_results.py      # Reward visualization
├── gif.py               # Video-to-GIF converter
│
├── yolov8n.pt           # Pre-trained YOLO model
├── agent_log.jsonl      # Action logs (generated at runtime)
├── assests/             # Simulation recordings and GIFs
│   └── simulation_*.gif
│
└── README.md            # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `game.py` | Manages AI2-THOR controller, scene initialization, and action execution |
| `detector.py` | YOLOv8 integration for object detection with confidence scoring |
| `game_gui.py` | Tkinter GUI with agent logic, auto-recording, and real-time visualization |
| `analyze_logs.py` | Analyzes JSONL logs to generate performance metrics |
| `plot_results.py` | Creates cumulative reward plots for agent evaluation |
| `gif.py` | Converts MP4 recordings to lightweight GIFs |

## Analysis Tools

### Understanding the Logs
The `agent_log.jsonl` file records each step with:
- `step`: Step number
- `action`: Action taken (RotateRight, MoveAhead, etc.)
- `success`: Whether action was physically successful
- `reward`: Reward received
- `seen`: List of detected objects
- `timestamp`: Action timestamp

### Metrics Tracked
- **Success Rate**: Whether the target was found
- **Efficiency**: Steps needed to find the target
- **Object Knowledge**: Frequency of object detections
- **Cumulative Reward**: Total reward accumulated over time

## Troubleshooting

### Common Issues

**1. AI2-THOR fails to start**
```bash
# Install X11 dependencies (Ubuntu/Debian)
sudo apt-get install xorg
# For WSL, install VcXsrv or Xming
```

**2. YOLO model not found**
The model will auto-download. If it fails:
```bash
# Download manually
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

**3. GUI doesn't display frames**
Ensure tkinter is installed:
```bash
sudo apt-get install python3-tk
```

**4. Low frame rate**
The environment is configured for "Very Low" quality for speed. To improve:
- Edit `game.py` and change `quality="Very Low"` to `quality="Medium"`
- Increase `width` and `height` values

## System Requirements

- **OS**: Ubuntu 18.04+, WSL2, or macOS
- **RAM**: Minimum 4GB
- **GPU**: Optional (CPU mode works fine for this project)
- **Python**: 3.10+

## Credits

Built using:
- [AI2-THOR](https://ai2thor.allenai.org/) - Interactive 3D environment
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection
- [OpenCV](https://opencv.org/) - Computer vision

## License

This project is for educational purposes.
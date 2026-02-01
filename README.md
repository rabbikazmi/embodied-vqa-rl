# VQA Reinforcement Learning Agent

This repository contains an autonomous agent designed to navigate the AI2-THOR environment. The system integrates real-time object detection with a search policy to solve Visual Question Answering (VQA) tasks.

## Demonstration
<p align="center">
  <img src="simulation_potted plant.gif" width="500">
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
## Installation

### Prerequisites
* Python 3.10+
* Ubuntu/WSL (Recommended)

### Setup
1. Clone the repository:
   ```bash
   git clone repo-url
   cd vqa_final
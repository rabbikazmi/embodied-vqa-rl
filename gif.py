from moviepy import VideoFileClip

# Load the video
clip = VideoFileClip("simulation_potted plant.mp4")

# Resize to 480px width to keep the file size small for GitHub
# and save as a GIF at 10 frames per second
clip.resized(width=480).write_gif("simulation_potted plant.gif", fps=10)
print("GIF created successfully!")
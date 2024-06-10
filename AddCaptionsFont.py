import subprocess
import os

# Define file paths
video_file = "output.mp4"
subtitle_file = "subtitles.srt"
output_file = "output_video_with_subtitles.mp4"

# Check if subtitle file exists
if not os.path.isfile(subtitle_file):
    raise FileNotFoundError(f"Subtitle file '{subtitle_file}' not found.")

# Define custom font style (adjust the path to your font file)
font_name = "Assets/Fonts/boldfont.ttf"  # Font name (must be installed on your system)
font_size = 24  # Font size
font_color = "white"  # Font color
border_style = 1  # Border style
outline = 2  # Outline thickness
shadow = 1  # Shadow depth
alignment = 2  # Center alignment

# Construct the ffmpeg command with subtitle styling
subtitle_file_absolute = os.path.abspath(subtitle_file)
ffmpeg_command = [
    "ffmpeg",
    "-i", video_file,
    "-vf", f"subtitles={subtitle_file_absolute}:force_style='Fontname={font_name},Fontsize={font_size},PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle={border_style},Outline={outline},Shadow={shadow},Alignment={alignment}'",
    "-c:a", "copy",
    output_file
]

# Run the ffmpeg command
try:
    subprocess.run(ffmpeg_command, check=True)
    print("Video with subtitles has been created successfully.")
except subprocess.CalledProcessError as e:
    print("An error occurred while processing the video with ffmpeg:")
    print(e.stderr.decode())

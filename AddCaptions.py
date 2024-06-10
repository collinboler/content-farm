import subprocess
import os
import subprocess
import os
import uuid
def add_captions():
    # Define file paths
    video_file = "output.mp4"
    subtitle_file = "subtitles.srt"



    
    output_file = "captionoutput.mp4"


    # Delete the file "captionoutput.mp4" if it exists
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Check if subtitle file exists
    if not os.path.isfile(subtitle_file):
        raise FileNotFoundError(f"Subtitle file '{subtitle_file}' not found.")

    # Define custom font style (adjust the path to your font file)
    font_name = "The Bold Font"  # Font name (must be installed on your system)
    font_size = 12  # Font size
    primary_color = "&HFFFFFF&"  # Primary color (black) in BGR format  
    outline_color = "&H000000&"  # Outline color (white) in BGR format  
    border_style = 1  # Border style (1 for outline)
    outline = 2  # Outline thickness
    shadow = 1  # Shadow depth
    alignment = 10  # Center alignment

    # Construct the ffmpeg command with absolute path
    subtitle_file_absolute = os.path.abspath(subtitle_file)
    ffmpeg_command = [
        "ffmpeg",
        "-i", video_file,
        "-vf", f"subtitles={subtitle_file_absolute}:force_style='Fontname={font_name},Fontsize={font_size},PrimaryColour={primary_color},OutlineColour={outline_color},BorderStyle={border_style},Outline={outline},Shadow={shadow},Alignment={alignment}'",
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
    # Define file paths
    video_file = "output.mp4"
    subtitle_file = "subtitles.srt"
    
    def add_captions():
        # Define file paths
        video_file = "output.mp4"
        subtitle_file = "subtitles.srt"

        # Generate a random output file name
        output_file = f"captionoutput_{uuid.uuid4().hex}.mp4"

        # Delete the file "captionoutput.mp4" if it exists
        if os.path.isfile(output_file):
            os.remove(output_file)

        # Rest of the code...

    if __name__ == "__main__":
        add_captions()

    # Delete the file "captionoutput.mp4" if it exists
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Check if subtitle file exists
    if not os.path.isfile(subtitle_file):
        raise FileNotFoundError(f"Subtitle file '{subtitle_file}' not found.")

    # Define custom font style (adjust the path to your font file)
    font_name = "The Bold Font"  # Font name (must be installed on your system)
    font_size = 12  # Font size
    primary_color = "&HFFFFFF&"  # Primary color (black) in BGR format  
    outline_color = "&H000000&"  # Outline color (white) in BGR format  
    border_style = 1  # Border style (1 for outline)
    outline = 2  # Outline thickness
    shadow = 1  # Shadow depth
    alignment = 10  # Center alignment

    # Construct the ffmpeg command with absolute path
    subtitle_file_absolute = os.path.abspath(subtitle_file)
    ffmpeg_command = [
        "ffmpeg",
        "-i", video_file,
        "-vf", f"subtitles={subtitle_file_absolute}:force_style='Fontname={font_name},Fontsize={font_size},PrimaryColour={primary_color},OutlineColour={outline_color},BorderStyle={border_style},Outline={outline},Shadow={shadow},Alignment={alignment}'",
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



if __name__ == "__main__":
    add_captions()

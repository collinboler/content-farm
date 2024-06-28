import os, random
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.fx.all import crop

# Define the path to your assets
short_video_path = "initial_videos/beach_background.mp4"
image_folder_path = "generated_images/test1"
texts = ["1", "2", "3", "4", 
         "5", "6", "7", "8", 
         "9", "10", "11", "12"]

# Get all image file paths from the specified folder
image_paths = sorted([os.path.join(image_folder_path, file) for file in os.listdir(image_folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))])

# Ensure there are exactly 12 images
if len(image_paths) != 12:
    raise ValueError("There must be exactly 12 images in the folder.")

# Load the short video clip
short_video = VideoFileClip(short_video_path)

video_duration = short_video.duration

# Choose a random start time within the video duration (subtracting 5 seconds to ensure we don't exceed the video length)
start_time = random.uniform(0, video_duration - 5)

# Extract a 5-second subclip starting from the randomly chosen start time
short_video = short_video.subclip(start_time, start_time + 8)

# Resize the cropped video to 1080x1920 (if needed)
resized_video = short_video.resize(height=1920, width=1080)

# Crop the short video to 1920x1080
cropped_video = resized_video.crop(x1=0, y1=0 / 2, x2=1080, y2=1920)

# Create a text clip
text_clip = TextClip(f"Which bathroom\n is your boyfriend \n choosing?", fontsize=60, color='white', bg_color='black')
text_clip = text_clip.set_position((270, 600)).set_duration(7)

# Overlay the text on the image
composite_clip = CompositeVideoClip([cropped_video, text_clip])

# Calculate the duration each image should be displayed
image_duration = (60 - cropped_video.duration) / 12

# Create a list to hold all the clips
clips = [composite_clip]

# Create image clips with text overlays
for image_path, text in zip(image_paths, texts):
    # Load the image
    image_clip = ImageClip(image_path).set_duration(image_duration).resize(height=1920)

    image_clip = image_clip.resize(lambda t : 1+0.01*t)
    image_clip = image_clip.set_position(('center', 'center'))

    # Center-crop the image to 1080x1920 if its width is larger than 1080
    if image_clip.w > 1080:
        image_clip = image_clip.crop(x_center=image_clip.w/2, y_center=image_clip.h/2, width=1080, height=1920)

    # Create a text clip
    text_clip = TextClip(text, fontsize=100, color='white', bg_color='black')
    text_clip = text_clip.set_position((600,400)).set_duration(image_duration)

    # Overlay the text on the image
    composite_clip = CompositeVideoClip([image_clip, text_clip])
    
    # Add the composite clip to the list of clips
    clips.append(composite_clip)

# Concatenate all the clips
final_clip = concatenate_videoclips(clips, method="compose")

# Write the final video to a file
final_clip.write_videofile("output/final_video.mp4", fps=24)

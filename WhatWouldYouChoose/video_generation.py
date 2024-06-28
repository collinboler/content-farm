import os
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.fx.all import crop

# Define the path to your assets
short_video_path = "initial_videos/beach_background.mp4"
image_folder_path = "generated_images/test1"
texts = ["Text for image 1", "Text for image 2", "Text for image 3", "Text for image 4", 
         "Text for image 5", "Text for image 6", "Text for image 7", "Text for image 8", 
         "Text for image 9", "Text for image 10", "Text for image 11", "Text for image 12"]

# Get all image file paths from the specified folder
image_paths = sorted([os.path.join(image_folder_path, file) for file in os.listdir(image_folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))])

# Ensure there are exactly 12 images
if len(image_paths) != 12:
    raise ValueError("There must be exactly 12 images in the folder.")

# Load the short video clip
short_video = VideoFileClip(short_video_path)

# Crop the short video to 1080x1920
cropped_video = crop(short_video, width=1080, height=1920, x_center=short_video.w/2, y_center=short_video.h/2)

# Calculate the duration each image should be displayed
image_duration = (60 - cropped_video.duration) / 12

# Create a list to hold all the clips
clips = [cropped_video]

# Function to apply subtle motion to an image clip
def apply_motion(image_clip, duration):
    def make_frame(t):
        x_mov = 20 * (t / duration)  # horizontal motion
        y_mov = 10 * (t / duration)  # vertical motion
        return image_clip.crop(x1=x_mov, y1=y_mov, width=1080, height=1920).get_frame(t)
    
    return image_clip.fl(make_frame)

# Create image clips with text overlays
for image_path, text in zip(image_paths, texts):
    # Load the image
    image_clip = ImageClip(image_path).set_duration(image_duration).resize(height=1920)

    # Center-crop the image to 1080x1920 if its width is larger than 1080
    if image_clip.w > 1080:
        image_clip = image_clip.crop(x_center=image_clip.w/2, y_center=image_clip.h/2, width=1080, height=1920)

    # Apply subtle motion effect
    #image_clip = apply_motion(image_clip, image_duration)

    # Create a text clip
    text_clip = TextClip(text, fontsize=24, color='white', bg_color='black')
    text_clip = text_clip.set_position('center').set_duration(image_duration)

    # Overlay the text on the image
    composite_clip = CompositeVideoClip([image_clip, text_clip])
    
    # Add the composite clip to the list of clips
    clips.append(composite_clip)

# Concatenate all the clips
final_clip = concatenate_videoclips(clips, method="compose")

# Write the final video to a file
final_clip.write_videofile("output/final_video.mp4", fps=24)

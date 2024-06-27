import moviepy.editor as mp
import pysrt
from PIL import Image, ImageDraw, ImageFont

def parse_srt(srt_path):
    subtitles = pysrt.open(srt_path)
    subs = []
    for subtitle in subtitles:
        start_time = (subtitle.start.hours * 3600 + subtitle.start.minutes * 60 +
                      subtitle.start.seconds + subtitle.start.milliseconds / 1000)
        end_time = (subtitle.end.hours * 3600 + subtitle.end.minutes * 60 +
                    subtitle.end.seconds + subtitle.end.milliseconds / 1000)
        text = subtitle.text
        subs.append((start_time, end_time, text))
    return subs

def create_text_image(text, image_size):
    image = Image.new('RGBA', image_size, (255, 255, 255, 0))
<<<<<<< HEAD:AddList.py
    draw = ImageDraw.Draw(image)
    bold_font = ImageFont.truetype("Assets/Fonts/boldfont.ttf", 60)  # Bold font
    emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 40)  # Font that supports emojis

    text_x, text_y = image_size[0] // 6, image_size[1] // 8  # Position text more centered to the top right
    lines = text.split('\n')
    for line in lines:
        text, color = extract_color(line)
        parts = split_text_and_emojis(text)

        for part, part_type in parts:
            font = emoji_font if part_type == 'emoji' else bold_font
            part_color = (255, 255, 255, 255) if part_type == 'emoji' else color  # Set emoji color to default
            draw_text_with_stroke(draw, (text_x, text_y), part, font, part_color, (0, 0, 0, 255), 2)
            text_x += draw.textbbox((0, 0), part, font=font)[2]
        
        text_y += bold_font.getbbox(line)[3]
        text_x = image_size[0] // 6  # Reset x position after each line
=======

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Assets/Fonts/boldfont.ttf", 30)  # You can change the font and size as needed

    text_x, text_y = 10, 10
    lines = text.split('\n')
    for line in lines:
        draw.text((text_x, text_y), line, font=font, fill=(255, 255, 255, 255))
        text_y += font.getbbox(line)[3]  # getbbox returns a tuple (left, top, right, bottom)
>>>>>>> parent of 58d872f (list with color):AdList.py

    combined_path = 'text_overlay.png'
    image.save(combined_path)
    return combined_path

def add_text_to_video(video_path, srt_path, output_path):
    video = mp.VideoFileClip(video_path)
    subs = parse_srt(srt_path)

    # Initial list
    initial_list = "1. Easy\n2. Easy\n3. Medium\n4. Medium\n5. Hard\n6. Impossible"
    initial_text_image_path = create_text_image(initial_list, video.size)

    # Create a clip for the initial list that spans the entire duration of the video
    initial_clip = (mp.ImageClip(initial_text_image_path)
                    .set_start(0)
                    .set_end(video.duration)
                    .set_position(("left", "top")))

    # Add the initial clip to the list of clips
    clips = [video, initial_clip]

    # Create and add clips for each subtitle
    for start_time, end_time, text in subs:
        text_image_path = create_text_image(text, video.size)
        text_clip = (mp.ImageClip(text_image_path)
                     .set_start(start_time)
                     .set_end(end_time)
                     .set_position(("left", "top")))
        clips.append(text_clip)

    final_clip = mp.CompositeVideoClip(clips)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

<<<<<<< HEAD:AddList.py
if __name__ == "__main__":
    # Usage
    video_path = 'vids/20240626-233444.mp4'
    srt_path = 'list.srt'  # Ensure you have the correct path to your SRT file
    output_path = 'output_video2.mp4'
=======
# Usage
video_path = 'output_video.mp4'
srt_path = 'subtitles.srt'  # Ensure you have the correct path to your SRT file
output_path = 'output_video2.mp4'
>>>>>>> parent of 58d872f (list with color):AdList.py

    add_text_to_video(video_path, srt_path, output_path)
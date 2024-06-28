import moviepy.editor as mp
import pysrt
from PIL import Image, ImageDraw, ImageFont
import emoji
import re

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

def extract_color(text):
    color_mapping = {
        'green': (0, 255, 0, 255),
        'yellow': (255, 255, 0, 255),
        'red': (255, 0, 0, 255),
        'purple': (128, 0, 128, 255)
    }
    color = (255, 255, 255, 255)  # default color (white)
    if '(' in text and ')' in text:
        color_name = text[text.find('(')+1:text.find(')')].strip()
        color = color_mapping.get(color_name, color)
        text = text[:text.find('(')].strip()
    return text, color

def split_text_and_emojis(text):
    parts = re.split(r'(\s+)', text)
    result = []
    buffer = ""
    for part in parts:
        if emoji.emoji_count(part):
            if buffer:
                result.append((buffer, 'text'))
                buffer = ""
            result.append((part, 'emoji'))
        else:
            buffer += part
    if buffer:
        result.append((buffer, 'text'))
    return result

def draw_text_with_stroke(draw, position, text, font, text_color, stroke_color, stroke_width):
    x, y = position
    for dx in range(-stroke_width, stroke_width+1):
        for dy in range(-stroke_width, stroke_width+1):
            if dx != 0 or dy != 0:
                draw.text((x+dx, y+dy), text, font=font, fill=stroke_color)
    draw.text((x, y), text, font=font, fill=text_color)

def create_text_image(text, image_size):
    image = Image.new('RGBA', image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    bold_font = ImageFont.truetype("Assets/Fonts/boldfont.ttf", 50)  # Bold font
    emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 40)  # Font that supports emojis

    text_x, text_y = image_size[0] // 2.5, image_size[1] // 8  # Position text more centered to the top right
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
        text_x = image_size[0] // 2.5  # Reset x position after each line

    combined_path = 'text_overlay.png'
    image.save(combined_path)
    return combined_path

def add_text_to_video(video_path, srt_path, output_path):
    video = mp.VideoFileClip(video_path)
    subs = parse_srt(srt_path)

    # Add clips for each subtitle
    clips = [video]
    for start_time, end_time, text in subs:
        text_image_path = create_text_image(text, video.size)
        text_clip = (mp.ImageClip(text_image_path)
                     .set_start(start_time)
                     .set_end(end_time)
                     .set_position(("center", "top")))  # Adjust position to be more centered
        clips.append(text_clip)

    final_clip = mp.CompositeVideoClip(clips)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

# Usage
# video_path = 'output_video.mp4'
# srt_path = 'list.srt'  # Ensure you have the correct path to your SRT file
# output_path = 'output_video2.mp4'

# add_text_to_video(video_path, srt_path, output_path)

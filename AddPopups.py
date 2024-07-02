import moviepy.editor as mp
import pysrt
from PIL import Image
import random
import os
import numpy as np

class VideoStickerOverlay:
    def __init__(self, video_path, sticker_dir, srt_path, output_path):
        self.video_path = video_path
        self.sticker_dir = sticker_dir
        self.srt_path = srt_path
        self.output_path = output_path
        self.subtitles = pysrt.open(srt_path)
        
    def _parse_srt_time(self, srt_time):
        return srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds + srt_time.milliseconds / 1000
    
    def _resize_sticker(self, sticker_path, video_w, video_h):
        sticker_img = Image.open(sticker_path)
        sticker_w, sticker_h = sticker_img.size
        aspect_ratio = sticker_h / sticker_w
        new_width = video_w
        new_height = int(new_width * aspect_ratio)
        
        resized_once = False

        if new_height >= 0.45 * video_h:
            new_height = int(0.55 * video_h)
            new_width = int(new_height / aspect_ratio)
            resized_once = True
        
        resized_sticker = sticker_img.resize((new_width, new_height), Image.LANCZOS)
        resized_sticker_path = os.path.join(self.sticker_dir, 'resized_sticker.png')
        resized_sticker.save(resized_sticker_path)
        return resized_sticker_path, resized_sticker.size
    
    def _get_random_sticker(self):
        sticker_num = random.randint(1, 7)
        sticker_path = os.path.join(self.sticker_dir, f"Bateman{sticker_num}.png")
        return sticker_path
    
    def _get_sticker_clips(self, video_clip):
        sticker_clips = []
        video_w, video_h = video_clip.size
        
        for subtitle in self.subtitles:
            start_time = self._parse_srt_time(subtitle.start)
            end_time = self._parse_srt_time(subtitle.end)
            duration = end_time - start_time
            random_sticker_path = self._get_random_sticker()
            resized_sticker_path, resized_size = self._resize_sticker(random_sticker_path, video_w, video_h)
            
            # Set initial position
            initial_x = 0 # random.uniform(0, video_w - resized_size[0])
            initial_y = random.uniform(video_h * 0.50, video_h - resized_size[1]) 

            # Define the movement function
            def move_position(t):
                x = initial_x + (video_w - resized_size[0]) * 0.1 * np.sin(2 * np.pi * t / duration)
                y = initial_y + (video_h * 0.45 - resized_size[1]) * 0.1 * np.cos(2 * np.pi * t / duration)
                return (x, y)

            sticker_clip = (mp.ImageClip(resized_sticker_path, transparent=True)
                            .set_start(start_time)
                            .set_duration(duration)
                            .set_position(move_position)
                            .set_opacity(1))
            
            sticker_clips.append(sticker_clip)
        
        return sticker_clips
    
    def add_sticker_to_video(self):
        video_clip = mp.VideoFileClip(self.video_path)
        sticker_clips = self._get_sticker_clips(video_clip)
        final_clip = mp.CompositeVideoClip([video_clip] + sticker_clips)
        
        final_clip.write_videofile(self.output_path, codec='libx264', audio_codec='aac')

# Usage

def main(video_path, sticker_dir, srt_path, output_path):
    overlay = VideoStickerOverlay(video_path, sticker_dir, srt_path, output_path)
    overlay.add_sticker_to_video()

if __name__ == "__main__":
    video_path = 'vids/20240623-111601.mp4'
    sticker_dir = 'stickers/bateman'
    srt_path = 'popup.srt'
    output_path = 'output_video.mp4'
    main(video_path, sticker_dir, srt_path, output_path)

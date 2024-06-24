import moviepy.editor as mp
import pysrt
from PIL import Image
import random
import os

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
            new_height = int(0.45 * video_h)
            new_width = int(new_height / aspect_ratio)
            resized_once = True
        
        resized_sticker = sticker_img.resize((new_width, new_height), Image.LANCZOS)
        resized_sticker_path = os.path.join(self.sticker_dir, 'resized_sticker.png')
        resized_sticker.save(resized_sticker_path)
        return resized_sticker_path, resized_once
    
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
            resized_sticker_path, resized_once = self._resize_sticker(random_sticker_path, video_w, video_h)  # Resize to fit video width and height constraints

            if resized_once:
                position = (0, 'bottom')  # Align left edge with the left side of the video
            else:
                position = ('center', 'bottom')  # Center position

            sticker_clip = (mp.ImageClip(resized_sticker_path, transparent=True)
                            .set_start(start_time)
                            .set_duration(duration)
                            .set_position(position)
                            .set_opacity(1))
            
            sticker_clips.append(sticker_clip)
        
        return sticker_clips
    
    def add_sticker_to_video(self):
        video_clip = mp.VideoFileClip(self.video_path)
        sticker_clips = self._get_sticker_clips(video_clip)
        final_clip = mp.CompositeVideoClip([video_clip] + sticker_clips)
        
        final_clip.write_videofile(self.output_path, codec='libx264', audio_codec='aac')

# Usage

video_path = 'vids/20240623-111601.mp4'
sticker_dir = 'stickers/bateman'
srt_path = 'popup.srt'
output_path = 'output_video.mp4'

overlay = VideoStickerOverlay(video_path, sticker_dir, srt_path, output_path)
overlay.add_sticker_to_video()

from moviepy.editor import VideoFileClip, CompositeVideoClip
import re

def parse_srt(srt_file):
    timestamps = []
    with open(srt_file, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):
            start_time = lines[i+1].split(' --> ')[0].replace(',', '.')
            end_time = lines[i+1].split(' --> ')[1].replace(',', '.')
            if '[GIF]' in lines[i+2]:
                timestamps.append((start_time, end_time))
    return timestamps

def add_gif_to_video(video_path, gif_path, srt_file, output_path):
    video = VideoFileClip(video_path)
    gif = VideoFileClip(gif_path, has_mask=True)

    timestamps = parse_srt(srt_file)
    clips = [video]

    for start, end in timestamps:
        start = convert_to_seconds(start)
        end = convert_to_seconds(end)
        gif_clip = gif.set_start(start).set_duration(end-start).set_position(("center", "center"))
        clips.append(gif_clip)

    final_video = CompositeVideoClip(clips, size=video.size)
    final_video.write_videofile(output_path, codec="libx264", fps=video.fps)

def convert_to_seconds(time_str):
    time_parts = re.split('[:.]', time_str)
    return int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2]) + int(time_parts[3]) / 1000

if __name__ == "__main__":
    video_path = 'vids/20240607-221502.mp4'
    gif_path = 'Assets/Timer/Timer2.gif'
    srt_file = 'gif_timings.srt'
    output_path = 'StickerVid.mp4'
    
    add_gif_to_video(video_path, gif_path, srt_file, output_path)

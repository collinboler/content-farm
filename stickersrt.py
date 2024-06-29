import re
from datetime import datetime, timedelta
import os

def parse_srt(file_path):
    with open(file_path, 'r') as file:
        srt_data = file.read()
        
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d|\Z)', re.DOTALL)
    matches = pattern.findall(srt_data)
    
    subtitles = []
    for match in matches:
        index, start_time, end_time, text = match
        subtitles.append({
            'index': int(index),
            'start_time': datetime.strptime(start_time, '%H:%M:%S,%f'),
            'end_time': datetime.strptime(end_time, '%H:%M:%S,%f'),
            'text': text.strip()
        })
        
    return subtitles

def create_gif_timings(subtitles, gif_duration=3.5):
    # Delete the file "gif_timings.srt" if it exists
    if os.path.isfile("gif_timings.srt"):
        os.remove("gif_timings.srt")

    gif_duration = timedelta(seconds=gif_duration)
    gif_timings = []
    
    # Handle the gap before the first subtitle
    if subtitles and subtitles[0]['start_time'] > (subtitles[0]['start_time'].replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=3)):
        gif_start = subtitles[0]['start_time'].replace(hour=0, minute=0, second=0, microsecond=0)
        gif_end = gif_start + gif_duration
        gif_timings.append({'start_time': gif_start, 'end_time': gif_end})
    
    for i in range(len(subtitles) - 1):
        current_end = subtitles[i]['end_time']
        next_start = subtitles[i + 1]['start_time']
        
        gap = next_start - current_end
        if gap > gif_duration:
            gif_start = current_end + timedelta(seconds=0.5)
            gif_end = gif_start + gif_duration
            gif_timings.append({'start_time': gif_start, 'end_time': gif_end})
    
    return gif_timings

def write_srt(file_path, gif_timings):
    with open(file_path, 'w') as file:
        for i, timing in enumerate(gif_timings):
            start_time = timing['start_time'].strftime('%H:%M:%S,%f')[:-3]
            end_time = timing['end_time'].strftime('%H:%M:%S,%f')[:-3]
            file.write(f"{i+1}\n{start_time} --> {end_time}\n[GIF]\n\n")

# Usage
def srt_create(original_srt, new_srt):
    subtitles = parse_srt(original_srt)
    gif_timings = create_gif_timings(subtitles)
    write_srt(new_srt, gif_timings)

    print(f"New SRT file with GIF timings created: {new_srt}")

if __name__ == '__main__':
    srt_create('subtitles.srt', 'gif_timings.srt')

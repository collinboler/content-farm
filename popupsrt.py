import re
from datetime import datetime, timedelta
import os
import subprocess

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

def create_all_empty_space_timings(gif_timings, video_length):
    empty_timings = []
    video_end = timedelta(seconds=float(video_length))

    previous_end = datetime(1900, 1, 1, 0, 0, 0, 0)

    for timing in gif_timings:
        current_start = timing['start_time']
        if current_start > previous_end:
            empty_timings.append({'start_time': previous_end, 'end_time': current_start})
        previous_end = timing['end_time']

    if previous_end < datetime(1900, 1, 1) + video_end:
        empty_timings.append({'start_time': previous_end, 'end_time': datetime(1900, 1, 1) + video_end})

    return empty_timings

def write_srt(file_path, timings):
    with open(file_path, 'w') as file:
        for i, timing in enumerate(timings):
            start_time = timing['start_time'].strftime('%H:%M:%S,%f')[:-3]
            end_time = timing['end_time'].strftime('%H:%M:%S,%f')[:-3]
            file.write(f"{i+1}\n{start_time} --> {end_time}\n[EMPTY SPACE]\n\n")

def get_video_length(video_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration = float(result.stdout)
    return str(duration)

# Usage
def create_empty_srt(gif_srt, video_path, new_srt):
    gif_timings = parse_srt(gif_srt)
    video_length = get_video_length(video_path)
    empty_timings = create_all_empty_space_timings(gif_timings, video_length)
    write_srt(new_srt, empty_timings)

    print(f"New SRT file with empty space timings created: {new_srt}")

# Call the function
if __name__ == '__main__':
    create_empty_srt('gif_timings.srt', 'vids/20240623-111601.mp4', 'popup.srt')

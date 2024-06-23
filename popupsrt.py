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

def create_empty_space_timings(gif_timings, video_length, empty_space_duration=3.5):
    empty_space_duration = timedelta(seconds=empty_space_duration)
    empty_timings = []

    # Add the empty space between the start of the video and the first gif_timing
    first_gif_start = gif_timings[0]['start_time']
    video_start = datetime(1900, 1, 1, 0, 0, 0, 0)
    if first_gif_start > video_start:
        empty_timings.append({
            'start_time': video_start,
            'end_time': first_gif_start
        })

    for i in range(len(gif_timings) - 1):
        current_end = gif_timings[i]['end_time']
        next_start = gif_timings[i + 1]['start_time']
        
        gap = next_start - current_end
        if gap > empty_space_duration:
            empty_start = current_end + timedelta(seconds=0.5)
            empty_end = empty_start + empty_space_duration
            empty_timings.append({'start_time': empty_start, 'end_time': empty_end})
    
    # Add the last empty space between the end of the last gif_timing and the end of the video
    last_gif_end = gif_timings[-1]['end_time']
    video_end = timedelta(seconds=float(video_length))
    final_gap = video_end - (last_gif_end - datetime(1900, 1, 1))
    if final_gap > empty_space_duration:
        final_start = last_gif_end 
        # + timedelta(seconds=0.5)
        final_end = last_gif_end + final_gap
        empty_timings.append({'start_time': final_start, 'end_time': final_end})
    
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
    empty_timings = create_empty_space_timings(gif_timings, video_length)
    write_srt(new_srt, empty_timings)

    print(f"New SRT file with empty space timings created: {new_srt}")

# Call the function
if __name__ == '__main__':
    create_empty_srt('gif_timings.srt', 'vids/20240623-111601.mp4', 'popup.srt')

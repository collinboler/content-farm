from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip
import pysrt

def parse_srt_for_gif_timing(srt_path):
    subs = pysrt.open(srt_path)
    gif_timings = []

    for sub in subs:
        if '[GIF]' in sub.text:
            start_time = sub.start.ordinal / 1000.0
            end_time = sub.end.ordinal / 1000.0
            gif_timings.append((start_time, end_time))

    return gif_timings

def overlay_gif_on_video(video_path, gif_path, srt_path, output_path, position=("center", "center")):
    print("Loading video clip...")
    video_clip = VideoFileClip(video_path)
    
    print("Loading GIF clip...")
    gif_clip = VideoFileClip(gif_path, has_mask=True)
    
    print("Parsing SRT file for GIF timings...")
    gif_timings = parse_srt_for_gif_timing(srt_path)
    
    print("Creating GIF clips with timings...")
    gif_clips = []
    for start_time, end_time in gif_timings:
        gif_clip_instance = gif_clip.subclip(0, end_time - start_time).set_start(start_time).set_position(position)
        gif_clips.append(gif_clip_instance)
    
    print("Creating composite video clip...")
    final_clip = CompositeVideoClip([video_clip] + gif_clips)
    
    print("Writing output video file to disk...")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec='aac')
    print("Finished writing video with GIF overlay.")

def add_audio_to_video(video_path, audio_path):
    print("Loading video clip for audio addition...")
    video_clip = VideoFileClip(video_path)
    
    print("Loading audio clip...")
    audio_clip = AudioFileClip(audio_path)
    
    print(f"Video duration: {video_clip.duration} seconds")
    print(f"Audio duration: {audio_clip.duration} seconds")
    
    # Ensure the audio duration matches the video duration
    if audio_clip.duration > video_clip.duration:
        print("Trimming audio to match video duration...")
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    elif audio_clip.duration < video_clip.duration:
        print("Extending audio to match video duration...")
        audio_clip = audio_clip.set_duration(video_clip.duration)
    
    # Set the audio to the video clip
    print("Setting audio to video clip...")
    final_clip = video_clip.set_audio(audio_clip)
    
    print("Writing final output video file with audio...")
    final_clip.write_videofile(video_path, codec='libx264', audio_codec='aac')
    print("Finished writing video with audio.")

# Example usage with your file paths
video_path = 'vids/20240607-224147.mp4'
gif_path = 'Assets/Timer/timer2.gif'
srt_path = 'gif_timings.srt'
output_path = 'StickerVid.mp4'

overlay_gif_on_video(video_path, gif_path, srt_path, output_path, position=("center", "center"))
add_audio_to_video(output_path, "finalresult.mp3")

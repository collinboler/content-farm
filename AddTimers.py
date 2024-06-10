from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioClip
import pysrt

from moviepy.editor import VideoFileClip, AudioFileClip


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
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Load the GIF and convert it to a clip
    gif_clip = VideoFileClip(gif_path, has_mask=True)
    
    # Parse the SRT file for GIF timings
    gif_timings = parse_srt_for_gif_timing(srt_path)
    
    # Create a list to hold the GIF clips with their timings
    gif_clips = []
    for start_time, end_time in gif_timings:
        gif_clip_instance = gif_clip.subclip(0, end_time - start_time).set_start(start_time).set_position(position)
        gif_clips.append(gif_clip_instance)
    
    # Create a composite video clip with the GIF overlaid on the video
    final_clip = CompositeVideoClip([video_clip] + gif_clips)

    audio = AudioFileClip("finalresult.mp3")
    final_clip = final_clip.set_audio(audio)

    # Write the output video file
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Replace the audio of the video clip with the MP3 audio
    # ideo_clip = video_clip.set_audio(audio)



def add_audio_to_video(video_path, audio_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Load the audio clip
    audio_clip = AudioFileClip(audio_path)
    
    # Ensure the audio duration matches the video duration
    if audio_clip.duration > video_clip.duration:
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    elif audio_clip.duration < video_clip.duration:
        audio_clip = audio_clip.set_duration(video_clip.duration)
    
    # Set the audio to the video clip
    final_clip = video_clip.set_audio(audio_clip)
    
    # Write the output video file, overwriting the original video
    final_clip.write_videofile(video_path, codec='libx264', audio_codec='aac')

# Example usage with your file paths

if __name__ == "__main__":
    video_path = 'vids/20240607-224147.mp4'
    gif_path = 'Assets/Timer/timer2.gif'
    srt_path = 'gif_timings.srt'
    output_path = 'StickerVid.mp4'

    overlay_gif_on_video(video_path, gif_path, srt_path, output_path, position=("center", "center"))
    add_audio_to_video(output_path, "finalresult.mp3")

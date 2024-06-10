from moviepy.editor import VideoFileClip, AudioFileClip
import random

def vid_create():
    # Load your MP4 and MP3 files
    video = VideoFileClip('background/mcpcvert.mp4')
    audio = AudioFileClip('finalresult.mp3')

    # Get the duration of the MP3 file in seconds
    audio_duration = audio.duration

    # Ensure the video is longer than the audio
    if audio_duration > video.duration:
        raise ValueError("The MP3 file is longer than the MP4 file.")

    # Choose a random start time for the clip in the video
    max_start = video.duration - audio_duration
    start_time = random.uniform(0, max_start)

    # Cut out the clip from the video
    video_clip = video.subclip(start_time, start_time + audio_duration)

    # Replace the audio of the video clip with the MP3 audio
    video_clip = video_clip.set_audio(audio)


    # Write the result to a file
    video_clip.write_videofile('output.mp4', codec='libx264', audio_codec='aac')


    # Load your video
    # clip = VideoFileClip('output.mp4')


if __name__ == "__main__":
    vid_create()




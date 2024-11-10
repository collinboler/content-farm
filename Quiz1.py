import VidScript
from AudioMash import concatenate_audio
import PauseDelete
from stringsfromfile import create_strings_from_file
from text_to_speech_file import text_to_speech_file
from VidAdd import vid_create
from Captions import create_captions
from AddCaptions import add_captions
# from AddTimers import overlay_gif_on_video
# from AddTimers import add_audio_to_video
from stickersrt import srt_create
import AddTimers
import time
import popupsrt
import AddPopups
import AddList
import listsrt
from moviepy.editor import VideoFileClip

def main():
    script_queue, answers = VidScript.script()
   
    for s in answers:
        print(s)


    for s in script_queue:
        print(s) 

    VidScript.write_to_file(script_queue, "results.txt")



    string = []
    string = create_strings_from_file("results.txt")


    text_to_speech_file(string[0], "P1.mp3")
    text_to_speech_file(string[1], "P2.mp3")
    text_to_speech_file(string[2], "P3.mp3")
    text_to_speech_file(string[3], "P4.mp3")
    text_to_speech_file(string[4], "P5.mp3")
    text_to_speech_file(string[5], "P6.mp3")
    text_to_speech_file(string[6], "P7.mp3")
    
    part_files = ["P1.mp3", "P2.mp3", "P3.mp3", "P4.mp3", "P5.mp3", "P6.mp3", "P7.mp3"]
    timer_file = "timer.mp3"
    output_file = "result.mp3"

    concatenate_audio(part_files, timer_file, output_file)


    input_file = "result.mp3"
    output_file = "finalresult.mp3"
    PauseDelete.remove_silence(input_file, output_file)

    # get background vid
    vid_create()
    # output.mp4

    # create auto captions srt
    create_captions()
    

    # add captions to video 
   
    # coutput.mp4 --> captionoutput.mp4


 # create srt for timer gif
    srt_create('subtitles.srt','gif_timings.srt')


    # # tag video with timestamp
    # timestamp = time.strftime("%Y%m%d-%H%M%S")
    # output_file = f"vids/{timestamp}.mp4"


    # Overlay timer GIF on the video
    video_path = 'output.mp4'
    gif_path = 'Assets/Timer/timer2.gif'
    srt_path = 'gif_timings.srt'
    output_path = 'StickerVid.mp4'

    #captionoutput.mp4 --> output.mp4

    AddTimers.add_gif_to_video(video_path, gif_path, srt_path, output_path)
    # overlay_gif_on_video(video_path, gif_path, srt_path, output_path, position=("center", "center"))
    # add_audio_to_video(output_path, "finalresult.mp3")



    
   # create SRT for popups
    popupsrt.create_empty_srt('gif_timings.srt', "StickerVid.mp4", 'popup.srt')

    # add popups to video

    AddPopups.main("StickerVid.mp4", 'stickers/bateman', 'popup.srt', "output.mp4")
    
    # output.mp4 --> output2.mp4 

    add_captions()

    # create list srt
     # Example usage


    # Example usage
    # subtitles_file = 'subtitles.srt'
    # new_srt_file = 'list.srt'

    listsrt.main(answers)

    # Copy answers to answers2 and modify as specified
    # answers2 = [answer.split()[0] if len(answer.split()) > 1 else answer for answer in answers]
    # answers2[1] = "specific"
    # timestamps = listsrt.extract_timestamps(subtitles_file, answers2)
    # listsrt.create_new_srt(new_srt_file, timestamps, answers)


    # subtitles_file = "subtitles.srt"
    # # answers = ['BBC', '👍', 'poodle', '26', 'Your Professor', 'Comedy']
    
    # answers2 = answers.copy()
    # answers2[1] = "this one"

    # timestamps = listsrt.extract_timestamps(subtitles_file, answers2)
    # # final_timestamp = listsrt.get_final_timestamp(subtitles_file)

    # # if len(timestamps) == len(answers2):
    # listsrt.create_new_srt(new_srt_file, timestamps, answers)
    # else:
    #     print("Not all timestamps found. Please check the input SRT file and the answers array.")



    # create timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_path = f"vids/{timestamp}.mp4"

    # ad list
   
    srt_path = "list.srt"  # Ensure you have the correct path to your SRT file
    

    AddList.add_text_to_video("captionoutput.mp4", srt_path, "output.mp4")

    increase_volume("output.mp4", output_path)

    # add_audio_to_video(output_path, "finalresult.mp3")
    # def add_audio_to_video(video_path, audio_path):
    #     """
    #     Add audio to a video file.

    #     Args:
    #         video_path (str): Path to the video file.
    #         audio_path (str): Path to the audio file.

    #     Returns:
    #         None
    #     """
    #     import moviepy.editor as mp

    #     video = mp.VideoFileClip(video_path)
    #     audio = mp.AudioFileClip(audio_path)

    #     video = video.set_audio(audio)
    #     video.write_videofile("output.mp4", codec="libx264", audio_codec="aac")


def increase_volume(input_video_path, output_video_path, factor=15.0):
    # Load the video
    video = VideoFileClip(input_video_path)
    
    # Increase the volume
    video_with_louder_audio = video.volumex(factor)
    
    # Write the result to a new file
    video_with_louder_audio.write_videofile(output_video_path, codec='libx264', audio_codec='aac')




if __name__ == "__main__":
    for i in range(1):
        main()
    
   
import VidScript
from AudioMash import concatenate_audio
import PauseDelete
from stringsfromfile import create_strings_from_file
from text_to_speech_file import text_to_speech_file
from VidAdd import vid_create
from Captions import create_captions
from AddCaptions import add_captions
from AddTimers import overlay_gif_on_video
from stickersrt import srt_create
import time
import popupsrt
import AddPopups
import AddList
import listsrt

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
    add_captions()
    # coutput.mp4 --> captionoutput.mp4


 # create srt for timer gif
    srt_create('subtitles.srt','gif_timings.srt')


    # # tag video with timestamp
    # timestamp = time.strftime("%Y%m%d-%H%M%S")
    # output_file = f"vids/{timestamp}.mp4"


    # Overlay timer GIF on the video
    video_path = 'captionoutput.mp4'
    gif_path = 'Assets/Timer/timer2.gif'
    srt_path = 'gif_timings.srt'

    #captionoutput.mp4 --> output.mp4

    overlay_gif_on_video(video_path, gif_path, srt_path, "output.mp4", position=("center", "center"))

    
   # create SRT for popups
    popupsrt.create_empty_srt('gif_timings.srt', "output.mp4", 'popup.srt')

    # add popups to video
    AddPopups.main("output.mp4", 'stickers/bateman', 'popup.srt', "output2.mp4")
    
    # output.mp4 --> output2.mp4 

    # create list srt
     # Example usage



    subtitles_file = 'subtitles.srt'
    new_srt_file = 'list.srt'
    # answers = ['BBC', '👍', 'poodle', '26', 'Your Professor', 'Comedy']
    
    answers2 = answers.copy()
    answers2[1] = "this one"

    timestamps = listsrt.extract_timestamps(subtitles_file, answers2)
    # final_timestamp = listsrt.get_final_timestamp(subtitles_file)

    # if len(timestamps) == len(answers2):
    listsrt.create_new_srt(new_srt_file, timestamps, answers)
    # else:
    #     print("Not all timestamps found. Please check the input SRT file and the answers array.")



    # create timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = f"vids/{timestamp}.mp4"

    output_path = output_file
    # ad list
   
    srt_path = 'list.srt'  # Ensure you have the correct path to your SRT file
    

    AddList.add_text_to_video("output2.mp4", srt_path, output_path)


if __name__ == "__main__":
    main()
   
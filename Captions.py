import assemblyai as aai
import os

def create_captions():
    aai.settings.api_key = "1aa12dae0dce489da66bc91d711280f8"

    transcript = aai.Transcriber().transcribe("finalresult.mp3")
    subtitles = transcript.export_subtitles_srt(chars_per_caption=15) #chars_per_caption=15


    # Delete the file "subtitles.srt"
    if os.path.isfile("subtitles.srt"):
        os.remove("subtitles.srt")

    f = open("subtitles.srt", "w")
    f.write(subtitles)
    f.close()

if __name__ == "__main__":
    create_captions()
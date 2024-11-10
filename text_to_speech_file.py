import elevenlabs
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs






ELEVENLABS_API_KEY = "63225124142cf7d0896ff733e6a22956"


client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str, save_file_path: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(

        # adam key: pNInz6obpgDQGcFmaJgB
        voice_id="TIZXPCSxhWyuUsLe5HfA", # Patrick Bateman custom voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text, 
        model_id="eleven_multilingual_v2", # use the turbo model (eleven_turbo_v2) for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=1.0, # og 0.0
            similarity_boost=1.0,
            style=0.25,  # og 0.0
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back


    # Generating a unique file name for the output MP3 file
    # save_file_path = f"{uuid.uuid4()}.mp3"
    
    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path


# print(ELEVENLABS_API_KEY)

if __name__ == "__main__" :
   text_to_speech_file("I'm patrick bateman. Though I may hide my cold gaze.", 'test.mp4')
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def remove_silence(input_file, output_file, silence_thresh=-50, min_silence_len=500, buffer=300):
    # Load the audio file
    audio = AudioSegment.from_mp3(input_file)

    # Detect non-silent chunks with conservative silence threshold
    non_silent_chunks = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # If there are no non-silent chunks detected, return the original audio
    if not non_silent_chunks:
        audio.export(output_file, format="mp3")
        return

    # Combine the non-silent chunks with buffer before and after
    new_audio = AudioSegment.empty()
    for i, (start, end) in enumerate(non_silent_chunks):
        # Add buffer before and after each chunk
        start = max(0, start - buffer)
        end = min(len(audio), end + buffer)
        chunk = audio[start:end]
        new_audio += chunk
        if i < len(non_silent_chunks) - 1:  # Don't add padding after the last chunk
            new_audio += AudioSegment.silent(duration=buffer)

    # Export the new audio file
    new_audio.export(output_file, format="mp3")

# Usage example
input_file = "result.mp3"
output_file = "finalresult.mp3"
remove_silence(input_file, output_file)

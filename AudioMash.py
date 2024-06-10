from pydub import AudioSegment

def concatenate_audio(part_files, timer_file, output_file):
    try:
        # Load the timer audio
        timer_audio = AudioSegment.from_mp3(timer_file)
        
        # Initialize an empty AudioSegment
        combined_audio = AudioSegment.empty()
        
        # Iterate over the part files and concatenate them with the timer audio
        for part_file in part_files:
            part_audio = AudioSegment.from_mp3(part_file)
            combined_audio += part_audio + timer_audio
        
        # Remove the last added timer audio segment
        combined_audio = combined_audio[:-len(timer_audio)]
        
        # Export the combined audio to the output file
        combined_audio.export(output_file, format="mp3")
        print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    part_files = ["P1.mp3", "P2.mp3", "P3.mp3", "P4.mp3", "P5.mp3", "P6.mp3", "P7.mp3"]
    timer_file = "timer.mp3"
    output_file = "result.mp3"

    concatenate_audio(part_files, timer_file, output_file)
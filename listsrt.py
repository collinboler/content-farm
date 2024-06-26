import re

def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def find_timestamp(srt_lines, search_text):
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})")
    for i, line in enumerate(srt_lines):
        if search_text in line:
            timestamp_match = pattern.search(srt_lines[i - 1])
            if timestamp_match:
                return timestamp_match.group(1)
    return None

def create_new_srt(srt_lines, answers, output_path):
    timestamps = []
    search_phrases = answers + ["this one."]
    
    for phrase in search_phrases:
        timestamp = find_timestamp(srt_lines, phrase)
        if timestamp:
            timestamps.append(timestamp)
    
    if len(timestamps) < len(search_phrases):
        print("Not all timestamps found.")
        return
    
    new_srt_content = [
        f"1\n00:00:00,000 --> {timestamps[0]}\n1. Easy (green)\n2. Easy (green)\n3. Medium (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)\n\n",
        f"2\n{timestamps[0]} --> {timestamps[1]}\n1. {answers[0]} (green)\n2. Easy (green)\n3. Medium (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)\n\n",
        f"3\n{timestamps[1]} --> {timestamps[2]}\n1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. Medium (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)\n\n",
        f"4\n{timestamps[2]} --> {timestamps[3]}\n1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)\n\n",
        f"5\n{timestamps[3]} --> {timestamps[4]}\n1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. {answers[3]} (yellow)\n5. Hard (red)\n6. Impossible (purple)\n\n",
        f"6\n{timestamps[4]} --> {timestamps[5]}\n1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. {answers[3]} (yellow)\n5. {answers[4]} (red)\n6. Impossible (purple)\n\n",
        f"7\n{timestamps[5]} --> 00:01:00,000\n1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. {answers[3]} (yellow)\n5. {answers[4]} (red)\n6. {answers[5]} (purple)\n\n",
    ]
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(new_srt_content)

# Example usage
answers = ["Keeping Up with the Kardashians",
"Labrador", "20", "Your girlfriend", "PlayStation"]
subtitles_path = 'subtitles.srt'
output_path = 'listsubtitles.srt'

srt_lines = read_srt(subtitles_path)
create_new_srt(srt_lines, answers, output_path)

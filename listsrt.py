import re

def extract_timestamps(subtitles_file, answers2):
    with open(subtitles_file, 'r') as file:
        content = file.read()

    timestamps = []
    for answer in answers2:
        pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n.*' + re.escape(answer), re.IGNORECASE)
        matches = pattern.findall(content)
        if matches:
            timestamps.extend(matches)
    
    # Get the final timestamp
    pattern_final = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    final_timestamp = None
    for match in pattern_final.finditer(content):
        final_timestamp = match.group(2)

    if timestamps and final_timestamp:
        timestamps[-1] = (timestamps[-1][0], final_timestamp)
    print(timestamps)
    return timestamps

def create_new_srt(new_srt_file, timestamps, answers):
    sections = [
        '1. Easy (green)\n2. Easy (green)\n3. Medium (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)',
        f'1. {answers[0]} (green)\n2. Easy (green)\n3. Medium (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)',
        f'1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. Medium (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)',
        f'1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. Medium (yellow)\n5. Hard (red)\n6. Impossible (purple)',
        f'1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. {answers[3]} (yellow)\n5. Hard (red)\n6. Impossible (purple)',
        f'1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. {answers[3]} (yellow)\n5. {answers[4]} (red)\n6. Impossible (purple)',
        f'1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. {answers[3]} (yellow)\n5. {answers[4]} (red)\n6. {answers[5]} (purple)'
    ]

    with open(new_srt_file, 'w') as file:
        file.write(f'1\n00:00:00,000 --> {timestamps[0][0]}\n{sections[0]}\n\n')
        for i, (start, end) in enumerate(timestamps):
            if i < len(timestamps) - 1:
                file.write(f'{i+2}\n{start} --> {timestamps[i+1][0]}\n{sections[i+1]}\n\n')
            # else:
            #     file.write(f'{i+2}\n{start} --> {end}\n{sections[i+1]}\n\n')
            #     final_section = f'1. {answers[0]} (green)\n2. {answers[1]} (green)\n3. {answers[2]} (yellow)\n4. {answers[3]} (yellow)\n5. {answers[4]} (red)\n6. {answers[5]} (purple)'
            #     file.write(f'{len(timestamps) + 2}\n{end} --> {end}\n{final_section}\n\n')

# Example usage
subtitles_file = 'subtitles.srt'
new_srt_file = 'list.srt'
answers = ['Ninja', '🤣', 'Soccer', '64', 'Your Librarian', 'Basketball']
answers2 = answers.copy()
answers2[1] = "this one"
timestamps = extract_timestamps(subtitles_file, answers2)
create_new_srt(new_srt_file, timestamps, answers)

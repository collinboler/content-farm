import re

def extract_timestamps(subtitles_file, answers2):
    with open(subtitles_file, 'r') as file:
        content = file.read()

    timestamps = []
<<<<<<< HEAD
    for answer in answers2:
=======
    for answer in answers:
>>>>>>> parent of 58d872f (list with color)
        pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n.*' + re.escape(answer), re.IGNORECASE)
        match = pattern.search(content)
        if match:
            timestamps.append((match.group(1), match.group(2)))

    return timestamps

def get_final_timestamp(subtitles_file):
    with open(subtitles_file, 'r') as file:
        lines = file.readlines()
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    last_timestamp = None
    for line in lines:
        match = pattern.search(line)
        if match:
            last_timestamp = match.group(2)
    return last_timestamp

def create_new_srt(new_srt_file, timestamps, answers, final_timestamp):
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
            else:
                file.write(f'{i+2}\n{start} --> {final_timestamp}\n{sections[i+1]}\n\n')

<<<<<<< HEAD
=======
# Example usage
subtitles_file = 'subtitles.srt'
new_srt_file = 'new_subtitles.srt'
answers = ['Stephen King', '😊', 'Apple', '27', 'Your Colleague', 'Beach']
>>>>>>> parent of 58d872f (list with color)

if __name__ == '__main__':
    # Example usage
    subtitles_file = 'subtitles.srt'
    new_srt_file = 'list.srt'
    answers = ['BBC', '👍', 'poodle', '26', 'Your Professor', 'Comedy']
    answers2 = ['BBC', 'this one', 'poodle', '26', 'Your Professor', 'Comedy']

    timestamps = extract_timestamps(subtitles_file, answers2)
    final_timestamp = get_final_timestamp(subtitles_file)

    if len(timestamps) == len(answers2):
        create_new_srt(new_srt_file, timestamps, answers, final_timestamp)
    else:
        print("Not all timestamps found. Please check the input SRT file and the answers array.")

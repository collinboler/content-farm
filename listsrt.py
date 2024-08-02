import re

import inflect

p = inflect.engine()

# def number_to_words(text):
#     return p.number_to_words(text) if text.isdigit() else text

def extract_timestamps(subtitles_file, answers2):
    with open(subtitles_file, 'r') as file:
        content = file.read()

    timestamps = []
    playstation_count = 0

    for answer in answers2:
        pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n.*' + re.escape(answer), re.IGNORECASE)
        matches = pattern.findall(content)
        if matches:
            if answer == answers2[-1]: # - 1
                for match in matches:
                    playstation_count += 1
                    if playstation_count > 1:
                        timestamps.append(match)
            else:
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
            section_index = min(i + 1, len(sections) - 1)
            if i < len(timestamps) - 1:
                file.write(f'{i+2}\n{start} --> {timestamps[i+1][0]}\n{sections[section_index]}\n\n')
            else:
                file.write(f'{i+2}\n{start} --> {end}\n{sections[section_index]}\n\n')

def modify_srt_file(input_srt_file, output_srt_file):
    """
    Modify the SRT file according to the specified changes and save the result to a new file.
    """
    def parse_srt(srt_content):
        """
        Parse the SRT file content into a list of dictionaries.
        """
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n(?=\d+\n|\Z)', re.DOTALL)
        matches = pattern.findall(srt_content)

        subtitles = []
        for match in matches:
            subtitles.append({
                'index': int(match[0]),
                'start': match[1],
                'end': match[2],
                'text': match[3].strip()
            })

        return subtitles

    def format_srt(subtitles):
        """
        Format the list of dictionaries into SRT file content.
        """
        formatted_srt = ""
        for subtitle in subtitles:
            formatted_srt += f"{subtitle['index']}\n"
            formatted_srt += f"{subtitle['start']} --> {subtitle['end']}\n"
            formatted_srt += f"{subtitle['text']}\n\n"
        return formatted_srt.strip()

    def modify_srt(subtitles):
        """
        Modify the SRT content as specified.
        """
        # Adjust the end timestamp of the 6th subtitle to the start of the last subtitle
        subtitles[5]['end'] = subtitles[-2]['start']

        # Remove the 7th subtitle
        del subtitles[6]

        # Re-index the subtitles
        for i in range(len(subtitles)):
            subtitles[i]['index'] = i + 1

        return subtitles

    # Read the original SRT file
    with open(input_srt_file, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # Parse the SRT content
    subtitles = parse_srt(srt_content)

    # Modify the SRT content
    modified_subtitles = modify_srt(subtitles)

    # Format the modified SRT content
    modified_srt_content = format_srt(modified_subtitles)

    # Write the modified SRT content to a new file
    with open(output_srt_file, 'w', encoding='utf-8') as file:
        file.write(modified_srt_content)

    print(f"Modified SRT file has been saved as {output_srt_file}")

def main(answers):
    subtitles_file = 'subtitles.srt'
    new_srt_file = 'list.srt'
   

    # Copy answers to answers2 and modify as specified
    answers2 = answers.copy()
   
    # answers2[3] = number_to_words(answers2[3])
    
    answers2 = [s.replace('-', ' ') for s in answers2]
    
    answers2 = [answer.split()[1] if len(answer.split()) > 1 else answer for answer in answers]

    answers2[1] = "specific"
  
    
    for answer in answers2:
        print(answer)

    print('answers2p[1]: ' + answers2[1])

    timestamps = extract_timestamps(subtitles_file, answers2)
    for timestamp in timestamps:
        print(timestamp)
    
    create_new_srt(new_srt_file, timestamps, answers)
    # modify_srt_file(new_srt_file, new_srt_file)

# Call main function
if __name__ == "__main__":
   answers = ["Stephen King", "👀", "Harry Potter", "Forest Green", "Your Coach", "Fiction"]
   main(answers)

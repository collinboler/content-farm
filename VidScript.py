import random
from collections import deque
from text_to_speech_file import text_to_speech_file
from stringsfromfile import create_strings_from_file

def random_line(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        random_index = random.randint(0, len(lines) - 1)
        return lines[random_index].strip()
    except IOError as e:
        print(f"Error: Could not read file. {e}")
        return ""

def random_2_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        if len(lines) % 2 != 0:
            raise ValueError("The file does not contain an even number of lines.")
        line_pairs = [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines), 2)]
        random_index = random.randint(0, len(line_pairs) - 1)
        return line_pairs[random_index]
    except IOError as e:
        return ["Error: Could not read file.", str(e)]
    except ValueError as e:
        return [str(e), ""]

def randomL():
    return random_line("files/Lose.txt")

def randomC():
    return random_line("files/Chose.txt")

def randomQ1():
    return random_2_lines("files/celebs.txt")

def randomQ3():
    return random_2_lines("files/Questions.txt")

def randomQ4():
    return random_2_lines("files/picknumber.txt")

def randomQ6():
    return random_2_lines("files/5050.txt")

def end(string):
    return f"{randomC()} {string} {randomL()}"

def quip():
    return random_line("files/Quip.txt")

def script():
    script_queue = deque()
    script_queue.append("") # Question 1
    Q1 = randomQ1()
    script_queue.append(Q1[0])
    script_queue.append(end(Q1[1]))

    script_queue.append(random_line("files/NoSame.txt"))

    script_queue.append("Question 2.")
    script_queue.append("Press and hold the comment button and select one of the four emojis")
    script_queue.append(end("this one"))

    script_queue.append("Question 3.")
    Q3 = randomQ3()
    script_queue.append(Q3[0])
    script_queue.append(end(Q3[1]))

    script_queue.append("Question 4.")
    Q4 = randomQ4()
    script_queue.append(Q4[0])
    script_queue.append(end(Q4[1]))

    script_queue.append("Question 5.")
    script_queue.append("Who appears when you click share and more?")
    script_queue.append(end(random_line("files/Names.txt")))
    script_queue.append((random_line("files/Impossible.txt")))

    script_queue.append("Question 6.")
    Q6 = randomQ6()
    script_queue.append(Q6[0])
    script_queue.append(end(Q6[1]))

    return script_queue

def write_to_file(queue, file_name):
    try:
        with open(file_name, 'w') as file:
            for line in queue:
                file.write(line + "\n")
    except IOError as e:
        print(f"Error: Could not write to file. {e}")


if __name__ == "__main__":
    script_queue = script()
    for s in script_queue:
        print(s) 

    write_to_file(script_queue, "results.txt")
    string = []
    string = create_strings_from_file("results.txt")


    text_to_speech_file(string[0], "P1.mp3")
    text_to_speech_file(string[1], "P2.mp3")
    text_to_speech_file(string[2], "P3.mp3")
    text_to_speech_file(string[3], "P4.mp3")
    text_to_speech_file(string[4], "P5.mp3")
    text_to_speech_file(string[5], "P6.mp3")
    text_to_speech_file(string[6], "P7.mp3")
   




#if __name__ == "__main__":
#    script_queue = script()
#    for s in script_queue:
#        print(s)
#    
#    write_to_file(script_queue, "results.txt")


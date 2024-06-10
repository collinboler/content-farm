import random

def random_line(file_path):
    try:
        # Step 1: Read all lines from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Step 2: Randomly select one line from the list
        random_index = random.randint(0, len(lines) - 1)
        random_line = lines[random_index].strip()

        return random_line

    except IOError as e:
        print(f"Error: Could not read file. {e}")
        return ""

# Example usage
if __name__ == "__main__":
    file_path = "your_file_path.txt"
    result = random_line(file_path)
    print(result)

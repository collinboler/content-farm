import random

def random_2_lines(file_path):
    try:
        # Read all lines from the file into a list
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Ensure there are an even number of lines
        if len(lines) % 2 != 0:
            raise ValueError("The file does not contain an even number of lines.")
        
        # Create a list of tuples, each containing two consecutive lines
        line_pairs = [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines), 2)]
        
        # Generate a random index
        random_index = random.randint(0, len(line_pairs) - 1)
        
        # Get random pair
        return line_pairs[random_index]

    except IOError:
        return ["Error: Could not read file."]
    
    except ValueError as e:
        return [str(e)]

# Example usage
if __name__ == "__main__":
    file_path = "your_file_path.txt"
    result = random_2_lines(file_path)
    print(result)

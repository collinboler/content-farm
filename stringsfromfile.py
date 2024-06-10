def create_strings_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        
        strings = []

        # Ensure there are at least 19 lines
        #if len(lines) < 19:
        #    raise ValueError("The file does not contain at least 19 lines.")

        strings.append(lines[0] + " " + lines[1])
        strings.append(lines[2] + " " + lines[3] + " " + lines[4] + " " + lines[5])
        strings.append(lines[6] + " " + lines[7] + " " + lines[8])
        strings.append(lines[9] + " " + lines[10] + " " + lines[11])
        strings.append(lines[12] + " " + lines[13] + " " + lines[14])
        strings.append(lines[15] + " " + lines[16] + " " + lines[17] + lines[18])
        strings.append(lines[19])

        return strings

    except IOError as e:
        print(f"Error: Could not read file. {e}")
        return []
    except ValueError as e:
        print(f"Error: {e}")
        return []

# Example usage
if __name__ == "__main__":
    file_path = "files/your_file.txt"
    result_strings = create_strings_from_file(file_path)
    for s in result_strings:
        print(s)

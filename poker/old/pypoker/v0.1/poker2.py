# Prints red text with a white background in the console using ANSI escape codes

def print_red(text):
    print(f'\033[1;31;47m{text}\033[0m')

def print_black(text):
    print(f'\033[1;90;47m{text}\033[0m')

# Example usage
print_red("This is red text on white background.")
print_black("This is black text on white background.")
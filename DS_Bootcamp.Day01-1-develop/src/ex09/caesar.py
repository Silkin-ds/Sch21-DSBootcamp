import sys

def caesar_cipher(text, shift, encode=True):
    result = []
    for char in text:
        if char.isalpha():
            if not char.isascii():
                raise ValueError("The script does not support your language yet.")
            offset = ord('a') if char.islower() else ord('A')
            if encode:
                new_char = chr((ord(char) - offset + shift) % 26 + offset)
            else:
                new_char = chr((ord(char) - offset - shift) % 26 + offset)
            result.append(new_char)
        elif char in [' ', '-', '@', '.', '_', ':', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            result.append(char)
        else:
            raise ValueError("The script does not support your language yet.")
    return ''.join(result)

def main():
    if len(sys.argv) != 4:
        raise ValueError("Incorrect number of arguments. Usage: python3 caesar.py <encode|decode> '<text>' <shift>")
    
    action = sys.argv[1].lower() 
    text = sys.argv[2].strip("'\"")
    shift_str = sys.argv[3]

    if not (shift_str.lstrip('-').isdigit() and (shift_str.count('-') <= 1)):
        raise ValueError("Shift must be an integer.")
    shift = int(shift_str)

    if action == 'encode':
        encoded_text = caesar_cipher(text, shift, encode=True)
        print(encoded_text)
    elif action == 'decode':
        decoded_text = caesar_cipher(text, shift, encode=False)
        print(decoded_text)
    else:
        raise ValueError("Invalid action. Use 'encode' or 'decode'.")

if __name__ == "__main__":
    main()
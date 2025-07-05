class Must_read():
    filename = "data.csv"
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}'not found.")

if __name__ == '__main__':
    Must_read()
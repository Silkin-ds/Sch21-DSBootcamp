class Research():
    def file_reader(self):
        filename = "data.csv"
        try:
            with open(filename,'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found.")

if __name__ == '__main__':
    research = Research()
    print(research.file_reader())
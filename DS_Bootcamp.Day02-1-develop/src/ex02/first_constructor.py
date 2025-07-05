import sys
import os
class Research():
    def __init__(self, file):
        self.file = file
    
    def file_reader(self):
        if not os.path.exists(self.file):
            raise FileNotFoundError(f'File {self.file} not found')
        with open(self.file, 'r') as input:
                lines = input.readlines()
        if len(lines) < 2:
            raise ValueError("Script not support null data")
        if len(lines[0].strip().split(',')) != 2:
            raise ValueError("Script not support this header")
        for line in lines[1:]:
            value = line.strip().split(',')
            if len(value) != 2 or (value[0] != '0' and value[0] != '1') or (value[1] != '0' and value[1] != '1'):
                raise ValueError('Values not support')
            if value[0] == value[1]:
                raise ValueError('Values must be different')
        return ''.join(lines)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments is given")
    else:
        res = Research(sys.argv[1])
        print(res.file_reader())
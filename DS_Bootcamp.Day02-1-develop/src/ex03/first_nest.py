import sys
import os

class Research():
    def __init__(self, file):
        self.file = file

    def file_reader(self, flag_header=True):
        if not os.path.exists(self.file):
            raise FileNotFoundError(f'File {self.file} not found')
        with open(self.file, 'r') as input_file:
            lines = input_file.readlines()
        if len(lines) < 1:
            raise ValueError("File is empty")
        if flag_header:
            header = lines[0].strip().split(',')
            if len(header) != 2:
                raise ValueError("Script does not support this header")
            lines = lines[1:]
        data = []
        for line in lines:
            values = line.strip().split(',')
            if len(values) != 2 or (values[0] not in ['0', '1']) or (values[1] not in ['0', '1']):
                raise ValueError('Values not supported')
            if values[0] == values[1]:
                raise ValueError('Values must be different')
            data.append([int(values[0]), int(values[1])])  
        return data

    class Calculations():
        def counts(self, data):
            head_count = sum(row[0] for row in data)
            tail_count = sum(row[1] for row in data)
            return head_count, tail_count

        def fractions(self, head_count, tail_count):
            total = head_count + tail_count
            if total == 0:
                raise ValueError("No data to calculate fractions")
            head_fraction = (head_count / total) * 100
            tail_fraction = (tail_count / total) * 100
            return head_fraction, tail_fraction


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments is given")
    research = Research(sys.argv[1])
    data = research.file_reader(flag_header=True)
    print(data)
    calculations = research.Calculations()
    head_count, tail_count = calculations.counts(data)
    print(head_count, tail_count)
    head_fraction, tail_fraction = calculations.fractions(head_count, tail_count)
    print(head_fraction, tail_fraction)
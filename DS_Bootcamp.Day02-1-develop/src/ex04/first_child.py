import sys
import os
import random

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
        def __init__(self, data):
            self.data = data

        def counts(self):
            head_count = sum(row[0] for row in self.data)
            tail_count = sum(row[1] for row in self.data)
            return head_count, tail_count

        def fractions(self, head_count, tail_count):
            total = head_count + tail_count
            if total == 0:
                raise ValueError("No data to calculate fractions")
            head_fraction = (head_count / total) * 100
            tail_fraction = (tail_count / total) * 100
            return head_fraction, tail_fraction

    class Analytics(Calculations):
        def __init__(self, data):
            super().__init__(data)

        def predict_random(self, num_predictions):
            predictions = []
            for _ in range(num_predictions):
                prediction = random.choice([[0, 1], [1, 0]])
                predictions.append(prediction)
            return predictions

        def predict_last(self):
            if not self.data:
                raise ValueError("No data available")
            return self.data[-1]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments is given")
    research = Research(sys.argv[1])
    data = research.file_reader(flag_header=True)
    analytics = research.Analytics(data)
    head_count, tail_count = analytics.counts()
    head_fraction, tail_fraction = analytics.fractions(head_count, tail_count)
    random_predictions = analytics.predict_random(3)
    last_prediction = analytics.predict_last()
    print("Data from file_reader():")
    print(data)
    print("\nCounts from counts():")
    print(head_count, tail_count)
    print("\nFractions from fractions():")
    print(head_fraction, tail_fraction)
    print("\nList of lists from predict_random() for 3 steps:")
    print(random_predictions)
    print("\nList from predict_last():")
    print(last_prediction)
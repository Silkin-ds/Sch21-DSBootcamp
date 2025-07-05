import os
from random import randint

class Research:
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

    class Calculations:
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
                prediction = [randint(0, 1), randint(0, 1)]
                if prediction[0] == prediction[1]:
                    prediction[1] = 1 - prediction[0]
                predictions.append(prediction)
            return predictions

        def predict_last(self):
            if not self.data:
                raise ValueError("No data available")
            return self.data[-1]

        def save_file(self, data, filename, extension):
            full_filename = f"{filename}.{extension}"
            with open(full_filename, 'w') as file:
                file.write(data)
            print(f"File saved as {full_filename}")
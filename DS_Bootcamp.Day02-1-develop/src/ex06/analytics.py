import os
import logging
import urllib
import json
import ssl
from random import randint
from urllib import request
from urllib import error
from config import LOG_FILE, LOG_FORMAT, TELEGRAM_API_URL, TELEGRAM_CHAT_ID

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)
ssl_context = ssl._create_unverified_context()

class Research:
    def __init__(self, file):
        self.file = file
        logging.info(f"Initialized Research with file: {file}")

    def file_reader(self, flag_header=True):
        logging.info("Reading file")
        if not os.path.exists(self.file):
            logging.error(f"File {self.file} not found")
            raise FileNotFoundError(f'File {self.file} not found')
        with open(self.file, 'r') as input_file:
            lines = input_file.readlines()
        if len(lines) < 1:
            logging.error("File is empty")
            raise ValueError("File is empty")
        if flag_header:
            header = lines[0].strip().split(',')
            if len(header) != 2:
                logging.error("Script does not support this header")
                raise ValueError("Script does not support this header")
            lines = lines[1:]
        data = []
        for line in lines:
            values = line.strip().split(',')
            if len(values) != 2 or (values[0] not in ['0', '1']) or (values[1] not in ['0', '1']):
                logging.error("Values not supported")
                raise ValueError('Values not supported')
            if values[0] == values[1]:
                logging.error("Values must be different")
                raise ValueError('Values must be different')
            data.append([int(values[0]), int(values[1])])  
        logging.info("File read successfully")
        return data

    def send_telegram_message(self, message):
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        data = json.dumps(payload).encode('utf-8')
        url = TELEGRAM_API_URL
        headers = {'Content-Type': 'application/json'}
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req, context=ssl_context) as response:
                response_data = response.read().decode('utf-8')
                logging.info("Telegram message sent successfully")
        except urllib.error.URLError as e:
            logging.error(f"Failed to send Telegram message: {e}")

class Calculations:
    def __init__(self, data):
        self.data = data
        logging.info("Initialized Calculations with data")

    def counts(self):
        logging.info("Calculating counts of heads and tails")
        head_count = sum(row[0] for row in self.data)
        tail_count = sum(row[1] for row in self.data)
        logging.info(f"Counts calculated: heads={head_count}, tails={tail_count}")
        return head_count, tail_count

    def fractions(self, head_count, tail_count):
        logging.info("Calculating fractions of heads and tails")
        total = head_count + tail_count
        if total == 0:
            logging.error("No data to calculate fractions")
            raise ValueError("No data to calculate fractions")
        head_fraction = (head_count / total) * 100
        tail_fraction = (tail_count / total) * 100
        logging.info(f"Fractions calculated: heads={head_fraction:.2f}%, tails={tail_fraction:.2f}%")
        return head_fraction, tail_fraction

class Analytics(Calculations):
    def __init__(self, data):
        super().__init__(data)
        logging.info("Initialized Analytics with data")

    def predict_random(self, num_predictions):
        logging.info(f"Generating {num_predictions} random predictions")
        predictions = []
        for _ in range(num_predictions):
            prediction = [randint(0, 1), randint(0, 1)]
            if prediction[0] == prediction[1]:
                prediction[1] = 1 - prediction[0]
            predictions.append(prediction)
        logging.info(f"Predictions generated: {predictions}")
        return predictions

    def predict_last(self):
        logging.info("Getting the last observation")
        if not self.data:
            logging.error("No data available")
            raise ValueError("No data available")
        last_prediction = self.data[-1]
        logging.info(f"Last observation: {last_prediction}")
        return last_prediction

    def save_file(self, data, filename, extension):
        logging.info(f"Saving data to {filename}.{extension}")
        full_filename = f"{filename}.{extension}"
        with open(full_filename, 'w') as file:
            file.write(data)
        logging.info(f"File saved as {full_filename}")
        print(f"File saved as {full_filename}")
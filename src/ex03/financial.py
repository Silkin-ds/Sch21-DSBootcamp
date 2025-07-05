#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import requests
import time
from fake_useragent import UserAgent

def financial_data(ticker, field):
    url=f"https://finance.yahoo.com/quote/{ticker}/financials/"
    user = UserAgent()
    headers = {'User-Agent':user.random}
    page = requests.get(url, headers = headers)
    if page.status_code != 200:
        raise Exception(f"Error read url {page.status_code}")
    time.sleep(5)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("div",{"class": "tableBody yf-9ft13"})
    if not table:
        raise Exception(f"Error financial {ticker}")
    tuple_result = ()
    for row in table.find_all('div', recursive=False):
        header_cell = row.find('div', {'class': 'rowTitle'})
        header = header_cell.text
        if header == field:
            values = [cell.text.strip() for cell in row.find_all('div', {'class': 'column'})]
            tuple_result = tuple(values)
    if not tuple_result:
        raise ValueError("The field not found")
    return tuple_result    

def main():
    if len(sys.argv) != 3:
        raise ValueError("You shoud write python finacial.py <symbol> <field>")
    ticker = sys.argv[1]
    field = sys.argv[2]
    result = financial_data(ticker, field)
    print(result)

if __name__ =="__main__":
    try:
        main()
    except Exception as e:
        print (e)
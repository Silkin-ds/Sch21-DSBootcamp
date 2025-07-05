#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import requests
import time
from fake_useragent import UserAgent
import pytest

def financial_data(ticker, field):
    url = f"https://finance.yahoo.com/quote/{ticker}/financials/"
    user = UserAgent()
    headers = {'User-Agent': user.random}
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        raise Exception(f"Error read url {page.status_code}")
    time.sleep(5)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("div", {"class": "tableBody yf-9ft13"})
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
        raise ValueError("You should write python financial.py <symbol> <field>")
    ticker = sys.argv[1]
    field = sys.argv[2]
    result = financial_data(ticker, field)
    print(result)

def test_financial_data_valid_ticker_and_field():
    ticker = "MSFT"
    field = "Total Revenue"
    result = financial_data(ticker, field)
    assert result, "Результат не должен быть пустым"
    assert all(isinstance(item, str) for item in result), "Все элементы должны быть строками"

def test_financial_data_invalid_ticker():
    ticker = "INVALID_TICKER"
    field = "Total Revenue"
    with pytest.raises(Exception):
        financial_data(ticker, field)

def test_financial_data_null_ticker():
    ticker = ""
    field = "Total Revenue"
    with pytest.raises(Exception):
        financial_data(ticker, field)

def test_financial_data_invalid_field():
    ticker = "MSFT"
    field = "Invalid Field"
    with pytest.raises(ValueError):
        financial_data(ticker, field)

def test_financial_data_return_type():
    ticker = "MSFT"
    field = "Total Revenue"
    result = financial_data(ticker, field)
    assert isinstance(result, tuple), "Функция должна возвращать кортеж"

def test_financial_data_empty_values():
    ticker = "MSFT"
    field = "Empty Field"
    with pytest.raises(ValueError):
        financial_data(ticker, field)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "-m":
        main()
    else:
        pytest.main([__file__])
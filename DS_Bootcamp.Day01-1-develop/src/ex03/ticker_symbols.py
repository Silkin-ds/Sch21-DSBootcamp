import sys

COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
}

STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
}

def get_price(flag):
    to_company = {v: k for k, v in COMPANIES.items()}
    company = to_company.get(flag)
    if company:
        stock_price = STOCKS.get(flag)
        return f"{company} {stock_price}"
    else:
        return "Unknown ticker"

def main():
    if len(sys.argv) != 2:
        return
    flag = sys.argv[1].upper()
    result = get_price(flag)
    print(result)

if __name__ == "__main__":
    main()
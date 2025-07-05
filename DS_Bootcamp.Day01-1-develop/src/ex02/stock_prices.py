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

def get_price(company_name):
    company_name = company_name.lower()
    companies_lower = {k.lower(): v for k, v in COMPANIES.items()}
    flag = companies_lower.get(company_name)
    if flag:
        return STOCKS.get(flag, "Unknown company")
    else:
        return "Unknown company"

def main():
    if len(sys.argv) != 2:
        return

    company_name = sys.argv[1]
    stock_price = get_price(company_name)
    print(stock_price)

if __name__ == "__main__":
    main()
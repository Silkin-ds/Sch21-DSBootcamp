import sys

def stocks():
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

    if len(sys.argv)!=2:
        return
    
    line=sys.argv[1]
    expressions=[e.strip() for e in line.split(",")]
    if ",," in line or " " in line:
        return

    for exp in expressions:
        e_u=exp.upper()
        e_c=exp.capitalize()
        flag = False

        if e_u in STOCKS:
            company_name = next(key for key, value in COMPANIES.items() if value == e_u)
            print(f"{e_u} is a ticker symbol for {company_name}")
            flag = True
        elif e_c in COMPANIES:
            print(f"{e_c} stock price is {STOCKS[COMPANIES[e_c]]}")
            flag = True
        if not flag:
            print(f"{exp} is an unknown company or an unknown ticker symbol")

if __name__ == '__main__':
    stocks()
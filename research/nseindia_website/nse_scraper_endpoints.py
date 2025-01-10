import requests

def fetch_stock_data(stock_code):
    #url = f"https://www.nseindia.com/api/quote-equity?symbol={stock_code}"
    #url = f"https://www.nseindia.com/api/allIndices"
    url = f"https://www.nseindia.com/api/historical/cm/equity?symbol=INFY&series=[EQ]&from=01-01-2023&to=31-05-2023"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36',
        'Referer': 'https://www.nseindia.com/get-quotes/equity'
    }

    session = requests.Session()
    session.headers.update(headers)

    # Perform an initial request to get cookies
    session.get("https://www.nseindia.com")

    # Fetch stock data
    response = session.get(url)
    data = response.json()
    print(data)

if __name__ == "__main__":
    stock_code = "TATAELXSI"
    fetch_stock_data(stock_code)

Market Watch and Stock Data
Equity Quote Details

URL: https://www.nseindia.com/api/quote-equity?symbol=<SYMBOL>
Replace <SYMBOL> with the stock code, e.g., TATAELXSI.
Example:
arduino
Copy code
https://www.nseindia.com/api/quote-equity?symbol=TATAELXSI
Index Details

URL: https://www.nseindia.com/api/allIndices
Fetches all index data (e.g., NIFTY50, NIFTY100).
Option Chain Data

URL (for equities):
vbnet
Copy code
https://www.nseindia.com/api/option-chain-equities?symbol=<SYMBOL>
Replace <SYMBOL> with the stock code.
Example:
vbnet
Copy code
https://www.nseindia.com/api/option-chain-equities?symbol=RELIANCE
Equity Historical Data

URL: https://www.nseindia.com/api/historical/cm/equity?symbol=<SYMBOL>&series=[EQ]&from=<DD-MM-YYYY>&to=<DD-MM-YYYY>
Example:
vbnet
Copy code
https://www.nseindia.com/api/historical/cm/equity?symbol=INFY&series=[EQ]&from=01-01-2023&to=31-12-2023
Indices and Market Overview
All Market Indices

URL: https://www.nseindia.com/api/allIndices
Fetches data for all NSE indices.
Gainers and Losers

Top Gainers (Equity):
perl
Copy code
https://www.nseindia.com/api/live-analysis-variations?index=gainers
Top Losers (Equity):
perl
Copy code
https://www.nseindia.com/api/live-analysis-variations?index=losers
Pre-Open Market Data

URL: https://www.nseindia.com/api/market-status
Provides pre-market status and details.
Derivatives
Option Chain Data

URL: https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY
For other indices, replace NIFTY with the desired index.
Futures and Options (F&O)

URL: https://www.nseindia.com/api/live-analysis-variations?index=derivatives
Other Useful APIs
Corporate Actions

URL: https://www.nseindia.com/api/corporates-corp-actions
Market Status

URL: https://www.nseindia.com/api/market-status
Index Constituents

URL: https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050
Replace NIFTY%2050 with other indices like NIFTY%20100.
Bulk Deals

URL: https://www.nseindia.com/api/bulk-deals
Block Deals

URL: https://www.nseindia.com/api/block-deals
Important Notes
Headers and Cookies:

NSE's APIs require proper headers and cookies for requests to succeed. Use a browser (like Chrome DevTools) to inspect the headers used by the site and replicate them in your code.
Example headers:
python
Copy code
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://www.nseindia.com/",
}
Session Handling:

NSE uses anti-bot techniques, so maintaining cookies and session headers between requests is critical.
Legal Considerations:

These endpoints are intended for NSE's internal use. Ensure compliance with their terms of service if you plan to use them.
Example: Fetch Stock Quote with requests
python
Copy code
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://www.nseindia.com/",
}

url = "https://www.nseindia.com/api/quote-equity?symbol=TATAELXSI"

session = requests.Session()
response = session.get(url, headers=headers)
print(response.json())
Let me know if you need help implementing or debugging any of these endpoints!
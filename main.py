import requests
import itertools
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHAVANTAGE_API_END = "https://www.alphavantage.co/query"
ALPHAVANTAGE_API_KEY = "Your key"

NEWS_API_END = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "Your key"

YOUR_EMAIL = ""
YOUR_PASSWORD = ""

PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_API_KEY
}

response = requests.get(url=ALPHAVANTAGE_API_END, params=PARAMS)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
data = dict(itertools.islice(data.items(), 2))
values = []

for key in data:
    number = data[key]["4. close"]
    number = number.replace(".", "")
    values.append(round(float(number)))

percent = round((values[1] - values[0]) * 100 / values[0], 2)

PARAMS = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
}

news_response = requests.get(url=NEWS_API_END, params=PARAMS)
news_response.raise_for_status()
articles = news_response.json()["articles"][:1]
formatted_article = f"Headline: {articles['title']}. \nBrief: {articles['description']}"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=YOUR_EMAIL, password=YOUR_PASSWORD)
    connection.sendmail(
        from_addr=YOUR_EMAIL,
        to_addrs=YOUR_EMAIL,
        msg=formatted_article)

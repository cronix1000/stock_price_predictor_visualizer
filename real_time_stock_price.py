import requests
import json


def real_time_price(ticker):
    api_key = load_api_key()
    symbol = ticker
    api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        print(response.text)
        return response.json()["price"]
    else:
        print("Error:", response.status_code, response.text)

def load_api_key():
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
        return secrets.get('ninja_api_key', '')
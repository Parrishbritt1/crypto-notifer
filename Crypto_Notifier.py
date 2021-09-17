import requests
import time
from datetime import datetime
from config import IFTTT_WEBHOOKS_URL, BITCOIN_API_URL, ETHEREUM_API_URL, LITECOIN_API_URL


IFTTT_WEBHOOKS_URL = IFTTT_WEBHOOKS_URL
BITCOIN_API_URL = BITCOIN_API_URL
ETHEREUM_API_URL = ETHEREUM_API_URL
LITECOIN_API_URL = LITECOIN_API_URL

class Bitcoin:

    def retrieve_data(self):
        btc_response = requests.get(BITCOIN_API_URL)
        btc_response_json = btc_response.json()
        self.data = {}
        self.data["price"] = float(btc_response_json[0]["current_price"])
        self.data["24h_change"] = float(btc_response_json[0]["price_change_percentage_24h_in_currency"])
        self.data["name"] = btc_response_json[0]["name"]
        return self.data


class Ethereum:

    def retrieve_data(self):
        eth_response = requests.get(ETHEREUM_API_URL)
        eth_response_json = eth_response.json()
        self.data = {}
        self.data["price"] = float(eth_response_json[0]["current_price"])
        self.data["24h_change"] = float(eth_response_json[0]["price_change_percentage_24h_in_currency"])
        self.data["name"] = eth_response_json[0]["name"]
        return self.data

class Litecoin:

    def retrieve_data(self):
        ltc_response = requests.get(LITECOIN_API_URL)
        ltc_response_json = ltc_response.json()
        self.data = {}
        self.data["price"] = float(ltc_response_json[0]["current_price"])
        self.data["24h_change"] = float(ltc_response_json[0]["price_change_percentage_24h_in_currency"])
        self.data["name"] = ltc_response_json[0]["name"]
        return self.data


def post_ifttt_webhook(event, values):
    data = {"value1": values[0], "value2": values[1], "value3": values[2]}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)

def get_data():
    btcData = Bitcoin().retrieve_data()
    ethData = Ethereum().retrieve_data()
    ltcData = Litecoin().retrieve_data()

    return btcData, ethData, ltcData


data = get_data()

btcData = data[0]
ethData = data[1]
ltcData = data[2]


post_ifttt_webhook("send_notif", [btcData["name"], btcData["price"], round(btcData["24h_change"], 2)])
post_ifttt_webhook("send_notif", [ethData["name"], ethData["price"], round(ethData["24h_change"], 2)])
post_ifttt_webhook("send_notif", [ltcData["name"], ltcData["price"], round(ltcData["24h_change"], 2)])

print("Bitcoin price: ", btcData["price"])
print("24h Price Change", round(btcData["24h_change"], 2))
print("*"*100)

print("Ethereum price: ", ethData["price"])
print("24h Price Change", round(ethData["24h_change"], 2))
print("*"*100)

print("Litecoin price: ", ltcData["price"])
print("24h Price Change", round(ltcData["24h_change"], 2))
print("*"*100)
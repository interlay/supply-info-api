from flask import Flask, json
import requests

SUBSCAN_URL = "https://kintsugi.api.subscan.io/"

def from_10_decimals(val):
    return val / 1_000_000_000_000

def from_8_decimals(val):
    return val / 10_000_000_000

api = Flask(__name__)

@api.route('/kint-supply', methods=['GET'])
def get_kint_supply():
    token_info_subscan = requests.get(SUBSCAN_URL + "api/scan/token").json()["data"]["detail"]
    unvested_supply = from_10_decimals(int(token_info_subscan["KINT"]["available_balance"]))
    system_accounts_subscan = requests.post("https://kintsugi.api.subscan.io/api/scan/accounts", json={"filter": "system", "row": 25,"page": 0}).json()["data"]["list"]
    system_accounts_supply = sum([float(a["balance"]) for a in system_accounts_subscan])
    circulating_supply = unvested_supply - system_accounts_supply
    return str(circulating_supply)

        
@api.route('/kbtc-supply', methods=['GET'])
def get_kbtc_supply():
    token_info_subscan = requests.get(SUBSCAN_URL + "api/scan/token").json()["data"]["detail"]
    kBTC_supply = from_10_decimals(int(token_info_subscan["KBTC"]["available_balance"]))
    return str(kBTC_supply)

if __name__ == '__main__':
    api.run() 
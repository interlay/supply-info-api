from flask import Flask, json
import requests
import os

SUBSCAN_URL = "https://interlay.api.subscan.io/"

API_KEY = os.environ.get('SUBSCAN_API_KEY')

CROWDLOAN_VESTING_END = 4838400

def from_10_decimals(val):
    return val / 10_000_000_000

def from_8_decimals(val):
    return val / 100_000_000

def subscan_get_request(url):
    headers_dict = {
        'content-type': 'application/json',
        'X-API-KEY' : API_KEY}
    return requests.get(url)
    

def subscan_post_request(url, json):
    headers_dict = {
        'content-type': 'application/json',
        'X-API-KEY' : API_KEY}
    return requests.post(url,json=json)
    

def max_crowdloan_vested():
    current_block = int(subscan_get_request(SUBSCAN_URL + "api/scan/metadata").json()["data"]["blockNum"])
    return 0.3 + (current_block / CROWDLOAN_VESTING_END)

api = Flask(__name__)

@api.route('/intr-circ-supply', methods=['GET'])
def get_intr_circ_supply():
    token_info_subscan = subscan_get_request(SUBSCAN_URL + "api/scan/token").json()["data"]["detail"]
    unvested_supply = from_10_decimals(int(token_info_subscan["INTR"]["available_balance"]))
    print(token_info_subscan["INTR"]["available_balance"])
    system_accounts_subscan = subscan_post_request(SUBSCAN_URL + "api/scan/accounts", json={"filter": "system", "row": 25,"page": 0}).json()["data"]["list"]
    system_accounts_supply = sum([float(a["balance"]) for a in system_accounts_subscan])
    circulating_supply = unvested_supply - system_accounts_supply
    print(max_crowdloan_vested())
    return str(circulating_supply)

@api.route('/intr-total-supply', methods=['GET'])
def get_kint_total_supply():
    return str(1_000_000_000)
        
@api.route('/ibtc-supply', methods=['GET'])
def get_kbtc_supply():
    token_info_subscan = subscan_get_request(SUBSCAN_URL + "api/scan/token").json()["data"]["detail"]
    kBTC_supply = from_10_decimals(int(token_info_subscan["IBTC"]["available_balance"]))
    return str(kBTC_supply)

if __name__ == '__main__':
    api.run(debug=True) 


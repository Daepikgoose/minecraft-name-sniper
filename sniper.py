import requests as r
import time
import threading
import string
import random

headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
  "Accept": "*/*",
  "Accept-Encoding": "deflate, gzip",
}

api = "https://api.mojang.com/users/profiles/minecraft/"
webhook = "https://discord.com/api/webhooks/1540098467853238293/PIYovFb24jZJrKm65ZaScMyLeA8CUIfo20WV-0HacXfCNH1YmWyDDlOH46vq0_GxvLsx"

locktime = 5184000
length = 4
checked = set()

def sendtowebhook(name):
    data = {
        "content" : "",
        "username" : "Goose's MC Sniper"
    }
    data["embeds"] = [
        {
            "description" : f"Minecraft username found!\nName: {name}",
            "title" : f"Minecraft username found! Length: {len(name)}"
        }
    ]
    r.post(webhook, json = data)

def isitvalid(name):
    if name in checked:
        print(f"[X] {name} has already been checked")
        return False
    else:
        try:
            results = r.get(api+name+f"?at={str(time.time()-locktime)}", headers=headers)
            if "errorMessage" in str(results.text):
                checked.add(name)
                sendtowebhook(name)
                print(f"[√] {name} is available!")
                return True
            else:
                print(f"[X] {name} isn't available!")
                return False
        except:
            print("[!] Something went wrong! Retrying in 2s")
            time.sleep(2)
            isitvalid(name)

def generate():
    print("")
    l = length
    randomstring = ''.join(random.choice(string.ascii_lowercase + string.digits + "_") for _ in range(length))
    print(f"[*] Checking {randomstring}")
    isitvalid(randomstring)

while True:
    threading.Thread(target=generate())
    time.sleep(0.1)

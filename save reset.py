import os

for item in os.listdir("img"):
    if item != "unknown.png":
        os.remove("img/" + item)
os.remove("apps_data.json")

os.remove("apps_data.json")
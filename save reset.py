import os

try:
    for item in os.listdir("img"):
        if item == "unknown.png" or item == "icon.ico":
            pass
        else:
            os.remove("img/" + item)
    os.remove("apps_data.json")
    os.remove("apps_data.json")
except:
    print("One of the itens doesn't exist")

''' # ima try this later (ro not)
try:
    os.remove("__pycache__")
except:
    print(";3")

try:
    os.remove("src\__pycache__")
except:
    print(":33")
'''

import os
import shutil

try:
    for item in os.listdir("img"):
        if item == "unknown.png" or item == "icon.ico":
            pass
        else:
            os.remove("img/" + item)
            print("removed " + item)

    os.remove("apps_data.json")
    print("removed saves data")

except:
    print("Save already cleared.")

print("attempting to clear cache...")
cache_foulders = ["view", "src"]
for s in cache_foulders:
    s = os.path.join(os.getcwd(), s, "__pycache__")

    try:
        shutil.rmtree(s)
        print("Deleted cache.")
    except FileNotFoundError:
        print("Nothing found ;)")
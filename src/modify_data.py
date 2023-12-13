from pydantic.utils import deep_update
import json
import os

class ModifyData():

    def __init__(self):
        self.data = {}

    # checa os apps no jsone cria uma lista com nomes, caminhos e icones deles.
    def read_data(self):
        if not os.path.exists("apps_data.json"):
            default_data = {"theme": "Dark",
                            "wnd_size":[600,680],
                            "srtc_size":"G",
                            "foulders":["Default"]}

            self.write_data(default_data)
            self.data = default_data

        with open("apps_data.json", "r") as read_file:
            self.data = json.load(read_file)
        
        self.clear_unused_img()

        return self.data

    def write_data(self, data):
        self.data = deep_update(self.data, data)
        with open("apps_data.json", "w") as write_file:
            json.dump(self.data, write_file, indent=4)

    def clear_unused_img(self):
        img_path = os.path.join(os.getcwd(), "img")
        try:
            saved_img = [os.path.basename(self.data["apps"][app]["icon"]) for app in self.data["apps"]]
        except KeyError:
            saved_img = []

        cache_img = os.listdir(img_path)

        app_imgs = ["unknown.png", "icon.ico"]
        for img in cache_img:
            if img not in saved_img and img not in app_imgs:
                os.remove(os.path.join(img_path, img))

    def clear_data(self, init):
        for item in os.listdir("img"):
            if item != "unknown.png":
                os.remove("img/" + item)
        os.remove("apps_data.json")
                
        init.call_window("close")
        init.call_window("restart")
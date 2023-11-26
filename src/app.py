from customtkinter import set_appearance_mode
import os

class App():
    def __init__(self, init):
        self.init = init

    def open_app(self, path):
        try:
            dir_path = os.path.dirname(path)
            os.chdir(dir_path[1:])
            os.startfile(path)

        #   GET ERROR THAT IS NOT A APP
        except:
            os.system(f"{path}")
        self.init.call_window("close")

    def add_thing(self, thing_button):
        thing = thing_button.get()
        thing_button.set("+")

    def switch_theme(self):
        # If the theme is dark it switches it to light and vice-versa
        current_theme = self.init.data["theme"]
        if current_theme == "Light":
            current_theme = "Dark"

        elif current_theme == "Dark":
            current_theme = "Light"

        self.init.data["theme"] = current_theme

        self.init.modify_data.write_data(self.init.data)
        set_appearance_mode(current_theme)
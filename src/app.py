from customtkinter import set_appearance_mode
import os

class App():
    def __init__(self, init):
        self.init = init
        self.srtc_btns = []
        self.changing = 0

        self.SIZE_DICT = {
            "G": {"icon":(100, 100), "srtc":150},
            "M": {"icon":(80, 80), "srtc":100},
            "P": {"icon":(50, 50), "srtc":70}
        }

        self.COLOR_DICT = {
            "None": "transparent",
            "Red": "red",
            "Green": "green",
            "Purple": "purple"
        }

    def open_app(self, path):
        try:
            dir_path = os.path.dirname(path)
            os.chdir(dir_path[1:])
            os.startfile(path)

        #   GET ERROR THAT IS NOT A APP
        except OSError:
            os.system(f"{path}")
        self.init.call_window("close")

    def enable_edit(self):
        if self.changing == 0:
            self.changing = 1
            for btn in self.srtc_btns:
                btn_data = self.init.data["apps"][btn.cget("text")]
                btn.configure(border_color="red", command=lambda app=btn_data["name"]: self.init.call_window("edit", app))

    # VOLTA AO NORMAL
        else:
            self.changing = 0
            for btn in self.srtc_btns:
                btn_data = self.init.data["apps"][btn.cget("text")]
                btn.configure(border_color="#1f6aa5", command=lambda app=btn_data["path"]: self.open_app(app))

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

    def correct_name(self, name):
        if len(name) >= 10:
            word_list = name.split(" ")

            # If its only one word
            if len(word_list) <= 1:
                new_name = name[:7] + "..."
                return new_name

            # insert enter between the two words
            word_list.insert(1, "\n")

            # if the list has more than 2 words (counting the enter)
            if len(word_list) >= 4:
                word_list.insert(3, "...")
                del word_list[4:]

            if len(word_list[2]) >= 10:
                word_list[2] = word_list[2][:7] + "..."

            new_name = " ".join(word for word in word_list)
            
            return new_name
        
        else:
            return name

    def send_to_foulder(self, app_name, foulder):
        print(app_name + " to " + foulder)

    def on_close(self, wnd_size):
        size_data = {"wnd_size":wnd_size}
        self.init.modify_data.write_data(size_data)
        self.init.call_window("close")
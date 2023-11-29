from customtkinter import set_appearance_mode
import os

class App():
    def __init__(self, init):
        self.init = init
        self.srtc_btns = []
        self.changing = 0

    def open_app(self, path):
        try:
            dir_path = os.path.dirname(path)
            os.chdir(dir_path[1:])
            os.startfile(path)

        #   GET ERROR THAT IS NOT A APP
        except:
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
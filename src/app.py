from customtkinter import set_appearance_mode
import os

class App():
    def __init__(self, init):
        self.init = init
        self.srtc_btns = {}
        self.changing = 0

        self.SIZE_DICT = {
            "G": {"icon":(120, 120), "srtc":115, "wrap":18},
            "M": {"icon":(80, 80), "srtc":80, "wrap":14},
            "P": {"icon":(50, 50), "srtc":70, "wrap":10}
        }

        # dark, light
        self.COLOR_DICT = {
            "Nenhum": "#1f6aa5",
            "Azul Alt": ("#38bfc8", "#37bec8"),
            "Rosa": ("#e92591", "#da1682"),
            "Vermelho": ("#ed3226", "#d91f12"),
            "Roxo": ("#8625e2", "#7e1cd9"),
            "Verde": ("#0ae683", "#1af592"),
            "Amarelo":("#f5ee12", "#ebe40a"),
            "Laranja": ("#e87524", "#e87524"),
            "Branco/Preto": ("Black", "White")
        }

    def open_app(self, path):
        try:
            dir_path = os.path.dirname(path)
            app_dir = os.getcwd()
            os.chdir(dir_path[1:])
            os.startfile(path)
            os.chdir(app_dir) # lazy? fix
                              # maybe better if didn't change the dir at all

        #   GET ERROR THAT IS NOT A APP
        except OSError:
            os.system(f"{path}")
        self.init.call_window("close")

    def enable_edit(self):
        if self.changing == 0:
            self.changing = 1
            for folder in self.srtc_btns:
                for btn in self.srtc_btns[folder]:
                    btn_data = self.init.data["apps"][btn.cget("text")]
                    btn.configure(border_color="red", command=lambda app=btn_data["name"]: self.init.call_window("edit", app))

    # VOLTA AO NORMAL
        else:
            self.changing = 0
            for folder in self.srtc_btns:
                for btn in self.srtc_btns[folder]:
                    btn_data = self.init.data["apps"][btn.cget("text")]
                    btn.configure(border_color=self.COLOR_DICT[btn_data["bd_color"]], command=lambda app=btn_data["path"]: self.open_app(app))

    def switch_theme(self):
        # If the theme is dark it switches it to light and vice-versa
        current_theme = self.init.data["theme"]
        if current_theme == "Light":
            current_theme = "Dark"

        elif current_theme == "Dark":
            current_theme = "Light"

        self.init.data["theme"] = current_theme

        self.init.modify_data.write_data()
        set_appearance_mode(current_theme)

    def send_to_folder(self, app_name, folder):
        print(folder)
        self.init.data["apps"][str(app_name)]["folder"] = folder
        self.init.modify_data.write_data()
        self.init.call_window("restart")

    def move_srct(self, app_start, app_end): # start and end positions
        app_dict = self.init.data["apps"]
        apps_list = [i for i in app_dict]

        swap_app = apps_list[app_start]
        apps_list[app_start] = apps_list[app_end]
        apps_list[app_end] = swap_app

        new_dict = {}
        for i in apps_list:
            new_dict[i] = app_dict[i]

        self.init.data["apps"] = new_dict

        self.init.modify_data.write_data()
        self.init.call_window("restart")

    def show_icons(self, show_icon):
        self.init.data["show_icons"] = show_icon
        self.init.modify_data.write_data()
        self.init.call_window("restart")

    def on_close(self, wnd_size):
        self.init.data["wnd_size"] = wnd_size
        self.init.modify_data.write_data()
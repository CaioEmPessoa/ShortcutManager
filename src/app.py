from customtkinter import set_appearance_mode
import os

class App():
    def __init__(self, init):
        self.init = init
        self.srtc_btns = {}
        self.changing = 0

        self.SIZE_DICT = {
            "G": {"icon":(100, 100), "srtc":150},
            "M": {"icon":(80, 80), "srtc":100},
            "P": {"icon":(50, 50), "srtc":70}
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
            "Bege": ("#bfb3ab", "#544840")
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
                    btn.configure(border_color=self.COLOR_DICT[btn_data["bg_color"]], command=lambda app=btn_data["path"]: self.open_app(app))

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
        #
        # THIS FUNCTION WORKS, BUT IT GETS IN CONFLICT WITH THE EDIT ONE, THAT NEEDS THE NAME OF THE BUTTON TO BE EXATCLY LIKE ON THE JSON.
        # I didn't want to do like this anyway, so Now I need to find a way to better padronize the size of the icons without change its text
        #
        return name
    
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

    def send_to_folder(self, app_name, folder):
        print(folder)
        self.init.data["apps"][app_name]["folder"] = folder
        self.init.modify_data.write_data(self.init.data)
        self.init.call_window("restart")

    def on_close(self, wnd_size):
        size_data = {"wnd_size":wnd_size}
        self.init.modify_data.write_data(size_data)
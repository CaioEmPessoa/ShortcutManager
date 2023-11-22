from customtkinter import set_appearance_mode
import os

class App():
    def __init__(self, init):
        self.init = init

    def change_buttons(self, init):
        # COLOCA PRA EDITAR OS APPS
        if init.changing == 0:
            init.changing = 1
            for button in init.created_buttons:
                button.configure(border_color="red", command=lambda app=init.names_list[init.created_buttons.index(button)]: init.call_edit_window(app))

        # VOLTA AO NORMAL
        else:
            init.changing = 0
            for button in init.created_buttons:
                button.configure(border_color="#1f6aa5", command=lambda app=init.path_list[init.created_buttons.index(button)]: self.open_app(init, app))

    def open_app(self, init, path):
        try:
            dir_path = os.path.dirname(path)
            os.chdir(dir_path[1:])
            os.startfile(path)

        #   GET ERROR THAT IS NOT A APP
        except:
            os.system(f"{path}")
        init.call_window("close")

    def switch_theme(self):
        # If the theme is dark it switches it to light and vice-versa
        if self.theme == "Light":
            theme_data = {"theme": "Light"}
            self.theme = "Dark"

        elif self.theme == "Dark":
            theme_data = {"theme": "Dark"}
            self.theme = "Light"

        self.modify_data.write_data(theme_data)
        set_appearance_mode(self.theme)
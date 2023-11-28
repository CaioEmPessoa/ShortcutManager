import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import shutil

class AddSrtc():
    def __init__(self, init):
        self.init = init
        self.add_srtc_view = init.add_srtc_view

    def search_window(self, path_icon):
        if path_icon == "path":
            self.add_srtc_view.path_entry.delete(0, "end")
            app_path = filedialog.askopenfilename()
            self.add_srtc_view.path_entry.insert(0, app_path)

        elif path_icon == "icon":
            self.add_srtc_view.icon_entry.delete(0, "end")
            icon_path = filedialog.askopenfilename()
            self.add_srtc_view.icon_entry.insert(0, icon_path)

    def send(self, view):
        name, app_path, icon_path = self.check_info(view)
        if self.type == "site":
            app_path = self.convert_browser(view, app_path)

        current_app_dic = {
            "apps": {
                name: {
                    "name": f"{name}",
                    "path": f"\"{app_path}\"",
                    "icon": f"{icon_path}",
                    "type": self.type
                    }
                }
            }

        self.init.modify_data.write_data(current_app_dic)
        self.init.call_window("restart")

    def convert_browser(self, add_srtc_view, link):
        browser = add_srtc_view.browser_entry.get()

        if browser == "":
            browser = "chrome"

        # formats the link if it isn't
        if link[:4] == 'www.':
            link = 'https://' + link

        elif link[:8] != 'https://':
            link = 'https://' + link

        link = f'start {browser} --new-window --app={link} & exit'
        return link

    def check_info(self, wnd):
        name = wnd.name_entry.get()
        stc_path = wnd.path_entry.get()
        icon_path = wnd.icon_entry.get()

        if wnd.is_app:
            self.type = "app"
        elif not wnd.is_app:
            self.type = "site"

        if stc_path == "":
            print("CAMINHO DO ATALHO VAZIO")

            wnd.send_button.configure(fg_color="Red", text="Caminho Vazio")
            return

        elif name == "":
            print("NOME VAZIO")

            # Get the name sliced of the app
            sliced = stc_path.split('/')
            sliced = sliced[len(sliced)-1]
            wnd.name_entry.insert(0, sliced.split('.')[0])
            return

        else:
            # Confere se a imagem é uma imagem, e logo depois a copia para o diretorio de imagens
            try:
                Image.open(icon_path)
                shutil.copy(icon_path, "img")

                sliced = icon_path.split('/')
                sliced = sliced[len(sliced)-1]

                icon_path = "img/" + sliced

            # caso nao seja uma imagem.
            except:
                icon_path = "None"

        return name, stc_path, icon_path
    
class Edit():
    def insert_data(self, init, wnd, app):
        app_data = init.data["apps"][app]

        if app_data["type"] == "broswer":
            wnd.browser_endry.insert(app_data["browser"])

        wnd.name_entry.set(app_data["name"])
        wnd.path_entry.insert(0, app_data["path"])
        wnd.icon_entry.insert(0, app_data["icon"])
        
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
        name, app_path, icon_path, folder, bd_color = self.check_info(view)
        if self.type == "site":
            app_path = self.convert_browser(view, app_path)

        current_app_dic = {
            "apps": {
                name: {
                    "name": f"{name}",
                    "path": f"\"{app_path}\"",
                    "icon": f"{icon_path}",
                    "type": self.type,
                    "folder":folder,
                    "bd_color": f"{bd_color}"
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
            
        if link[:5] == "steam":
            return "start " + link

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
        folder = self.init.app_view.main_tab
        bd_color = wnd.bd_color_entry.get()

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
            # caso nao seja uma imagem.
            except:
                icon_path = "None"

            try:
                shutil.copy(icon_path, "img")

                sliced = icon_path.split('/')
                sliced = sliced[len(sliced)-1]

                icon_path = "img/" + sliced
            except FileNotFoundError:
                icon_path = "None"
            except shutil.SameFileError:
                pass

        return name, stc_path, icon_path, folder, bd_color

class Edit():
    def call_srtc_wnd(self, init, app_name):
        type = init.data["apps"][app_name]["type"]

        if type == "site":
            init.add_srtc_view.new_site_itens(init.add_srtc)
        elif type == "app":
            init.add_srtc_view.new_app_itens(init.add_srtc)

    def delete(self, srtc, init):
        del init.data["apps"][srtc]
        init.modify_data.write_data(init.data)
        init.call_window("restart")

    def insert_data(self, init, wnd, app):
        app_data = init.data["apps"][app]

        if app_data["type"] == "site":
            path = app_data["path"]
            split_path = path.split(" ")
            
            if split_path[1][:5] == "steam":
                path = split_path[1].replace("\"", "")
            else:
                path = split_path[3].replace("--app=", "")
                browser = split_path[1]

                wnd.browser_entry.insert(0, browser)

        elif app_data["type"] == "app":
            path = app_data["path"]
            path = path[:len(path)-1][1:]
        
        if app_data["icon"] != "None":
            wnd.icon_entry.insert(0, app_data["icon"])

        wnd.name_entry.insert(0, app_data["name"])
        wnd.name_entry.configure(state="disabled")

        wnd.path_entry.insert(0, path)
        
        wnd.bd_color_entry.set(app_data["bd_color"])
 
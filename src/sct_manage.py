import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import shutil

class AddEdit():
    def __init__(self, init):
        self.init = init
    
    def add_app(self, app_sct_view):
        app_sct_view.new_app_itens(self)
        app_sct_view.grab_set()

    def add_site(self, site_sct_view):
        site_sct_view.new_site_itens(self)
        site_sct_view.grab_set()

    def edit_stc(self, app_sct_view, site_sct_view):
        self.apps_list = [save for save in self.init.data["apps"]]
        app_data = self.apps_list[app]

        self.app_view.name_entry.insert(app_data["name"])
        self.app_view.path_entry.insert(app_data["path"])
        self.app_view.icon_entry.insert(app_data["icon"])
        
        # not ready yet
        if "is a website":
            self.app_view.browser_entry.insert(app_data["browser"])

    def search_window(self, wnd, path_icon):
        if path_icon == "path":
            wnd.path_entry.delete(0, "end")
            app_path = filedialog.askopenfilename()
            wnd.path_entry.insert(0, app_path)

        elif path_icon == "icon":
            wnd.icon_entry.delete(0, "end")
            icon_path = filedialog.askopenfilename()
            wnd.icon_entry.insert(0, icon_path)

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

    def convert_browser(self, app_view, link):
        browser = app_view.browser_entry.get()
        
        if browser == "":
            browser = "chrome"

        # formats the link if it isn't
        if link[:4] == 'www.':
            link = 'https://' + link

        elif link[:8] != 'https://':
            link = 'https://' + link

        link = f'start {browser} --new-window --app={link} & exit'
        return link

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
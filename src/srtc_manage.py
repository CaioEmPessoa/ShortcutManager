import customtkinter as ctk
from tkinter import filedialog
from os.path import splitext, split
from os import listdir, getcwd
from random import random
from math import floor
from PIL import Image
import shutil

class AddSrtc():
    def __init__(self, init):
        self.init = init
        self.add_srtc_view = init.add_srtc_view

    def search_window(self, file_type):
        if file_type == "path":
            self.add_srtc_view.path_entry.delete(0, "end")
            app_path = filedialog.askopenfilename()
            self.add_srtc_view.path_entry.insert(0, app_path)


        elif file_type == "icon":
            self.add_srtc_view.icon_entry.delete(0, "end")
            icon_path = filedialog.askopenfilename()
            self.add_srtc_view.icon_entry.insert(0, icon_path)
            
        elif file_type == "steam":
            self.add_srtc_view.path_entry.delete(0, "end")
            self.add_srtc_view.name_entry.delete(0, "end")
            self.add_srtc_view.icon_entry.delete(0, "end")
            srtc_path = filedialog.askopenfilename(filetypes=[("Atalho da Internet", ".url")])
            name, url_path, icon_path = self.convert_url_path(srtc_path)

            self.add_srtc_view.name_entry.insert(0, name)
            self.add_srtc_view.path_entry.insert(0, url_path)
            self.add_srtc_view.icon_entry.insert(0, icon_path)

    def send(self, view, edit_id=False):

        if edit_id in self.init.data["apps"]:
            self.edit_id = edit_id
        else:
            apps_dict = self.init.data["apps"]
            if len(apps_dict) > 0:
                self.edit_id = str(floor(random()*10000))
            else:
                self.edit_id = "1"

        name, app_path, icon_path, srtc_type, folder, bd_color = self.check_info(view)


        current_app_dict = {
                self.edit_id: {
                    "name": f"{name}",
                    "id":self.edit_id,
                    "path": f"\"{app_path}\"",
                    "icon": f"{icon_path}",
                    "type": srtc_type,
                    "folder":folder,
                    "bd_color": f"{bd_color}"
                    }
                }
        
        self.init.data["apps"].update(current_app_dict)
        self.init.modify_data.write_data()
        self.init.call_window("restart")


    def convert_url_path(self, srtc_path):
        with open(srtc_path, 'rb') as stream:
            content = str(stream.read())
            url_start = content.find("URL=")
            url_end = content.find("\\r", url_start)
            url = content[url_start:url_end].replace("URL=", "")

            icon_start = content.find("IconFile=")
            icon_end = content.find("\\r", icon_start)
            icon = content[icon_start:icon_end].replace("IconFile=", "")
            icon = icon.replace("\\\\", "/")

            split_path = splitext(split(srtc_path)[1])
            name = split_path[len(split_path)-2]
            
            return name, url, icon

    def convert_browser(self, add_srtc_view, link):
        browser = add_srtc_view.browser_entry.get()

        if browser == "":
            browser = "chrome"

        # formats the link if it isn't
        if link[:4] == 'www.':
            link = 'https://' + link

        elif link[:8] != 'https://':
            link = 'https://' + link
        
        if browser == "firefox":
            link = f"start firefox --name=AppName --no-remote -P \"Apps\" {link}"
        else:
            link = f'start {browser} --new-window --app={link} & exit'
        
        return link

    def check_info(self, wnd):
        name = wnd.name_entry.get()
        srtc_path = wnd.path_entry.get()
        icon_path = wnd.icon_entry.get()
        folder = self.init.app_view.main_tab
        bd_color = wnd.bd_color_entry.get()
        srtc_type = wnd.srtc_type

        if srtc_path == "":
            print("CAMINHO DO ATALHO VAZIO")

            wnd.send_button.configure(fg_color="Red", text="CAMINHO VAZIO")
            return

        elif name == "":
            print("NOME VAZIO")

            # Get the name sliced of the app
            sliced = srtc_path.split('/')
            sliced = sliced[len(sliced)-1]
            wnd.name_entry.insert(0, sliced.split('.')[0])
            return

        ## tentando extrair imagens de .exe caso nao tenha escolhido imagem
        if icon_path == "":
            icon_path = "None"
            
            '''
            # Auto get a icon from a .exe file
            this once worked but the module was discontinued.
            if srtc_path.endswith(".exe"):
                path_icon = icoextract.IconExtractor(srtc_path).get_icon()
                path_icon = Image.open(path_icon)

                # TODO: name = id like other one
                copy_path = "img/"+name+".ico"
                path_icon.save(copy_path)
            '''

        ## caso o user tenha escolhido uma imagem ...
        else:
            # Confere se a imagem é uma imagem
            try:
                Image.open(icon_path)
            # caso nao seja uma imagem.
            except:
                copy_path = "None"
                print("IMAGEM INVÁLIDA")

                wnd.send_button.configure(fg_color="Red", text="IMAGEM INVALIDA")
                return

            try:
                icon_id = self.edit_id

                copy_path = "img/" + str(icon_id) + ".png"

                print(icon_path, copy_path)
                shutil.copy(icon_path, copy_path)

                sliced = copy_path.split('/')
                sliced = sliced[len(sliced)-1]

                icon_path = "img/" + sliced
            except shutil.SameFileError:
                pass

        if srtc_type == "site":
            srtc_path = self.convert_browser(wnd, srtc_path)
        elif srtc_type == "steam":
            srtc_path = "start " + srtc_path
        
        return name, srtc_path, icon_path, srtc_type, folder, bd_color

class Edit():
    def call_srtc_wnd(self, init, app_name):
        type = init.data["apps"][app_name]["type"]

        if type == "site":
            init.add_srtc_view.new_site_itens(init.add_srtc)
        elif type == "app":
            init.add_srtc_view.new_app_itens(init.add_srtc)
        elif type == "steam":
            init.add_srtc_view.new_steam_itens(init.add_srtc)

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
        
        elif app_data["type"] == "steam":
            path = app_data["path"]
            path = path[6:-1]

        elif app_data["type"] == "app":
            path = app_data["path"]
            path = path[:len(path)-1][1:]
        
        if app_data["icon"] != "None":
            wnd.icon_entry.insert(0, app_data["icon"])

        wnd.name_entry.insert(0, app_data["name"])

        wnd.path_entry.insert(0, path)
        
        wnd.bd_color_entry.set(app_data["bd_color"])
 
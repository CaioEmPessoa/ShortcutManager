import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import shutil

class AddApp():
    def __init__(self, init):
        self.init = init
        self.app_view = init.add_app_view

    def send(self):

        name = self.app_view.name_entry.get() 
        app_path = self.app_view.path_entry.get()
        icon_path = self.app_view.icon_entry.get()
        browser = self.app_view.browser_entry.get()

        if app_path == "":
            print("CAMINHO DO APP VAZIO")
            
            self.app_view.send_button.configure(fg_color="Red", text="Caminho Vazio")

        elif name == "":
            print("NOME VAZIO")

            # Get the name sliced of the app
            sliced = app_path.split('/')
            sliced = sliced[len(sliced)-1]
            self.app_view.name_entry.insert(0, sliced.split('.')[0])

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

            # caso seja um site, o formata da forma correta.
            # Coloquei aqui por que precisa ser depis de passar por toda aquela peneira de erros ali de cima
            if self.app_view.site_check.get() == 1:
                # caso nao tenha nada no navegador, coloca o chrome como padrão.
                if browser == "":
                    browser = "chrome"

                # formats the link if it isn't
                if app_path[:4] == 'www.':
                    app_path = 'https://' + app_path

                elif app_path[:8] != 'https://':
                    app_path = 'https://' + app_path

                app_path = f'start {browser} --new-window --app={app_path} & exit'


            current_app_dic = {
                "apps": {
                    name: {
                        "name": f"{name}",
                        "path": f"\"{app_path}\"",
                        "icon": f"{icon_path}"
                        }
                    }
                }

            self.init.modify_data.write_data(current_app_dic)
            
            self.init.call_window("restart")

    def site_app(self):
        # Caso seja um site
        if self.app_view.site_check.get() == 1:
            self.app_view.path_label.configure(text="Insira o link para o site")
            self.app_view.path_window_button.configure(state="disabled")

            self.app_view.browser_label.grid(row=5, column=0, padx=10, columnspan=2, sticky="W")
            self.app_view.browser_entry.grid(row=6, column=0, pady=10, padx=10, sticky="W")

        # Não é um site
        if self.app_view.site_check.get() == 0:
            self.app_view.path_label.configure(text="Insira o caminho do app:")
            self.app_view.path_window_button.configure(state="normal")

            self.app_view.browser_entry.grid_forget()
            self.app_view.browser_label.grid_forget()


    def search_window(self, path_icon):
        if path_icon == "path":
            self.app_view.path_entry.delete(0, "end")
            app_path = filedialog.askopenfilename()
            self.app_view.path_entry.insert(0, app_path)

        elif path_icon == "icon":
            self.app_view.icon_entry.delete(0, "end")
            icon_path = filedialog.askopenfilename()
            self.app_view.icon_entry.insert(0, icon_path)

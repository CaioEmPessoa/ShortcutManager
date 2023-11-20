import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import shutil

class AddApp(ctk.CTkToplevel):

    def send(self, init):

        self.name = self.name_entry.get() 
        self.app_path = self.path_entry.get()
        self.icon_path = self.icon_entry.get()
        self.browser = self.browser_entry.get()

        if self.app_path == "":
            print("CAMINHO DO APP VAZIO")
            
            self.send_button.configure(fg_color="Red", text="Caminho Vazio")

        elif self.name == "":
            print("NOME VAZIO")

            # Get the name sliced of the app
            sliced = self.app_path.split('/')
            sliced = sliced[len(sliced)-1]
            self.name_entry.insert(0, sliced.split('.')[0])

        else:
            # Confere se a imagem é uma imagem, e logo depois a copia para o diretorio de imagens
            try:
                Image.open(self.icon_path)
                shutil.copy(self.icon_path, "img")

                sliced = self.icon_path.split('/')
                sliced = sliced[len(sliced)-1]

                self.icon_path = "img/" + sliced

            # caso nao seja uma imagem.
            except:
                self.icon_path = "None"

            # caso seja um site, o formata da forma correta.
            # Coloquei aqui por que precisa ser depis de passar por toda aquela peneira de erros ali de cima
            if self.site_check.get() == 1:
                # caso nao tenha nada no navegador, coloca o chrome como padrão.
                if self.browser == "":
                    self.browser = "chrome"

                # formats the link if it isn't
                if self.app_path[:4] == 'www.':
                    self.app_path = 'https://' + self.app_path

                elif self.app_path[:8] != 'https://':
                    self.app_path = 'https://' + self.app_path

                self.app_path = f'start {self.browser} --new-window --app={self.app_path} & exit'


            current_app_dic = {
                self.name: {
                    "name": f"{self.name}",
                    "path": f"\"{self.app_path}\"",
                    "icon": f"{self.icon_path}"
                }
            }

            init.write_data(current_app_dic)
            
            init.call_window("close")
            init.call_window("restart")
        
    def search_window(self, path_icon):
        if path_icon == "path":
            self.path_entry.delete(0, "end")
            self.app_path = filedialog.askopenfilename()
            self.path_entry.insert(0, self.app_path)

        elif path_icon == "icon":
            self.icon_entry.delete(0, "end")
            self.icon_path = filedialog.askopenfilename()
            self.icon_entry.insert(0, self.icon_path)


    def __init__(self, init):
        super().__init__()
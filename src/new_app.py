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

    def site_app(self):

        # Caso seja um site
        if self.site_check.get() == 1:
            self.path_label.configure(text="Insira o link para o site")
            self.path_window_button.configure(state="disabled")

            self.browser_label.grid(row=5, column=0, padx=10, columnspan=2, sticky="W")
            self.browser_entry.grid(row=6, column=0, pady=10, padx=10, sticky="W")


        # Não é um site
        if self.site_check.get() == 0:
            self.path_label.configure(text="Insira o caminho do app:")
            self.path_window_button.configure(state="normal")

            self.browser_entry.grid_forget()
            self.browser_label.grid_forget()


    def __init__(self, init):
        super().__init__()

        # Buttons, Labels and Entrys
        # LABELS
        self.name_label = ctk.CTkLabel(master=self, justify="left", text="(Escolha o nome do app:")
        self.name_label.grid(row=0, column=0, padx=10, columnspan=3, sticky="W")

        self.site_label = ctk.CTkLabel(master=self, text="É um site?")
        self.site_label.grid(row=2, column=0, pady=10, padx=10, columnspan=3, sticky="W")

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador utilizará?")

        self.path_label = ctk.CTkLabel(master=self, text="Escolha o caminho do app:")
        self.path_label.grid(row=3, column=0, padx=10, columnspan=2, sticky="W")

        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do app:")
        self.icon_label.grid(row=7, column=0, padx=10, columnspan=2, sticky="W")

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador? Chrome é padrão.\n(precisa ser baseado em chromium)")
        # END Labels

        # ENTRY
        self.name_entry = ctk.CTkEntry(master=self, width=200)
        self.name_entry.grid(row=1, column=0, 
                        pady=10, padx=10, sticky="W", columnspan=3)
        
        self.site_check = ctk.CTkCheckBox(master=self, text="", command=self.site_app)
        self.site_check.grid(row=2, column=1, padx=10, columnspan=3, sticky="W")

        self.path_entry = ctk.CTkEntry(master=self)
        self.path_entry.grid(row=4, column=0, 
                        pady=10, padx=10, sticky="W")

        self.icon_entry = ctk.CTkEntry(master=self)
        self.icon_entry.grid(row=8, column=0, pady=10, padx=10, sticky="W")

        self.browser_entry = ctk.CTkEntry(master=self)
        # END Entry

        # Buttons
        self.path_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("path"))
        self.path_window_button.grid(row=4, column=1, sticky="W")

        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("icon"))
        self.icon_window_button.grid(row=8, column=1, sticky="W")

        self.send_button = ctk.CTkButton(master=self, command=lambda: self.send(init), text="Concluir")
        self.send_button.grid(row=9, pady=15, columnspan=2)
        # END Buttons

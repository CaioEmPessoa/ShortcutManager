import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import shutil



class AddApp(ctk.CTkToplevel):

    def send(self, init):

        self.name = self.name_entry.get() 
        self.app_path = self.path_entry.get()
        self.icon_path = self.icon_entry.get()

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
                print("img/unknown.png")
                self.icon_path = "None"

            current_app_dic = {
                self.name: {
                    "name": self.name,
                    "path": self.app_path,
                    "icon": self.icon_path
                }
            }
            
            init.write_data(current_app_dic)
            
            init.call_window("close")
            init.call_window("restart")
        
    def search_window(self, app_icon):

        if app_icon == "app":
            self.app_path = filedialog.askopenfilename()
            self.path_entry.insert(0, self.app_path)

        elif app_icon == "icon":
            self.icon_path = filedialog.askopenfilename()
            self.icon_entry.insert(0, self.icon_path)


    def __init__(self, init):
        super().__init__()

        # Buttons, Labels and Entrys
        # LABELS
        self.name_label = ctk.CTkLabel(master=self, text="Escolha o nome do app: (Colocar nome repetido caso queria atualizar)")
        self.name_label.grid(row=0, column=0, padx=10, columnspan=2, sticky="W")

        self.path_label = ctk.CTkLabel(master=self, text="Escolha o caminho do app:")
        self.path_label.grid(row=2, column=0, padx=10, columnspan=2, sticky="W")

        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do app:")
        self.icon_label.grid(row=4, column=0, padx=10, columnspan=2, sticky="W")
        # END Labels

        # ENTRY
        self.name_entry = ctk.CTkEntry(master=self, width=200)
        self.name_entry.grid(row=1, column=0, 
                        pady=10, padx=10, sticky="W",
                        columnspan=2)

        self.path_entry = ctk.CTkEntry(master=self)
        self.path_entry.grid(row=3, column=0, 
                        pady=10, padx=10)

        self.icon_entry = ctk.CTkEntry(master=self)
        self.icon_entry.grid(row=5, column=0,
                        pady=10, padx=10)
        # END Entry

        # Buttons
        self.path_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("app"))
        self.path_window_button.grid(row=3, column=1)

        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("icon"))
        self.icon_window_button.grid(row=5, column=1)

        self.send_button = ctk.CTkButton(master=self, command=lambda: self.send(init), text="Concluir")
        self.send_button.grid(row=6, pady=10, columnspan=2)
        # END Buttons

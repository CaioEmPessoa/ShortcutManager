import customtkinter as ctk
import json

#my code
import main
from src import new_app
from src import edit_app

class DefaultClass():

    def call_window(self, window):

        match window:
            case "root":
                self.root = main.Root(self)
                
                self.root.minsize(600, 680)
                self.root.maxsize(600, 680)
                self.root.iconbitmap("img/icon.ico")
                self.root.title("Shortcut Manager")

                self.root.mainloop()

            case "add_app":
                self.add_app = new_app.AddApp(self)
                self.add_app.grab_set()

            case "restart":
                default = DefaultClass()

            case "close":
                self.root.destroy()

    def call_edit_window(self, app):
        self.add_app = edit_app.EditAppWindow(self, app)
        self.add_app.grab_set()

    def switch_theme(self):

        # se o tema for escuro ele troca pra claro e vice versa
        if self.tema == "Dark":
            
            # Salva o tema (reverso) para o json
            theme_data = {"tema": "Dark"}
            self.write_data(theme_data)

            # Seta o tema para o verdadeiro
            self.tema = "Light"

        elif self.tema == "Light":

            # Salva o tema (reverso) para o json
            theme_data = {"tema": "Light"}
            self.write_data(theme_data)

            # seta o tema para o verdadeiro
            self.tema = "Dark"

        ctk.set_appearance_mode(self.tema)

    # checa os apps no jsone cria uma lista com nomes, caminhos e icones deles.
    def read_data(self):
        with open("apps_data.json", "r") as read_file:
            self.data = json.load(read_file)

            try:
                self.tema = self.data["tema"]
                print(self.tema)
                
            except:
                print("no theme")
                self.tema = "Light"
                theme_data = {"tema": "Light"}
                self.write_data(theme_data)
                self.switch_theme()

        for key in self.data:
            if key != "tema":
                # Access the elements dynamically using the key
                element = self.data[key]

                self.names_list.append(element['name'])
                self.path_list.append(element['path'])
                self.icon_list.append(element['icon'])

        self.list_number = len(self.names_list)
        self.switch_theme()

    def write_data(self, data):
        self.data.update(data)

        with open("apps_data.json", "w") as write_file:
            json.dump(self.data, write_file, indent=4)


    def __init__(self):
        super().__init__()

        # DEFAULT VALUES ----------------<
        self.row = 1
        self.column = 0

        self.changing = 0

        self.names_list = []
        self.path_list = []
        self.icon_list = []
        self.created_buttons = []
        
        ctk.set_default_color_theme("dark-blue")
        # >--------------------------- END

        # tenta checar se existe um app salvo
        try:
            print("Lendo Data")
            self.read_data()
        
        # caso nao tenha apsp salvos, diz que a lista de itens é 0. 
        except:
            print('no previus apps')

            self.list_number = 0
            self.data = {}

            try:
                self.tema = self.data["tema"]
                print(self.tema)
                
            except:
                print("no theme")
                self.tema = "Light"
                theme_data = {"tema": "Light"}
                self.write_data(theme_data)
                self.switch_theme()
            
        self.call_window("root")

default = DefaultClass()

import customtkinter as ctk
import json

#my code
import main
from src import new_app

class DefaultClass():

    def call_window(self, window):

        match window:
            case "root":
                self.root = main.Root(self)
                
                self.root.minsize(550, 50)
                self.root.maxsize(550, 2000)

                self.root.mainloop()

            case "add_app":
                self.add_app = new_app.AddApp(self)
                self.add_app.grab_set()

            case "restart":
                default = DefaultClass()

            case "close":
                self.root.destroy()

    def switch_theme(self):
        if self.tema == "escuro":
            self.tema = "claro"
            ctk.set_appearance_mode("Light")

        elif self.tema == "claro":
            self.tema = "escuro"
            ctk.set_appearance_mode("Dark")

    def read_data(self):
        with open("apps_data.json", "r") as read_file:
            self.data = json.load(read_file)

        for key in self.data:
            # Access the elements dynamically using the key
            element = self.data[key]

            self.names_list.append(element['name'])
            self.path_list.append(element['path'])
            self.icon_list.append(element['icon'])

        self.list_number = len(self.names_list)

    def write_data(self, data):
        self.data.update(data)

        with open("apps_data.json", "w") as write_file:
            json.dump(self.data, write_file, indent=4)


    def __init__(self):
        super().__init__()

        # DEFAULT VALUES ----------------<
        ctk.set_appearance_mode("Dark")
        self.tema = "escuro"

        self.row = 1
        self.column = 0

        self.names_list = []
        self.path_list = []
        self.icon_list = []
        # >--------------------------- END

        # tenta ler a data salva
        try:
            print("Lendo Data")
            self.read_data()
        
        # caso nao tenha data salva, diz que a lista de itens é 0, 
        except:
            print('no previus data')
            
            open("apps_data.json", "w")
            self.list_number = 0
            self.data = {}

        self.call_window("root")

default = DefaultClass()
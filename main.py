import customtkinter as ctk 
from PIL import Image
import subprocess
from src import edit_app
import os

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class Root(ctk.CTk):

    def clear_data(self, init):
        for item in os.listdir("img"):
            if item != "unknown.png":
                os.remove("img/" + item)
        os.remove("apps_data.json")
                
        init.call_window("close")
        init.call_window("restart")

    def change_buttons(self, init):

    # COLOCA PRA EDITAR OS APPS
        if init.changing == 0:
            init.changing = 1
            for button in init.created_buttons:
                button.configure(border_color="red", 
                                 command=lambda app=init.names_list[init.created_buttons.index(button)]: 
                                 init.call_edit_window(app))

    # VOLTA AO NORMAL
        else:
            init.changing = 0
            for button in init.created_buttons:
                button.configure(border_color="#1f6aa5", 
                                 command=lambda app=init.path_list[init.created_buttons.index(button)]: 
                                 self.open_app(init, app))

    def open_app(self, init, path):
        os.startfile(path)
        init.call_window("close")

    def __init__(self, init):
        super().__init__()
        
        # WELCOME LABEL ------------------------------------<
        welcome = ctk.CTkLabel(master=self, text="Escolha um ou adicione um novo atalho", 
                               font=('Segoe UI', 20), text_color="#807e7e", width=500)
        welcome.grid(row=0, column=0, columnspan=3)
        # -----------------------------------------------> END

        # Calls the app buttons to generate them. ------------------------------<

        self.my_frame = MyFrame(master=self, fg_color="transparent",
                                width=550, height=600, corner_radius=0)
        self.my_frame.grid(row=1, column=0, padx=10,
                           columnspan=3, sticky="nsew")

        self.app_buttons(init) 

        # Generate the last button, an "add more" one.
        add_button = ctk.CTkButton(master=self, text=" + ", width=70, 
                                   command=lambda: init.call_window("add_app"))
        add_button.grid(row=init.row+1, column=0, 
                        padx=10, pady=10, sticky="E")

        edit_button = ctk.CTkButton(master=self, text="Editar", width=70,
                                    command=lambda: self.change_buttons(init))
        edit_button.grid(row=init.row+1, column=1, pady=10)

        theme_buttom = ctk.CTkButton(master=self, text="Tema", width=70,
                                     command=lambda: init.switch_theme())
        theme_buttom.grid(row=init.row+1, column=2, 
                          padx=10, pady=10, sticky="W")

        # >---------------------------------------------------------------- END

    def app_buttons(self, init):
        for item in range(0, init.list_number): # Loop around the list of app names and create apps with their names.
            
            icon = ctk.CTkImage(light_image=Image.open("img/unknown.png"),size=(150, 150))

            app_button = ctk.CTkButton(master=self.my_frame, width=70, text=init.names_list[item], compound="top",
                                   command=lambda app=init.path_list[item]: self.open_app(init, app), image=icon, font=('Segoe UI', 16),
                                   text_color="#807e7e", fg_color="transparent", border_color="#1f6aa5", border_width=2.5, hover_color="#184c74")
            app_button.grid(row=init.row, column=init.column, pady=10, padx=5)

            init.created_buttons.append(app_button)

            # coloca imagem do ícone ao lado do nome do app caso esteja salvo alguma imagem no json

            if init.icon_list[item] != "None":
                icon = ctk.CTkImage(light_image=Image.open(init.icon_list[item]),size=(150, 150))
                app_button.configure(image=icon)

            # Change the pos of the buttons
            init.column += 1
            if init.column == 3:
                init.column = 0
                init.row += 3
            # >--------------------- END

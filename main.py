import customtkinter as ctk 
from PIL import Image
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
        

    def open_app(self, init, path):
        
        os.system(f"\"{path}\"")
        init.call_window("close")
        
    

    def __init__(self, init):
        super().__init__()
        
        # WELCOME LABEL ------------------------------------<
        welcome = ctk.CTkLabel(master=self, text="Escolha um app ou adicione um novo.", 
                               font=('Segoe UI', 20), text_color="#807e7e", width=500)
        welcome.grid(row=0, column=0, columnspan=9)
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

        clear_button = ctk.CTkButton(master=self, text="Apagar", width=70,
                                    command=lambda: self.clear_data(init))
        clear_button.grid(row=init.row+1, column=1, pady=10)

        theme_buttom = ctk.CTkButton(master=self, text="Tema", width=70,
                                     command=lambda: init.switch_theme())
        theme_buttom.grid(row=init.row+1, column=2, 
                          padx=10, pady=10, sticky="W")

        # >---------------------------------------------------------------- END

    def app_buttons(self, init):
        for item in range(0, init.list_number): # Loop around the list of app names and create apps with their names.
            
            icon = ctk.CTkImage(light_image=Image.open("img/unknown.png"),size=(150, 150))

            button = ctk.CTkButton(master=self.my_frame, width=70, text=init.names_list[item], compound="top",
                                   command=lambda app=init.path_list[item]: self.open_app(init, app), image=icon, font=('Segoe UI', 16),
                                   text_color="#807e7e", fg_color="transparent", border_color="#1f6aa5", border_width=2.5)
            button.grid(row=init.row, column=init.column, columnspan=3, pady=10, padx=10)

            # coloca imagem do ícone ao lado do nome do app caso esteja salvo alguma imagem no json 

            if init.icon_list[item] != "None":
                icon = ctk.CTkImage(light_image=Image.open(init.icon_list[item]),size=(150, 150))
                button.configure(image=icon)

            # Change the pos of the buttons
            init.column += 3
            if init.column == 9:
                init.column = 0
                init.row += 3
            # >--------------------- END
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
        
        os.system(path)
        init.call_window("close")
        
    

    def __init__(self, init):
        super().__init__()
        
        # WELCOME LABEL ------------------------------------<
        welcome = ctk.CTkLabel(master=self, 
        text="Escolha um app ou adicione um novo.", width=500, font=('Comic Sans MS', 20))
        welcome.grid(row=0, column=0, columnspan=3)
        # -----------------------------------------------> END

        # Calls the app buttons to generate them. ------------------------------<

        self.my_frame = MyFrame(master=self, fg_color="transparent",
                                width=550, height=600, corner_radius=0)
        self.my_frame.grid(row=1, column=0, padx=10,
                           columnspan=3, sticky="nsew")

        self.app_buttons(init) 

        # Generate the last button, an "add more" one.
        add_button = ctk.CTkButton(master=self.my_frame, text=" + ", width=70, 
                                   command=lambda: init.call_window("add_app"))
        add_button.grid(row=init.row, column=init.column, 
                        padx=10, pady=10, sticky="S")

        clear_button = ctk.CTkButton(master=self.my_frame, text="Apagar", width=70,
                                    command=lambda: self.clear_data(init))
        clear_button.grid(row=init.row+1, column=init.column, pady=10)

        theme_buttom = ctk.CTkButton(master=self.my_frame, text="Tema", width=70,
                                     command=lambda: init.switch_theme())
        theme_buttom.grid(row=init.row+2, column=init.column, 
                          padx=10, pady=10, sticky="N")

        # >---------------------------------------------------------------- END

    def app_buttons(self, init):
        for item in range(0, init.list_number): # Loop around the list of app names and create apps with their names.
            
            icon = ctk.CTkImage(light_image=Image.open("img/unknown.png"),size=(150, 150))

            button = ctk.CTkButton(master=self.my_frame, width=70, text=init.names_list[item], compound="bottom",
                                   command=lambda app=init.path_list[item]: self.open_app(init, app), 
                                   image=icon)
            button.grid(row=init.row, column=init.column, rowspan=3, pady=10, padx=10)

            # coloca imagem do ícone ao lado do nome do app caso esteja salvo alguma imagem no json 

            if init.icon_list[item] != "None":
                icon = ctk.CTkImage(light_image=Image.open(init.icon_list[item]),size=(150, 150))
                button.configure(image=icon)

            # Change the pos of the buttons
            init.column += 1
            if init.column == 3:
                init.column = 0
                init.row += 3
            # >--------------------- END
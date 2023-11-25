import customtkinter as ctk
from PIL import Image

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class AppWnd(ctk.CTk):

    def __init__(self, init, app):
        super().__init__()

        self.title("Shortcut Manager")
        self.iconbitmap("img/icon.ico")

        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.set_appearance_mode(init.data["theme"])

        w = 600 
        h = 680 
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.create_itens(init, app)

    def create_itens(self, init, app):

        welcome = ctk.CTkLabel(master=self, text="Escolha um ou adicione um novo atalho", 
                               font=('Segoe UI', 20), text_color="#807e7e", width=500)
        welcome.grid(row=0, column=0, columnspan=3)

        self.my_frame = MyFrame(master=self, fg_color="transparent",
                                width=550, height=600, corner_radius=0)
        self.my_frame.grid(row=1, column=0, padx=10,
                           columnspan=3, sticky="nsew")

        self.app_buttons(init, app) 

        '''
        add_button = ctk.CTkButton(master=self, text=" + ", width=70, 
                                   command=lambda: init.call_window("add_app"))
        add_button.grid(row=2, column=0, 
                        padx=10, pady=10, sticky="E")
        '''
        optionmenu = ctk.CTkOptionMenu(self, values=["App", "Site", "Foulder"])
        optionmenu.set("+")
        optionmenu.grid(row=2, column=0, 
                        padx=10, pady=10, sticky="E")

        edit_button = ctk.CTkButton(master=self, text="Editar", width=70,
                                    command=lambda: app.change_buttons(init))
        edit_button.grid(row=2, column=1, pady=10)

        theme_buttom = ctk.CTkButton(master=self, text="Tema", width=70,
                                     command=lambda: app.switch_theme())
        theme_buttom.grid(row=2, column=2, 
                          padx=10, pady=10, sticky="W")

    def app_buttons(self, init, app):
        try:
            data = init.data["apps"]

        except KeyError:
            return
    
        btn_nmb = 0
        max_columns = 3

        for app_name in data:
            app_data = data[app_name]

            if app_data["icon"] != "None":
                icon = ctk.CTkImage(light_image=Image.open(app_data["icon"]),size=(150, 150))
            else:
                icon = ctk.CTkImage(light_image=Image.open("img/unknown.png"),size=(150, 150))

            app_button = ctk.CTkButton(master=self.my_frame, width=70, text=app_data["name"], compound="top",
                                   command=lambda app_path=app_data["path"]: app.open_app(app_path), image=icon, font=('Segoe UI', 16),
                                   text_color="#807e7e", fg_color="transparent", border_color="#1f6aa5", border_width=2.5, hover_color="#184c74")

            row = btn_nmb // max_columns
            col = btn_nmb % max_columns
            app_button.grid(row=row, column=col, pady=10, padx=5)
            btn_nmb+=1
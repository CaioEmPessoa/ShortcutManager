import customtkinter as ctk

class edit_app_wnd():
    def __init__(self, init, app):
        super().__init__()
        
        self.title("Shortcut Manager")
        self.iconbitmap("img/icon.ico")

        self.app = app

        # "Head?" of this window -----------------------------------------------------------------------------------<
        
        if init.data[self.app]['icon'] == "None":
            icon = ctk.CTkImage(light_image=Image.open("img/unknown.png"),size=(150, 150))
        else:
            icon = ctk.CTkImage(light_image=Image.open(init.data[self.app]['icon']),size=(150, 150))

        label = ctk.CTkLabel(master=self, text=f"Editar o atalho \"{init.data[self.app]['name']}\" !!", font=('Segoe UI', 16))
        label.grid(row=0, column=0, padx=10, pady=10)

        del_button = ctk.CTkButton(master=self, text="Delete", fg_color="red", command=lambda: self.delete_app(init))
        del_button.grid(row=0, column=1, padx=10, pady=10)

        apply_button = ctk.CTkButton(master=self, text="Apply", command=lambda: self.apply_changes(init))
        apply_button.grid(row=0, column=2, padx=10, pady=10)

        # >------------------------------------------------------------------------------------------------------ END

        # Showing the originals -----------------------------------------------------------------------------<
        icon_label = ctk.CTkLabel(master=self, text="", image=icon)
        icon_label.grid(row=1, column=0, rowspan=3, pady=10, padx=10)

        original_info_text = f"Nome original: {init.data[self.app]['name']}\nCaminho Original: {init.data[self.app]['path']}\nÍcone Original: {init.data[self.app]['icon']}\n\n**Deixe o espaço vazio para não alterar"

        original_info_label = ctk.CTkLabel(master=self, text=original_info_text, font=('Segoe UI', 15), justify="left")
        original_info_label.grid(row=1, column=1, padx=10, pady=10, sticky="W", columnspan=2)
        
        # >--------------------------------------------------------------------------------------------- END

        # Labels / entrys to update the app ----------------------------------------------------- <   
        self.path_label = ctk.CTkLabel(master=self, text="Escolha o caminho do app:")
        self.path_label.grid(row=4, column=0)

        self.path_entry = ctk.CTkEntry(master=self)
        self.path_entry.grid(row=5, column=0)


        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do app:")
        self.icon_label.grid(row=4, column=1)

        self.icon_entry = ctk.CTkEntry(master=self)
        self.icon_entry.grid(row=5, column=1)
        
        self.name_label = ctk.CTkLabel(master=self, justify="left", text="Escolha o nome do app:")
        self.name_label.grid(row=4, column=2)

        self.name_entry = ctk.CTkEntry(master=self)
        self.name_entry.grid(row=5, column=2)

        # >--------------------------------------------------------------------------------- END

        # Buttons
        self.path_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("path"))
        self.path_window_button.grid(row=6, column=0, pady=10)

        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("icon"))
        self.icon_window_button.grid(row=6, column=1, pady=10)

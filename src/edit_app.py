from tkinter import filedialog
import customtkinter as ctk
from PIL import Image

class EditAppWindow(ctk.CTkToplevel):

    def apply_changes(self, init):
        self.name = self.name_entry.get() 
        self.app_path = self.path_entry.get()
        self.icon_path = self.icon_entry.get()

        if self.name != "":
            init.data[self.app]['name'] = self.name
            init.data[self.name] = init.data.pop(self.app)

        if self.app_path != "":
            init.data[self.app]['path'] = self.app_path
        
        if self.icon_path != "":
            init.data[self.app]['icon'] = self.icon_path

        init.write_data(init.data)
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

    def delete_app(self, init):
        del init.data[self.app]
        init.write_data(init.data)

        init.call_window("close")
        init.call_window("restart")

    def __init__(self, init, app):
        super().__init__()
        self.app = app

        # "Head?" of this window -----------------------------------------------------------------------------------<
        icon = ctk.CTkImage(light_image=Image.open(init.data[self.app]['icon']),size=(150, 150))

        label = ctk.CTkLabel(master=self, text=f"Edit {init.data[self.app]['name']} Shortcut!", font=('Segoe UI', 16))
        label.grid(row=0, column=0, padx=10, pady=10)

        del_button = ctk.CTkButton(master=self, text="Delete", fg_color="red", command=lambda: self.delete_app(init))
        del_button.grid(row=0, column=1, padx=10, pady=10)

        apply_button = ctk.CTkButton(master=self, text="Apply", command=lambda: self.apply_changes(init))
        apply_button.grid(row=0, column=2, padx=10, pady=10)

        # >------------------------------------------------------------------------------------------------------ END

        # Showing the originals -----------------------------------------------------------------------------<
        icon_label = ctk.CTkLabel(master=self, text="", image=icon)
        icon_label.grid(row=1, column=0, rowspan=3, pady=10, padx=10)

        original_info_text = f"Original Name: {init.data[self.app]['name']}\nOriginal Path: {init.data[self.app]['path']}\nOriginal Icon: {init.data[self.app]['icon']}\n\n**Deixe o espaço vazio para não alterar"

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
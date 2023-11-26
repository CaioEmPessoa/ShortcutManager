import customtkinter as ctk

class NewAppWnd(ctk.CTkToplevel):
    def edit_itens(self, newapp, init):
        '''
        self.saves_list = [save for save in init.data["saves"]]
        self.name_entry.destroy()
        self.name_entry = ctk.CTkOptionMenu(master=self, values=self.saves_list, width=220, font=('',16), command=newapp.insert_save,
                                fg_color=("White", "#343638"), text_color=("Black", "White"), button_color=("#969da3", "#565a5f"))
        self.name_entry.grid(row=2, column=0, columnspan=3)

        self.image_path_label.configure(text="Path to the preview image:\n(empty to remove)")

        self.send_button.grid_forget()
        self.send_button.configure(width=100)
        self.send_button.grid(row=11, column=0, pady=15, columnspan=1)
        
        self.delete_button = ctk.CTkButton(master=self, fg_color="red", text="delete", width=100,
                                           command=new_save.delete_save)
        self.delete_button.grid(row=11, column=2, pady=15, columnspan=1)

        new_save.insert_save(self.saves_list[0])
        '''

    def new_site_itens(self, newapp):
        self.new_app_itens(newapp)
        self.is_app = False

        w, h = 230, 340
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) / 2, (hs - h) / 2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

        self.path_label.configure(text="Insira o link para o site:")
        self.path_window_button.grid_forget()

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador? Chrome é padrão.\n(precisa ser baseado em chromium)")
        self.browser_label.grid(row=5, column=0, padx=10, columnspan=2, sticky="W")
        
        self.browser_entry = ctk.CTkEntry(master=self)
        self.browser_entry.grid(row=6, column=0, padx=10, sticky="W")

    def new_app_itens(self, newapp):
        w, h = 220, 330
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) / 2, (hs - h) / 2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

        self.title("Shortcut Manager")
        self.iconbitmap("img/icon.ico")

        self.is_app = True

        # Buttons, Labels and Entrys
        # LABELS
        self.name_label = ctk.CTkLabel(master=self, justify="left", text="Escolha o nome do app:")
        self.name_label.grid(row=0, column=0, padx=10, columnspan=3, sticky="W")

        self.path_label = ctk.CTkLabel(master=self, text="Escolha o caminho do atalho:")
        self.path_label.grid(row=3, column=0, padx=10, columnspan=2, sticky="W")

        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do atalho:")
        self.icon_label.grid(row=7, column=0, padx=10, columnspan=2, sticky="W")

        # END Labels

        # ENTRY
        self.name_entry = ctk.CTkEntry(master=self, width=200)
        self.name_entry.grid(row=1, column=0, 
                        pady=10, padx=10, sticky="W", columnspan=3)

        self.path_entry = ctk.CTkEntry(master=self)
        self.path_entry.grid(row=4, column=0, 
                        pady=10, padx=10, sticky="W")

        self.icon_entry = ctk.CTkEntry(master=self)
        self.icon_entry.grid(row=8, column=0, pady=10, padx=10, sticky="W")
        # END Entry

        # Buttons
        self.path_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: newapp.search_window("path"))
        self.path_window_button.grid(row=4, column=1, sticky="W")

        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: newapp.search_window("icon"))
        self.icon_window_button.grid(row=8, column=1, sticky="W")

        self.send_button = ctk.CTkButton(master=self, command=newapp.send, text="Concluir")
        self.send_button.grid(row=9, pady=15, columnspan=2)
        # END Buttons

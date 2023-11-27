import customtkinter as ctk

class AppSctWnd(ctk.CTkToplevel):
    def new_app_itens(self, sct):
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
                                    command=lambda: sct.search_window(self, "path"))
        self.path_window_button.grid(row=4, column=1, sticky="W")

        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: sct.search_window(self, "icon"))
        self.icon_window_button.grid(row=8, column=1, sticky="W")

        self.send_button = ctk.CTkButton(master=self, command=lambda: sct.send(self), text="Concluir")
        self.send_button.grid(row=9, pady=15, columnspan=2)
        # END Buttons

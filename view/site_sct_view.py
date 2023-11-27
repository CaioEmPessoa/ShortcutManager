import customtkinter as ctk
class SiteSctWnd(ctk.CTkToplevel):

    def new_site_itens(self, sct):
        self.is_app = False

        w, h = 230, 340
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) / 2, (hs - h) / 2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

        self.name_label = ctk.CTkLabel(master=self, justify="left", text="Escolha o nome do app:")
        self.name_label.grid(row=0, column=0, padx=10, columnspan=3, sticky="W")

        self.path_label = ctk.CTkLabel(master=self, text="Insira o link para o site:")
        self.path_label.grid(row=3, column=0, padx=10, columnspan=2, sticky="W")

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador? Chrome é padrão.\n(precisa ser baseado em chromium)")
        self.browser_label.grid(row=5, column=0, padx=10, columnspan=2, sticky="W")

        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do atalho:")
        self.icon_label.grid(row=7, column=0, padx=10, columnspan=2, sticky="W")

        # END Labels

        # ENTRY
        self.name_entry = ctk.CTkEntry(master=self, width=200)
        self.name_entry.grid(row=1, column=0, 
                        pady=10, padx=10, sticky="W", columnspan=3)

        self.path_entry = ctk.CTkEntry(master=self)
        
        self.browser_entry = ctk.CTkEntry(master=self)
        self.browser_entry.grid(row=6, column=0, padx=10, sticky="W")
        
        self.path_entry.grid(row=4, column=0, 
                        pady=10, padx=10, sticky="W")

        self.icon_entry = ctk.CTkEntry(master=self)
        self.icon_entry.grid(row=8, column=0, pady=10, padx=10, sticky="W")
        # END Entry
    
        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: sct.search_window(self, "icon"))
        self.icon_window_button.grid(row=8, column=1, sticky="W")

        self.send_button = ctk.CTkButton(master=self, command=lambda: sct.send(self), text="Concluir")
        self.send_button.grid(row=9, pady=15, columnspan=2)
        # END Buttons



import customtkinter as ctk

class NewAppWnd():
    def site_app(self):
        # Caso seja um site
        if self.site_check.get() == 1:
            self.path_label.configure(text="Insira o link para o site")
            self.path_window_button.configure(state="disabled")

            self.browser_label.grid(row=5, column=0, padx=10, columnspan=2, sticky="W")
            self.browser_entry.grid(row=6, column=0, pady=10, padx=10, sticky="W")

        # Não é um site
        if self.site_check.get() == 0:
            self.path_label.configure(text="Insira o caminho do app:")
            self.path_window_button.configure(state="normal")

            self.browser_entry.grid_forget()
            self.browser_label.grid_forget()

    def create_itens(self):
        self.title("Shortcut Manager")
        self.iconbitmap("img/icon.ico")

        # Buttons, Labels and Entrys
        # LABELS
        self.name_label = ctk.CTkLabel(master=self, justify="left", text="(Escolha o nome do app:")
        self.name_label.grid(row=0, column=0, padx=10, columnspan=3, sticky="W")

        self.site_label = ctk.CTkLabel(master=self, text="É um site?")
        self.site_label.grid(row=2, column=0, pady=10, padx=10, columnspan=3, sticky="W")

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador utilizará?")

        self.path_label = ctk.CTkLabel(master=self, text="Escolha o caminho do app:")
        self.path_label.grid(row=3, column=0, padx=10, columnspan=2, sticky="W")

        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do app:")
        self.icon_label.grid(row=7, column=0, padx=10, columnspan=2, sticky="W")

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador? Chrome é padrão.\n(precisa ser baseado em chromium)")
        # END Labels

        # ENTRY
        self.name_entry = ctk.CTkEntry(master=self, width=200)
        self.name_entry.grid(row=1, column=0, 
                        pady=10, padx=10, sticky="W", columnspan=3)
        
        self.site_check = ctk.CTkCheckBox(master=self, text="", command=self.site_app)
        self.site_check.grid(row=2, column=1, padx=10, columnspan=3, sticky="W")

        self.path_entry = ctk.CTkEntry(master=self)
        self.path_entry.grid(row=4, column=0, 
                        pady=10, padx=10, sticky="W")

        self.icon_entry = ctk.CTkEntry(master=self)
        self.icon_entry.grid(row=8, column=0, pady=10, padx=10, sticky="W")

        self.browser_entry = ctk.CTkEntry(master=self)
        # END Entry

        # Buttons
        self.path_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("path"))
        self.path_window_button.grid(row=4, column=1, sticky="W")

        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: self.search_window("icon"))
        self.icon_window_button.grid(row=8, column=1, sticky="W")

        self.send_button = ctk.CTkButton(master=self, command=lambda: self.send(init), text="Concluir")
        self.send_button.grid(row=9, pady=15, columnspan=2)
        # END Buttons

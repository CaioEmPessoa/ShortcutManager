import customtkinter as ctk
from tkinter import messagebox

class NewSrtcWnd(ctk.CTkToplevel):
    def new_site_itens(self, newapp):
        self.new_app_itens(newapp)
        self.srtc_type = "site"

        self.path_label.configure(text="Insira o link para o site:")
        self.path_window_button.grid_forget()

        self.path_entry.configure(width=250)
        self.path_entry.grid_forget()
        self.path_entry.grid(row=4, column=0, pady=10, padx=10, columnspan=2)

        self.path_label.configure(width=250)

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador? Chrome é padrão.\n(precisa ser baseado em chromium)\n")
        self.browser_label.grid(row=5, column=0, padx=10, columnspan=2)
        
        self.browser_entry = ctk.CTkEntry(master=self, width=250)
        self.browser_entry.grid(row=6, column=0, padx=10, columnspan=2)

    def new_steam_itens(self, newapp):
        self.new_app_itens(newapp)
        self.srtc_type = "steam"
        self.path_label.configure(text="Escolha o caminho do atalho (ou link direto do jogo):")
        self.path_window_button.configure(command=lambda: newapp.search_window("steam"))

    def new_app_itens(self, newapp):
        w, h = 330, 440
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) / 2, (hs - h) / 2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((tuple(range(12))), weight=1)

        self.title("Shortcut Manager")
        self.after(200, lambda:self.iconbitmap("img/icon.ico"))

        self.srtc_type = "app"

        # Buttons, Labels and Entries
        # LABELS
        self.name_label = ctk.CTkLabel(master=self, anchor="w", text="Escolha o nome do app:", )
        self.name_label.grid(row=0, column=0, padx=10, columnspan=2)

        self.path_label = ctk.CTkLabel(master=self, text="Escolha o caminho do atalho:")
        self.path_label.grid(row=3, column=0, padx=10, columnspan=2)

        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do atalho:")
        self.icon_label.grid(row=7, column=0, padx=10, columnspan=2)

        self.bd_color_label = ctk.CTkLabel(master=self, text="Cor da borda do botão:")
        self.bd_color_label.grid(row=9, column=0, columnspan=2)

        # END Labels

        # ENTRY
        self.name_entry = ctk.CTkEntry(master=self, width=250)
        self.name_entry.grid(row=1, column=0, pady=10, padx=10, columnspan=2)

        self.path_entry = ctk.CTkEntry(master=self, width=200)
        self.path_entry.grid(row=4, column=0, pady=10, padx=10, sticky="e")

        self.icon_entry = ctk.CTkEntry(master=self, width=200)
        self.icon_entry.grid(row=8, column=0, pady=10, padx=10, sticky="e")
        
        color_list = [color for color in newapp.init.app.COLOR_DICT]

        self.bd_color_entry = ctk.CTkOptionMenu(master=self, values=color_list)
        self.bd_color_entry.grid(row=10, column=0, pady=10, padx=10, columnspan=2)
        # END Entry

        # Buttons
        self.path_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: newapp.search_window("path"))
        self.path_window_button.grid(row=4, column=1, sticky="W")

        self.icon_window_button = ctk.CTkButton(master=self, text="Janela", width=10, 
                                    command=lambda: newapp.search_window("icon"))
        self.icon_window_button.grid(row=8, column=1, sticky="W")

        self.send_button = ctk.CTkButton(master=self, text="Concluir", command=lambda: newapp.send(self), width=80)
        self.send_button.grid(row=11, column=0, pady=15, padx=15, columnspan=2)
        # END Buttons

class EditSrtcView():
    def change_elements(self, init, wnd, edit_srtc, app_to_edit):
        edit_srtc.call_srtc_wnd(init, app_to_edit)

        wnd.icon_label.configure(text="Caminho pro ícone:\n(vazio para remover)")

        wnd.send_button.grid_forget()
        wnd.send_button.grid(row=11, column=0, pady=15, columnspan=1)
        
        wnd.delete_button = ctk.CTkButton(master=wnd, fg_color="red", text="delete", width=80,
                                           command=lambda: edit_srtc.delete(srtc=app_to_edit, init=init))
        wnd.delete_button.grid(row=11, column=1, pady=15, sticky="w")

        edit_srtc.insert_data(init, wnd, app_to_edit)
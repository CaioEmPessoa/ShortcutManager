import customtkinter as ctk
from tkinter import messagebox

class NewSrtcWnd(ctk.CTkToplevel):
    def new_site_itens(self, newapp):
        self.new_app_itens(newapp)
        self.is_app = False

        w, h = 230, 440
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) / 2, (hs - h) / 2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((tuple(range(12))), weight=1)

        self.path_label.configure(text="Insira o link para o site:")
        self.path_window_button.grid_forget()

        self.browser_label = ctk.CTkLabel(master=self, text="Qual navegador? Chrome é padrão.\n(precisa ser baseado em chromium)")
        self.browser_label.grid(row=5, column=0, padx=10, columnspan=2, sticky="W")
        
        self.browser_entry = ctk.CTkEntry(master=self)
        self.browser_entry.grid(row=6, column=0, padx=10, sticky="W")

    def new_app_itens(self, newapp):
        w, h = 220, 430
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) / 2, (hs - h) / 2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((tuple(range(12))), weight=1)

        self.title("Shortcut Manager")
        self.after(200, lambda:self.iconbitmap("img/icon.ico"))

        self.is_app = True

        # Buttons, Labels and Entries
        # LABELS
        self.name_label = ctk.CTkLabel(master=self, justify="left", text="Escolha o nome do app:")
        self.name_label.grid(row=0, column=0, padx=10, columnspan=3, sticky="W")

        self.path_label = ctk.CTkLabel(master=self, text="Escolha o caminho do atalho:")
        self.path_label.grid(row=3, column=0, padx=10, columnspan=2, sticky="W")

        self.icon_label = ctk.CTkLabel(master=self, text="Escolha o icone do atalho:")
        self.icon_label.grid(row=7, column=0, padx=10, columnspan=2, sticky="W")

        self.bg_color_label = ctk.CTkLabel(master=self, text="Cor de fundo do botão:")
        self.bg_color_label.grid(row=9, column=0)

        # END Labels

        # ENTRY
        self.name_entry = ctk.CTkEntry(master=self, width=200)
        self.name_entry.grid(row=1, column=0, 
                        pady=10, padx=10, sticky="W", columnspan=3)

        self.path_entry = ctk.CTkEntry(master=self)
        self.path_entry.grid(row=4, column=0, 
                        pady=10, padx=10, sticky="W")
        
        self.bg_color_entry = ctk.CTkOptionMenu(master=self, values=["None", "Red", "Green", "Purple"])
        self.bg_color_entry.grid(row=10, column=0, 
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

        self.send_button = ctk.CTkButton(master=self, command=lambda: newapp.send(self), text="Concluir")
        self.send_button.grid(row=11, pady=15, padx=15)
        # END Buttons

class EditSrtcView():
    def change_elements(self, init, wnd, edit_srtc, app_to_edit):
        edit_srtc.call_srtc_wnd(init, app_to_edit)

        wnd.icon_label.configure(text="Path to the preview image:\n(empty to remove)")

        wnd.send_button.grid_forget()
        wnd.send_button.grid(row=11, column=0, pady=15, columnspan=1)
        
        wnd.delete_button = ctk.CTkButton(master=wnd, fg_color="red", text="delete",
                                           command=lambda:print("delete :)"))
        wnd.delete_button.grid(row=11, column=1, pady=15, padx=10)

        edit_srtc.insert_data(init, wnd, app_to_edit)
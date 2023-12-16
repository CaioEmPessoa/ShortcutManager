import customtkinter as ctk

class NewfolderWnd(ctk.CTkToplevel):
    def __init__(self, init):
        super().__init__()
        self.init = init

        w, h = 400, 200
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) / 2, (hs - h) / 2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.title("Shortcut Manager")
        self.after(500, lambda: self.iconbitmap("img/icon.ico"))

        self.new_folder_elements()

    def send_info(self):
        new_folder_name = self.name_entry.get()
        if new_folder_name == "":
            return
        
        folders_list = self.init.data["folders"]
        folders_list.append(new_folder_name)

        new_folder_dict = {
            "folders":folders_list
        }

        self.init.modify_data.write_data(new_folder_dict)
        self.init.call_window("restart")

    def new_folder_elements(self):
        self.name_label = ctk.CTkLabel(master=self, text="Insira o nome da pasta:")
        self.name_label.pack(pady=7)

        self.name_entry = ctk.CTkEntry(master=self, width=300)
        self.name_entry.pack(pady=15)
        self.name_entry.focus()

        self.send_btn = ctk.CTkButton(master=self, text="Ok", width=50, command=lambda: self.send_info())
        self.send_btn.pack(pady=15)

        self.bind("<Return>", lambda e: self.send_info())
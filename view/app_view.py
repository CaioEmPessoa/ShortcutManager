import customtkinter as ctk
from tkinter import Menu
from PIL import Image

class PopupMenu():
    def __init__(self, init, app, app_wnd):
        super().__init__()
        self.init, self.app, self.app_wnd = init, app, app_wnd

    def create_menus(self, app_name=False):
        self.main_menu = Menu(tearoff=0)
        
        self.size_menu = Menu(tearoff=0)
        self.size_menu.add_command(label="Ícones Grandes", command= lambda: self.app_wnd.change_icon_size("G"))
        self.size_menu.add_command(label="Ícones Médios", command= lambda: self.app_wnd.change_icon_size("M"))
        self.size_menu.add_command(label="Ícones Pequenos", command= lambda: self.app_wnd.change_icon_size("P"))

        if app_name:
            self.folder_menu = Menu(tearoff=0)
            for folder in self.init.data["folders"]:
                self.folder_menu.add_command(label=folder, command= lambda right_folder = folder: self.app.send_to_folder(app_name, right_folder))
            self.main_menu.add_cascade(label="Enviar Atalho Para...", menu=self.folder_menu)
        
        self.main_menu.add_cascade(label="Exibir", menu=self.size_menu)
        self.main_menu.add_checkbutton(label="Mostrar Ícones?")

    def show_srtc_menu(self, event, app_name):
        self.create_menus(app_name)
        self.main_menu.tk_popup(event.x_root, event.y_root)

    def show_main_menu(self, event):
        self.create_menus()
        self.main_menu.tk_popup(event.x_root, event.y_root)

class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((1), weight=1)

class AppWnd(ctk.CTk):
    def __init__(self, init, app):
        super().__init__()
        self.init, self.app, self.menu = init, app, PopupMenu(init, app, self)

        self.title("Shortcut Manager")
        self.iconbitmap("img/icon.ico")

        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.set_appearance_mode(init.data["theme"])

        w, h = tuple(self.init.data["wnd_size"])
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws/2) - (w/2), (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.app_size = (w, h)
        self.icon_size = self.init.data["srtc_size"]
        self.main_tab = "Default"
        self.max_columns = 3

        self.create_itens()
        self.after(5, self.adjust_shortcuts_grid)
        self.protocol("WM_DELETE_WINDOW", lambda:app.on_close(self.app_size))

    def create_itens(self):
        welcome = ctk.CTkLabel(master=self, text="Escolha um ou adicione um novo atalho", 
                               font=('Segoe UI', 20), text_color="#807e7e", width=500)
        welcome.grid(row=0, column=0, columnspan=3)

        self.add_button = ctk.CTkOptionMenu(self, values=["App", "Site", "folder"], width=70, dropdown_direction="up",
                                            command=lambda x: self.init.call_window(self.add_button.get()))
        self.add_button.set("Add")
        self.add_button.grid(row=2, column=0, padx=10, pady=10, sticky="E")

        edit_button = ctk.CTkButton(master=self, text="Editar", width=70,
                                    command=lambda: self.app.enable_edit())
        edit_button.grid(row=2, column=1, pady=10)

        theme_buttom = ctk.CTkButton(master=self, text="Tema", width=70,
                                     command=lambda: self.app.switch_theme())
        theme_buttom.grid(row=2, column=2, 
                          padx=10, pady=10, sticky="W")

        self.create_tabs()

        self.create_shortcuts() 

        self.grid_srcts()


    def create_tabs(self):
        self.folders_tab = ctk.CTkTabview(master=self)
        self.folders_tab.grid(row=1, column=0, columnspan=3, padx=15, pady=15, sticky="nsew")
        self.folders_frame = {}
        
        for folder in self.init.data["folders"]:
            self.folders_tab.add(folder)
            my_frame = ScrollFrame(master=self.folders_tab.tab(folder))
            my_frame.pack(fill="both", expand=True)
            
            self.folders_frame[folder] = my_frame

            my_frame.bind("<Button-3>", lambda e: self.menu.show_main_menu(e))

    def create_shortcuts(self):
        try:
            data = self.init.data["apps"]

        except KeyError:
            return
        
        # creating lists to store btns ont its folders
        for folder in self.init.data["folders"]:
            self.app.srtc_btns[folder] = []

        icon_size = self.app.SIZE_DICT[self.icon_size]["icon"]
        srtc_size = self.app.SIZE_DICT[self.icon_size]["srtc"]
        
        for app_name in data:
            app_data = data[app_name]

            icon = ctk.CTkImage(light_image=Image.open(app_data["icon"]),size=(icon_size))

            name = self.app.correct_name(app_data["name"])
            app_button = ctk.CTkButton(master=self.folders_frame[app_data["folder"]], 
                                       width=srtc_size, height=srtc_size, compound="top", 
                                       text=name, command=lambda app_path=app_data["path"]: self.app.open_app(app_path), 
                                       image=icon, font=('Segoe UI', 16),
                                       text_color="#807e7e", border_width=2.5, border_color="#1f6aa5", 
                                       hover_color="#184c74", fg_color=self.app.COLOR_DICT[app_data["bg_color"]])
            
            app_button.bind("<Button-3>", lambda e, name=app_data["name"]: self.menu.show_srtc_menu(e, name))
            
            self.app.srtc_btns[app_data["folder"]].append(app_button)

    def grid_srcts(self):
        for folder in self.app.srtc_btns:
            btn_nmb = 0
            for srtc_btn in self.app.srtc_btns[folder]:
                row = btn_nmb // self.max_columns
                col = btn_nmb % self.max_columns
                srtc_btn.grid(row=row, column=col, pady=10, padx=5)
                btn_nmb+=1

    def change_icon_size(self, size):
        self.icon_size = size
        for folder in self.app.srtc_btns:
            for btn in self.app.srtc_btns[folder]:
                btn.destroy()

        self.app.srtc_btns = {}
        self.create_shortcuts()
        self.grid_srcts()

    def adjust_shortcuts_grid(self):
        current_tab = self.folders_tab.get()
        srtc_size = self.app.SIZE_DICT[self.icon_size]["srtc"]

        new_size = (self.winfo_width(), self.winfo_height())
        if new_size != self.app_size or current_tab != self.main_tab:
            self.app_size = new_size
            self.main_tab = current_tab

            max_columns = int(self.winfo_width() / int(srtc_size+50))
            if max_columns == 0:
                self.max_columns = max_columns

            for folder in self.app.srtc_btns:
                for btn in self.app.srtc_btns[folder]:
                    btn.grid_forget()

                self.grid_srcts()
            
            btn_ammount = len(self.app.srtc_btns[self.main_tab])
            if self.max_columns > btn_ammount and btn_ammount != 0:
                self.max_columns = btn_ammount
                        
            self.folders_frame[self.main_tab].grid_columnconfigure((tuple(range(self.max_columns))), weight=1)

        #restart loop
        self.after(5, self.adjust_shortcuts_grid)


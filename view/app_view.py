import customtkinter as ctk
from tkinter import Menu, BooleanVar
from textwrap import wrap
from PIL import Image
import ctypes

class PopupMenu():
    def __init__(self, init, app, app_wnd):
        super().__init__()
        self.init, self.app, self.app_wnd = init, app, app_wnd

    def create_menus(self, srtc_id=False):
        self.main_menu = Menu(tearoff=0)
        
        self.size_menu = Menu(tearoff=0)
        self.size_menu.add_command(label="Ícones Grandes", command= lambda: self.app_wnd.change_icon_size("G"))
        self.size_menu.add_command(label="Ícones Médios", command= lambda: self.app_wnd.change_icon_size("M"))
        self.size_menu.add_command(label="Ícones Pequenos", command= lambda: self.app_wnd.change_icon_size("P"))

        # se for botão direito em um atalho
        if srtc_id:
            # adiciona o editar
            self.main_menu.add_command(label="Editar", command=lambda app=srtc_id: self.init.call_window("edit", app))
            
            # adiciona o enviar para
            self.folder_menu = Menu(tearoff=0)
            for folder in self.init.data["folders"]:
                self.folder_menu.add_command(label=folder, command= lambda right_folder = folder: self.app.send_to_folder(srtc_id, right_folder))
            self.main_menu.add_cascade(label="Enviar Atalho Para...", menu=self.folder_menu)
            
            # submenu pra mover atalho de lugar
            self.move_menu = Menu(tearoff=0)
            app_data = self.init.data["apps"]
            start = [i for i in app_data].index(srtc_id)
            pos = 0 # used for change location label
            for i in app_data:
                if app_data[i]["folder"] != self.app_wnd.folders_tab.get(): # hides apps from another tab
                    continue

                pos += 1
                if i == srtc_id: # don't add same srtc to the submenu
                    continue
                command_label = f"{pos} ({app_data[i]["name"]})"
                self.move_menu.add_command(label=command_label, command= lambda start=start, end=pos-1: self.app.move_srct(start, end))

            self.main_menu.add_cascade(label="Mover Atalho Para...", menu=self.move_menu)

            self.main_menu.add_separator()

        self.main_menu.add_cascade(label="Exibir", menu=self.size_menu)

        self.main_menu.add_checkbutton(label="Mostrar Ícones?", 
                                       command=lambda: self.app.show_icons(self.app_wnd.check_btn.get()),
                                       variable=self.app_wnd.check_btn, onvalue=1, offvalue=0)
        
    def show_srtc_menu(self, event, srtc_id):
        self.create_menus(srtc_id)
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

        self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)/100

        w, h = tuple(self.init.data["wnd_size"])
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws/2) - (w/2), (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x*self.scale_factor, y*self.scale_factor))

        self.check_btn = BooleanVar()
        self.check_btn.set(self.init.data["show_icons"])
        self.app_size = (w, h)
        self.icon_size = self.init.data["srtc_size"]
        self.main_tab = "Default"
        self.max_columns = 3

        self.create_itens()
        self.after(5, self.adjust_shortcuts_grid)
        self.protocol("WM_DELETE_WINDOW", lambda:init.call_window("close"))

        self.bind("<MouseWheel>", self.switch_tabs)

    def create_itens(self):
        welcome = ctk.CTkLabel(master=self, text="Escolha um ou adicione um novo atalho", 
                               font=('Segoe UI', 20), text_color="#807e7e", width=500)
        welcome.grid(row=0, column=0, columnspan=3)

        self.add_button = ctk.CTkOptionMenu(self, values=["App", "Site", "Steam", "Pasta"], width=70, dropdown_direction="up",
                                            command=lambda x: self.init.call_window(self.add_button.get()))
        self.add_button.set("Novo")
        self.add_button.grid(row=2, column=0, padx=10, pady=10, sticky="E")

        edit_button = ctk.CTkButton(master=self, text="Editar", width=70,
                                    command=lambda: self.app.enable_edit())
        edit_button.grid(row=2, column=1, padx=10, pady=10)

        theme_buttom = ctk.CTkButton(master=self, text="Tema", width=70,
                                     command=lambda: self.app.switch_theme())
        theme_buttom.grid(row=2, column=2, padx=10, pady=10, sticky="W")

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

        size_dict_info = self.app.SIZE_DICT[self.icon_size]
        icon_size = size_dict_info["icon"]
        srtc_size = size_dict_info["srtc"]
        wrap_size = size_dict_info["wrap"]
        
        for app_name in data:
            app_data = data[app_name]

            if app_data["icon"] == "None":
                icon = ctk.CTkImage(light_image=Image.open("img/unknown_light.png"), dark_image=Image.open("img/unknown_dark.png"), size=(icon_size))
            else:
                icon = ctk.CTkImage(light_image=Image.open(app_data["icon"]),size=(icon_size))

            name = "\n".join(wrap(app_data["name"], wrap_size-1))
            bd_color = self.app.COLOR_DICT[app_data["bd_color"]]
            text_color = ("Black", "White")
            show_icons = self.init.data["show_icons"]
            compound="top"
            
            if not show_icons:
                compound="bottom"
                icon = ""

            app_button = ctk.CTkButton(master=self.folders_frame[app_data["folder"]], 
                                       width=srtc_size, height=srtc_size, compound=compound, 
                                       text=name, command=lambda app_path=app_data["path"]: self.app.open_app(app_path), 
                                       image=icon, font=("Consolas", 16),
                                       text_color=text_color, border_width=3, border_color=bd_color, 
                                       hover_color=("#37709f", "#184c74"), fg_color="transparent")
                        
            app_button.bind("<Button-3>", lambda e, srtc_id=app_data["id"]: self.menu.show_srtc_menu(e, srtc_id))
            
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
        self.init.data["srtc_size"] = self.icon_size
        
        for folder in self.app.srtc_btns:
            for btn in self.app.srtc_btns[folder]:
                btn.destroy()

        self.app.srtc_btns = {}
        self.create_shortcuts()
        self.grid_srcts()
        self.adjust_shortcuts_grid(True)

    def adjust_shortcuts_grid(self, size_cng=False):
        current_tab = self.folders_tab.get()
        srtc_size = self.app.SIZE_DICT[self.icon_size]["srtc"]

        new_size = (self.winfo_width()/self.scale_factor, self.winfo_height()/self.scale_factor)
        if new_size != self.app_size or current_tab != self.main_tab or size_cng:
            self.app_size = new_size
            self.main_tab = current_tab

            max_columns = int(self.winfo_width() / int(srtc_size+50))
            if max_columns != 0:
                self.max_columns = max_columns

            for folder in self.app.srtc_btns:
                for btn in self.app.srtc_btns[folder]:
                    btn.grid_forget()

                self.grid_srcts()
            
            try:
                btn_ammount = len(self.app.srtc_btns[self.main_tab])
            except KeyError:
                btn_ammount = 0

            if self.max_columns > btn_ammount and btn_ammount != 0:
                self.max_columns = btn_ammount
            
            self.folders_frame[self.main_tab].grid_columnconfigure((tuple(range(self.max_columns))), weight=1)

        #restart loop
        self.after(5, self.adjust_shortcuts_grid)

    def switch_tabs(self, event):
        current_tab_index = self.init.data["folders"].index(self.folders_tab.get())

        # if scroll is not vertical
        if event.state != 9:
            return
        # left
        if event.delta > 0 and current_tab_index != 0:
            prev_tab = self.init.data["folders"][current_tab_index-1]
            self.folders_tab.set(prev_tab)
        # right
        elif event.delta < 0 and current_tab_index != len(self.init.data["folders"])-1:
            next_tab = self.init.data["folders"][current_tab_index+1]
            self.folders_tab.set(next_tab)

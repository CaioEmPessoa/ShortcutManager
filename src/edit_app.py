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

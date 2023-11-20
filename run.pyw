from customtkinter import set_appearance_mode
import json

#my code
import main
from src import new_app
from src import edit_app

class DefaultClass():

    def call_window(self, window):

        match window:
            case "root":
                self.root = main.Root(self)

                self.root.mainloop()

            case "add_app":
                self.add_app = new_app.AddApp(self)
                self.add_app.grab_set()

            case "edit":
                self.add_app = edit_app.EditAppWindow(self, app)
                self.add_app.grab_set()


            case "restart":
                default = DefaultClass()

            case "close":
                self.root.destroy()

    def switch_theme(self):
        # If the theme is dark it switches it to light and vice-versa
        if self.theme == "Light":
            theme_data = {"theme": "Light"}
            self.theme = "Dark"

        elif self.theme == "Dark":
            theme_data = {"theme": "Dark"}
            self.theme = "Light"

        self.modify_data.write_data(theme_data)
        set_appearance_mode(self.theme)

default = DefaultClass()
default.call_window("root")

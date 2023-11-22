from src import modify_data
from src import app
from view import app_view
from src import new_app
from view import new_app_view
from src import edit_app
from view import edit_app_view

class DefaultClass():
    def __init__(self):
        super().__init__(self)



        self.app = app.App(self)
        self.app_view = app_view.AppWnd(self, self.root)
        self.app_view.mainloop()

    def call_window(self, window):

        match window:
            case "root":
                self.root_view.destroy()
                default = DefaultClass()

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

if __name__ == "__main__":
    default = DefaultClass()
    default.call_window("root")

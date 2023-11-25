from src import modify_data
from src import app
from view import app_view
from src import new_app
from view import new_app_view
from src import edit_app
from view import edit_app_view

class DefaultClass():
    def __init__(self):
        super().__init__()

        self.modify_data = modify_data.ModifyData()
        self.data = self.modify_data.read_data()
        
        self.app = app.App(self)
        self.app_view = app_view.AppWnd(self, self.app)
        self.app_view.mainloop()

    def call_window(self, window):

        match window:
            case "root":
                self.app_view.destroy()
                default = DefaultClass()

            case "add_app":
                self.add_app_view = new_app_view.NewAppWnd()
                self.add_app = new_app.AddApp(self)
                self.add_app_view.create_itens(self.add_app)
                self.add_app_view.grab_set()

            case "edit":
                self.add_app = edit_app.EditAppWindow(self, app)
                self.add_app.grab_set()


            case "restart":
                self.app_view.destroy()
                default = DefaultClass()

            case "close":
                self.app_view.destroy()

if __name__ == "__main__":
    default = DefaultClass()

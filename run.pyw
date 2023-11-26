from src import modify_data
from src import app
from view import app_view
from src import add_edit_shorcuts
from view import add_edit_shorcuts_view

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

            case "App":
                self.app_view.add_button.set("Add")
                self.add_app_view = add_edit_shorcuts_view.NewAppWnd()
                self.add_app = add_edit_shorcuts.AddApp(self)
                self.add_app_view.new_app_itens(self.add_app)
                self.add_app_view.grab_set()
            
            case "Site":
                self.app_view.add_button.set("Add")
                self.add_app_view = add_edit_shorcuts_view.NewAppWnd()
                self.add_app = add_edit_shorcuts.AddApp(self)
                self.add_app_view.new_site_itens(self.add_app)
                self.add_app_view.grab_set()

            case "Pasta":
                self.app_view.add_button.set("Add")
                print("don't.")

            case "edit":
                print("don't.")

            case "restart":
                self.app_view.destroy()
                default = DefaultClass()

            case "close":
                self.app_view.destroy()

if __name__ == "__main__":
    default = DefaultClass()

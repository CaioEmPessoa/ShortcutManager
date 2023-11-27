from src import modify_data
from src import app
from view import app_view
from src import sct_manage
from view import app_sct_view
from view import site_sct_view

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

                self.app_sct_view = app_sct_view.AppSctWnd()
                self.sct_manage = sct_manage.AddEdit(self)
                self.sct_manage.add_app(self.app_sct_view)
            
            case "Site":
                self.app_view.add_button.set("Add")

                self.site_sct_view = site_sct_view.SiteSctWnd()
                self.sct_manage = sct_manage.AddEdit(self)
                self.sct_manage.add_site(self.site_sct_view)
                

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

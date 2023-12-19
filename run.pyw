from src import modify_data
from src import app
from view import app_view
from src import srtc_manage
from view import srtc_manage_view
from src import manage_folders

class DefaultClass():
    def __init__(self):
        super().__init__()

        self.modify_data = modify_data.ModifyData()
        self.data = self.modify_data.read_data()
 
        self.app = app.App(self)
        self.app_view = app_view.AppWnd(self, self.app)
        self.app_view.mainloop()

    def call_window(self, window, app_to_edit=None):

        self.app_view.add_button.set("Add")
        match window:
            case "root":
                self.app_view.destroy()
                default = DefaultClass()

            case "App":
                self.add_srtc_view = srtc_manage_view.NewSrtcWnd()
                self.add_srtc = srtc_manage.AddSrtc(self)
                self.add_srtc_view.new_app_itens(self.add_srtc)
                self.add_srtc_view.grab_set()
            
            case "Site":
                self.add_srtc_view = srtc_manage_view.NewSrtcWnd()
                self.add_srtc = srtc_manage.AddSrtc(self)
                self.add_srtc_view.new_site_itens(self.add_srtc)
                self.add_srtc_view.grab_set()

            case "folder": 
                self.add_folder = manage_folders.NewfolderWnd(self)
                self.add_folder.grab_set()

            case "edit":
                self.add_srtc_view = srtc_manage_view.NewSrtcWnd()
                self.add_srtc = srtc_manage.AddSrtc(self)
                self.edit_srtc = srtc_manage.Edit()
                self.srtc_edit = srtc_manage_view.EditSrtcView().change_elements(self, self.add_srtc_view, self.edit_srtc, app_to_edit)
                self.add_srtc_view.grab_set()

            case "restart":
                self.app_view.destroy()
                default = DefaultClass()

            case "close":
                self.app_view.destroy()

if __name__ == "__main__":
    default = DefaultClass()

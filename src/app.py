class App():
    def __init__(self):
        super.__init__(self)

    def change_buttons(self, init):

        # COLOCA PRA EDITAR OS APPS
        if init.changing == 0:
            init.changing = 1
            for button in init.created_buttons:
                button.configure(border_color="red", command=lambda app=init.names_list[init.created_buttons.index(button)]: init.call_edit_window(app))

        # VOLTA AO NORMAL
        else:
            init.changing = 0
            for button in init.created_buttons:
                button.configure(border_color="#1f6aa5", command=lambda app=init.path_list[init.created_buttons.index(button)]: self.open_app(init, app))

    def open_app(self, init, path):

        try:
            # It is a app
            # get the path of the app
            dir_path = os.path.dirname(path)
            os.chdir(dir_path[1:])
            os.startfile(path)

        except:
            # It is a website
            os.system(f"{path}")
            

            
        init.call_window("close")
class Model:
    def __init__(self, controller):
        self.controller = controller
        self.current_set = None

    def create_new_set(self, set_data):
        self.current_set = set_data

    def load_set(self, set_name):
        pass

    def save_current_set(self, file_name):
        pass
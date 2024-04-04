import model
import view
import time
import os
import sys

class Controller:
    def __init__(self):
        self.model = model.Model(self)
        self.view = view.View(self)
        self.framerate = 15
        self.last_update = time.time()

        # update loop
        self.active = True
        while self.active:

            # checking framerate
            curr_time = time.time()
            dt = curr_time - self.last_update
            if dt > 1 / self.framerate:

                # updating
                self.last_update = curr_time
                self.update(dt)

    def on_closing(self):
        self.active = False
        self.view.window.destroy()

    def update(self, dt):
        self.view.update()

    def prompt_new_set(self, set_data=None, set_name=None):
        self.view.set_window("new_set_prompt", set_data, set_name)

    def prompt_load_set(self, *args):
        all_files = []
        for file in os.listdir(self.model.sets_folder):
            if file.endswith(".set"):
                all_files.append(file)

        self.view.set_window("load_set", all_files, *args)

    def prompt_delete_set(self, set_name):

        # double checking action
        def on_yes():
            os.remove(self.model.sets_folder + "/" + set_name)
            self.view.reset_view()
            self.prompt_load_set()

        def on_no():
            self.view.back_button()

        self.view.set_window("are_you_sure", f"Do you want to delete the card set {set_name}?", on_yes, on_no)

    def create_new_set(self, set_data, name):
        self.model.create_new_set(set_data, name)
        self.view.reset_view()
        self.prompt_load_set()
    
    def load_set(self, set_name, callback=None, *callback_args):
        self.model.load_set(set_name)
        if callback != None:
            callback(*callback_args)

    def prompt_practice(self):
        self.prompt_load_set(self.view.set_window, "practice_menu")

    def prompt_settings(self):
        self.view.set_window("settings_menu")

    def confirm_settings_change(self, settings: dict):
        self.model.apply_settings(settings)
        self.model.save_cache_file("settings", settings)

    def start_quiz(self, subset, to_flip, to_shuffle):
        quiz_data = self.model.create_quiz(subset, to_flip, to_shuffle)
        self.view.set_window("practice_quiz", quiz_data)

# starting
Controller()
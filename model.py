import random
import os
import ast

class Model:
    def __init__(self, controller):
        self.controller = controller
        self.current_set = None
        self.current_set_name = ""

        self.folder_path = os.path.dirname(__file__).replace("\\", "/")
        self.sets_folder = self.folder_path + "/CardSets"
        self.cache_folder = self.folder_path + "/Cache"
        self.load_settings()

        # creating folders
        if not os.path.exists("CardSets"):
            os.mkdir("CardSets")

        if not os.path.exists("Cache"):
            os.mkdir("Cache")

    def save_cache_file(self, file_name, file_content: dict):
        with open(self.cache_folder + "/" + file_name, "w") as f:
            f.write(str(file_content))
            f.close()

    def load_cache_file(self, file_name):
        if os.path.exists(self.cache_folder + "/" + file_name):
            file = open(self.cache_folder + "/" + file_name)
            string_text = file.read()
            cache_dict = ast.literal_eval(string_text)
            return cache_dict
        
    def load_settings(self):
        file_path = self.cache_folder + "/settings"
        if os.path.exists(file_path):
            settings = self.load_cache_file("settings")
            self.apply_settings(settings)
        
    def apply_settings(self, settings: dict):
        for property_name in settings:
            property_value = settings[property_name]
            if getattr(self, property_name):
                setattr(self, property_name, property_value)

    def change_folder_path(self, property_name: str, new_folder_path: str):
        if getattr(self, property_name):
            if os.path.exists(new_folder_path):
                setattr(self, property_name, new_folder_path)

    def shuffle_set(self, set_data=None):
        if set_data == None:
            set_data = self.current_set

        # shuffling set
        shuffled_set = []
        used_indices = []

        for i in range(len(set_data)):

            # finding random index
            card_index = None
            while card_index == None or card_index in used_indices:
                card_index = random.randint(0, len(set_data) - 1)

            # adding card
            shuffled_set.append(set_data[card_index])
            used_indices.append(card_index)

        # returning shuffled set
        return shuffled_set
    
    def get_subset(self, var):
        
        # getting current text
        text = var.get()
        split = text.split("-")
        first_index = int(split[0])
        second_index = int(split[1])
        first_index = min(first_index, second_index)

        # getting subset
        subset = self.current_set[first_index - 1 : second_index]

        # returning
        return subset
    
    def flip_set(self, set_data=None):
        if set_data == None:
            set_data = self.current_set

        # creating flipped set
        flipped = []
        for card in set_data:
            flipped.append((card[1], card[0]))

        # returning
        return flipped

    def create_new_set(self, set_data, set_name):
        self.current_set = set_data
        self.current_set_name = set_name
        self.save_current_set()

    def load_set(self, file_name):
        set_data = []

        # finding file
        with open(self.sets_folder + "/" + file_name, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                set_data.append(tuple(line.split(",")))

        # setting open set
        self.current_set = set_data
        self.current_set_name = file_name.replace(".set", "")

    def save_current_set(self):
        if self.current_set == None:
            return
        
        # creating file
        file_name = self.current_set_name + ".set"
        with open(self.sets_folder + "/" + file_name, "w", encoding="utf-8") as f:
            file_content = ""
            for card in self.current_set:
                file_content += card[0] + "," + card[1] + "\n"
                
            # writing file
            f.write(file_content)

    def load_set_text(self, file_name=None):
        if file_name == None:
            file_name = self.current_set_name + ".set"

        # saving
        

        # loading
        with open(self.sets_folder + "/" + file_name, "r", encoding="utf-8") as file:
            return file.read()
        
    def apply_direct_edit(self, file_text, file_name=None):
        if file_name == None:
            file_name = self.current_set_name + ".set"

        # checking validity
        lines = file_text.split("\n")
        for line in lines:
            if line != "":
                split = line.split(",")
                if len(split) != 2:
                    return "Invalid"

        # saving to file
        with open(self.sets_folder + "/" + file_name, "w", encoding="utf-8") as file:
            file.write(file_text)

        # loading file again
        self.load_set(file_name)

        # success
        return "Success"

    def create_quiz(self, subset, to_flip, to_shuffle):

        # creating quiz data
        quiz_data = self.current_set[subset[0]:subset[1]]
        if to_flip:
            quiz_data = self.flip_set(quiz_data)
        if to_shuffle:
            quiz_data = self.shuffle_set(quiz_data)

        # returning quiz
        return quiz_data
        
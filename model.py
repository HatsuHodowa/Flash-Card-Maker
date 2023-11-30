import random

class Model:
    def __init__(self, controller):
        self.controller = controller
        self.current_set = None
        self.current_set_name = ""

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
        with open("CardSets/" + file_name, "r", encoding="utf-8") as f:
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
        with open("CardSets/" + file_name, "w", encoding="utf-8") as f:
            file_content = ""
            for card in self.current_set:
                file_content += card[0] + "," + card[1] + "\n"
                
            # writing file
            f.write(file_content)

    def create_quiz(self, subset, to_flip, to_shuffle):

        # creating quiz data
        quiz_data = self.current_set[subset[0]:subset[1]]
        if to_flip:
            quiz_data = self.flip_set(quiz_data)
        if to_shuffle:
            quiz_data = self.shuffle_set(quiz_data)

        # returning quiz
        return quiz_data
        
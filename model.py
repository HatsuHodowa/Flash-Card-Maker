class Model:
    def __init__(self, controller):
        self.controller = controller
        self.current_set = None
        self.current_set_name = ""

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
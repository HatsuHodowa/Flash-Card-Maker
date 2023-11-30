from tkinter import *
import tkinter.font as tkFont
import time
import threading

class View:
    def __init__(self, controller):
        self.controller = controller
        
        # creating main window
        self.window = Tk()
        self.error_label = None
        self.window.protocol("WM_DELETE_WINDOW", self.controller.on_closing)

        # color scheme & configuration
        self.background = "#303030"
        self.middleground = "gray"
        self.foreground = "white"
        self.error = "red"

        self.widget_padx = 10
        self.widget_pady = 5
        self.window_padx = 15
        self.window_pady = 15

        self.heading_font = tkFont.Font(self.window, family="Helvetica", size=24, weight="bold")
        self.subheading_font = tkFont.Font(self.window, family="Helvetica", size=18, weight="bold")
        self.normal_font = tkFont.Font(self.window, family="Helvetica", size=14)

        self.card_front_color = "#dddddd"
        self.card_back_color = "#505050"

        self.card_front_text = "#000000"
        self.card_back_text= "#ffffff"

        self.widget_padding = {"padx":self.widget_padx, "pady":self.widget_pady}
        self.widget_grid_kwargs = {"sticky":NSEW, "padx":self.widget_padx, "pady":self.widget_pady}
        self.spacer_kwargs = {"bg":self.background, "fg":self.foreground, "text":"", "height":2}

        self.title_kwargs = {"bg":self.background, "fg":self.foreground, "font":self.heading_font}
        self.subtitle_kwargs = {"bg":self.background, "fg":self.foreground, "font":self.subheading_font}
        self.label_kwargs = {"bg":self.background, "fg":self.foreground, "font":self.normal_font}
        self.error_kwargs = {"bg":self.background, "fg":self.error, "font":self.normal_font, "justify":CENTER}
        self.entry_kwargs = {"bg":self.middleground, "fg":self.foreground, "font":self.normal_font, "width":15}

        self.button_kwargs = {"bg":self.middleground, "fg":self.foreground, "font":self.normal_font, "width":15}
        self.big_button_kwargs = {"bg":self.middleground, "fg":self.foreground, "font":self.subheading_font}
        self.back_button_kwargs = {"bg":"#ab3c3c", "fg":self.foreground, "font":self.normal_font, "width":15, "command":self.back_button}
        self.reset_button_kwargs = {"bg":"#996b32", "fg":self.foreground, "font":self.normal_font, "width":15, "command":self.reset_button}
        self.red_button_kwargs = {"bg":"#ab3c3c", "fg":self.foreground, "font":self.normal_font, "width":15}
        self.green_button_kwargs = {"bg":"#3cab4b", "fg":self.foreground, "font":self.normal_font, "width":15}

        # other attributes
        self.current_card = None
        self.current_side = False

        self.window_history = []
        self.window_args_history = []

        # opening main menu
        self.set_window("main_menu")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def set_window(self, to_set, *args, **kwargs):
        
        # setting window with args
        self.clear_window()
        self.window.configure(background=self.background, padx=self.window_padx, pady=self.window_pady)
        getattr(self, to_set)(*args)

        # adding to history
        if not "history_disabled" in kwargs or kwargs["history_disabled"] == False:
            self.window_history.append(to_set)
            self.window_args_history.append(args)

    def back_button(self):

        # checking history
        if len(self.window_history) > 1:
            
            # finding last page
            last_window = self.window_history[-2]
            last_window_args = self.window_args_history[-2]

            # reverting
            self.window_history.pop()
            self.window_args_history.pop()
            self.set_window(last_window, *last_window_args)
            self.window_history.pop()
            self.window_args_history.pop()
        
        else:
            self.set_window("main_menu")

    def reset_button(self):

        # checking history
        if len(self.window_history) >= 1:
            this_window = self.window_history[-1]
            this_window_args = self.window_args_history[-1]

            # re-opening
            self.set_window(this_window, *this_window_args, history_disabled=True)

    def create_error(self, message="An error ocurred", error_time=2):

        # destroying previous error
        if self.error_label != None:
            self.clear_error()

        # creating and packing error
        self.error_label = Label(self.window, **self.error_kwargs, text=message)
        self.error_label.grid(row=100, column=0, columnspan=100)

    def clear_error(self):
        if self.error_label != None:
            self.error_label.destroy()
            self.error_label = None

    def numeric_range_entry(self, var, set_data):

        # filtering text
        text = var.get()
        new_text = ""
        has_dash = False

        for char in text:
            if char.isnumeric() or (char == "-" and not has_dash):
                new_text += char

            if char == "-":
                has_dash = True

        # checking numbers
        if has_dash and new_text.split("-")[1] != "":

            # setting caps
            split = new_text.split("-")
            first_index = max(min(int(split[0]), len(set_data)), 1)
            second_index = max(min(int(split[1]), len(set_data)), 1)

            # setting text
            var.set(f"{first_index}-{second_index}")

        else:
            var.set(new_text)

    def boolean_button_toggle(self, button):
        if button.cget("text") == "True":
            button.config(text="False", **self.red_button_kwargs)
        else:
            button.config(text="True", **self.green_button_kwargs)

    def main_menu(self):

        # creating window items
        title = Label(self.window, text="Flash Card Maker", **self.title_kwargs)
        create_button = Button(self.window, text="Create New Set", **self.big_button_kwargs, command=self.controller.prompt_new_set)
        open_button = Button(self.window, text="Load Previous Set", **self.big_button_kwargs, command=self.controller.prompt_load_set)
        practice_button = Button(self.window, text="Practice Set", **self.big_button_kwargs, command=self.controller.prompt_practice)

        # adding window items
        title.grid(row=0, column=1, **self.widget_grid_kwargs)
        create_button.grid(row=1, column=1, **self.widget_grid_kwargs)
        open_button.grid(row=2, column=1, **self.widget_grid_kwargs)
        practice_button.grid(row=3, column=1, **self.widget_grid_kwargs)

    def new_set_prompt(self, set_data=None, name=None):

        # creating window items
        title = Label(self.window, text="Create New Card Set", **self.title_kwargs)
        set_name_title = Label(self.window, **self.label_kwargs, text="Set Name")
        set_name = Entry(self.window, **self.entry_kwargs)

        card_list = Listbox(self.window, **self.entry_kwargs, height=6)
        scrollbar = Scrollbar(self.window)

        card_key_title = Label(self.window, **self.label_kwargs, text="Term")
        card_key = Entry(self.window, **self.entry_kwargs)
        card_value_title = Label(self.window, **self.label_kwargs, text="Definition")
        card_value = Entry(self.window, **self.entry_kwargs)

        delete_buton = Button(self.window, **self.button_kwargs, text="Delete Card")
        new_button = Button(self.window, **self.button_kwargs, text="Create Card")
        cancel_button = Button(self.window, **self.back_button_kwargs, text="Cancel")
        confirm_button = Button(self.window, **self.green_button_kwargs, text="Confirm")

        # adding window items
        title.grid(row=0, column=0, columnspan=2, **self.widget_grid_kwargs)
        set_name_title.grid(row=1, column=0, **self.widget_grid_kwargs)
        set_name.grid(row=1, column=1, **self.widget_grid_kwargs)
        card_list.grid(row=2, column=0, columnspan=2, **self.widget_grid_kwargs)
        scrollbar.grid(row=2, column=2, sticky=NSEW, pady=self.widget_pady)

        card_key_title.grid(row=3, column=0, **self.widget_grid_kwargs)
        card_key.grid(row=3, column=1, **self.widget_grid_kwargs)
        card_value_title.grid(row=4, column=0, **self.widget_grid_kwargs)
        card_value.grid(row=4, column=1, **self.widget_grid_kwargs)

        delete_buton.grid(row=5, column=0, **self.widget_grid_kwargs)
        new_button.grid(row=5, column=1, **self.widget_grid_kwargs)
        cancel_button.grid(row=6, column=0, **self.widget_grid_kwargs)
        confirm_button.grid(row=6, column=1, **self.widget_grid_kwargs)

        # loading current set info
        if name != None:
            set_name.insert(0, name)

        if set_data != None:
            for card in set_data:
                key = card[0]
                value = card[1]

                card_list.insert(END, f"{key} : {value}")

        # button functions
        def create_new_card():

            # finding card key/value
            key = card_key.get()
            value = card_value.get()

            if key == "" or value == "":
                self.create_error("Missing term or definition")
                return
            else:
                self.clear_error()
            
            # creating new card
            card_list.insert(END, f"{key} : {value}")

            # clearing entries
            card_key.delete(0, END)
            card_value.delete(0, END)

        def delete_card():
            for i in card_list.curselection():
                card_list.delete(i)

        def confirm_set():
            
            # checking set name
            name = set_name.get()
            if name == "":
                self.create_error("Missing card set name")
                return
            else:
                self.clear_error()
            
            # getting set data
            set_data = []
            for card_text in card_list.get(0, END):
                card_split = card_text.split(" : ")
                key = card_split[0]
                value = card_split[1]

                set_data.append((key, value))

            # creating set
            self.controller.create_new_set(set_data, name)

        # configuration
        scrollbar.config(command=card_list.yview)
        card_list.config(yscrollcommand=scrollbar.set)
        new_button.config(command=create_new_card)
        delete_buton.config(command=delete_card)
        confirm_button.config(command=confirm_set)

    def display_set(self, set_data=None):
        if set_data == None:
            set_data = self.controller.model.current_set

        # other variables
        self.current_card = 0
        self.current_side = False
        last_card = len(set_data) - 1
        subset_text = StringVar()

        # creating window items
        title = Label(self.window, text=self.controller.model.current_set_name, **self.title_kwargs)
        card_display = Button(self.window, bg=self.foreground, fg=self.background, font=self.subheading_font, text="No current card", wraplength=250, height=5, width=15)

        card_index = Label(self.window, **self.label_kwargs, text=f"Card 1 / {last_card + 1}")
        card_side = Label(self.window, **self.label_kwargs, text="Side: Front")
        subset = Entry(self.window, **self.entry_kwargs, textvariable=subset_text)

        subset_button = Button(self.window, **self.button_kwargs, text="Set Subset")
        next_button = Button(self.window, **self.button_kwargs, text="Next")
        prev_button = Button(self.window, **self.button_kwargs, text="Previous")
        flip_button = Button(self.window, **self.button_kwargs, text="Flip Cards")
        shuffle_button = Button(self.window, **self.button_kwargs, text="Shuffle")
        back_button = Button(self.window, **self.back_button_kwargs, text="Back")
        reset_button = Button(self.window, **self.reset_button_kwargs, text="Reset")

        # adding window items
        title.grid(row=0, column=0, columnspan=2, **self.widget_grid_kwargs)
        card_display.grid(row=1, column=0, columnspan=2, **self.widget_grid_kwargs)

        card_index.grid(row=2, column=0, sticky=E, **self.widget_padding)
        card_side.grid(row=2, column=1, sticky=W, **self.widget_padding)
        subset.grid(row=3, column=0, **self.widget_grid_kwargs)

        subset_button.grid(row=3, column=1, **self.widget_grid_kwargs)
        next_button.grid(row=4, column=1, **self.widget_grid_kwargs)
        prev_button.grid(row=4, column=0, **self.widget_grid_kwargs)
        flip_button.grid(row=5, column=0, **self.widget_grid_kwargs)
        shuffle_button.grid(row=5, column=1, **self.widget_grid_kwargs)
        back_button.grid(row=6, column=0, **self.widget_grid_kwargs)
        reset_button.grid(row=6, column=1, **self.widget_grid_kwargs)

        # button functions
        def update_card():
            
            # finding color
            background = None
            foreground = None
            side_name = None

            if self.current_side == False:
                background = self.card_front_color
                foreground = self.card_front_text
                side_name = "Side: Front"
            else:
                background = self.card_back_color
                foreground = self.card_back_text
                side_name = "Side: Back"

            # updating display
            card_info = set_data[self.current_card]
            card_display.config(text=card_info[self.current_side], bg=background, fg=foreground)
            card_side.config(text=side_name)
            card_index.config(text=f"Card {self.current_card + 1} / {len(set_data)}")

        update_card()

        def on_next_button():
            if self.current_card + 1 <= last_card:
                self.current_card += 1
            else:
                self.current_card = 0

            self.current_side = False
            update_card()

        def on_prev_button():
            if self.current_card - 1 >= 0:
                self.current_card -= 1
            else:
                self.current_card = last_card

            self.current_side = False
            update_card()

        def on_set_shuffle():
            shuffled_set = self.controller.model.shuffle_set(set_data)
            self.set_window("display_set", shuffled_set, history_disabled=True)

        def on_set_flip():
            flipped_set = self.controller.model.flip_set(set_data)
            self.set_window("display_set", flipped_set, history_disabled=True)

        def on_card_press():
            self.current_side = not self.current_side
            update_card()

        def on_subset_changed(var, index, mode):
            self.numeric_range_entry(subset_text, set_data)

        def on_subset_set():
            subset = self.controller.model.get_subset(subset_text)
            self.set_window("display_set", subset, history_disabled=True)

        # configuration
        subset_button.config(command=on_subset_set)
        next_button.config(command=on_next_button)
        prev_button.config(command=on_prev_button)
        shuffle_button.config(command=on_set_shuffle)
        card_display.config(command=on_card_press)
        flip_button.config(command=on_set_flip)

        subset_text.set(f"1-{len(set_data)}")
        subset_text.trace("w", on_subset_changed)

    def load_set(self, all_files, callback=None, *callback_args):

        # creating window items
        title = Label(self.window, text="Load from file", **self.title_kwargs)
        set_list = Listbox(self.window, **self.entry_kwargs, height=6)
        scrollbar = Scrollbar(self.window)

        edit_file = Button(self.window, **self.button_kwargs, text="Edit Selected")
        delete_file = Button(self.window, **self.button_kwargs, text="Delete Selected")
        load_file = Button(self.window, **self.green_button_kwargs, text="Load Selected")
        back_button = Button(self.window, **self.back_button_kwargs, text="Cancel")

        # adding window items
        title.grid(row=0, column=0, columnspan=2, **self.widget_grid_kwargs)
        set_list.grid(row=1, column=0, columnspan=2, **self.widget_grid_kwargs)
        scrollbar.grid(row=1, column=2, sticky=NSEW, pady=self.widget_pady)
        
        edit_file.grid(row=2, column=0, **self.widget_grid_kwargs)
        delete_file.grid(row=2, column=1, **self.widget_grid_kwargs)
        back_button.grid(row=3, column=0, **self.widget_grid_kwargs)
        load_file.grid(row=3, column=1, **self.widget_grid_kwargs)

        # adding files to list
        for file in all_files:
            set_list.insert(END, file.replace(".set", ""))

        # button functions
        def get_selected():
            selected = set_list.curselection()
            if len(selected) > 0 :
                return set_list.get(selected[0])

        def on_load_file():
            selected = get_selected()
            if selected != None:
                if callback == None:
                    self.controller.load_set(selected + ".set", self.set_window, "display_set")
                else:
                    self.controller.load_set(selected + ".set", callback, *callback_args)

        def on_edit_file():
            selected = get_selected()
            if selected != None:
                self.controller.model.load_set(selected + ".set")
                set_data = self.controller.model.current_set
                set_name = self.controller.model.current_set_name

                self.controller.prompt_new_set(set_data, set_name)

        def on_delete_file():
            selected = get_selected()
            self.controller.prompt_delete_set(selected + ".set")

        # configuration
        scrollbar.config(command=set_list.yview)
        set_list.config(yscrollcommand=scrollbar.set)
        load_file.config(command=on_load_file)
        edit_file.config(command=on_edit_file)
        delete_file.config(command=on_delete_file)

    def practice_menu(self):

        # variables
        set_data = self.controller.model.current_set
        set_name = self.controller.model.current_set_name
        current_range = StringVar()

        # creating window items
        title = Label(self.window, text="Practice Set", **self.title_kwargs)
        name_label = Label(self.window, text=set_name, **self.subtitle_kwargs)

        range_label = Label(self.window, **self.label_kwargs, text="Range:")
        range_entry = Entry(self.window, **self.entry_kwargs, textvariable=current_range)
        flipped_label = Label(self.window, **self.label_kwargs, text="Cards Flipped:")
        flip_button = Button(self.window, **self.red_button_kwargs, text="False")
        shuffle_label = Label(self.window, **self.label_kwargs, text="Shuffled:")
        shuffle_button = Button(self.window, **self.green_button_kwargs, text="True")

        spacer_label = Label(self.window, **self.spacer_kwargs)
        reset_button = Button(self.window, **self.reset_button_kwargs, text="Reset")
        back_button = Button(self.window, **self.back_button_kwargs, text="Back")
        start_button = Button(self.window, **self.green_button_kwargs, text="Start")

        # gridding window items
        title.grid(row=0, column=0, columnspan=2, **self.widget_grid_kwargs)
        name_label.grid(row=1, column=0, columnspan=2, **self.widget_grid_kwargs)

        range_label.grid(row=2, column=0, **self.widget_grid_kwargs)
        range_entry.grid(row=2, column=1, **self.widget_grid_kwargs)
        flipped_label.grid(row=3, column=0, **self.widget_grid_kwargs)
        flip_button.grid(row=3, column=1, **self.widget_grid_kwargs)
        shuffle_label.grid(row=4, column=0, **self.widget_grid_kwargs)
        shuffle_button.grid(row=4, column=1, **self.widget_grid_kwargs)

        spacer_label.grid(row=5, column=0, columnspan=2, **self.widget_grid_kwargs)
        reset_button.grid(row=6, column=1, **self.widget_grid_kwargs)
        back_button.grid(row=7, column=0, **self.widget_grid_kwargs)
        start_button.grid(row=7, column=1, **self.widget_grid_kwargs)

        # button functions
        def on_range_changed(var, index, mode):
            self.numeric_range_entry(current_range, set_data)

        def on_flip_button():
            self.boolean_button_toggle(flip_button)

        def on_shuffle_button():
            self.boolean_button_toggle(shuffle_button)

        def on_start_button():
            
            # finding first and second indices
            subset_split = current_range.get().split("-")
            first_index, second_index = None, None
            if len(subset_split) >= 2:
                first_index = int(subset_split[0])
                second_index = int(subset_split[1])
            else:
                first_index = 0
                second_index = len(set_data)

            # variables
            subset = (first_index - 1, second_index)
            to_flip = flip_button.cget("text") == "True"
            to_shuffle = shuffle_button.cget("text") == "True"

            # starting quiz
            self.controller.start_quiz(subset, to_flip, to_shuffle)
        
        # configuration
        current_range.set(f"1-{len(set_data)}")
        current_range.trace("w", on_range_changed)

        flip_button.config(command=on_flip_button)
        shuffle_button.config(command=on_shuffle_button)
        start_button.config(command=on_start_button)

    def practice_quiz(self, quiz_data):

        # variables
        set_name = self.controller.model.current_set_name
        current_question = 1
        last_question = len(quiz_data)
        current_answer = StringVar()
        
        # creating window items
        title = Label(self.window, text=f"Quiz: {set_name}", **self.title_kwargs)
        question_number = Label(self.window, **self.label_kwargs, text=f"Question {current_question}/{last_question}")

        question_label = Label(self.window, **self.subtitle_kwargs, text="None", wraplength=250)
        answer_label = Label(self.window, **self.label_kwargs, text="Answer:")
        answer_entry = Entry(self.window, **self.entry_kwargs, textvariable=current_answer)
        submit_button = Button(self.window, text="Submit", **self.green_button_kwargs)

        prev_button = Button(self.window, **self.button_kwargs, text="Previous")
        next_button = Button(self.window, **self.button_kwargs, text="Next")
        back_button = Button(self.window, **self.back_button_kwargs, text="Back")

        # positioning window items
        title.grid(row=0, column=0, columnspan=2, **self.widget_grid_kwargs)
        question_number.grid(row=1, column=0, columnspan=2, **self.widget_grid_kwargs)

        question_label.grid(row=2, column=0, columnspan=2, **self.widget_grid_kwargs)
        answer_label.grid(row=3, column=0, columnspan=2, **self.widget_grid_kwargs)
        answer_entry.grid(row=4, column=0, columnspan=2, **self.widget_grid_kwargs)
        submit_button.grid(row=5, column=0, columnspan=2, **self.widget_grid_kwargs)

        prev_button.grid(row=6, column=0, **self.widget_grid_kwargs)
        next_button.grid(row=6, column=1, **self.widget_grid_kwargs)
        back_button.grid(row=7, column=0, **self.widget_grid_kwargs)

        # TODO - set up quiz

    def are_you_sure(self, prompt, yes_callback, no_callback):

        # creating window items
        title = Label(self.window, text="Are you sure?", **self.title_kwargs)
        message = Label(self.window, text=prompt, **self.subtitle_kwargs)

        yes_button = Button(self.window, **self.green_button_kwargs, text="Yes", command=yes_callback)
        no_button = Button(self.window, **self.red_button_kwargs, text="No", command=no_callback)
        warning = Label(self.window, **self.error_kwargs, text="You cannot undo this action.")

        # placing window items
        title.grid(row=0, column=0, columnspan=2, **self.widget_grid_kwargs)
        message.grid(row=1, column=0, columnspan=2, **self.widget_grid_kwargs)

        yes_button.grid(row=2, column=0, **self.widget_grid_kwargs)
        no_button.grid(row=2, column=1, **self.widget_grid_kwargs)
        warning.grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=self.widget_pady, pady=self.widget_pady)

    def update(self):
        self.window.update()
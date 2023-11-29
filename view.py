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

    def create_error(self, message="An error ocurred", error_time=2):

        # destroying previous error
        if self.error_label != None:
            self.clear_error()

        # creating and packing error
        self.error_label = Label(self.window, bg=self.background, fg=self.error, text=message, font=self.normal_font, justify=CENTER)
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
            button.config(text="False", bg="red")
        else:
            button.config(text="True", bg="green")

    def main_menu(self):

        # creating window items
        title = Label(self.window, bg=self.background, fg=self.foreground, text="Flash Card Maker", font=self.heading_font)
        create_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Create New Set", font=self.subheading_font, command=self.controller.prompt_new_set)
        open_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Load Previous Set", font=self.subheading_font, command=self.controller.prompt_load_set)
        practice_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Practice Set", font=self.subheading_font, command=self.controller.prompt_practice)

        # adding window items
        title.grid(row=0, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        create_button.grid(row=1, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        open_button.grid(row=2, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        practice_button.grid(row=3, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

    def new_set_prompt(self, set_data=None, name=None):

        # creating window items
        title = Label(self.window, bg=self.background, fg=self.foreground, text="Create New Card Set", font=self.heading_font)
        set_name_title = Label(self.window, bg=self.background, fg=self.foreground, text="Set Name", font=self.normal_font)
        set_name = Entry(self.window, bg=self.middleground, fg=self.foreground, font=self.normal_font)

        card_list = Listbox(self.window, bg=self.middleground, fg=self.foreground, font=self.normal_font, height=6)
        scrollbar = Scrollbar(self.window)

        card_key_title = Label(self.window, bg=self.background, fg=self.foreground, text="Term", font=self.normal_font)
        card_key = Entry(self.window, bg=self.middleground, fg=self.foreground, font=self.normal_font)
        card_value_title = Label(self.window, bg=self.background, fg=self.foreground, text="Definition", font=self.normal_font)
        card_value = Entry(self.window, bg=self.middleground, fg=self.foreground, font=self.normal_font)

        delete_buton = Button(self.window, bg=self.middleground, fg=self.foreground, text="Delete Card", font=self.normal_font)
        new_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Create Card", font=self.normal_font)
        cancel_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Cancel", font=self.normal_font, command=self.back_button)
        confirm_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Confirm", font=self.normal_font)

        # adding window items
        title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        set_name_title.grid(row=1, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        set_name.grid(row=1, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        card_list.grid(row=2, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        scrollbar.grid(row=2, column=2, sticky=NSEW, pady=self.widget_pady)

        card_key_title.grid(row=3, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        card_key.grid(row=3, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        card_value_title.grid(row=4, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        card_value.grid(row=4, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

        delete_buton.grid(row=5, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        new_button.grid(row=5, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        cancel_button.grid(row=6, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        confirm_button.grid(row=6, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

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
        title = Label(self.window, bg=self.background, fg=self.foreground, text=self.controller.model.current_set_name, font=self.heading_font)
        card_display = Button(self.window, bg=self.foreground, fg=self.background, text="No current card", wraplength=250, font=self.subheading_font, height=5, width=15)

        card_index = Label(self.window, bg=self.background, fg=self.foreground, text=f"Card 1 / {last_card + 1}", font=self.normal_font)
        card_side = Label(self.window, bg=self.background, fg=self.foreground, text="Side: Front", font=self.normal_font)
        subset = Entry(self.window, bg=self.middleground, fg=self.foreground, font=self.normal_font, textvariable=subset_text, width=10)

        subset_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Set Subset", font=self.normal_font, width=10)
        next_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Next", font=self.normal_font, width=10)
        prev_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Previous", font=self.normal_font, width=10)
        flip_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Flip Cards", font=self.normal_font, width=10)
        shuffle_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Shuffle", font=self.normal_font, width=10)
        back_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Back", font=self.normal_font, command=self.back_button)
        reset_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Reset", font=self.normal_font)

        # adding window items
        title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        card_display.grid(row=1, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

        card_index.grid(row=2, column=0, sticky=E, padx=self.widget_padx, pady=self.widget_pady)
        card_side.grid(row=2, column=1, sticky=W, padx=self.widget_padx, pady=self.widget_pady)
        subset.grid(row=3, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

        subset_button.grid(row=3, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        next_button.grid(row=4, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        prev_button.grid(row=4, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        flip_button.grid(row=5, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        shuffle_button.grid(row=5, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        back_button.grid(row=6, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        reset_button.grid(row=6, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

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

        def on_reset():
            self.set_window("display_set", history_disabled=True)

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
        reset_button.config(command=on_reset)

        subset_text.set(f"1-{len(set_data)}")
        subset_text.trace("w", on_subset_changed)

    def load_set(self, all_files, callback=None, *callback_args):

        # creating window items
        title = Label(self.window, bg=self.background, fg=self.foreground, text="Load from file", font=self.heading_font)
        set_list = Listbox(self.window, bg=self.middleground, fg=self.foreground, font=self.normal_font, height=6)
        scrollbar = Scrollbar(self.window)

        load_file = Button(self.window, bg=self.middleground, fg=self.foreground, text="Load Selected", font=self.normal_font, width=15)
        edit_file = Button(self.window, bg=self.middleground, fg=self.foreground, text="Edit Selected", font=self.normal_font, width=15)
        delete_file = Button(self.window, bg=self.middleground, fg=self.foreground, text="Delete Selected", font=self.normal_font, width=15)
        back_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Cancel", font=self.normal_font, width=15, command=self.back_button)

        # adding window items
        title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        set_list.grid(row=1, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        scrollbar.grid(row=1, column=2, sticky=NSEW, pady=self.widget_pady)
        
        edit_file.grid(row=2, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        load_file.grid(row=2, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        back_button.grid(row=3, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        delete_file.grid(row=3, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

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
        title = Label(self.window, bg=self.background, fg=self.foreground, text="Practice Set", font=self.heading_font)
        name_label = Label(self.window, bg=self.background, fg=self.foreground, text=set_name, font=self.subheading_font)

        range_label = Label(self.window, bg=self.background, fg=self.foreground, text="Range:", font=self.normal_font)
        range_entry = Entry(self.window, bg=self.middleground, fg=self.foreground, textvariable=current_range, font=self.normal_font, width=10)
        flipped_label = Label(self.window, bg=self.background, fg=self.foreground, text="Cards Flipped:", font=self.normal_font)
        flip_button = Button(self.window, bg="red", fg=self.foreground, text="False", font=self.normal_font)
        shuffle_label = Label(self.window, bg=self.background, fg=self.foreground, text="Shuffled:", font=self.normal_font)
        shuffle_button = Button(self.window, bg="green", fg=self.foreground, text="True", font=self.normal_font)

        reset_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Reset", font=self.normal_font)
        back_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Back", font=self.normal_font, command=self.back_button)

        # gridding window items
        title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        name_label.grid(row=1, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

        range_label.grid(row=2, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        range_entry.grid(row=2, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        flipped_label.grid(row=3, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        flip_button.grid(row=3, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        shuffle_label.grid(row=4, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        shuffle_button.grid(row=4, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

        back_button.grid(row=5, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        reset_button.grid(row=5, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

        # button functions
        def on_range_changed(var, index, mode):
            self.numeric_range_entry(current_range, set_data)

        def on_flip_button():
            self.boolean_button_toggle(flip_button)

        def on_shuffle_button():
            self.boolean_button_toggle(shuffle_button)

        def on_reset_button():
            self.set_window("practice_menu")

        # configuration
        current_range.set(f"1-{len(set_data)}")
        current_range.trace("w", on_range_changed)

        flip_button.config(command=on_flip_button)
        shuffle_button.config(command=on_shuffle_button)
        reset_button.config(command=on_reset_button)

    def are_you_sure(self, prompt, yes_callback, no_callback):

        # creating window items
        title = Label(self.window, bg=self.background, fg=self.foreground, text="Are you sure?", font=self.heading_font)
        message = Label(self.window, bg=self.background, fg=self.foreground, text=prompt, font=self.subheading_font)

        yes_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Yes", font=self.normal_font, width=15, command=yes_callback)
        no_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="No", font=self.normal_font, width=15, command=no_callback)
        warning = Label(self.window, bg=self.background, fg=self.foreground, text="You cannot undo this action.", font=self.normal_font)

        # placing window items
        title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        message.grid(row=1, column=0, columnspan=2, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

        yes_button.grid(row=2, column=0, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        no_button.grid(row=2, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        warning.grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=self.widget_pady, pady=self.widget_pady)

    def update(self):
        self.window.update()
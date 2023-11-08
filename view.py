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

        # opening main menu
        self.set_window("main_menu")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def set_window(self, to_set):
        self.clear_window()
        self.window.configure(background=self.background, padx=self.window_padx, pady=self.window_pady)
        getattr(self, to_set)()

    def back_button(self):
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

    def main_menu(self):

        # creating window items
        title = Label(self.window, bg=self.background, fg=self.foreground, text="Flash Card Maker", font=self.heading_font)
        create_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Create New Set", font=self.subheading_font, command=self.controller.prompt_new_set)
        open_button = Button(self.window, bg=self.middleground, fg=self.foreground, text="Load Previous Set", font=self.subheading_font)

        # adding window items
        title.grid(row=0, column=1, columnspan=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        create_button.grid(row=1, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)
        open_button.grid(row=2, column=1, sticky=NSEW, padx=self.widget_padx, pady=self.widget_pady)

    def new_set_prompt(self):

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
            self.controller.create_new_set(set_data)
            self.back_button()

        # configuration
        scrollbar.config(command=card_list.yview)
        card_list.config(yscrollcommand=scrollbar.set)
        new_button.config(command=create_new_card)
        delete_buton.config(command=delete_card)
        confirm_button.config(command=confirm_set)

    def update(self):
        self.window.update()
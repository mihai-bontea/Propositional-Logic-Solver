import customtkinter
from functools import partial

class KeyboardButton(customtkinter.CTkButton):
    def __init__(self, master, textbox, char):
        kb_font = customtkinter.CTkFont(size=20, weight="bold", family="Times")
        kb_size = 40
        super().__init__(master=master,
                         text=char,
                         width=kb_size,
                         height=kb_size,
                         font=kb_font,
                         command=partial(KeyboardButton.insert_char_into_textbox, textbox, char))

    @staticmethod
    def insert_char_into_textbox(textbox, char):
        cursor_position = textbox.index(customtkinter.INSERT)
        textbox.insert(cursor_position, char)
    
    def grid(self, row, column, padx, pady, sticky="n"):
        super().grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
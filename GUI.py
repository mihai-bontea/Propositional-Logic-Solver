import tkinter.messagebox
import customtkinter
import pyperclip

from tkinter import filedialog
from functools import partial
from Controller import Controller

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

KB_W = 40

class GraphicalUserInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.configure_window()
        self.create_sidebar()

        self.create_tabview()
        self.set_conversion_tab()
        self.set_decoding_tab()
        self.set_default_values()
    
    def configure_window(self):
        self.title("Propositional Logic Solver")
        self.geometry(f"{900}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_tabview(self):
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, rowspan=3, padx=(0, 0), pady=(10, 0), sticky="nsew")
        self.tabview.add("Conversion")
        self.tabview.add("Interpret")
        self.tabview.add("Resolution")
        self.tabview.tab("Conversion").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Interpret").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Resolution").grid_columnconfigure(0, weight=1)

    def create_sidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="Propositional Logic\nSolver", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
    
    def set_conversion_tab(self):
        self.conversion_options_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Conversion"),
                                                        values=["NNF", "CNF", "DNF"])
        self.conversion_options_menu.grid(row=0, column=0, padx=(0, 250), pady=(10, 10))

        # self.checkbox = customtkinter.CTkCheckBox(self.tabview.tab("Conversion"), text="Use Encryption")
        # self.checkbox.grid(row = 0, column = 0, padx=(250, 0), pady=(10, 10))

        # self.encoding_file_selection_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="Select a file",
                                                                    #   command=self.encoding_upload_action)
        # self.encoding_file_selection_button.grid(row=1, column=0, padx=(0, 250), pady=(10, 10))

        self.conv_textbox = customtkinter.CTkTextbox(self.tabview.tab("Conversion"), width=700, height=100)
        self.conv_textbox.grid(row=1, column=0, padx=(150, 150), pady=(20, 10), sticky="n")

        kb_font=customtkinter.CTkFont(size=20, weight="bold")

        # Make this into a class

        self.conj_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="∧", width=KB_W, height=KB_W, font=kb_font,
                                                   command=partial(self.insert_char_into_textbox, self.conv_textbox, "∧"))
        self.conj_button.grid(row=2, column=0, padx=(0, 50), pady=(0, 0), sticky="n")

        self.disj_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="∨", width=KB_W, height=KB_W, font=kb_font,
                                                   command=partial(self.insert_char_into_textbox, self.conv_textbox, "∨"))
        self.disj_button.grid(row=2, column=0, padx=(100, 50), pady=(0, 0), sticky="n")

        self.impl_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="→", width=KB_W, height=KB_W, font=kb_font,
                                                   command=partial(self.insert_char_into_textbox, self.conv_textbox, "→"))
        self.impl_button.grid(row=2, column=0, padx=(200, 50), pady=(0, 0), sticky="n")

        self.equiv_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="↔", width=KB_W, height=KB_W, font=kb_font,
                                                    command=partial(self.insert_char_into_textbox, self.conv_textbox, "↔"))
        self.equiv_button.grid(row=2, column=0, padx=(300, 50), pady=(0, 0), sticky="n")

        self.neg_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="¬", width=KB_W, height=KB_W, font=kb_font,
                                                  command=partial(self.insert_char_into_textbox, self.conv_textbox, "¬"))
        self.neg_button.grid(row=2, column=0, padx=(400, 50), pady=(0, 0), sticky="n")

        self.top_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="⊤", width=KB_W, height=KB_W, font=kb_font,
                                                  command=partial(self.insert_char_into_textbox, self.conv_textbox, "⊤"))
        self.top_button.grid(row=2, column=0, padx=(500, 50), pady=(0, 0), sticky="n")

        self.bot_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="⊥", width=KB_W, height=KB_W, font=kb_font,
                                                  command=partial(self.insert_char_into_textbox, self.conv_textbox, "⊥"))
        self.bot_button.grid(row=2, column=0, padx=(600, 50), pady=(0, 0), sticky="n")

        self.convert_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="Conversion",
                                                             command=partial(self.attempt_encode, self.conv_textbox))
        self.convert_button.grid(row=0, column=0, padx=(250, 0), pady=(10, 10))

        self.copy_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="Download to PDF",
                                                   command=self.copy_to_clipboard_action)
        self.copy_button.grid(row=3, column=0, padx=(0, 0), pady=(10, 10))

        self.encode_result = customtkinter.CTkLabel(
            self.tabview.tab("Conversion"), text="", font=customtkinter.CTkFont(size=12))

    def set_decoding_tab(self):
        self.decoding_lsb_option_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Interpret"),
                                                        values=["1", "2", "3", "4", "5", "6", "7", "8"])
        self.decoding_lsb_option_menu.grid(row=0, column=0, padx=(0, 250), pady=(10, 10))

        self.decoding_file_selection_button = customtkinter.CTkButton(self.tabview.tab("Interpret"), text="Select a file",
                                                                      command=self.decoding_upload_action)
        self.decoding_file_selection_button.grid(row=1, column=0, padx=(0, 250), pady=(10, 10))

        self.decode_button = customtkinter.CTkButton(self.tabview.tab("Interpret"), text="Interpret",
                                                             command=self.attempt_decode)
        self.decode_button.grid(row=2, column=0, padx=(0, 250), pady=(10, 10))

        self.mask_label = customtkinter.CTkLabel(self.tabview.tab("Interpret"), text="🔑 Encryption key:", anchor="w")
        self.mask_label.grid(row=0, column=0, padx=(250, 0), pady=(10, 0))

        self.mask_frame = customtkinter.CTkFrame(self.tabview.tab("Interpret"), width=140, height=30)
        self.mask_frame.grid(row=1, column=0, padx=(250, 0), pady=(10, 10))
        self.decoding_mask = tkinter.StringVar()
        self.mask_entry = customtkinter.CTkEntry(self.mask_frame, textvariable=self.decoding_mask)
        self.mask_entry.grid(row=1, column=0, padx=(0, 0), pady=(0,0), sticky="we")

        self.decode_result = customtkinter.CTkLabel(
            self.tabview.tab("Interpret"), text="", font=customtkinter.CTkFont(size=12))        
        self.decode_secret_message = customtkinter.CTkTextbox(self.tabview.tab("Interpret"), width=10)

    def set_default_values(self):
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.conversion_options_menu.set("Conversion type")
        self.decoding_lsb_option_menu.set("LSBs used")
        self.convert_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.decode_button.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def encoding_upload_action(self,event=None):
        self.encoding_filename = filedialog.askopenfilename()
        self.convert_button.configure(state="normal")
        self.copy_button.configure(state="disabled")
    
    def decoding_upload_action(self):
        self.decoding_filename = filedialog.askopenfilename()
        self.decode_button.configure(state="normal")
    
    def select_output_path(self, extension):
        return filedialog.asksaveasfilename(defaultextension=extension) 
    
    def copy_to_clipboard_action(self):
        pyperclip.copy(str(self.mask))
    
    def attempt_encode(self):
        pass

    def attempt_decode(self):
        pass

    def insert_char_into_textbox(self, textbox, char):
        textbox.insert("end", char)


if __name__ == "__main__":
    gui = GraphicalUserInterface()
    gui.mainloop()
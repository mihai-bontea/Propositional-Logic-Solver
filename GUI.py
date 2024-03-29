import customtkinter

from tkinter import filedialog
from functools import partial
from Controller import Controller, ConversionType, ResolutionType
from KeyboardButton import KeyboardButton
from ExpressionTreeRelated.LogicOperators import *
from ResolutionMethod.ResolutionResultInfo import *

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GraphicalUserInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.configure_window()
        self.create_sidebar()

        self.create_tabview()
        self.set_conversion_tab()
        self.set_resolution_tab()
        self.set_default_values()
    
    def configure_window(self):
        self.title("Propositional Logic Solver")
        self.geometry(f"{900}x{580}")

        # configure grid layout (4x3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_tabview(self):
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, rowspan=3, padx=(0, 0), pady=(10, 0), sticky="nsew")
        self.tabview.add("Conversion")
        self.tabview.add("Resolution")
        self.tabview.tab("Conversion").grid_columnconfigure(0, weight=1)
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

        textbox_font = customtkinter.CTkFont(size=20, family="Times")
        self.conv_textbox = customtkinter.CTkTextbox(self.tabview.tab("Conversion"), width=700, height=300, font=textbox_font)
        self.conv_textbox.grid(row=1, column=0, padx=(80, 80), pady=(20, 10), sticky="n")

        self.conj_button = KeyboardButton(self.tabview.tab("Conversion"), self.conv_textbox, CONJ)
        self.conj_button.grid(row=2, column=0, padx=(0, 200), pady=(0, 10))

        self.disj_button = KeyboardButton(self.tabview.tab("Conversion"), self.conv_textbox, DISJ)
        self.disj_button.grid(row=2, column=0, padx=(100, 200), pady=(0, 10))

        self.impl_button = KeyboardButton(self.tabview.tab("Conversion"), self.conv_textbox, IMPL)
        self.impl_button.grid(row=2, column=0, padx=(200, 200), pady=(0, 10))

        self.equiv_button = KeyboardButton(self.tabview.tab("Conversion"), self.conv_textbox, EQUIV)
        self.equiv_button.grid(row=2, column=0, padx=(300, 200), pady=(0, 10))

        self.neg_button = KeyboardButton(self.tabview.tab("Conversion"), self.conv_textbox, NEG)
        self.neg_button.grid(row=2, column=0, padx=(400, 200), pady=(0, 10))

        self.top_button = KeyboardButton(self.tabview.tab("Conversion"), self.conv_textbox, TOP)
        self.top_button.grid(row=3, column=0, padx=(150, 200), pady=(0, 10))

        self.bot_button = KeyboardButton(self.tabview.tab("Conversion"), self.conv_textbox, BOT)
        self.bot_button.grid(row=3, column=0, padx=(250, 200), pady=(0, 10))

        self.convert_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="Convert",
                                                             command=self.attempt_convert)
        self.convert_button.grid(row=0, column=0, padx=(250, 0), pady=(10, 10))

        self.conv_copy_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="Download to PDF",
                                                   command=lambda: None)
        self.conv_copy_button.grid(row=4, column=0, padx=(0, 250), pady=(10, 10))

        self.conv_clear_button = customtkinter.CTkButton(self.tabview.tab("Conversion"), text="Clear", 
                                                         command=partial(self.clear_textbox, self.conv_textbox))
        self.conv_clear_button.grid(row=4, column=0, padx=(250, 0), pady=(10, 10))
        
    def set_resolution_tab(self):
        self.resolution_options_menu = customtkinter.CTkOptionMenu(self.tabview.tab("Resolution"),
                                                        values=["Resolution", "DP", "DPLL"])
        self.resolution_options_menu.grid(row=0, column=0, padx=(0, 250), pady=(10, 10))

        textbox_font = customtkinter.CTkFont(size=20, family="Times")
        self.res_textbox = customtkinter.CTkTextbox(self.tabview.tab("Resolution"), width=700, height=300, font=textbox_font)
        self.res_textbox.grid(row=1, column=0, padx=(80, 80), pady=(20, 10), sticky="n")

        self.apply_button = customtkinter.CTkButton(self.tabview.tab("Resolution"), text="Apply",
                                                             command=self.attempt_resolution)
        self.apply_button.grid(row=0, column=0, padx=(250, 0), pady=(10, 10))

        self.res_copy_button = customtkinter.CTkButton(self.tabview.tab("Resolution"), text="Download to PDF",
                                                   command=lambda: None)
        self.res_copy_button.grid(row=4, column=0, padx=(0, 250), pady=(10, 10))

        self.res_clear_button = customtkinter.CTkButton(self.tabview.tab("Resolution"), text="Clear", 
                                                         command=partial(self.clear_textbox, self.res_textbox))
        self.res_clear_button.grid(row=4, column=0, padx=(250, 0), pady=(10, 10))

    def set_default_values(self):
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.conversion_options_menu.set("Conversion type")
        self.resolution_options_menu.set("Resolution type")
        self.conv_copy_button.configure(state="disabled")
        self.res_copy_button.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def select_output_path(self, extension):
        return filedialog.asksaveasfilename(defaultextension=extension) 
    
    def clear_textbox(self, textbox):
        textbox.delete("0.0", "end")

    def get_conv_option(self):
        conversion_type_str = self.conversion_options_menu.get()
        conversion_type = ConversionType.__members__.get(conversion_type_str)
        return ConversionType.NNF if conversion_type == None else conversion_type
    
    def get_res_option(self):
        resolution_type_str = self.resolution_options_menu.get()
        resolution_type = ResolutionType.__members__.get(resolution_type_str)
        return ResolutionType.RES if resolution_type == None else resolution_type

    def attempt_convert(self):
        self.conv_textbox.tag_config("green_color", foreground="green")
        self.conv_textbox.tag_config("red_color", foreground="red")

        textbox_contents_no_space = self.conv_textbox.get(1.0, "end-1c").replace(" ", "")
        result = self.controller.convert_to_normal_forms(textbox_contents_no_space,
                                                         self.get_conv_option())
        self.conv_textbox.insert("end", '\n')

        if isinstance(result, Exception):
            self.conv_textbox.insert("end", str(result) + '\n', "red_color")

        else:
            for prop in result:
                desc, actual = prop.split('\n')
                self.conv_textbox.insert("end", desc + '\n', "green_color")
                self.conv_textbox.insert("end", actual + '\n')

    def attempt_resolution(self):
        self.res_textbox.tag_config("green_color", foreground="green")
        self.res_textbox.tag_config("red_color", foreground="red")
        self.res_textbox.tag_config("cyan_color", foreground="cyan")
        self.res_textbox.tag_config("underline", underline=True)

        enum_to_tag = {LineEffect.GREEN: "green_color",
                       LineEffect.RED: "red_color",
                       LineEffect.CYAN: "cyan_color",
                       LineEffect.UNDERLINED: "underline"}

        result = self.controller.is_proposition_satisfiable(self.res_textbox.get(1.0, "end-1c"), 
                                                            self.get_res_option())
        self.res_textbox.insert("end", '\n')
        
        if isinstance(result, Exception):
            self.res_textbox.insert("end", str(result) + '\n', "red_color")
        
        else:
            for step in result.steps:
               self.res_textbox.insert("end", step[0] + '\n', enum_to_tag[step[1]]) 


if __name__ == "__main__":
    gui = GraphicalUserInterface()
    gui.mainloop()
#!/usr/bin/python3
"""
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL

    Dummy demonstrator for the Classic Mac inspired
    ttk theme "Koollooks" by Dogcow (moof-moof) 2026.
    
    The demo script itself is based on 
    "ttk-example.py" by RedFantom 2018.
    License: GNU GPLv3
    
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
"""

import KL_wrappers as kl
import tkinter as tk
import os
import time
from tkinter import ttk
from tkinter import Tk
from tkinter import font
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk, ImageDraw
from itertools import count

# Version number
vnum ='v2.10'

# WIDTH, HEIGHT = 500, 700

# Chicago font "bicolours"
chi_fg = chi_act_bg = '#000000'
chi_bg = chi_act_fg = '#ffffff'

# Cursor images
arrow_16       = "gumby"
mac_mickey_16  = "mouse"
sizegripper_16 = "gobbler"
i_beam_16      = "bogosity"

theme = "koollooks"


def main():
    app = Example()
    app.set_theme(theme)
    app.mainloop()



class Example(ThemedTk):
    

    def __init__(self):#, theme="koollooks"):
        
        ThemedTk.__init__(self, fonts=True, themebg=True)
#         self.set_theme(theme)
        self.title('Finder Demo '+ vnum)
#         self.minsize(350, 425) 
#         self.maxsize(400, 600)
        self.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use(theme)
        self.configure(cursor=arrow_16)
        
    # Some global customizations
        self.style.map("TButton", foreground=[('pressed', chi_bg)])
        self.buttonFont = ('Chicago Kare', 12)
        self.monofont = ('monaco-12-(accurate)', 12)
        self.tk_strictMotif=0
        
        self.img_indicator = tk.PhotoImage(file=os.path.expanduser( \
                            "~/koollooks_alias/sub-menu-indicator-sn.gif")) 

    # Let's turn off every kind of focus-indication already!
        self.style.configure("TNotebook.Tab", focuscolor="chi_bg")
        self.option_add('*TNotebook*takeFocus',    0)
        self.option_add('*TButton*takeFocus',      0)
        self.option_add('*TRadiobutton*takeFocus', 0)
        self.option_add('*TCheckbutton*takeFocus', 0)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)



#                      Create widgets:
#  *************************************************************#
                                                                #
                                                                #
#[kl] "Slate"
        kl.KL_setup_slate(self, 350, 475)
        
#+++# Menubar
        self.setup_menubar()
        
#[kl] Notebook
        self.notebook = kl.KL_notebook(self, 150, 100, 5)
        
    # Let's add some (1-bit) images to the Notebook! 
   
    #   (1) Create a frame within the notebook window
        f1 = tk.Frame(self, background="#FFF")
        
    #   (2) Load the image using PIL
        image_f11 = "./assets/dogcow48x48.png"
        image_f12 = "./assets/py-gitter2.png"
        image_f13 = "./assets/resEdit-x2.png"
        
        image11 = Image.open(image_f11)
        image12 = Image.open(image_f12)
        image13 = Image.open(image_f13)
        
        img_f11 = ImageTk.PhotoImage(image11)
        img_f12 = ImageTk.PhotoImage(image12)
        img_f13 = ImageTk.PhotoImage(image13)

    #   (3) Create a Canvas widget and add the images to it
        _canv = tk.Canvas(f1, width=150, height=120, background="#fff")
        _canv.pack(fill="both", expand=True)

        _canv.create_image( 20, 45, anchor=tk.NW, image=img_f11)
        _canv.create_image( 85, 40, anchor=tk.NW, image=img_f12)
        _canv.create_image( 155,27, anchor=tk.NW, image=img_f13)
        
    #   (4) Keep a reference to avoid garbage collection:
        img_f11.image = img_f11
        img_f12.image = img_f12
        img_f13.image = img_f13
        
        self.notebook.add(f1, text="Tabby")

#[kl] Populating a second frame we call a wrapper function instead:
        f2 = tk.Frame(self, background="#fff")
        kl.KL_image_on_canvas(f2, 
                    "./assets/tubby_1bit.png", 165, 40, 150, 130)

        self.notebook.add(f2, text="Tubby")

#[kl] For the third frame we demo an animated gif label
        f3 = tk.Frame(self, background="#fff") 
        img_lbl = kl.KL_AnimLabel(f3, background="#fff")
        img_lbl.delay_last = 3000
        img_lbl.delay_rest = 500
        img_lbl.pack()
        img_lbl.load("./assets/fubby.gif")

        self.notebook.add(f3, text="Fubby")

#+++# Labels        
        self.labelvers = ttk.Label(self, text='['+ vnum + ']    ')

#+++# Label as a margin spacer  
        self.spaceXY = ttk.Label(self, width=1, background=chi_bg)
         
#[kl] Options menu        
        self.dropdown = kl.KL_optionsmenu(self, 
                                        tk.StringVar(),
                                        " Pick..", 
                                        " Val A ", 
                                        " Val B ",
                                        " Val C ")
#[kl] TextEntry box
        self.txt_entry = kl.KL_entry(self, " Default entry value...")  

#[kl] Button(Fancy)
        self.button1 = kl.fancy_butt(self,"OK", 5, False) 
    
#[kl] Button(Plain)
        self.button2 = kl.plain_butt(self, "Cancel", 6, False, 5)

#+++# Radio group dummies
        self.v = tk.StringVar(self, "1")
        self.radio_one = ttk.Radiobutton(self, 
                                        text="Radio 1", 
                                        variable = self.v, 
                                        value=1, 
                                        cursor=mac_mickey_16)                               
        self.radio_two = ttk.Radiobutton(self, 
                                        text="Radio 2", 
                                        variable = self.v, 
                                        value=2, 
                                        cursor=mac_mickey_16)
#[kl] Check button dummies
        self.checked = kl.KL_checkbutton(self, 
                                        "Checked", 
                                        True)

        self.unchecked = kl.KL_checkbutton(self, 
                                        "Unchecked", 
                                        False)

#[kl] Listbox
        self.listbox = kl.KL_listbox(self, 3, 9)
        self.listbox.insert(tk.END, *(f" #{i}" for i in range(100)))

#+++# Scrollbar
        self.scrollv = ttk.Scrollbar(self, 
                                        orient=tk.VERTICAL, 
                                        command=self.listbox.yview, 
                                        cursor=mac_mickey_16)
                                        
        self.style.configure("Vertical.TScrollbar", arrowsize=40)

        # Configure bilateral association of listbox and scrollbar:
        self.listbox['yscrollcommand'] = self.scrollv.set
        # A similar, alternative statement:
        # self.scrollv.config(command = self.listbox.yview)

#+++# Treeview
        self.tree = ttk.Treeview(self, 
                                height=5, 
                                show=("tree", "headings"), 
                                cursor=mac_mickey_16)
        self.setup_tree()
    
#+++# ScaleEntry
        self.scale = ScaleEntry(self, 
                                from_= 0, 
                                to = 50, 
                                orient = tk.HORIZONTAL, 
                                compound = tk.RIGHT, 
                                cursor = mac_mickey_16)
#+++# Combobox
        self.style.configure('TCombobox', background=chi_bg, foreground=chi_fg)   # Superfluous?
        self.combo = AutocompleteCombobox(self, 
                                        cursor=arrow_16, 
                                        completevalues=["something", "nothing", "Tralalah"])
        self.option_add("*TCombobox*Listbox*Background", chi_bg)
        self.option_add("*TCombobox*Listbox*Foreground", chi_fg)
        self.option_add("*TCombobox*Listbox*cursor", i_beam_16)

#+++# Radio group for progress bar
        self.v = tk.StringVar(self, "1")
        
        self.r1 = ttk.Radiobutton(self, 
                                    text="Start", 
                                    variable = self.v, 
                                    value=2,
                                    command = lambda: self.progress.start(75),
                                    cursor=mac_mickey_16)                               
        self.r2 = ttk.Radiobutton(self, 
                                    text="Stop!", 
                                    variable = self.v, 
                                    value=1,
                                    command = lambda: self.stop_all_progress(),
                                    cursor=mac_mickey_16)
#+++# Progress bar
        self.progress = ttk.Progressbar(self, 
                                        mode = 'determinate', 
                                        maximum = 100, 
                                        value = 70)
#+++# Sizegrip
        self.grip = ttk.Sizegrip(self, cursor=sizegripper_16)
   
#+++# Separator (horisontal):
        self.separat_h = ttk.Separator()


    # Grid widgets
        self.grid_widgets()

                                                                #
#                    [End create widgets]                       #
#  *************************************************************#



    def stop_all_progress(self):
        val = self.progress["value"]
        self.progress.stop()
        self.progress["value"] = val


    def setup_tree(self):
        """Setup an example Treeview"""
        self.tree.insert("", tk.END, text="Example 1", iid="1", open=False)
        self.tree.insert("", tk.END, text="Example 2", iid="2")
        self.tree.insert('1', tk.END, text='Exmpl 11', iid="11")
        self.tree.insert('1', tk.END, text='Exmpl 12', iid="12",open=False)
        self.tree.insert("12", tk.END, text='exmpl 121', iid="121")
        
        self.tree.heading("#0", text="Tree Heading")


    
    def setup_menubar(self):
        """Setup a standard menubar populated with some stubs"""
        self.menubar = tk.Menu(self,
                            bg=chi_bg,
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg,
                            borderwidth=1)
        self.config(menu=self.menubar)
        self.menubar.configure(cursor=mac_mickey_16)
    # Apple -----------------------------------------------        
        self.apple_menu = tk.Menu(self.menubar,
                            bg=chi_bg,
                            tearoff=False,
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg)
        self.apple_menu.add_command(label="About...", command=False)
        self.apple_menu.add_separator()
        self.apple_menu.add_command(label="Help", command=False)
        self.menubar.add_cascade(menu=self.apple_menu, \
                                label=(u'\uf8ff'), \
                                font=('Chicago Kare', 12)) 
    # File -----------------------------------------------
        self.file_menu = tk.Menu(self.menubar,
                            bg=chi_bg,
                            tearoff=False,
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg)
        self.file_menu.add_command(label="New", command=False)
        self.file_menu.add_command(label="Open", command=False)
        self.file_menu.add_command(label="Save", command=False, state="disabled")
        self.file_menu.add_command(label="Save as...", command=False)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.destroy)
        self.menubar.add_cascade(menu=self.file_menu, label="File")
    # Edit -----------------------------------------------
        self.edit_menu = tk.Menu(self.menubar,
                            bg=chi_bg,
                            tearoff=False,
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg)
        self.edit_menu.add_command(label="Cut", command=False)
        self.edit_menu.add_command(label="Copy", command=False)
        self.edit_menu.add_command(label="Paste", command=False)
        self.edit_menu.add_command(label="Delete", command=False)
        self.edit_menu.add_command(label="Select All", command=False)
    # Edit>Options ----------------------------------------
        self.sub_edit_menu = tk.Menu(self.edit_menu,
                            bg=chi_bg,
                            tearoff=False,
                            relief="flat",  # Doesn't kill the corny relief arrow ...
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg)
        self.sub_edit_menu.add_command(label="Subadub", command=False)
        self.sub_edit_menu.add_command(label="Yada", command=False)
        self.sub_edit_menu.add_command(label="Nada", command=False)
        self.edit_menu.add_cascade( menu=self.sub_edit_menu, 
                                    label="Options ",
                                    bitmap="", 
                                    image=self.img_indicator, 
                                    compound='right')
        self.menubar.add_cascade(menu=self.edit_menu, label="Edit")




    
    def grid_widgets(self):
        """Put widgets on the grid"""
        sticko = {"sticky": "news"}
      
        self.spaceXY.grid(  row=0, column=0,                padx=(1,0), pady=(1,0), sticky="nw")
        self.notebook.grid( row=1, column=2, columnspan=2,                          **sticko)
        self.labelvers.grid(row=1, column=0,                padx=(20,0),pady=9,     sticky="new")
        self.separat_h.grid(row=1, column=0,                            pady=35,    sticky="new")
        self.dropdown.grid( row=3, column=2,                padx=5,                 **sticko)
        self.txt_entry.grid(row=3, column=3,                padx=5,                 **sticko)
        self.button1.grid(  row=4, column=0, columnspan=1,  padx=10,    pady=10)
        self.button2.grid(  row=4, column=2, columnspan=1,  padx=5,                 sticky="nsw")   
        self.radio_one.grid(row=5, column=2,                padx=5,                 **sticko)
        self.radio_two.grid(row=6, column=2,                padx=5,     pady=(5,0), **sticko)
        self.checked.grid(  row=5, column=3,                padx=5,                 **sticko)
        self.unchecked.grid(row=6, column=3,                padx=5,                 **sticko)        
        self.listbox.grid(  row=7, column=0, rowspan=3,     padx=12,    pady=0,     sticky="new")
        self.scrollv.grid(  row=0, column=4, rowspan=11,    padx=0,     pady=(1,16),sticky="nes")
        self.tree.grid(     row=7, column=2, columnspan=2,  padx=5,                 **sticko)
        self.scale.grid(    row=8, column=2, columnspan=2,  padx=5,                 **sticko)
        self.combo.grid(    row=9, column=2, columnspan=2,  padx=5,                 sticky="w")
        self.r1.grid(       row=9, column=0,                                        sticky="s")
        self.r2.grid(       row=10,column=0,                                        sticky="n")
        self.progress.grid( row=10,column=2, columnspan=2,  padx=5,     pady=12,    **sticko)
        self.grip.grid(     row=10,column=4,                                        sticky="se")
        
        self.rowconfigure( 0, minsize=2,    weight=1)
        self.rowconfigure(10, minsize=5,    weight=0)
        self.rowconfigure( 2, minsize=1,    weight=5)



if __name__ == '__main__':
    main()




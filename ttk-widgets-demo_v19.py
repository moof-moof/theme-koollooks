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

import os
import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from tkinter import font
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk, ImageDraw


# Version number
vnum ='v19'

# WIDTH, HEIGHT = 500, 700

# Chicago text "bicolours"
chi_fg =     '#000000'
chi_bg =     '#ffffff'
chi_act_fg = '#ffffff'
chi_act_bg = '#000000'

# Cursor images
arrow_16       = "gumby"
mac_mickey_16  = "mouse"
sizegripper_16 = "gobbler"
i_beam_16      = "bogosity"



def main():
    app = Example()
    app.mainloop()



class Example(ThemedTk):
    

    def __init__(self, theme="koollooks"):
        
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.set_theme(theme)
        self.title('Finder Demo '+ vnum)
        self.minsize(350, 425) 
        self.maxsize(400, 600)
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
    # Preload our 36x28 pixel fancy button images
        self.img_active  = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-ax.gif"))
        self.img_disabld = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-dx.gif"))
        self.img_normal  = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-nx.gif"))
        self.img_pressed = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-px.gif"))
        
    # Let's turn off every kind of focus-indication already!
        self.style.configure("TNotebook.Tab", focuscolor="chi_bg")
        self.option_add('*TNotebook*takeFocus',    0)
        self.option_add('*TButton*takeFocus',      0)
        self.option_add('*TRadiobutton*takeFocus', 0)
        self.option_add('*TCheckbutton*takeFocus', 0)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)



#  Create widgets:
#  ***************

    # Menubar
        self.setup_menubar()
        
    # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.add(ttk.Button(self, 
                                    width=2, 
                                    style="nobo.TButton", 
                                    text="Akchully...", 
                                    cursor=mac_mickey_16), 
                                    text="Tab 1")
        self.notebook.add(ttk.Button(self, 
                                    style="nobo.TButton", 
                                    text="Hello Universe", 
                                    cursor=mac_mickey_16), 
                                    text="Tab 2")
    # Label        
        self.labelv = ttk.Label(self, text='  ['+ vnum + ']  ')  
         
    # Options menu        
        self.dropdown = ttk.OptionMenu(self, tk.StringVar(), " Pick-val", "  1st Value", " 2nd Value")
        self.dropdown.config(cursor=mac_mickey_16)
        self.dropdown["menu"].config(background=chi_bg,
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg, 
                            cursor=mac_mickey_16)
    # TextEntry box        
        self.entry = ttk.Entry(self, 
                            textvariable=tk.StringVar(value="Default entry value."), 
                            cursor=i_beam_16)
    # Button(Fancy)
        self.button1 = self.fancy_butt("OK", 5, self.do_nuthin()) 
    
    # Button(Plain)
        self.button2 = ttk.Button(self, 
                                style="Plain.TButton", 
                                width=6, 
                                padding=5, 
                                text="Cancel", 
                                cursor=mac_mickey_16) 
    # Radio        
        self.radio_one = ttk.Radiobutton(self, text="On",  value=True, cursor=mac_mickey_16)
        self.radio_two = ttk.Radiobutton(self, text="Off", value=False, cursor=mac_mickey_16)

    # Listbox
        self.listbox = tk.Listbox(self, 
                                width=3, 
                                height=9, 
                                font=self.monofont, 
                                bg=chi_bg,
                                selectbackground=chi_act_bg, 
                                selectforeground=chi_act_fg, 
                                activestyle='none', 
                                cursor=mac_mickey_16)
        self.listbox.insert(tk.END, *(f" #{i}" for i in range(100)))

    # Scrollbar
        # Create a scrollbar and grid it:
        self.scrollv = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview, cursor=mac_mickey_16)

        # Configure bilateral association of listbox and scrollbar:
        self.listbox['yscrollcommand'] = self.scrollv.set
#         self.scrollv.config(command = self.listbox.yview)   # similar, alternative statement

   
    # Checkbtn     
        self.checked = ttk.Checkbutton(self, 
                                        text="Checked", 
                                        variable=tk.BooleanVar(value=True), 
                                        cursor=mac_mickey_16)
        self.unchecked = ttk.Checkbutton(self, 
                                        text="Unchecked", 
                                        cursor=mac_mickey_16)
    # Treeview
        self.tree = ttk.Treeview(self, height=5, show=("tree", "headings"), cursor=mac_mickey_16)
        self.setup_tree()
    
    # ScaleEntry
        self.scale_entry = ScaleEntry(self, 
                                    from_=0, to=50, 
                                    orient=tk.HORIZONTAL, 
                                    compound=tk.RIGHT, 
                                    cursor=mac_mickey_16)
    # Combobox
        self.style.configure('TCombobox', background=chi_bg, foreground=chi_fg)   # Superfluous?
        self.combo = AutocompleteCombobox(self, 
                                        cursor=arrow_16, 
                                        completevalues=["something", "nothing", "Tralah"])
        self.option_add("*TCombobox*Listbox*Background", chi_bg)
        self.option_add("*TCombobox*Listbox*Foreground", chi_fg)
        self.option_add("*TCombobox*Listbox*cursor", i_beam_16)
    
    # Progress bar
        self.progress = ttk.Progressbar(self, maximum=100, value=70)
    
    # Sizegrip
        self.grip = ttk.Sizegrip(self, cursor=sizegripper_16)
   
    # Separator (horisontal) as spacer?:
        self.separator1h = ttk.Separator()


#  Do da layout:
#  *************   
    
    # Grid widgets
        self.grid_widgets()


     
    def do_nuthin(self):
        pass

##  Menu.tk_strictMotif=False  ## TEST THIS

    def setup_menubar(self):
        """Setup a standard menubar"""
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
        self.apple_menu.add_command(label="About...", command=self.do_nuthin())
        self.apple_menu.add_separator()
        self.apple_menu.add_command(label="Help", command=self.do_nuthin())
        self.menubar.add_cascade(menu=self.apple_menu, \
                                label=(u'\uf8ff'), \
                                font=('Chicago Kare', 12)) 
    # File -----------------------------------------------
        self.file_menu = tk.Menu(self.menubar,
                            bg=chi_bg,
                            tearoff=False,
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg)
        self.file_menu.add_command(label="New", command=self.do_nuthin())
        self.file_menu.add_command(label="Open", command=self.do_nuthin())
        self.file_menu.add_command(label="Save", command=self.do_nuthin(), state="disabled")
        self.file_menu.add_command(label="Save as...", command=self.do_nuthin())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.destroy)
        self.menubar.add_cascade(menu=self.file_menu, label="File")
    # Edit -----------------------------------------------
        self.edit_menu = tk.Menu(self.menubar,
                            bg=chi_bg,
                            tearoff=False,
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg)
        self.edit_menu.add_command(label="Cut", command=self.do_nuthin())
        self.edit_menu.add_command(label="Copy", command=self.do_nuthin())
        self.edit_menu.add_command(label="Paste", command=self.do_nuthin())
        self.edit_menu.add_command(label="Delete", command=self.do_nuthin())
        self.edit_menu.add_command(label="Select All", command=self.do_nuthin())
    # Edit>Options ----------------------------------------
        self.sub_edit_menu = tk.Menu(self.edit_menu,
                            bg=chi_bg,
                            tearoff=False,
                            relief="flat",  # Doesn't kill the corny relief arrow ...
                            activebackground=chi_act_bg,
                            activeforeground=chi_act_fg)
        self.sub_edit_menu.add_command(label="Subadub", command=self.do_nuthin())
        self.sub_edit_menu.add_command(label="Yada", command=self.do_nuthin())
        self.sub_edit_menu.add_command(label="Nada", command=self.do_nuthin())
        self.edit_menu.add_cascade( menu=self.sub_edit_menu, 
                                    label="Options ",
                                    bitmap="", 
                                    image=self.img_indicator, 
                                    compound='right')
        self.menubar.add_cascade(menu=self.edit_menu, label="Edit")

    def setup_tree(self):
        """Setup an example Treeview"""
        self.tree.insert("", tk.END, text="Example 1", iid="1", open=False)
        self.tree.insert("", tk.END, text="Example 2", iid="2")
        self.tree.insert('1', tk.END, text='Exmpl 11', iid="11")
        self.tree.insert('1', tk.END, text='Exmpl 12', iid="12",open=False)
        self.tree.insert("12", tk.END, text='exmpl 121', iid="121")
        
        self.tree.heading("#0", text="Tree Heading")

    def fancy_butt(self, txt, hpad, cmd):        
        ''' 
    1. Map the 7-pixels thick border regions '''
        # format: border = (left, top, right, bottom)
        # Setting top/bottom to 0 prevents vertical scaling distortions
        self.style.element_create(
            "dflt.Button.background", 
            "image", 
            self.img_normal,
            ("pressed", self.img_pressed),
            ("active", self.img_active),
            border=(7, 0, 7, 0),    # Claims 7px on each side (left/right)
            sticky="ew"             # Restricts stretching strictly to the X-axis
        )
        ''' 
    2. Rebuild button layout with centered text '''
        self.style.layout(
            "dflt.TButton",
            [
                ("dflt.Button.background", {"children": [
                    ("Button.padding", {"children": [ 
                        ("Button.label", {"sticky": "nswe"}) 
                    ], 'sticky': 'nswe'})
                ], 'sticky': 'nswe'})
            ]
        )
        '''
    3. Enforce the fixed 28px height '''
        # Koolooks/clam may add default padding, so we control that explicitly here.
        # Inside padding: left/right, top/bottom (managed by image height).
        self.style.configure("dflt.TButton", padding=((hpad-12), 0))
        # Force the button widget to match our 28px image limit natively.
        self.option_add("*dflt.TButton.height", 28)
        # This width param is ignored, just stuck on 78px (7+64+7) even with padding=0!
        self.option_add("*dflt.TButton.width", 0)
        
        # We sneak in the Mickey Mouse pointer glove on return
        return ttk.Button(self, style="dflt.TButton", text=txt, command=cmd, cursor=mac_mickey_16)
  
    
    def grid_widgets(self):
        """Put widgets in the grid"""
        sticko = {"sticky": "news"}
        self.notebook.grid(row=0, column=1, columnspan=2, **sticko)
        self.labelv.grid(row=9, column=0, columnspan=1, sticky="ew")
        self.dropdown.grid(row=2, column=1, **sticko)
        self.entry.grid(row=2, column=2, **sticko)
        self.button1.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        self.button2.grid(row=3, column=1, columnspan=1, sticky=tk.NS)
        self.radio_one.grid(row=4, column=1, **sticko)
        self.radio_two.grid(row=4, column=2, **sticko)
        self.checked.grid(row=5, column=1, **sticko)
        self.unchecked.grid(row=5, column=2, **sticko)        
        self.listbox.grid(row=6, column=0, rowspan=3, padx=12, pady=0, sticky="new")
        self.scrollv.grid(row=0, column=3, rowspan=10, padx=5, pady=5, **sticko)
        self.tree.grid(row=6, column=1, columnspan=2, **sticko)
        self.scale_entry.grid(row=7, column=1, columnspan=2, **sticko)
        self.combo.grid(row=8, column=1, columnspan=2, sticky="w")
        self.progress.grid(row=9, column=1, columnspan=2, padx=5, pady=5, **sticko)
        self.grip.grid(row=10, column=3, sticky="se")
        self.separator1h.grid(row=10, column=1, sticky="we")




if __name__ == '__main__':
    main()











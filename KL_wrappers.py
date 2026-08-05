#!/usr/bin/python3
'''
VERSION USING PLACE().
'''
import os
import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from tkinter import font
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk, ImageDraw
from itertools import count



# Chicago text "bicolours"
chi_fg = chi_act_bg = '#000000'
chi_bg = chi_act_fg = '#ffffff'

# Cursor images
arrow_16       = "gumby"
mac_mickey_16  = "mouse"
sizegripper_16 = "gobbler"
i_beam_16      = "bogosity"


'''                                                         
||||||||||||||||||||-VERSION USING PLACE()-|||||||||||||||| version 1.4p
'''




def KL_setup_dBoxProc(parent, _w, _h):
    
    perim_frame = tk.Frame( parent,  
                            bg = "#ccf",
#                             borderwidth = 1, 
                            highlightbackground = "#000", 
                            highlightthickness  = 1, 
                            cursor = "gumby",
                            width  = _w, 
                            height = _h )


    inner_frame = tk.Frame( parent,
                            bg = chi_bg,
                            highlightbackground = "#000", 
                            highlightthickness  = 1, 
#                             cursor = "gumby",
                            width  = _w - 8,
                            height = _h - 8)


    perim_frame.place(x=0, y=0)
    inner_frame.place(x=4, y=4)
    


    
    

def KL_some_global_customizations(parent):
    
    parent.style.map("TButton", foreground=[('pressed', chi_bg)])
    parent.buttonFont = ('Chicago Kare', 12)
    parent.monofont = ('monaco-12-(accurate)', 12)
    parent.img_indicator = tk.PhotoImage(file=os.path.expanduser( \
                        "~/koollooks_alias/sub-menu-indicator-sn.gif")) 



def KL_checkbutton(parent, txt, bool_var):

    chk = ttk.Checkbutton(parent, 
                            text = txt, 
                            variable = tk.BooleanVar(value = bool_var), 
                            cursor = mac_mickey_16
                            )
    return chk



def KL_notebook(parent, wid, hgt, pad):

    style = ttk.Style()
    style.layout("TNotebook", [("TNotebook.client", {"sticky": "nswe"})])
    
    nb = ttk.Notebook(parent,  
                        width   = wid,
                        height  = hgt,
                        padding = pad,
                        cursor  = mac_mickey_16, 
                        style   = "TNotebook"
                        )          
    return nb
    
    
    
def KL_image_on_canvas(parent, img_pth, img_x, img_y, canvas_w, canvas_h):
    
    # Load the image using PIL
    pic = ImageTk.PhotoImage(Image.open(img_pth))
    
    # Create a Canvas widget
    canvas = tk.Canvas(parent, width=canvas_w, height=canvas_h, background="#FFF")
    canvas.pack(fill="both", expand=True)
    
    # Add the image to the canvas
    canvas.create_image(img_x, img_y, anchor=tk.NW, image=pic)

    # Beware the garbage collector
    canvas.image = pic



class KL_AnimLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    
    delay_dflt =  300
    delay_last = 2500
    delay_rest =  200
    
    
    def load(self, img):
        if isinstance(img, str):
            img = Image.open(img)
        self.loc = 0
        self.frames = []
        
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(i)
        except EOFError:
            pass

        try:
            self.delay = img.info['duration']
        except:
            self.delay = self.delay_dflt

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def next_frame(self):
            
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            if self.loc == 0:
                self.delay = self.delay_last
            else:
                self.delay = self.delay_rest
            self.config(image = self.frames[self.loc])
            self.after(self.delay, self.next_frame)



def KL_optionsmenu(parent, strvar, dflt_val, *values):
    
    options_list = [*values]
    value_inside = tk.StringVar(parent)
    
    dropdown = ttk.OptionMenu(  parent, 
                                value_inside, 
                                dflt_val,
                                *options_list
                                )
    dropdown["menu"].config(    value_inside.set(dflt_val),
                                background = chi_bg,
                                activebackground = chi_act_bg,
                                activeforeground = chi_act_fg,
                                cursor = mac_mickey_16
                                )
    return dropdown
  


def  KL_entry(parent, dflt_str):  

    txtvar = tk.StringVar(value=dflt_str)  
    
    entry = tk.Entry(parent, 
                    textvariable = txtvar,
                    bg = chi_bg,  
                    fg = chi_fg,
                    selectbackground = chi_act_bg,
                    selectforeground = chi_act_fg,
                    exportselection = False,
                    takefocus = False,
                    cursor = i_beam_16
                    )
    return entry



def fancy_butt(parent, txt, hpad, cmd):
    '''
0. Preload our special 36x28 pxl button images '''
    parent.img_active  = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-ax.gif"))
    parent.img_disabld = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-dx.gif"))
    parent.img_normal  = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-nx.gif"))
    parent.img_pressed = tk.PhotoImage(file=os.path.expanduser("~/koollooks_alias/button-px.gif"))

    ''' 
1. Map the 7-pixels thick border regions '''
    parent.style.element_create(
        "dflt.Button.background", 
        "image", 
        parent.img_normal,
        ("pressed", parent.img_pressed), 
        ("active", parent.img_active),
        border=(7, 0, 7, 0),    # Claims 7px on each side (left/right),
                                # 0px prevents vertical scaling distortions (top/bottom).
        sticky="ew" )           # Restricts stretching strictly to the X-axis.
        
    ''' 
2. Rebuild button layout with centered text '''
    parent.style.layout(
        "dflt.TButton", [(
            "dflt.Button.background", {"children": [(
                "Button.padding", {"children": [(
                    "Button.label", {"sticky": "nswe"} 
                    )], 'sticky': 'nswe'}
                )], 'sticky': 'nswe'}
            )]
        )
    '''
3. Enforce the fixed 28px height '''
        # Koolooks/clam may add default padding, so we control that explicitly here.
        # Inside padding: left/right, top/bottom (managed by image height).
    parent.style.configure("dflt.TButton", padding=((hpad-12), 0))
    
        # Force the button widget to match our 28px image limit natively.
    parent.option_add("*dflt.TButton.height", 28)
    
        # This width param is ignored; stuck on 78px (7+64+7) even with padding=0!
    parent.option_add("*dflt.TButton.width", 0)
    
        # We sneak in the Mickey Mouse glove pointer on return...
    return ttk.Button(parent,  
                    style   = "dflt.TButton", 
                    text    = txt, 
                    command = cmd, 
                    cursor  = mac_mickey_16
                    )



def plain_butt(parent, txt, wid, cmd, pad):

    return ttk.Button(parent, 
                    style   = "Plain.TButton",  
                    text    = txt,
                    width   = wid, 
                    command = cmd,
                    padding = pad,
                    cursor  = mac_mickey_16
                    ) 



def KL_listbox(parent, wid, hgt): 
    
    lbx = tk.Listbox(parent,
                    width   = wid, 
                    height  = hgt, 
                    font    = parent.monofont, 
                    bg      = chi_bg,
                    selectbackground = chi_act_bg, 
                    selectforeground = chi_act_fg, 
                    activestyle      = 'none', 
                    cursor  = mac_mickey_16
                    )  
    return lbx




def KL_LabelFrame(canv, oX, oY, wid, hei, txt):
        
    _nw = oX,       oY
    _ne = (oX+wid), oY 
    _se = (oX+wid),(oY+hei)
    _sw = oX,      (oY+hei)
    
    canv.create_rectangle(oX,oY, oX+wid,oY+hei, width=1)
    
    Lbl = tk.Label(text=txt, bg=chi_bg, fg=chi_fg)
    Lbl.place(x=oX+16, y=oY-3)



def KL_dashed_LabelFrame(canv, oX, oY, wid, hei, txt):

    _nw = oX,       oY          # 248,      33      >   248x, 33y
    _ne = (oX+wid), oY          # 248+213,  33      >   461x, 33y
    _se = (oX+wid),(oY+hei)     # 248+213,  33+130  >   461x, 163y
    _sw = oX,      (oY+hei)     # 248,      33+130  >   248x, 163y
    
# Draw each edge separately:
    canv.create_line(_nw,_ne , dash=(1, 1), width=1, fill='black')
    canv.create_line(_ne,_se , dash=(1, 1), width=1, fill='black')
    canv.create_line(_se,_sw , dash=(1, 1), width=1, fill='black')
    canv.create_line(_sw,_nw , dash=(1, 1), width=1, fill='black')

# Slap a text label across top edge:
    Lbl = tk.Label(canv, text = txt, bg = chi_bg, fg = chi_fg)
    Lbl.place(x = oX+8, y = oY-10)


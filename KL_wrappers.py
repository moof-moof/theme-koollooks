#!/usr/bin/python3


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


# Exclusive set of fonts
buttonFont = ('Chicago Kare', 12)
textfont = ('Geneva 9.1', 12)
monofont = ('Monaco Regular', 8)

# Chicago text "bicolours"
chi_fg = chi_act_bg = '#000000'
chi_bg = chi_act_fg = '#ffffff'

# Cursor images
arrow_16       = "gumby"
mac_mickey_16  = "mouse"
sizegripper_16 = "gobbler"
i_beam_16      = "bogosity"


'''                                                         
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| version 1.8
'''


def KL_setup_slate(parent, _w, _h):
    
    perim_frame = tk.Frame( parent,  
                            bg     = "#FFF",
                            borderwidth = 10, 
                            highlightbackground = "#000", 
                            highlightthickness  = 1, 
                            padx   = 0, 
                            pady   = 0, 
                            bd     = 0,  
                            cursor = "gumby",
                            width  = _w, 
                            height = _h   )

    perim_frame.grid(row=0, column=0, rowspan=100, columnspan=100, sticky="news")
    perim_frame.rowconfigure(0, weight=0)
    perim_frame.columnconfigure(0, weight=1)
    perim_frame.rowconfigure(1, weight=2)

    parent.minsize(_w, _h)
    parent.maxsize((_w+50), (_h+50))
    parent.resizable(True, True) 

    return perim_frame
    
    


def KL_some_global_customizations(parent):
    
    parent.style.map("TButton", foreground=[('pressed', chi_bg)])
    parent.buttonFont = ('Chicago Kare', 12)
    parent.disabledFont = ('chicago-disabled-2', 12)
    parent.monofont = ('Monaco Regular', 8)
    parent.textfont = ('Geneva 9.1', 12)
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



def plain_butt(parent, txt, wid, pad, cmd):

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




'''                                                         
||||||||||||||-DEFS USING PLACE() IN PLACES-|||||||||||| version 1.5_pl
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

# Slap a text label across frame's top edge:
    Lbl = tk.Label(canv, text = txt, bg = chi_bg, fg = chi_fg)
    Lbl.place(x = oX+8, y = oY-10)


def cmd_line_lbl(canv, oX, oY, dir_name):
    
    _fo = monofont
    _an = "e"
    _ju = tk.LEFT
    _bg = chi_bg 
    _fg = chi_fg
    
    prompt = tk.Label(canv, text=dir_name, font=_fo, anchor=_an, justify=_ju, bg=_bg, fg=_fg, height=1)


    return prompt



def KL_help_text(canv, oX, oY, txt1, txt2, txt3):
    '''
    To avoid having the help-text background overwriting parts of the labelframe,
    we can control the effective lineheight by making each text-line a separate label.
    '''
    _fo = textfont
    _an = "e"
    _ju = tk.LEFT
    _bg = chi_bg 
    _fg = chi_fg

    '''
    Note that the order of the following variable declarations is reversed. 
    This is to prevent lines from being partially obscured by its succeeding line'''
    line3 = tk.Label(canv, text=txt3, font=_fo, anchor=_an, justify=_ju, bg=_bg, fg=_fg, height=1)
    line2 = tk.Label(canv, text=txt2, font=_fo, anchor=_an, justify=_ju, bg=_bg, fg=_fg, height=1)
    line1 = tk.Label(canv, text=txt1, font=_fo, anchor=_an, justify=_ju, bg=_bg, fg=_fg, height=1)

    '''
    Finally the line-heights are set to 11px instead of the default 12
    '''
    line1.place(x=oX, y=oY)
    line2.place(x=oX, y=oY+11)
    line3.place(x=oX, y=oY+22)



def KL_vertical_scrollbar(parent, slave):
    
    '''
    This "alternative" scrollbar is a silly hack! The reason it is needed at all is 
    due to the fact that Tkinter's filedialogue boxes, when requiring scrollbars 
    (always horizontal by design), automatically use the "sbtrough-v" trough image which
    of course is designed to fit vertical scrollbars only! It simply looks grotesque. 
    Since the viewport parts of Tk's filedialogues are not managed by our app's code, 
    but are actually rendered by OS routines "behind the scene", I doubt there exists 
    an easy way for us to coerce the system to use the correct trough image.
    
    This function is a work-around for "fixing" this bug: A copy of sbtrough-h.gif
    is simply renamed sbtrough-v.gif. Meanwhile the "real" sbtrough-v image is
    renamed sbtrough-w and instead used for all actual vertical scrollbars. '''

# ---------------------------------------------------------
# 1. Create a Custom Trough Image Element
# ---------------------------------------------------------

    parent.new_trough_img = tk.PhotoImage(file=os.path.expanduser(\
                                            "~/koollooks_alias/sbtrough-w.gif"))
    parent.style.element_create(  "w.trough", 
                                  "image",
                                   parent.new_trough_img,
                                   sticky = "ns"
                                   )

# ---------------------------------------------------------
# 2. Build the Custom Layout
# ---------------------------------------------------------
    ''' 
    Define an alternate layout for our "new" vertical scrollbar style, replacing
    the default "Vertical.Scrollbar.trough" with our custom "w.trough".'''

    parent.style.layout("Alt.Vertical.TScrollbar", [
        ('w.trough', {
            'sticky': 'ns', 
            'children': [
                ('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}),
                ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}),
                ('Vertical.Scrollbar.thumb', {'sticky': 'nswe', 'expand': '1'})
            ]
        })
    ])

# ---------------------------------------------------------
# 3. Implement the Scrollbars
# --------------------------------------------------------- 

    parent.scrollw = ttk.Scrollbar(parent,
                                    command= slave.yview, 
                                    style="Alt.Vertical.TScrollbar",
                                    cursor=mac_mickey_16
                                )

    # Callback to scrollbar from scrollable widget:
    slave['yscrollcommand']  = parent.scrollw.set
    
    # A suitable pack() stanza:
#     parent.scrollw.pack(padx=(0,4), pady=(5,5), side=tk.RIGHT, fill=tk.Y)
        
    return  parent.scrollw
    

# ?????????????????????????????????????????????????????????????????????????????????????
# ¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿
  
    


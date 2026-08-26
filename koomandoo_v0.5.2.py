#!/usr/bin/python3
"""
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL

Koomandoo is a facsimile recreation of Apple Unix (A/UX) utility (called 
"Commando") for composing unix commands simply by choosing available 
command-options through point-and-click. This python application has no 
actual functionality yet, just a pretty ui.

(Quote from Wikipedia's entry for A/UX:)
"The Commando utility assists users with entering Unix commands, 
resembling the one in Macintosh Programmer's Workshop. Opening a Unix 
executable file from Finder opens a dialog box that allows the user to 
choose command-line options for the program using standard controls such 
as radio buttons and check boxes, and display the resulting command line 
argument for the user before executing the command or program." 
    
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
"""


import KL_wrappers as kl
import tkinter as tk
import os
import time
from tkinter import ttk
from tkinter import Tk
from tkinter import font
from tkinter.ttk import Checkbutton, Button, LabelFrame
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk, ImageDraw
from itertools import count

# Version number
vnum ='v0.5x'

WIDTH, HEIGHT = 496, 311

# Chicago font "bicolours"
chi_fg = chi_act_bg = '#000000'
chi_bg = chi_act_fg = '#ffffff'

# Cursor images
arrow_16       = "gumby"
mac_mickey_16  = "mouse"
sizegripper_16 = "gobbler"
i_beam_16      = "bogosity"

theme = "koollooks"


## Measurements constants:
wd = 496
ht = 311
wdB = wd-16         # == 480
htB = ht-17         # == 294

# Origo<-->lf_options (old labelframe type) diff constant:
xa = 14
ya = 24


def main():
    app = Composer()
    app.set_theme(theme)
    app.mainloop()



class Composer(ThemedTk):
    

    def __init__(self):#, theme="koollooks"):
        
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.title('Koomandoo '+ vnum)
        self.minsize(wd, ht) 
        self.maxsize(wd, ht)
        self.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use(theme)
        self.configure(cursor=arrow_16)
        
#[kl] Some global customizations
        kl.KL_some_global_customizations(self)

    # Let's turn off every kind of focus-indication already!
        self.style.configure("TNotebook.Tab", focuscolor="chi_bg")
        self.style.configure('TLabelframe', 
                                background=chi_bg, 
                                borderwidth=1)
        self.option_add('*TNotebook*takeFocus',    0)
        self.option_add('*TButton*takeFocus',      0)
        self.option_add('*TRadiobutton*takeFocus', 0)
        self.option_add('*TCheckbutton*takeFocus', 0)


#                      Create widgets:
#  ********************************************************************#


#+++# Ground work ::::::::::::::::::::::::::::::::::::::::::::::::::::::

#[kl] "Slate"
        kl.KL_setup_dBoxProc(self, wd, ht)


# Frame-up from the bottom
        self.Bframe = tk.Frame(self,
                                bg = chi_bg,
                                cursor = "gumby",
                                width  = wdB,       # == 480
                                height = htB )      # == 294
                            
        self.Bframe. place (x=8, y=7)

        
#+++# Canvas :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        self.canvas0 = tk.Canvas(self.Bframe,
                                    highlightthickness=0, 
                                    width=wdB, height=htB, bg=chi_bg)                                 
        self.canvas0.place(x=0, y=0)          ### Covers Bframe exactly!
#       ----------------------------------------------------------------
        self.canvas1 = tk.Canvas(self.Bframe, 
                                    highlightthickness=0, 
                                    width=222, height=91, bg=chi_bg)
        self.canvas1.place(x=9, y=47)
#       ----------------------------------------------------------------
        self.canvas2 = tk.Canvas(self.Bframe, 
                                    highlightthickness=0, 
                                    width=222, height=70, bg=chi_bg)
        self.canvas2.place(x=9, y=120)
#       ----------------------------------------------------------------       
        self.canvas3 = tk.Canvas(self.Bframe, 
                                    highlightthickness=0, 
                                    width=233, height=170, bg=chi_bg)
        self.canvas3.place(x=235, y=17)


#+++# Dashed "LabelFrames" :::::::::::::::::::::::::::::::::::::::::::::

        self.fileTypes_Frm = kl.KL_dashed_LabelFrame(self.canvas1,
                                                    4, 8, 
                                                    213, 62, 
                                                    "Mark file types")
#       ----------------------------------------------------------------                                             
        self.show_More_Frm = kl.KL_dashed_LabelFrame(self.canvas2,
                                                    4, 8, 
                                                    213, 62, 
                                                    "Show more information") 
#       ----------------------------------------------------------------                                            
        self.listStyle_Frm = kl.KL_dashed_LabelFrame(self.canvas3,
                                                    7, 9, 
                                                    213, 130, 
                                                    "Listing style")

#+++# kl.LabelFrames :::::::::::::::::::::::::::::::::::::::::::::::::::

        self.lf_options = kl.KL_LabelFrame(self.canvas0,
                                            5, 8,
                                            470, 182, 
                                            'ls Options')
#       ----------------------------------------------------------------
        self.lf_Cmnd =    kl.KL_LabelFrame(self.canvas0,
                                            5, 201, 
                                            470, 32, 
                                            'Command Line')
#       ----------------------------------------------------------------                                            
        self.lf_Help =    kl.KL_LabelFrame(self.canvas0,
                                            5, 244, 
                                            350, 44, 
                                            'Help')

#+++" kl.KL_help_text ::::::::::::::::::::::::::::::::::::::::::::::::::

        self.help_text = kl.KL_help_text(self.canvas0,
            oX = 8, 
            oY = 250, 
            txt1 = 'List the contents of a directory and/or display information about the files ', 
            txt2 = 'listed.',
            txt3 = '')


#+++# Radio groups :::::::::::::::::::::::::::::::::::::::::::::::::::::

        self.var_mark   = tk.StringVar(self, "11")        # 3 switches
        self.var_format = tk.StringVar(self, "12")        # 2 switches
        self.var_sort   = tk.StringVar(self, "121")       # 2 switches
        self.var_group  = tk.StringVar(self, "122")       # 3 switches

    ## Filter types
        self.radbtn1 = ttk.Radiobutton(self.lf_options, 
                                        text="No marking", 
                                        variable = self.var_mark,
                                        value=1, 
                                        cursor=mac_mickey_16) 
        self.radbtn1.place(x=xa+13, y=ya+45)
#       ----------------------------------------------------------------
        self.radbtn2 = ttk.Radiobutton(self.lf_options, 
                                        text="Mark directories", 
                                        variable = self.var_mark, 
                                        value=2, 
                                        cursor=mac_mickey_16) 
        self.radbtn2.place(x=xa+13, y=ya+62)
#       ----------------------------------------------------------------
        self.radbtn2 = ttk.Radiobutton(self.lf_options, 
                                        text="Mark other types", 
                                        variable = self.var_mark, 
                                        value=3, 
                                        cursor=mac_mickey_16) 
        self.radbtn2.place(x=xa+13, y=ya+79)


    ## Listing style
        self.radbtn11 = ttk.Radiobutton(self.lf_options, 
                                        text="Short format, one column",
                                        variable = self.var_format,
                                        value=1, 
                                        cursor=mac_mickey_16,
                                        command = self.enbl_sort_opts) 
        self.radbtn11.place(x=xa+242, y=ya+16)
#       ----------------------------------------------------------------
        self.radbtn12 = ttk.Radiobutton(self.lf_options, 
                                        text="  sorted vertically",
                                        variable = self.var_sort,
                                        value=2, 
                                        cursor=mac_mickey_16,
                                        state='disabled')
        self.radbtn12.place(x=xa+242, y=ya+33)
#       ----------------------------------------------------------------
        self.radbtn13 = ttk.Radiobutton(self.lf_options, 
                                        text="  sorted horizontally", 
                                        variable = self.var_sort,
                                        value=3, 
                                        cursor=mac_mickey_16,
                                        state='disabled')
        self.radbtn13.place(x=xa+242, y=ya+50)
#       ----------------------------------------------------------------



    ## Configure custom text styles for different radio-button "states"
        self.style.configure("Norml.TRadiobutton", font=("Chicago Kare", 12))
                                                    
        self.style.configure("Disab.TRadiobutton", foreground="black",
                                                   font=("Chicago-Disabled-3", 12))


        self.radbtn14 = ttk.Radiobutton(self.listStyle_Frm,
                                        text="Long format",
                                        variable = self.var_format,
                                        value=2, 
                                        cursor=mac_mickey_16,
                                        command = self.enbl_info_opts) 
        self.radbtn14.place(x=xa+242, y=ya+67)
#       ----------------------------------------------------------------
        self.radbtn15 = ttk.Radiobutton(self.lf_options, 
                                        text="  show ID numbers",
                                        style = "Norml.TRadiobutton",
                                        variable = self.var_group, 
                                        value=1, 
                                        cursor=mac_mickey_16,
                                        state='disabled')
        self.radbtn15.place(x=xa+242, y=ya+84)
#       ----------------------------------------------------------------
        self.radbtn16 = ttk.Radiobutton(self.lf_options, 
                                        text="  no group information",
                                        style = "Norml.TRadiobutton",
                                        variable = self.var_group,  
                                        value=2, 
                                        cursor=mac_mickey_16,
                                        state='disabled')
        self.radbtn16.place(x=xa+242, y=ya+101)
#       ----------------------------------------------------------------
        self.radbtn17 = ttk.Radiobutton(self.lf_options, 
                                        text="  no owner information",
                                        style = "Norml.TRadiobutton",
                                        variable = self.var_group,  
                                        value=3, 
                                        cursor=mac_mickey_16,
                                        state='disabled')
        self.radbtn17.place(x=xa+242, y=ya+118)



#+++# Checkbuttons :::::::::::::::::::::::::::::::::::::::::::::::::::::

    ## Show more information
        self.chkbtn1 = Checkbutton(self.lf_options, text='List all files', 
                                        cursor=mac_mickey_16)
        self.chkbtn1.place(x=xa+12, y=ya+117)
#       ----------------------------------------------------------------
        self.chkbtn2 = Checkbutton(self.lf_options, text='Show size in blocks', 
                                        cursor=mac_mickey_16)
        self.chkbtn2.place(x=xa+12, y=ya+134)
#       ----------------------------------------------------------------
        self.chkbtn3 = Checkbutton(self.lf_options, text='Show i-node numbers', 
                                        cursor=mac_mickey_16)
        self.chkbtn3.place(x=xa+12, y=ya+151)
        

#+++# Buttons ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
       
#[kl] Buttons(Plain)                (parent, txt, wid, cmd, pad):
        self.button2 = kl.plain_butt(self, "Cancel",
                            12, False, 0)
        self.button2.place(x=375, y=242)
#       ----------------------------------------------------------------
        self.button3 = kl.plain_butt(self.lf_options, "Choose directories/files", 
                            26, False, 0)
        self.button3.place(x=6+xa, y=-1+ya)
#       ----------------------------------------------------------------
        self.button4 = kl.plain_butt(self.lf_options, "More options", 
                            12, False, 0)
        self.button4.place(x=254, y=169)
#       ----------------------------------------------------------------
        self.button5 = kl.plain_butt(self.lf_options, "Output & Error", 
                            13, False, 0)
        self.button5.place(x=364, y=169)
#       ----------------------------------------------------------------

        '''
        The "fancy" button (button1) has bigger dimensions than button2,
        so has to pe placed last in order not to be partially covered by 
        the simpler button gif-image's surrounding "whitespace".
        '''
#[kl] Button(Fancy)
        self.button1 = kl.fancy_butt(self,"    ls    ", 29, False)
        self.button1.place(x=372, y=268) 



# #[kl] Options menu        
#         self.dropdown = kl.KL_optionsmenu(self, 
#                                         tk.StringVar(),
#                                         "     Choose directories/files ", 
#                                         " Val A ", 
#                                         " Val B ",
#                                         " Val C ")
# #[kl] TextEntry box
#         self.txt_entry = kl.KL_entry(self, " Default entry value...")         
#         self.txt_entry2 = kl.KL_entry(self, " Default2 entry value...")  



#                    [End create widgets]                              #
#  ********************************************************************#


    def enbl_sort_opts(self, *args):
    # Enable sorts:
        self.radbtn12.config(state='normal', style="Norml.TRadiobutton")
        self.radbtn13.config(state='normal', style="Norml.TRadiobutton")
    # Disable info-groups:
        self.radbtn15.config(state='disabled', style="Disab.TRadiobutton")
        self.radbtn16.config(state='disabled', style="Disab.TRadiobutton")
        self.radbtn17.config(state='disabled', style="Disab.TRadiobutton")


    def enbl_info_opts(self, *args):
    # Disable sorts:
        self.radbtn12.config(state='disabled', style="Disab.TRadiobutton")
        self.radbtn13.config(state='disabled', style="Disab.TRadiobutton")
    # Enable info-groups:
        self.radbtn15.config(state='normal', style="Norml.TRadiobutton")
        self.radbtn16.config(state='normal', style="Norml.TRadiobutton")
        self.radbtn17.config(state='normal', style="Norml.TRadiobutton")



if __name__ == '__main__':
    main()



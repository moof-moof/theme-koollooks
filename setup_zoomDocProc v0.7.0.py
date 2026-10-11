#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys, os, platform
from PIL import Image, ImageTk, ImageDraw
import KL_wrappers as kl


WW = 500        # Default window width
HH = 400        # Default window height
xx = 300        # Default window x coordinate
yy = 400        # Default window y coordinate

Wmin = 180      # Used for sizing "iconified" state
Hmin = 54       # Used for sizing "iconified" state

Wmax = 640      # Used for sizing "full VGA" state
Hmax = 480      # Used for sizing "full VGA" state

barT = 18       # Height of Title bar panel
barM = 20       # Height of Menu bar panel

headH = barT+barM

x1, y1 = 0, 0   # Mouse tracking vars

_resize_job = True



def setup_titled_menued_slate():

    # Create the main window
    root = tk.Tk()
    # Title for the WM frame-header. Only used in framed mode.
    root.title("Title+Menu+Scrollbar (zoomDocProc-template)")


    # Set the window size and initial position
    root.geometry("{}x{}+{}+{}".format(WW,HH,xx,yy))
    root.minsize(Wmin, Hmin)   # "Iconified" size
    root.maxsize(Wmax, Hmax)   # == 14"(13") screen resolution
    root.resizable(True, True)
    _iconic = False  

    
    # Save screen dimensions
    scrW = root.winfo_screenwidth()
    scrH = root.winfo_screenheight()

    
    theme = "koollooks"
    ck12 = ('Chicago Kare', 12)
    buttonFont = ck12
    chi_bg = chi_act_fg = "#ffffff"
    chi_fg = chi_act_bg = "#000000"
    root.style = ttk.Style()
    root.style.theme_use(theme)

    
    # Pre-selecting various button images   
    ii = tk.PhotoImage(file = "~/koollooks_alias/sub-menu-indicator-sn.gif")
    sg = tk.PhotoImage(file = "~/koollooks_alias/sizegrip-n.gif")
    cb = tk.PhotoImage(file = "~/koollooks_alias/sys6/close-btn_extd.png")
    zb = tk.PhotoImage(file = "~/koollooks_alias/sys6/expand-btn_extd.png")
 
    
    
    def on_start_hover(menu_btn):
        menu_btn.configure(state=ACTIVE)

    def on_end_hover(menu_btn):
        menu_btn.configure(state=NORMAL)

    def basho(cmd):
        print(cmd) #(cmd, end='')
        
    def window_closer():
        root.destroy()
        
    # Cross platform scroll wheel event handler 
    def on_mouse_wheel(event):
        if platform.system() == 'Windows':
            canv_bdy.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            canv_bdy.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                canv_bdy.yview_scroll( -1, "units" )
            elif event.num == 5:
                canv_bdy.yview_scroll( 1, "units" )
    
    # Bind wheel events when the cursor enters
    def on_enter(event): 
        if platform.system() == 'Linux':
            canv_bdy.bind_all("<Button-4>", on_mouse_wheel)
            canv_bdy.bind_all("<Button-5>", on_mouse_wheel)
        else:
            canv_bdy.bind_all("<MouseWheel>", on_mouse_wheel)

    # Unbind wheel events when the cursor exits
    def on_leave(event):
        if platform.system() == 'Linux':
            canv_bdy.unbind_all("<Button-4>")
            canv_bdy.unbind_all("<Button-5>")
        else:
            canv_bdy.unbind_all("<MouseWheel>")



    ''' ====================== WINDOW ZOOMS ============================
    '''
    # Shows/Hides window-manager's title-bar and frame per saved settings:
    def reference_frame():
        a = "./settings.conf"
        if os.path.exists(a) and os.path.getsize(a) > 0: # Let's READ it
            _fl = open(a, "r") 
            _ln = _fl.readlines()        
            oo = _ln[1]  # 2nd line: on/off, True/False   
            return oo     
        else:    # Write a new config file from scratch with temporary truth
            fl = open(a, "w")
            ln = ["Go frameless? (0==False,1==True)\n"]
            fl.writelines(ln)   # line 1: First place the info-text
            fl.write("True")    # line 2: The boolean value next 
            return True

    root.overrideredirect(reference_frame())  # Triggers frame status update


    def iconifyer():     
        global lw, lh, lx, ly
        
        # Store current geometry
        root.update_idletasks() 
        lw = root.winfo_width()
        lh = root.winfo_height()
        lx = root.winfo_x()
        ly = root.winfo_y()
        iw,ih = root.minsize()
        
        # Apply the pseudo icon-format:   ( w,  h, x,  y )
        root.geometry("{}x{}+{}+{}".format(iw, ih, 1, scrH - 83))

    def expander():
        # Restore previous geometry
        root.geometry("{}x{}+{}+{}".format(lw, lh, lx, ly))

    def toggler():
        nonlocal _iconic
        if _iconic: expander()
        else: iconifyer()
        _iconic = not _iconic



    ''' ====================== GO FRAMELESS ============================
    '''
    # Reads boolean frame state, dumps inverse state back to settings file:
    def frame_set():
        f2 = open("./settings.conf", "r")               ## Inhale ...
        l2 = f2.readlines()        
        tf = str(l2[1])      # on/off, True or False 
        if tf == "True": tf = "False"                   ## Switcheroo!
        else: tf = "True"
        
        fl = open("settings.conf", "w")                 ## Exhale ...
        ln = ["Go frameless? (0==False,1==True)\n"]
        fl.writelines(ln)   # line 1: Place the info-text firstly
        fl.write(str(tf))   # line 2: The boolean value next
        fl.close()   

    def frame_toggler(frmls):
        print("1", frmls)
        frmls = not frmls   # Inverting state
        print("2", frmls)
        nonlocal frame_set
        frame_set(frmls)    # Write new state value back to config



    ''' ================== TRACK WINDOW RESIZING =======================
    '''
    def on_window_resize(event):
        '''Coalesce rapid resize events to avoid excessive redraw'''
        global _resize_job
        if _resize_job:
            canv_bdy.after_cancel(_resize_job)
        w, h = event.width, event.height
        canv_bdy.itemconfig(canvas_window, width = w)
        _resize_job = canv_bdy.after(80, lambda: redraw(w, h)) 

    def redraw(w, h,):
#         root.update_idletasks()
#         frm_bdy_content.height = h-headH
        frm_bdy_content.width = w

    def on_frame_configure(event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        canv_bdy.configure(scrollregion=canv_bdy.bbox("all"))

    def on_canvas_configure(event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        canv_bdy.itemconfig(canvas_window, width = canvas_width)
 
        
        
    ''' ================== GRAB PANEL...DRAG WINDOW! ===================
    '''
    def drag_window(widget):
        
        if not root.overrideredirect:
            return
        else:
            if isinstance(widget, Tk):
                master = widget  # == root window (never accessed)
            else:
                master = root
            
            def mouse_motion(event):
                global x1, y1
                offset_x, offset_y = event.x - x1, event.y - y1  
                new_x = master.winfo_x() + offset_x
                new_y = master.winfo_y() + offset_y
                new_geometry = f"+{new_x}+{new_y}"
                master.geometry(new_geometry)

            def mouse_press(event):
                global x1, y1
                x1, y1 = event.x, event.y

            # Left-mouse-button-drag events
            widget.bind("<B1-Motion>", mouse_motion)
            # The left mouse button press event
            widget.bind("<Button-1>", mouse_press)


    """ =====================  TITLE-BAR FRAME  ========================
    """
    # Create our custom title bar
    frm_titlebar = tk.Frame(root,
                            height = 20,
#                             width = WW,
                            bd = 0,
                            bg = chi_bg,
                            highlightbackground = chi_act_bg, 
                            highlightthickness  = 1)
                            
    frm_titlebar.place(x=0, y=0, anchor="nw", relwidth=1.0)


    """ =====================  BUTTONS  ================================
    """
    # Adding 'Close' and 'Expand' buttons to the title bar.
    close_button = tk.Button(frm_titlebar, 
                            image = cb, 
                            command = window_closer,
                            text = False, 
                            bd = 0, 
                            bg = chi_bg, 
                            height = 0,
                            highlightthickness = 0)

    close_button.pack(side=tk.LEFT, anchor=tk.NW)
    close_button.config(width = 18, height = 15)


    zoom_button = tk.Button(frm_titlebar, 
                            image = zb, 
                            command = toggler,
                            text = False, 
                            bd = 0, 
                            bg = chi_bg, 
                            height = 0,
                            highlightthickness = 0)

    zoom_button.pack(side = tk.RIGHT, anchor = tk.NE)
    zoom_button.config(width = 18, height = 15)



    """ ==================  TITLEBAR CANVAS  ===========================
    """
    wiwi = Wmax-42  # wiwi: Dynamic window-width variable
    toTop = 3       # Topmost stripe's distance to window top-edge

    midpanel = tk.Canvas(frm_titlebar,
                           bg = chi_bg, 
                           width = wiwi,
                           height = 16, 
                           highlightbackground = chi_bg, 
                           highlightthickness  = 0 )
               
    # Bind the panel to the window-moving function
    if root.overrideredirect:
        drag_window(midpanel)
    

    """ =====================  STRIPES  ============================= 
    """
    # Start points for stripe cluster:
    W = 0  
    w = toTop

    # End points for stripe cluster:
    E = wiwi
    e = toTop

    # Draw six horisontal 1 pixel wide stripes, 2 pixels apart
    for stripes in range(6):
        stripe = midpanel.create_line( W, w, E, e, fill = chi_fg )
        w = e = e+2

    midpanel.pack(anchor=tk.N)
    midpanel.pack_propagate(0)


    """ =====================  LABEL  ===============================
    """
    # Add a title (via a compound label) to our custom title bar
    blank = tk.PhotoImage()
    
    titl = tk.Label(midpanel, 
                    image = blank, 
                    font = buttonFont,
                    text ="Titulus",
                    width = 70,
                    height = 15, 
                    compound = "c", 
                    bg = chi_bg, 
                    fg = chi_fg,
                    bd = 1 )
 
    titl.pack(anchor=tk.S,
                pady = (1, 0))
    
    # Also bind the title label to the window moving function
    if root.overrideredirect:
        drag_window(titl)


    
    """ ===================  MENUBAR FRAME  =========================
    """
    """ Create a framed foundation for drawing the black "borders", etc."""
    frm_menubar_bottom = tk.Frame(root, 
                            bg = chi_bg, 
                            highlightbackground = chi_act_bg, 
                            highlightthickness = 1)

    # Here we restrict "menubar" height by limiting its enclosing frame.
    frm_menubar_bottom.place(relwidth = 1.0, height = 21, x = 0, y = 18) 
    
    
    """ Create a Frame to serve as a custom container for the menubar."""     
    frm_menubar_proper = tk.Frame(frm_menubar_bottom, 
                            bg = chi_bg, 
                            bd = -1,                     # No borders ...
                            highlightbackground= chi_act_bg,
                            highlightthickness = 0)      # Invisible!
    
    frm_menubar_proper.pack(side = LEFT, 
                            expand = 0, 
                            fill = "both", 
                            padx = 0,
                            pady = (0, 2) )


    """ Add Menubuttons inside the frame.
        Directly limit vertical sizing via internal padding (pady)."""        
    # Apple -----------------------------------------------        
    apple_btn = tk.Menubutton(frm_menubar_proper,
                            text = (" " u'\uf8ff'),
                            font = ck12,
                            fg = chi_fg, 
                            bg = chi_bg, 
                            activeforeground = chi_act_fg,
                            activebackground = chi_act_bg)
                        
    apple_btn.pack(side="left", pady=(2,0))
    
    
    # File ----------------------------------------------- 
    file_btn = tk.Menubutton(frm_menubar_proper,
                            text ="File",
                            font = ck12,
                            fg = chi_fg, 
                            bg = chi_bg, 
                            activeforeground = chi_act_fg,
                            activebackground = chi_act_bg)
    
    file_btn.pack(side="left", pady=(2,0))
    
    # Edit ----------------------------------------------- 
    edit_btn = tk.Menubutton(frm_menubar_proper,
                            text ="Edit",
                            font = ck12,
                            fg = chi_fg, 
                            bg = chi_bg, 
                            activeforeground = chi_act_fg,
                            activebackground = chi_act_bg)
    
    edit_btn.pack(side="left", pady=(2,0))
    
    
    # Commands -------------------------------------------- 
    cmd_btn = tk.Menubutton(frm_menubar_proper,
                            text="Cmd",
                            font = ck12,
                            fg= chi_fg, 
                            bg= chi_bg, 
                            activeforeground = chi_act_fg,
                            activebackground = chi_act_bg)
    
    cmd_btn.pack(side="left", pady=(2,0))
 
    
    """ Attach regular dropdown Menus to the Menubuttons.""" 
    apple_menu = tk.Menu(apple_btn, 
                            tearoff = False, 
                            font = ck12,
                            fg = chi_fg, 
                            bg = chi_bg, 
                            activeforeground = chi_act_fg, 
                            activebackground = chi_act_bg)
    
    file_menu = tk.Menu(file_btn, 
                            tearoff = False, 
                            font = ck12,
                            fg = chi_fg, 
                            bg = chi_bg, 
                            activeforeground = chi_act_fg, 
                            activebackground = chi_act_bg)
    
    edit_menu = tk.Menu(edit_btn,
                            tearoff = False,
                            font = ck12,
                            fg = chi_fg,
                            bg = chi_bg,
                            activebackground = chi_act_bg,
                            activeforeground = chi_act_fg)
                        
    cmd_menu = tk.Menu(cmd_btn,
                            tearoff = False,
                            font = ck12,
                            fg = chi_fg,
                            bg = chi_bg,
                            activebackground = chi_act_bg,
                            activeforeground = chi_act_fg)
                        
                        
    """ Populate the menus ('submenus') with appropriate commands. """   
        
    ### Apple ----------------------------------------------------------
    apple_menu.add_command(label = "About...", command = None)
    apple_menu.add_command(label = "Toggle Frameless", command = frame_set)     
    
    apple_btn.config(menu=apple_menu)
    
    apple_menu.bind('<Enter>', lambda btn: on_start_hover(apple_btn))
    apple_menu.bind('<Leave>', lambda btn: on_end_hover(apple_btn))


    ## File ------------------------------------------------------------
    file_menu.add_command(label ="New", accelerator=u'\u2318'"N", command = None)
    file_menu.add_command(label ="Open...", accelerator=u'\u2318'"O", command = None)
    file_menu.add_command(label ="Save", accelerator=u'\u2318'"S", command = None)
    file_menu.add_command(label ="Close", accelerator=u'\u2318'"S", command = window_closer)
    file_menu.add_separator()
    file_menu.add_command(label ="Quit", accelerator=u'\u2318'"Q", command=root.quit)
    
    file_btn.config(menu=file_menu)
    
    file_menu.bind('<Enter>', lambda btn: on_start_hover(file_btn))
    file_menu.bind('<Leave>', lambda btn: on_end_hover(file_btn))
    
    
    ## Edit ------------------------------------------------------------
    edit_menu.add_command(label = "Cut", accelerator=u'\u2318'"X", command = False)
    edit_menu.add_command(label = "Copy", accelerator=u'\u2318'"C", command = False)
    edit_menu.add_command(label = "Paste", accelerator=u'\u2318'"V", command = False)
    edit_menu.add_command(label = "Select All", accelerator=u'\u2318'"A", command = False)
    
    edit_btn.config(menu = edit_menu)
    
    edit_menu.bind('<Enter>',  lambda btn: on_start_hover(edit_btn))
    edit_menu.bind('<Leave>',  lambda btn: on_end_hover(edit_btn))
    
    
    ## Commands --------------------------------------------------------
    cmd_menu.add_command(label = "ls", command = lambda:basho('ls '))
    cmd_menu.add_command(label = "cd", command = lambda:basho('cd '))
    cmd_menu.add_command(label = "find", command = lambda:basho('find '))
    cmd_menu.add_command(label = "grep", command = lambda:basho('grep '))
    cmd_menu.add_command(label = "cp", command = lambda:basho('cp '))
    
    cmd_btn.config(menu = cmd_menu)
    
    cmd_menu.bind('<Enter>', lambda btn: on_start_hover(cmd_btn))
    cmd_menu.bind('<Leave>', lambda btn: on_end_hover(cmd_btn))
    

    
    """ Finally populate the sub-submenus proper too."""
    
    # Edit>Options ----------------------------------------
    sub_edit_menu = tk.Menu(edit_menu,
                        font = ck12,
                        fg = chi_fg,
                        bg = chi_bg,
                        tearoff = False,
                        activebackground = chi_act_bg,
                        activeforeground = chi_act_fg)
                                    
    sub_edit_menu.add_command(label = "Subadub", command = False)
    sub_edit_menu.add_command(label = "Yada", command = False)
    sub_edit_menu.add_command(label = "Nada", command = False)
    
    
    ## Edit ------------------------------------------------------------
    edit_menu.add_cascade( menu = sub_edit_menu, 
                                label = "Options ",
                                bitmap = None,
                                image = ii, 
                                compound = 'right')




    """ ====================  BODY BOTTOM FRAME  =======================
    """
    frm_bdy_bottom = tk.Frame(root, 
                        bg = chi_act_bg, 
                        highlightbackground = chi_act_bg, 
                        highlightthickness = 1,
#                         width = WW,
                        height = HH-headH )

    frm_bdy_bottom.place(relwidth = 1.0, relheight = 1.0, x = 0, y = headH) 


    
    """ =====================  BODY CANVAS  ============================
    """
    canv_bdy = tk.Canvas(frm_bdy_bottom, 
                        bg = chi_bg, 
                        highlightbackground = chi_act_bg, 
                        highlightthickness  = 0,
                        width = 0,
                        height = Hmax)
                        
    canv_bdy.pack(anchor=tk.N, 
                        side="left",
                        expand = True, 
                        fill = "both", pady=(0,headH))
                        
                        
    """ =====================  BODY TOP FRAME  =========================
    """
    frm_bdy_content = tk.Frame(canv_bdy, 
                        bg = chi_bg, 
                        highlightbackground = chi_act_bg, 
                        highlightthickness = 0,
                        height = Hmax)

    frm_bdy_content.pack(anchor = tk.N, expand = True, fill ="both") 
    frm_bdy_content.pack_propagate(True)
    
    
    root.update_idletasks()
    canvas_window = canv_bdy.create_window((0, headH), 
                                window=frm_bdy_content,
                                width=root.winfo_width(), 
                                anchor="nw")

    frm_bdy_content.bind("<Configure>",
                lambda e: canv_bdy.configure(scrollregion=canv_bdy.bbox("all")))
    
    frm_bdy_content.bind("<Configure>", on_frame_configure)
    canv_bdy.bind("<Configure>", on_canvas_configure)


    frm_bdy_content.bind('<Enter>', on_enter)   # bind wheel events when the cursor enters
    frm_bdy_content.bind('<Leave>', on_leave)   # unbind wheel events as the cursor exits

    on_frame_configure(None)  # do an initial stretch on render, pre resizing



    # Inject a number of dummy label widgets for testing:
#     import random
# #     a = [8, 24, 40 , 56]
#     for i in range(12):
# #         j=random.choice(a)
#         tk.Label(frm_bdy_content,
#                 bg=chi_act_bg , 
#                 fg=chi_act_fg, 
#                 text=f" Item {i+1}").pack(pady=5, anchor="center")



    """ =====================  SCROLLBAR  ==============================
    """
    scrollbar = kl.KL_vertical_scrollbar(root, canv_bdy)
    scrollbar.pack(padx=(0,0), 
                   pady=(headH+1,16), 
                   side=tk.RIGHT, 
                   fill=tk.Y)

    canv_bdy.configure(yscrollcommand=scrollbar.set)
    canv_bdy.bind("<Configure>", on_window_resize)


    """ =====================  SIZE-GRIP  ==============================
    """    
    root.style.element_create("CustomSizegrip.image", "image", sg)

    # Overwrite the default TSizegrip layout with our new gif:
    root.style.layout("TSizegrip", [
        ("CustomSizegrip.image", {"side": "bottom", "sticky": "se"})])
        
    sizegrip = ttk.Sizegrip(root)
    sizegrip.place(relx=1.0, rely=1.0, anchor="se")


    """ ================================================================
    """


    # Run
    root.mainloop()

# Start here!
setup_titled_menued_slate()





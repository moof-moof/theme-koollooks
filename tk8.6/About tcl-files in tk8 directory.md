
###Regarding some tcl files in the local tk directory.

The **tkfbox.tcl** file implements the Tk standard file selection dialog box (example below), used on unix-like platforms whenever the *tk_strictMotif* flag is not set.

The modified file provided here as part of the Koollooks theme would typically be located in **~/.local/share/tcltk/tk8.6/**. However this may not always be sufficient for it to be recognised properly. In such a case it should instead simply replace **/usr/share/tcltk/tk8.6/tkfbox.tcl** 

The modifications replace the default icon images for *fileImage*, *folderImage* and *updirImage* with images more appropriate for the Koollooks theme.



![ ](../meta/
askdirectory-dialogue.png )
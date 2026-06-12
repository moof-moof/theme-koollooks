if {[file isdirectory [file join $dir koollooks]]} {
    if {![catch {package require Ttk}]} {
        package ifneeded ttk::theme::koollooks 0.1 \
            [list source [file join $dir koollooks.tcl]]
    } elseif {![catch {package require tile}]} {
        package ifneeded tile::theme::koollooks 0.1 \
            [list source [file join $dir koollooks.tcl]]
    } else {
	return
    }
}


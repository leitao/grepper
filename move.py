import globvar
import tab

def move_left():
    globvar.clear_screen = True
    globvar.redraw = True

    # is the current tab the last one
    if tab.is_last_tab() and tab.get_current_tab().name == "Unfiltered":
        tab.delete_tab()
        return

    # Just go left
    tab.decrease_idx()


def move_right():
    globvar.clear_screen = True
    globvar.redraw = True

    # is the current tab the last one
    if tab.is_last_tab():
        # add a new one
        tab.add_new_tab()
        return

    # Just move
    tab.increase_idx()




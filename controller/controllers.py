from view.views import *

def get_passcode():
    flag = True
    while flag:
        passcode = get_passcode_view()
        if len(passcode) < 4:
            show_error_view(
                'Passcode should be at least 4 characters..... try again')
        else:
            flag = False

    return passcode

def get_passcode_view():
    
    print('Enter the passcode: ')
    passcode = input('Passcode: ').strip()

    return passcode

def show_message_view(msg):
    print(msg)

def show_error_view(err):
    print('\n' + str(err) + '\n')
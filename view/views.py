# ******************************************
#  Author : Ali Azhari
#  Created On : Mon Jul 01 2019
#  File : views.py
# *******************************************/

def prompt_passcode():
 
    passcode = input('Enter Passcode: ').strip()

    return passcode

def get_passcode_view(MIN_MAX):

    flag = True
    while flag:
        passcode = input('Enter Passcode: ').strip()
        if len(passcode) < MIN_MAX:
            show_error_view(
                'Passcode should be at least 4 characters..... try again')
        else:
            flag = False
    return passcode


def show_menu():
    print('Choose one of the following:')
    print('\t 1: Add email account')
    print('\t 2: Select email account')
    print('\t 3: Add folder/matching email eg: mail.com')
    print('\t 4: Add folder to server')
    print('\t 5: Synchronize folders')
    print('\t 6: Synchronize emails')
    print('\t 7: Quit')
    choice = input(': ')

    return choice

def add_account_menu():
    # the followings need to be validated

    name = input('Enter the name of this account: ')
    incoming = input('Enter the incoming server (eg: imap.gmail.com: ')
    outgoing = input('Enter the outgoing server (eg: smtp.gmail.com: ')
    email = input('Enter your email account (eg: name@mail.com: ')
    password = input('Enter your email password: ')

    new_account = [name, incoming, outgoing, email, password]

    return new_account

def select_account(accounts):
    if len(accounts) == 0:
        print('The list is empty')
        return None

    flag = True
    
    print('Select an account.')
    i = 1
    for row in accounts:
        print('\t ' + str(i) + ': ' + row[0])
        i += 1
    print('\t ' + str(i) + ': Back to previous menu')
       
    choice = int(input(': '))
    return choice

def get_folder_name():
    print('Folder name: ')
    folder_name = input(': ').strip()
    return folder_name

def get_matching_email():
    print('Matching email: eg: gmail.com: ')
    matching = input(': ').strip()
    return matching

def add_folder_server():
    print('Folder name: ')
    folder_name = input(': ').strip()

    return folder_name

def  prompt_to_add_folder_view(folder):
    answer = input('Do you want to add this folder \'' + folder + '\' to server, type !q to skip: ').strip()
    return answer

def show_message_view(err):
    print('\n' + str(err) + '\n')

def show_error_view(err):
    print('\n' + str(err) + '\n')



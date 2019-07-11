
# ******************************************
#  Author : Ali Azhari
#  Created On : Mon Jul 01 2019
#  File : app.py
# *******************************************/

import controller.controllers as ct
import view.views as vw

from utilities.passcode import Passcode
from utilities.errors import *

import os

MIN_PASS = 3
MAX_TRIAL = 3
accounts = []
account = []


def get_keysalt():

    count = 0
    flag = True
    global accounts
    while flag and count < MAX_TRIAL:
        try:
            passcode = ct.get_passcode(MIN_PASS)
            key_salt = Passcode(passcode)
            encrypted_accounts = ct.get_accounts()
            accounts = ct.decrypt_accounts(encrypted_accounts, key_salt)
            flag = False

        except InproperPasscodeException as ex:
            vw.show_error_view(
                'Your passcode should be at least 4 characters....')
        except FileNotFoundError as fex:
            flag = False
            vw.show_error_view(fex)
        except EmptyFileException as ex:
            flag = False
            vw.show_error_view(fex)
        except DecryptionException as decx:
            count += 1
            vw.show_error_view(decx)
        except Exception as ex:
            vw.show_error_view(ex)

    if count == 3:
        vw.show_error_view('Goodbye!!')
        exit()

    return key_salt


def main():
    global keysalt
    global account

    keysalt = get_keysalt()

    flag = True

    while flag:
        try:
            choice = vw.show_menu()
            if choice == '1':
                accounts.append(ct.add_account(keysalt))

            elif choice == '2':
                account = ct.select_account(accounts)
            elif choice == '3':
                ct.add_folder_to_disk(account)
            elif choice == '4':
                ct.add_folder_to_server(account)
            elif choice == '5':
                ct.synchronize(account)
            elif choice == '6':
                ct.synchronize_emails(account)
            elif choice == '7':
                print('Goodbye')
                quit()
            else:
                vw.show_error_view('Invalid Entry..... try again!')
        except EmptyListException as emx:
            vw.show_error_view(emx)
        except NoAccountException as naex:
            vw.show_error_view(naex)
        except PassException:
            pass
        except Exception as ex:
            
            vw.show_error_view(ex)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')

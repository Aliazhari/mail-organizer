# ******************************************
#  Author : Ali Azhari
#  Created On : Mon Jul 01 2019
#  File : controllers.py
# *******************************************/

from utilities.crypt import Crypt
from utilities.passcode import Passcode
from utilities.errors import *

import model.accounts as ct
import model.folders as fd
import view.views as vw

from utilities.imap_client import *

import os
import time

# *******************************************/

def get_passcode(MIN_PASS):

    passcode = vw.prompt_passcode()
    if len(passcode) < 4:
        raise InproperPasscodeException('Inproper Password!')

    return passcode

# *******************************************/

def add_account(keysalt):
    account_encrypted = []
    account = vw.add_account_menu()
    crypt = Crypt(keysalt.key, keysalt.salt)
    for field in account:
        account_encrypted.append(crypt.encrypt(field))
    ct.Accounts.add_account(account_encrypted)
    vw.show_message_view('Account {} has been added.'.format(account[0]))

    return account

# *******************************************/

def get_accounts():
    try:
        accounts = ct.Accounts.get_accounts()
        if len(accounts) == 0:
            raise EmptyFileException('No account exists..')
    except FileNotFoundError as fex:
        raise FileNotFoundError(fex)
    except EmptyFileException as emx:
        raise FileNotFoundError(emx)
    except Exception as ex:
        raise Exception(ex)

    return accounts

# *******************************************/

def select_account(accounts):
    length = len(accounts)
    if length == 0:
        raise EmptyListException('Can\' select. No account is registered yet')

    active_account = []
    flag = True
    while flag:
        active_account = []
        index = vw.select_account(accounts)

        if index in range(1, length + 1):
            active_account = accounts[index-1]
            vw.show_message_view(
            'The account {} -----> {} is active'.format(active_account[0], active_account[3]))
            flag = False
        elif index == length + 1:
            flag = False
            raise PassException('')
        else:
            vw.show_error_view(
            'Invalid entry.... try again')
    
    return active_account

# *******************************************/
def save_folder_to_disk(account, folder, domain):

    try:
        fd.Folders.add_folder([account, folder, domain])
        vw.show_message_view('Folder {} has been added for the account {}.'.format(folder, account))
    except Exception as ex:
        vw.show_error_view(ex)

def add_folder_to_disk(account):
    length = len(account)
    if length == 0:
        raise NoAccountException('No account is active. You need to select an account.')
    
    try:
        folder = vw.get_folder_name()
        domain = vw.get_matching_email()
        acc = account[3]
        save_folder_to_disk(acc, folder, domain)
    except Exception as ex:
        vw.show_error_view(ex)

# *******************************************/

def initialize_imap(account, password, server):
    return ImapClient(account, password, server)

# *******************************************/

def add_folder_to_server(account, folder=None):
    length = len(account)
    if length == 0:
        raise NoAccountException('No account is active. You need to select an account.')
    try:
        if folder is None:
            folder = vw.add_folder_server()
        imap = initialize_imap(account[3], account[4], account[1])
        imap.login()
        imap.create_folder(folder)
    except Exception as ex:
        raise Exception(ex)

# ******************************************* /

def decrypt_accounts(accounts, keysalt):
    try:
        crypt = Crypt(keysalt.key, keysalt.salt)
        decrypted_accounts = []
        for account in accounts:
            aRow = []
            for field in account:
                aRow.append(crypt.decrypt(field))
            decrypted_accounts.append(aRow)
    except DecryptionException as dex:
        raise DecryptionException(dex)

    return decrypted_accounts

# ******************************************* /

def get_local_folders(account):
    """[summary]
    
    Arguments:
        account {[type]} -- [description]
    
    Returns:
        folders as set and dictionary: keys are folders names in lower case, 
        values are folders names as entered originally
    """
    folders_dict = {}
    accts = fd.Folders.get_folders(account[3])  # get raw data from disk folder.csv
    for acc in accts:
        folders_dict[acc[1].lower()] = acc[1]

    folders_set = set()
    for key, _ in folders_dict.items():
        folders_set.add(key)

    return folders_dict, folders_set

# ******************************************* /

def get_folders_as_dict(account):
    folders_dict = {}
    accts = fd.Folders.get_folders(account)  # get raw data from disk folder.csv
    for acc in accts:
        folders_dict[acc[2].lower()] = acc[1]

    return folders_dict

def get_remote_folders(account):
    imap = initialize_imap(account[3], account[4], account[1])
    imap.login()
    folders = imap.get_folders()

    folders_set_temp = set()
    for item in folders[1]:
        folders_set_temp.add((item.split()[2].decode("utf-8")))

    folders_dict = {}
    folders_set = set()
    for folder in folders_set_temp:
        folders_dict[folder.lower()] = folder
        folders_set.add(folder.lower())

    return folders_dict, folders_set


# ******************************************* /
def synchronize(account):
    length = len(account)
    if length == 0:
        raise NoAccountException('No account is active. You need to select an account.')

    try:
        # get folders from disk  as dict and set
        lfolders_dict, lfolders_set = get_local_folders(account)
        
        # get folders from server as dict and set
        rfolders_dict, rfolders_set = get_remote_folders(account)

        vw.show_message_view('Synchronizing local folders...')
        folders_from_remote = rfolders_set - lfolders_set

        if len(folders_from_remote) == 0:
            vw.show_message_view('The local folders are up to date.')
        else:
            for folder in folders_from_remote:
                vw.show_message_view('Enter a matching domain for folder: ' + folder)
                matching = vw.get_matching_email()
                if not matching:
                    continue
                if matching == '!q':
                    break
                save_folder_to_disk(account[3], folder, matching)

        vw.show_message_view('Synchronizing remote folders...')
        folders_from_local = lfolders_set - rfolders_set
        if len(folders_from_local) == 0:
            vw.show_message_view('The remote folders are up to date.')

        for folder in folders_from_local:
            answer = vw.prompt_to_add_folder_view(lfolders_dict[folder])
            if not answer:
                continue
            if answer == '!q':
                break
            if answer == 'y':
                add_folder_to_server(account, lfolders_dict[folder])
                vw.show_message_view('{} is added to server. '.format(folder))


    except Exception as ex:
        raise Exception(ex)

def get_messages_from_server(imap, folder='Inbox', matching=''):
    
    return imap.get_messages(folder, matching)

# ******************************************* /
def synchronize_emails(account):
    length = len(account)
    if length == 0:
        raise NoAccountException('No account is active. You need to select an account.')

    imap = initialize_imap(account[3], account[4], account[1])
    imap.login()
    emails = get_messages_from_server(imap, 'Inbox', 'walmart.com')

    folders_dict = get_folders_as_dict(account[3])

    i = 1
    for email in emails:
        # print(i, email)
        i = i+1

    for email in emails:
       
        
        domain = email[3].split('@')[1]
        # last_dot = domain.rfind('.')
        # domain = domain[:last_dot]
        # domain_words = domain.split('.')
        # domain_length = len(domain_words)
        # domain = domain_words[domain_length - 1].lower()

        if domain in folders_dict:
            print(email)
            imap.copy_to_folder(email[0], folders_dict[domain])
            print('Email {} from {} has been moved to folder {}'.format(email[0], email[3], folders_dict[domain]))
            time.sleep(2)
        # else:
        #     print('{} does not have a folder'.format(domain))

        


        






# def get_emails(keysalt):

#     try:
#         Emails.initialization()

#         emails = Emails.get_emails()

#         crypt = Crypt(keysalt.key, keysalt.salt)
#         crypted_emails = []
#         for row in emails:
#             aRow = []
#             for field in row:
#                 aRow.append(crypt.decrypt(field))
#             crypted_emails.append(aRow)
#     except FileNotFoundError as ex:
#         raise FileNotFoundError(ex)
#     except:
#         raise Exception

#     return crypted_emails

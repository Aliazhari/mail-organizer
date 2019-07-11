# ******************************************
#  Author : Ali Azhari
#  Created On : Mon Jul 01 2019
#  File : accounts.py
# *******************************************/

import csv
import os


class Accounts:

    ACCOUNTS_FILENAME = 'accounts.csv'
    FOLDERS_FILENAME = 'folders.csv'

# ************************************************* /
    @staticmethod
    def get_accounts():
        accounts = []
        try:
            with open(Accounts.ACCOUNTS_FILENAME, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row is not None and len(row) != 0:
                        accounts.append(row)

        except FileNotFoundError as ex:
            raise FileNotFoundError(ex)
        except Exception as e:
            raise Exception(e)

        return accounts

# *************************************************/

    @staticmethod
    def add_account(account):
        try:
            with open(Accounts.ACCOUNTS_FILENAME, 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(account)
                csv_file.flush()
                os.fsync(csv_file.fileno())
        except:
            raise Exception('Error occured while adding new account')


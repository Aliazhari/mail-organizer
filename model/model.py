# ******************************************
#  Author : Ali Azhari
#  Created On : Sat Jun 29 2019
#  File : model.py
# *******************************************/

import csv
import os


class Emails:

    EMAIL_FILENAME = 'accounts.csv'
    FOLDERS_FILENAME = 'folders.csv'
    email_accounts = []

    @staticmethod
    def initialization():
        Emails.email_accounts = []
        try:
            with open(Emails.EMAIL_FILENAME, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row is not None and len(row) != 0:
                        Emails.email_accounts.append(row)

        except FileNotFoundError as ex:
            raise FileNotFoundError(ex)
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def add(account):
        try:
            with open(Emails.EMAIL_FILENAME, 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(account)
                csv_file.flush()
                os.fsync(csv_file.fileno())
                Emails.email_accounts.append(account)
        except:
            raise Exception('Error in model/Emails/add')

    @staticmethod
    def get_emails():
        return Emails.email_accounts

    @staticmethod
    def add_folder(row):
        try:
            with open(Emails.FOLDERS_FILENAME, 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(row)
                csv_file.flush()
                os.fsync(csv_file.fileno())
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_folders(account):
        folders = []
        try:
            with open(Emails.FOLDERS_FILENAME, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row is not None and len(row) != 0:
                        if account in row[0]:
                            folders.append(row)
            return folders

        except FileNotFoundError as ex:
            raise ex
        except Exception as e:
            raise Exception(e)

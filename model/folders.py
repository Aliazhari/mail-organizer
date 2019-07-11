# ******************************************
#  Author : Ali Azhari 
#  Created On : Thu Jul 04 2019
#  File : folders.py
# *******************************************/


import csv
import os


class Folders:

    FOLDERS_FILENAME = 'folders.csv'

# ************************************************* /
    @staticmethod
    def get_folders(account):
        folders = []
        try:
            with open(Folders.FOLDERS_FILENAME, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row is not None and len(row) != 0:
                        folders.append(row)

        except FileNotFoundError as ex:
            raise FileNotFoundError(ex)
        except Exception as e:
            raise Exception(e)

        return folders

# *************************************************/

    @staticmethod
    def add_folder(account):
        try:
            with open(Folders.FOLDERS_FILENAME, 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(account)
                csv_file.flush()
                os.fsync(csv_file.fileno())
        except:
            raise Exception('Error occured while adding new account')


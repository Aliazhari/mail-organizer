# ******************************************
#  Author : Ali Azhari 
#  Created On : Sat Jun 29 2019
#  File : passcode.py
# *******************************************/

class Passcode:
    """Class Account creates mail account with its passcode for encryption."""

    MAX = 16

    def __init__(self, passcode):
        length = len(passcode)
        if length < self.MAX:
            xtra = '*' * (self.MAX - length)
            self.key = passcode + xtra
            self.salt = passcode + xtra
        else:
            self.key = passcode[:self.MAX]
            self.salt = passcode[:self.MAX]
# ******************************************
#  Author : Ali Azhari 
#  Created On : Sun Jun 30 2019
#  File : errors.py
# *******************************************/

class InproperPasscodeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class EmptyFileException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class EncryptionException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class DecryptionException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class EmptyListException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class PassException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        
class NoAccountException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class EmptySetException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class NoUpdateException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class ConnectionException(Exception):
    def __init__(self, msg):
        super().__init__(msg)



class LoginException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class CreateFolderException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
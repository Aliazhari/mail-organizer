# ******************************************
#  Author : Ali Azhari 
#  Created On : Sun Jun 30 2019
#  File : config.py
# *******************************************/

import json

class Config:
    FILENAME = 'config.dat'

    @staticmethod
    def get_config():
        try:
            with open(Config.FILENAME) as json_file:
                data = json.load(json_file)
        except FileNotFoundError as fex:
            raise FileNotFoundError(fex)
        return data

    @staticmethod
    def save_config(data):
        try:
            with open(Config.FILENAME, 'w') as outfile:  
                json.dump(data, outfile)
        except FileNotFoundError as fex:
            raise fex
        except Exception as ex:
            raise ex



# data['people'].append({  
#     'name': 'Larry',
#     'website': 'google.com',
#     'from': 'Michigan'
# })


# ******************************************
#  Author : Ali Azhari 
#  Created On : Fri Jul 05 2019
#  File : imap_client.py
# *******************************************/


import datetime
import email
import email.header
import imaplib
import sys

import re

from utilities.errors import *

pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')


class ImapClient:
    imap = None

    def __init__(self,
                 recipient,
                 passwd,
                 server,
                 use_ssl=True,
                 move_to_trash=True):
        # check for required param
        if not recipient:
            raise ValueError('You must provide a recipient email address')
        if not passwd:
            raise ValueError('You must provide email address password')
        self.recipient = recipient
        self.passwd = passwd
        self.use_ssl = use_ssl
        self.move_to_trash = move_to_trash
        self.recipient_folder = 'inbox'
        # instantiate our IMAP client object
        try:
            if self.use_ssl:
                self.imap = imaplib.IMAP4_SSL(server)
            else:
                self.imap = imaplib.IMAP4(server)
        except Exception:
            raise ConnectionException("Connection error: Make sure you are connected to the Internet")

    def login(self):
        try:
            rv, data = self.imap.login(self.recipient, self.passwd)
            return rv, data
        except (imaplib.IMAP4_SSL.error, imaplib.IMAP4.error) as err:
            raise LoginException('Login failed: Check your login credentials')

    def get_folders(self):
        return self.imap.list()

    def create_folder(self, folder):
        try:
            self.imap.create(folder)
        except:
            raise CreateFolderException('Create folder: error')

    def folder_exists(self, folder):
        """Return ``True`` if *folder* exists on the server.
        """
        return len(self.imap.list_folders("", folder)) > 0

    def logout(self):
        self.imap.close()
        self.imap.logout()

    def close(self):
        self.imap.close()

    def select_folder(self, folder):
        """
        Select the IMAP folder to read messages from. By default
        the class will read from the INBOX folder
        """
        self.recipient_folder = folder

    # def getmsg(self):
    #     T = time.time()
    #
    #     self.imap.select(self.recipient_folder)
    #     typ, data, string = self.imap.search(None, 'UNSEEN SINCE T')
    #     print(string)
    #     for num in string.split(data[0]):
    #         try:
    #             typ, data = self.imap.fetch(num, '(RFC822)')
    #             msg = email.message_from_string(data[0][1])
    #             print(msg["From"])
    #             print(msg["Subject"])
    #             print(msg["Date"])
    #         except:
    #             print('error')

    def parse_uid(self, data):
        match = pattern_uid.match(data)
        return match.group('uid')

    def move_to_folder(self, uid, folder):
        result = self.imap.uid('MOVE', uid, folder)
        self.imap.store()
        return result

    def copy_to_folder(self, uid, folder):
        self.imap.store(uid, '-FLAGS', r'(\SEEN)')
        self.imap.copy(uid, folder)
        self.imap.store(uid, '+FLAGS', r'(\Deleted)')

        
        
        
        

    def get_messages(self, folder, matching):
        """
        Scans for email messages from the given sender and optionally
        with the given subject

        :param matching:
        :param sender Email address of sender of messages you're searching for
        :param subject (Partial) subject line to scan for
        :return List of dicts of {'num': num, 'body': body}
        """
        # if not sender:
        #     raise ValueError('You must provide a sender email address')

        # select the folder, by default INBOX
        resp, _ = self.imap.select(folder)
        if resp != 'OK':
            print(f"ERROR: Unable to open the {folder} folder")
            sys.exit(1)

        messages = []

        date = (datetime.date.today() - datetime.timedelta(2)).strftime("%d-%b-%Y")

        mbox_response, msgnums = self.imap.search(None, '(SENTSINCE {0}) SEEN'.format(date))
      
        if mbox_response == 'OK':

            i = 1
            for num in msgnums[0].split():
                retval, rawmsg = self.imap.fetch(num, '(RFC822)')

                if retval != 'OK':
                    print('ERROR getting message', num)
                    continue
                msg = email.message_from_bytes(rawmsg[0][1])
                msg_from = email.utils.parseaddr(msg['From'])
                msg_subject = msg["Subject"]
                msg_date = msg['Date']
                msg_uid = msg['UID']

                # messages.append([num.decode('utf-8'), msg_uid, msg_date, msg_from[1], msg_subject])
                messages.append([num, msg_uid, msg_date, msg_from[1], msg_subject])

                # print(msg['Date'], msg_from, msg_subject[0])

                # print(msg_from[1])
                # print(i, num, msg_uid, msg_date, msg_from[1], msg_subject)
                
                # if matching in msg_from[1]:
                
                    # print('*****************************************************')
                    # print(str(i), num.decode('utf-8'), msg_date, msg_from)
                    # i = i + 1

                    # self.imap.copy(num.decode('utf-8'), 'Galaxy')
                    # self.imap.store(num.decode('utf-8'), '+FLAGS', '\\Deleted')

                    # print(result)

                    # body = ""
                    # if msg.is_multipart():
                    #
                    #     for part in msg.walk():
                    #         type = part.get_content_type()
                    #         disp = str(part.get('Content-Disposition'))
                    #         # look for plain text parts, but skip attachments
                    #         if type == 'text/plain' and 'attachment' not in disp:
                    #             charset = part.get_content_charset()
                    #
                    #             # decode the base64 unicode bytestring into plain text
                    #             body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                    #             # if we've found the plain/text part, stop looping thru the parts
                    #             break
                    # else:
                    #     print(msg.is_multipart())
                    #     # not multipart - i.e. plain text, no attachments
                    #     charset = msg.get_content_charset()
                    #     body = msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                    # messages.append({'num': num, 'body': body})
        
        return messages

    def delete_message(self, msg_id):
        if not msg_id:
            return
        if self.move_to_trash:
            # move to Trash folder
            self.imap.store(msg_id, '+X-GM-LABELS', '\\Trash')
            self.imap.expunge()
        else:
            self.imap.store(msg_id, '+FLAGS', '\\Deleted')
            self.imap.expunge()



import imaplib
import email
import os
import time
import requests

"""
Leave one email with given subject and do not remove it! Leave it unread. 
"""


class Mailer:
    def __init__(self):
        self.response = None
        self.messages = None
        self.last_subject = "DO NOT REMOVE"
        self.username = "username"
        self.password = "password"
        self.webhook = "webhook_url"
        try:
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.result = self.imap.login(self.username, self.password)
        except Exception as e:
            print(f"Exception occurred: {e}")
            time.sleep(2)
            try:
                requests.post(self.webhook, data=f"**ERROR : ** {e}")
            except Exception as e:
                exit(f"Exception occurred: {e}")

    def checkMail(self):
        self.imap.select('Inbox', True)
        self.response, self.messages = self.imap.search(None, "UnSeen")
        self.messages = self.messages[0].split()
        self.messages = list(map(int, self.messages))
        return self.messages[-1]

    def sendInfo(self):
        count = 0
        while True:
            try:
                latest_email_number = self.checkMail()
            except Exception as e:
                print(f"Exception occurred: {e}")
                time.sleep(2)
                try:
                    requests.post(self.webhook, data=f"**ERROR : ** {e}")
                except Exception as e:
                    exit(f"Exception occurred: {e}")

            res, msg = self.imap.fetch(str(latest_email_number - count), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    if msg["Subject"] == self.last_subject:
                        print(self.last_subject + " is the last new email. Finishing now")
                        return
                    else:
                        subject = make_header(decode_header(msg["Subject"]))
                        sender = str(make_header(decode_header(msg["From"]))).replace('"', '')
                        print(f'FROM: {sender} \t SUBJECT: {subject}'.expandtabs(70))
                        payload = f"**FROM: {sender}** \\nSUBJECT: {subject}"
                        time.sleep(2)
                        try:
                            requests.post(self.webhook, data=payload)
                        except Exception as e:
                            print(f"Exception occurred: {e}")
                            pass
                        count = count + 1


notify = Mailer()
notify.sendInfo()

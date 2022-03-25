import imaplib
import email
import os
import re
import time
import requests

"""
Leave one email with given subject and do not remove it! Leave it unread. 
"""


def getFiles():
    if os.path.isfile('discord.sh'):
        print("File 'discord.sh' already exists. Proceeding...")
    else:
        filename = "discord.sh"
        url = 'https://raw.githubusercontent.com/ChaoticWeg/discord.sh/master/discord.sh'
        f = requests.get(url)
        open(filename, 'wb').write(f.content)
        os.popen('chmod +x discord.sh').read()
        print("File 'discord.sh' downloaded. Proceeding...")
    if os.path.isfile('.webhook'):
        print(".webhook file fund! Proceeding...")
    else:
        exit("No .webhook file. Create one with webhook url inside.")
    return


class Mailer:
    def __init__(self):
        self.response = None
        self.messages = None
        self.last_subject = "DO NOT REMOVE"
        self.username = "username"
        self.password = "password"
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.result = self.imap.login(self.username, self.password)

    def checkMail(self):
        self.imap.select('Inbox', True)
        self.response, self.messages = self.imap.search(None, "UnSeen")
        self.messages = self.messages[0].split()
        self.messages = list(map(int, self.messages))
        return self.messages[-1]

    def sendInfo(self):
        count = 0
        while True:
            latest_email_number = self.checkMail()
            res, msg = self.imap.fetch(str(latest_email_number - count), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    if msg["Subject"] == self.last_subject:
                        print(self.last_subject + " is the last new email. Finishing now")
                        return
                    else:
                        # msg_email = re.findall(r"\<(.*?)\>", msg["From"])
                        # print(f'OD: {msg_email} Subject: {msg["Subject"]}')
                        sender = make_header(decode_header(msg["From"]))
                        subject = make_header(decode_header(msg["Subject"]))
                        print(f'FROM: {sender} \t SUBJECT: {subject}'.expandtabs(70))

                        command = f'./discord.sh \
                                    --username "Username" \
                                    --avatar "https://avatarlink.com/logo.png" \
                                    --text "**FROM: {sender}** \\nSUBJECT: {subject}"'

                        time.wait(1)
                        os.popen(command)
                        count = count + 1


getFiles()
notify = Mailer()
notify.sendInfo()

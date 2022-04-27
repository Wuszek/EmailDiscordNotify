# EmailDiscordNotify
This is simple tool, to automatically check for new email on mailbox and send 
notifications to Discord channel. It could be usefull to watch over some spam/old account, that
you do not want to connect to private mailbox/outlook/phone.

## How to use 

### Install required dependencies

```bash
pip3 install imaplib email os re time requests
```
or something like this ;) 

### Change init settings
 ```python 
 def __init__(self):
    self.response = None
    self.messages = None
    self.last_subject = "DO NOT REMOVE"
    self.username = "username"
    self.password = "password"
    self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
    self.result = self.imap.login(self.username, self.password)
``` 
- You need to leave one email onopen and unread with given title, eg. above: "DO NOT REMOVE".
- Fill rest of settings with username, password and your mailbox imap address.
- Script will check for unread emails everytime from the top of mailbox and stop on setu-up last subject.

### Create .webhook file 
- Create bot and webhook no Discord channel.
- Create `.webhook` file and fill it with webhook url.

### Update Discord bot command 
``` python
command = f'./discord.sh \
            --username "Bot username" \
            --avatar "Bot avatar link" \
            --text "**FROM: {sender}** \\nSUBJECT: {subject}"'
```
### Run script

It would be pointless to run it manually! Script has no loop, so it should be run 
periodically using built-in scheduler (e.g. cron).
```bash
sudo apt update
sudo apt install cron -y
sudo systemctl enable cron
crontab -e
```
fill crontab to run every week:
```bash
0 0 * * 0 /usr/bin/python3 /path/to/file/main.py /path/to/file/logger.log
```

More on how to use crontab: [click](https://www.jcchouinard.com/python-automation-with-cron-on-mac/)

# EmailDiscordNotify
This is simple tool, to automatically check for new email on mailbox and send 
notifications to Discord channel. It could be useful to watch over some spam/old account, that
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
    self.last_subject = "DO NOT REMOVE"
    self.username = "username"
    self.password = "password"
    self.webhook = "webhook_url"
    self.bot_username = "Username"
    self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
    self.result = self.imap.login(self.username, self.password)
``` 
- You need to leave one email onopen and unread with given title, eg. above: "DO NOT REMOVE".
- Fill rest of settings with username, password and your mailbox imap address.
- Script will check for unread emails everytime from the top of mailbox and stop on setu-up last subject.

### Create discord bot and update webhook constant 
- Create bot and webhook on Discord channel.
- Update webhook constant in main.py.

### Update Discord bot command 
``` python
content = f"**FROM: {sender}** \nSUBJECT: {subject}"
payload = {'username': 'Username', "content": {content}}
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

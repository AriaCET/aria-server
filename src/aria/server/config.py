import os
asteriskconf='/etc/asterisk'

HOME = os.getenv("HOME")
default_path = os.path.join(HOME, '.aria')
DB_path = os.path.join(default_path,"ariaDB")

clientConf = os.path.join(asteriskconf,'sip.conf')
channelConf = os.path.join(asteriskconf,'extensions.conf')

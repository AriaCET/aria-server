import os
asteriskconf='/tmp'
default_path = "aria"

DB_path = os.path.join(default_path,"ariaDB")

clientConf = os.path.join(asteriskconf,'sip.conf')
channelConf = os.path.join(asteriskconf,'extensions.conf')

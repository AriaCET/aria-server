import os
asteriskconf='/etc/asterisk'
default_path = os.getenv('HOME')

DB_path = os.path.join(default_path,".ariaDB")

clientConf = os.path.join(asteriskconf,'sip.conf')
channelConf = os.path.join(asteriskconf,'extentions.conf')

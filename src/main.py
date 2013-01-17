#!/usr/bin/env python2

import aria

HOST = '127.0.0.1'
PORT = 5000
DEBUG = False

aria.app.config.from_object(__name__)
aria.app.run(host=HOST,port=PORT)

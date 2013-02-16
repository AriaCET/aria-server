#!/usr/bin/env python2

import aria


HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

aria.app.config.from_object(__name__)
aria.app.run(host=HOST,port=PORT)

#!/usr/bin/env python2


from aria import accs_control
if accs_control.create_key():
    print "Key created sucessfully."
else:
    print "Null length input forund! - Not updating"

import os, re
from popen2 import Popen3
from populous.messaging.concierge.exceptions import ConciergeError

CONCIERGE_DAEMON    = '/home/code/concierge'
CONCIERGE_PID       = '/usr/local/var/run/concierge.pid'
CONCIERGE_DBUS      = '/usr/local/var/run/concierge.dbus'

DBUS_ADDRESS_RE = re.compile("DBUS_SESSION_BUS_ADDRESS='([\S^']*)'")

def start_dbus():
    try:
        # Launch dbus and get address
        dbus_info = os.popen('dbus-launch --sh-syntax')
        dbus_address = DBUS_ADDRESS_RE.findall(dbus_info.read())[0]
        
        # Set the eviron variable for dbus
        os.environ['DBUS_SESSION_BUS_ADDRESS'] = dbus_address
        
        # Save the dbus address to file
        dbus_address_file = open(CONCIERGE_DBUS, 'w')
        dbus_address_file.write(dbus_address)
        dbus_address_file.close()
    except:
        raise ConciergeError('Could not start Concierge.  There was an error with dbus.')

def setup_dbus():
    # Get dbus address and set it
    dbus_address = open(CONCIERGE_DBUS, 'r').readline()
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = dbus_address

def start_concierge():
    try:
        p = Popen3('exec %s' % CONCIERGE_DAEMON)
        f = open(CONCIERGE_PID, 'w')
        f.write(str(p.pid))
        f.close()
    except:
        raise ConciergeError('Could not start Concierge.  There was an error with the concierge daemon.')

def stop_concierge():
    try:
        pid = open(CONCIERGE_PID, 'r').readline()
        os.kill(int(pid), 9)
    except:
        raise ConciergeError('Could not stop Concierge.')
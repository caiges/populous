import os
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

CONCIERGE_DBUS      = '/usr/local/var/run/concierge.dbus'

def setup_dbus():
    # Get dbus address and set it
    dbus_address = open(CONCIERGE_DBUS, 'r').readline()
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = dbus_address

setup_dbus()
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

def received_im_msg_cb(account, sender, message, conversation, flags):
    conv = purple.PurpleFindConversationWithAccount(1, sender, account)
    im = purple.PurpleConvIm(conv)
    stories = Story.objects.count()
    purple.PurpleConvImSend(im, 'I found %d stories' % stories)
    print sender, "said:", purple.PurpleMarkupStripHtml(message)

bus.add_signal_receiver(received_im_msg_cb,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

os.environ['DJANGO_SETTINGS_MODULE'] = 'kerckhoffproject_demo.settings'
from populous.news.models import Story

loop = gobject.MainLoop()
loop.run()


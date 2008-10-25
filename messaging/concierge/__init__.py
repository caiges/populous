from django.db.models import signals
from populous.messaging import models as messaging_app

def get_prpl_protocols(app, **kwargs):
    from popen2 import popen2
    from populous.messaging.concierge.connection import CONCIERGE_DAEMON_DIR
    from populous.messaging.models import IMProtocol
    try:
        protocols = popen2('%sconcierge -p' % CONCIERGE_DAEMON_DIR)[0].read()
        protocols_created = 0
        existing_protocols = 0
        for data in protocols.split('\n')[:-1]:
            info = eval(data)
            p, created = IMProtocol.objects.get_or_create(
                protocol_id=info['id'],
                name=info['name'],
                summary=info['summary'],
                description=info['description']
            )
            if created:
                protocols_created += 1
            else:
                existing_protocols += 1
        print "Added %d IM protocols, %d already exist." % (protocols_created, existing_protocols)
    except:
        print "No IM protocols added!"

signals.post_syncdb.connect(get_prpl_protocols, sender=messaging_app)
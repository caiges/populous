import sys, os, time

from django.core.management.base import BaseCommand
from populous.messaging.concierge.connection import start_dbus, start_concierge, stop_concierge

class Command(BaseCommand):
    
    pid_file = "%s/concierge.pid" % os.getcwd()
    
    def __get_pid(self):
        if os.path.exists(pid_file):
            return pid_file
        else:
            return None
    
    def __main(self):
        from populous.concierge.server import IMServer
        #TODO: setup a socket server to listen for incoming requests
        IMServer.start()
        while 1:
            time.sleep(1)
    
    def __start(self):
        from django.conf import settings
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError, e: 
            print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork()
            if pid > 0:
                # pid_file = self.__get_pid()
                # exit from second parent, print eventual PID before
                print "Concierge PID %d" % pid
                print "Saving PID to %s" % self.pid_file
                
                f = open(self.pid_file, 'w')
                f.write(str(pid))
                f.close()
                
                sys.exit(0) 
        except OSError, e: 
            print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
            sys.exit(1)
        
        self.__main()

    def __stop(self):
        from signal import SIGTERM
        f = open(self.pid_file, 'r')
        pid = int(f.readline())
        f.close()
        os.kill(pid, SIGTERM)
        print "Concierge stopped\n"
        os.remove(self.pid_file)
                
    def handle(self, *args, **options):
        if len(args) > 0:
            command = args[0]
        
            if command == 'start':
                #self.__start()
                print "Starting dbus"
                start_dbus()
                print "Starting concierge"
                start_concierge()
                
            
            elif command == 'stop':
                #self.__stop()
                print "Stopping concierge"
                stop_concierge()
            
            elif command == 'cwd':
                print os.getcwd()
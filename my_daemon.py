import time
from daemon3x import daemon
import signal, sys, os, syslog
import tarfile
import datetime


daemon_instance= None
path_for_backups = "/home/ms_lilibeth/"
def handler_SIGUSR1(signum, frame):
    global daemon_instance
    try:
        dt = datetime.datetime.now()
        dt_str = dt.strftime("%d %m %Y %H:%M")
        dt_str = dt_str.replace(" ","_")
        filename = path_for_backups + "backup_" + dt_str + '.tar.gz'
        syslog.syslog("Daemon: file_to_compress: %s" % daemon_instance.file_to_compress)
        with tarfile.open(filename, 'w:gz') as tar:
            tar.add(daemon_instance.file_to_compress,arcname=os.path.basename(daemon_instance.file_to_compress))
        daemon_instance.compressed.append(filename)
        str_tmp = "Daemon: backup made: " + filename
        syslog.syslog(str_tmp)
    except:
        e = sys.exc_info()
        syslog.syslog("Daemon Error: %s \n %s \n %s" % (e[0], e[1], e[2]))
def handler_SIGUSR2(signum, frame):
    try:
        if len(daemon_instance.compressed) == 0:
            syslog.syslog("Daemon: no backups available.")
            return
        filename = ''
        while filename == '' and len(daemon_instance.compressed) != 0:
            if os.path.exists(daemon_instance.compressed[-1]):
                filename = daemon_instance.compressed[-1]
            else:
                daemon_instance.compressed = daemon_instance.compressed[:-1]
        if filename == '':
            syslog.syslog("Daemon: no backups available.")
            return
        with tarfile.open(filename,'r:gz') as tar:
            tar.extractall(path=daemon_instance.compressed_from)
            syslog.syslog("Daemon: files extracted")
    except:
        e = sys.exc_info()
        syslog.syslog("Daemon Error: %s \n %s \n %s" % (e[0], e[1], e[2]))

class MyDaemon(daemon):
        def __init__(self, pidfile):
            daemon.__init__(self,pidfile)
            self.file_to_compress = None
            self.compressed = []
            self.compressed_from = ''
        def run(self):
            signal.signal(signal.SIGUSR1, handler_SIGUSR1)
            signal.signal(signal.SIGUSR2, handler_SIGUSR2)
            daemon_instance.compressed_from = os.path.dirname(daemon_instance.file_to_compress)
            syslog.syslog("Daemon: run")
            while(True):
                time.sleep(10)

if __name__ == "__main__":
        if len(sys.argv) == 1:
            raise Exception("Pass the file/folder path(s) as the argument, please")
        if len(sys.argv) > 2:
            raise Exception("Backup of only 1 file|dir is available")
        tmp = path_for_backups + "daemon.pid"
        daemon_instance = MyDaemon(tmp)
        daemon_instance.file_to_compress = sys.argv[1]
        daemon_instance.start()

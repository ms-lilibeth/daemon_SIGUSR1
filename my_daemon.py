import time
from daemon3x import daemon
import signal, sys

daemon_instance= None

def handler(signum, frame):
    global daemon_instance
    # daemon_instance.RestoreStandard()
    sys.stdout("SIGUSR1")
    daemon_instance.stop()

class MyDaemon(daemon):
        def run(self):
            signal.signal(signal.SIGUSR1, handler)
            while(True):
                time.sleep(10)

if __name__ == "__main__":
        daemon_instance = MyDaemon('home/ms_lilibeth/daemon-example.pid')
        daemon_instance.start()

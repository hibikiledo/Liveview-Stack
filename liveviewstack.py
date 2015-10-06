import streamer
import eater
import digester

import signal

from multiprocessing import Process

def SIGINT_handler(signum, frame):
    streamer.running = False
    eater.running = False
    digester.running = False


if __name__ == '__main__':

    # Setup signal handler
    signal.signal(signal.SIGINT, handler=SIGINT_handler)

    # Start all processes
    a = Process(target=eater.eater, args=('192.168.2.100', 1234, 'tmp/full.partial.jpg', 'tmp/full.jpg'))
    b = Process(target=digester.digester, args=('tmp/full.jpg', 'tmp/stream.partial.jpg', 'tmp/stream.jpg'))
    c = Process(target=streamer.streamer, args=(1234, 'tmp/stream.jpg'))

    # Start all process
    a.start()
    b.start()
    c.start()

    # Join all process back for clean termination
    a.join()
    b.join()
    c.join()

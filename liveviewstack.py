import signal
import sys
import os

from multiprocessing import Process
import subprocess

from processes import streamer, eater, digester, recorder, feeder, raspimjpeg

stack_type = None
raspimjpeg_pid = None

def SIGINT_handler(signum, frame):

    if stack_type == 'server':
        streamer.running = False
        eater.running = False
        digester.running = False
        recorder.running = False

    elif stack_type == 'robot':
        os.killpg(raspimjpeg_pid, signal.SIGTERM)


if __name__ == '__main__':

    # Setup signal handler
    signal.signal(signal.SIGINT, SIGINT_handler)

    # Get stack type
    global stack_type
    stack_type = sys.argv[1]

    if stack_type == 'server':

        '''
        STACK FOR RUNNING ON SERVER
        '''

        # Create processes
        a = Process(target=eater.eater, args=('192.168.2.100', 1234, 'tmp/full.partial.jpg', 'tmp/full.jpg'))
        b = Process(target=digester.digester, args=('tmp/full.jpg', 'tmp/stream.partial.jpg', 'tmp/stream.jpg'))
        c = Process(target=streamer.streamer, args=(1234, 'tmp/stream.jpg'))
        d = Process(target=recorder.server, args=('0.0.0.0', 5001))

        # Start all process
        a.start()
        b.start()
        c.start()
        d.start()

        # Join all process back for clean termination
        a.join()
        b.join()
        c.join()
        d.join()

    elif stack_type == 'robot':

        '''
        STACK FOR RUNNING ON ROBOT
        '''

        # Create processes
        e = Process(target=raspimjpeg.server, args=())
        f = Process(target=feeder.server, args=('0.0.0.0', 1234, '/dev/shm/mjpeg/cam.jpg'))
        g = subprocess.Popen('3rd_bin/raspimjpeg', '--config', 'raspimjpeg.config')

        # Update shared variables
        global raspimjpeg_pid
        raspimjpeg_pid = g.pid

        # Start processes
        e.start()
        f.start()

        # Join all process back for clean termination
        e.join()
        f.join()

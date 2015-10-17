from multiprocessing import Process
import signal
import sys

import socket

from processes import streamer, eater, digester, recorder, feeder
import config_loader

# specify whether this running stack is robot stack or server stack
stack_type = None

'''
    Fake a connection to specified port.
      This will unblock call to accept() and process can terminate gracefully
'''
def dummy_connect(PORT):
    sock = socket.socket()
    sock.connect(('127.0.0.1', PORT))
    sock.close()

'''
    Handle SIGINT
      Setting running flags for each process to false.
      And send dummy requests to unblock call to accept()
'''
def SIGINT_handler(signum, frame):

    global stack_type

    if stack_type == 'server':
        streamer.running = False
        eater.running = False
        digester.running = False
        recorder.running = False
        dummy_connect(5000)
        dummy_connect(5001)

    elif stack_type == 'robot':
        feeder.running = False
        dummy_connect(1234)


if __name__ == '__main__':

    # Setup signal handler
    signal.signal(signal.SIGINT, SIGINT_handler)

    # Get stack type
    stack_type = sys.argv[1]

    # Load configuration file
    config = config_loader.load(sys.argv[2])

    if stack_type == 'server':

        '''
        STACK FOR RUNNING ON SERVER
        '''

        # Create processes
        a = Process(target=eater.eater, args=(config, ))
        b = Process(target=digester.digester, args=(config, ))
        c = Process(target=streamer.streamer, args=(config, ))
        d = Process(target=recorder.server, args=(config, ))

        # Start all process
        a.start()
        b.start()
        c.start()
        d.start()

        '''
        for i in range(2):

            time.sleep(2)

            # Create dummy packet for testing our recorder
            builder = packet.BananaPacketBuilder()
            builder.set_type(packet.REQ_TYPE)
            builder.set_command(packet.COMMAND_ON)
            builder.set_resolution(packet.RES_480)

            sock = socket.socket()
            sock.connect(('127.0.0.1', 5001))
            packet_bytes = bytes((builder.create(), ))
            sock.sendall(packet_bytes)
            sock.close()

            time.sleep(2)

            # Create dummy packet for testing our recorder
            builder = packet.BananaPacketBuilder()
            builder.set_type(packet.REQ_TYPE)
            builder.set_command(packet.COMMAND_OFF)
            builder.set_resolution(packet.RES_480)

            sock = socket.socket()
            sock.connect(('127.0.0.1', 5001))
            packet_bytes = bytes((builder.create(), ))
            sock.sendall(packet_bytes)
            sock.close()
        '''

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
        f = Process(target=feeder.server, args=('0.0.0.0', 1234, 'sample.jpg'))

        # Start processes
        f.start()

        # Join all process back for clean termination
        f.join()

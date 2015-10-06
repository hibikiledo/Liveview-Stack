import eventlet

import os
import signal

from multiprocessing import Process, RLock
from PIL import Image


running = True


def eater(ip, port, output_partial_path, output_path):

    print("eater started")

    while running:
        s = eventlet.connect((ip, port))
        output_bytes = bytearray()

        while True:
            data = s.recv(4096)
            output_bytes.extend(data)
            if len(data) == 0:
                break

        output_file = open(output_partial_path, 'wb')
        output_file.write(output_bytes)
        output_file.close()

        os.rename(output_partial_path, output_path)

    print("eater stopped")


def digester(input_path, output_partial_path, output_path):

    print("digester started")

    while running:
        im = Image.open(input_path)
        im.thumbnail((640, 480), Image.ANTIALIAS)
        im.save(output_partial_path)

        os.rename(output_partial_path, output_path)

    print("digester stopped")


def streamer_handler(client_socket, address, image_path):
    print("Handling", address)
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    client_socket.sendall(image_bytes)
    client_socket.close()


def streamer(port, src_path):
    server_socket = eventlet.listen(('0.0.0.0', port))
    pool = eventlet.GreenPool(10)
    while running:
        client_socket, address = server_socket.accept()
        pool.spawn_n(streamer_handler, client_socket, address, src_path)


def SIGINT_handler(signum, frame):
    global running
    running = False


if __name__ == '__main__':

    # Setup signal handler
    signal.signal(signal.SIGINT, handler=SIGINT_handler)

    # Start all processes
    a = Process(target=eater, args=('192.168.2.100', 1234, 'tmp/full.partial.jpg', 'tmp/full.jpg'))
    b = Process(target=digester, args=('tmp/full.jpg', 'tmp/stream.partial.jpg', 'tmp/stream.jpg'))
    c = Process(target=streamer, args=(1234, 'tmp/stream.jpg'))

    # Start all process
    a.start()
    b.start()
    c.start()

    # Join all process back for clean termination
    a.join()
    b.join()
    c.join()



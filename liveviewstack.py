import eventlet

import os

from multiprocessing import Process, RLock
from PIL import Image


def eater(ip, port, output_partial_path, output_path):
    while True:
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


def digester(input_path, output_partial_path, output_path):
    while True:
        im = Image.open(input_path)
        im.thumbnail((640, 480), Image.ANTIALIAS)
        im.save(output_partial_path)

        os.rename(output_partial_path, output_path)


def streamer_handler(client_socket, address, image_path, streamer_lock):
    print("Handling", address)
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    client_socket.sendall(image_bytes)
    client_socket.close()


def streamer(streamer_lock, port, src_path):
    server_socket = eventlet.listen(('0.0.0.0', port))
    pool = eventlet.GreenPool(10)
    while True:
        client_socket, address = server_socket.accept()
        pool.spawn_n(streamer_handler, client_socket, address, src_path, streamer_lock)


if __name__ == '__main__':
    # Start all processes
    Process(target=eater, args=('192.168.2.100', 1234, 'tmp/full.jpg.part', 'tmp/full.jpg')).start()
    Process(target=digester, args=('tmp/full.jpg', 'tmp/stream.jpg.part', 'tmp/stream.jpg')).start()
    Process(target=streamer, args=(1234, 'tmp/stream.jpg')).start()

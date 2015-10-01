import eventlet

from multiprocessing import Process, RLock
from PIL import Image


def eater(digester_lock, ip, port, output_path):
    while True:
        s = eventlet.connect((ip, port))
        output_bytes = bytearray()

        while True:
            data = s.recv(4096)
            output_bytes.extend(data)
            if len(data) == 0:
                break

        digester_lock.acquire()
        try:
            output_file = open(output_path, 'wb')
            output_file.write(output_bytes)
            output_file.close()
        finally:
            digester_lock.release()


def digester(digester_lock, streamer_lock, input_path, output_path):
    while True:
        digester_lock.acquire()
        streamer_lock.acquire()
        try:
            im = Image.open(input_path)
            im.thumbnail((640, 480), Image.ANTIALIAS)
            im.save(output_path)
        finally:
            digester_lock.release()
            streamer_lock.release()

def streamer_handler(client_socket, address, image_path, streamer_lock):
    print("Handling", address)
    streamer_lock.acquire()
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    streamer_lock.release()
    client_socket.sendall(image_bytes)
    client_socket.close()

def streamer(streamer_lock, port, src_path):
    server_socket = eventlet.listen(('0.0.0.0', port))
    pool = eventlet.GreenPool(10)
    while True:
        client_socket, address = server_socket.accept()
        pool.spawn_n(streamer_handler, client_socket, address, src_path, streamer_lock)


if __name__ == '__main__':
    # create an RLock that share among 2 processes
    digester_lock = RLock()
    streamer_lock = RLock()
    # Create 2 processes sharing the same lock
    Process(target=eater, args=(digester_lock, '192.168.2.100', 1234, 'tmp/full.jpg')).start()
    Process(target=digester, args=(digester_lock, streamer_lock, 'tmp/full.jpg', 'tmp/stream.jpg')).start()
    Process(target=streamer, args=(streamer_lock, 1234, 'tmp/stream.jpg')).start()

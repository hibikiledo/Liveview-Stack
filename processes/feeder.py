import eventlet

'''
    - Feeder
    ---- Feed image frame as response to any incoming request.
    ---- This application is meant to be run on Raspberry Pi.
'''

running = True


def handle(s, addr, source_file):
    image_file = open(source_file, 'rb')
    image_bytes = image_file.read()
    s.sendall(image_bytes)
    s.close()


def server(config):

    port = int(config['feeder.port'])
    source_file = config['feeder.source_file']

    print("Server is listening on {}".format(port))

    server_socket = eventlet.listen(('0.0.0.0', port))
    pool = eventlet.GreenPool(10)

    while running:
        client_socket, address = server_socket.accept()
        pool.spawn_n(handle, client_socket, address, source_file)


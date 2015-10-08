import eventlet

'''
    - Feeder
    ---- Feed image frame as response to any incoming request.
    ---- This application is meant to be run on Raspberry Pi.
'''

running = True

def handle(s, addr, image_path):
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    s.sendall(image_bytes)
    s.close()

def server(host, port, image_path):
    print("Server is listening on {} {}".format(host, port))

    server_socket = eventlet.listen((host, port))
    pool = eventlet.GreenPool(10)

    while running:
        client_socket, address = server_socket.accept()
        pool.spawn_n(handle, client_socket, address, image_path)


import eventlet

import packet

running = True

def streamer_handler(client_socket, address, image_path):

    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()

    client_socket.sendall(image_bytes)
    client_socket.close()


def streamer(config, resolution):

    port = int(config['streamer.port'])
    src_file = config['streamer.source_file'].format(packet.RESOLUTIONS.get(resolution))

    print("---- Streamer started ...")
    print("PORT:", port)
    print("Source file:", src_file)

    server_socket = eventlet.listen(('0.0.0.0', port))
    pool = eventlet.GreenPool(10)

    while running:
        client_socket, address = server_socket.accept()
        pool.spawn_n(streamer_handler, client_socket, address, src_file)

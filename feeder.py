import eventlet

import getopt
import sys

'''
    - Feeder
    ---- Feed image frame as response to any incoming request.
    ---- This application is meant to be run on Raspberry Pi.
'''

def handle(s, addr, image_path):
    image_file = open(image_path, 'rb')
    image_bytes = image_file.read()
    s.sendall(image_bytes)
    s.close()

def usage():
    print("Usage ..")
    print("python feeder.py -p <port> -s <image path>")

def main(argv):

    # Default port for server to listen on
    port = 5555
    image_path = None

    # User can specify optional port instead of the default one
    try:
        opts, args = getopt.getopt(argv[1:], "s:p:", ['source=', 'port='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # If user specify another port, we then use it
    for (opt, arg) in opts:
        if opt in ("-p", "--port"):
            port = int(arg)
        if opt in ('-s', '--source'):
            image_path = arg

    # Start our server if image_path is specified
    if image_path is not None:
        start_server("0.0.0.0", port, image_path)
    else:
        usage()
        sys.exit(2)

def start_server(host, port, image_path):
    print("Server is listening on {} {}".format(host, port))
    server_socket = eventlet.listen((host, port))
    pool = eventlet.GreenPool(10)
    while True:
        client_socket, address = server_socket.accept()
        pool.spawn_n(handle, client_socket, address, image_path)

if __name__ == "__main__":
    main(sys.argv)



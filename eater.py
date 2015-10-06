import liveviewstack

import eventlet

import os

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

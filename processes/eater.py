import eventlet

import os

running = True

def eater(config):

    # Read from configuration file
    ip = config['eater.ip']
    port = int(config['eater.port'])
    output_partial_filename = config['eater.partial_file']
    output_filename = config['eater.complete_file']

    print("---- Eater process started ...")
    print("IP:", ip)
    print("PORT:", port)
    print("Output file(partial):", output_partial_filename)
    print("Output file(complete):", output_filename)

    while running:
        s = eventlet.connect((ip, port))
        output_bytes = bytearray()

        while True:
            data = s.recv(4096)
            output_bytes.extend(data)
            if len(data) == 0:
                break

        partial_output_file = open(output_partial_filename, 'wb')
        partial_output_file.write(output_bytes)
        partial_output_file.close()

        os.rename(output_partial_filename, output_filename)

    print("Eater stopped")

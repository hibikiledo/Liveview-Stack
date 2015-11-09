from PIL import Image

import time
import os

running = True

def digester(config):

    # Read from configuration file
    input_filename = config['digester.source_file']
    output_partial_filename = config['digester.stream_partial_file']
    output_filename = config['digester.stream_complete_file']

    print("---- Digester process started ...")
    print("Input path", input_filename)
    print("Output file(partial)", output_partial_filename)
    print("Output file(complete)", output_filename)

    while running:
        try:
            im = Image.open(input_filename)
            im.thumbnail((640, 480), Image.ANTIALIAS)
            im.save(output_partial_filename)

            os.rename(output_partial_filename, output_filename)
        except FileNotFoundError:
            # eater may not be able to fetch image yet
            # we need to wait a while and hope that image will available next time
            print("[DIGESTER] Image file is not available .. try again in 5 seconds")
            time.sleep(5)

    print("[DIGESTER] Stopped")

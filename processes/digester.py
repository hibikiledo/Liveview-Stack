from PIL import Image

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
        im = Image.open(input_filename)
        im.thumbnail((640, 480), Image.ANTIALIAS)
        im.save(output_partial_filename)

        os.rename(output_partial_filename, output_filename)

    print("Digester stopped")

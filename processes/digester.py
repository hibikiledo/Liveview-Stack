from PIL import Image

import time
import os

import packet

running = True

def digester(config, resolution=None):

    # Read from configuration file
    input_filename = config['digester.source_file']
    output_partial_filename = config['digester.partial_file'].format(packet.RESOLUTIONS.get(resolution))
    output_filename = config['digester.complete_file'].format(packet.RESOLUTIONS.get(resolution))

    # Convert single value constant from module packet into tuples of width and height
    if resolution == packet.RES_480:
        resolution = (640, 480)
    elif resolution == packet.RES_720:
        resolution = (1280, 720)

    print("---- Digester process started ...")
    print("Input path", input_filename)
    print("Output file(partial)", output_partial_filename)
    print("Output file(complete)", output_filename)

    while running:
        try:
            im = Image.open(input_filename)
            im.thumbnail((resolution[0], resolution[1]), Image.ANTIALIAS)
            im.save(output_partial_filename)

            os.rename(output_partial_filename, output_filename)
        except FileNotFoundError:
            # eater may not be able to fetch image yet
            # we need to wait a while and hope that image will available next time
            print("[DIGESTER] Image file is not available .. try again in 5 seconds")
            time.sleep(5)

    print("[DIGESTER] Stopped")

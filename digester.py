import liveviewstack

from PIL import Image

import os

running = True

def digester(input_path, output_partial_path, output_path):

    print("digester started")

    while running:
        im = Image.open(input_path)
        im.thumbnail((640, 480), Image.ANTIALIAS)
        im.save(output_partial_path)

        os.rename(output_partial_path, output_path)

    print("digester stopped")

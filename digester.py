import eventlet

from PIL import Image

import getopt
import time
import sys

def digest_image(input_path, output_path):
    im = Image.open(input_path)
    im.thumbnail((640, 480), Image.ANTIALIAS)
    im.save(output_path)

def usage():
    print("Usage ...")
    print("python digester.py -i <input path> -o <output path>")

def main(argv):

    # Default values for customizable parameters
    input_path = None
    output_path = None

    # Get user settings for fps which will overwrite the default one
    try:
        opts, args = getopt.getopt(argv[1:], "i:o:", ['input=', 'output='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for (opt, arg) in opts:
        if opt in ('-i', '--input'):
            input_path = arg
        if opt in ('-o', '--output'):
            output_path = arg

    # Perform forever digesting until Ctrl+C is received
    print("Digesting images from {} to {}".format(input_path, output_path))
    while True:
        digest_image(input_path, output_path)

if __name__ == '__main__':
    main(sys.argv)




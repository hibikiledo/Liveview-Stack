import eventlet

import getopt
import time
import sys

def eat_image(filename, ip, port):
    s = eventlet.connect((ip, port))
    output_bytes = bytearray()

    while True:
        data = s.recv(4096)
        output_bytes.extend(data)
        if len(data) == 0:            
            break

    output_file = open(filename, 'wb')
    output_file.write(output_bytes)

def usage():
    print("Usage ...")
    print("python eater.py -fps <fps> -o <output path>")

def main(argv):

    # Default values for customizable parameters
    ip = None
    port = None
    fps = None
    output_path = None
    delay_time = 40.0 / 1000.0

    # Get user settings for fps which will overwrite the default one
    try:
        opts, args = getopt.getopt(argv[1:], "t:p:f:o:", ['target=','port=', 'fps=', 'output='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for (opt, arg) in opts:
        if opt in ('-f', '--fps='):
            fps = float(arg)
            delay_time = (1000.0 / fps ) / 1000.0
        if opt in ('-t', '--target'):
            ip = arg
        if opt in ('-p', '--port'):
            port = int(arg)
        if opt in ('-o', '--output'):
            output_path = arg

    # Counter for creating unique image frame filename
    counter = 0

    # Perform forever eating until Ctrl+C is received
    print("Eating images from {}:{} @ {} fps".format(ip, port, fps))
    while True:
        eat_image("{}/frame-{}.png".format(output_path, counter), ip, port)
        counter += 1
        # Delay for specified amount
        time.sleep(delay_time)

if __name__ == '__main__':
    main(sys.argv)




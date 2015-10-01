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
    print("python eater.py -t <target ip> -p <port> -o <output path>")

def main(argv):

    # Default values for customizable parameters
    ip = None
    port = None
    output_path = None

    # Get user settings for fps which will overwrite the default one
    try:
        opts, args = getopt.getopt(argv[1:], "t:p:o:", ['target=','port=', 'output='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for (opt, arg) in opts:
        if opt in ('-t', '--target'):
            ip = arg
        if opt in ('-p', '--port'):
            port = int(arg)
        if opt in ('-o', '--output'):
            output_path = arg

    # Perform forever eating until Ctrl+C is received
    print("Eating images from {}:{}".format(ip, port))
    while True:
        mark = time.time()
        eat_image(output_path, ip, port)
        print((time.time() - mark) * 10)

if __name__ == '__main__':
    main(sys.argv)




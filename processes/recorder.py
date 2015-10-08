
import packet
import time
import os
import eventlet
import threading

running = True

recorder_thread = None
recorder_running = True

def record(src_path, output_path):

    print("recorder starting ..")

    global recorder_running

    # counter for creating unique frame number
    counter = 0

    # create output_path
    os.mkdir(output_path)

    # forever record until flag is false
    while recorder_running:

        image_file = open(src_path, 'rb')
        image_bytes = image_file.read()

        image_file.close()

        output_filename = "frame-{}".format(counter) + '.jpg'
        output_full_path = os.path.join(output_path, output_filename)
        print(output_full_path)

        output_file = open(output_full_path, 'wb')
        output_file.write(image_bytes)
        output_file.close()

        counter += 1

    print("recorder is dead ..")


def handler(client_socket, address, src_path):

    global recorder_thread, recorder_running

    # get request packet
    request_packet = packet.read_command(client_socket)

    packet_reader = packet.BananaPacketReader(packet.byte_to_int(request_packet))

    # extract information
    type    = packet_reader.get_type()
    command = packet_reader.get_command()
    resolution = packet_reader.get_resolution()

    packet_reader.report()

    # handle record command
    if command == packet.COMMAND_ON:
        # reset flag
        recorder_running = True
        # start new recorder thread as respond to the request
        output_path = time.strftime("%d-%m-%Y-%H-%M-%S")

        recorder_thread = threading.Thread(target=record, args=(src_path, output_path))
        recorder_thread.start()

    elif command == packet.COMMAND_OFF:
        # check if recorder thread exist, if so .. join it back
        if recorder_thread != None:
            # unset flag
            recorder_running = False
            recorder_thread = None

    # send ACK and mirror request message
    packet_builder = packet.BananaPacketBuilder()
    packet_builder.set_type(packet.ACK_TYPE)
    packet_builder.set_command(command)
    packet_builder.set_resolution(resolution)

    # create respond packet
    reply_packet = packet_builder.create()

    packet_builder.report()

    # send acknowledge packet back to phone
    client_socket.sendall(bytes((reply_packet, )))

    # close socket
    client_socket.close()


def server(HOST, PORT, src_path):

    print("Server started on {}:{}".format(HOST, PORT))

    server_socket = eventlet.listen((HOST, PORT))
    thread_pool = eventlet.GreenPool(10)

    while running:
        clientsocket, addr = server_socket.accept()
        thread_pool.spawn_n(handler, clientsocket, addr, src_path)

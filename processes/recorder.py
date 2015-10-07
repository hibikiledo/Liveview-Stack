
import packet
import eventlet

running = True

def handler(client_socket, address):

    # get request packet
    request_packet = packet.read_command(client_socket)

    packet_reader = packet.BananaPacketReader(packet.byte_to_int(request_packet))

    # extract information
    type    = packet_reader.get_type()
    command = packet_reader.get_command()
    resolution = packet_reader.get_resolution()

    packet_reader.report()

    # Let dispatcher dispatch command
    # self.dispatcher.handle(command, value)

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


def server(HOST, PORT):

    print("Server started on {}:{}".format(HOST, PORT))

    server_socket = eventlet.listen((HOST, PORT))
    thread_pool = eventlet.GreenPool(10)

    while running:
        clientsocket, addr = server_socket.accept()
        thread_pool.spawn_n(handler, clientsocket, addr)

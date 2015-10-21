import struct

# Define constants for packet type
REQ_TYPE = 0
ACK_TYPE = 1

TYPES = {
    0: 'REQ_TYPE',
    1: 'ACK_TYPE'
}

# Define constants for commands
COMMAND_ON = 1
COMMAND_OFF = 0

COMMANDS = {
    1: 'COMMAND_ON',
    0: 'COMMAND_OFF'
}

# Define constants for resolution
RES_480 = 0
RES_720 = 1
RES_1080 = 2

RESOLUTIONS = {
    0: 'RES_480',
    1: 'RES_720',
    2: 'RES_1080'
}

MAX_ATTEMPT = 20

'''
    Utility function
    [0] Continue reading for command until get the complete one.
'''


def read_command(s):
    attempt_count = 0
    byte_count = 0
    command_packet = bytearray()
    # keep reading until get 2 byte (complete command packet)
    while byte_count < 1:
        # increment attempt
        attempt_count += 1
        partial = s.recv(1)
        if len(partial) == 1:
            command_packet.append(byte_to_int(partial))
            byte_count += 1
        # check for fail command
        if attempt_count > MAX_ATTEMPT:
            return None
    # return
    return command_packet


'''
    Utility function
    [1] Convert byte into integer
'''


def byte_to_int(byte):
    return struct.unpack("B", byte)[0]

'''
    BananaPacketBuilder
    [1] Allow programmer to set type, command, and resolution.
    --- create() build a packet and return as integer.
'''


class BananaPacketBuilder:

    def __init__(self):
        self.type = None
        self.command = None
        self.resolution = None

    def set_type(self, type):
        self.type = type

    def set_command(self, command):
        self.command = command

    def set_resolution(self, resolution):
        self.resolution = resolution

    def create(self):

        # create our request byte
        request = int('00000000', 2)

        # handle type
        if self.type == REQ_TYPE:
            request |= int('10000000', 2)
        elif self.type == ACK_TYPE:
            request |= int('01000000', 2)

        # handle command ON/OFF
        request |= (self.command << 5)

        # handle resolution
        request |= (self.resolution << 3)

        # return request
        return request

    def report(self):
        print(
            ": ".join([
                TYPES.get(self.type), COMMANDS.get(self.command), RESOLUTIONS.get(self.resolution)
            ])
        )


'''
    BananaPacketReader
    [1] Allow programmer to access type, command, and resolution
    --- _read() is called automatically to make value accesible
'''


class BananaPacketReader:

    def __init__(self, packet):
        self.packet = packet
        self.type = None
        self.command = None
        self.resolution = None

        self._read()

    def get_type(self):
        return self.type

    def get_command(self):
        return self.command

    def get_resolution(self):
        return self.resolution

    def _read(self):

        packet = self.packet

        # handle Packet types
        if packet & int('11000000', 2) == int('10000000', 2):
            self.type = REQ_TYPE
        elif packet & int('11000000', 2) == int('01000000', 2):
            self.type = ACK_TYPE

        # handle command ON/OFF
        self.command = (packet & int('00100000', 2)) >> 5
        if self.command not in COMMANDS.keys():
            print("Unknown command")

        # handle resolution
        self.resolution = (packet & int('00011000', 2)) >> 3
        if self.command not in RESOLUTIONS.keys():
            print("Unknown resolution")

    def report(self):
        print(
            ": ".join([
                TYPES.get(self.type), COMMANDS.get(self.command), RESOLUTIONS.get(self.resolution)
            ])
        )

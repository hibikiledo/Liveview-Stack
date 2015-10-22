import struct
from exceptions import *

# Packet Type
# 10xx xxxx - REQ_TYPE
# 01xx xxxx - ACK_TYPE
REQ_TYPE = int('10000000', 2)
ACK_TYPE = int('01000000', 2)
TYPE_MASK = int('11000000', 2)
TYPES = {
    REQ_TYPE: 'REQ_TYPE',
    ACK_TYPE: 'ACK_TYPE'
}

# Define constants for commands
COMMAND_ON = int('00100000', 2)
COMMAND_OFF = int('00000000', 2)
COMMAND_MASK = int('00100000', 2)
COMMANDS = {
    COMMAND_ON: 'COMMAND_ON',
    COMMAND_OFF: 'COMMAND_OFF'
}

# Define constants for resolution
RES_480 = int('00000000', 2)
RES_720 = int('00001000', 2)
RES_1080 = int('00010000', 2)
RES_MASK = int('00011000', 2)
RESOLUTIONS = {
    RES_480: 'RES_480',
    RES_720: 'RES_720',
    RES_1080: 'RES_1080'
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
        if type not in [REQ_TYPE, ACK_TYPE]:
            raise UnknownPacketType()
        self.type = type

    def set_command(self, command):
        if command not in [COMMAND_ON, COMMAND_OFF]:
            raise UnknownCommand()
        self.command = command

    def set_resolution(self, resolution):
        if resolution not in [RES_480, RES_720, RES_1080]:
            raise UnknownResolution()
        self.resolution = resolution

    def validate(self):
        for field in [self.type, self.command, self.resolution]:
            if field is None:
                return False
        return True

    def create(self):

        if not self.validate():
            raise IncompletePacket()

        # create our request byte
        request = int('00000000', 2)

        # handle type
        request |= self.type

        # handle command ON/OFF
        request |= self.command

        # handle resolution
        request |= self.resolution

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

        if self.packet is None:
            raise InvalidPacket()

        packet = self.packet

        # handle Packet types
        if (packet & TYPE_MASK) in [ACK_TYPE, REQ_TYPE]:
            self.type = packet & TYPE_MASK
        else:
            raise UnknownPacketType()

        # handle command ON/OFF
        if (packet & COMMAND_MASK) in [COMMAND_ON, COMMAND_OFF]:
            self.command = packet & COMMAND_MASK
        else:
            raise UnknownCommand()

        # handle resolution
        if (packet & RES_MASK) in [RES_480, RES_720, RES_1080]:
            self.resolution = packet & RES_MASK
        else:
            raise UnknownResolution()

    def report(self):
        print(
            ": ".join([
                TYPES.get(self.type), COMMANDS.get(self.command), RESOLUTIONS.get(self.resolution)
            ])
        )

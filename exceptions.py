class UnknownPacketType(Exception):
    def __init__(self):
        self.value = 'Packet type is neither ACK nor REQ'

    def __str__(self):
        return repr(self.value)


class UnknownCommand(Exception):
    def __init__(self):
        self.value = 'Command is neither ON nor OFF'

    def __str__(self):
        return repr(self.value)


class UnknownResolution(Exception):
    def __init__(self):
        self.value = 'Resolution is not RES_480 or RES_720 or RES_1080'

    def __str__(self):
        return repr(self.value)


class IncompletePacket(Exception):
    def __init__(self):
        self.value = 'Packet is not completed. Some fields is None'

    def __str__(self):
        return repr(self.value)


class InvalidPacket(Exception):
    def __init__(self):
        self.value = 'Given packet to reader is invalid (None)'

    def __str__(self):
        return repr(self.value)

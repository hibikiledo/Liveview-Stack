import unittest

import packet
from exceptions import *


class PacketBuilderReaderTest(unittest.TestCase):

    def test_build_read(self):

        types = packet.TYPES.keys()
        commands = packet.COMMANDS.keys()
        resolutions = packet.RESOLUTIONS.keys()

        for type in types:
            for command in commands:
                for resolution in resolutions:

                    builder = packet.BananaPacketBuilder()
                    builder.set_type(type)
                    builder.set_command(command)
                    builder.set_resolution(resolution)

                    output = builder.create()

                    reader = packet.BananaPacketReader(output)

                    self.assertEqual(reader.get_type(), type)
                    self.assertEqual(reader.get_command(), command)
                    self.assertEqual(reader.get_resolution(), resolution)


class PacketBuilderTest(unittest.TestCase):

    def test_build_incomplete_packet(self):

        # empty packet
        builder = packet.BananaPacketBuilder()
        self.assertRaises(IncompletePacket, builder.create)

        # packet with type set
        builder = packet.BananaPacketBuilder()
        builder.set_type(packet.ACK_TYPE)
        self.assertRaises(IncompletePacket, builder.create)

        # packet with command set
        builder = packet.BananaPacketBuilder()
        builder.set_command(packet.COMMAND_ON)
        self.assertRaises(IncompletePacket, builder.create)

        # packet with resolution set
        builder = packet.BananaPacketBuilder()
        builder.set_resolution(packet.RES_480)
        self.assertRaises(IncompletePacket, builder.create)

        # packet with type and command set
        builder = packet.BananaPacketBuilder()
        builder.set_type(packet.ACK_TYPE)
        builder.set_command(packet.COMMAND_ON)
        self.assertRaises(IncompletePacket, builder.create)

        # packet with command and resolution set
        builder = packet.BananaPacketBuilder()
        builder.set_command(packet.COMMAND_ON)
        builder.set_resolution(packet.RES_720)
        self.assertRaises(IncompletePacket, builder.create)

    def test_build_incorrect_field_value(self):

        # wrong resolution field
        builder = packet.BananaPacketBuilder()
        self.assertRaises(UnknownResolution, builder.set_resolution, packet.ACK_TYPE)

        # wrong type field
        builder = packet.BananaPacketBuilder()
        self.assertRaises(UnknownPacketType, builder.set_type, packet.RES_480)

        # wrong command field
        builder = packet.BananaPacketBuilder()
        self.assertRaises(UnknownCommand, builder.set_command, packet.ACK_TYPE)


class PacketReaderTest(unittest.TestCase):

    def test_with_none_packet(self):

        # pass in none as packet
        broken_packet = None
        self.assertRaises(InvalidPacket, packet.BananaPacketReader, broken_packet)

    def test_with_wrong_field_value(self):

        broken_type_packet = int('00000000', 2)
        self.assertRaises(UnknownPacketType, packet.BananaPacketReader, broken_type_packet)

        broken_type_packet = int('11000000', 2)
        self.assertRaises(UnknownPacketType, packet.BananaPacketReader, broken_type_packet)

        broken_res_packet = int('01011000', 2)
        self.assertRaises(UnknownResolution, packet.BananaPacketReader, broken_res_packet)


if __name__ == '__main__':
    unittest.main()


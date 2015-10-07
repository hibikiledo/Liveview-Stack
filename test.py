import unittest

import packet

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


if __name__ == '__main__':
    unittest.main()


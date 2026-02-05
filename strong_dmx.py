 #!/usr/bin/env bash
 # -*- coding: utf-8 -*-
 # /////////////////////////////////////////////////////////////////////////////
 # //
 # // test.py 
 # //
 # // strong.py DMX
 # //
 # // 05/02/2026 10:40:37  
 # // (c) 2026 Juan M. Casillas <juanm.casillas@gmail.com>
 # // 
 # // Send UDP packets (DMX512) to STRONG controller so we can manage the lights
 # //
 # /////////////////////////////////////////////////////////////////////////////
 
import os
import copy
from pprint import pprint
class DMXPacket:

    # 0000  44 4d 58 35 31 32 2d 02  00 01 00 02 00 ff 00 ff   DMX512-· ········
    # 0010  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
    # 0020  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
    # 0030  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 00 00 00   ········ ········

    payload_start = 12
    max_signals = 24
    packet_size = 1036
    payload_size = 64

    empty_packet = bytearray().fromhex(
      "44 4d 58 35 31 32 2d 02  00 01 00 02 00 ff 00 ff" + \
      "00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff" + \
      "00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff" + \
      "00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 00 00 00" + \
      "00" * (packet_size - payload_size)
      
    )
    # package data has 1036 bytes

    commands = {
        'down': bytearray.fromhex('1e e1'),
        'up'  : bytearray.fromhex('96 69'),
        'none': bytearray.fromhex('00 ff'),
    }

    


    def __init__(self):
        pass

    def hexdump(src: bytes, bytesPerLine: int = 16, bytesPerGroup: int = 2, asciiPerGroup: int = 4, sep: str = '.', joinlines: bool = True):
        FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
        lines = []
        maxAddrLen = len(hex(len(src)))
        if 8 > maxAddrLen:
            maxAddrLen = 8

        for addr in range(0, len(src), bytesPerLine):
            hexString = ""
            printable = ""

            # The chars we need to process for this line
            chars = src[addr : addr + bytesPerLine]

            # Create hex string
            tmp = ''.join(['{:02x}'.format(x) for x in chars]) ## X means uppercase
            idx = 0
            for c in tmp:
                hexString += c
                idx += 1
                # 2 hex digits per byte.
                if idx % bytesPerGroup * 2 == 0 and idx < bytesPerLine * 2:
                    hexString += " "
            # Pad out the line to fill up the line to take up the right amount of space to line up with a full line.
            hexString = hexString.ljust(bytesPerLine * 2 + int(bytesPerLine * 2 / bytesPerGroup) - 1)

            # create printable string
            tmp = ''.join(['{}'.format((x <= 127 and FILTER[x]) or sep) for x in chars])
            # insert space every asciiPerGroup
            idx = 0
            for c in tmp:
                printable += c
                idx += 1
                # Need to check idx because strip() would also delete genuine spaces that are in the data.
                if idx % asciiPerGroup == 0 and idx < len(chars):
                    printable += " "

            lines.append(f'{addr:0{maxAddrLen}X}  {hexString}  |{printable}|')
        
        if not joinlines:
            return lines
        return os.linesep.join(lines)

    def empty():
        return copy.copy(DMXPacket.empty_packet)

    def cmd(indexes, cmd_str):
        pkg = copy.copy(DMXPacket.empty_packet)

        for index in indexes:
            # copy the command bytes (2) into the position.

            position = DMXPacket.payload_start + ((index-1)* 2)
            pkg[position] = DMXPacket.commands[cmd_str][0]
            pkg[position+1] = DMXPacket.commands[cmd_str][1]

        return pkg
    
    def up(indexes):   return DMXPacket.cmd(indexes, "up")
    def down(indexes): return DMXPacket.cmd(indexes, "down")
    def none(indexes): return DMXPacket.cmd(indexes, "none")


def test_packages():
    packet = DMXPacket()
    print("emtpy packet")
    print("-" * 70)
    print(DMXPacket.hexdump( DMXPacket.empty()))

    indexes = [ 1, 2, 3,24  ]
    
    print("down, indexes: ", indexes)
    print("-" * 70)
    print(DMXPacket.hexdump( DMXPacket.down( indexes)))

    print("up, indexes: ", indexes)
    print("-" * 70)
    print(DMXPacket.hexdump( DMXPacket.up( indexes)))

    print("none, indexes: ", indexes)
    print("-" * 70)
    print(DMXPacket.hexdump( DMXPacket.none( indexes)))

if __name__ == "__main__":

    test_packages()
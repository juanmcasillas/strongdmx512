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
import socket
import time

from hexdump import hexdump

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

   

    def empty():
        return copy.copy(DMXPacket.empty_packet)

    def cmd(cmd_str, indexes):
        """Generate the proper package configured on DMXPacket.commands. If no indexes, return empty packet

        Args:
            cmd_str (_type_): _description_
            indexes (_type_): _description_

        Returns:
            _type_: _description_
        """
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


class LampClient:
    def __init__(
            self, 
            src_addr: str = "192.168.72.228",
            dst_addr: str = "192.168.72.226",
            dst_port: int = 53704,
            fps: int = 8,
            socket_timeout: int = 1.0
        ):
        self.src_addr = src_addr
        self.dst_addr = dst_addr
        self.dst_port = dst_port
        self.fps = fps
        self.socket_timeout = socket_timeout

        self.socket = None

    def send_cmd(
            self,
            cmd: str = "none",
            addrs: list = []
        ):

        if not self.socket:
            raise IOError("Socket not connected")
        addr = (self.dst_addr, self.dst_port)

        
        packet = DMXPacket.cmd(cmd, addrs)

        self.socket.sendto(packet, addr)
            

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.socket_timeout)
    

    def disconnect(self):
        
        if self.socket == None:
            raise IOError("Socket not connected")
        self.socket.close()
        return True







def test_packages():
    packet = DMXPacket()
    print("emtpy packet")
    print("-" * 70)
    print(hexdump( DMXPacket.empty()))

    indexes = [ 1, 2, 3,24  ]
    
    print("down, indexes: ", indexes)
    print("-" * 70)
    print(hexdump( DMXPacket.down( indexes)))

    print("up, indexes: ", indexes)
    print("-" * 70)
    print(hexdump( DMXPacket.up( indexes)))

    print("none, indexes: ", indexes)
    print("-" * 70)
    print(hexdump( DMXPacket.none( indexes)))


def test_client(rounds: int = 10, wait_time: int = 1.0):

    indexes = [ 1, 2, 3,24  ]
    client = LampClient(src_addr = "192.168.1.92", dst_addr = "192.168.1.92")
    client.connect()
    for i in range(rounds):
        print("sending round #%d" % i)
        client.send_cmd("down",indexes)
        time.sleep(wait_time)
    client.disconnect()

if __name__ == "__main__":
    #test_packages()
    test_client()
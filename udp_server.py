#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ############################################################################
#
# udp_server.py
# 02/06/2026 (c) Juan M. Casillas <juanm.casillas@gmail.com>
#
# simple udp server to test the commands.
#
# ############################################################################

import socket
import sys
from hexdump import hexdump

PORT: int = 53704
PKT_SIZE: int = 1036

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 53704))

while True:
    try:
        message, address = server_socket.recvfrom(PKT_SIZE)
        print("-------")
        print("%d size" % len(message))
        print(hexdump(message[0:64]))
    except KeyboardInterrupt:
            server_socket.close()
            sys.exit(0)


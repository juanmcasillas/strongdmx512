#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ############################################################################
#
# hexdump.py
# 02/06/2026 (c) Juan M. Casillas <juanm.casillas@gmail.com>
#
# a function to dump nicely bytes
#
# ############################################################################

import os

def hexdump(src: bytes, bytesPerLine: int = 16, bytesPerGroup: int = 2, asciiPerGroup: int = 4, sep: str = '.', joinlines: bool = True):
    """Dumps a byte array into a pretty print hexdump with ASCII visualization. Very configurable.

    Args:
        src (bytes): _description_
        bytesPerLine (int, optional): _description_. Defaults to 16.
        bytesPerGroup (int, optional): _description_. Defaults to 2.
        asciiPerGroup (int, optional): _description_. Defaults to 4.
        sep (str, optional): _description_. Defaults to '.'.
        joinlines (bool, optional): _description_. Defaults to True.

    Returns:
        list|str: if joinlines is True, a str is returned, else a list with the lines.
    """
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

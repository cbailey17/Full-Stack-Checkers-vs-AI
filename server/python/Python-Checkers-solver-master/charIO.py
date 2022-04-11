#! /usr/bin/python3
# io - Functions for input/output

import os
import platform
import stat
import sys

# Tested on Windows and Ubuntu 16.04


def getchWindows():
    "getchWindows() - Return an unbuffered character"
    ch = msvcrt.getch()
    return ch.decode('utf-8')


def getchUnix():
    "getchUnix - Return an unbuffered character"
    try:
        tty.setraw(fd)  # Set tty to unbuffered
        ch = sys.stdin.read(1)    # Read one character
    finally:
        # Reset to buffered I/O
        termios.tcsetattr(fd, termios.TCSADRAIN, sanetty)
    return ch


def getchBuffered():
    """"getchBuffered() -  Read a line, user must terminate with carriage return
    Not as fancy as the raw reads, but more likely to not have problems
    """

    line = input()
    # Only care about the first character
    return line[0] if len(line) else ""


fd = sys.stdin.fileno()  # get stdin file descriptor handle
# If anything other than a TTY, use buffered input
mode = os.fstat(fd).st_mode
if stat.S_ISCHR(mode):
    # chracter device

    systype = platform.system()
    if systype == "Windows":
        import msvcrt
        getch = getchWindows
    elif systype == "Linux":
        # Get the current tty settings and save them
        import tty
        import termios
        fd = sys.stdin.fileno()
        sanetty = termios.tcgetattr(fd)
        getch = getchUnix
    else:
        getch = getchBuffered
else:
    getch = getchBuffered


is_buffered = getch == getchBuffered

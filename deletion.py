#!/usr/env/bin python3
import dircache
import os
import random
import subprocess
import time

import serial


ROOT_DIR = '~izzy/publicprint'
PRINTER_NAME = 'hp-inkjet'

DEVICE_PATH = '/dev/ttyACM0'
BAUD_RATE = 9600


def readSignal(device_path, baud_rate):
    """Listen for signals on the serial line and print files."""
    ser = serial.Serial(device_path, baud_rate)
    while True:
        if s.in_waiting > 0:  # when new serial info is waiting
            cmd = s.readline()
            print('new serial command:', cmd)
            if cmd == b'1':
                # keep old file, print new file
                selected = chooseFile(ROOT_DIR)
                print('selected file:', selected)
                printFile(selected)
            elif cmd == b'd'
                # delete last file
            else:
                print('unknown serial command: {!r}'.format(cmd))
    time.sleep(0.5)


def chooseFile(dir):
    """Pick a file from a directory."""
    contents = [os.path.join(dir, c) for c in os.listdir(dir)]
    if list == []:
        print 'restarting'
        return chooseFile(ROOT_DIR)
    else:
        filename = random.choice(list)
        path = os.path.join(dir, filename)
    if path[-1] == '/':
        path = path[:-1]
        return chooseFile(path)
    else:
         return path


def printFile(path):
    """Print a file - regardless of type."""
    def add_to_queue(path):
        """Add a file to the printer queue."""
        subprocess.run(
            ['lp',
             '-P', '"1"',  # print only the first page
             '-d', PRINTER_NAME,  # select printer by name
             path],
            timeout=5)

    def unoconv(path):
        """Convert a file to a pdf using unoconv.

        Returns:
            The path of the pdf version.
        """
        subprocess.run(
            ['unoconv',
             '-f', 'pdf',
             path],
            timeout=5)
        return os.path.splitext(path)[0] + '.pdf'

    ext = os.path.splitext(path)
    if ext in ['.pdf', '.txt']:  # file can be printed directly
        add_to_queue(path)
    elif ext in ['.doc', '.docx']:  # file can be converted w/ unoconv
        pdf_version = unoconv(path)
        add_to_queue(pdf_version)
    else:
        print("couldn't print file:", path)


if __name__ == '__main__':
    readSignal(DEVICE_PATH, BAUD_RATE)

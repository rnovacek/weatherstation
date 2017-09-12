
import sys
import os

from ampy import pyboard, files

import config

if not config.SSID:
    print('SSID must be set up in config.py prior to uploading')
    sys.exit(1)

if not config.SERVER_URL:
    print('SERVER_URL must be set up in config.py prior to uploading')
    sys.exit(1)

FILES = [
    'main.py',
    'config.py',
    'si7021.py',
    '../common/wemos.py',
]

port = os.environ.get('PORT', '/dev/ttyUSB0')
print('Using port', port)

board = pyboard.Pyboard(port)
board_files = files.Files(board)


def upload(board_files, filename):
    remote = os.path.basename(os.path.abspath(filename))

    with open(filename, 'rb') as infile:
        board_files.put(remote, infile.read())


for filename in FILES:
    print('Uploading', filename)
    upload(board_files, filename)

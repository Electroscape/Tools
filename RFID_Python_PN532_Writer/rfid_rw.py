# Author Martin Pek

import board
import busio
import binascii
from digitalio import DigitalInOut
from time import sleep
import json

from adafruit_pn532.i2c import PN532_I2C
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A, MIFARE_CMD_AUTH_B

try:
    with open('cfg.json') as json_file:
        cfg = json.loads(json_file.read())
        rooms = cfg['rooms']
except ValueError as e:
    print('failure to read config.json')
    print(e)
    input("Press any key to exit")
    exit()

'''
# getting tired of fucked up imports in example code that doesnt work ...
MIFARE_CMD_AUTH_A                   = 0x60
MIFARE_CMD_AUTH_B                   = 0x61
MIFARE_CMD_READ                     = 0x30
'''

i2c = busio.I2C(board.SCL, board.SDA)

reset_pin = DigitalInOut(board.D6)
req_pin = DigitalInOut(board.D12)

# if it gets stuck so we hit the reset that is performed with debugmode ... too lazy to write the pins myself
# pn532 = PN532_I2C(i2c, debug=True, reset=reset_pin, req=req_pin)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
# this delay avoids some problems after wakeup
sleep(0.5)

# no longer supported in never version, not needed too
# ic, ver, rev, support = pn532.get_firmware_version()
# print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

'''
protocols

0 is the sr with authA and default f key
1 is currently deprecated, all rooms shall stick to one setup
'''

def authenticate(uid, protocol, read_block, auth_mode):
    rc = 0
    if protocol == 0:
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        rc = pn532.mifare_classic_authenticate_block(uid, read_block, auth_mode, key)
        print(rc)
    return rc


def write_with_check(write_to_block, write_data, protocol, uid):
    if protocol == 0:
        auth = authenticate(uid, protocol, write_to_block, MIFARE_CMD_AUTH_B)
        sleep(0.5)
        if not auth:
            print('authentication failed, aborting process')
            return 0
        rc = pn532.mifare_classic_write_block(write_to_block, write_data)
    if not rc:
        print('writing failed... exiting')
        return False

    print('return of write: ' + str(rc))

    return True

def read_card_block(uid, protocol, read_block=1):

    rc = 0
    if protocol == 0:
        auth = authenticate(uid, protocol, read_block, MIFARE_CMD_AUTH_A)
        if not auth:
            print('authentication failed, aborting process')
            return 0

    print('Content of block ' + str(read_block))
    if protocol == 0:
        rc = pn532.mifare_classic_read_block(read_block)

    if rc is not None:
        text = "".join(chr(x) for x in rc)
        print(text)
            # [hex(x) for x in pn532.ntag2xx_read_block(read_block)])
    return rc


def wait_for_card():
    print('Waiting for RFID/NFC card...')
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is None:
            continue
        print('Found card with UID:', [hex(i) for i in uid])
        return uid

def convert_data(data):
    data = data + " "
    data_byte = data.encode('utf-8')
    print(len(data_byte))
    return data_byte


def write_preset_item(room):
    protocol = room['protocol']
    block_address = room['blockaddress']

    items = room['items']

    print('\nselect the item to tag with RFID\n')
    for item in items:
        print(item)

    item = input('\nselect Item: ')
    try:
        data = items[item]
        if not isinstance(data, list):
            print('data is not bytearray, needs to convert')
            data = convert_data(data)
    except ValueError as e:
        print(e)
        print('invalid selection or data')
        return 0

    data = bytearray(data)

    while len(data) < 16:
        data.append(0)

    if len(data) > 16:
        print('data is too long and need to be truncated')
        data = data[:16]

    print('datalength is: ' + str(len(data)))
    # since a string terminates with a 0 set it so...
    if data[15] is not 0:
        data[15] = 0



    print(data)
    uid = wait_for_card()

    write_with_check(block_address, data, protocol, uid)

    return 1


def select_room():
    print("\n\nSelect what room\n")
    for room in rooms:
        print(room)

    room = input("\ntype the room name\n")
    print(room + ' has been selected as room\n')
    room = rooms[room]
    return room


def handle_read(room, duplicate=False):
    try:
        protocol = room['protocol']
    except ValueError as e:
        print(e)
        print('invalid selection')
        return False

    print("waiting to read")
    uid = wait_for_card()
    if duplicate:
        # blocks multiple of 4-1 are used to store the keys, so we skip them
        block_addresses = filter(lambda x: (x+1) % 4 > 0, range(1, 64))
    else:
        block_addresses = [room["blockaddress"]]

    blocks_read = []
    for block_address in block_addresses:
        rc = read_card_block(uid, protocol, block_address)
        if not rc:
            print('could not read given block, possibly out of range for ' + str(block_address))
            break
        # since they provice RC and content in one variable ...
        blocks_read.append((block_address, rc))

    return blocks_read, uid



def main():

    room = select_room()

    while True:

        # modes would be read, write, duplicate, compare
        print("\n\n1: read \n2: write\n3: duplicate\n4: compare\n9: change room")
        mode = input("enter a number of what to do\n\n")

        valid_selection = False

        # readmode
        if mode == '1':
            valid_selection = True
            handle_read(room)
        if mode == '2':
            valid_selection = True
            rc = write_preset_item(room)
            if not rc:
                print('writing failed aborting')
            handle_read(room)

        if mode == '3':
            valid_selection = True
            print('Duplication mode: Place the RFID that should be Duplicated on the reader')
            blocks_read, uid_old = handle_read(room, True)

            if not blocks_read:
                print('failed to get content of the old card, aborting')
                return 0

            print('Place a new card to write content to')
            sleep(1)
            uid_new = wait_for_card()
            while uid_new == uid_old:
                print('card is still the same, place a new card on the reader')
                sleep(1)
                uid_new = wait_for_card()

            sleep(0.2)
            protocol = room['protocol']
            for block_address, block_content in blocks_read:
                print(block_content)
                print(type(block_content))
                print('attempting to write to address: ' + str(block_address))
                print('with content: ' + str(block_content))
                print('protocol: ' + str(protocol))
                print('uid_new: ' + str(uid_new))
                if not write_with_check(block_address, block_content, protocol, uid_new):
                    print('duplication failed!')
                    return 0


        if mode == '9':
            valid_selection = True
            room = select_room()

        if not valid_selection:
            print('invalid selection')




main()


'''
data = bytearray(b'asdf')
# write_with_check(6, data)

read_card()  
exit()
'''




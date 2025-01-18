import board
import busio
import RPi.GPIO as GPIO
from time import sleep

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A, BusyError
from adafruit_pn532.i2c import PN532_I2C

GPIO.cleanup()

classic_read_block = 1
ntag_read_block = 4


def rfid_present(pn532: PN532_I2C) -> bytearray:
    """
    checks if the card is present inside the box
    @return: (bytearray) with uid or empty value.
    """
    uid = b''
    if pn532:
        try:
            uid = pn532.read_passive_target(timeout=0.5)  # read the card
        except (RuntimeError, OSError, BusyError) as err:
            print(err)

    return uid


def authenticate(uid: bytearray, pn532: PN532_I2C) -> bool:
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    rc = False
    if pn532:
        try:
            rc = pn532.mifare_classic_authenticate_block(
                uid, classic_read_block, MIFARE_CMD_AUTH_A, key)
            print("classic card authenticate successfully")
        except Exception as e:
            #print(e)
            print("ntag needs no authentication")

    return rc


def rfid_read(uid: bytearray, pn532: PN532_I2C) -> str:
    """
    Reads data written on the card
    """
    read_data = "x"
    if not pn532:
        return read_data

    auth = authenticate(uid, pn532)

    try:
        # Switch between ntag and classic
        if auth:  # True for classic and False for ntags
            data = pn532.mifare_classic_read_block(classic_read_block)
        else:
            data = pn532.ntag2xx_read_block(ntag_read_block)

        if data:
            # get useful data only
            read_data = data.decode('utf-8').split().pop(0)
        else:
            read_data = "x"
            print("None block")

    except Exception as e:
        pass
        # print(e)

    return read_data.strip('\x00')


def get_rfid_configurations(pn532 : PN532_I2C) -> str:
    try:
        ic, ver, rev, support = pn532.firmware_version
        print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))
        sleep(0.5)
        pn532.SAM_configuration()  # Configure PN532 to communicate with cards
        print("we live")
        return "Found PN532 with firmware version: {0}.{1}".format(ver, rev)
    except Exception as err:
        print(err)
        print("failed to init rfid! try again")
        return "failed to init rfid! try again"


def init_rfid() -> PN532_I2C | None:
    # I2C connection:
    print("PN352 init loop")
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        sleep(1)
        pn532 = PN532_I2C(i2c, debug=False)  # <= always breaks here
        return pn532
    except Exception as err:
        print(err)
        print("failed to init rfid! try again")
        return None


def rfid_write(pn532: PN532_I2C, data: str, protocol: int=0) -> bool:
    if not pn532:
        print('RFID not initialized')
        return False

    data = bytearray(data.encode('utf-8'))

    while len(data) < 16:
        data.append(0)

    if len(data) > 16:
        print('data is too long and need to be truncated')
        data = data[:16]

    print('datalength is: ' + str(len(data)))
    # since a string terminates with a 0 set it so...
    if data[15] != 0:
        data[15] = 0

    print(data)

    uid = wait_for_card(pn532)
    try:
        if protocol == 4:  # NTAG
            data = data[:4]
            rc = pn532.ntag2xx_write_block(ntag_read_block, data)
        elif protocol == 0:  # Classic
            auth = authenticate(uid, pn532)
            sleep(0.5)
            if not auth:
                print('authentication failed, aborting process')
                return False
            rc = pn532.mifare_classic_write_block(classic_read_block, data)

        if not rc:
            print('writing failed... exiting')
            return False
        
    except Exception as e:
        print(e)
        return False

    print('return of write: ' + str(rc))

    return True


def wait_for_card(pn532: PN532_I2C) -> bytearray:
    print('Waiting for RFID/NFC card...')
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is None:
            continue
        print('Found card with UID:', [hex(i) for i in uid])
        return uid
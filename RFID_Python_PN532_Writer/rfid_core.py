import board
import busio
import RPi.GPIO as GPIO
from time import sleep

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A, BusyError
from adafruit_pn532.i2c import PN532_I2C

GPIO.cleanup()

classic_read_block = 1
ntag_read_block = 4

def rfid_present(pn532) -> bytearray:
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


def authenticate(uid, pn532) -> bool:
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


def rfid_read(uid, pn532) -> str:
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

    return read_data


def init_rfid() -> str:
    # I2C connection:
    print("PN352 init loop")
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        sleep(1)
        pn532 = PN532_I2C(i2c, debug=False)  # <= always breaks here
        ic, ver, rev, support = pn532.firmware_version
        print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))
        sleep(0.5)
        pn532.SAM_configuration()  # Configure PN532 to communicate with cards
        print("we live")
        return "Found PN532 with firmware version: {0}.{1}".format(ver, rev)
    except Exception as err:
        print(err)
        print("failed to init rfid! try again")
        return ""

class RFID:
    def __init__(self, cards=None, **config):
        if cards is None:
            cards = [0]
            
        self.name = config.get("name", "rfid")
        self.cards = cards
        
        # Requirment: default value is last in the list 
        self.data = {
            "data": str(cards[-1])
        }
        self.pn532 = None
        self.rfid_task = self.sio.start_background_task(self.init_rfid)
        self.rfid_task = self.sio.start_background_task(self.check_loop)

    def set_rfid_data(self, msg):
        print(f"override data to: {msg}")
        self.data["data"] = msg

    def get_data(self):
        return self.data

    def check_loop(self):
        while True:
            sleep(0.05)
            card_uid = rfid_present(self.pn532)
            if card_uid:
                print(f"Card found uid: {card_uid}")

                card_read = rfid_read(card_uid, self.pn532)

                # Remove prefix "P" <- POD related 
                if card_read.startswith("P"):
                    card_read = card_read[1:]

                print(f"Data on card: {card_read}")
                if card_read in self.cards:
                    self.data["data"] = card_read
                    print(f"chosen card: {card_read}")
                else:
                    print(f'Wrong data: {card_read}')

                # wait here until card is removed
                current_card = rfid_present(self.pn532)
                if card_read != "x":
                    while current_card and current_card == rfid_present(self.pn532):
                        continue
                
                    # Return to default value
                    self.data["data"] = str(self.cards[-1])
                    print("card removed")
                else:
                    print(f"data is: {card_read} , repeat checking..")
import base64
import struct
import hmac
import hashlib
import math
import pykeyboard
import time
from pykeyboard import PyKeyboardEvent
import Quartz
import time

secret = "1234567890XXXXXX"


def truncate(hmac_hash, offset) :
    four_bytes = hmac_hash[offset: offset + 4]
    big_endian, uint32 = ">", "I"
    fmt = big_endian + uint32
    return struct.unpack(fmt, four_bytes)[0]


def hash_offset(hmac_hash):
    last_byte = ord(hmac_hash[-1:])
    lower_4_bits = 0xf
    return last_byte & lower_4_bits


def token(hmac_hash, digit):
    offset = hash_offset(hmac_hash)
    raw_token = truncate(hmac_hash, offset)
    d = int(math.pow(10, digit))
    t = (raw_token & 0x7fffffff) % d
    return t


def counter_to_binary(c):
    big_endian, uint64 = ">", "Q"
    fmt = big_endian + uint64
    return struct.pack(fmt, c)


def hotp(secret, counter,  digit=6):
    s = base64.b32decode(secret, casefold=True)
    c = counter_to_binary(counter)
    hmac_hash = hmac.new(s, c, hashlib.sha1).digest()
    t = token(hmac_hash, digit)
    return str(t).zfill(digit)


def totp(secret, period=30):
    counter = int(time.time()) // period
    return hotp(secret, counter)


class Keyb(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.input = ""
        self.diagnostic = True
        self.k = pykeyboard.PyKeyboard()

    def handler(self, proxy, type, event, refcon):
        key = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        if type == Quartz.kCGEventKeyDown:
            if self.key_press(key, event):
                Quartz.CGEventSetType(event, Quartz.kCGEventNull)
        return event

    def key_press(self, key, event):
        ktbl = pykeyboard.mac.key_code_translate_table
        ctc = pykeyboard.mac.character_translate_table
        flags = Quartz.CGEventGetFlags(event)
        if flags & Quartz.kCGEventFlagMaskCommand\
                and not flags & Quartz.kCGEventFlagMaskAlternate \
                and not flags & Quartz.kCGEventFlagMaskControl \
                and not flags & Quartz.kCGEventFlagMaskShift:
            if key in ktbl and '0' == ktbl[key]:

                for x in totp(secret):
                    str_no = ctc[x]
                    event = Quartz.CGEventCreateKeyboardEvent(None, str_no, True)
                    flags = Quartz.CGEventGetFlags(event)
                    flags = flags & ~Quartz.kCGEventFlagMaskCommand
                    Quartz.CGEventSetFlags(event, flags)
                    Quartz.CGEventPost(0, event)
                return True
        return False


if __name__ == "__main__":
    print("start")
    ke = Keyb()
    ke.run()
    print("finish")



#!/usr/bin/env python3
import struct

# RC4 Python implementation from https://fr.wikipedia.org/wiki/RC4
class WikipediaARC4:
    def __init__(self, key=None):
        self.state = list(range(256))
        self.x = self.y = 0

        if key is not None:
            self.init(key)

    def init(self, key):
        for i in range(256):
            self.x = (key[i % len(key)] + self.state[i] + self.x) & 0xFF
            self.state[i], self.state[self.x] = self.state[self.x], self.state[i]
        self.x = 0

    def crypt(self, data):
        output = bytearray(len(data))
        for i in range(len(data)):
            self.x = (self.x + 1) & 0xFF
            self.y = (self.state[self.x] + self.y) & 0xFF
            self.state[self.x], self.state[self.y] = self.state[self.y], self.state[self.x]
            output[i] = data[i] ^ self.state[(self.state[self.x] + self.state[self.y]) & 0xFF]
        return bytes(output)


def rc4crypt(key, data):
    return WikipediaARC4(key).crypt(data)


def hexdump(data, start_addr=0):
    """Show an hexadecimal dump of the data"""
    for line_addr in range(0, len(data), 16):
        hexbytes = ''
        ascbytes = ''
        for col, x in enumerate(data[line_addr:line_addr + 16]):
            if col % 2 == 0:
                hexbytes += ' '
            hexbytes += '{:02x}'.format(x)
            ascbytes += chr(x) if 32 <= x < 127 else '.'
        print('{:04x}:{:40s} {}'.format(start_addr + line_addr, hexbytes, ascbytes))


def compute_checksum(data):
    """Custom Ndh2k15 checksum function"""
    result = 0x52415742
    for c in data:
        result = ((result + c) * 0xd34dbeef) & 0xffffffff
    return result


# Open the external flash
with open('extflash.bin', 'rb') as f:
    extflash = f.read()
assert len(extflash) == 256

# Check header signature and checksum
print("Header:")
hexdump(extflash[:16], 0)
assert extflash[:4] == b'NDHC'
cksum = compute_checksum(extflash[8:])
assert cksum == struct.unpack('<I', extflash[4:8])[0]
print("")

# Decrypt the badge
BASEKEY = extflash[8:16]
cleartext = b''
for pageaddr in range(0x10, 0x100, 8):
    decblk = rc4crypt(BASEKEY + struct.pack('B', pageaddr), extflash[pageaddr:pageaddr + 8])
    cleartext += decblk

print("Decrypted content:")
hexdump(cleartext, 16)
print("")

# Decrypt the final message
encmsg_key = b'\x03\x05\xff\xff\x30\x36\x31\x39\x31\x37\x38\x33'
message = rc4crypt(encmsg_key, cleartext[0x53 - 0x10:0xab - 0x10])
print("Final message: " + repr(message))

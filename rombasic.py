# -*- coding: utf-8 -*-
#!/usr/bin/env python3
 
import struct


# Address 	Length 	    Data Name Type
# 0xFFB0 	2 bytes 	Maker Code
# 0xFFB2 	4 bytes 	Game Code
# 0xFFB6 	7 bytes 	Fixed Value
# 0xFFBD 	1 byte 	    Expansion RAM Size
# 0xFFBE 	1 byte 	    Special Version
# 0xFFBF 	1 byte 	    Cartridge Type (Sub-number)
# 0xFFC0 	21 bytes 	Game Title Registration
# 0xFFD5 	1 byte 	    Map Mode
# 0xFFD6 	1 byte 	    Cartridge Type
# 0xFFD7 	1 byte 	    ROM Size
# 0xFFD8 	1 byte 	    RAM Size
# 0xFFD9 	1 byte 	    Destination Code
# 0xFFDA 	1 byte 	    Fixed Value
# 0xFFDB 	1 byte 	    Mask ROM Version
# 0xFFDC 	2 bytes 	Complement Check
# 0xFFDE 	2 bytes 	Check Sum 
# 
# Data Name Types
# ===============================================================================================================
# Maker Code
# Two alphanumeric ASCII bytes identifying your company. Ignored by emulators; for ROM hackers and homebrewers, just insert whatever.
# 
# Game Code
# Four alphanumeric ASCII bytes identifying your game. Ignored by emulators; for ROM hackers and homebrewers, just insert whatever.
# Exception: If the game code starts with Z and ends with J, it's a BS-X flash cartridge.
# 
# Fixed Value
# The fixed value bytes at $00FFB6-$00FFBC should be #$00. The fixed value byte at $00FFDA should be #$33.
# 
# Expansion RAM Size
# Should be #$00 for most roms. For the exception, see RAM Size.
#
# Special Version
# Should be #$00 normally. Can be set for promotional events.
# 
# Game Title Specification
# The game title is 21 bytes long, encoded with the JIS X 0201 character set (which consists of standard ASCII plus katakana). If the title is shorter than 21 bytes, then the remainder should be padded with spaces (0x20).
# 
# Cartridge Configuration
# Map Mode
# Common values: #$20 - 2.68MHz LoROM, #$21 - 2.68MHz HiROM, #$23 - SA-1; #$25 - 2.68MHz ExHiROM; #$30 - 3.58MHz LoROM, #$31 - 3.58MHz HiROM; #$35 - 3.58MHz ExHiROM
# 
# Cartridge Type
# Common values: #$00 - ROM only; #$01 - ROM and RAM; #$02 - ROM, RAM and battery; #$33 - ROM and SA-1; #$34 - ROM, SA-1 and RAM; #$35 - ROM, SA-1, RAM and battery
# 
# Sub-Number
# ROM Size
# 2^(this value) would be the size of the ROM in kilobytes. For example, for 512KB, this should be #$09.
# 
# RAM Size
# 2^(this value) would be the size of the SRAM (if present) in kilobytes. Maximum supported value is #$07.
# Exception: If you're using Super FX aka GSU-1, move this value to the Expansion RAM Size field, and put #$00 in this byte.
# 
# Destination Code
# Where the game is intended to be sold. Common values: #$00 - Japan; #$01 - USA; #$02 - Europe (enables 50fps PAL mode)
#
# Mask ROM Version
# Should be #$00, or increased every time you release a new ROM version.
# 
# ROM Verification
# 
# Complement Check
# This is the 16-bit complement (bit-inverse) of the checksum. This is used so that the checksum value cancels itself out when calculating the real checksum.
# 
# Check Sum
# This is simply the 16-bit sum of all bytes in the ROM. For power-of-2-sized ROMs, no mirroring is used, each byte of ROM is counted exactly once.
# For non-power-of-2-sized ROMs (e.g. 2.5MB or 6MB), first the checksum for the largest power-of-2 area smaller than the ROM size (so 4MB for 6MB ROMs, 2MB for 2.5MB ROMs) is computed normally. Then the remaining part is repeated until it's the same size as the first part (so the last 2MB of a 6MB ROM is repeated once so both halves are 4MB, and the last 512KB of a 2.5MB ROM is repeated 4 times so both halves are 2MB). Then its checksum is computed and the checksums of the 2 halves are added to get the final checksum. 

# open the file as binary read only
data = open('rom.sfc', 'rb')

# move the file pointer to the starting point of the header data
data.seek(0xFFB0)

# start reading one by one
maker_code, = struct.unpack('<2s', data.read(2))
game_code, = struct.unpack('<4s', data.read(4))
fixed_value, = struct.unpack('<7s', data.read(7))
expansion_ram_size, = struct.unpack('<b', data.read(1))
special_version, = struct.unpack('<b', data.read(1))
cartridge_type_sub, = struct.unpack('<b', data.read(1))
game_title, = struct.unpack('<21s', data.read(21))
map_code, = struct.unpack('<b', data.read(1))
cartridge_type, = struct.unpack('<b', data.read(1))
rom_size, = struct.unpack('<b', data.read(1))
ram_size, = struct.unpack('<b', data.read(1))
destination_code, = struct.unpack('<b', data.read(1))
fixed_value2, = struct.unpack('<b', data.read(1))
mask_rom_version, = struct.unpack('<b', data.read(1))
complement_check, = struct.unpack('<h', data.read(2))
checksum , = struct.unpack('<h', data.read(2))

# Two alphanumeric ASCII bytes identifying your company. 
# Ignored by emulators; for ROM hackers and homebrewers, just insert whatever.
print('Maker Code =', maker_code.decode('utf-8'))

# Four alphanumeric ASCII bytes identifying your game. 
# Ignored by emulators; for ROM hackers and homebrewers, just insert whatever.
# Exception: If the game code starts with Z and ends with J, it's a BS-X flash cartridge. 
print('Game Code =', game_code.decode('utf-8'))

# Should be #$00 for most roms. For the exception, see RAM Size. 
print('Expansion RAM Size =', expansion_ram_size)

# Should be #$00 normally. Can be set for promotional events. 
print('Special Version =', special_version)

# The game title is 21 bytes long, encoded with the JIS X 0201 
# character set (which consists of standard ASCII plus katakana). 
# If the title is shorter than 21 bytes, then the remainder should be padded with spaces (0x20). 
print('Game Title =', game_title.decode('utf-8'))

# Common values: 
# 0x20 - 2.68MHz LoROM
# 0x21 - 2.68MHz HiROM
# 0x23 - SA-1
# 0x25 - 2.68MHz ExHiROM
# 0x30 - 3.58MHz LoROM
# 0x31 - 3.58MHz HiROM
# 0x35 - 3.58MHz ExHiROM 
print('Map Code =', hex(map_code))

# Common values: 
# 0x0 - ROM only
# 0x1 - ROM and RAM
# 0x2 - ROM, RAM and battery
# 0x33 - ROM and SA-1
# 0x34 - ROM, SA-1 and RAM
# 0x35 - ROM, SA-1, RAM and battery 
print('Cartridge Type =', hex(cartridge_type))

# 2^(this value) would be the size of the ROM in kilobytes. For example, 
# for 512KB, this should be #$09. 
print('ROM Size =', 2 ** rom_size, 'kilobytes')

# 2^(this value) would be the size of the SRAM (if present) in kilobytes. 
# Maximum supported value is #$07.
# Exception: If you're using Super FX aka GSU-1, 
# move this value to the Expansion RAM Size field, and put #$00 in this byte. 
print('RAM Size =', 2 ** ram_size, 'kilobytes')

# Where the game is intended to be sold.
# Common values: 
# 0x0 - Japan
# 0x1 - USA 
# 0x2 - Europe (enables 50fps PAL mode) 
print('Destination Code =', hex(destination_code))

# Should be #$00, or increased every time you release a new ROM version. 
print('Mask ROM Version =', mask_rom_version)

# This is the 16-bit complement (bit-inverse) of the checksum. 
# This is used so that the checksum value cancels itself out when calculating the real checksum. 
print('Complement Check =', complement_check)

# This is simply the 16-bit sum of all bytes in the ROM. 
# For power-of-2-sized ROMs, no mirroring is used, each byte of ROM is counted exactly once. 
print('Checksum =', checksum)

# we can close the file now
data.close()
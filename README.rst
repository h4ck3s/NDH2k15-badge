NDH 2k15 Blackbadge Challenge
=============================

This repository contains files used to solve the challenge which was on the
Blackbadge of 2015' edition of the Nuit du Hack:

* ``dump.ihex`` contains the firmware and the bootloader which were on the badge.
* ``extflash.ihex`` contains the content of the external EEPROM after solving the games on the badge.
* ``writeup.tex`` is a write-up in French of the challenge, written in LaTeX.
* ``writeup.pdf`` is the compiled write-up.
* ``atmega32u4.py``, ``avr8bit_instructions.py`` and ``decode_firmware.py`` are
  Python3 scripts which were used to reverse-engineer the firmware.  The output
  of ``decode_firmware.py`` is provided in ``dump.disassembled.txt``.
* ``decode_extflash.py`` is a Python3 script which decrypts the content of the
  external memory (``extflash.ihex``).  Its output is provided in
  ``extflash.decoded.txt``.
* ``Makefile`` allows using ``make`` command to build the generated files.


External links:
* https://github.com/virtualabs/Ndh15Badge-library/ An Arduino library to program the badge.
* https://twitter.com/hackerzvoice/status/609854354913366016 a picture of the badge.

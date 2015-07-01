#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Nicolas Iooss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
@author: Nicolas Iooss
@license: MIT
"""
import os.path
import sys
from atmega32u4 import ATmega32U4Meta, Label


LABELS = [
    Label(0x00ac, 'J', 'jumptable_00ac?'),
    Label(0x00e4, 'D', '?'),

    Label(0x0302, 'J', 'constructors_tables'),

    Label(0x030a, 'C', 'boot()'),
    Label(0x0316, 'c', 'copy .data to RAM[0x100..0x65a]'),
    Label(0x0332, 'c', 'Zero-ize RAM[0x65a..0x89f]'),
    Label(0x033e, 'c', 'Use jumptable 0x302..0x30a'),

    Label(0x035a, 'C', 'bad_interrupt'),

    # *********************************************************************

    Label(0x035e, 'C', 'int32_t checksum(byte *data=r25:r24, uint size=r23:r22)->r25:r24:r23:r22'),
    Label(0x0374, 'c', 'r = 0x52415742'),  # RAWB
    Label(0x037c, 'C', '_for(r31:r30 in data..data+size)'),
    Label(0x0396, 'c', 'r21:r20:r19:r18 = r + *(r31:r30)'),
    Label(0x039a, 'c', 'r = r21:r20:r19:r18 * 0xd34dbeef'),

    Label(0x03ba, 'C', 'world_war_simulation'),
    Label(0x044a, 'c', 'Read a char into [SP+1+r17:r16] ; r17:r16=0..7'),
    Label(0x0466, 'C', '_readcode_end'),
    Label(0x046c, 'c', 'Read last char...'),
    Label(0x0486, 'c', 'r17:r16 = SP+1, r19:r18 = SP+9=end of inputbuffer'),
    Label(0x048a, 'C', '_char_is_\\r_or_\\n'),
    Label(0x0498, 'C', '_loop_check_alldigits'),
    Label(0x04ac, 'C', '_loop_check_alldigits_ok'),
    # ...
    Label(0x057e, 'C', '_print_r23:r22_and_ret'),
    Label(0x0586, 'C', '_ret'),

    Label(0x05a4, 'C', 'show_victory_if_complete_and_mode3()'),

    Label(0x0636, 'C', 'rc4_init(uint8 rc4State[256]=r25:r24, uint8* key=r23:r22, keylen=r21:r20)'),
    Label(0x0664, 'c', 'fill 256 bytes of r25:r24 with 0,1,2,3...'),
    Label(0x067e, 'C', '_for(r31:r30 in 0..0xff)'),
    Label(0x06c8, 'C', '_return 1'),
    Label(0x06cc, 'C', '_ret'),

    Label(0x06e2, 'C', 'rc4_crypt(uint8 rc4State[256]=r25:r24, uint8* data=r23:r22, len=r21:r20)'),
    Label(0x0742, 'c', '*(r27:r26 ++) ^= RC4_PRGA(...)'),

    Label(0x0760, 'C', 'quizz_game()'),
    Label(0x0784, 'c', 'Copy 5 question addresses into [SP+0x41..]'),
    Label(0x079e, 'c', 'Load quizz question number into [SP+0x4b]'),
    Label(0x094c, 'C', '_game_won'),

    Label(0x09be, 'C', 'fortune_game()'),

    Label(0x0cdc, 'C', 'Chall::Chall(r25:r24=this)'),

    Label(0x0cee, 'C', 'Chall::checksum(r25:r24=this, r23:r22=data, r21:r20=size)->r25:r24:r23:r22'),

    Label(0x0d4a, 'C', 'Chall::check_extflashmem()'),
    Label(0x0d9a, 'c', 'First 4 bytes at page 0 are "NDHC"'),
    Label(0x0da6, 'c', 'Read the 0xf8 bytes after the first 8 in a buffer'),
    Label(0x0ddd, 'c', 'Read 4 bytes from addr 4...'),
    Label(0x0e2c, 'C', '_return 0'),
    Label(0x0e32, 'C', '_return 2'),
    Label(0x0e36, 'C', '_ret'),

    Label(0x0e58, 'C', 'Chall::genkey(this=r25:r24, r22=pageaddr, r21:r20=keybuffer[9])'),
    Label(0x0e58, 'c', 'Copy 8 bytes from this+0x100 to buffer...'),
    Label(0x0e6c, 'c', '... and put r22 after ; return 0'),

    Label(0x0e76, 'C', 'Chall::read_from_encextflash(r22=pageaddr, r21:r20=buffer, r19:r18=size)'),
    Label(0x0eac, 'c', 'save args: r13:r12=this, r17=pageaddr, r11:r10=buffer, r15:r14=size'),
    Label(0x0ec0, 'c', 'read into [SP+10] flash[arg_addr & 0xf8 ..+8]'),
    # ...
    Label(0x0f58, 'C', '_read_aligned_page_on_8bytes'),
    Label(0x0f6c, 'c', 'r5:r4 = (size + 7) / 8'),
    Label(0x0f94, 'c', 'Read 8 bytes from extflash page r23=r2+r16 into r11:r10[r17:r16..]'),
    Label(0x1060, 'C', '_ret'),

    Label(0x1092, 'C', 'Chall::read_1b_from_encextflash(r22=pageaddr, r21:r20=buffer)'),
    Label(0x109a, 'C', 'Chall::read_2b_from_encextflash(r22=pageaddr, r21:r20=buffer)'),
    Label(0x10a2, 'C', 'Chall::read_4b_from_encextflash(r22=pageaddr, r21:r20=buffer)'),

    Label(0x10aa, 'C', 'Chall::write_to_encextflash(r25:r24=this, r22=pageaddr, r21:r20=data, r19:r18=size)'),

    Label(0x133e, 'C', 'Chall::write_int8_to_encextflash(r22=pageaddr, r20)'),
    Label(0x1364, 'C', 'Chall::write_int16_to_encextflash(r22=pageaddr, r21:r20)'),

    Label(0x138a, 'C', 'Chall::write_all_extflashmem(data@stack, size is 0xf8)'),

    Label(0x1468, 'C', 'cons4_Chall'),

    Label(0x1470, 'C', 'accelero_labygame()'),
    Label(0x148a, 'C', '_repeat_16_times'),
    Label(0x14a6, 'c', 'r17:r16 += (accel_x + (3 if accel_x<0)/4'),
    Label(0x14be, 'c', 'r29:r28 += (accel_y + ...)/4'),
    Label(0x14d6, 'c', 'accX = r19:r18 = (acc_accel_x + (15 if < 0)) / 16 ; signed div'),
    Label(0x14e6, 'c', 'accY = r25:r24 = signeddiv(acc_accel_y / 16)'),
    Label(0x14f6, 'C', '_(accX < -50)'),
    Label(0x14fc, 'c', 'accX < -50 && accY < 20 => move 2'),
    Label(0x1504, 'C', '_(accX >= -50)'),
    Label(0x150a, 'C', '_(accX >= 51)'),
    Label(0x1510, 'C', '_(accX >= 51 && accY < 20)'),
    Label(0x1516, 'c', 'accX >= 51 && -19 <= accY < 20 => move 1'),
    Label(0x1518, 'C', '_((accX < -50 && accY >= 20) || (-50 <= accX < 51) || (accX >= 51 && accY < -19)'),
    Label(0x1526, 'c', '... && accY < -50 && accX < 20 => move 4'),
    Label(0x152e, 'C', '_((accX >=51 && accY >= 20) || (... && accY >= -50)'),
    Label(0x153a, 'c', '... && accX < 20 => move 3'),
    Label(0x1540, 'C', '_???1540'),
    Label(0x154c, 'C', '_((1540) && accX < 20)'),
    Label(0x1550, 'c', '(1540) && accX < 20 && accY < -20 => move 0'),
    Label(0x1554, 'C', '_move0'),
    Label(0x155a, 'C', '_move2'),
    Label(0x1560, 'C', '_move1'),
    Label(0x1566, 'C', '_move4'),
    Label(0x156c, 'C', '_move3'),
    Label(0x15a8, 'c', 'on end, return 1'),
    Label(0x15c2, 'C', '_go to next pos'),
    Label(0x15d4, 'C', '_fail_reset_labystate'),
    Label(0x15e4, 'C', '_return 0'),
    Label(0x15e8, 'C', '_ret'),

    Label(0x15f6, 'C', 'read_gamemode_from_flash()->r24'),

    Label(0x161a, 'C', 'write_gamemode_to_flash(r24)'),

    Label(0x1630, 'C', 'format_hexbyte(r24=byte, r23:r22=char[3] buffer)'),
    Label(0x1644, 'c', 'Copy "0123456789ABCDEF" into [SP+1+...]'),
    Label(0x166a, 'c', '(r23:r22)[0] = hexencode(high nibble of r24)'),
    Label(0x167c, 'c', '(r23:r22)[1] = hexencode(low nibble of r24)'),

    Label(0x1696, 'C', 'dump_memory()...'),

    Label(0x17be, 'C', 'dump_mem_if_mode2()'),

    Label(0x17d0, 'C', 'print_menu_choosegame()'),

    Label(0x183e, 'C', '?copy_serial_to_flash?()'),
    Label(0x18ce, 'C', '?copy_flash_to_serial?()'),

    Label(0x193c, 'C', 'setup()'),
    Label(0x1996, 'C', '_mem_is_ok'),

    Label(0x1a00, 'C', 'loop()'),
    Label(0x1a14, 'C', '_input_available'),
    Label(0x1a32, 'C', '_process_inchar_r28'),
    Label(0x1a54, 'C', '_menu-2_fortunegame'),
    Label(0x1a5a, 'C', '_(r28 >= \'3\')'),
    Label(0x1a6a, 'C', '_menu-1_quizzgame'),
    Label(0x1a70, 'C', '_menu-3_wargame'),
    Label(0x1a76, 'C', '_menu-h_infos'),
    Label(0x1af8, 'C', '_menu-m_dumpmem'),
    Label(0x1b0a, 'C', '_println_and_print_menu'),
    Label(0x1b16, 'C', '_print_menu'),
    Label(0x1b18, 'C', '_process_labygame'),
    Label(0x1b26, 'C', '_won_labygame_blink_3times_R100'),
    Label(0x1b6e, 'C', '_read_tooth_button'),
    Label(0x1ba6, 'C', '_blink_mode3_B500_-100_B500_-100_B500_-100'),
    Label(0x1c40, 'C', '_blink_mode0_G500_-100_G500_-100_G500_-500'),
    Label(0x1ca6, 'C', '_blink_mode1_G500_R500_G500_-500'),
    Label(0x1cd6, 'C', '_delay(...)_blink_G500_-500'),
    Label(0x1d0c, 'C', '_blink_mode2_R400_G400_B400_-400'),
    Label(0x1d70, 'C', '_ret_delay(r25:r24:r23:r22)'),
    Label(0x1d78, 'C', '_ret'),

    # *********************************************************************
    # Arduinohardware/arduino/avr/libraries/Wire/Wire.cpp
    Label(0x1d7e, 'C', 'int TwoWire::available(void)'),
    Label(0x1d8e, 'C', 'int TwoWire::read(void)'),
    Label(0x1db6, 'C', 'int TwoWire::peek(void)'),
    Label(0x1dd4, 'C', 'void TwoWire::flush(void)'),
    Label(0x1dd6, 'C', 'size_t TwoWire::write(const uint8_t *data, size_t quantity)'),
    Label(0x1e36, 'C', 'size_t TwoWire::write(uint8_t data)'),
    Label(0x1e94, 'C', 'TwoWire::TwoWire()'),
    Label(0x1eb4, 'C', 'void TwoWire::begin(void)'),
    Label(0x1ec8, 'C', 'uint8_t TwoWire::requestFrom(uint8_t address, uint8_t quantity, uint8_t sendStop)'),
    Label(0x1ee2, 'C', 'uint8_t TwoWire::requestFrom(int address, int quantity)'),
    Label(0x1ee8, 'C', 'void TwoWire::beginTransmission(uint8_t address)'),
    Label(0x1efc, 'C', 'void TwoWire::beginTransmission(int address)'),
    Label(0x1f00, 'C', 'uint8_t TwoWire::endTransmission(uint8_t sendStop)'),
    Label(0x1f26, 'C', 'uint8_t TwoWire::endTransmission(void)'),
    Label(0x1f2c, 'C', 'cons3_Wire'),

    # *********************************************************************
    # Arduino hardware/arduino/avr/libraries/Wire/utility/twi.c
    Label(0x1f34, 'C', 'twi_init()'),
    Label(0x1f70, 'C', 'uint8_t twi_readFrom(uint8_t address, uint8_t* data, uint8_t length, uint8_t sendStop)'),
    Label(0x1ff8, 'C', 'uint8_t twi_writeTo(uint8_t address, uint8_t* data, uint8_t length, uint8_t wait, uint8_t sendStop)'),
    Label(0x209c, 'C', 'uint8_t twi_transmit(const uint8_t* data, uint8_t length)'),

    # *********************************************************************
    Label(0x20ee, 'C', 'int24'),

    # *********************************************************************
    # Ndh Badge
    Label(0x2348, 'C', 'void Ndh15Badge::play(long freq, long duration)'),
    Label(0x2416, 'C', 'void Ndh15Badge::adc_channel(uint8_t channel)'),
    Label(0x242a, 'C', 'uint16_t Ndh15Badge::adc_get(void)'),
    Label(0x2450, 'C', 'uint16_t Ndh15Badge::touch_measure(uint8_t pin)'),
    Label(0x24d4, 'C', 'int Ndh15Badge::button(int pin)'),
    Label(0x2502, 'C', 'void Ndh15Badge::led(byte red=r22, byte green=r20, byte blue=r18)'),
    Label(0x254e, 'C', 'int Ndh15Badge::readX(void)'),
    Label(0x2556, 'C', 'int Ndh15Badge::readY(void)'),
    Label(0x255e, 'C', 'void Ndh15Badge::accelero_send(unsigned char reg_addr, unsigned char data)'),
    Label(0x25a0, 'C', 'void Ndh15Badge::begin(void)'),
    Label(0x2646, 'C', 'int Ndh15Badge::writePage(uint8_t paddr, byte *pdata, int length)'),
    Label(0x26be, 'C', 'int Ndh15Badge::readPage(uint8_t paddr=r22, byte *pdata=r21:r20, int length=r19:r18)'),
    Label(0x273e, 'C', 'void Ndh15Badge::accelero_read(uint8_t reg_addr)'),
    Label(0x2820, 'C', 'void Ndh15Badge::updateAccel(void)'),
    Label(0x2826, 'C', 'void Ndh15Badge::??led(led, value)'),

    # *********************************************************************
    # Arduino hardware/arduino/avr/cores/arduino/wiring.c
    Label(0x2942, 'C', 'TIMER0_OVF_vect'),
    Label(0x29d6, 'C', 'unsigned long micros()'),
    Label(0x2a20, 'C', 'void delay(unsigned long ms)'),
    Label(0x2a6c, 'C', 'void delayMicroseconds(unsigned int us)'),
    Label(0x2a80, 'C', 'void init()'),

    # *********************************************************************

    Label(0x2b9e, 'C', 'pinMode(r24=pin, r22=value)'),

    Label(0x2c16, 'C', 'digitalWrite(r24=pin, r22=value)'),


    # *********************************************************************
    # Arduino hardware/arduino/avr/cores/arduino/Print.cpp
    Label(0x2c76, 'C', 'size_t Print::write(const uint8_t *buffer=r23:r22, size_t size)'),
    Label(0x2cc6, 'C', 'size_t Print::write(const char *str)'),
    Label(0x2cf0, 'C', 'size_t Print::print(const char str[]=r23:r22)'),
    Label(0x2cf4, 'C', 'size_t Print::print(char c=r22)'),
    Label(0x2d02, 'C', 'size_t Print::println(void)'),
    Label(0x2d2a, 'C', 'size_t Print::println(const char c[]=r23:r22)'),
    Label(0x2d4e, 'C', 'size_t Print::printNumber(unsigned long n=r23:r22:r21:r20, uint8_t base=r19:r18)'),
    Label(0x2dfa, 'C', 'size_t Print::print(long n=r23:r22:r21:r20, int base=r19:r18)'),
    Label(0x2e8e, 'C', 'size_t Print::print(unsigned int n=r23:r22, int base=r21:r20)'),
    Label(0x2e9e, 'C', 'size_t Print::print(unsigned long n=r23:r22:r21:r20, int base=r19:r18)'),
    Label(0x2eb8, 'C', 'size_t Print::println(unsigned long num, int base)'),

    # *********************************************************************

    Label(0x2edc, 'C', 'int Serial?::available()'),  # read buffer 64 bytes
    Label(0x2ef6, 'C', 'int Serial?::peek()'),
    Label(0x2f24, 'C', 'int Serial?::read()'),

    Label(0x2f6a, 'C', 'Serial.?(vtable6)'),

    Label(0x2fb6, 'C', 'void Serial_::flush(void)'),

    # *********************************************************************
    # Arduino hardware/arduino/avr/cores/arduino/CDC.cpp
    Label(0x2fbc, 'C', 'size_t Serial_::write(uint8_t c)'),

    Label(0x30ca, 'C', 'Serial.nullsub'),

    Label(0x30cc, 'C', 'cons2_Serial'),

    # *********************************************************************
    # Arduino hardware/arduino/avr/cores/arduino/main.cpp
    Label(0x30ee, 'C', 'main()'),

    # *********************************************************************
    # Arduino hardware/arduino/avr/cores/arduino/CDC.cpp
    Label(0x3248, 'C', 'size_t Serial_::write(const uint8_t *buffer, size_t size)'),

    Label(0x3462, 'C', 'int0b'),

    Label(0x36b4, 'C', 'void USB_Flush(uint8_t ep)'),

    Label(0x36c8, 'C', 'USBDevice.attach'),

    Label(0x3708, 'C', 'int0a'),

    Label(0x37c6, 'C', 'sub?vtable?_37c6'),
    Label(0x38ac, 'C', 'sub?vtable?_38ac'),
    Label(0x3982, 'C', 'sub?vtable?_3982'),
    Label(0x3a0a, 'C', 'sub?vtable?_3a0a'),

    Label(0x3a24, 'C', 'cons1_?'),


    # *********************************************************************
    # libgcc

    Label(0x3a3a, 'C', 'libgcc.mulsi3(A=r25:r24:r23:r22, B=r21:r20:r19:r18)->r25:r24:r23:r22=A*B'),

    Label(0x3a5a, 'C', 'libgcc.udivmodhi4(dividend=r25:r24, divisor=r23:r22)->25:r24=r,r23:r22=q'),

    Label(0x3a82, 'C', 'libgcc.divmodhi4(dividend=r25:r24, divisor=r23:r22)->25:r24=r,r23:r22=q'),

    Label(0x3aaa, 'C', 'libgcc.udivmodsi4(dividend=r25:r24:r23:r22, divisor=r21:r20:r19:r18)->r25:r24:r23:r22=r,r21:r20:r19:r18=q'),

    Label(0x3aee, 'C', 'libgcc.divmodsi4(dividend=r25:r24:r23:r22, divisor=r21:r20:r19:r18)->r25:r24:r23:r22=r,r21:r20:r19:r18=q'),

    Label(0x3b2c, 'C', 'jump_indirect_to_PROG[r31:r30*2]'),

    Label(0x3b38, 'C', 'libgcc.muluhisi3(A=r27:r26, B=r21:r20:r19:r18)->r25:r24:r23:r22=A*B'),

    Label(0x3b4e, 'C', 'libgcc.umulhisi3(A=r27:r26, B=r19:r18)->r25:r24:r23:r22=A*B'),

    Label(0x3b6c, 'C', 'libgcc.atoi(r25:r24=str)->r25:r24=number'),
    Label(0x3b96, 'C', '_read_+'),
    Label(0x3b98, 'C', '_read_digit'),

    Label(0x3ba8, 'C', 'libgcc.strncmp(r25:r24=s1, r23:r22=s2, r21:r20=n)->r24'),

    Label(0x3bc4, 'C', 'mul_by_10(r25:r24)->r25:r24'),

    Label(0x3bd4, 'C', 'halt'),

    # *********************************************************************
    # .data = 0x3bd8 ..+0x65a-0x100=0x4112

    Label(0x3bd8, 'D', 'gamemode_addresses'),
    Label(0x3bea, 'D', 'quizz_questions'),
    Label(0x3bf4, 'D', '"=============================================="'),
    Label(0x3c23, 'D', '"              World War Simulation"'),
    Label(0x3c46, 'D', '"=====================\\o/======================"'),
    Label(0x3c75, 'D', '"Enter access code to launch nuclear strike: "'),
    Label(0x3ca2, 'D', '"- ERROR -"'),
    Label(0x3cb0, 'D', '"Read serial:"'),
    Label(0x3cbd, 'D', '"Expecting: "'),
    Label(0x3cc9, 'D', '"- MISSILES LAUNCHED, ENJOY -"'),
    Label(0x3cea, 'D', '"!!! GOD MODE ENABLED !!!"'),
    Label(0x3d03, 'D', '"Quizz> answer \'q\' to quit the game, names start with a capital letter."'),
    Label(0x3d4a, 'D', '"You won this game !"'),
    Label(0x3d5e, 'D', '"Quizz> "'),
    Label(0x3d66, 'D', '"Question "'),
    Label(0x3d70, 'D', '"Correct."'),
    Label(0x3d79, 'D', '" Next question."'),
    Label(0x3d89, 'D', '"Nope, try again."'),
    Label(0x3d9a, 'D', '"What is the Answer to the Ultimate Question of Life, The Universe, and Everything ?"'),
    Label(0x3dee, 'D', '"What is the main town of Assyria ?"'),
    Label(0x3e11, 'D', '"Uncipher this: 413532 541215 244422 1154"'),
    Label(0x3e3a, 'D', '"Can you name Gibson\'s *cold* intelligence ?"'),
    Label(0x3e66, 'D', '"Who reads Playboy in the movie \'Sneakers\' ?"'),
    Label(0x3e92, 'D', '"Fortune> Get 65535 coins to win this game. Enter \'q\' to quit."'),
    Label(0x3ed0, 'D', '"Fortune> You have "'),
    Label(0x3ee3, 'D', '"You won this game."'),
    Label(0x3ef6, 'D', '"Fortune> Bet on number (0-9): "'),
    Label(0x3f12, 'D', '": "'),
    Label(0x3f15, 'D', '"Fortune> Number of coins to bet: "'),
    Label(0x3f37, 'D', '"Fortune> Lucky you ! You\'ve been rewarded with "'),
    Label(0x3f67, 'D', '" coins !"'),
    Label(0x3f70, 'D', '"Fortune> Nope, you lost "'),
    Label(0x3f89, 'D', '" coins ..."'),
    Label(0x3f94, 'D', '"Fortune> You don\'t have enough coins."'),
    Label(0x3fba, 'D', '"0123456789ABCDEF"'),
    Label(0x3fcb, 'D', '"Memory> Dumping ..."'),
    Label(0x3fdf, 'D', '"> Shall we play a game ?"'),
    Label(0x3ffb, 'D', '"\\r\\n"'),
    Label(0x3ffd, 'D', '""'),
    Label(0x3ffe, 'D', '" 1 - Quizz"'),
    Label(0x4009, 'D', '" 2 - Fortune"'),
    Label(0x4016, 'D', '" 3 - Wargame"'),
    Label(0x4023, 'D', '" h - Badge infos"'),
    Label(0x4036, 'D', '" m - Dump memory"'),
    Label(0x4049, 'D', '"Choice: "'),
    Label(0x4054, 'D', '"XXX MEMORY CORRUPTION DETECTED XXX"'),
    Label(0x4077, 'D', '"<< Ndh2015 - National LOL Agency >>"'),
    Label(0x409f, 'D', '"BADGE INFOS:"'),
    Label(0x40ac, 'D', '"------------"'),
    Label(0x40b9, 'D', '"Current mode: "'),
    Label(0x40c8, 'D', '"DUMMY"'),
    Label(0x40ce, 'D', '"ROOKIE"'),
    Label(0x40d5, 'D', '"NINJA"'),
    Label(0x40db, 'D', '"GOD"'),

    Label(0x40df, 'D', 'accelero_laby'),

    Label(0x4105, 'J', 'TwoWire_vtable'),
    Label(0x4111, 'D', 'padding'),
    Label(0x4115, 'J', 'Serial_vtable'),
    Label(0x4123, 'D', 'padding'),
    Label(0x4127, 'J', '?2_vtable'),
    Label(0x4131, 'D', 'padding'),

    Label(0x4132, 'p'),  # ff padding
]

for i, lab in enumerate(LABELS):
    if i + 1 < len(LABELS):
        nextlab = LABELS[i+1]
        if lab.addr > nextlab.addr or (lab.addr == nextlab.addr and nextlab.labtype != 'c'):
            sys.stderr.write("Invalid label ordering between {} and {}\n".format(lab, nextlab))
            sys.exit(1)

# Add SRAM labels for data section
SRAM_LABELS = [
    Label(0x065a, 'R', 'Chall'),  # Challenge object, rc4state[256]
    Label(0x075a, 'R', 'Chall.keybuffer[0]'),  # RC4 key, Size 8, until 0x762

    Label(0x0762, 'R', 'laby_curpos_L'),
    Label(0x0763, 'R', 'laby_curpos_H'),
    Label(0x0764, 'R', 'laby_lastmove_L'),
    Label(0x0765, 'R', 'laby_lastmove_H'),

    Label(0x0766, 'R', 'state_L'),
        # < 0  : have "Badge infos" item
        # >= 2 : have "Dump memory" item
    Label(0x0767, 'R', 'state_H'),

    Label(0x0768, 'R', 'Wire'),  # TwoWire instance

    Label(0x0774, 'R', 'TwoWire::transmitting'),
    Label(0x0775, 'R', 'TwoWire::txBufferLength'),
    Label(0x0776, 'R', 'TwoWire::txBufferIndex'),

    Label(0x0797, 'R', 'TwoWire::txAddress'),
    Label(0x0798, 'R', 'TwoWire::rxBufferLength'),
    Label(0x0799, 'R', 'TwoWire::rxBufferIndex'),
    Label(0x079a, 'R', 'TwoWire::rxBuffer[0]'),  # Size 0x20

    Label(0x0824, 'R', 'twi_inRepStart'),
    Label(0x0825, 'R', 'twi_sendStop'),
    Label(0x0827, 'R', 'twi_state'),

    Label(0x0828, 'R', 'Badge'),  # Ndh15Badge instance

    Label(0x082e, 'R', 'timer0_fract'),
    Label(0x082f, 'R', 'timer0_millis_LL'),
    Label(0x0830, 'R', 'timer0_millis_LH'),
    Label(0x0831, 'R', 'timer0_millis_HL'),
    Label(0x0832, 'R', 'timer0_millis_HH'),
    Label(0x0833, 'R', 'timer0_overflow_count_LL'),
    Label(0x0834, 'R', 'timer0_overflow_count_LH'),
    Label(0x0835, 'R', 'timer0_overflow_count_HL'),
    Label(0x0836, 'R', 'timer0_overflow_count_HH'),

    Label(0x0837, 'R', 'Serial'),  # Serial_ (USBAPI CDC) instance, inherit Stream
    Label(0x0845, 'R', 'Serial_._rx_buffer[0]'), # Size 0x40
    Label(0x0885, 'R', 'Serial_._rx_buffer_head_L'),
    Label(0x0886, 'R', 'Serial_._rx_buffer_head_H'),
    Label(0x0887, 'R', 'Serial_._rx_buffer_tail_L'),
    Label(0x0888, 'R', 'Serial_._rx_buffer_head_H'),

    Label(0x0889, 'R', 'UsbDevice'),

    Label(0xaff, 'R', '__stack'),
]

for lab in LABELS:
    if 0x3bd8 <= lab.addr < 0x3bd8 + 0x65a - 0x100 and lab.name:
        SRAM_LABELS.append(Label(lab.addr - 0x3bd8 + 0x100, 'R', lab.name))
LABELS += SRAM_LABELS

def decode(filepath, labels):
    with open(filepath, 'rb') as f:
        fwmem = f.read()
    assert fwmem

    meta = ATmega32U4Meta(fwmem, labels)

    # First pass: find every code label
    brdict = meta.get_branch_targets()
    for addr, is_call in brdict.items():
        if addr not in meta.labels:
            name = '{}_{:04x}'.format('sub' if is_call else '_loc', addr)
            if addr < 0x10000:
                meta.labels[addr] = Label(addr, 'C', name)

    # Second pass: dump everything
    meta.show_all()

if __name__ == '__main__':
    decode(os.path.join(os.path.dirname(__file__), 'dump.bin'), LABELS)

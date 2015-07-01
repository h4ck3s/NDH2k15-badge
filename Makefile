all: dump.disassembled.txt extflash.decoded.txt writeup.pdf

%.bin: %.ihex
	objcopy -I ihex -O binary $< $@

dump.disassembled.txt: dump.bin atmega32u4.py avr8bit_instructions.py  decode_firmware.py
	python3 ./decode_firmware.py > $@.tmp
	rm -f $@
	mv $@.tmp $@

extflash.decoded.txt: extflash.bin decode_extflash.py
	python3 ./decode_extflash.py > $@.tmp
	rm -f $@
	mv $@.tmp $@

writeup.pdf: writeup.tex
	latexmk -pdf $<

.PHONY: all

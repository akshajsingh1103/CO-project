sim: 
	python3 Simulator.py code.bin output
	cat output

asm:
	python3 Assembler.py code.asm code.bin
	cat code.bin


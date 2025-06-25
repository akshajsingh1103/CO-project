import sys
import re

# NOTE:
# Instructions Completed
#   R Type
#   I Type
#   S Type
#   B Type
#   U Type
#   J Type
#   Bonus
# Instructions Left
#   NaN

#   R type instructions
#
#   f7      rs2     rs1     f3      rd      opcode
#   31:25   24:20   19:15   14:12   11:07   06:00
#   00:07   07:12   12:17   17:20   20:25   25:32

#   I type instructions
#
#   imm     rs1     f3      rd      opcode
#   31:20   19:15   14:12   11:07   06:00
#   00:12   12:17   17:20   20:25   25:32

#   S type instructions
#
#   imm1    rs2     rs1     f3      imm2    opcode
#   31:25   24:20   19:15   14:12   11:7    6:0
#   00:07   07:12   12:17   17:20   20:25   25:32

#   B type instructions
#
#   imm1    rs2     rs1     f3      imm2    opcode
#   31:25   24:20   19:15   14:12   11:7    6:0
#   00:07   07:12   12:17   17:20   20:25   25:32

#   U type instructions

#   imm     rd      opcode
#   31:12   11:07   6:0
#   00:20   20:25   25:32

#   J type instructions

#   imm     rd      opcode
#   31:12   11:07   6:0
#   00:20   20:25   25:32

#   Bonus
#   rs2     rs1     rd
#   24:20   19:15   11:7
#   07:12   12:17   20:25

# clears the output file
with open(sys.argv[2], "w") as f:
    something = "" 

reg_val = {}
for i in range(32):
    reg_val[f"x{i}"] = 32*"0"

reg_encoding = {
    "00000" : "x0",
    "00001" : "x1",
    "00010" : "x2",
    "00011" : "x3",
    "00100" : "x4",
    "00101" : "x5",
    "00110" : "x6",
    "00111" : "x7",
    "01000" : "x8",
    "01001" : "x9",
    "01010" : "x10",
    "01011" : "x11",
    "01100" : "x12",
    "01101" : "x13",
    "01110" : "x14",
    "01111" : "x15",
    "10000" : "x16",
    "10001" : "x17",
    "10010" : "x18",
    "10011" : "x19",
    "10100" : "x20",
    "10101" : "x21",
    "10110" : "x22",
    "10111" : "x23",
    "11000" : "x24",
    "11001" : "x25",
    "11010" : "x26",
    "11011" : "x27",
    "11100" : "x28",
    "11101" : "x29",
    "11110" : "x30",
    "11111" : "x31"
}

# Memory Stats
mem_val = {}
for i in range(32):
    mem_val[65536+4*i] = 32*"0"

# padding hex numbers e.g. 1C to 0x0000...0001C
def hex_padding(string, num):
    string = str(string)
    while len(string) < num:
        string = "0" + string
    return f"0x{string}"

# pad the string with <num> MSBs
def padding(string, num):
    msb = string[0]
    while len(string) < num:
        string = str(msb) + string
    return str(string)

# pass as int cuz
# but it returns as a string
def decimalToBinary(dec, signed = True):
    temp = ""
    if dec == 0:
        return str(0)
    elif dec > 0:
        bin_s = ""
        while dec > 0:
            bin_s += str(dec % 2)
            dec = dec // 2
        bin_i = int(bin_s[::-1])
        return str("0" + str(bin_i)) if str(bin_i)[0] == "1" and signed == True else bin_i
    else:
        if signed:
            for i in str(decimalToBinary(int(str(dec)[1:]), False)):
                temp += "0" if i == "1" else "1"
            plus_1 = str(decimalToBinary(binaryToDecimal(temp)+1, False))

            # added zeros as padding
            plus_1 = plus_1[::-1]
            while len(temp) != len(plus_1):
                plus_1 += "0"
            plus_1 = plus_1[::-1]
            return str("1" + plus_1)
        elif not signed:
            return str("1" + str(decimalToBinary(int(str(dec)[1:]), False)))

# pass as string because we do not want to loose the zeros at the MSBs
def binaryToDecimal(binary, signed = True):
    dec = 0
    temp = ""
    binary = str(binary)
    if binary[0] == "0":
        for i in range(len(binary)):
            if binary[i] == "1":
                dec += pow(2,int(len(binary)-1)-i)
        return(int(dec))
    else:
        if signed:
            for i in binary:
                temp += "0" if i == "1" else "1"
            dec = binaryToDecimal(temp)
            return int("-" + f"{dec}")-1
        elif not signed:
            binary = "0" + binary[1:]
            return int("-" + str(binaryToDecimal(binary)))

# Input : string
def xor(a, b):
    a = padding(a, 32)
    b = padding(b, 32)
    temp = ""
    for i in range(32):
        if a[i] == b[i]:
            temp += "0"
        else:
            temp += "1"
    return str(temp)

def and_op(a, b):
    a = padding(a, 32)
    b = padding(b, 32)
    temp = ""
    for i in range(32):
        if a[i] == "1" and b[i] == "1":
            temp += "1"
        else:
            temp += "0"
    return str(temp)

def or_op(a, b):
    a = padding(a, 32)
    b = padding(b, 32)
    temp = ""
    for i in range(32):
        if a[i] == "0" and b[i] == "0":
            temp += "0"
        else:
            temp += "1"
    return str(temp)

# Stack Pointer
reg_val["x2"] = padding(decimalToBinary(256),32)

# Program Counter
PC = decimalToBinary(0)

# read from the binary file
with open(sys.argv[1], "r") as f:
    lines = f.readlines()

# remove \n characters from each line using a "sed" like function in the re module
for i in range(len(lines)):
    lines[i] = re.sub("\n", "", lines[i])

halt = False

# parse through the lines
for line in lines:

    # Virual Halt
    if line == "00000000000000000000000001100011":
        # Print reg values after the halt has been called
        with open(sys.argv[2], "a") as f:
            f.write("0b" + PC + " ")
            for i in range(32):
                f.write("0b"+str(reg_val[f"x{i}"])+" ")
            f.write("\n")

        # Mem stats
        with open(sys.argv[2], "a") as f:
            for a,b in mem_val.items():
                f.write(f"{(hex_padding(re.sub('0x', '', hex(a)),8))}:{'0b'+b}\n")
        exit()

    opcode = line[25:32]

    # R TYPE INSTRUCTIONS
    if opcode == "0110011":
        funct7 = line[0:7]
        rs2 = line[7:12]
        rs1 = line[12:17]
        funct3 = line[17:20]
        rd = line[20:25]

        # add
        if funct3 == "000" and funct7 == "0000000":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(reg_val[reg_encoding[rs1]]) + binaryToDecimal(reg_val[reg_encoding[rs2]])), 32)

        # sub
        elif funct3 == "000" and funct7 == "0100000":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(reg_val[reg_encoding[rs1]]) - binaryToDecimal(reg_val[reg_encoding[rs2]])), 32)

        # sll
        elif funct3 == "001" and funct7 == "0000000":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(reg_val[reg_encoding[rs1]]) << binaryToDecimal(reg_val[reg_encoding[rs2]])), 32)

        # slt
        elif funct3 == "010" and funct7 == "0000000":
            if binaryToDecimal(reg_val[reg_encoding[rs1]]) < binaryToDecimal(reg_val[reg_encoding[rs2]]):
                reg_val[reg_encoding[rd]] = padding(decimalToBinary(1), 32) 

        # sltu
        elif funct3 == "011" and funct7 == "0000000":
            if binaryToDecimal(reg_val[reg_encoding[rs1]], False) < binaryToDecimal(reg_val[reg_encoding[rs2]], False):
                reg_val[reg_encoding[rd]] = padding(decimalToBinary(1), 32) 

        # xor
        elif funct3 == "100" and funct7 == "0000000":
            reg_val[reg_encoding[rd]] = xor(reg_val[reg_encoding[rs1]], reg_val[reg_encoding[rs2]])

        # srl
        elif funct3 == "101" and funct7 == "0000000":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(reg_val[reg_encoding[rs1]]) >> binaryToDecimal(reg_val[reg_encoding[rs2]])), 32)

        # or
        elif funct3 == "110" and funct7 == "0000000":
            reg_val[reg_encoding[rd]] = or_op(reg_val[reg_encoding[rs1]], reg_val[reg_encoding[rs2]])

        # and
        elif funct3 == "111" and funct7 == "0000000":
            reg_val[reg_encoding[rd]] = and_op(reg_val[reg_encoding[rs1]], reg_val[reg_encoding[rs2]])

    # I type instruction
    elif opcode == "0000011" or opcode == "0010011" or opcode == "1100111":

        imm = line[0:12]
        rs1 = line[12:17]
        funct3 = line[17:20]
        rd  = line[20:25]

        # lw
        # load the value at memory address (rs1+imm) to rd
        if opcode == "0000011" and funct3 == "010":
            reg_val[reg_encoding[rd]] = mem_val[int(binaryToDecimal(reg_val[reg_encoding[rs1]])+binaryToDecimal(imm))]

        # addi
        elif opcode == "0010011" and funct3 == "000":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(reg_val[reg_encoding[rs1]]) + binaryToDecimal(imm)), 32)

        # sltiu
        elif opcode == "0010011" and funct3 == "011":
            if binaryToDecimal(reg_val[reg_encoding[rs1]], signed=False) < binaryToDecimal(imm, signed=False):
                reg_val[reg_encoding[rd]] = padding(decimalToBinary(1),32)

        # jalr
        elif opcode == "1100111" and funct3 == "000":
            print(binaryToDecimal(PC))
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(PC) + 4), 32)
            PC = PC[:-1] + "0"
            # PC = padding(decimalToBinary(binaryToDecimal(rs1) + binaryToDecimal(imm)),32) # i was not sure whether to use the VALUE of rs1 or ADDRESS of rs1. Logically, I ended up using address of the register

    # S type instruction (sw)
    elif opcode == "0100011":
        imm1 = line[0:7]
        imm2 = line[20:25]
        rs1 = line[12:17]
        rs2 = line[7:12]
        funct3 = line[17:20]
        imm = imm1 + imm2

        if funct3 == "010":
            mem_val[binaryToDecimal(reg_val[reg_encoding[rs1]])+binaryToDecimal(imm)] = reg_val[reg_encoding[rs2]]

    # B type instruction
    elif opcode == "1100011":
        imm1 = line[0:7]
        imm2 = line[20:25]
        rs1 = line[12:17]
        rs2 = line[7:12]
        funct3 = line[17:20]
        imm = imm1 + imm2
        imm = imm + "0"

        # # beq
        # if funct3 == "000":
        #     if binaryToDecimal(reg_val[reg_encoding[rs1]]) == binaryToDecimal(reg_val[reg_encoding[rs2]]):
        #         PC = padding(decimalToBinary(binaryToDecimal(PC) + binaryToDecimal(imm)),32)
        #
        # # bne
        # elif funct3 == "001":
        #     if binaryToDecimal(reg_val[reg_encoding[rs1]]) != binaryToDecimal(reg_val[reg_encoding[rs2]]):
        #         # PC = padding(decimalToBinary(binaryToDecimal(PC) + binaryToDecimal(imm)),32)
        #
        # # bge
        # elif funct3 == "100":
        #     if binaryToDecimal(reg_val[reg_encoding[rs1]]) >= binaryToDecimal(reg_val[reg_encoding[rs2]]):
        #         PC = padding(decimalToBinary(binaryToDecimal(PC) + binaryToDecimal(imm)),32)
        #
        # # bgeu
        # elif funct3 == "101":
        #     if binaryToDecimal(reg_val[reg_encoding[rs1]], False) >= binaryToDecimal(reg_val[reg_encoding[rs2]], False):
        #         PC = padding(decimalToBinary(binaryToDecimal(PC) + binaryToDecimal(imm)),32)
        #
        # # blt
        # elif funct3 == "110":
        #     if binaryToDecimal(reg_val[reg_encoding[rs1]]) < binaryToDecimal(reg_val[reg_encoding[rs2]]):
        #         PC = padding(decimalToBinary(binaryToDecimal(PC) + binaryToDecimal(imm)),32)
        #
        # # bltu
        # elif funct3 == "111":
        #     if binaryToDecimal(reg_val[reg_encoding[rs1]], False) < binaryToDecimal(reg_val[reg_encoding[rs2]], False):
        #         PC = padding(decimalToBinary(binaryToDecimal(PC) + binaryToDecimal(imm)),32)

    # U type instructions
    elif opcode == "0110111" or opcode == "0010111":
        imm = line[0:20]
        rd = line[20:25]

        # lui
        if opcode == "0110111":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(str(imm) + (12*"0"))), 32)

        # auipc
        elif opcode == "0010111":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(imm + (12*"0")) + binaryToDecimal(PC)), 32)

    # J type instructions (jal)
    elif opcode == "1101111":
        imm = line[0:20]
        imm = imm[0] + imm[10:20] + imm[9] + imm[1:9]
        imm = imm[1:] + "0"
        rd = line[20:25]
        reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(PC) + 4), 32)
        PC = PC[:-1] + "0"
        # PC = padding(decimalToBinary(binaryToDecimal(PC) + binaryToDecimal(imm)),32)

    # Bonus Questions
    elif opcode == "0000000":
        funct3 = line[17:20]
        rs1 = line[12:17]
        rs2 = line[7:12]
        rd = line[20:25]

        # mul
        if funct3 == "000":
            reg_val[reg_encoding[rd]] = padding(decimalToBinary(binaryToDecimal(reg_val[reg_encoding[rs1]]) * binaryToDecimal(reg_val[reg_encoding[rs2]])),32)

        #rst
        elif funct3 == "001":
            for i in range(32):
                reg_val[f"x{i}"] = 32*"0"

        # halt
        elif funct3 == "010":
            exit()

        # rvrs
        elif funct3 == "011":
            reg_val[reg_encoding[rd]] = padding(reg_val[reg_encoding[rs1]][::-1],32)


    else:
        print ("Invalid Type")
        exit()

    # updating the PC
    PC = padding(decimalToBinary(binaryToDecimal(PC) + 4), 32)


    # Print reg values
    with open(sys.argv[2], "a") as f:
        f.write("0b" + PC + " ")
        for i in range(32):
            f.write("0b"+str(reg_val[f"x{i}"])+" ")
        f.write("\n")

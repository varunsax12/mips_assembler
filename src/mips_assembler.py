# -*- coding: utf-8 -*-
"""
Top file for assembler to convert assembly language into machine
Reference: MIPS instruction set in "Digital Design and Computer Architecture"
    by David Money Harris and Sarah L. Harris

1. It is a simple assembler which converts assembly code into machine code
2. It does not optimize the code by reordering the instructions
    (Possible future enhancement->2 above)
    a. Does not support globals currently, treats everything as .data

Author: Varun Saxena
Date  : 02/15/2020
"""

from mips_utils import *
from instruction_map import instruction_map
import re
import os
import sys

register_map = {}

def build_reg_map():
    """ Function to build register mapping to number instead of hardcoding
    """
    register_map["0"] = 0
    register_map["at"] = 1
    for i in range(0, 2):                  # reg prefix     displacement
        register_map["v"+str(i)] = i+2     # v0-v1          2-3
    for i in range(0, 4):
        register_map["a"+str(i)] = i+4     # a0-a3          4-7
    for i in range(0, 8):
        register_map["t"+str(i)] = i+8     # t0-t7          8-15
    for i in range(0, 8):
        register_map["s"+str(i)] = i+16    # s0-s7          16-23
    for i in range(8, 10):
        register_map["t"+str(i)] = i+16    # t8-t9          24-25
    for i in range(0, 1):
        register_map["k"+str(i)] = i+26    # k0-k1          26-27
    register_map["gp"] = 28
    register_map["sp"] = 29
    register_map["fp"] = 30
    register_map["ra"] = 31

class MIPSAssembler:
    def __init__(self):
        self.addressBase = hex(0)
        self.address = self.addressBase
        self.inputInstructionList = []
        self.instructionList = []
        self.symbolTable = {} #this will hold the label to address map
        self.dataType = None

    def readASM(self, filePath):
        """ Function to read the asm file
        """
        with open(filePath, "r") as fh:
            self.inputInstructionList = fh.readlines()
    
    def setDataType(self, data_type):
        """ Function to set the data type to the in-built bin or hex
        """
        self.dataType = data_type

    def setAddressBase(self, base):
        """ Function to set the address base for instruction set
        """
        if type(base)==int:
            self.addressBase = hex(base)
        else:
            self.addressBase = base
        self.address = self.addressBase

    def resetProgramCounter(self):
        self.address = self.addressBase

    def getProgramCounter(self):
        return self.address

    def programCounter(self, increment=4):
        self.address = hex(int(self.address, 16)+int(increment))

    def firstPass(self):
        """ Function to perform first pass parsing
            1. Reads the label if present and stores into symbol map
               Removes the label from instruction
        """
        for instruction in self.inputInstructionList:
            #clean the white spaces in the instruction
            instruction = re.sub(r"\s+", " ", instruction)
            label_check = re.match(r'^\s*(\S+)\:', instruction)
            if label_check:
                label = label_check.group(1)
                self.symbolTable[label] = self.getProgramCounter()
                # remove label from instruction for easy parsing and 
                # maintaining uniform regex
                instruction = re.sub(r'^\s*(\S+)\:\s*', "", instruction)
            self.instructionList.append({
                "address" : self.getProgramCounter(), 
                "word"    : instruction})
            self.programCounter()
        
    def handleRType(self, op, rs, rt, rd, shamt, funct):
        """ Function to build the r-type instruction word
            Bit size=>
            op=6, rs=5, rt=5, rd=5, shamt=5, funct=6
        """
        ret_val = funct
        ret_val += shamt<<6
        ret_val += rd<<11
        ret_val += rt<<16
        ret_val += rs<<21
        ret_val += op<<26
        return ret_val
    
    def handleIType(self, op, rs, rt, Imm):
        """ Function to build the i-type instruction word
            Bit size=>
            op=6, rs=5, rt=5, Imm=16
        """
        if type(Imm)==int:
            # case when Imm is an integer
            if(Imm<0):
                Imm = twoComplement(Imm, 16)
        else:
            # case wehn Imm is a label => type hex
            Imm = int(Imm, 16)
        ret_val = Imm
        ret_val += rt<<16
        ret_val += rs<<21
        ret_val += op<<26
        return ret_val

    def handleJType(self, op, addr):
        """ Function to build the j-type instruction word
            Bit size=>
            op=6, addr=26
        """
        # remove the first 4 at MSB and last 2 at LSB bits
        addr = intToBin(int(addr, 16), 32)
        addr = '0b'+addr[4:-2]
        ret_val = op<<26
        ret_val += int(addr,2)
        return ret_val

    def parseInstruction(self, word, nextPC=None):
        """ Function to parse the input assembly instruction
        """
        # clean up random whitespaces
        re.sub('\s+', ' ', word)
        mnemonic = re.match(r'^\s*?(\S+?) ', word)
        mnemonic = mnemonic.group(1)
        if instruction_map[mnemonic]["type"][0]=="r":
            # register type instruction format normal and shift-variable
            operands_1 = re.match(r'^.*?\$(\S+?), \$(\S+), \$(\S+)\s*$', word)
            # register type instruction format of shift with shamt value in 3rd
            operands_2 = re.match(r'^.*?\$(\S+?), \$(\S+), (\d+)\s*$', word)
            # register type instruction format jump
            operands_3 = re.match(r'^.*?\$(\S+?)\s*$', word)
            shamt = 0
            # register type instruction format for shift
            if operands_1:
                rd = operands_1.group(1)
                if "shift" in instruction_map[mnemonic]["type"]:
                    # shift variable type switches rs and rt from other
                    # arith and logical
                    rs = operands_1.group(3)
                    rt = operands_1.group(2)
                else:
                    rs = operands_1.group(2)
                    rt = operands_1.group(3)
            elif operands_2:
                rs = "0" # using the $0 register as its position converts to 0
                rd = operands_2.group(1)
                rt = operands_2.group(2)
                # can add possible QC here to ensure that the shamt is int
                shamt = int(operands_2.group(3))
            elif operands_3:
                rs = operands_3.group(1)
                rd = "0"
                rt = "0"
            opcode = instruction_map[mnemonic]["opcode"]
            funct = instruction_map[mnemonic]["funct"]
            return self.handleRType(opcode, register_map[rs],
                                            register_map[rt], register_map[rd],
                                            shamt, funct)
        elif instruction_map[mnemonic]["type"]=="i":
            # immediate type instruction format
            # format_1 of opcode, reg, reg, Imm
            operands_1 = re.match(r'^.*?\$(\S+?), \$(\S+), (\S+)\s*$', word)
            # format_2 of opcode, reg, Imm(reg)
            operands_2 = re.match(r'^.*?\$(\S+?), (\S+?)\(\$(\S+)\)\s*$', word)
            if(operands_1):
                rt = operands_1.group(1)
                rs = operands_1.group(2)
                Imm = operands_1.group(3)
            elif(operands_2):
                rt = operands_2.group(1)
                rs = operands_2.group(3)
                Imm = operands_2.group(2)
            # check if branch instruction is using label
            if Imm in self.symbolTable.keys():
                # relative addrssing mode from next instruction
                # find displacement and set to Imm
                Imm = int(self.symbolTable[Imm], 16) - int(nextPC)
                Imm = int(Imm/4)
                # in the branch instruction the rs and rt are inverted
                temp = rt
                rt = rs
                rs = temp
            else:
                Imm = int(Imm)
            opcode = instruction_map[mnemonic]["opcode"]
            return self.handleIType(opcode, register_map[rs],
                                    register_map[rt], Imm)
        elif instruction_map[mnemonic]["type"][0]=="j":
            operands = re.match(r'^.*?'+mnemonic+r'\s*(\S+)', word)
            addr = self.symbolTable[operands.group(1)]
            opcode = instruction_map[mnemonic]["opcode"]
            return self.handleJType(opcode, addr)

    def secondPass(self):
        """ Function to parse the instructions and resolve the labels if needed
        """
        for instructions in self.instructionList:
            currentPC = int(self.getProgramCounter(), 16)
            nextPC    = currentPC+4            
            print(instructions["address"], hex(self.parseInstruction(instructions["word"], nextPC)))
            self.programCounter()

    def topRunner(self, baseAddress=0):
        """ Top runner to call the first pass and second pass
        """
        build_reg_map()
        self.setAddressBase(baseAddress)
        self.resetProgramCounter()
        self.firstPass()
        self.resetProgramCounter()
        self.secondPass()

if __name__ == '__main__':
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print("Invalid asm file passed: "+file_path)
        sys.exit()
    X = MIPSAssembler()
    X.readASM(file_path)
    X.topRunner('0x0')

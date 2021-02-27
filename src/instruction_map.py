# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:48:29 2021

@author: a0230100
"""

# using an instruction map as the top level instruction formatter to avoid
# complicated if-else or switch-case sections in the final instruction parser
instruction_map = {
    "mul"  : {"opcode" : 28,"funct"  : 2,  "type"   : "r"},
    "jr"   : {"opcode" : 0, "funct"  : 8,  "type"   : "r-jump"},
    "jalr" : {"opcode" : 0, "funct"  : 9,  "type"   : "r-jump"},
    "add"  : {"opcode" : 0, "funct"  : 32, "type"   : "r"},
    "addu" : {"opcode" : 0, "funct"  : 33, "type"   : "r"},
    "sub"  : {"opcode" : 0, "funct"  : 34, "type"   : "r"},
    "subu" : {"opcode" : 0, "funct"  : 35, "type"   : "r"},
    "and"  : {"opcode" : 0, "funct"  : 36, "type"   : "r"},
    "or"   : {"opcode" : 0, "funct"  : 37, "type"   : "r"},
    "xor"  : {"opcode" : 0, "funct"  : 38, "type"   : "r"},
    "nor"  : {"opcode" : 0, "funct"  : 39, "type"   : "r"},
    "slt"  : {"opcode" : 0, "funct"  : 42, "type"   : "r"},
    "sktu" : {"opcode" : 0, "funct"  : 43, "type"   : "r"},
    "sll"  : {"opcode" : 0, "funct"  : 0,  "type"   : "r-shift"},
    "srl"  : {"opcode" : 0, "funct"  : 2,  "type"   : "r-shift"},
    "sra"  : {"opcode" : 0, "funct"  : 3,  "type"   : "r-shift"},
    "sllv" : {"opcode" : 0, "funct"  : 4,  "type"   : "r-shift"},
    "srlv" : {"opcode" : 0, "funct"  : 6,  "type"   : "r-shift"},
    "srav" : {"opcode" : 0, "funct"  : 7,  "type"   : "r-shift"},
    "beq" :  {"opcode" : 4,  "type"  : "i"},
    "bne" :  {"opcode" : 5,  "type"  : "i"},
    "addi" : {"opcode" : 8,  "type"  : "i"},
    "addiu": {"opcode" : 9,  "type"  : "i"},
    "slti" : {"opcode" : 10, "type"  : "i"},
    "sltiu": {"opcode" : 11, "type"  : "i"},
    "andi" : {"opcode" : 12, "type"  : "i"},
    "ori"  : {"opcode" : 13, "type"  : "i"},
    "xori" : {"opcode" : 14, "type"  : "i"},
    "lui"  : {"opcode" : 15, "type"  : "i"},
    "lb"   : {"opcode" : 32, "type"  : "i"},
    "lh"   : {"opcode" : 33, "type"  : "i"},
    "lw"   : {"opcode" : 35, "type"  : "i"},
    "lbu"  : {"opcode" : 36, "type"  : "i"},
    "lhu"  : {"opcode" : 37, "type"  : "i"},
    "sb"   : {"opcode" : 40, "type"  : "i"},
    "sh"   : {"opcode" : 41, "type"  : "i"},
    "sw"   : {"opcode" : 43, "type"  : "i"},
    "j"    : {"opcode" : 2,  "type"  : "j"},
    "jal"  : {"opcode" : 3,  "type"  : "j"},
}

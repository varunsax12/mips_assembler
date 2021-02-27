# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 19:50:44 2021

@author: a0230100
"""

def print_reg_map():
    """ Function to print the reg map
    """
    for keys, values in register_map.items():
        print(keys, " => ", values)

def binToHex(value, hex_size=8):
    """ Function to convert bin to hex
    """
    hex_val = hex(int(value, 2)).replace('0x', '')
    if(len(hex_val)<hex_size):
        return str((hex_size-len(hex_val))*'0'+hex_val)
    return str(hex_val[hex_size-len(hex_val):])

def intToBin(value, bit_size):
    """ Function to convert int into bits of given size
        Adds padding 0s ahead of MSB if needed
        Return: string of binary data
    """
    bin_val = bin(value).replace(r'0b', '')
    if(len(bin_val)<bit_size):
        return str((bit_size-len(bin_val))*'0'+bin_val)
    return str(bin_val[bit_size-len(bin_val):])

def twoComplement(value, bit_size):
    """ Function to convert number into 2s complement
        Using 2^bit_size+(value) where value is a negative number
    """
    return pow(2, bit_size)+value

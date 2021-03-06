'''
Created on 10.03.2017

@author: HunterxPokemon
'''

import argparse
import numpy

#variables
byteCount = 0

#parse arguments
parser = argparse.ArgumentParser(description="Transform binary data into assembly file")
parser.add_argument("symbol", type=str, help="name for the global definition")
parser.add_argument("input_file", type=argparse.FileType("rb"), help="binary file")
parser.add_argument("output_file", type=argparse.FileType("w"), help="assembly file")
#read arguments
args = parser.parse_args()
#read binary file
bin_block = args.input_file.read()
args.input_file.close()

def binary2assembly( bin_block ):
    #transform to text file format
    txt_bin_block = (''.join(len(bin_block) * ['{:02x}']).format(*numpy.frombuffer(bin_block, numpy.uint8)))
    #write header in assembly file
    args.output_file.write('// Copyright (C) by HunterxPokemon\n// generated by binary2assembly\n\n')
    args.output_file.write('.section\n.rodata\n.balign 4\n.global ' + 
                           args.symbol + '_bin' + '\n' + '.global ' + args.symbol + '_bin_size\n\n')
    args.output_file.write(args.symbol + '_bin_size:\n\n' + '\t.int ' + 
                           (str)(len(bin_block)) + '\t//bytes\n\n\n')
    args.output_file.write(args.symbol + '_bin' + ':\n')
    
    #write assembly data in file
    for i in range(len(txt_bin_block)):
        #if 16 bytes in one line
        if (byteCount % 32) == 0:
            args.output_file.write('\n\t.byte ' + '0x' + txt_bin_block[i])
        #if first number of byte
        elif (i % 2) == 0:
            args.output_file.write('0x' + txt_bin_block[i])
        #if not last byte of file and if not last byte of line
        elif (i != len(txt_bin_block) - 1) and ((byteCount + 1) % 32 != 0):
            args.output_file.write(txt_bin_block[i] + ', ')
        #else write number
        else:
            args.output_file.write(txt_bin_block[i])
        byteCount += 1
        
    args.output_file.close()
    return



#Author    : HunterxPokemon
#Date      : 04.04.2017
#Title     : lz77 decompression
#Brief     : tool to decompress gba graphics

import argparse

#parse arguments
parser = argparse.ArgumentParser(description='lz77 decompress tool for gba')
parser.add_argument('in_gba', type=str, help='GBA ROM File')
parser.add_argument('in_offset_graphic', type=str, help='Offset Adress of lz77 Compressed Graphic in ROM')

args = parser.parse_args()

#variables
#address of lz77 graphic
start_offset = args.in_offset_graphic


#static variables



#open gba file
infile = open(args.in_gba, 'rb')
#read gba file
infile.seek(start_offset)

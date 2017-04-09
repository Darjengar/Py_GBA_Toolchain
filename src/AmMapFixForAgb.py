'''
Created on 17.03.2017

@author: HunterxPokemon
'''

import argparse
import os

#variables
start_index = 20
border_block_length = 8

#parse arguments
parser = argparse.ArgumentParser(description='Fix AM Map Data for GBA Format')
parser.add_argument('input_file', type=str, help='Map file from AM')
parser.add_argument('directory', type=str, help='Directory of output files')

#read arguments
args = parser.parse_args()

#open input file
infile = open(args.input_file, 'rb')
#got to byte 20
infile.seek(start_index)
#read from this adress border block data
border_block_data = infile.read(border_block_length)
#read map data
map_data = infile.read()
infile.close()

#split file name of input file
output_str = os.path.splitext(os.path.basename(args.input_file))[0]

#create border_block_file
border_block_file = open(args.directory + '/' + output_str + '_border_block.bin', 'wb')
#create map_file
map_file = open(args.directory + '/' + output_str + '.bin', 'wb')
#write border block data into file
border_block_file.write(border_block_data)
border_block_file.close()
#write map data into file
map_file.write(map_data)
map_file.close()

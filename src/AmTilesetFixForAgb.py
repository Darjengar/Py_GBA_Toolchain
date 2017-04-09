'''
Created on 17.03.2017

@author: HunterxPokemon
'''

import argparse
import os

#parse arguments
parser = argparse.ArgumentParser(description='Fix Am Block and Behavior Data')
parser.add_argument('input_file', type=str, help='Am tileset data')
parser.add_argument('input_file2', type=int, help='number of blocks')
parser.add_argument('directory', type=str, help='Directory of output files')
#read arguments
args = parser.parse_args()

#variable
start_index = 4
number_of_blocks = args.input_file2
block_data_block_len = 16
behavior_data_block_len = 4

#open input file
infile = open(args.input_file, 'rb')
#start at start index
infile.seek(start_index)
#read from offset block data
block_data = infile.read(number_of_blocks * block_data_block_len)
behavior_data = infile.read(number_of_blocks * behavior_data_block_len)
infile.close()
#split file name of input file
output_str = os.path.splitext(os.path.basename(args.input_file))[0]
#create block data file
block_data_file = open(args.directory + '/' + output_str + '_block_data.bin', 'wb')
#create behavior data file
behavior_data_file = open(args.directory + '/' + output_str + '_behavior_data.bin', 'wb')
#write block data into file
block_data_file.write(block_data)
block_data_file.close()
#write behavior data into file
behavior_data_file.write(behavior_data)
behavior_data_file.close()




#HunterxPokemon 2017

import sys
sys.path.append('c:/users/hunterxpokemon/documents/workspace/python/py_gba_tools/src/gba')
import lz77
import argparse

#parse arguments
parser = argparse.ArgumentParser(description='Tool to decompress LZ77 graphics.')
parser.add_argument('inGbaFile', type=str, help='Input: GBA File')
parser.add_argument('startOffset', type=lambda x: int(x,0), help='Input: Start Offset of the LZ77 graphic')
parser.add_argument('outGraphic', type=str, help='Ouput: Binary File ')

args = parser.parse_args()

#call lz77 decompress algorithm
lz77DecompData = lz77.lz77Decompress( args.inGbaFile, args.startOffset)
#create binary file
outFile = open(args.outGraphic, 'wb')

#write grapic data into binary file
for i in range(len(lz77DecompData[1])):
    outFile.write(lz77DecompData[1][i].to_bytes(1, byteorder='big'))
outFile.close()

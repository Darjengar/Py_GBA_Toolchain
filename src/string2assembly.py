#HunterxPokemon 2017
import sys, argparse, time, os
#
#TODO: optimize the code
#
#text file example:
#ref_123=hello
#//
#ref_456=ciao
#

#save start time to variable
start_time = time.time()

parser = argparse.ArgumentParser(description='String to Assembly converter')
#parse arguments
parser.add_argument('in_text_file', type=str, help='Text File')
parser.add_argument('in_charmap_file', type=str, help='Charmap File')
parser.add_argument('out_file', type=str, help='Output File')
#get arguments from command line
args = parser.parse_args()

#global variables
byteCount = 0
symbolTable = []
stringTable = []
alphabetTable = []
hexTable = []
byteBlock = []
dictCharmap = {}
byteBlockTable = []

#loop variables
j = 0

#static variables
TERMINATOR = '0xff'
ALIGNMENT = '.align 2'

#open text file
infile = open(args.in_text_file, 'r')
#create list of text file
line = list(infile)
infile.close()

#split string into symbols and text
for i in range(len(line)):
    #if line begin with '//' then ignore the line
    if line[i].startswith('//'):
        continue
    string = line[i].strip('\n').split('=',maxsplit=1)
    for j in range(len(string)):
        if j < 1:
            symbolTable.append(string[j])
        else:
            stringTable.append(string[j])

#open charmap
infile = open(args.in_charmap_file, 'r')
#create list of chars
line = list(infile)
infile.close()

for i in range(len(line)):
    #if line begin with '//' then ignore the line
    if line[i].startswith('//'):
        continue
    #remove newline and split string into two pieces between '='
    string = line[i].strip('\n').split('=',maxsplit=1)
    #create alphabet and hex table for string encoding
    for j in range(len(string)):
        #if index 0 then add the string to alphabetTable 
        if j < 1:
            alphabetTable.append(string[j])
        #if index 1 then add the string to hexTable
        else:
            hexTable.append(string[j])

#create charmap as dictionary
for i in range(len(alphabetTable)):
    dictCharmap[alphabetTable[i]] = hex(int(hexTable[i],0))
    
#convert string to byte string
for i in range(len(stringTable)):
    string = stringTable[i]
    j = 0
    while j < len(string):
        print('j ist gleich ',j)
        if string[j] == '\\':
            if string[j + 1] == 'h':
                escapeChar = string[j] + string[j + 1] + string[j + 2] + string[j + 3]
                #try to find char of string in charmap       
                try:
                    byteBlock.append(dictCharmap[escapeChar])
                    j += 3
                #if KeyError print error message and exit the program with error 1
                except KeyError:
                    print('KeyError: No such escape char in charmap: %s' % (escapeChar))
                    sys.exit(1)
            else:
                escapeChar = string[j] + string[j + 1]
                #try to find char of string in charmap       
                try:
                    byteBlock.append(dictCharmap[escapeChar])
                    j += 1
                #if KeyError print error message and exit the program with error 1
                except KeyError:
                    print('KeyError: No such escape char in charmap: %s' % (escapeChar))
                    sys.exit(2)            
        else:
            #try to find char of string in charmap       
            try:
                byteBlock.append(dictCharmap[string[j]])
                #if KeyError print error message and exit the program with error 1
            except KeyError:
                print('KeyError: No such character in charmap: %s' % (string[j]))
                sys.exit(3)
        j += 1
    #add byteBlockTable list byte string
    byteBlockTable.append(byteBlock)
    byteBlock = []

#create output file
outfile = open(args.out_file, 'w')
#create file header
outfile.write('// Copyright (C) by HunterxPokemon\n// generated by String2Assembly\n\n')

#create assembly symbol form
for i in range(len(byteBlockTable)):
    #set byteCount to zero for next byte string
    byteCount = 0
    outfile.write('\n// ' + stringTable[i] + '\n' + ALIGNMENT + '\n.global ' + symbolTable[i] + '\n\n' + symbolTable[i] + ':')
    for j in range(len(byteBlockTable[i])):
        #if last byte of string
        if j == len(byteBlockTable[i]) - 1:
            outfile.write(byteBlockTable[i][j] + ', ' + TERMINATOR + '\n\n')
        #if 16 bytes in one line
        elif byteCount % 16 == 0:
                outfile.write('\n\t.byte ' + byteBlockTable[i][j] + ', ')
        #if not last byte and if not last byte of a line
        elif j != len(byteBlockTable[i]) - 1 and ((byteCount + 1) % 16 != 0):
                outfile.write(byteBlockTable[i][j] + ', ') 
        #if not last byte of string and if last byte of a line 
        else:
            outfile.write(byteBlockTable[i][j])
        byteCount += 1

#print compile time
print('\n------ %s seconds ------' % (time.time() - start_time) )
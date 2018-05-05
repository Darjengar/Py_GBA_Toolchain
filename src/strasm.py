# DarkGengar (C) 2018
# Date 04/27/18
# License GNU GPL

# Strasm - String Assembly Interpreter
# TODO: Refactor Code:
#           - Optimize Code

import sys
import argparse
import os
import pathlib
import time

#save start time to variable
start_time = time.time()

# strasm syntax
operators = [
    '$',
    '='
]

format = [
    '{',
    '}',
    '"',
    ';',
    '[+]'
]

data_types = [
    "str",
    "tbl" 
]

#static variables
TERMINATOR = '0xff'
ALIGNMENT = '.align 2'

#error classes
class Error(Exception):
    """Base class for other exceptions"""
    pass
    
class FormatError(Error):
    pass
    
class DataTypeOpError(Error):
    pass
    
class DataTypeError(Error):
    def __init__(self, type):
        self.type = type
    def print_error(self):
        print(self.type)
    
class SymbolOpError(Error):
    pass

parser = argparse.ArgumentParser(description='Strasm Interpreter')
# parse arguments
parser.add_argument('in_str_file', type=str, help='Strasm File')
parser.add_argument('in_charmap_file', type=str, help='Charmap File')
parser.add_argument('out_file', type=str, help='Output File')
# parser.add_argument('-c', action='store_true')
args = parser.parse_args()

def strasm_interpreter(file_list):
    print("Start Strasm interpreter")
    # file in single line
    sg_line = ''
    string = ''

    symbols = []
    pstrings = []
    byteBlockTable = []
    pstrings = []
    types = []

    # open charmap
    infile = open(args.in_charmap_file, 'r')
    # create list of chars
    line = list(infile)
    infile.close()
    dictCharmap = charmap_interpreter(line)
    
    for i in range(len(file_list)):
        if(file_list[i] == '\n' or file_list[i].startswith('//')):
            continue
        sg_line += file_list[i].strip('\n').strip('\r').lstrip(' ').lstrip('\t')

    try:
        new_string = sg_line.split(';')

        for i in range(len(new_string)):
            list2 = new_string[i].split(' ', 3)
            list3 = list2[:3] + list2[3].split('"')
            strasm_handler(list3, byteBlockTable, dictCharmap, pstrings, types)
            
            symbols.append(list3[1])
        
        # C Version
        generate_c_file(byteBlockTable, symbols, pstrings, types)
        
        # if args.c:
            # generate_c_file(byteBlockTable, symbols, pstrings, types)

        # ASM Version
        # else:
            # generate_asm_file(byteBlockTable, symbols, pstrings, types)
        print("End Strasm Interpreter")
    except FormatError:
        print("FormatError: The string have not the right format: $type symbol = {\"string\"}")
    except DataTypeOpError:
        print("DataTypeOpError: You forgot the data type operator '$'")
    except SymbolOpError:
        print("SymbolOpError: You forgot the symbol operator '='")
    except DataTypeError as error:
        print("DataTypeError: Unknown data type " + error.type)
    
def strasm_handler(strasm_list, byteBlockTable, dictCharmap, pstrings, types):
    if(strasm_list[0][0] != operators[0]):
        print(strasm_list)
        raise DataTypeOpError
    if(strasm_list[2] != operators[1]):
        print(strasm_list)
        raise SymbolOpError
    type = strasm_list[0][1:]
    if(type not in data_types):
        print(strasm_list)
        raise DataTypeError(type)
    types.append(type)
    if(type == data_types[0]):
        if(len(strasm_list) != 6 or strasm_list[3] != format[0] or strasm_list[-1] != format[1]):
            print(strasm_list)
            raise FormatError
        str2bytes(strasm_list[4][:], byteBlockTable, dictCharmap, type)
        pstrings.append(strasm_list[4][:])
    elif(type == data_types[1]):
        strasm_list = strasm_list[:4] + strasm_list[4].split(format[4]) + list(strasm_list[5])
        if(len(strasm_list) < 6 or strasm_list[3] != format[0] or strasm_list[-1] != format[1]):
            print(strasm_list)
            raise FormatError
        string_entries = len(strasm_list) - 5
        str2bytes(strasm_list[4:4+string_entries][:], byteBlockTable, dictCharmap, type)
        pstrings.append(strasm_list[4:4+string_entries][:])
        
        

# open charmap
# infile = open(args.in_charmap_file, 'r')
# create list of chars
# line = list(infile)
# infile.close()

# function make hextable and alphabettable
# create hextable and alphabettable
def charmap_interpreter(charmap):
    alphabetTable = []
    hexTable = []
    for i in range(len(charmap)):
        #if line begin with '//' then ignore the line
        if charmap[i].startswith('//'):
            continue
        #remove newline and split string into two pieces between '='
        string = charmap[i].strip('\n').strip('\r').split('=', 1)
        #create alphabet and hex table for string encoding
        for j in range(len(string)):
            #if index 0 then add the string to alphabetTable 
            if j < 1:
                alphabetTable.append(string[j])
            #if index 1 then add the string to hexTable
            else:
                hexTable.append(string[j])
    return charmap2dict(alphabetTable, hexTable)

# create charmap as dictionary
def charmap2dict(alphabetTable, hexTable):
    dictCharmap = {}
    for i in range(len(alphabetTable)):
        dictCharmap[alphabetTable[i]] = hex(int(hexTable[i],0))
    return dictCharmap
        
# function str2bytes
# convert string to byte string
def str2bytes(string, byteBlockTable, dictCharmap, type):
    byteBlock = []
    
    if(type == data_types[0]):
        j = 0
        while j < len(string):
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
                    print(string)
                    print('KeyError: No such character in charmap: %s' % (string[j]))
                    sys.exit(3)
            j += 1
        #add byteBlockTable list byte string
        byteBlockTable.append(byteBlock)
    elif(type == data_types[1]):
        byteBlockTable.append([])
        for i in range(len(string)):
            j = 0
            while j < len(string[i]):
                if string[i][j] == '\\':
                    if string[i][j + 1] == 'h':
                        escapeChar = string[i][j] + string[i][j + 1] + string[i][j + 2] + string[i][j + 3]
                        #try to find char of string in charmap       
                        try:
                            byteBlock.append(dictCharmap[escapeChar])
                            j += 3
                        #if KeyError print error message and exit the program with error 1
                        except KeyError:
                            print('KeyError: No such escape char in charmap: %s' % (escapeChar))
                            sys.exit(1)
                    else:
                        escapeChar = string[i][j] + string[i][j + 1]
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
                        byteBlock.append(dictCharmap[string[i][j]])
                        #if KeyError print error message and exit the program with error 1
                    except KeyError:
                        print('KeyError: No such character in charmap: %s' % (string[i][j]))
                        sys.exit(3)
                j += 1
            #add byteBlockTable list byte string
            byteBlockTable[-1].append(byteBlock)
            byteBlock = []

def generate_c_file(byteBlockTable, symbolTable, stringTable, types):
    # create output file
    outfile = open(args.out_file, 'w')
    # create file header
    outfile.write('// Copyright (C) by DarkGengar\n// Generated by Strasm\n\n')

    for i in range(len(byteBlockTable)):
        if(types[i] == data_types[0]):
            # set byteCount to zero for next byte string
            byteCount = 0
            outfile.write('const unsigned char ' + symbolTable[i] + '[' + str(len(byteBlockTable[i]) + 1) + '] = {')
            for j in range(len(byteBlockTable[i])):
                # if last byte of string
                if j == len(byteBlockTable[i]) - 1:
                    outfile.write(byteBlockTable[i][j] + ', ' + TERMINATOR + '\n};\n\n')
                elif byteCount == 0:
                    outfile.write('\n\t' + byteBlockTable[i][j] + ', ')
                # if 16 bytes in one line
                elif byteCount % 16 == 0:
                    outfile.write(',\n\t' + byteBlockTable[i][j] + ', ')
                # if not last byte and if not last byte of a line
                elif j != len(byteBlockTable[i]) - 1 and ((byteCount + 1) % 16 != 0):
                    outfile.write(byteBlockTable[i][j] + ', ') 
                # if not last byte of string and if last byte of a line 
                else:
                    outfile.write(byteBlockTable[i][j])
                byteCount += 1
        elif(types[i] == data_types[1]):
            # set byteCount to zero for next byte string
            max_str_len = len(max(stringTable[i], key=len)) + 1
            outfile.write('const unsigned char ' + symbolTable[i] + '[' + str(len(byteBlockTable[i])) + '][' + str(max_str_len) + '] = {\n')
            for j in range(len(stringTable[i])):
                outfile.write('\t// ' + stringTable[i][j] + '\n\t{')
                # set byteCount to zero for next byte string
                byteCount = 0
                for k in range(len(byteBlockTable[i][j])):
                    if k == len(byteBlockTable[i][j]) - 1 and j == len(byteBlockTable[i])-1:
                        outfile.write(byteBlockTable[i][j][k] + ', ' + TERMINATOR + '\n\t}\n')
                    # if last byte of string
                    elif k == len(byteBlockTable[i][j]) - 1:
                        outfile.write(byteBlockTable[i][j][k] + ', ' + TERMINATOR + '\n\t},\n\n')
                    elif byteCount == 0:
                        outfile.write('\n\t\t' + byteBlockTable[i][j][k] + ', ')
                    # if 16 bytes in one line
                    elif byteCount % 16 == 0:
                        outfile.write(',\n\t' + byteBlockTable[i][j][k] + ', ')
                    # if not last byte and if not last byte of a line
                    elif k != len(byteBlockTable[i][j]) - 1 and ((byteCount + 1) % 16 != 0):
                        outfile.write(byteBlockTable[i][j][k] + ', ') 
                    # if not last byte of string and if last byte of a line 
                    else:
                        outfile.write(byteBlockTable[i][j][k])
                    byteCount += 1
            outfile.write('};')
    # Close C Source file
    outfile.close()

    # get c source file path
    outpath = pathlib.Path(args.out_file)
    base = os.path.splitext(outpath)[0]
    # create header file path
    header_file = base + '.h'
    outfile = open(header_file, 'w')
    # create file header
    outfile.write('// Copyright (C) by DarkGengar\n// Generated by Strasm\n\n')
    outfile.write('#ifndef ' + symbolTable[i].upper() + '_H\n' + '#define ' + symbolTable[i].upper() + '_H\n\n')
    
    for i in range(len(symbolTable)):
        if(types[i] == data_types[0]):
            outfile.write( '#define ' + symbolTable[i].upper() + '_LEN ' + str(len(byteBlockTable[i]) + 1) + '\nextern const unsigned char ' + symbolTable[i] + '[' + str(len(byteBlockTable[i]) + 1) + '];\n\n')
        elif(types[i] == data_types[1]):
            max_str_len = len(max(stringTable[i], key=len))+1
            outfile.write( '#define ' + symbolTable[i].upper() + '_LEN ' + str(len(byteBlockTable[i]) + 1) + '\n#define ' + symbolTable[i].upper() + '_ENTRY_LEN ' + str(max_str_len) + '\nextern const unsigned char ' + symbolTable[i] + '[' + str(len(byteBlockTable[i]) + 1) + '][' + str(max_str_len) + '];\n\n')
    outfile.write('#endif // ' + symbolTable[i].upper() + '_H\n\n/* --- EOF --- */')
    outfile.close()

def generate_asm_file(byteBlockTable, symbolTable, stringTable, types):
    # create output file
    outfile = open(args.out_file, 'w')
    # create file header
    outfile.write('// Copyright (C) by DarkGengar\n// Generated by Strasm\n\n')

    for i in range(len(types)):
        if(types[i] == data_types[0]):
            # set byteCount to zero for next byte string
            byteCount = 0
            outfile.write('\n// ' + stringTable[i] + '\n' + ALIGNMENT + '\n.global ' + symbolTable[i] + '\n.global ' + symbolTable[i] + '_len\n\n' + symbolTable[i] + '_len: .hword ' + str(len(byteBlockTable[i]) + 1) + '\n' + symbolTable[i] + ':')
            for j in range(len(byteBlockTable[i])):
                # if last byte of string
                if j == len(byteBlockTable[i]) - 1:
                    outfile.write(byteBlockTable[i][j] + ', ' + TERMINATOR + '\n\n')
                # if 16 bytes in one line
                elif byteCount % 16 == 0:
                    outfile.write('\n\t.byte ' + byteBlockTable[i][j] + ', ')
                # if not last byte and if not last byte of a line
                elif j != len(byteBlockTable[i]) - 1 and ((byteCount + 1) % 16 != 0):
                    outfile.write(byteBlockTable[i][j] + ', ') 
                # if not last byte of string and if last byte of a line 
                else:
                    outfile.write(byteBlockTable[i][j])
                byteCount += 1
        elif(types[i] == data_types[1]):
            len_str_list = 0
            for j in range(len(byteBlockTable[i])):
                len_str_list += len(byteBlockTable[i][j]) + 1
            outfile.write('\n' + ALIGNMENT + '\n.global ' + symbolTable[i] + '\n.global ' + symbolTable[i] + '_len\n\n' + symbolTable[i] + '_len: .hword ' + str(len_str_list) + '\n' + symbolTable[i] + ':\n')
            for j in range(len(stringTable[i])):
                outfile.write('// ' + stringTable[i][j] + '\n\tentry_' + str(j) + ':')
                # set byteCount to zero for next byte string
                byteCount = 0
                for k in range(len(byteBlockTable[i][j])):
                    # if last byte of string
                    if k == len(byteBlockTable[i][j]) - 1:
                        outfile.write(byteBlockTable[i][j][k] + ', ' + TERMINATOR + '\n\n')
                    # if 16 bytes in one line
                    elif byteCount % 16 == 0:
                        outfile.write('\n\t\t.byte ' + byteBlockTable[i][j][k] + ', ')
                    # if not last byte and if not last byte of a line
                    elif k != len(byteBlockTable[i][j]) - 1 and ((byteCount + 1) % 16 != 0):
                        outfile.write(byteBlockTable[i][j][k] + ', ') 
                    # if not last byte of string and if last byte of a line 
                    else:
                        outfile.write(byteBlockTable[i][j][k])
                    byteCount += 1
    outfile.close()


# open text file
infile = open(args.in_str_file, 'r')
# create list of text file
line = list(infile)
infile.close()
strasm_interpreter(line)

#print compile time
print('\n------ %s seconds ------' % (time.time() - start_time) )

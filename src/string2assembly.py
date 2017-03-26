#HunterxPokemon 2017
import sys, argparse, time

#Todo: finish the tool
start_time = time.time()

parser = argparse.ArgumentParser(description='String to Assembly converter')
#parse arguments
parser.add_argument('in_text_file', type=str, help='Text File')
parser.add_argument('in_charmap_file', type=str, help='Charmap File')
#get arguments from command line
args = parser.parse_args()

#variables
symbolTable = []
stringTable = []
alphabetTable = []
hexTable = []
byteBlock = []
dictCharmap = {}

#open text file
infile = open(args.in_text_file, 'r')

line = list(infile)
infile.close()

for i in range(len(line)):
    string = line[i].strip('\n').split('=',maxsplit=1)
    for j in range(len(string)):
        if j < 1:
            symbolTable.append(string[j])
        else:
            stringTable.append(string[j])

for i in range(len(symbolTable)):
    print(symbolTable[i])

#open charmap
infile = open(args.in_charmap_file, 'r')
line = list(infile)

for i in range(len(line)):
    if line[i].startswith('//'):
        continue
    string = line[i].strip('\n').split('=',maxsplit=1)
    for j in range(len(string)):
        if j < 1:
            alphabetTable.append(string[j])
        else:
            hexTable.append(string[j])

for i in range(len(alphabetTable)):
    dictCharmap[alphabetTable[i]] = hex(int(hexTable[i],0))
    
for i in range(len(stringTable)):
    for j in range(len(stringTable[i])):       
        try:
            byteBlock.append(dictCharmap[stringTable[i][j]])
        except KeyError:
            print('KeyError: No such character in charmap: %s' % (stringTable[i][j]))
            sys.exit(1)
        
print(byteBlock[0])

for i in range(len(stringTable)):
    print(stringTable[i])

print('\n------ %s seconds ------' % (time.time() - start_time) )
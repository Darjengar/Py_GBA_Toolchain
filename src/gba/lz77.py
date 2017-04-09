"""
@author HunterxPokemon
@date 09.04.17
@brief module with graphic functions

"""

#variables 
outputBytes = []

#loop variables
i = 0
k = 0

#static variables
MASK1 = 0b000001
MASK2 = 0xFFF

#functions
def littleEndian( codeBlock ):
    """
    decrypt code in little endian
    
    @param codeBlock Byte block of data.
    @return code block in little endian format
    """
    leCode = codeBlock[::-1]
    return leCode

def lz77Decompress( gba_file, startOffset ):
    """
    decompress lz77 graphics
    
    @param gba_file ROM image
    @param startOffset Offset to lz77 graphic.
    @return list with graphic header list and lz77 decompressed output list.
    """
    #open gba file
    in_gba_file = open(gba_file, 'rb')
    #goto graphic adress
    in_gba_file.seek(startOffset)
    #read color of graphic
    color = int.from_bytes(in_gba_file.read(1), byteorder='big')
    #read size of graphic
    size = int.from_bytes(littleEndian(in_gba_file.read(3)), byteorder='big')
    
    #begin of lz77 algorithm
    while len(outputBytes) < size:
        #read decode byte
        decodeByte = int.from_bytes(in_gba_file.read(1), byteorder='big')
        #read decode byte in bit structure
        i = 8
        while i != 0:
            i -= 1
            #read each bit alone
            bit = decodeByte >> i
            #read bit
            bitFlag = bit & MASK1
            #if bit is true read compressed bytes and encode the bytes 
            if bitFlag:
                #read two compress bytes
                tempBytes = int.from_bytes(in_gba_file.read(2), byteorder='big')
                #calculate how many bytes to jump back
                jumpNBytes = (tempBytes & MASK2) + 1
                #calculate length of bytes to take from the jump back address
                takeLength = (tempBytes >> 12) + 3
                #jump back address
                takeAddress = ((len(outputBytes) -1) - jumpNBytes + 1)
                #calculate how many times the algorithm have to read the ouput for the take length
                nTimes = takeLength/len(outputBytes[takeAddress::])
                #length of bytes at the jump back address
                takeNTimesBytes = len(outputBytes[takeAddress::])
                
                k = nTimes
                #begin to read from the output
                #if length from the jump back address is bigger equals the length needed
                if len(outputBytes[takeAddress::]) >= takeLength:
                    outputBytes.extend(outputBytes[takeAddress:takeAddress + takeLength:])
                else:
                    while k:
                        #if k = 0.XX
                        if k < 1:
                            #read three quarters of bytes at jump back address
                            if k == 0.75:
                                outputBytes.extend(outputBytes[takeAddress: takeAddress + takeNTimesBytes - 1])
                                k -= 0.75
                            #read two quarters of bytes at jump back address
                            elif k == 0.5:
                                outputBytes.extend(outputBytes[takeAddress: takeAddress + int(takeNTimesBytes * 0.5)])
                                k -= 0.5
                            #read a quarter of bytes at jump back address
                            else:
                                outputBytes.extend(outputBytes[takeAddress: takeAddress + takeNTimesBytes - 3])
                                k -= k
                        #if X>0.XX        
                        else:
                            outputBytes.extend(outputBytes[takeAddress:takeAddress + takeNTimesBytes:])
                            k -= 1
                #if graphic is decompressed
                if len(outputBytes) == size:
                    break
            #if bit flag is false read decompressed byte to ouput
            else:
                outputBytes.extend(in_gba_file.read(1))
    
    in_gba_file.close()
    graphicHeader = [color, size]
    return graphicHeader, outputBytes
    
    
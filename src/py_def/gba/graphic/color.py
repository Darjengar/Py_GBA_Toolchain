'''
Created on 12.04.2017

@author: HunterxPokemon
'''

MASK = 0x1F

class RGB5:
    '''
    Class RGB5
    '''
    def __init__(self, color):
        self.red = color and MASK
        self.green = color >> 5 and MASK
        self.blue = color >> 10 and MASK
    
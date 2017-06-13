'''
Created on 10.04.2017

@author: HunterxPokemon
'''

#error classes
class Error(Exception):
    """Base class for other exceptions"""
    pass

class Lz77CompressedError(Error):
    """Raised if the graphic has no Lz77 format"""
    pass

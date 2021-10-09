# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:42:33 2021

@author: Linus
"""

from en15804lcadata import En15804LcaData

class En15804MainLcaData(En15804LcaData):
    
    def __init__(self, parent = None):
        super(En15804LcaData, self).__init__(parent)
        
        self._fallback = None
    
    @property
    def fallback(self):
        return(self._fallback)
    
    @fallback.setter
    def fallback(self, value):
        if isinstance(value, En15804LcaData):
            self._fallback = value
        else:
            print("En15804MainLcaData.fallback must be string!")
    
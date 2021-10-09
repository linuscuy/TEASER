# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:09:07 2021

@author: Linus
"""

from en15804lcadata import En15804LcaData

class En15804FallbackLcaData(En15804LcaData):
    
    def __init__(self, parent = None):
        super(En15804LcaData, self).__init__(parent)
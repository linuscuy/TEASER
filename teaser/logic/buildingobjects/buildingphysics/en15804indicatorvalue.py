# -*- coding: utf-8 -*-

# created September 2021
# by Johannes Linus Cuypers

class en15804IndicatorValue(object):
    def __init__(self, parent = None):
        self.parent = parent
        self._unit = None
        
        self._a1 = None
        self._a2 = None
        self._a3 = None
        self._a1_a3 = None
        
        self._a4 = None
        self._a5 = None
        
        self._b1 = None
        self._b2 = None
        self._b3 = None
        self._b4 = None
        self._b5 = None
        self._b6 = None
        self._b7 = None
        
        self._c1 = None
        self._c2 = None
        self._c3 = None
        self._c4 = None
        
        self._d = None
        
    def _validate_stage_value(self, value, stage_name):
        if isinstance(value, float):
            return(value)
        else:
            if not value:
                return(None)
            try:
                value = float(value)
                return(value)
            except ValueError:
                print("Can't convert value of '{}' to float".format(stage_name))
            
            except TypeError:
                print("Can´t convert {} into float".format(type(value)))
                
    @property
    def unit(self):
        return(self._unit)
    
    @unit.setter
    def unit(self, value):
        if isinstance(value, str):
            self._unit = value
        else:
            print("en15804IndicatorValue.unit must be string!")
                  
    @property
    def a1(self):
        return(self._a1)
    
    @a1.setter
    def a1(self, value):
       self._a1 = self._validate_stage_value(value, "A1")
       
    @property
    def a2(self):
        return(self._a2)
    
    @a2.setter
    def a2(self, value):
       self._a2 = self._validate_stage_value(value, "a2")
       
    @property
    def a3(self):
        return(self._a3)
    
    @a3.setter
    def a3(self, value):
       self._a3 = self._validate_stage_value(value, "a3")
    
    @property
    def a1_a3(self):
        return(self._a1_a3)
    
    @a1_a3.setter
    def a1_a3(self, value):
       self._a1_a3 = self._validate_stage_value(value, "a1_a3")
       
    @property
    def a4(self):
        return(self._a4)
    
    @a4.setter
    def a4(self, value):
       self._a4 = self._validate_stage_value(value, "a4")
       
    @property
    def a5(self):
        return(self._a5)
    
    @a5.setter
    def a5(self, value):
       self._a5 = self._validate_stage_value(value, "a5")
       
    @property
    def b1(self):
        return(self._b1)
    
    @b1.setter
    def b1(self, value):
       self._b1 = self._validate_stage_value(value, "b1")
       
    @property
    def b2(self):
        return(self._b2)
    
    @b2.setter
    def b2(self, value):
       self._b2 = self._validate_stage_value(value, "b2")
       
    @property
    def b3(self):
        return(self._b3)
    
    @b3.setter
    def b3(self, value):
       self._b3 = self._validate_stage_value(value, "b3")
       
    @property
    def b4(self):
        return(self._b4)
    
    @b4.setter
    def b4(self, value):
       self._b4 = self._validate_stage_value(value, "b4")
       
    @property
    def b5(self):
        return(self._b5)
    
    @b5.setter
    def b5(self, value):
       self._b5 = self._validate_stage_value(value, "b5")
       
    @property
    def b6(self):
        return(self._b6)
    
    @b6.setter
    def b6(self, value):
       self._b6 = self._validate_stage_value(value, "b6")
       
    @property
    def b7(self):
        return(self._b7)
    
    @b7.setter
    def b7(self, value):
       self._b7 = self._validate_stage_value(value, "b7")
       
    @property
    def c1(self):
        return(self._c1)
    
    @c1.setter
    def c1(self, value):
       self._c1 = self._validate_stage_value(value, "c1")
       
    @property
    def c2(self):
        return(self._c2)
    
    @c2.setter
    def c2(self, value):
       self._c2 = self._validate_stage_value(value, "c2")
       
    @property
    def c3(self):
        return(self._c3)
    
    @c3.setter
    def c3(self, value):
       self._c3 = self._validate_stage_value(value, "c3")
       
    @property
    def c4(self):
        return(self._c4)
    
    @c4.setter
    def c4(self, value):
       self._c4 = self._validate_stage_value(value, "c4")
       
    @property
    def d(self):
        return(self._d)
    
    @d.setter
    def d(self, value):
       self._d = self._validate_stage_value(value, "d")
       
    def set_values(self, **values):
        for attr, value in values.items():
            setattr(self, attr, value)

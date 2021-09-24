# -*- coding: utf-8 -*-

# created September 2021
# by Johannes Linus Cuypers

class En15804IndicatorValue(object):
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
            print("En15804IndicatorValue.unit must be string!")
                  
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
    
    def _ignore_none_sum(self, value1, value2):
        if value1 and value2:
            return(value1 + value2)
        else:
            if not value1 and not value2:
                return(None)
            else:
                if value1:
                    return(value1)
                else:
                    return(value2)
                
    def __add__(self, other):
        
        if isinstance(other, En15804IndicatorValue):

            values = {"a1": self._ignore_none_sum(self.a1, other.a1),
                "a2": self._ignore_none_sum(self.a2, other.a2),
                "a3": self._ignore_none_sum(self.a3, other.a3),
                "a1_a3": self._ignore_none_sum(self.a1_a3, other.a1_a3),
                "a4": self._ignore_none_sum(self.a4, other.a4),
                "a5": self._ignore_none_sum(self.a5, other.a5),
                "b1": self._ignore_none_sum(self.b1, other.b1),
                "b2": self._ignore_none_sum(self.b2, other.b2),
                "b3": self._ignore_none_sum(self.b3, other.b3),
                "b4": self._ignore_none_sum(self.b4, other.b4),
                "b5": self._ignore_none_sum(self.b5, other.b5),
                "b6": self._ignore_none_sum(self.b6, other.b6),
                "b7": self._ignore_none_sum(self.b7, other.b7),
                "c1": self._ignore_none_sum(self.c1, other.c1),
                "c2": self._ignore_none_sum(self.c2, other.c2),
                "c3": self._ignore_none_sum(self.c3, other.c3),
                "c4": self._ignore_none_sum(self.c4, other.c4),
                "d": self._ignore_none_sum(self.d, other.d)}

            
            new = En15804IndicatorValue()
            new.set_values(**values)
            return(new)
        else:
            print("Addend must be 'en15804IndicatorValue'-Object!")
            
    def _ignore_none_mul(self, value1, value2):
        if not value1 or not value2:
            return(None)
        else:
            return(value1 * value2)
        
    def __mul__(self, scalar):
        try:
            scalar = float(scalar)
            
            values = {"a1": self._ignore_none_mul(self.a1, scalar),
                "a2": self._ignore_none_mul(self.a2, scalar),
                "a3": self._ignore_none_mul(self.a3, scalar),
                "a1_a3": self._ignore_none_mul(self.a1_a3, scalar),
                "a4": self._ignore_none_mul(self.a4, scalar),
                "a5": self._ignore_none_mul(self.a5, scalar),
                "b1": self._ignore_none_mul(self.b1, scalar),
                "b2": self._ignore_none_mul(self.b2, scalar),
                "b3": self._ignore_none_mul(self.b3, scalar),
                "b4": self._ignore_none_mul(self.b4, scalar),
                "b5": self._ignore_none_mul(self.b5, scalar),
                "b6": self._ignore_none_mul(self.b6, scalar),
                "b7": self._ignore_none_mul(self.b7, scalar),
                "c1": self._ignore_none_mul(self.c1, scalar),
                "c2": self._ignore_none_mul(self.c2, scalar),
                "c3": self._ignore_none_mul(self.c3, scalar),
                "c4": self._ignore_none_mul(self.c4, scalar),
                "d": self._ignore_none_mul(self.d, scalar)}
            
            new = En15804IndicatorValue()
            new.set_values(**values)
            return(new)
            
        except ValueError:
            print("Can't convert value of '{}' to float. Please insert scalar!".format(scalar))
        
        except TypeError:
            print("Can´t convert {} into float. Please insert scalar!".format(type(scalar)))
            
    def sum_stages(self, add_stage_d = False):
        addends = []
        
        if self.a1: addends.append(self.a1)
        if self.a2: addends.append(self.a2)
        if self.a3: addends.append(self.a3)
        if self.a1_a3: addends.append(self.a1_a3)
        if self.a4: addends.append(self.a4)
        if self.a5: addends.append(self.a5)
        if self.b1: addends.append(self.b1)
        if self.b2: addends.append(self.b2)
        if self.b3: addends.append(self.b3)
        if self.b4: addends.append(self.b4)
        if self.b5: addends.append(self.b5)
        if self.b6: addends.append(self.b6)
        if self.b7: addends.append(self.b7)
        if self.c1: addends.append(self.c1)
        if self.c2: addends.append(self.c2)
        if self.c3: addends.append(self.c3)
        if self.c4: addends.append(self.c4)
        if self.d and add_stage_d: addends.append(self.d)
        
        return(sum(addends))
    
        

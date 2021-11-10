# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 15:33:51 2021

@author: Linus
"""

import uuid

from teaser.logic.buildingobjects.buildingphysics.en15804indicatorvalue import En15804IndicatorValue

import teaser.data.input.lca_data_input as lca_data_input

class En15804LcaData(object):
    """En15804LcaData class
    
    This class can be used to store environmental indicators according to 
    EN 15804 
    
    Parameters
    ----------
    
    parent : XXX, optional
        Default is None
    
    Attributes
    ----------
        ref_flow_value : float [-]
            value of the reference flow
        ref_flow_unit : str
            unit of the reference flow
        pere : En15804IndicatorValue [MJ]
            Use of renewable primary energy
        perm : En15804IndicatorValue [MJ]
            Use of renewable primary energy resources used as raw materials
        pert : En15804IndicatorValue [MJ]
            Total use of renewable primary energy resources
        penre : En15804IndicatorValue [MJ]
            Use of non renewable primary energy 
        penrm : En15804IndicatorValue [MJ]
            Use of non renewable primary energy resources used as raw materials
        penrt : En15804IndicatorValue [MJ]
            Total use of non renewable primary energy resource 
        sm : En15804IndicatorValue [kg]
            Use of secondary material 
        rsf : En15804IndicatorValue [MJ]
            Use of renewable secondary fuels 
        nrsf : En15804IndicatorValue [MJ]
            Use of non renewable secondary fuels 
        fw : En15804IndicatorValue [m^3]
            Use of net fresh water 
        hwd : En15804IndicatorValue [kg]
            Hazardous waste disposed
        nhwd : En15804IndicatorValue [kg]
            Non hazardous waste dispose 
        rwd : En15804IndicatorValue [kg]
            Radioactive waste disposed
        cru : En15804IndicatorValue [kg]
            Components for re-use 
        mfr : En15804IndicatorValue [kg]
            Materials for recycling 
        mer : En15804IndicatorValue [kg]
            Materials for energy recovery
        eee : En15804IndicatorValue [MJ]
            Exported electrical energy 
        eet : En15804IndicatorValue [MJ]
            Exported thermal energy
        gwp : En15804IndicatorValue [kg CO2 eq.]
            Global warming potential
        odp : En15804IndicatorValue [kg R11 eq.]
            Depletion potential of the stratospheric ozone layer 
        pocp : En15804IndicatorValue [kg Ethene eq.]
            Formation potential of tropospheric ozone 
        ap : En15804IndicatorValue [kg SO2 eq.]
            Acidification potential of soil and water 
        ep : En15804IndicatorValue [kg Phosphate eq.]
            Eutrophication potential 
        adpe : En15804IndicatorValue [kg Sb eq.]
            Abiotic depletion potential for non fossil resources
        adpf : En15804IndicatorValue [MJ]
            Abiotic depletion potential for fossil resources 
    """
    def __init__(self, parent = None):
      
        self.lca_data_id = str(uuid.uuid1())
        
        self._name = None
        
        self._ref_flow_value = None
        self._ref_flow_unit = None
        
        self._pere = None
        self._perm = None
        self._pert = None
        self._penre = None
        self._penrm = None
        self._penrt = None
        self._sm = None
        self._rsf = None
        self._nrsf = None
        self._fw = None
        self._hwd = None
        self._nhwd = None
        self._rwd = None
        self._cru = None
        self._mfr = None
        self._mer = None
        self._eee = None
        self._eet = None
        self._gwp = None
        self._odp = None
        self._pocp = None
        self._ap = None
        self._ep = None
        self._adpe = None
        self._adpf = None
        
        self._fallback = None
        
        
    def _check_unit(self, unit, unit_expected, var_name = None):
        """function to check if unit

        Parameters
        ----------
        unit : str
            Unit to be checked
        unit_expected : str
            unit to be expected
        var_name : str, optional
            Name of the Variable to display Error. The default is None.

        Returns
        -------
        Boolean

        """
        
        if unit == unit_expected:
            return(True)
        else:
            if var_name:
                print("Variable '{}' should be specified in {}".format(var_name, unit_expected))
            else:
                print("Please insert value in {}".format(unit_expected))
            return(False)
        
    def _check_en15804indicatorvalue_class(self, value, var_name = None):

        if value:
            if isinstance(value, En15804IndicatorValue): 
                return(True)
            else:
                if var_name:
                    print("'{}' has to be an En15804IndicatorValue-Object!".format(var_name))
                else:
                    print("Please insert a En15804IndicatorValue-Object!")
                return(False)
        else:
            return(False)
        
        
        
        

    @property
    def ref_flow_value(self):
        return self._ref_flow_value
    
    @ref_flow_value.setter
    def ref_flow_value(self, value):
        self.ref_flow_value = value
        
    @property
    def ref_flow_unit(self):
        return self._ref_flow_unit
    
    @ref_flow_unit.setter
    def ref_flow_unit(self, value):
        self.ref_flow_unit = value
        
    @property
    def fallback(self):
        return self._fallback 
    
    @fallback.setter
    def fallback(self, value):
        self._fallback = value
        
    @property
    def pere(self):
        return self._pere
    
    @pere.setter
    def pere(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "pere"):
            if self._check_unit(value.unit, "MJ", "pere"):
                self._pere = value
                
    @property
    def perm(self):
        return self._perm
    
    @perm.setter
    def perm(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "perm"):
            if self._check_unit(value.unit, "MJ", "perm"):
                self._perm = value
                         
    @property
    def pert(self):
        return self._pert 
    
    @pert.setter
    def pert(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "pert"):
            if self._check_unit(value.unit, "MJ", "pert"):
                self._pert = value
                
    @property
    def penre(self):
        return self._penre
    
    @penre.setter
    def penre(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "penre"):
            if self._check_unit(value.unit, "MJ", "penre"):
                self._penre = value
                
    @property
    def penrm(self):
        return self._penrm
    
    @penrm.setter
    def penrm(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "penrm"):
            if self._check_unit(value.unit, "MJ", "penrm"):
                self._penrm = value
                
    @property
    def penrt(self):
        return self._penrt
    
    @penrt.setter
    def penrt(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "penrt"):
            if self._check_unit(value.unit, "MJ", "penrt"):
                self._penrt = value
    
    @property
    def sm(self):
        return self._sm
    
    @sm.setter
    def sm(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "sm"):
            if self._check_unit(value.unit, "kg", "sm"):
                self._sm = value
    
    @property
    def rsf(self):
        return self._rsf
    
    @rsf.setter
    def rsf(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "rsf"):
            if self._check_unit(value.unit, "MJ", "rsf"):
                self._rsf = value
    
    @property
    def nrsf(self):
        return self._nrsf
    
    @nrsf.setter
    def nrsf(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "nrsf"):
            if self._check_unit(value.unit, "MJ", "nrsf"):
                self._nrsf = value
    
    @property
    def fw(self):
        return self._fw
    
    @fw.setter
    def fw(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "fw"):
            if self._check_unit(value.unit, "m^3", "fw"):
                self._fw = value
    
    @property
    def hwd(self):
        return self._hwd
    
    @hwd.setter
    def hwd(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "hwd"):
            if self._check_unit(value.unit, "kg", "hwd"):
                self._hwd = value
                
    @property
    def nhwd(self):
        return self._nhwd
    
    @nhwd.setter
    def nhwd(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "nhwd"):
            if self._check_unit(value.unit, "kg", "nhwd"):
                self._nhwd = value
                
    @property
    def rwd(self):
        return self._rwd
    
    @rwd.setter
    def rwd(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "rwd"):
            if self._check_unit(value.unit, "kg", "rwd"):
                self._rwd = value
                
    @property
    def cru(self):
        return self._cru
    
    @cru.setter
    def cru(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "cru"):
            if self._check_unit(value.unit, "kg", "cru"):
                self._cru = value
                
    @property
    def mfr(self):
        return self._mfr
    
    @mfr.setter
    def mfr(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "mfr"):
            if self._check_unit(value.unit, "kg", "mfr"):
                self._mfr = value
                
    @property
    def mer(self):
        return self._mer
    
    @mer.setter
    def mer(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "mer"):
            if self._check_unit(value.unit, "kg", "mer"):
                self._mer = value
                
    @property
    def eee(self):
        return self._eee
    
    @eee.setter
    def eee(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "eee"):
            if self._check_unit(value.unit, "MJ", "eee"):
                self._eee = value
                
    @property
    def eet(self):
        return self._eet
    
    @eet.setter
    def eet(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "eet"):
            if self._check_unit(value.unit, "MJ", "eet"):
                self._eet = value
                
    @property
    def gwp(self):
        return self._gwp
    
    @gwp.setter
    def gwp(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "gwp"):
            if self._check_unit(value.unit, "kg CO2 eq.", "gwp"):
                self._gwp = value
    
    @property
    def odp(self):
        return self._odp
    
    @odp.setter
    def odp(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "odp"):
            if self._check_unit(value.unit, "kg R11 eq.", "odp"):
                self._odp = value
    
    @property
    def pocp(self):
        return self._pocp
    
    @pocp.setter
    def pocp(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "pocp"):
            if self._check_unit(value.unit, "kg Ethene eq.", "pocp"):
                self._pocp = value
    
    @property
    def ap(self):
        return self._ap
    
    @ap.setter
    def ap(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "ap"):
            if self._check_unit(value.unit, "kg SO2 eq.", "ap"):
                self._ap = value
    
    @property
    def ep(self):
        return self._ep
    
    @ep.setter
    def ep(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "ep"):
            if self._check_unit(value.unit, "kg Phosphate eq.", "ep"):
                self._ep = value
    
    @property
    def adpe(self):
        return self._adpe
    
    @adpe.setter
    def adpe(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "adpe"):
            if self._check_unit(value.unit, "kg Sb eq.", "adpe"):
                self._adpe = value
    
    @property
    def adpf(self):
        return self._adpf
    
    @adpf.setter
    def adpf(self, value):
        if self._check_en15804indicatorvalue_class(value, var_name = "adpf"):
            if self._check_unit(value.unit, "MJ", "adpf"):
                self._adpf = value
    
    def set_values(self, **values):
        """Procedure to set all object-attributes at once

        Parameters
        ----------
        **values : dict
            Dictionary with attribute-name as key and attribute-value as value 

        """
        
        for attr, value in values.items():
            setattr(self, attr, value)
            
    def _ignore_none_mul(self, lca_indicator, scalar):
        if lca_indicator:
            return(lca_indicator * scalar)
        else:
            return None
            

    def __mul__(self, scalar):
        """Multiplies every indicator with a scalar
        

        Parameters
        ----------
        scalar : int, float
            scalar to be mutliplied

        Returns
        -------
        new : En15804LcaData
            product of "self" and scalar
        """       
        
        
        values = {"pere": self._ignore_none_mul(self.pere , scalar),
                "pert": self._ignore_none_mul(self.pert , scalar),
                "penre": self._ignore_none_mul(self.penre , scalar),
                "penrm": self._ignore_none_mul(self.penrm , scalar),
                "penrt": self._ignore_none_mul(self.penrt , scalar),
                "sm": self._ignore_none_mul(self.sm , scalar),
                "rsf": self._ignore_none_mul(self.rsf , scalar),
                "nrsf": self._ignore_none_mul(self.nrsf , scalar),
                "fw": self._ignore_none_mul(self.fw , scalar),
                "hwd": self._ignore_none_mul(self.hwd , scalar),
                "nhwd": self._ignore_none_mul(self.nhwd , scalar),
                "rwd": self._ignore_none_mul(self.rwd , scalar),
                "cru": self._ignore_none_mul(self.cru , scalar),
                "mfr": self._ignore_none_mul(self.mfr , scalar),
                "mer": self._ignore_none_mul(self.mer , scalar),
                "eee": self._ignore_none_mul(self.eee , scalar),
                "eet": self._ignore_none_mul(self.eet , scalar),
                "gwp": self._ignore_none_mul(self.gwp , scalar),
                "odp": self._ignore_none_mul(self.odp , scalar),
                "pocp": self._ignore_none_mul(self.pocp , scalar),
                "ap": self._ignore_none_mul(self.ap , scalar),
                "ep": self._ignore_none_mul(self.ep , scalar),
                "adpe": self._ignore_none_mul(self.adpe , scalar),
                "adpf": self._ignore_none_mul(self.adpf , scalar)
                }
        
        new = En15804LcaData()
        new.set_values(**values)
        
        return(new)

        
    def __add__(self, other):
        
        if isinstance(other, En15804LcaData):

            values = {"pere": self.pere + other.pere,
                        "pert": self.pert + other.pert,
                        "penre": self.penre + other.penre,
                        "penrm": self.penrm + other.penrm,
                        "penrt": self.penrt + other.penrt,
                        "sm": self.sm + other.sm,
                        "rsf": self.rsf + other.rsf,
                        "nrsf": self.nrsf + other.nrsf,
                        "fw": self.fw + other.fw,
                        "hwd": self.hwd + other.hwd,
                        "nhwd": self.nhwd + other.nhwd,
                        "rwd": self.rwd + other.rwd,
                        "cru": self.cru + other.cru,
                        "mfr": self.mfr + other.mfr,
                        "mer": self.mer + other.mer,
                        "eee": self.eee + other.eee,
                        "eet": self.eet + other.eet,
                        "gwp": self.gwp + other.gwp,
                        "odp": self.odp + other.odp,
                        "pocp": self.pocp + other.pocp,
                        "ap": self.ap + other.ap,
                        "ep": self.ep + other.ep,
                        "adpe": self.adpe + other.adpe,
                        "adpf": self.adpf + other.adpf    
                    }
                        
            new = En15804LcaData()
            new.set_values(**values)
            return(new)
        else:      
            print("Addend must be an 'En15804LcaData'-Object!")
            
        def load_lca_data_template(self, lca_id, data_class=self.parent.parent.parent.parent.data):
            """LCA-data loader.

            Loads LCA-data specified in the json.

            Parameters
            ----------

            lca_id : str
                LCA-data Identifier

            data_class : DataClass()
                

            """
            #data_class = self.parent.parent.parent.parent.data
  

            lca_data_input.load_en15804_lca_data_id(lca_data=self,
                                         lca_id=lca_id,
                                         data_class=data_class)
            
        def load_fallbacks(self, fallback_dictonarie, data_class):
            if fallback_dictonarie:
                self.fallback = {}
                for stage in fallback_dictonarie:
                    
                    fallback_id = fallback_dictonarie["stage"]
                    
                    fallback_object = En15804LcaData()
                    
                    self.fallback[stage] = fallback_object
                    
                    self.fallback[stage].load_lca_data_fallback_template(fallback_id, data_class)
        
        def load_lca_data_fallback_tempalte(self, lca_id, data_class=self.parent.parent.parent.parent.data):
            """LCA-data-fallback loader.

            Loads LCA-data-fallbacks specified in the json.

            Parameters
            ----------

            lca_id : str
                LCA-Data Identifier

            data_class : DataClass()
                

            """
               #data_class = self.parent.parent.parent.parent.data


            lca_data_input.load_en15804_lca_data_fallback_id(lca_data=self,
                                         lca_id=lca_id,
                                         data_class=data_class)
            
        def convert_ref_unit(self, target_unit, area = None, thickness = None, density = None):
            
            result = En15804LcaData()
            
            if target_unit == "pcs":

                if self.ref_flow_unit == "m^3":
                    scalar = (area * thickness)
                    
                elif self.ref_flow_unit == "kg":
                    scalar = (area * thickness * density)

                elif self.ref_flow_unit == "m^2":
                    scalar = area
                
                elif self.ref_flow_unit == "pcs":
                    scalar = 1
                    
                else:
                    scalar = 1
                    target_unit = self.unit
                    print("Unknown unit for reference flow!")
            
            #elif target_unit == "m^3":
                
                scalar = scalar / self.ref_flow_value
                result = self * scalar
                result.ref_flow_unit = target_unit
                result.ref_flow_value = 1
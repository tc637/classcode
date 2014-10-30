# -*- coding: utf-8 -*-
"""
TC

tc_radar_equation.py

"""

def radar_equation(k_squared,dbz,dist,atten):
    """Function used to calculate the received power of a radar pulse.
    
    Calculates the received power of a return radar pulse emitted by a Nexsat
    WSR-88D radar.
    
    Uses R. Stull (8.23) and (8.27)
    
    Args:
        k_squared: refractive-index magnitude squared
        dbz: reflectivity factor in dBZ
        dist: range to target in km
        atten: atmospheric attenuation factor
        
    Returns:
        Pr: received power in W
    
    Examples:
    
        Example from Sample Application, p. 246
    
        >>> act = radar_equation(0.93,40,20,1.0)
        >>> exp = 1.09e-8
        >>> abs( act - exp ) < abs( exp ) * EPS
        True
        
    """
    
    # define constants
    R1 = 2.17e-10 # range factor, km
    b = 14255.    # equipment factor
    Pt = 750.0e3  # transmitted power, w
    
    # (8.27)
    reflect = 10**(dbz/10) # reflectivity ratio, Z/Z1
    
    # (8.23)
    Pr = Pt*b*(k_squared/atten)**2*(R1/dist)**2*reflect
    
    return Pr
    
# run test
if __name__ == "__main__":
    import doctest
    EPS = 1.0e-2  # admit 1% error; would be less if result was rounded
    doctest.testmod()

    
    
    
    
    
    
    
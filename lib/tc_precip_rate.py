# -*- coding: utf-8 -*-
"""
TC

tc_precip_rate.py

"""

import numpy as np

def precip_rate(power,k_squared,atten,distance):
    """Function used to calculate the precipitation rate of a storm.
    
    Calculates the precipitation rate of a storm as seen from a distance by a 
    Nexsat WSR-88D radar.
    
    Uses R. Stull (8.23) and (8.30)
    
    Args:
        power: received power of a return pulse, in dBm
        k_squared: refractive-index magnitude squared
        atten: atmospheric attenuation factor
        dist: range to target in km

    Returns:
        rate: precipitation rate, in mm/h
            
    """
    
    # define constants
    R1 = 2.17e-10 # range factor, km
    b = 14255.    # equipment factor
    Pt = 750.0e3  # transmitted power, w
    a1 = 0.0017   # mm/h
    a2 = 0.0714   # dBz^-1
    
    if k_squared == 0.208: # for snow
        a3 = 2000.
        a4 = 2.
    else:                  # for everything else
        a3 = 300. 
        a4 = 1.4
    
    # convert power from dBm to W
    Pr = (10**(power/10))/1000
    
    power_ratio = Pr/Pt
    atmos_effects = k_squared/atten**2
    range_inverse = (R1/distance)**2
    
    # (8.23)
    target_reflect = power_ratio/(b*atmos_effects*range_inverse)
    
    # tried dBz approach
    # (8.28)
    #dBz = 10*np.log10(power_ratio)-10*np.log10(b)-20*np.log(atmos_effects)+20*np.log(range_inverse)
    # (8.27)
    #dBz = 10*np.log(target_reflect)
    # (8.29)
    #rate = a1*10**(a2*dBz)
    
    # (8.30)
    rate = (target_reflect/a3)**(1/a4)
    
    return rate
    

if __name__ == "__main__":
    # rainstorm, no attenuation, target 100 km away
    power = -58.        # dBm
    k_squared_rain = 0.93  # for rain
    atten1 = 1.            # no attenunation
    distance = 100.        # km
    
    rate1 = precip_rate(power,k_squared_rain,atten1,distance)
    
    print('\nRainstorm, no attenuation: {:.2f} mm/h\n'.format(rate1))
    
    # snowstorm, no attenuation
    k_squared_snow = 0.208 # for snow

    rate2 = precip_rate(power,k_squared_snow,atten1,distance)
    
    print('Snowstorm, no attenuation: {:.2f} mm/h\n'.format(rate2))
    
    # rainstorm, factor of 2 for attenuation
    atten2 = 2.              # 3 dBz attenuation
    
    rate3 = precip_rate(power,k_squared_rain,atten2,distance)
    
    print('Rainstorm, 3 dBz attenuation: {:.2f} mm/h\n'.format(rate3))




  
    
    
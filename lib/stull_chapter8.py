# -*- coding: utf-8 -*-
"""
TC

Goes through problems A10-A14 in Chapter 8 of Roland Stull's Practical Meteorology
"""

light = 3.e8 # speed of light, m/s

def beamwidth(wavel,diameter):
    """function for problem A10
    
    Function used to calculate the beamwidth of a radar beam.
    
    Args:
        wavel: wavelength of pulse, cm
        diameter: diameter of antenna dish, m
        
    Returns:
        d_beta: beamwidth of radar beam, degrees
        
    """
    
    a = 71.6 # degrees
    wavel = wavel/100. # convert to m
    d_beta = (a*wavel)/diameter # Stull (8.13)
    return d_beta 
    
    
def bands(wavel):
    """function for problem A11

    Function used to determine the radar band to which the wavelength belongs.
    
    From (Stull 242)

    Args:
        wavel: wavelength of pulse, cm
        
    Returns:
        band: radar band, string
    """
        
    if wavel >= 15 and wavel < 30:
        band = 'L'
        
    elif wavel >= 7.5 and wavel < 15:
        band = 'S'
        
    elif wavel >= 3.75 and wavel < 7.5:
        band = 'C'
        
    elif wavel >= 2.5 and wavel < 3.75:
        band = 'X'
        
    elif wavel >= 1.67 and wavel < 2.5:
        band = 'Ku'
        
    elif wavel >= 0.75 and wavel < 1.11:
        band = 'Ka'
        
    else:
        band = 'invalid wavelength'
      
    return band
    
        
def beam_range(return_time):
    """function for problem A12
    
    Function used to calculate the range from the radar to a target.
    
    Args:
        return_time: return time of pulse, in microseconds
        
    Returns:
        distance: radial distance to target, m
    """

    t = return_time/1.e6
    distance = (light*t)/2. # Stull (8.16)
    return distance
    
    
def max_range(PRF):
    """function for problem A13
    
    Function used to calculate the maximum unambiguous range of a radar pulse.
    
    Args:
        PRF: pulse repetition frequency, s^-1
        
    Returns:
        max_range: maximum unambiguous range, m
    """
    
    max_range = light/(2.*PRF) # Stull (8.17)
    return max_range
    
def doppler_velocity(PRF,wavel):
    """function for problem A14
    
    Function used to calculate the Doppler max unambiguous velocity of a pulse.
    
    Args:
        PRF: pulse repetition frequency, s^-1
        wavel: wavelength, cm
    
    Returns:
        max_velocity: maximum unambiguous velocity, m/s
    """
    
    wavel = wavel/100. # convert to m
    max_velocity = (wavel*PRF)/4 # Stull (8.35)
    
    return max_velocity 
    
if __name__=="__main__":
    # create dictionaries for each problem
    a = [20, 8] 
    b = [20, 10] 
    c = [10, 10] 
    d = [10, 5]
    e = [10, 3]
    f = [5, 7] 
    g = [5, 5] 
    h = [5, 2]
    i = [5, 3]
    j = [3, 1]

    a10_11 = {'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'h':h,'i':i,'j':j}
    
    a12 = {'a':2, 'b':5, 'c':10, 'd':25, 'e':50,'f':75, 'g':100,'h':150, 'i':200, 'j':300}
    
    a13 = {'a':50,'b':100, 'c':200, 'd':400, 'e':600, 'f':800, 'g':1000,'h':1200, 'i':1400,'j':1600}
    
    a14 = [10,5]    
    
    # print out answers
    gap = '==============================='
    print(gap)
    print('A10\n\n')
        
    for key,value in sorted(a10_11.iteritems()):
        width = beamwidth(value[0],value[1])
        
        print('{}: {:>4.3f} degrees\n'.format(key,width))
        
    print(gap)
    print('A11\n\n')
    
    for key,value in sorted(a10_11.iteritems()):
        band = bands(value[0])
        
        print('{}: {:>2}\n'.format(key,band))
        
    print(gap)
    print('A12\n\n')
    
    for key,value in sorted(a12.iteritems()):
        distance = (beam_range(value))/1000.
        
        print('{}: {:>6.2f} km\n'.format(key,distance))
        
    print(gap)
    print('A13\n\n')
    
    for key,value in sorted(a13.iteritems()):
        MUR = max_range(value)/1000.
        
        print('{}: {:>6.1f} km\n'.format(key,MUR))
        
    print(gap)
    print('A14\n\n')
    
    for key,value in sorted(a13.iteritems()):
        MUVi = doppler_velocity(value,a14[0])
        MUVii = doppler_velocity(value,a14[1])
        
        print('{}: (i)  {:>5.2f} m/s       (ii)  {:>5.2f} m/s\n'.format(key,MUVi,MUVii))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
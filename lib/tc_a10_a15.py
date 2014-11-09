import numpy as np

#A10  beamwidth angle


def stull_8_13(the_wavel,dish_size):
    """
       input:  the_wavel : wavelength (cm)
               dish_size : antenna dish diameter (m)
       output: beamwidth : beamwidth angle  (degrees)
              
    """
    a = 71.6 #constant (degrees)
    the_wavel = the_wavel/100. #convert cm to m
    beamwidth = a*the_wavel/dish_size #beamwitdh in degrees
    return beamwidth


letters=['a','b','c','d','e','f','g','h','i','j'] #assignment letter
the_wavel=[20,20,10,10,10,5,5,5,5,3]  #wavelength (cm)
dish_size=[8,10,10,5,3,7,5,2,3,1]   #dishsize (meters)

input_vals=zip(the_wavel,dish_size)

beamwidth=[stull_8_13(wavel,dish_size) for wavel,dish_size in input_vals]

output_pairs=zip(letters,beamwidth)

print "\nQuestion A10\n" 
for letter,beamwidth in output_pairs:
    print "%s) %5.3f degrees" % (letter,beamwidth)

print "\nQuestion A11\n"
prob_tups=zip(letters,the_wavel)
band_vals=[('l_band',15,30),('s_band',7.5,15),('c_band',3.75,7.5),('x_band',2.5,3.75),('ku_band',1.67,2.5),('ka_band',0.75,1.11)]
for letter,wavel in prob_tups:
    for band_name,left_lim,right_lim in band_vals:
        if wavel >= left_lim and wavel < right_lim:
            print "%s) wavelength of %3d cm is %s" % (letter,int(wavel),band_name)
            break

## #A12 Find the range to a radar target, given the round-trip (return) travel times (us) t.
times=[2,5,10,25,50,75,100,150,200,300]

def stull_8_16(delT):
    """
       input:  delT : the round-trip travel times (us)
       output: radar range (km)
    """
    c = 3e8 #speed of light (m/s)
    delT = delT*(1.e-6) #convert  to s
    radar_range = c*delT/2
    return radar_range*1.e-3  #kilometers

radar_range=[stull_8_16(delT) for delT in times]

output_pairs=zip(letters,radar_range)

print "\nQuestion A12\n"

for letter,range in output_pairs:
    print "%s) %3.1f km" % (letter,range)

#A13 Find the radar max unambiguous range for pulse repetition frequencies (s^-1) PRF.

PRFs=[50,100,200,400,600,800,1000,1200,1400,1600]

def stull_8_17(PRF):
    """
       input:  PRF : pulse repetition frequencies (s^-1)
       output: Rmax : the rad max unambiguous range (km)
              
    """
    c = 3.e8 #speed of light (m/s)
    Rmax = c/(2*PRF)
    return Rmax*1.e-3  #range in km

radar_range=[stull_8_17(PRF) for PRF in PRFs]
output_vals=zip(letters,PRFs,radar_range)
     
print "\nQuestion A13\n"

for letter,PRF,range in output_vals:
    print "%s) PRF=%d, range=%3.1f km" % (letter,PRF,range)
     

#A14 Find the Doppler max unambiguous velocity for a radar with pulse repetition frequency (s^-1) 
#    as given in the previous exercise, for radar with wavelength of: (i) 10 cm (ii) 5 cm

def stull_8_35(the_lambda,PRF):
    """
       input:  the_lambda:  wavelength (cm)
               PRF : pulse repetition frequencies (s^-1)
       output: Mmax : the Doppler max unambiguous velocity (m/s)
              
    """
    the_lambda = the_lambda/100. #convert cm to m
    Mmax = the_lambda*PRF/4.
    return Mmax

vel_10cm=[stull_8_35(10,PRF) for PRF in PRFs]

vel_5cm=[stull_8_35(5,PRF) for PRF in PRFs]

output_quad=zip(letters,PRFs,vel_10cm,vel_5cm)

print "\nQuestion A14\n" 
for letter,PRF,vel10,vel5 in output_quad:
    print "%s) PRF=%d Hz, 10 cm velocity=%5.2f m/s, 5 cm velocity=%5.2f m/s" % (letter,PRF,vel10,vel5)


def stull_r7(delT):
    """
       input: delT: pulse duration (us)
       output: the_vol: the size of the radar sample volume (km^3)
    """
    delT=delT*1.e-6 #convert to seconds
    range = 30.e3 #convert km to m
    the_wavel = 10 #cm
    dish_size = 5 #m
    beam_width=stull_8_13(the_wavel,dish_size) #degrees       
    vol_radius = range*(beam_width*np.pi/180.)/2.
    volume=np.pi*vol_radius**2.*delT*3.e8 #m^3
    return volume*1.e-9  #km^3

times=[0.1,0.2,0.5,1.0,1.5,2,3,5]
letters=letters[:7]
volumes=[stull_r7(delT) for delT in times]
output_vals=zip(letters,times,volumes)

print "\nQuestion A15\n" 
for letter,the_time,volume in output_vals:
    print "%s) for pulse duration of %4.1f microseconds the sample volume is %5.2f km^3" % (letter,the_time,volume)

def stull_8_32(Mr,wavel):
    """
        input: Mr: average radial velocity (m/s)
               wavel: wavelength (m)
        output: dopp_shift: magnitude of Doppler frequency shift (s^-1)
    """
    dopp_shift = 2*abs(Mr)/wavel
    return dopp_shift

def stull_8_36(MUV,Mr):
    """
        input: MUV: max unambiguous velocity (m/s)
               Mr:  average radial velocity (m/s)
        output: Mr_dopp: displayed velocity (m/s)
        
    """
    if MUV < Mr and Mr < 2.*MUV:
        Mr_dopp = Mr - 2.*MUV
    elif -2.*MUV < Mr and Mr < -MUV:
        Mr_dopp = Mr + 2.*MUV
    else:
        Mr_dopp = Mr
        
    return Mr_dopp
    
if __name__ == '__main__':
    print('\nQuestion A21\n')
    dBz = np.array([15,30,43,50,18,10])
    time = np.array([10-0,25-10,29-25,30-29,55-30,60-55]) # minutes
    hour_ratio = [t/60. for t in time] # in hours
    
    a1 = 0.0017 # mm/h
    a2 = 0.0714 # dBz^-1
    
    rain_rate = a1*10**(a2*dBz) 
    
    total_rain = sum(rain_rate*hour_ratio) # mm
    
    print('Total rainfall is {:.3} mm.'.format(total_rain))

    print('\nQuestion A22\n')
    
    velocities = np.array([-110,-85,-60,-20,90,65,40,30]) # m/s
    dopp_shifts = stull_8_32(velocities,0.1)
    letters=['a','b','c','d','e','f','g','h','i','j','k','l']
    
    letters_h = letters[:-4]
    
    a22_answers = zip(letters_h,dopp_shifts)
    
    for letter,dopp_shift in a22_answers:
        print('{} {:6} s^-1'.format(letter,dopp_shift))
    
    print ('\nQuestion A23\n')
    real_vels = np.array([26,28,30,35,20,25,55,-26,-28,-30,-35,-20]) # m/s
    
    Mr_dopps = [stull_8_36(25.,float(real_vel)) for real_vel in real_vels]
    
    a23_answers = zip(letters,Mr_dopps)
    
    for letter,Mr_dopp in a23_answers:
        print('{} {:5.1f} m/s'.format(letter,Mr_dopp))
    
    print('\nQuestion A24\n')
    ranges = [205,210,250,300,350,400,230,240,390,410] # km
    
    MUF = 200 # km
    distances = []
    
    for dist in ranges:
        if dist <= MUF:
            distances.append(dist)
        else:
            distances.append(dist-MUF)
    
    letters_j = letters[:-2]
    
    a24_answers = zip(letters,distances)
    
    for letter,distance in a24_answers:
        print('{} {} km'.format(letter,distance))
    
    
    
    
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import sys
#
# use pretty plotting if it can be imported
#
try:
    import seaborn
except:
    pass

sigma=5.67e-8

def find_tau(tot_trans,num_layers):
    """find_tau function, written by P. Austin
    
    Function which produces the vertical optical depth of the 
    atmosphere at each level.
    
    Args:
        tot_trans: Total transmission of the atmosphere, float
        num_layers: Number of layers of the atmosphere, integer
        
    Returns:
        tau_levels: numpy array of optical depth at each level
    """
    trans_layer=tot_trans**(1./num_layers)
    tau_layer= -1.*np.log(trans_layer)
    tau_layers=np.ones([num_layers])*tau_layer
    tau_levels=np.cumsum(tau_layers)
    tau_levels=np.concatenate(([0],tau_levels))
    return tau_levels

def find_heights(press_levels,rho_layers):
    """find_heights function, written by P. Austin
    
    Function which calculates the height of the atmosphere at each pressure level.
    Assumes a hydrostatic atmosphere.
    
    Args:
        press_levels: A numpy array of the pressure levels of the atmosphere, in kPa
        rho_layers: A numpy array of the air density in each layer, in kg/m^3
        
    Returns:
        level_heights: A numpy array of the altitude at each pressure level, in m
    """
    Rd=287.
    g=9.8
    press_layers=(press_levels[1:] + press_levels[:-1])/2.
    del_press=(press_levels[1:] - press_levels[0:-1])
    rho_layers=press_layers/(Rd*Temp_layers)
    del_z= -1.*del_press/(rho_layers*g)
    level_heights=np.cumsum(del_z)
    level_heights=np.concatenate(([0],level_heights))
    return level_heights

def fluxes(tau_levels,Temp_layers,T_surf):
    """fluxes function, written by P. Austin
    
    Calculates the upward and downward long-wave radiative flux across each level.
    Assumes a black surface, and a grey atmosphere.
    
    Upward flux is calculated by iterating from the bottom of the atmosphere
    to the top, starting with the upward surface flux.
    
    Downward flux is calculated by iterating from the top of the atmosphere
    to the bottom, assuming 0 W/m^2 of incoming longwave radiation above the 
    atmosphere.
    
    Args:
        tau_levels: A numpy array of the optical depth at each level.
        Temp_layers: A numpy array of the temperature within each layer, each in K.
        T_surf: The surface temperature, in K as a float.
        
    Returns:
        up_rad: A numpy array of the upward flux across each level, in W/m^2
        down_rad: A numpy array of the downward flux across each level, in W/m^2
    """
    up_rad=np.empty_like(tau_levels)
    down_rad=np.empty_like(tau_levels)
    sfc_rad=sigma*T_surf**4.
    up_rad[0]=sfc_rad
    tot_levs=len(tau_levels)
    for index in np.arange(1,tot_levs):
        upper_lev=index
        lower_lev=index - 1
        layer_num=index-1
        del_tau=tau_levels[upper_lev] - tau_levels[lower_lev]
        trans=np.exp(-1.666*del_tau)
        emiss=1 - trans
        layer_rad=sigma*Temp_layers[layer_num]**4.*emiss
        up_rad[upper_lev]=trans*up_rad[lower_lev] + layer_rad
    down_rad[tot_levs-1]=0
    for index in np.arange(1,tot_levs):
        upper_lev=tot_levs - index
        lower_lev=tot_levs - index -1
        layer_num=tot_levs - index - 1
        del_tau=tau_levels[upper_lev] - tau_levels[lower_lev]
        trans=np.exp(-1.666*del_tau)
        emiss=1 - trans
        layer_rad=sigma*Temp_layers[layer_num]**4.*emiss
        down_rad[lower_lev]=down_rad[upper_lev]*trans + layer_rad
    return (up_rad,down_rad)

def heating_rate(net_up,height_levels,rho_layers):
    """heating_rate function, written by P. Austin
    
    Calculates the heating rate across each layer of the atmosphere by using
    the net flux divergence. Assumes a hydrostatic atmosphere.
    
    Args:
        net_up: A numpy array containing the net upward flux at each layer, W/m^2
        height_levels: A numpy array containing the altitude at each level, m
        rho_layers: A numpy array containing the air density of each layer, kg/m^3
        
    Returns:
        dT_dt: A numpy array containing the net heating rate across each layer, K/s
    """
    cpd=1004.
    dFn_dz= -1.*np.diff(net_up)/np.diff(height_levels)
    dT_dt=dFn_dz/(rho_layers*cpd)
    return dT_dt

def time_step(heating_rate,Temp_layers,delta_time):
    """time_step function, written by P. Austin
    
    Advances the temperature in each layer of the atmosphere by one time step, 
    using the Euler forward method.
    
    Args:
        heating_rate: A numpy array containing the net heating rate across each layer, K/s
        Temp_layers: A numpy array containing the initial temps of each layer, K
        delta_time: The time step used for finite differencing, s
    
    Returns:
        Temp_layers: A numpy array containing the stepped-forward temps of each layer, K
    """
    Temp_layers[:] =  Temp_layers[:] + heating_rate*delta_time
    return Temp_layers

if __name__=="__main__":
    
    tot_trans=0.2
    num_layers=100
    p_sfc=1000.*1.e2
    p_top=100.*1.e2
    g=9.8
    T_sfc=300.
    Rd=287. #J/kg/K
    num_levels=num_layers+1
    tau_levels=find_tau(tot_trans,num_layers)
    press_levels=np.linspace(p_top,p_sfc,num_levels)
    press_diff=np.diff(press_levels)[0]
    press_levels=press_levels[::-1]
    press_layers=(press_levels[1:] + press_levels[:-1])/2.
    Temp_levels=np.ones([num_levels])*T_sfc
    Temp_layers=(Temp_levels[1:] + Temp_levels[:-1])/2.

    S0=241.
    Tc=273.15
    delta_time_hr=30   #time interval in hours
    delta_time_sec=30*3600.  #time interval in seconds
    stop_time_hr=600*24.  #stop time in hours
    times=np.arange(0,stop_time_hr,delta_time_hr) #times in hours
    tot_loops=len(times)
    num_times=len(times)
    #
    # Defined on levels: tau_levels, press_levels, level_heights, up_rad, down_rad
    # Defined on layers: num_layers, rho_layers, Temp_layers, net_up 
    # 
    sfc_temp=np.empty([num_times],dtype=np.float64)
    hours=np.empty_like(sfc_temp)
    #
    # 2-D arrays used to describe space and time, containing the fluxes across
    # each level at each time, and the temperature of each layer at each time.
    #
    air_temps=np.empty([num_layers,num_times],dtype=np.float64)
    up_flux_run=np.empty([num_levels,num_times],dtype=np.float64)
    down_flux_run=np.empty_like(up_flux_run)
    height_levels_run=np.empty_like(up_flux_run)
        
    for index in np.arange(0,num_times):
        rho_layers=press_layers/(Rd*Temp_layers)
        height_levels=find_heights(press_levels,rho_layers)
        up,down=fluxes(tau_levels,Temp_layers,T_sfc)
        sfc_temp[index]=T_sfc
        #
        # Loops through the entirety of num_times (i.e. all times separated in
        # between by delta_time, in hours), to calculate the temperature of each
        # layer at each time, by running all of the functions defined above for
        # each time step.
        #
        if np.mod(index,50)==0:
            the_frac=np.int(index/tot_loops*100.)
            sys.stdout.write("\rpercent complete: %d%%" % the_frac)
            sys.stdout.flush()
        air_temps[:,index]=Temp_layers[:]
        up,down=fluxes(tau_levels,Temp_layers,T_sfc)
        up_flux_run[:,index]=up[:]
        down_flux_run[:,index]=down[:]
        height_levels_run[:,index]=height_levels[:]
        dT_dt=heating_rate(up-down,height_levels,rho_layers)
        Temp_layers[:]=time_step(dT_dt,Temp_layers,delta_time_sec)
        #
        # Calculates the new surface temperature based on the downward longwave
        # and shortwave (solar) flux after each time step.
        #
        net_downsfc=S0 + down[0]
        T_sfc=(net_downsfc/sigma)**0.25
    
    plt.close('all')
    fig1,axis1=plt.subplots(1,1)
    snapshots=[0,2,8,30,40,50,60,70]
    days=times/24.
    for the_snap in snapshots:
        #
        # Labels each temperature profile by days from start.
        #
        label="%3.1f" % days[the_snap]
        height_levels=height_levels_run[:,the_snap]
        layer_heights=(height_levels[1:] + height_levels[:-1])/2.
        axis1.plot(air_temps[:,the_snap],layer_heights*1.e-3,label=label)
        axis1.legend()
    axis1.set_title('temperature profiles for {} days'.format(len(snapshots)))
    axis1.set_xlabel('temperature (deg C)')
    fig1.savefig("snapshots.png")

    fig2,axis2=plt.subplots(1,1)
    axis2.plot(days,sfc_temp-Tc)
    axis2.set_title('surface temperature (deg C)')
    axis2.set_ylabel('temperature (degC)')
    axis2.set_xlabel('day')
    axis2.set_xlim((0,100))
    fig2.savefig("sfc_temp.png")

    fig3,axis3=plt.subplots(1,1)
    axis3.plot(days,sfc_temp - air_temps[0,:])
    axis3.set_title('air-sea temperature difference (deg C)')
    axis3.set_ylabel('surface - first layer temp (degC)')
    axis3.set_xlabel('day')
    axis3.set_xlim((0,100))
    fig3.savefig("air_sea.png")
    
    # closest pressure level to 80 kPa
    min_index_80=np.argmin(np.abs(press_levels - 80.e3)) 
    heights80 = height_levels_run[min_index_80,:]
    
     # closest pressure level to 50 kPa
    min_index_50=np.argmin(np.abs(press_levels - 50.e3))
    heights50 = height_levels_run[min_index_50,:]
    
    fig4,axis4=plt.subplots(1,1)
    axis4.plot(days,heights80/1000.)
    axis4.plot(days,heights50/1000.)
    axis4.set_title('80 kPa and 50 kPa heights vs. time')
    axis4.legend(['80 kPa heights','50 kPa heights'])
    axis4.set_ylabel('height (km)')
    axis4.set_xlabel('day')
    axis4.set_xlim((0,100))
    fig4.savefig("heights.png")
    
    plt.show()

    

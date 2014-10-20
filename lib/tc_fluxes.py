# -*- coding: utf-8 -*-
"""
contains code copied over from the original hydrostat.py
written by P. Austin
"""
import numpy as np
import matplotlib.pyplot as plt

def hydrostat(T_surf,p_surf,dT_dz,delta_z,num_levels):
    """
       build a hydrostatic atmosphere by integrating the hydrostatic equation from the surface,
       using num_layers=num_levels-1 of constant thickness delta_z
       input:  T_surf -- surface temperature in K
              p_surf -- surface pressure in Pa
              dT_dz -- constant rate of temperature change with height in K/m
              delta_z  -- layer thickness in m
              num_levels -- number of levels in the atmosphere
       output:
              numpy arrays: Temp (K) , press (Pa), rho (kg/m^3), height (m)
    """
    Rd=287. #J/kg/K  -- gas constant for dry air
    g=9.8  #m/s^2
    Temp=np.empty([num_levels])
    press=np.empty_like(Temp)
    rho=np.empty_like(Temp)
    height=np.empty_like(Temp)
    num_layers=num_levels-1
    #
    # layer 0 sits directly above the surface, so start
    # with pressure, temp of air equal to ground temp, press
    # and get density from equaiton of state
    # 
    press[0]=p_surf
    Temp[0]=T_surf
    rho[0]=p_surf/(Rd*T_surf)
    height[0]=0
    #
    #now march up the atmosphere a layer at a time
    #using the hydrostatic equation from the Beer's law notes
    #
    for i in range(num_layers):
        delP= -rho[i]*g*delta_z
        height[i+1] = height[i] + delta_z
        Temp[i+1] = Temp[i] + dT_dz*delta_z
        press[i+1]= press[i] + delP
        rho[i+1]=press[i+1]/(Rd*Temp[i+1])
    return (Temp,press,rho,height)

def find_tau(r_gas,k_lambda,rho,height):
    """
       input: r_gas -- gas mixing ratio in kg/kg
              k_lambda -- mass absorption coefficient in kg/m^2
              rho -- vector of air densities in kg/m^3
              height -- corresponding level heights in m
       output:  tau -- vetical optical depth from the surface, same shape as rho
    """
    print r_gas,k_lambda
    tau=np.empty_like(rho)
    tau[0]=0
    num_levels=len(rho)
    num_layers=num_levels-1
    #
    # see Wallace and Hobbs equation 4.32
    #
    for index in range(num_layers):
        delta_z=height[index+1] - height[index]
        delta_tau=r_gas*rho[index]*k_lambda*delta_z
        tau[index+1]=tau[index] + delta_tau
    return tau     


def fluxes(tau,Temp,height,T_surf):
   """
      calculate the flux at every level, by building from bottom up 
      and from top down 
      
       input: tau = vertical optical depth from the surface
              Temp = temp array of the atmosphere at each layer, K
              height = array of levels, m
              T_surf = surface temperature, K
       output:
              numpy arrays: up_flux(W/m^2), down_flux(W/m^2)
    """
   sigma = 5.67e-8
   up_flux=np.empty_like(height)
   down_flux=np.empty_like(height)
   sfc_flux=sigma*T_surf**4.
   up_flux[0]=sfc_flux
   tot_levs=len(tau)
   # now build up_flux from the bottom up
   #
   
   # start at the top of the atmosphere
   # with zero downwelling flux
   for index in np.arange(1,tot_levs):
       up_flux[index] = up_flux[index-1]*np.exp(-(5./3.)*(tau[index]-tau[index-1]))+sigma*(Temp[index]**4)*(1.-np.exp(-(5./3.)*(tau[index]-tau[index-1])))
   #

   #
   # now build down_flux from the top down
   #
   down_flux[tot_levs-1] = 0
   for index in range(tot_levs-2,-1,-1):
       down_flux[index] = down_flux[index+1]*np.exp(-(5./3.)*(tau[index+1]-tau[index]))+sigma*Temp[index]**4*(1-np.exp(-(5./3.)*(tau[index+1]-tau[index])))

   return (up_flux,down_flux)

def heating_rate(up_flux,down_flux,rho,height):
    """
      calculate the heating rate at every level, by taking the flux
      divergence at each level
      
       input: up_flux = upward fluxes array at each layer, W/m^2
              down_flux = downward fluxes array at each layer, W/m^2
              rho = air density array at each layer, kg/m^3
              height = array of levels, m
       output:
              numpy array: heating_rate, K/s
    """
    c_pd = 1004 # J/kg
    heating_rate = np.empty_like(height)
    net_flux = up_flux - down_flux 
    dF = np.diff(net_flux) # calculate dF
    dz = np.diff(height)   # calculate dz
    
    for index in np.arange(0,len(dF)):
        dFdz = dF[index]/dz[index] # calculate dF/dz
        heating_rate[index] = (1/(rho[index]*c_pd))*dFdz # K/s
        
    return heating_rate
        
    
        
    
if __name__=="__main__":
    r_gas=0.01  #kg/kg
    k_lambda=0.01  #m^2/kg
    T_surf=300 #K
    p_surf=100.e3 #Pa
    dT_dz = -7.e-3 #K/km
    delta_z=1
    num_levels=15000    
    Temp,press,rho,height=hydrostat(T_surf,p_surf,dT_dz,delta_z,num_levels)
    tau=find_tau(r_gas,k_lambda,rho,height)
    up_flux,down_flux = fluxes(tau,Temp,height,T_surf)
    heating_rate = heating_rate(up_flux,down_flux,rho,height)
    
    fig1,axis1=plt.subplots(1,1)
    axis1.plot(heating_rate[0:-1]*3600*24,height[0:-1]*1.e-3,'b-')
    axis1.set_title('heating rate vs. height')
    axis1.set_ylabel('height (km)')
    axis1.set_xlabel('heating rate (K/day)')

   
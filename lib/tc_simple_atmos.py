# -*- coding: utf-8 -*-
""" 
Uses a modified version of find_tau to calculate heating rates
"""

import numpy as np
import matplotlib.pyplot as plt

def find_tau(tot_trans,num_layers):
    """
      calculate the optical depth at each height, assuming constant
      transmission across all heights; also returns the heights and densities
      of a uniform atmosphere
      
      bottom of the atmosphere is at 100 kPa, top of atmosphere at 10 kPa
      
      also assumes uniform temperature throughout the atmosphere
      
       input: tot_trans -- total transmission of the atmosphere
              num_layers -- number of layers of the atmosphere

       output:
              numpy arrays: tau_levels, rho (kg/m^3), height (m)
    """
    g = 9.81 # N/m
    p_top = 10  # kPa
    p_sfc = 100 # kPa
    num_levels = num_layers + 1
    
    press_levels=np.linspace(p_top,p_sfc,num_levels)
    press_diff=np.diff(press_levels)[0]
    press_levels=press_levels[::-1]  #flip pressure levels
    mass_layer=press_diff/g
    
    Rd = 287. #J/kg/K  -- gas constant for dry air
    Temp = 300 # K
    
    rho = np.empty_like(press_levels)
    height = np.empty_like(press_levels)
    height[0] = 0
    

    for i in range(num_layers):
        rho[i]=press_levels[i]*1000/(Rd*Temp)
        height[i+1] = (press_diff/(rho[i]*g) + height[i])

    
    trans_layer=tot_trans**(1./num_layers)
    tau_layer= -1.*np.log(trans_layer)
    tau_layers=np.ones([num_layers])*tau_layer
    tau_levels=np.cumsum(tau_layers)
    tau_levels=np.concatenate(([0],tau_levels))
  
    return(tau_levels,rho,height*1000)
    
def fluxes(tau,Temp,height):
   """
      calculate the flux at every level, by building from bottom up 
      and from top down 
      
      assumes an atmosphere at the same temperature as the surface
      
       input: tau = vertical optical depth from the surface
              Temp = temp of the atmosphere, K
              height = array of levels, m
       output:
              numpy arrays: up_flux(W/m^2), down_flux(W/m^2)
    """
   sigma = 5.67e-8
   up_flux=np.empty_like(height)
   down_flux=np.empty_like(height)
   sfc_flux=sigma*Temp**4.
   up_flux[0]=sfc_flux
   tot_levs=len(tau)
   # now build up_flux from the bottom up
   #
   
   # start at the top of the atmosphere
   # with zero downwelling flux
   for index in np.arange(1,tot_levs):
       up_flux[index] = up_flux[index-1]*np.exp(-(5./3.)*(tau[index]-tau[index-1]))+sigma*Temp**4*(1.-np.exp(-(5./3.)*(tau[index]-tau[index-1])))
       print(up_flux[index])
   #

   #
   # now build down_flux from the top down
   #
   down_flux[tot_levs-1] = 0
   for index in range(tot_levs-2,-1,-1):
       down_flux[index] = down_flux[index+1]*np.exp(-(5./3.)*(tau[index+1]-tau[index]))+sigma*Temp**4*(1-np.exp(-(5./3.)*(tau[index+1]-tau[index])))

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
        heating_rate[index] = (-1/(rho[index]*c_pd))*dFdz # K/s
        
    return heating_rate   

if __name__=="__main__":
    
    Temp=300 #K
    num_layers = 100
    tot_trans = 0.2    

    tau,rho,height=find_tau(tot_trans,num_layers)
    up_flux,down_flux = fluxes(tau,Temp,height)
    heating_rate = heating_rate(up_flux,down_flux,rho,height)
    
    fig1,axis1=plt.subplots(1,1)
    axis1.plot(heating_rate[0:-1]*3600*24,height[0:-1]*1.e-3,'b-')
    axis1.set_title('heating rate vs. height')
    axis1.set_ylabel('height (km)')
    axis1.set_xlabel('heating rate (K/day)')    
  
        

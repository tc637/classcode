# -*- coding: utf-8 -*-
"""
tc_subset.py

Uses code from P. Austin's h5_write.py
"""
from __future__ import print_function
    
def output_h5(level1b_file,geom_file,output_name):
    """
        input:  two input filenames or h5py.File objects
          level1b_file
          geom_file
        that contain the
        level1b radiances and reflectivities from Laadsweb and the
        full pixel latitude and longitudes
        and one filename:
           output_name
        that is the name of the file to write the subsetted data to.
        output:  side effect -- writes an output file with new datasets
          chan1, chan31, latitude, longitude and metadata
    """


    import os,site
    import glob
    import h5py
    #
    # add the lib folder to the path assuming it is on the same
    # level as the notebooks folder
    #
    libdir=os.path.abspath('../lib')
    site.addsitedir(libdir)
    from modismeta_h5 import parseMeta
    
    l1b_filename=glob.glob(level1b_file)[0]
    print("found l1b file {}".format(l1b_filename))
    geom_filename=glob.glob(geom_file)[0]
    print("found geom file {}".format(geom_filename))
    
    l1b_file=h5py.File(l1b_filename)
    geom_file=h5py.File(geom_filename)
    
    print(l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['Band_1KM_Emissive'].shape)
    print(l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['Band_1KM_Emissive'][...])
    print(l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].shape)
    
    index31=10
    
    chan31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
    print(chan31.shape,chan31.dtype)
    
    chan31[:3,:3]
    
    scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
    offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]
    
    chan31=(chan31 - offset)*scale
   
    reflective=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'][0,:,:]

    scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['radiance_scales']
    offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['radiance_offsets']
    chan1=(reflective - offset[0])*scale[0]
    
    out=plt.hist(chan1.flat)
    
    the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
    the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]

    f = h5py.File(output_name, "w")
       
    dset = f.create_dataset("lattitude", the_lat.shape, dtype=the_lat.dtype)
    dset[...]=the_lat[...]
    dset = f.create_dataset("longitude", the_lon.shape, dtype=the_lon.dtype)
    dset[...]=the_lon[...]
    dset = f.create_dataset("channel1", chan1.shape, dtype=chan1.dtype)
    dset[...]=chan1[...]
    dset = f.create_dataset("channel31", chan31.shape, dtype=chan31.dtype)
    dset[...]=chan31[...]

    metadata=parseMeta(l1b_file)
    print(metadata)
    
    for the_key in metadata.keys():
        f.attrs[the_key]=metadata[the_key]
    
    f.close()
    
    
        
if __name__ == "__main__":
    import h5py
    from h5dump import dumph5
    l1b_file="MYD021KM.A2013274.2035.005.2013275164943.h5"
    geom_file="MYD03.A2013274.2035.005.2013275155818.h5"
    output_file='test_output.h5'
    output_h5(l1b_file,geom_file,output_file)
    
    # dump out contents of file to see if function works
    f=h5py.File(output_file,'r')
    dumph5(f)
    f.close()
    
    
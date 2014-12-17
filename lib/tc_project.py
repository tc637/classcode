"""
tc_project.py

Timothy Chui
"""


def color_edit(ax,image,xlim,ylim,title,bar_label,font_size):
    """Modifies a colormapped image.
    
    Takes in an axis for a colormapped plot, and adjusts
    the axes limits and font sizes, as well as labels.
    
    Args:
        axis: an instance of Figure
        image: an instance of ax
        xlim: 1-D array for x-axis limits
        ylim: 1-D array for y-axis limits
        title: string for the plot title
        bar_label: string, label for the colorbar
        font_size: integer for label size
        
    """
    
    from matplotlib import pyplot as plt
    
    # set axes limits
    
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    
    # set title
    
    ax.set_title(title)
    
    # make color bar
    
    cbar=plt.colorbar(image)
    
    # set labels
    
    cbar.set_label(bar_label)
    ax.set_ylabel('Height (km)')
    ax.set_xlabel('Longitude (deg W)')
    
    # adjust font sizes
    
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
                 item.set_fontsize(font_size)
    
    
    

def proj_edit(ax,proj,parallels,meridians,longitude,latitude,temp_grid,bar_label,title):
    """Modifies a Basemap projection.
    
    Takes in a projection from Basemap, and creates a plot involving
    MODIS swath temperatures.
    
    Args:
        axis: an instance of Figure
        proj: an instance of Basemap
        parallels: tuple of latitudes
        meridians: tuple of longitudes
        longitude: array of longitudes of the swath
        latitude: array of latitudes of the swath
        temp_grid: array of gridded temperatures
        bar_label: string for the colorbar label
        title: string for the title
         
    """
        
    from matplotlib import pyplot as plt
    
    # draw parallels and meridians
    
    proj.drawparallels(parallels, labels=[1, 0, 0, 0],\
                  fontsize=10, latmax=90)
    proj.drawmeridians(meridians, labels=[0, 0, 0, 1],\
                  fontsize=10, latmax=90)
                  
    # draw coast & fill continents
                  
    out=proj.drawcoastlines(linewidth=1.5, linestyle='solid', color='k')
    x, y=proj(longitude, latitude)
    
    # fill in colors for temperature
    
    CS=proj.pcolor(x, y, temp_grid, cmap=plt.cm.hot)
                  
    # create colorbar
                  
    CBar=proj.colorbar(CS, 'right', size='5%', pad='5%')
    CBar.set_label(bar_label)
    
    # title
    
    title=ax.set_title(title)
        
    
    
    
    
        
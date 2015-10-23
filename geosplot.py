import pylab as pl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable as mal


def geosmap(lon, lat, data, proj = 'mill',
            colorticks=None, colormap='seismic',
            figsize=(18,14),
            latlines=None, lonlines=None,
            ortho0=None):
    if proj == 'mill':
        bmargs = {'projection' : 'mill', 
                  'llcrnrlon' : min(lon), 
                  'llcrnrlat' : min(lat),
                  'urcrnrlon' : max(lon), 
                  'urcrnrlat' : max(lat)
                  }
    elif proj == 'ortho':
        if ortho0:
            lon0 = ortho0[0]
            lat0 = ortho0[1]
        else:
            lon0 = lon[len(lon)/2]
            lat0 = lat[len(lat)/2]
        bmargs = {'projection' : 'ortho',
                  'lon_0' : lon0,
                  'lat_0' : lat0,
                  }
    else:
        print "Projection not recognized"
        return

    bm = Basemap(**bmargs)
    lons, lats = np.meshgrid(lon, lat)
    x, y = bm(lons, lats)

    pl.figure(figsize=figsize)
    ax = pl.gca()
    bm.drawcoastlines(linewidth=1.25, color='white')

    if latlines:
        parallels = latlines
    else:
        parallels = np.array([-60,-30,0,30,60])
    bm.drawparallels(parallels, labels=[1,0,0,0])

    if lonlines:
        meridians = lonlines
    else:
        meridians = np.arange(min(lon),max(lon),60)
    bm.drawmeridians(meridians, labels=[0,0,0,1])

    bm.pcolor(x,y,data, cmap=colormap)

    if colorticks:
        tiks = colorticks
    else:
        tiks = np.linspace(np.min(data),np.max(data),10)

    divider = mal(ax)
    cax = divider.append_axes("right", size='5%', pad=0.05)
    cbar = pl.colorbar(cax=cax,ticks=tiks)

    tiklabs = ['%.2f'%ti for ti in tiks]
    cbar.ax.set_yticklabels(tiklabs)

#    pl.savefig('figs/%s_new_site_metric_%s.png'%(pah,titles[pah][str(tail)]), 
#               bbox_inches='tight')

def make_z(x,y):
    xi = len(x)/3
    yi = 2*len(y)/3
    xx = np.exp(-((x-xi)/100.)**2)
    yy = np.exp(-((y-yi)/55.)**2)
    xx = np.array([list(xx)]*len(y)).T
    yy = np.array([list(yy)]*len(x))
    z = np.ones((len(x), len(y)))
    z = z*xx
    z = z*yy
    return z

if __name__=='__main__':
    
    noise = np.random.rand(46,72)
    
    lon = np.linspace(-180, 175, 72)
    lat = np.linspace(-90, 90, 46)
    lat[0] = -89.
    lat[-1] = 89.

    zdata = 10*make_z(lon,lat).T + noise -5.5

    geosmap(lon,lat,zdata, colorticks = [-5.,-2.5, 0., 2.5, 5])

#    geosmap(lon,lat,zdata, proj='ortho', ortho0 = (50,45), colormap='winter')
    
    pl.show()

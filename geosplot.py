try:
    import pylab as pl
except ImportError:
    print "pylab module required but not found"

try:
    import numpy as np
except ImportError:
    print "numpy module required but not found"

try:
    from mpl_toolkits.basemap import Basemap
except ImportError:
    print "basemap module required but not found"

try:
    from mpl_toolkits.axes_grid1 import make_axes_locatable as mal
except ImportError:
    print "axes_grid1 module required but not found"

import matplotlib as mpl

def geosmap(lon, lat, data, proj = 'mill',
            colorticks=None, colormap='seismic',
            colortick_labels=None,
            colorbar_orientation='vertical',
            figsize=(18,14),
            latlines=None, lonlines=None,
            minlat=None, maxlat=None,
            minlon=None, maxlon=None,
            ortho0=None,
            colorlimits=None,
            coastlines=True,
            countries=False,
            states=False,
            title=None,
            titlefontsize=20.,
            coastcolor='white',
            bordercolor='white',
            plottype='pcolor',
            fontname='sans-serif',
            savefig=False,
            outfile=None,
            subplot=False,
            subplot_position=None,
            fig=None
            ):
    """Plot data on map with lon-lat grid.
    Arguments:
    lon - array-like longitude points
    lat - array-like latitude points
    data - 2D array of points to plot on lon-lat grid
    Keyword Arguments:
    proj - type of projection to plot map on
    colormap - color scheme of color axis
    colorbar_orientation - vertical (default) or horizontal
    colorticks - points to label on color axis
    colortick_labels - labels for colorticks (list of strings)
    colorlimits - (min,max) tuple: saturation colors for color axis 
                  if None, use limits of colorticks
    latlines - latitudes at which to draw lines
    lonlines - longitudes at which to draw lines
    minlat - minimum latitude to map. If None, use min of given lat
    maxlat - maximum latitude to map. If None, use max of given lat
    minlon - minimum longitude to map. If None, use min of given lon
    maxlon - maximum longitude to map. If None, use max of given lon
    figsize - size of figure frame
    ortho0 - (lon,lat) point to center ortho projection on
    coastlines - whether to draw coastlines, default True
    countries - whether to draw country borders, default False
    states - whether to draw sub-country borders (NA only?), default False
    coastcolor - color to make drawn coastlines
    bordercolor - color to make drawn national and state borders
    title - title to put above plot (string)
    fontname - font name (use matplotlib font manager to check 
               available fonts)
    savefig - whether or not to save output to file, default False
    outfile - name of output file if savefig is True
    subplot - whether to plot subplots,
    subplot_position - relative location of each subplot,[nrows,ncols,plot_number]
    fig - create a figure outside of geosplot when subplot is active
               
    """

    # Set font name

    mpl.rcParams['font.family'] = fontname
    
    assert len(lon) in data.shape, 'lon mismatch with data to plot dimension'
    assert len(lat) in data.shape, 'lat mismatch with data to plot dimension'

    if colortick_labels:
        assert colorticks, 'Must specify colorticks if specifying labels'
        assert len(colorticks) == len(colortick_labels), 'colorticks and '\
                                   'colortick labels must be same size' 

    # Set up projection parameters
    if not minlat:
        minlat = min(lat)
    if not maxlat:
        maxlat = max(lat)
    if not minlon:
        minlon = min(lon)
    if not maxlon:
        maxlon = max(lon)

    if proj == 'mill':
        bmargs = {'projection' : 'mill', 
                  'llcrnrlon' : minlon, 
                  'llcrnrlat' : minlat,
                  'urcrnrlon' : maxlon, 
                  'urcrnrlat' : maxlat
                  }
    elif proj == 'ortho':
        if ortho0:
            assert type(ortho0) in [list, tuple, np.array], 'wrong type for ortho0'
            assert len(ortho0) == 2, 'ortho0 must be in the form [lon0, lat0]'
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
    ####################

    # General figure details
    bm = Basemap(**bmargs)
    lons, lats = np.meshgrid(lon, lat)
    x, y = bm(lons, lats)

    # subplot arguments; figure need to be created outside of geosplot for the this to work
    if not fig: 
        fig = pl.figure(figsize=figsize)

    if subplot:
        assert subplot_position is not None, "subplot_position not specified"
        nrows, ncols, plot_number = subplot_position
        fig.add_subplot(nrows, ncols, plot_number)

    ax = pl.gca()

    if coastlines:
        bm.drawcoastlines(linewidth=1.25, color=coastcolor)

    if countries:
        bm.drawcountries(linewidth=1, color=bordercolor)

    if states:
        bm.drawstates(linewidth=1, color=bordercolor)

    if latlines != None:
        parallels = latlines
    else:
        parallels = np.array([-60,-30,0,30,60])
    if not proj in ['ortho']:
        bm.drawparallels(parallels, labels=[1,0,0,0], fontsize=20)

    if lonlines != None:
        meridians = lonlines
    else:
        meridians = np.arange(min(lon),max(lon),60)
    bm.drawmeridians(meridians, labels=[0,0,1,0], fontsize=20)
    ####################

    # Plotting and colorbar
    if colormap == 'WhGrYlRd':
        WhGrYlRd_scheme = np.genfromtxt('WhGrYlRd.txt',delimiter=' ')
        colormap = mpl.colors.ListedColormap(WhGrYlRd_scheme/255)

    if colorticks:
        tiks = colorticks
    else:
        tiks = np.linspace(np.min(data),np.max(data),10)

    if colorlimits:
        vmin, vmax = colorlimits
    else:        
        vmin, vmax = min(tiks), max(tiks)

    if plottype == 'pcolor':
        bm.pcolor(x,y,data, cmap=colormap, vmin=vmin, vmax=vmax)

    elif plottype == 'contourf':
        bm.contourf(x,y,data, vmin=vmin, vmax=vmax, cmap=colormap)
    else:
        print "plottype not recognized"
        raise TypeError
    
    if title and (colorbar_orientation in ['horizontal','bottom']):
        fig.suptitle(title,fontsize=titlefontsize)
    elif title:
        fig.suptitle(title,fontsize=titlefontsize)

    divider = mal(ax)
    if not colortick_labels:
        tiklabs = ['%.2f'%ti for ti in tiks]
    else:
        tiklabs = colortick_labels

    if colorbar_orientation in ['vertical','right']:
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = pl.colorbar(orientation='vertical',cax=cax,ticks=tiks)
        cbar.ax.set_yticklabels(tiklabs, fontsize=20)
    elif colorbar_orientation in ['horizontal','bottom']:
        cax = divider.append_axes('bottom', size='10%', pad=0.1)
        cbar = pl.colorbar(orientation='horizontal',cax=cax,ticks=tiks)
        cbar.ax.set_xticklabels(tiklabs, fontsize=20)

    if savefig:
        if outfile !=None:
            fig.savefig(outfile)

        else:
            print "No outfile given: fig not saved"
            
    return fig
    
  ####################


if __name__=='__main__':

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

    
    noise = np.random.rand(46,72)
    
    lon = np.linspace(-180, 175, 72)
    lat = np.linspace(-90, 90, 46)
    lat[0] = -89.
    lat[-1] = 89.

    zdata = 10*make_z(lon,lat).T + noise -5.5

    fg = geosmap(lon,lat,zdata, colorticks = [-5.,-2.5, 0., 2.5, 5], minlat=-30,
                 colorbar_orientation='right', 
                 colortick_labels=['-5','-2 1/2','zero','2.5','five'],
                 title='Title',subplot=True, subplot_position=(1,2,1))

    fg = geosmap(lon,lat,zdata, proj='ortho', ortho0 = (50,45), 
                colormap='WhGrYlRd',
                plottype='contourf', countries=True, states=True, 
                title='The Title',
                subplot=True, subplot_position=(1,2,2), fig=fg)
    
    pl.show()

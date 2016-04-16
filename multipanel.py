from geosplot import geosmap
import pylab as pl

def squarest(number):
    """Find the squarest number of rows and columns to accomodate
    this number of plots."""

    rows, cols = 1,2
    while rows*cols < number:
        if cols > rows:
            rows += 1
        else:
            cols += 1
    return rows, cols

def multipanel(data,  keyorder=None, colorticks=None, subshape=None, 
               colortick_labels=None, **kwargs):
    """Plot a bunch of dictionary contents according to 
    key names as a multipanel plot.

    Takes a dictionary (data) that contains 'lat':latdata, 'lon':londata,
    and other keys that contain 2D lat-lon datasets. Keyorder is a 
    list of keys that determines the order in which to plot the 
    datasets in data.

    Arguments:
    data - dictionary of lat-lon resolved datasets along with lat 
           and lon data under the keys 'lat' and 'lon'.
    keyorder - list of keys to plot, in the order to plot them.
           
    Keyword Arguments:
    colorticks - list of values to draw colorticks at, default None.
    subshape - (r,c) tuple. number of rows and columns of panels. 
    colortick_labels - list of labels for colorticks. Must be same size
                       as colorticks. default None
    **kwargs - any other kwargs to pass to geosplot
    """
    
    lon = data['lon']
    lat = data['lat']
    keys = [d for d in data.keys() if d not in ['lon','lat']]
    print keys

    if colorticks and colortick_labels:
        assert len(colorticks) == len(colortick_labels), ("There must be a "\
                                          "label for every tick on colorbar")
    if subshape:
        panelslots = subshape[0]*subshape[1]
        assert len(subshape) == 2, "subshape must be (numrows,numcols)" 
    if keyorder and subshape:
        assert len(keyorder) <= panelslots, ("too many keys "\
                                            "for given panel layout") 

    if not keyorder:
        if subshape:
            # fill in available slots
            keyorder = data.keys()[:panelslots]
        else:
            # if no limit to panels, plot all
            keyorder = data.keys()

    if subshape:
        subx, suby = subshape
    else:
        # find the squarest number of rows and columns
        subx, suby = squarest(len(keyorder))

    if not colortick_labels:
        colticks = None
    else:
        colticks = colortick_labels
    fg = geosmap(lon, lat, data[keyorder[0]], subplot=True, 
                 subplot_position=(subx,suby,1), subplot_title=keyorder[0],
                 colorticks=colorticks, colortick_labels=['']*len(colorticks),
                 hide_colorbar=True, **kwargs)

    subcounter = 2 # id of next subplot
    for key in keyorder[1:]:
        if subcounter % subshape[1]: # only draw colorbar at end of row
            cticks = ['']*len(colorticks)
            hide = True
        else:
            cticks = colticks
            hide= False
        fg = geosmap(lon, lat, data[key], subplot=True,
                     subplot_position=(subx,suby,subcounter),
                     fig=fg, subplot_title=key, colortick_labels=cticks,
                     colorticks=colorticks, hide_colorbar=hide,
                     **kwargs)
        subcounter += 1
        

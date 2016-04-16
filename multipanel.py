from geosplot import geosmap
import pylab as pl


def multipanel(data, colorticks, keyorder = None, subshape = None, 
               colortick_labels=None, **kwargs):

    lon = data['lon']
    lat = data['lat']
    keys = [d for d in data.keys() if d not in ['lon','lat']]
    print keys

    if subshape:
        subx, suby = subshape
    else:
        # figure it out
        pass

    if not keyorder:
        # do stuff
        pass

    if not colortick_labels:
        colticks = None
    else:
        colticks = colortick_labels
    fg = geosmap(lon, lat, data[keyorder[0]], subplot=True, 
                 subplot_position=(subx,suby,1), subplot_title=keyorder[0],
                 colorticks=colorticks, colortick_labels=['']*len(colorticks),
                 hide_colorbar=True, **kwargs)

    subcounter = 2
    for key in keyorder[1:]:
        if subcounter % subshape[1]:
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
        

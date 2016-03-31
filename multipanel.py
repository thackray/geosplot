from geosplot import geosmap
import pylab as pl


def multipanel(data, keyorder = None, subshape = None, **kwargs):

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

    fg = geosmap(lon, lat, data[keyorder[0]], subplot=True, 
                 subplot_position=(subx,suby,1), title=keyorder[0],
                 **kwargs)

    subcounter = 2
    for key in keyorder[1:]:
        fg = geosmap(lon, lat, data[key], subplot=True,
                     subplot_position=(subx,suby,subcounter),
                     fig=fg, title=key, **kwargs)


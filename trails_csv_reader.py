import pandas as pd
import dem_xform
import rasterio

# According to my AllTrails data I started here:
start_coords = [39.02472000,-107.051090,3176.0]
# Manually pulled point from hike data for 2nd summit.
second_summit = [39.05371,-107.02017,3773.0]


def get_highest_point():
    fn = 'data/myhike/West Maroon Pass, Frigid Air, Hadley Pass.csv'
    hike = pd.read_csv(fn)
    summit_idx = hike['Elevation'].idxmax()
    max_elevation_pt = hike.loc[summit_idx]
    return max_elevation_pt


def get_path_points():
    fn = 'data/myhike/West Maroon Pass, Frigid Air, Hadley Pass.csv'
    hike = pd.read_csv(fn)
    ds_start = rasterio.open('data/USGS_13_n40w108_20210312.tif', 'r')
    pts = []
    for row in hike.itertuples():
        pt = dem_xform.get_index(ds_start, (row.Latitude, row.Longitude))
        pts.append(pt)
    return pts

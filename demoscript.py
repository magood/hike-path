import rasterio
import numpy as np


ds = rasterio.open('data/USGS_13_n40w108_20210312.tif', 'r')
ds.shape # (10812, 10812)
arr = ds.read() # Reads ALL the values. May take a while and eat all yer RAM.
# arr is now a numpy ndarray, (layer, row, col) of float32 values

# Set a start and end point
# Define the weighting tradeoff between distance and climb
# Write adjacency functions to make the array behave as a graph
# Do shortest path iterations, create and save images, build a gif.

# According to my AllTrails data I started here:
start = [39.02472000,-107.051090]
# And similarly, set an interesting endpoint from an AllTrails sample, using the max elevation:
from trails_csv_reader import get_highest_point
hp = get_highest_point()
end = [hp[0], hp[1]]

# Some example python on this dem:
# >>> ds.bounds
# BoundingBox(left=-108.00055555609345, bottom=38.99944444420663, right=-106.99944444390536, top=40.000555556394715)
# >>> ds.count
# 1
# >>> ds.dtypes
# ('float32',)
# >>> ds.crs
# CRS.from_epsg(4269)
# >>> #crs ref system for this geotiff
# >>> #Use the transform to get coords
# >>> ds.transform
# Affine(9.259259269220167e-05, 0.0, -108.00055555609345,
#        0.0, -9.259259269220167e-05, 40.000555556394715)
# i.e. top right pixel is some coordinate
# >>> ds.transform * (0,0)
# (-108.00055555609345, 40.000555556394715)
# >>> # You can get the coords for any pixel like so:
# >>> ds.xy(50,50)
# (-107.99587963016249, 39.99587963046376)
# >>> # Or get the center of the image:
# >>> ds.xy(ds.height / 2, ds.width / 2)
# (-107.49995370370306, 39.49995370400433)
# >>> #Yep, epsg 4269 is coords: https://epsg.io/4269
# >>> # 1/3 arcsecond is said to be ~10m per pixel and for now we can go with that.
# >>> arr = ds.read()
# >>> arr.shape
# (1, 10812, 10812)
# >>> arr = arr[0]
# >>> arr.shape
# (10812, 10812)
# >>> arr[0,0]
# 1920.1868
# >>> arr[0,1]
# 1920.2319
# >>> arr[0,2]
# 1920.2213
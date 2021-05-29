# Merge the 2 DEMs to include the full hike,
# Then crop to only include a reasonable area.add()
import rasterio
from rasterio.enums import Resampling
import numpy as np
import vis
from devtools import debug


def get_index(ds, coords):
    point = ds.index(coords[1], coords[0]) #poin is r,c index in the ds shape
    return point


def scale_pos(pos, scale_factor, shape):
    """Scale a position in a resized image, ensuring the resulting position remains within the bounds of the image."""
    scaled = (round(pos[0] * scale_factor), round(pos[1] * scale_factor))
    scaled = (min(scaled[0], shape[0]-1), min(scaled[1], shape[1]-1))
    return scaled


def scale_offset_points(points, offset, sf):
    """Translate points to account for offset, scale to acount for scale factor sf."""
    pts = [( int(round((p[0]-offset[0]) * sf)), int(round((p[1]-offset[1]) * sf))) for p in points]
    return pts


def create_merged_dem():
    """Piece together two DEMs, as the hike I did spans a border.
    Save the output as a GeoTIFF to avoid doing this again."""
    #Includes the start of the hike:
    ds_start = rasterio.open('data/USGS_13_n40w108_20210312.tif', 'r')
    debug(ds_start.shape ) # (10812, 10812)
    #Includes the END of the hike:
    ds_end = rasterio.open('data/USGS_13_n40w107_20210312.tif', 'r')
    debug(ds_end.shape) # (10812, 10812)
    left_arr = ds_start.read()[0]
    right_arr = ds_end.read()[0]
    debug(left_arr.shape, right_arr.shape)
    m = np.concatenate((left_arr, right_arr), axis=1)
    debug(m.shape)
    del left_arr
    del right_arr
    # Save a preview:
    vis.quicksave(m, 'data/USGS_merged_13_n40w107-108.preview.png')
    # Save off the merged file.
    # The transform here is TBD and not specified.  May be easier to forgo.
    ds_out = rasterio.open('data/USGS_merged_13_n40w107-108.tif', 'w', driver='GTiff', height=m.shape[0], width=m.shape[1], count=1, dtype=m.dtype, crs=ds_start.crs)
    ds_out.write(m, 1)


def setup_full_dem(start_coords, end_coords):
    """Returns the merged dataset, and start and end indexes in row,column order"""
    ds_start = rasterio.open('data/USGS_13_n40w108_20210312.tif', 'r')
    ds_end = rasterio.open('data/USGS_13_n40w107_20210312.tif', 'r')
    ds = rasterio.open('data/USGS_merged_13_n40w107-108.tif', 'r')
    start = ds_start.index(start_coords[1], start_coords[0]) #r,c coords in the ds shape
    end = ds_end.index(end_coords[1], end_coords[0]) #r,c coords in the ds shape
    # The trek is from West to East, so left to right in this frame.
    # This means the start indexes are also correct in ds.
    # But the end indexes need to be shifted by the shape of ds_start's width:
    end_adjusted = ds_start.shape[1] + end[1]
    end_adjusted = (end[0], end_adjusted)
    # debug(start, end_adjusted, ds.shape)
    return ds, start, end_adjusted


def grow_bounds(ds, start, end, padding_factor=2.0):
    """return new bounds in the dataset ds around the start and end coordinaes,
    grown on each side by padding_factor * max(north-south distance, east-west destance),
    but cropped to the image if necessary.
    This is currently NOT a general solution - only works on southeast treks.
    It should return (topleft, bottomright) in row,col order."""
    dist = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
    extent = dist * padding_factor
    extent = int(extent - dist) # This is how much to add on each side.
    # This starts the non-general code:
    tl = [start[0] - extent, start[1] - extent]
    br = [end[0] + extent, end[1] + extent]
    # debug(extent, start, s2, end, e2)
    # clamp to the ds shape
    tl[0] = sorted((0, tl[0], ds.shape[0]-1))[1]
    tl[1] = sorted((0, tl[1], ds.shape[1]-1))[1]
    br[0] = sorted((0, br[0], ds.shape[0]-1))[1]
    br[1] = sorted((0, br[1], ds.shape[1]-1))[1]
    # debug("clamped", ds.shape, start, s2, end, e2)
    return tuple(tl), tuple(br)


if __name__ == '__main__':
    pass
import numpy as np
from rasterio.windows import Window
import shortestpath as sp
import vis
import dem_xform
import trails_csv_reader as trails
from devtools import debug
from PIL import Image
import multiprocessing
from functools import partial


def get_cropped_dem(endpoint):
    # Set an endpoint from my AllTrails data, using the max elevation:
    ds, start, end = dem_xform.setup_full_dem(trails.start_coords, endpoint)
    extent_tl, extent_br = dem_xform.grow_bounds(ds, start, end, padding_factor=2)
    dem = ds.read(indexes=1,window=((extent_tl[0],extent_br[0]),(extent_tl[1],extent_br[1])))
    # dem.shape -> (867, 1782)
    # Now the start and end indexes are of course skewed by window read we did:
    start = (start[0] - extent_tl[0], start[1] - extent_tl[1])
    end = (end[0] - extent_tl[0], end[1] - extent_tl[1])
    vis.savegoals(dem, start, end, 'data/study_area.preview.png')
    return dem, start, end


def get_cropped_scaled_dem(endpoint, sf=1/10):
    # Use Pillow to do the image resize - this is just easier
    dem, s1, e1 = get_cropped_dem(endpoint)
    dem_im = Image.fromarray(dem)
    (width, height) = (int(round(dem_im.width * sf)), int(round(dem_im.height * sf)))
    im_resized = dem_im.resize((width, height))
    sm_dem = np.array(im_resized)
    # Appropriately scale start and end points to new image size:
    s = dem_xform.scale_pos(s1, sf, sm_dem.shape)
    e = dem_xform.scale_pos(e1, sf, sm_dem.shape)
    vis.savegoals(sm_dem, s, e, f'data/study_area_sf_{sf:.3f}.preview.png')
    return sm_dem, s, e


def run(dem, start, end, sf=1.0, testname = 'hike', zw=1.5):
    outdir = testname
    # adjust the lateral weights for any scaling that has been done.
    scaleweighting = 1 / sf
    print(f'Running for z-weight: {zw:.3f}...')
    dists, prevs = sp.shortest(dem, start, xy_weight=scaleweighting, z_weight=zw)
    path = sp.get_path(dem, end, prevs)
    print(f"Found path from {start} to {end} with cost: {dists[end]}.")
    vis.savepath(dem, path, f'output/{outdir}/path_zw_{zw:.3f}.png')


def iterative_run(dem, start, end, sf=1.0, testname = 'hike', n=5, maxweight=4):
    """Synchronously run over a range of values"""
    z_weights = np.linspace(0, maxweight, n)
    vis.cleardir(f'output/{testname}')
    t = debug.timer()
    for zw in z_weights:
        with t(f'Shortest Path Run, zw: {zw}', verbose=False):
            run(dem, start, end, sf=sf, zw=zw, testname=testname)
    t.summary(verbose=True)


def multi_iterative_run(dem, start, end, sf=1.0, testname = 'hike', n=5, maxweight=4):
    """Use multiprocessing to run for a range of values at once"""
    z_weights = np.linspace(0, maxweight, n)
    vis.cleardir(f'output/{testname}')
    runfunc = partial(run, dem, start, end, sf, testname)
    with multiprocessing.Pool(4) as p:
        p.map(runfunc, z_weights)


def first_summit_run():
    scale = 1/6
    hp = trails.get_highest_point()
    dem, s, e = get_cropped_scaled_dem(hp, sf=scale)
    # Note that if you scale down the dem, you should also scale down the verticals?
    # Or otherwise account for this in the distance calculation using the inverse scale factor.
    print(f"Starting shortest path runs on scaled DEM of shape {dem.shape} from {s} to {e}...")
    multi_iterative_run(dem, s, e, sf=scale, maxweight=4, n=10, testname = 'maroon_sm')


def second_summit_run():
    scale = 1/10
    dem, s, e = get_cropped_scaled_dem(trails.second_summit, sf=scale)
    # Note that if you scale down the dem, you should also scale down the verticals?
    # Or otherwise account for this in the distance calculation using the inverse scale factor.
    print(f"Starting shortest path runs on scaled DEM of shape {dem.shape} from {s} to {e}...")
    multi_iterative_run(dem, s, e, sf=scale, maxweight=4, n=10, testname = 'maroon2_sm')


if __name__ == '__main__':
    second_summit_run()
    first_summit_run()
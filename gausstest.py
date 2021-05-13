import numpy as np
import matplotlib.pyplot as plt
import vis
import shortestpath as sp


def create_gaussian(size=10):
    # Create a 2D Gaussian:
    # From https://www.geeksforgeeks.org/how-to-generate-2-d-gaussian-array-using-numpy/
    x, y = np.meshgrid(np.linspace(-1,1,10), np.linspace(-1,1,10))
    dst = np.sqrt(x*x+y*y)
    # Intializing sigma and muu
    sigma = 1
    muu = 0.000
    # Calculating Gaussian array
    gauss = np.exp(-( (dst-muu)**2 / ( 2.0 * sigma**2 ) ) )
    return gauss


def run(dem, start, end, zrange, num, outdir):
    vis.cleardir(f'output/{outdir}')
    for zw in np.linspace(*zrange, num):
        print(f'Running for z-weight: {zw:.3f}...')
        dists, prevs = sp.shortest(gauss, start, xy_weight=1.0, z_weight=zw)
        path = sp.get_path(gauss, end, prevs)
        print(f"Found path from {start} to {end} with cost: {dists[end]}.")
        print(path)
        vis.savepath(gauss, path, f'output/{outdir}/path_zw_{zw:.3f}.png')


testname = 'gaussiantest'
gauss = create_gaussian(10)
gauss = gauss * 3 # Make it a bigger hill :)
# Add some randomness to the terrain
np.random.seed(0)
r = np.random.rand(10,10)
gauss = gauss + r
# Save off the terrain:
vis.quicksave(gauss, f'output/{testname}/terrain.png')

start = (gauss.shape[0]-1,0) #Bottom-left
end = (0,9) # top right

run(gauss, start, end, (0,4), 10, testname)
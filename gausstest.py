import numpy as np
import matplotlib.pyplot as plt
import vis


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


gauss = create_gaussian(10)
gauss = gauss * 5 # Make it a bigger hill :)
# Add some randomness to the terrain
np.random.seed(0)
r = np.random.rand(10,10)
gauss = gauss + r
# Save off the terrain:
vis.quicksave(gauss, 'output/test/terrain.png')

import shortestpath as sp
start = (gauss.shape[0]-1,0) #Bottom-left
end = (0,9) # top right

dists, prevs = sp.shortest(gauss, start)

path = sp.get_path(end, prevs)
print(f"Found path from {start} to {end} with cost: {dists[end]}.")
print(path)
# Save the path image
vis.savepath(gauss, path, 'output/test/path.png')
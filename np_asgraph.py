import numpy as np
import math


ROOTTWO = math.sqrt(2)


def locs_out(arr, vertex):
    """Gets a list of locations (row,col) of adjacent pixels in the array to the vertex (row,col) specified.
    Akin to "edges out" minus any weights.

    Args:
        vertex (2-tuple): (row,col) location in the image array.

    Returns:
        list of 2-tuples: Every valid neighbor pixel location to the vertex, including diagonals
    """
    # Vertex is a x,y index into the 2d array self.arr as a typle (NOT list)
    v = np.array(vertex)
    out_locs = []
    for u in range(vertex[0]-1, vertex[0]+2):
        for v in range(vertex[1]-1, vertex[1]+2):
            if u >= 0 and u < arr.shape[0] \
                and v >= 0 and v < arr.shape[1] \
                and vertex != (u,v):
                out_locs.append((u,v))
    return out_locs


def distance(arr, u, v, xy_weight=1.0, z_weight=1.0, z_scale=1.0):
    rowdist = abs(u[0] - v[0])
    coldist = abs(u[1] - v[1])
    zdist = abs(arr[u] - arr[v])
    # Cheat the actual formula:
    xydist = rowdist + coldist
    if xydist == 2:
        xydist = ROOTTWO
    # Scale the z dist so that it is the same units as the xydist
    zdist = zdist * z_scale
    return xy_weight * xydist + z_weight * zdist
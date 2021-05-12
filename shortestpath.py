import numpy as np
import np_asgraph as npg

def nextNode(dem, dist, R):
    """Find the next-closest vertex, not yet in the explored region R."""
    unexplored_dists = dist.copy()
    unexplored_dists[R] = np.nan
    mx,my = np.unravel_index(np.nanargmin(unexplored_dists), dist.shape)
    # mindist = unexplored_dists[mx,my]
    return (mx,my)


def shortest(dem, s, xy_weight=1.0, z_weight=1.5):
    dist = np.ones_like(dem) * float("inf")
    dist[s] = 0
    # dist[r,c] is the minimum distance to vertex (r,c) we have found so far.
    R = np.zeros_like(dem, dtype=bool)
    prev = np.empty_like(dem, dtype=tuple)
    while not np.all(R):
        v = nextNode(dem, dist, R)
        R[v] = True
        out_vertices = npg.locs_out(dem, v)
        for z in out_vertices:
            # Compute some "distance" cost based on various weightings
            # 1 pixel lateral = 10 m
            # 1 unit z = 1m.
            # Hence z_scale = 10.0
            z_cost = npg.distance(dem, v, z, xy_weight=xy_weight, z_weight=z_weight, z_scale=10.0)
            if dist[z] > dist[v] + z_cost:
                dist[z] = dist[v] + z_cost
                # Pretty sure this is where we'd set the prev value as well:
                prev[z] = v
    # At the end of this, the distance matrix will be the min cost to every node from s
    # And the previous vertex array
    return dist, prev


def get_path(end, prevs):
    path = []
    path.append(end)
    p = end
    while p is not None:
        p = prevs[p]
        if p is not None:
            path.append(p)
    return list(reversed(path))
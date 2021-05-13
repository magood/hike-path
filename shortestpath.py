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
        u = nextNode(dem, dist, R)
        R[u] = True
        out_vertices = npg.locs_out(dem, u)
        for v in out_vertices:
            # Compute some "distance" cost from u to v based on various weightings
            # 1 pixel lateral = 10 m
            # 1 unit z = 1m.
            # Hence z_scale = 10.0
            uv_dist = npg.distance(dem, u, v, xy_weight=xy_weight, z_weight=z_weight, z_scale=10.0)
            if dist[v] > dist[u] + uv_dist:
                dist[v] = dist[u] + uv_dist
                # Mark the previous vertex, leave the breadcrumbs
                prev[v] = u
    # At the end of this, the distance matrix will be the min cost to every node from s
    # And the previous vertex array
    return dist, prev


def get_path(dem, end, prevs):
    path = []
    path.append(end)
    p = end
    c = 0
    maxpathlen = dem.shape[0] * dem.shape[1]
    while p is not None:
        if c > maxpathlen:
            raise Exception("ERROR: Path has cycles. Are all costs positive?")
        p = prevs[p]
        if p is not None:
            path.append(p)
            c += 1
    return list(reversed(path))
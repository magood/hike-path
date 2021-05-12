import pandas as pd


def get_highest_point():
    fn = 'data/myhike/West Maroon Pass, Frigid Air, Hadley Pass.csv'
    hike = pd.read_csv(fn)
    summit_idx = hike['Elevation'].idxmax()
    max_elevation_pt = hike.loc[summit_idx]
    return max_elevation_pt
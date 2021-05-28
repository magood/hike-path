# Visualization tools
import numpy as np
import matplotlib.pyplot as plt
import os
import glob


def quicksave(arr, fn):
    plt.clf()
    terrain_plt = plt.imshow(arr)
    plt.colorbar(terrain_plt)
    plt.savefig(fn)


def savegoals(arr, start, end, fn):
    """Saves an image of the terrain with start and end points marked"""
    plt.clf()
    terrain_plt = plt.imshow(arr)
    plt.colorbar(terrain_plt)
    plt.scatter(start[1], start[0], marker="p", color="green", zorder=2)
    plt.scatter(end[1], end[0], marker="X", color="blue", zorder=2)
    plt.savefig(fn)

def savepath(arr, path, fn):
    plt.clf()
    terrain_plt = plt.imshow(arr)
    plt.colorbar(terrain_plt)
    p = np.array(path)
    r = p[:,0]
    c = p[:,1]
    plt.plot(c,r, linewidth=1, color='red', zorder=1)
    # Get start and end so we can plot markers:
    start = path[0]
    end = path[-1]
    plt.scatter(start[1], start[0], marker="p", color="green", zorder=2)
    plt.scatter(end[1], end[0], marker="X", color="blue", zorder=2)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(8, 6)
    # when saving, specify the DPI
    plt.savefig(fn, dpi=100)


# Thanks to: https://stackoverflow.com/questions/3812849/how-to-check-whether-a-directory-is-a-sub-directory-of-another-directory
def in_directory(file, directory):
    #make both absolute    
    directory = os.path.join(os.path.realpath(directory), '')
    file = os.path.realpath(file)
    #return true, if the common prefix of both is equal to directory
    #e.g. /a/b/c/d.rst and directory is /a/b, the common prefix is /a/b
    return os.path.commonprefix([file, directory]) == directory


def cleardir(dir):
    # Safety valve - don't delete fiels outside of the working directory
    if in_directory(dir, os.getcwd()):
        files = glob.glob(f'{dir}/*')
        for f in files:
            print(f"removing file: {f}")
            os.remove(f)
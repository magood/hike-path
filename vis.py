# Visualization tools
import numpy as np
import matplotlib.pyplot as plt
import os
import glob


def quicksave(arr, fn):
    plt.clf()
    plt.imshow(arr)
    plt.savefig(fn)

def savepath(arr, path, fn):
    plt.clf()
    plt.imshow(arr)
    p = np.array(path)
    r = p[:,0]
    c = p[:,1]
    plt.plot(c,r, linewidth=3, color='red')
    plt.savefig(fn)


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
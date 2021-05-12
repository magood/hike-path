# Visualization tools
import numpy as np
import matplotlib.pyplot as plt


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
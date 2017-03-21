#!/usr/bin/env python3

import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

cutoff = 20

if __name__ == "__main__":
    names = open(sys.argv[1], 'r', encoding='utf-8').readline().strip().split(',')
    names = names[1:cutoff+1] + [names[-1]]
    df = pd.read_csv(sys.argv[1])
    df = df.drop(df.columns[cutoff+1:-1], axis=1)
    df = df.drop(df.columns[0], axis=1)

    # correlation
    corr = df.corr()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(corr, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, len(names), 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)

    plt.show()

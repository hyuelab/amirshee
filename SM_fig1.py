#!/usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit

# ---------------------------
# Plot settings
# ---------------------------
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
fontsize   = 22
labelsize  = 18
point_size = 64

# 1) Create 1000 points between 0 and 1
x = np.linspace(0, 1, 1000)

# 2) Define the "harmonic" curve as (1 - x)^2
y_harmonic = (1 - x)**2

# 3) Define the three alpha values and corresponding colors
alphas = [0.5, 0.1, 0.01]
colors = ['c', 'b', 'g']   # cyan, blue, green
linestyles = ['--', '-.', ':'] 

# Precompute denominators D0^-1 = exp(2alpha) - 2 exp(alpha) + 1 for each alpha
denoms = [np.exp(2*alpha) - 2*np.exp(alpha) + 1 for alpha in alphas]

plt.figure(figsize=(8, 6))

# 4) Plot each "morse-shifted" curve with its own linestyle, linewidth=2.5
for alpha, denom, col, ls in zip(alphas, denoms, colors, linestyles):
    # V_shift(x) = [exp(2alpha(1-x)) - 2 exp(alpha(1-x)) + 1] / [exp(2alpha) - 2 exp(alpha) + 1]
    y_morse = (np.exp(2*alpha*(1 - x))
               - 2*np.exp(alpha*(1 - x))
               + 1) / denom

    plt.plot(
        x, y_morse,
        linestyle=ls,
        color=col,
        linewidth=3.0,
        label=rf'$\kappa={alpha}$'
    )

# 5) Plot the harmonic curve in solid red, linewidth=2.5
plt.plot(
    x, y_harmonic,
    color='r',
    linestyle='-',
    linewidth=3.5,
    alpha = 0.75,
    label=r'$\mathrm{Harmonic}$'
)

# 6) Formatting: no grid, set limits, labels, and force a boxed legend
plt.xlim(-0.01, 1)
plt.ylim(-0.01, 1)
plt.xlabel(r'$r$', fontsize=fontsize)
plt.ylabel(r'$U(r)$', fontsize=fontsize)

# 7) Adjust ticks: inward direction, mirror on top/right, and set label size
plt.tick_params(
    axis='both',
    which='both',
    direction='in',
    top=True,
    right=True,
    labelsize=labelsize
)

leg = plt.legend(loc='upper right', fontsize=fontsize, frameon=True)
leg.get_frame().set_edgecolor('black')

# 8) Turn off the grid lines
plt.grid(False)

plt.tight_layout()
plt.savefig('SM_fig0.png', dpi=600)
plt.show()

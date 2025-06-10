#!/usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, AutoMinorLocator
import matplotlib.ticker as mticks

# ---------------------------
# Plot settings
# ---------------------------
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
fontsize   = 20
labelsize  = 18

# ---------------------------
# Directories
# ---------------------------
data_dir       = 'data'
fig_output_dir = 'figures'
os.makedirs(fig_output_dir, exist_ok=True)

# ---------------------------
# Discover alpha and Pe values
# ---------------------------
alpha_vals, Pe_vals = set(), set()
for fn in os.listdir(data_dir):
    if not fn.endswith('.csv'): continue
    parts = fn[:-4].split('_')
    if 'alpha' in parts and 'Pe' in parts:
        try:
            alpha_vals.add(float(parts[parts.index('alpha') + 1]))
            Pe_vals.add(float(parts[parts.index('Pe') + 1]))
        except ValueError:
            continue
alpha_vals = sorted(alpha_vals)
Pe_vals    = sorted(Pe_vals)
if not alpha_vals or not Pe_vals:
    sys.exit('No alpha/Pe values found')

# ---------------------------
# Load data for skewness and kurtosis
# ---------------------------
# We expect CSVs with columns: Shear Rate, Skewness, Kurtosis
records = []
target_gamma = 1e-6
rtol = 1e-2
for fn in os.listdir(data_dir):
    if not fn.endswith('.csv'): continue
    parts = fn[:-4].split('_')
    try:
        alpha = float(parts[parts.index('alpha') + 1])
        Pe    = float(parts[parts.index('Pe') + 1])
    except (ValueError, IndexError):
        continue
    df = pd.read_csv(os.path.join(data_dir, fn))
    if 'Shear Rate' not in df.columns:
        continue
    # select gamma = target_gamma
    df_sel = df[np.isclose(df['Shear Rate'], target_gamma, rtol=rtol)]
    if df_sel.empty:
        continue
    # average by alpha, Pe (should be single value per file)
    skew = df_sel['Skewness'].mean()
    kurt = df_sel['Kurtosis'].mean()
    records.append({'alpha': alpha, 'Pe': Pe,
                    'Skewness': skew, 'Kurtosis': kurt - 3.0})

if not records:
    sys.exit(f'No data at gamma={target_gamma}')

# ---------------------------
# Build pivot tables
# ---------------------------
df = pd.DataFrame(records)
df_skew = df.pivot(index='alpha', columns='Pe', values='Skewness')
df_kurt = df.pivot(index='alpha', columns='Pe', values='Kurtosis')

# ---------------------------
# Plot heatmaps
# ---------------------------
# ---------------------------
# Plot heatmaps
# ---------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), sharey=False)
fig.subplots_adjust(
     left=0.065, right=0.99, top=0.98, bottom=0.175,
     wspace=0.20, hspace=0.0
)

pcm1 = ax1.pcolormesh(df_skew.columns, df_skew.index, df_skew.values,
                       cmap='coolwarm', alpha = 0.7, shading='auto')
cb1 = fig.colorbar(pcm1, ax=ax1, shrink=0.7, pad=0.03)
cb1.ax.tick_params(labelsize=labelsize, direction='in')                 # colorbar tick label size
cb1.ax.set_title(r"$S_{\sigma}$", fontsize=fontsize, pad=10)


ax1.set_xlabel(r'$\mathrm{Pe}$', fontsize=fontsize, labelpad=-2)
ax1.set_ylabel(r'$\alpha$', fontsize=fontsize, labelpad=-5)

pcm2 = ax2.pcolormesh(df_kurt.columns, df_kurt.index, df_kurt.values,
                       cmap='coolwarm', alpha = 0.7, shading='auto')
cb2 = fig.colorbar(pcm2, ax=ax2, shrink=0.7, pad=0.035)
cb2.ax.tick_params(labelsize=labelsize, direction='in')                       # colorbar tick label size
cb2.ax.set_title(r"$\mathcal{K}_{\sigma}$", fontsize=fontsize, pad=10)
ax2.set_xlabel(r'$\mathrm{Pe}$', fontsize=fontsize, labelpad=-2)
ax2.set_ylabel(r'$\alpha$', fontsize=fontsize, labelpad=-5)


# Major tick spacing
Pe_step   = 10
alpha_step = 0.1

for ax in (ax1, ax2):
    # set major ticks
    ax.xaxis.set_major_locator(mticks.MultipleLocator(Pe_step))
    ax.yaxis.set_major_locator(mticks.MultipleLocator(alpha_step))
    # set minor ticks
    ax.xaxis.set_minor_locator(mticks.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(mticks.AutoMinorLocator(2))
    # turn on the minor ticks
    ax.tick_params(which='major', direction='in', top=True, right=True, labelsize=labelsize)
    ax.tick_params(which='minor', direction='in', top=True, right=True)

ax1.contour(df_kurt.columns, df_kurt.index, df_skew.values, levels=[0.5],
            colors='darkblue', linestyles='-.', linewidths=2.0)

ax2.contour(df_kurt.columns, df_kurt.index, df_kurt.values, levels=[0.5],
            colors='darkred', linestyles=':', linewidths=2.0)

# panel labels
ax1.text(0.02, 0.95, "(c)", transform=ax1.transAxes,
         fontsize=fontsize, fontweight='bold', va='top')
ax2.text(0.02, 0.95, "(d)", transform=ax2.transAxes,
         fontsize=fontsize, fontweight='bold', va='top')

ax1.text(0.15, 0.25, r'$\mathrm{\bf Glass}$', transform=ax1.transAxes,
            fontsize=labelsize, fontweight='bold', va='bottom')
ax1.text(0.65, 0.75, r'$\mathrm{\bf Fluid}$', transform=ax1.transAxes,
            fontsize=labelsize, fontweight='bold', va='top')
ax2.text(0.15, 0.25, r'$\mathrm{\bf Glass}$', transform=ax2.transAxes,
            fontsize=labelsize, fontweight='bold', va='bottom')
ax2.text(0.65, 0.75, r'$\mathrm{\bf Fluid}$', transform=ax2.transAxes,
            fontsize=labelsize, fontweight='bold', va='top')


# Save and show
out_dir = "figures"
os.makedirs(out_dir, exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(
        os.path.join(out_dir, f"fig5cd.{ext}"),
        dpi=600, bbox_inches='tight'
    )

plt.show()

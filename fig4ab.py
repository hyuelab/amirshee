#!/usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
from matplotlib.lines import Line2D

# ---------------------------
# Plot settings
# ---------------------------
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
fontsize   = 20
labelsize  = 18
point_size = 64

# ---------------------------
# Directories
# ---------------------------
data_dir       = "data"
fig_output_dir = "figures"
os.makedirs(fig_output_dir, exist_ok=True)

# ---------------------------
# Discover alpha values from filenames (exclude alpha=0)
# ---------------------------
alpha_values = set()
for fn in os.listdir(data_dir):
    if not fn.endswith('.csv'):
        continue
    parts = fn[:-4].split('_')
    if 'alpha' in parts:
        try:
            alpha = float(parts[parts.index('alpha') + 1])
            if alpha != 0:
                alpha_values.add(alpha)
        except ValueError:
            continue
alpha_values = sorted(alpha_values)
if not alpha_values:
    sys.exit('No non-zero alpha values found in data directory')

# ---------------------------
# Load & flatten data (include alpha and Pe arrays)
# ---------------------------
all_gdot, all_yp, all_sigma, all_alpha, all_pe = [], [], [], [], []
for fn in os.listdir(data_dir):
    if not fn.endswith('.csv'):
        continue
    parts = fn[:-4].split('_')
    try:
        α  = float(parts[parts.index('alpha') + 1])
        Pe = float(parts[parts.index('Pe') + 1])
    except (ValueError, IndexError):
        continue
    if α == 0:
        continue
    df = pd.read_csv(os.path.join(data_dir, fn))
    cols = {c.strip(): c for c in df.columns}
    if 'Shear Rate' not in cols or 'Shear Stress' not in cols:
        continue
    gdot   = df[cols['Shear Rate']].values
    sigma  = df[cols['Shear Stress']].values
    yp_val = α * Pe**2
    all_gdot.append(gdot)
    all_yp.append(np.full_like(gdot, fill_value=yp_val, dtype=float))
    all_sigma.append(sigma)
    all_alpha.append(np.full_like(gdot, fill_value=α, dtype=float))
    all_pe.append(np.full_like(gdot, fill_value=Pe, dtype=float))
if not all_gdot:
    sys.exit('No data points found for non-zero alpha')

gdot     = np.concatenate(all_gdot)
yp       = np.concatenate(all_yp)
sigma    = np.concatenate(all_sigma)
alpha_arr= np.concatenate(all_alpha)
pe_arr   = np.concatenate(all_pe)

# ---------------------------
# Specify only one γ̇ value to plot (10^-6)
# ---------------------------
gamma_val = 1e-6
rtol      = 0.01

# ---------------------------
# Colormap settings for Pe
# ---------------------------
cmap   = plt.cm.viridis
pe_min = pe_arr.min()
pe_max = pe_arr.max()
norm   = plt.Normalize(pe_min, pe_max)

# marker styles for different alpha values
markers = ['o','s','^','D','v','h','P','>','*']

# ---------------------------
# Create two panels
# ---------------------------
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))
for idx, (ax, ylabel, compute_y) in enumerate([
    (ax1, r"$\langle\sigma_{xy}\rangle$", lambda dfm: dfm['sigma'].values),
    (ax2, r"$\eta = \langle\sigma_{xy}\rangle / \dot\gamma$", lambda dfm: dfm['sigma'].values / gamma_val),
]):
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.xaxis.set_major_locator(LogLocator())
    ax.yaxis.set_major_locator(LogLocator())
    ax.set_xlabel(r"$\alpha\,\mathrm{Pe}^2$", fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.tick_params(which='both', direction='in', top=True, right=True, labelsize=labelsize)
    label = "(a)" if idx==0 else "(b)"
    ax.text(0.05, 0.90, label, transform=ax.transAxes, fontsize=fontsize, va='top')

    # filter for this shear rate
    mask = np.isclose(gdot, gamma_val, rtol=rtol)
    for i, α_val in enumerate(alpha_values):
        m = mask & np.isclose(alpha_arr, α_val)
        if not np.any(m):
            continue
        df_sel = pd.DataFrame({
            'yp': yp[m],
            'sigma': sigma[m],
            'pe': pe_arr[m]
        })
        df_mean = df_sel.groupby('yp', as_index=False).mean().sort_values('yp')
        x = df_mean['yp'].values
        y = compute_y(df_mean)
        pe_vals = df_mean['pe'].values
        # remove non-positive values to avoid log warnings
        valid = (x > 0) & (y > 0)
        x = x[valid]
        y = y[valid]
        pe_vals = pe_vals[valid]
        if x.size == 0:
            continue
        # plot smoothed line in black if enough points
        #if x.size > 1:
        #    xs = np.logspace(np.log10(x.min()), np.log10(x.max()), 200)
        #    ys = 10**np.interp(np.log10(xs), np.log10(x), np.log10(y))
        #    ax.plot(xs, ys, '-', lw=2, color='k', zorder=1)
        # scatter mean points colored by Pe
        marker = markers[i % len(markers)]
        ax.scatter(
            x, y,
            c=pe_vals, cmap=cmap, norm=norm,
            marker=marker, edgecolor='k', s=point_size, zorder=2
        )

# legend for alpha markers on first panel
handles = [Line2D([0],[0], marker=markers[i % len(markers)], color='k', linestyle='None', markersize=8,
                   label=rf"${a:.2f}$")
           for i, a in enumerate(alpha_values)]
ax1.legend(handles=handles, title=r"$\alpha$", fontsize=labelsize-2,
           title_fontsize=labelsize, 
           frameon=False, 
           loc='lower left', 
           ncol=2,    
           columnspacing=0.2, 
           labelspacing=0.0,
           handletextpad=0.1, 
           borderpad=0.01)

# colorbar for Pe to the right of panel (b)
mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])
cbar = fig.colorbar(mappable, ax=ax2, pad=0.02)
cbar.set_label(r"$\mathrm{Pe}$", fontsize=fontsize)
cbar.ax.tick_params(labelsize=labelsize, direction='in', which='both')

fig.subplots_adjust(left=0.09, right=0.98, top=0.96, bottom=0.15, wspace=0.2)
out_png = os.path.join(fig_output_dir, 'fig4ab.png')
fig.savefig(out_png, dpi=600)
plt.show()

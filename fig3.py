#!/usr/bin/env python3
import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import  LogNorm
from matplotlib.ticker import AutoMinorLocator


# ---------------------------
# Plot settings
# ---------------------------
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
fontsize   = 20
labelsize  = 18

# ---------------------------
# Load data
# ---------------------------
data_file = "yield_data_alpha_Pe.csv"
data = pd.read_csv(data_file)

data.columns = [c.strip().lower() for c in data.columns]
if 'number_ratio' in data.columns and 'alpha' not in data.columns:
    data.rename(columns={'number_ratio': 'alpha'}, inplace=True)
if 'yield_stress' in data.columns and 'sigma_y' not in data.columns:
    data.rename(columns={'yield_stress': 'sigma_y'}, inplace=True)

for c in ['alpha', 'pe', 'sigma_y']:
    if c not in data.columns:
        print(f"ERROR: Missing column {c}")
        sys.exit(1)

# ---------------------------
# Threshold and pivot
# ---------------------------
ymin = 1e-6
group = data.groupby(['alpha', 'pe'], as_index=False)['sigma_y'].mean()
heatmap_data = group.pivot(index='alpha', columns='pe', values='sigma_y')
heatmap_data.replace([np.inf, -np.inf], np.nan, inplace=True)
heatmap_data.fillna(ymin, inplace=True)

ymax = data['sigma_y'].replace([np.inf, -np.inf], np.nan).dropna().max()

def get_edges(centers):
    centers = np.array(centers, float)
    n = centers.size
    if n <= 1:
        d = abs(centers[0])*0.1 if n==1 and centers[0]!=0 else 0.5
        return np.array([centers[0]-d, centers[0]+d]) if n==1 else np.array([])
    e = np.zeros(n+1)
    e[1:-1] = (centers[:-1] + centers[1:]) / 2
    e[0] = centers[0] - (centers[1] - centers[0]) / 2
    e[-1] = centers[-1] + (centers[-1] - centers[-2]) / 2
    return e

# ---------------------------
# Figure
# ---------------------------
fig = plt.figure(figsize=(8, 6))
gs = fig.add_gridspec(2, 2, height_ratios=[1,2], wspace=0.05, hspace=0.15)

# (a) σᵧ vs Pe
pe_ax = fig.add_subplot(gs[0,0])
marker_a = {0.00:'o',0.15:'s',0.40:'^',0.50:'>'}
pe_ax.plot([], [], ' ', label=r'$\alpha$')


for α, m in marker_a.items():
    sub = data[data['alpha']==α].sort_values('pe')
    real = sub[sub['sigma_y']>ymin]
    drop = sub[sub['sigma_y']<=ymin]

    if not real.empty:
        line, = pe_ax.plot(real['pe'], real['sigma_y'],
                           label=f"${α:.2f}$", marker=m,
                           markeredgecolor='k', linestyle='-',
                           linewidth=1.5, markersize=8)
        color = line.get_color()
    else:
        color = 'k'

    if not drop.empty and not real.empty:
        x_drop = drop['pe'].iloc[0]
        prev = real[real['pe'] < x_drop]
        if not prev.empty:
            sy_prev = prev['sigma_y'].iloc[-1]
            pe_ax.plot([x_drop-2, x_drop-2], [sy_prev, ymin],
                       '--', color=color, linewidth=1.5, zorder=1)

pe_ax.set_xlabel(r"$\mathrm{Pe}$", fontsize=fontsize, labelpad=-40)
pe_ax.set_ylabel(r"$\sigma_Y$", fontsize=fontsize)
pe_ax.set_yscale('log')
pe_ax.set_ylim(ymin, 0.0005)
pe_ax.legend(loc='lower right', fontsize=labelsize-2, frameon=False,
             markerfirst=False, labelspacing=0.0, handletextpad=0.3, borderpad=0.1)
pe_ax.tick_params(labelsize=labelsize, direction='in', which='both', top=True, right=True)
pe_ax.xaxis.set_minor_locator(AutoMinorLocator(5))
pe_ax.text(0.02,0.85,'(a)',transform=pe_ax.transAxes,
           ha='left',va='top',fontsize=fontsize,fontweight='bold')

# (b) σᵧ vs α
alpha_ax = fig.add_subplot(gs[0,1])
marker_b = {0.0:'o',4.0:'s',8.0:'^',12.0:'>'}
alpha_ax.plot([], [], ' ', label=r'$\mathrm{Pe}$')

for Pe, m in marker_b.items():
    sub = data[data['pe']==Pe].sort_values('alpha')
    real = sub[sub['sigma_y']>ymin]
    drop = sub[sub['sigma_y']<=ymin]

    if not real.empty:
        line, = alpha_ax.plot(real['alpha'], real['sigma_y'],
                              label=f"${Pe:.0f}$", marker=m,
                              markeredgecolor='k', linestyle='-',
                              linewidth=1.5, markersize=8)
        color = line.get_color()
    else:
        color = 'k'

    if not drop.empty and not real.empty:
        x_drop = drop['alpha'].iloc[0]
        prev = real[real['alpha'] < x_drop]
        if not prev.empty:
            sy_prev = prev['sigma_y'].iloc[-1]
            alpha_ax.plot([x_drop-0.05, x_drop-0.05], [sy_prev, ymin],
                          '--', color=color, linewidth=1.5, zorder=1)

alpha_ax.set_xlabel(r"$\alpha$", fontsize=fontsize, labelpad=-40)
alpha_ax.set_yscale('log')
alpha_ax.set_ylim(ymin, 0.0005)
alpha_ax.legend(loc='lower right', fontsize=labelsize-2, frameon=False,
                markerfirst=False, labelspacing=0.0, handletextpad=0.3, borderpad=0.1)
alpha_ax.tick_params(axis='y',labelleft=False, direction='in', which='both', top = True, right = True)
alpha_ax.tick_params(axis='x',labelsize=labelsize, direction='in', which='both', top = True, right = True)
alpha_ax.set_yscale("log")
alpha_ax.xaxis.set_minor_locator(AutoMinorLocator(4))
alpha_ax.text(0.02,0.85,'(b)',transform=alpha_ax.transAxes,
             ha='left',va='top',fontsize=fontsize,fontweight='bold')

# (c) Heatmap unchanged...
heatmap_ax = fig.add_subplot(gs[1,:])
pe_edges = get_edges(heatmap_data.columns.values)
alpha_edges = get_edges(heatmap_data.index.values)
im = heatmap_ax.pcolormesh(pe_edges, alpha_edges,
                           heatmap_data.values,
                           cmap='coolwarm_r', alpha = 0.7,
                           norm=LogNorm(vmin=ymin, vmax=ymax),
                           shading='flat')

'''
# --- add this just after your pcolormesh() call in panel (c) ---
sigma_target = 3.985e-04
# build a mesh of the Pe vs α centers
Pe_centers    = heatmap_data.columns.values
alpha_centers = heatmap_data.index.values
X, Y = np.meshgrid(Pe_centers, alpha_centers)

# draw the contour where σᵧ == sigma_target
cs = heatmap_ax.contour(
    X, Y, heatmap_data.values,
    levels=[sigma_target],
    colors='k',
    linestyles='--',
    linewidths=2
)
# label the contour line
heatmap_ax.clabel(
    cs,
    fmt={sigma_target: r'$\sigma_Y = 3.985\times10^{-4}$'},
    fontsize=labelsize-2,
    inline=True
)
'''



heatmap_ax.set_xlabel(r"$\mathrm{Pe}$", fontsize=fontsize)
heatmap_ax.set_ylabel(r"$\alpha$", fontsize=fontsize)
heatmap_ax.tick_params(labelsize=labelsize, direction='in', which='both', top=True, right=True)
heatmap_ax.xaxis.set_minor_locator(AutoMinorLocator(5))
heatmap_ax.yaxis.set_minor_locator(AutoMinorLocator(5))
Pe_vals = np.linspace(min(heatmap_data.columns)+1,
                      max(heatmap_data.columns),300)
alpha_curve = 22/Pe_vals**2
heatmap_ax.plot(Pe_vals,alpha_curve,'k-',linewidth=2.5, label = r'$\alpha \mathrm{Pe}^2=(\alpha \mathrm{Pe}^2)_G$')
heatmap_ax.set_xlim(0,20); heatmap_ax.set_ylim(0,0.5)
heatmap_ax.text(0.25,0.5,'$\\mathbf{Glass}$',
                transform=heatmap_ax.transAxes,
                fontsize=fontsize,fontweight='bold',ha='center')
heatmap_ax.text(0.7,0.5,'$\\mathbf{Fluid}$',
                transform=heatmap_ax.transAxes,
                fontsize=fontsize,fontweight='bold',ha='center')
cbar = plt.colorbar(im, ax=heatmap_ax,
                    orientation='vertical',
                    fraction=0.046, pad=0.02)
cbar.set_label(r"$\sigma_Y$", fontsize=fontsize, labelpad=-20)
cbar.ax.tick_params(direction='in', which='both', labelsize=labelsize)
heatmap_ax.text(0.02,0.98,'(c)',transform=heatmap_ax.transAxes,
               ha='left',va='top',fontsize=fontsize,fontweight='bold')


heatmap_ax.set_xticks([0, 10, 20])
heatmap_ax.set_xticklabels(['$0$', '$10$', '$20$'], fontsize=labelsize)
Pe_vals = np.linspace(min(heatmap_data.columns)+1, max(heatmap_data.columns),300)
#alpha_curve = 2187/Pe_vals**2
#heatmap_ax.plot(Pe_vals,alpha_curve,'k--',linewidth=2)





'''
# — load your jamming‑line data —
crit_df = pd.read_csv('critical_alpha_Pe_jamming.csv')

# exclude Pe == 0 and sort
crit_plot = crit_df[crit_df['Pe'] > 0].sort_values('Pe')

# plot critical points as black circles
heatmap_ax.scatter(
    crit_plot['Pe'],
    crit_plot['alpha'],
    c='grey',
    marker='o',
    s=50
)


# vertical dashed grey line at Pe=3 from α=0 to 0.25
heatmap_ax.plot(
    [3, 3],
    [0, 0.25],
    color='gray',
    linestyle='--',
    linewidth=2
)

# horizontal dashed grey line at α=0.25 from Pe=0 to Pe=3
heatmap_ax.plot(
    [0, 3],
    [0.25, 0.25],
    color='gray',
    linestyle='--',
    linewidth=2
)

heatmap_ax.text(0.05,0.10,'$\\mathbf{Jamming}$',
                transform=heatmap_ax.transAxes,
                fontsize=fontsize,fontweight='bold',ha='center', rotation=90)


'''



# --- load your saved contour data ---
contours = pd.read_csv('contours_alpha_Pe.csv')

# split by metric
skew_cs = contours[contours['metric'] == 'skewness']
kurt_cs = contours[contours['metric'] == 'kurtosis']

# overlay skewness contour (level 0.5)
heatmap_ax.plot(
    skew_cs['Pe'], skew_cs['alpha'],
    linestyle='-.', linewidth=2,
    color='darkblue', label=r'$\mathcal{S}_\sigma (\dot{\gamma}=10^{-6})$'
)

# overlay kurtosis contour (level 0.5)
heatmap_ax.plot(
    kurt_cs['Pe'], kurt_cs['alpha'],
    linestyle=':', linewidth=2,
    color='darkred', label=r'$\mathcal{K}_\sigma (\dot{\gamma}=10^{-6})$'
)

# add a legend (optional)
heatmap_ax.legend(
    loc='upper right', fontsize=labelsize-2,
    frameon=False
)





# Adjust figure margins (modify these values as needed)
plt.subplots_adjust(
    left=0.10,   # Left margin
    right=0.95,  # Right margin
    bottom=0.1,  # Bottom margin
    top=0.98,    # Top margin
)


plt.savefig("fig3.png", dpi=600)
plt.show()

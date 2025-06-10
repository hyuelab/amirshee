import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, AutoMinorLocator
from matplotlib.lines import Line2D
from scipy.interpolate import UnivariateSpline
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
data_dir       = 'data'
fig_output_dir = 'figures'
os.makedirs(fig_output_dir, exist_ok=True)

# ---------------------------
# Discover alpha values (exclude alpha=0)
# ---------------------------
alpha_values = set()
for fn in os.listdir(data_dir):
    if not fn.endswith('.csv'): continue
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
    sys.exit('No non-zero alpha values found')

# ---------------------------
# Load & flatten data for skewness and kurtosis
# ---------------------------
all_gdot, all_yp, all_skew, all_kurt = [], [], [], []
all_alpha, all_pe = [], []
for fn in os.listdir(data_dir):
    if not fn.endswith('.csv'): continue
    parts = fn[:-4].split('_')
    try:
        a_val = float(parts[parts.index('alpha')+1])
        Pe    = float(parts[parts.index('Pe')+1])
    except (ValueError, IndexError):
        continue
    if a_val == 0:
        continue
    df = pd.read_csv(os.path.join(data_dir, fn))
    if 'Shear Rate' not in df.columns or 'Skewness' not in df.columns:
        continue
    gdot_val  = df['Shear Rate'].values
    skew_val  = df['Skewness'].values
    kurt_val  = df['Kurtosis'].values
    yp_val    = a_val * Pe**2
    all_gdot.append(gdot_val)
    all_yp.append(np.full_like(gdot_val, yp_val))
    all_skew.append(skew_val)
    all_kurt.append(kurt_val)
    all_alpha.append(np.full_like(gdot_val, a_val))
    all_pe.append(np.full_like(gdot_val, Pe))

# flatten arrays
gdot      = np.concatenate(all_gdot)
yp        = np.concatenate(all_yp)
skewness  = np.concatenate(all_skew)
kurtosis  = np.concatenate(all_kurt)
alpha_arr = np.concatenate(all_alpha)
pe_arr    = np.concatenate(all_pe)

# ---------------------------
# γ̇ values and styling
# ---------------------------
gamma_list    = [1e-6]
rtol          = 0.01
cmap          = plt.cm.plasma
border_colors = ['k', 'darkred', 'darkblue', 'darkgreen', 'darkorange']
norm          = plt.Normalize(pe_arr.min(), pe_arr.max())
markers       = ['o', 's', '^', 'D', 'v', 'h', 'P', '>', '*', '<']

# ---------------------------
# Create panels for skewness and kurtosis collapse
# ---------------------------
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))
for idx, ax in enumerate((ax1, ax2)):
    ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.xaxis.set_major_locator(LogLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel(r'$\alpha\,\mathrm{Pe}^2$', fontsize=fontsize)
    ax.tick_params(which='both', direction='in', top=True, right=True, labelsize=labelsize)
    ax.text(0.05, 0.90, '(a)' if idx == 0 else '(b)', transform=ax.transAxes, fontsize=fontsize)

    for j, g in enumerate(gamma_list):
        mask = np.isclose(gdot, g, rtol=rtol)
        # scatter data by alpha
        for i, a in enumerate(alpha_values):
            m = mask & np.isclose(alpha_arr, a)
            if not m.any():
                continue
            dfm = pd.DataFrame({
                'yp':    yp[m],
                'value': skewness[m] if idx==0 else kurtosis[m]-3.0,
                'pe':    pe_arr[m]
            })
            dfm = dfm.groupby('yp', as_index=False).mean().sort_values('yp')
            x, y, pe_vals = dfm['yp'].values, dfm['value'].values, dfm['pe'].values
            valid = (x > 0)
            ax.scatter(
                x[valid], y[valid], c=pe_vals[valid], cmap=cmap, norm=norm,
                marker=markers[i % len(markers)], facecolors='none',
                edgecolors=border_colors[j], s=point_size, linewidths=1
            )




    # legends for panel (a)
    if idx == 0:
        # alpha legend
        alpha_handles = [Line2D([0],[0], marker=markers[k], color='k', linestyle='None', markersize=8,
                                 label=f'${{a:.2f}}$'.format(a=a))
                         for k, a in enumerate(alpha_values)]
        alpha_leg = ax.legend(handles=alpha_handles, title=r'$\alpha$', frameon=False,
                              fontsize=labelsize-2, title_fontsize=labelsize,
                              loc='upper left', ncol=2, columnspacing=0.2,
                              labelspacing=0.0, handletextpad=0.1, borderpad=0.05)
        ax.add_artist(alpha_leg)
        # gamma legend
        gamma_handles = [Line2D([0],[0], marker='o', color=border_colors[k], linestyle='None',
                                 markersize=6, markerfacecolor='none', markeredgecolor=border_colors[k],
                                 label=rf'$10^{{{int(np.log10(g))}}}$')
                         for k, g in enumerate(gamma_list)]
        #ax.legend(handles=gamma_handles, title=rf'$\dot\gamma$', frameon=False,
       #          fontsize=labelsize-3, title_fontsize=labelsize,
         #         loc='lower left', bbox_to_anchor=(0.0,0.65), ncol=2,
         #         columnspacing=0.2, labelspacing=0.0, handletextpad=0.1, borderpad=0.0)

ax1.set_ylim(-0.05,1.05)
ax2.set_ylim(-0.45,1.05)
ax1.set_xlim(0.1, 300)
ax2.set_xlim(0.1, 300)
ax1.set_ylabel(r'$\mathcal{S}_{\sigma}$', fontsize=fontsize, labelpad=-50)
ax2.set_ylabel(r'$\mathcal{K}_{\sigma}$', fontsize=fontsize, labelpad=-75)

# Annotate Glass / Fluid
ax1.text(0.15, 0.25, r'$\mathrm{\bf Glass}$', transform=ax1.transAxes,
            fontsize=labelsize, fontweight='bold', va='bottom')
ax1.text(0.75, 0.85, r'$\mathrm{\bf Fluid}$', transform=ax1.transAxes,
            fontsize=labelsize, fontweight='bold', va='top')

ax2.text(0.15, 0.25, r'$\mathrm{\bf Glass}$', transform=ax2.transAxes,
            fontsize=labelsize, fontweight='bold', va='bottom')
ax2.text(0.75, 0.70, r'$\mathrm{\bf Fluid}$', transform=ax2.transAxes,
            fontsize=labelsize, fontweight='bold', va='top')

for ax in (ax1, ax2):
    ax.axvline(17, color='gray', linestyle='--', linewidth=2, alpha=0.7)
    ax.axvline(22, color='gray', linestyle='--', linewidth=2, alpha=0.7)


# colorbar and finalize
mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array([])

#cbar = fig.colorbar(mappable, ax=[ax1, ax2], pad=0.02, shrink=0.4, aspect=10)



# Create colorbar axis manually to the right of ax2
# [left, bottom, width, height] in figure coordinates
cax = fig.add_axes([0.94, 0.2, 0.02, 0.6])  # <-- customize these

# Create colorbar
cbar = fig.colorbar(mappable, cax=cax)
cbar.ax.set_title(r'$\mathrm{Pe}$', fontsize=fontsize, pad=10)
cbar.ax.tick_params(labelsize=labelsize, direction='in')


fig.subplots_adjust(left=0.06, right=0.93, top=0.96, bottom=0.14, wspace=0.22)
out_png = os.path.join(fig_output_dir, 'fig5ab.png')
fig.savefig(out_png, dpi=600)
plt.show()

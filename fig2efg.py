import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator 

# Set Parameters
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
fontsize = 20
labelsize = 18

# Load data from the results file
data_file = "yield_stress.csv"
data = pd.read_csv(data_file)

# Pivot the data to create a matrix for heatmap
heatmap_data = data.pivot(index="alpha", columns="phi", values="sigma_Y")

# Ensure that the rows (phi) and columns (alpha) are sorted
heatmap_data.sort_index(axis=0, inplace=True)  # Sort by phi
heatmap_data.sort_index(axis=1, inplace=True)  # Sort by alpha

# Replace NaN or non-positive values with a small positive number (e.g., 10^{-6})
heatmap_data.replace([np.inf, -np.inf], np.nan, inplace=True)
heatmap_data.fillna(1e-6, inplace=True)
heatmap_data[heatmap_data <= 0] = 1e-6

# Determine color bar range
color_min = 1e-6
color_max = heatmap_data.max().max()

# Create the figure and custom grid layout
fig = plt.figure(figsize=(8, 6))
wspace = 0.05
hspace = 0.15
gs = fig.add_gridspec(2, 2, height_ratios=[1, 2], wspace=wspace, hspace=hspace)
# Subplot for yield stress vs phi for alpha = 0 and 0.15
phi_ax = fig.add_subplot(gs[0, 0])
phi_ax.plot([], [], ' ', label=r'$\alpha$')
marker_styles = {0.00: 'o', 0.05: 's', 0.30: '^', 0.50: '>'} 
for alpha_val in [0.00, 0.05, 0.30, 0.50]:
    subset = data[data["alpha"] == alpha_val]
    subset_sorted = subset.sort_values(by="phi")  # Ensure sorting by phi
    line, = phi_ax.plot(
        subset_sorted["phi"], 
        subset_sorted["sigma_Y"], 
        label = f"${alpha_val:.2f}$", 
        marker=marker_styles[alpha_val],
        markersize=8,
        markeredgecolor='k',
    )

    # Find the minimal sigma_Y for this alpha
    min_sigma_idx = subset_sorted["sigma_Y"].idxmin()
    phi_min = subset_sorted.loc[min_sigma_idx, "phi"]
    sigma_min = subset_sorted.loc[min_sigma_idx, "sigma_Y"]
    
    # Add vertical dashed line from minimal sigma_Y down to 1e-6
    phi_ax.plot(
        [phi_min, phi_min], 
        [sigma_min, 1e-6], 
        linestyle='--', 
        color=line.get_color(),  # Match curve color
        linewidth=1.5,
        zorder=1  # Ensure line is behind markers
    )
phi_ax.set_xlabel(r"$\phi$", fontsize=fontsize, labelpad=-40)
phi_ax.set_ylabel(r"$\sigma_Y$", fontsize=fontsize)
phi_ax.legend(loc='lower right', fontsize=labelsize-2, markerfirst=False,
               labelspacing=0.0, 
               handletextpad=0.3, 
               borderpad=0.1,
               frameon=False)
phi_ax.tick_params(labelsize=labelsize, direction='in', which='both', top = True, right = True)
phi_ax.set_yscale("log")
# Add label (e)
phi_ax.text(0.02, 0.98, '(e)', transform=phi_ax.transAxes, fontsize=fontsize, 
            ha='left', va='top', fontweight='bold')

phi_ax.xaxis.set_minor_locator(AutoMinorLocator(5))
phi_ax.set_ylim(0.000001, 0.004)

# Subplot for yield stress vs alpha for phi = 0.66 and 0.67
alpha_ax = fig.add_subplot(gs[0, 1])
alpha_ax.plot([], [], ' ', label=r'$\phi$')
marker_styles = {0.65: 'o', 0.66: 's', 0.67: '^', 0.68: '>'} 
for phi_val in [0.65, 0.66, 0.67, 0.68]:
    subset = data[data["phi"] == phi_val]
    subset_sorted = subset.sort_values(by="alpha")  # Ensure sorting by alpha
    line, = alpha_ax.plot(
        subset_sorted["alpha"], 
        subset_sorted["sigma_Y"], 
        label=f"${phi_val}$", 
        marker=marker_styles[phi_val],
        markeredgecolor='k',
        markersize=8,
        #markerfacecolor='none',
        linestyle='-',
        linewidth=1.5
    )
    # Add dashed line for phi=0.66 only
    if phi_val == 0.65:
        # Get last point (maximum alpha)
        last_point = subset_sorted.iloc[-1]
        alpha_max = last_point["alpha"]
        sigma_Y_last = last_point["sigma_Y"]
        
        # Draw vertical dashed line to 1e-6
        alpha_ax.plot(
            [alpha_max, alpha_max], 
            [sigma_Y_last, 1e-6], 
            linestyle='--', 
            color=line.get_color(),  # Match curve color
            linewidth=1.5,
            zorder=1  # Behind markers
        )

    if phi_val == 0.66:
        # Get last point (maximum alpha)
        last_point = subset_sorted.iloc[-1]
        alpha_max = last_point["alpha"]
        sigma_Y_last = last_point["sigma_Y"]
        
        # Draw vertical dashed line to 1e-6
        alpha_ax.plot(
            [alpha_max, alpha_max], 
            [sigma_Y_last, 1e-6], 
            linestyle='--', 
            color=line.get_color(),  # Match curve color
            linewidth=1.5,
            zorder=1  # Behind markers
        )



alpha_ax.set_xlabel(r"$\alpha$", fontsize=fontsize, labelpad=-40)
alpha_ax.xaxis.set_label_coords(0.4, 0.18)
alpha_ax.legend(loc='lower right', 
                bbox_to_anchor=(0.9, 0.0),
                fontsize=labelsize-2, 
                markerfirst=False,
                 labelspacing=0.0, 
                 handletextpad=0.5,
                 borderpad=-0.5,
                 frameon=False,
                 ncol=1,
                 columnspacing=0.5)
alpha_ax.tick_params(axis='y',labelleft=False, direction='in', which='both', top = True, right = True)
alpha_ax.tick_params(axis='x',labelsize=labelsize, direction='in', which='both', top = True, right = True)
alpha_ax.set_yscale("log")
# Add label (f)
alpha_ax.text(0.02, 0.98, '(f)', transform=alpha_ax.transAxes, fontsize=fontsize, 
              ha='left', va='top', fontweight='bold')

alpha_ax.xaxis.set_minor_locator(AutoMinorLocator(4))
alpha_ax.set_ylim(0.000001, 0.004)


# Plot the heatmap (phase diagram) using pcolormesh for accurate grid spacing
heatmap_ax = fig.add_subplot(gs[1, :])

# Compute edges for phi and alpha to create proper grid cells
def get_edges(centers):
    edges = np.zeros(len(centers) + 1)
    edges[1:-1] = (centers[1:] + centers[:-1]) / 2
    edges[0] = centers[0] - (centers[1] - centers[0])/2
    edges[-1] = centers[-1] + (centers[-1] - centers[-2])/2
    return edges

phi_centers = heatmap_data.columns.astype(float).values
alpha_centers = heatmap_data.index.astype(float).values

phi_edges = get_edges(phi_centers)
alpha_edges = get_edges(alpha_centers)

# Create the heatmap with pcolormesh using computed edges
im = heatmap_ax.pcolormesh(
    phi_edges,
    alpha_edges,
    heatmap_data.values,
    cmap="coolwarm_r", alpha = 0.7,
    norm=LogNorm(vmin=color_min, vmax=color_max),
    shading='flat'
)

# Add colorbar and adjust limits to include all edges
heatmap_ax.set_xlim(phi_edges[0], phi_edges[-1])
heatmap_ax.set_ylim(alpha_edges[0], alpha_edges[-1])

# Add colorbar
cbar = plt.colorbar(im, ax=heatmap_ax, orientation="vertical", fraction=0.046, pad=0.01)
cbar.set_label(r"$\sigma_{Y}$", fontsize=fontsize, labelpad = -15)
# Set colorbar ticks inward
cbar.ax.tick_params(direction='in', which='both', labelsize=labelsize)


# Add labels and title to heatmap
heatmap_ax.set_ylabel(r"$\alpha$", fontsize=fontsize)
heatmap_ax.set_xlabel(r"$\phi$", fontsize=fontsize, labelpad=-2)
heatmap_ax.tick_params(labelsize=labelsize, direction='in', which='both', top = True, right = True)
heatmap_ax.set_xlim(0.595, 0.725)
heatmap_ax.set_ylim(0.0, 0.5)
heatmap_ax.text(0.62, 0.25, r'$\mathbf{Fluid}$', fontsize=fontsize, fontweight='normal', va='top')
heatmap_ax.text(0.68, 0.25, r'$\mathbf{Glass}$', fontsize=fontsize, fontweight='normal', va='top')
#heatmap_ax.text(0.68, 0.25, r'$\mathbf{Jamming}$', fontsize=fontsize, fontweight='normal', va='top')

# Add label (g)
heatmap_ax.text(0.02, 0.98, '(g)', transform=heatmap_ax.transAxes, fontsize=fontsize, 
                ha='left', va='top', fontweight='bold')

# Add minor ticks to heatmap axes (linear scale)
heatmap_ax.xaxis.set_minor_locator(AutoMinorLocator(2))
heatmap_ax.yaxis.set_minor_locator(AutoMinorLocator(2))

# Overlay the line on the heatmap
x1 = np.linspace(0.61, 0.68, 1000)
phi0 = 0.61
A = 0.0643
B = 0.1621
y1 = ((x1-phi0)/A)**(1/B)
heatmap_ax.plot(x1, y1, color='black', linewidth=2.5, linestyle='-', label=r'$\phi=\phi_{0}+a_1\alpha^{b_1}$')




heatmap_ax.scatter(
    0.61, 0.0,
    marker='h',
    s=75,            # adjust size to taste
    color='black',
    clip_on=False,    # ← allow it to draw outside the axes patch
    zorder=5
)

heatmap_ax.text(
    0.61 - 0.0035,  # small shift in x (data units)
    0.0   + 0.01,  # small shift in y
    r"$\phi_{0}$",
    ha="left",
    va="bottom",
    fontsize=fontsize,
    color="black",
    zorder=6,
    clip_on=False
)


heatmap_ax.scatter(
    0.648, 0.0,
    marker='o',
    s=75,            # adjust size to taste
    color='black',
    clip_on=False,    # ← allow it to draw outside the axes patch
    zorder=5
)

heatmap_ax.text(
    0.648 + 0.0015,  # small shift in x (data units)
    0.0   + 0.01,  # small shift in y
    r"$\phi_{J}$",
    ha="left",
    va="bottom",
    fontsize=fontsize,
    color="black",
    zorder=6,
    clip_on=False
)



'''
heatmap_ax.scatter(
    0.66, 0.22,
    marker='H',
    s=75,            # adjust size to taste
    color='darkred',
    clip_on=False,    # ← allow it to draw outside the axes patch
    zorder=5
)
'''

'''

# — load your jamming‑line data —
crit_df = pd.read_csv('critical_alpha_phi_jamming.csv')

# plot critical points as black circles
heatmap_ax.scatter(
    crit_df['phi'],
    crit_df['alpha'],
    c='grey',
    marker='o',
    s=50,
    clip_on=False, 
    zorder=5
)


# vertical dashed grey line at Pe=3 from α=0 to 0.25
heatmap_ax.plot(
    crit_df['phi'],
    crit_df['alpha'],
    color='gray',
    linestyle='--',
    linewidth=2,
    clip_on=False, 
    zorder=5
)

# ─── load & plot local‐extrema lines ───
ext_df = pd.read_csv("local_extrema_shear_rate_0.csv")

heatmap_ax.plot(
    ext_df["phi_max"],
    ext_df["alpha"],
    linestyle='--',            # dashed line only
    color='k',                 # match your other lines
    linewidth=2,               # line thickness
    clip_on=False,             # allow drawing outside axes
    zorder=5,
    label=r'$S(q)_{\rm peak}^{\max}(\dot\gamma=0)$'
)

'''

# ─── load & plot additional dashed‐line data ───
contours = pd.read_csv("contour_lines_sr6.csv")

# ─── skewness contour (level=0.5) as dash‑dot ───
skew_df = contours[contours['metric'] == 'skewness']
heatmap_ax.plot(
    skew_df['phi'],
    skew_df['alpha'],
    linestyle='-.',       # dash‑dot
    color='darkblue',
    linewidth=2.0,
    label='$\mathcal{S}_\sigma(\dot{\gamma}=10^{-6})$'
)

# ─── kurtosis contour (level=0.5) as dotted ───
kurt_df = contours[contours['metric'] == 'kurtosis']
heatmap_ax.plot(
    kurt_df['phi'],
    kurt_df['alpha'],
    linestyle=':',        # dotted
    color='darkred',
    linewidth=2.0,
    label='$\mathcal{K}_\sigma (\dot{\gamma}=10^{-6})$'
)





# if you have a legend:
heatmap_ax.legend(loc="upper right", fontsize=labelsize-2, frameon=False)




# Adjust figure margins (modify these values as needed)
plt.subplots_adjust(
    left=0.10,   # Left margin
    right=0.94,  # Right margin
    bottom=0.1,  # Bottom margin
    top=0.98,    # Top margin
)





# Save and show the figure
plt.savefig("fig2efg.png", dpi=600)
plt.show()

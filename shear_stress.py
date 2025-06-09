import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Set Parameters
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
fontsize = 20

# Define the Herschel-Bulkley model
def herschel_bulkley_model(shear_rate, sigma_Y, k, n):
    """Herschel-Bulkley model function."""
    return sigma_Y + k * shear_rate**n

# Define saturation check
def check_saturation(shear_rates, stresses, threshold = 3.0):
    """
    Check for saturation of stress at small shear rates.
    """
    sorted_indices = np.argsort(shear_rates)
    shear_rates = np.array(shear_rates)[sorted_indices]
    stresses = np.array(stresses)[sorted_indices]

    # Focus on the smallest shear rates
    low_shear_stresses = stresses[:5]  # Take the first 5 (smallest shear rates)
    relative_changes = np.abs(np.diff(low_shear_stresses) / low_shear_stresses[:-1])

    # Check if relative changes are below threshold
    return np.all(relative_changes < threshold)

# Function to load and filter data for specified alpha values
def load_and_filter_data(data_dir, alpha_values):
    filtered_data = {alpha: {} for alpha in alpha_values}
    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            try:
                # Extract phi and alpha from filename
                phi = float(filename.split("phi_")[1].split("_")[0])
                alpha = float(filename.split("alpha_")[1].replace(".csv", ""))
                
                if alpha in alpha_values:
                    # Load data
                    file_path = os.path.join(data_dir, filename)
                    data = pd.read_csv(file_path)
                    filtered_data[alpha][phi] = data
            except (IndexError, ValueError):
                print(f"Error: Could not extract phi and alpha from filename: {filename}")
                continue
    return filtered_data

# Directory containing data files
data_dir = "analysis/shear_data"

# Load and filter data for alpha = 0 and alpha = 0.05 in subplot 1
alpha_values1 = [0.0, 0.05]
filtered_data1 = load_and_filter_data(data_dir, alpha_values1)

# Load and filter data for alpha = 0.30 and alpha = 0.50 in subplot 2
alpha_values2 = [0.35, 0.50]
filtered_data2 = load_and_filter_data(data_dir, alpha_values2)

# Define markers and color
marker_styles = ['o', 's', '^', 'D', 'v', '<', '>', 'P', '*', 'h', 'H', 'X', 'd', '|', '_']
colors = plt.cm.tab10.colors  # Use a colormap for consistent colors

# Create a figure with two subplots
fig = plt.figure(figsize=(8,6))
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax2 = plt.subplot2grid((2, 2), (0, 1))
ax3 = plt.subplot2grid((2, 2), (1, 0))
ax4 = plt.subplot2grid((2, 2), (1, 1))
left_margin = 0.105
right_margin = 0.985
bottom_margin = 0.10
top_margin = 0.94
wspace = 0.0 #25
hspace = 0.0
fig.subplots_adjust(left=left_margin, right=right_margin, bottom=bottom_margin, top=top_margin, wspace=wspace, hspace=hspace)

point_size = 50
labelsize = 14

# Function to plot data in a subplot
def plot_data(ax, filtered_data, title, alpha_values):
    ax.tick_params(labelsize=labelsize)
    ax.plot([], [], ' ', label=r'$\phi$')

    for alpha, data_dict in filtered_data.items():
        # Sort phi values to ensure sequential order
        sorted_data = dict(sorted(data_dict.items()))

        for idx, (phi, data) in enumerate(sorted_data.items()):
            shear_rates = data["Shear Rate"]
            stresses = data["Shear Stress"]

            # Assign marker and color
            marker = marker_styles[idx % len(marker_styles)]
            color = colors[idx % len(colors)]

            # Open markers for specific alpha values
            face_color = color if alpha == alpha_values[0] else 'none'  # Filled for first alpha, open for others

            # Plot data points
            if alpha == alpha_values[0]:  # Only label points for first alpha value
                label_points = fr"${phi:.2f}$"
            else:
                label_points = None  # No label for other alpha values

            ax.scatter(
                shear_rates,
                stresses,
                label=label_points,
                alpha=0.9,
                marker=marker,
                edgecolor=color,
                facecolor=face_color,
                linewidths=1.0,  # Enhance edge line for visibility
                s=point_size
            )

            # Check for saturation and fit the data
            if check_saturation(shear_rates, stresses):
                try:
                    # Fit the Herschel-Bulkley model
                    popt, _ = curve_fit(
                        herschel_bulkley_model, 
                        shear_rates, 
                        stresses, 
                        p0=[0.1, 1.0, 0.5],
                        bounds=([0, 0, 0], [np.inf, np.inf, 1])
                    )
                    sigma_Y, k, n = popt

                    # Generate fitted curve
                    shear_rate_fit = np.logspace(np.log10(min(shear_rates)), np.log10(max(shear_rates)), 100)
                    stress_fit = herschel_bulkley_model(shear_rate_fit, sigma_Y, k, n)

                    # Plot the fitted line
                    linestyle = '-' if alpha == alpha_values[0] else '--'  # Solid for first alpha, dashed for others
                    ax.plot(
                        shear_rate_fit,
                        stress_fit,
                        linestyle=linestyle,
                        color=color
                    )
                    print(f"alpha = {alpha}, phi = {phi:.2f}: sigma_Y = {sigma_Y:.4f}, k = {k:.4f}, n = {n:.4f}")

                except RuntimeError:
                    print(f"Fit failed for alpha = {alpha}, phi = {phi:.2f}.")

    ax.set_xlabel(r"$\dot{\gamma}$", fontsize=fontsize+2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.tick_params(which='major', direction='in', bottom=True, top=True, left=True, right=True)
    ax.tick_params(which='minor', direction='in', bottom=True, top=True, left=True, right=True)
    ax1.legend(loc='lower right', ncol=3, fontsize=fontsize-6, markerfirst=False, 
               labelspacing=0.05, 
               handletextpad=-0.1, 
               columnspacing=0.15, 
               frameon=False)
    ax.set_title(title, fontsize=fontsize-2)
    ax.grid(False)


# Plot data in subplot 1
ax1.set_ylim([5e-8, 1e-2])
ax1.set_ylabel(r"$\langle\sigma_{xy}\rangle$", fontsize=fontsize+2)
plot_data(ax1, filtered_data1, r"$\mathrm{Symbols}:~\alpha=0.0 (\mathrm{solid}), 0.05 (\mathrm{open})$", alpha_values1)
ax1.text(0.05, 0.92, "(a)", transform=ax1.transAxes, fontsize=fontsize, fontweight='bold')

# Plot data in subplot 2
ax2.set_ylim([5e-8, 1e-2])
ax2.tick_params(labelleft=False)
plot_data(ax2, filtered_data2, r"$0.35 (\mathrm{solid}), 0.50 (\mathrm{open})$", alpha_values2)
ax2.text(0.05, 0.92, "(b)", transform=ax2.transAxes, fontsize=fontsize, fontweight='bold')


# Function to plot viscosity and fitted lines in a subplot
def plot_viscosity(ax, filtered_data, title, alpha_values):
    ax.tick_params(labelsize=labelsize)
    ax.plot([], [], ' ', label=r'$\phi$')

    for alpha, data_dict in filtered_data.items():
        sorted_data = dict(sorted(data_dict.items()))

        for idx, (phi, data) in enumerate(sorted_data.items()):
            shear_rates = data["Shear Rate"]
            stresses = data["Shear Stress"]
            viscosity = stresses / shear_rates  # Calculate viscosity

            # Assign marker and color
            marker = marker_styles[idx % len(marker_styles)]
            color = colors[idx % len(colors)]

            # Open markers for specific alpha values
            face_color = color if alpha == alpha_values[0] else 'none'

            # Plot data points
            if alpha == alpha_values[0]:
                label_points = fr"${phi:.2f}$"
            else:
                label_points = None

            ax.scatter(
                shear_rates,
                viscosity,
                label=label_points,
                alpha=0.9,
                marker=marker,
                edgecolor=color,
                facecolor=face_color,
                linewidths=1.0,
                s=point_size
            )

            # Fit the Herschel-Bulkley model if saturation check passes
            threshold_value = 1.99
            if check_saturation(shear_rates, stresses):
                try:
                    # Fit the Herschel-Bulkley model
                    popt, _ = curve_fit(
                        herschel_bulkley_model, 
                        shear_rates, 
                        stresses, 
                        p0=[0.1, 1.0, 0.5],
                        bounds=([0, 0, 0], [np.inf, np.inf, 1])
                    )
                    sigma_Y, k, n = popt

                    # Generate fitted viscosity curve
                    shear_rate_fit = np.logspace(np.log10(min(shear_rates)), np.log10(max(shear_rates)), 100)
                    stress_fit = herschel_bulkley_model(shear_rate_fit, sigma_Y, k, n)
                    viscosity_fit = stress_fit / shear_rate_fit  # Calculate fitted viscosity

                    # Plot the fitted line
                    linestyle = '-' if alpha == alpha_values[0] else '--'  # Solid for first alpha, dashed for others
                    ax.plot(
                        shear_rate_fit,
                        viscosity_fit,
                        linestyle=linestyle,
                        color=color
                    )
                    print(f"alpha = {alpha}, phi = {phi:.2f}: sigma_Y = {sigma_Y:.4f}, k = {k:.4f}, n = {n:.4f}")

                except RuntimeError:
                    print(f"Fit failed for alpha = {alpha}, phi = {phi:.2f}.")

    ax.set_xlabel(r"$\dot{\gamma}$", fontsize=fontsize+2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.tick_params(which='major', direction='in', bottom=True, top=True, left=True, right=True)
    ax.tick_params(which='minor', direction='in', bottom=True, top=True, left=True, right=True)
    #ax.legend(loc='lower right', ncol=2, fontsize=fontsize-2, markerfirst=False, labelspacing=0.1, handletextpad=-0.1)
    #ax.set_title(title, fontsize=fontsize-2)
    ax.grid(False)


# Plot viscosity data in subplot 3
x1 = np.linspace(0.001,0.01,1000)
y1 = 0.01/x1
ax3.plot(x1, y1, color='black', linewidth=2.0, linestyle='--')
ax3.text(0.004, 10, r'$\dot{\gamma}^{-1}$', fontsize=fontsize, fontweight='normal', va='top')

ax3.set_ylim([1e-2, 5e3])
ax3.set_ylabel(r"$\eta = \langle\sigma_{xy}\rangle / \dot{\gamma}$", fontsize=fontsize+2)
plot_viscosity(ax3, filtered_data1, r"$\mathrm{Symbols:~} \alpha=0.35 (\mathrm{solid}), 0.50 (\mathrm{open})$", alpha_values1)
ax3.text(0.90, 0.90, "(c)", transform=ax3.transAxes, fontsize=fontsize, fontweight='bold')

# Plot viscosity data in subplot 4
x1 = np.linspace(0.001,0.01,1000)
y1 = 0.01/x1
ax4.plot(x1, y1, color='black', linewidth=2.0, linestyle='--')
ax4.text(0.004, 10, r'$\dot{\gamma}^{-1}$', fontsize=fontsize, fontweight='normal', va='top')

ax4.set_ylim([1e-2, 5e3])
ax4.tick_params(labelleft=False)
plot_viscosity(ax4, filtered_data2, r"$\mathrm{Symbols:~} \alpha=0.35 (\mathrm{solid}), 0.50 (\mathrm{open})$", alpha_values2)
ax4.text(0.90, 0.90, "(d)", transform=ax4.transAxes, fontsize=fontsize, fontweight='bold')

plt.show()
fig.savefig('shear_stress_viscosity_phi.pdf', dpi=600)
fig.savefig('shear_stress_viscosity_phi.png', dpi=600)

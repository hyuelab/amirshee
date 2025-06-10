#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import LogLocator, LogFormatterSciNotation, NullFormatter


# ---------------------------
# Plot settings
# ---------------------------
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
fontsize   = 20
labelsize  = 14
point_size = 50

# ---------------------------
# Load data
# ---------------------------
csv_path = 'figures/fit_parameters.csv'
df = pd.read_csv(csv_path)

gamma    = df['gamma'].values
sigma0   = df['sigma0'].values
eta0     = df['eta0'].values
alpha_c  = df['alpha_c'].values
n_param  = df['n'].values  # this is your “m”

# ---------------------------
# Generic offset–power‑law model
# ---------------------------
def offset_power_law(x, y0, k, p):
    return y0 + k * x**p

# common initial guess / bounds
bounds = ([0, 0, 0], [np.inf, np.inf, np.inf])

# ---------------------------
# 1) Fit σ₀ vs γ (c) & derive η (d)
# ---------------------------
mask_sig = np.isfinite(gamma) & np.isfinite(sigma0)
g_sig, s0_sig = gamma[mask_sig], sigma0[mask_sig]
p0_sig = [s0_sig.min(), s0_sig.max() - s0_sig.min(), 0.5]
popt_sig, _ = curve_fit(offset_power_law, g_sig, s0_sig,
                        p0=p0_sig, bounds=bounds)
g_fit   = np.logspace(np.log10(g_sig.min()), np.log10(g_sig.max()), 200)
s0_fit  = offset_power_law(g_fit, *popt_sig)
eta_fit = s0_fit / g_fit

# ---------------------------
# 2) Fit α_c vs γ (e)
# ---------------------------
mask_alpha = np.isfinite(gamma) & np.isfinite(alpha_c) & (gamma <= 1e-3)
g_alpha, ac_alpha = gamma[mask_alpha], alpha_c[mask_alpha]
p0_alpha = [ac_alpha.min(), ac_alpha.max() - ac_alpha.min(), 0.5]
popt_alpha, _ = curve_fit(offset_power_law, g_alpha, ac_alpha,
                          p0=p0_alpha, bounds=bounds)
g_fit_alpha = np.logspace(np.log10(g_alpha.min()), np.log10(g_alpha.max()), 200)
ac_fit      = offset_power_law(g_fit_alpha, *popt_alpha)

sat_val = popt_alpha[0]

# ---------------------------
# 3) Fit m/γ̇ vs γ̇ (f) & reconstruct m
# ---------------------------
mask_m = np.isfinite(gamma) & np.isfinite(n_param)
g_m, m_m = gamma[mask_m], n_param[mask_m]

# compute y = m/γ̇
y_m = m_m / g_m
p0_m = [y_m.min(), y_m.max() - y_m.min(), 0.5]
popt_m, _ = curve_fit(offset_power_law, g_m, y_m,
                      p0=p0_m, bounds=bounds)


# ---------------------------
# 4) Plot all panels
# ---------------------------
fig, axes = plt.subplots(1, 3, figsize=(8, 2.5))
ax1, ax2, ax3 = axes.flatten()
fig.subplots_adjust(left=0.06, right=0.98, top=0.95,
                    bottom=0.12, wspace=0.20, hspace=0.0)

for ax in axes.flatten():
    ax.tick_params(direction='in', which='both',
                   top=True, right=True, labelsize=labelsize)

# (c) σ₀
ax1.scatter(g_sig, s0_sig, s=point_size, c='C1', marker='o')
ax1.plot(g_fit, s0_fit, '--', lw=2, color='k')
ax1.set_xscale('log'); ax1.set_yscale('log')
ax1.set_xlabel(r'$\dot\gamma$', fontsize=fontsize, labelpad=-40)
ax1.set_ylabel(r'$\sigma_0$', fontsize=fontsize, labelpad = -50)
ax1.set_ylim(0.0001, 0.01)
ax1.text(0.10, 0.95, '(c)', transform=ax1.transAxes,
         fontsize=fontsize, fontweight='bold', va='top')
ax1.text(0.05, 0.18, r'$\sigma_{0p}$', transform=ax1.transAxes, fontsize=fontsize, rotation = 0)


# (d) α_c
ax2.scatter(g_alpha, ac_alpha, s=point_size, c='C2', marker='^')
ax2.plot(g_fit_alpha, ac_fit, '--', lw=2, color='k')
ax2.set_xscale('log'); ax2.set_yscale('log')
ax2.set_xlim(8e-7, 1.5e-3); ax2.set_ylim(10, 1000)
ax2.set_xlabel(r'$\dot\gamma$', fontsize=fontsize, labelpad=-40)
ax2.set_ylabel(r'$(\alpha\mathrm{Pe}^2)_c$', fontsize=fontsize, labelpad = -50)
ax2.text(0.10, 0.95, '(d)', transform=ax2.transAxes,
         fontsize=fontsize, fontweight='bold', va='top')
ax2.text(-0.10, 0.10, r'$G$', transform=ax2.transAxes, fontsize=fontsize, rotation = 0)

# (e) m
ax3.scatter(g_m, m_m, s=point_size, c='C3', marker='d')
ax3.set_xscale('log')
ax3.set_xlim(8e-7, 1.5e-3)
ax3.set_ylim(0.9, np.max(m_m)*1.1)
ax3.set_xlabel(r'$\dot\gamma$', fontsize=fontsize, labelpad=-40)
ax3.set_ylabel(r'$m$', fontsize=fontsize, labelpad = -40)
ax3.text(0.10, 0.95, '(e)', transform=ax3.transAxes,
         fontsize=fontsize, fontweight='bold', va='top')

for ax in axes.flatten():
    ax.set_xscale('log')

    # --- force every decade for majors ---
    ax.xaxis.set_major_locator(LogLocator(base=10.0,
                                          subs=(1.0,),
                                          numticks=10))
    ax.xaxis.set_major_formatter(LogFormatterSciNotation())
    ax.tick_params(which='major', length=4)

    # --- minor ticks 2–9× each decade ---
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(LogLocator(base=10.0,
                                          subs=np.arange(2, 10) * 0.1,
                                          numticks=12))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(which='minor', length=2)



# save & show
fig.savefig('fig4cde.png', dpi=600)
plt.show()

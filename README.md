<p align="center">
  <img 
    src="https://img.shields.io/badge/Tuning_Shear_Rheology_through_Active_Dopants-lightblue?style=for-the-badge" 
    alt="Tuning Shear Rheology through Active Dopants" />
  <br/>
  by
  <br/>
  <strong> Amir Shee, Ritwik Bandyopadhyay, and Haicen Yue </strong>
</p>



<p>&nbsp;</p>
<p>&nbsp;</p>



<div style="text-align: center;">
  <img
    src="https://img.shields.io/badge/Main_Article-lightgreen?style=for-the-badge"
    alt="Main Article"
</div>

### `fig1.png`

A 2D x-y view of our 3D simulation cell containing mixture of passive (C, D) and active (A, B) Brownian particles under simple shear velocity profile.  


### `fig2abcd.py`

This Python script reads shear‐flow data from `shear_data_alpha_phi/` (CSV files named `phi_<φ>_alpha_<α>.csv`), fits the Herschel–Bulkley model, and produces `fig2abcd.png` showing stress and viscosity curves:

- **Panel (a):**  
  Average shear stress ⟨σₓᵧ⟩ vs. shear rate \(\dot\gamma\) for α = 0.00 (solid markers) and α = 0.05 (open markers) across φ values. Dashed lines indicate yield‐stress saturation.  

- **Panel (b):**  
  Same as (a) but for α = 0.35 (solid) and α = 0.50 (open).  

- **Panel (c):**  
  Viscosity η = ⟨σₓᵧ⟩/ \(\dot\gamma\) vs. \(\dot\gamma\) for α = 0.00 and 0.05, with a \(\dot\gamma^{-1}\) reference (dashed line).  

- **Panel (d):**  
  Viscosity curves for α = 0.35 and 0.50, with the same reference line.




### `fig2efg.py`

This script reads `yield_stress.csv` and produces:

1. **Panel (e):** Yield stress \(\sigma_Y\) vs.\ packing fraction \(\phi\) for fixed dopant fractions \(\alpha = [0.00,0.05,0.30,0.50]\).
2. **Panel (f):** Yield stress \(\sigma_Y\) vs.\ dopant fraction \(\alpha\) for fixed \(\phi = [0.65,0.66,0.67,0.68]\).  
3. **Panel (g):** Heatmap of \(\sigma_Y(\phi,\alpha)\) saved as `fig2efg.png`.

### `fig3.py`

This script reads `yield_data_alpha_Pe.csv`, computes mean yield stress \(\sigma_Y\) for each \((\alpha,\mathrm{Pe})\), and generates `fig3.png` with:

1. **Panel (a):**  
   \(\sigma_Y\) vs Péclet number (Pe) at fixed dopant fractions \(\alpha = \{0.00,\,0.15,\,0.40,\,0.50\}\). Markers denote data points above the noise floor (\(10^{-6}\)); dashed vertical guides indicate where yield stress falls to baseline.  

2. **Panel (b):**  
   \(\sigma_Y\) vs dopant fraction \(\alpha\) at fixed Pe = \(\{0,\,4,\,8,\,12\}\), with analogous markers and guides.  

3. **Panel (c):**  
   Heatmap of \(\sigma_Y(\mathrm{Pe},\alpha)\) with the glass–fluid boundary \(\alpha\,\mathrm{Pe}^2=\text{const}\), and skewness/kurtosis contours from `skewnes_kurtosis_alpha_Pe.csv`.




### `fig4ab.py`

This Python script reads all nonzero-α CSV files from `data_alpha_Pe/`, computes the composite “active-energy” parameter \(\alpha\,\mathrm{Pe}^2\), and plots at fixed shear rate \(\dot\gamma=10^{-6}\):

- **Panel (a):**  
  Mean shear stress \(\langle\sigma_{xy}\rangle\) vs.\ \(\alpha\,\mathrm{Pe}^2\). Data points are colored by Pe and marked by different α.

- **Panel (b):**  
  Viscosity \(\eta = \langle\sigma_{xy}\rangle/\dot\gamma\) vs.\ \(\alpha\,\mathrm{Pe}^2\) at the same fixed \(\dot\gamma\).




### `fig4cde.py`

This Python script reads fitted model parameters from `fit_parameters.csv` and produces `fig4cde.png`:

1. **Panel (c):**  
   Offset–power-law fit of \(\sigma_0\) vs.\ shear‐rate \(\dot\gamma\). Data points (marker ‘o’, color C1) are plotted on log–log axes with a dashed black fit curve.

2. **Panel (d):**  
   Critical active-energy \((\alpha\,\mathrm{Pe}^2)_c\) vs.\ \(\dot\gamma\). Data points (marker ‘^’, color C2) and dashed fit curve are shown on log–log axes, with the glass boundary \(G\) annotated.

3. **Panel (e):**  
   Flow‐exponent parameter \(m\) vs.\ \(\dot\gamma\). Data points (marker ‘d’, color C3) are plotted on log–log axes.



<p>&nbsp;</p>
<p>&nbsp;</p>


<div style="text-align: center;">
  <img 
    src="https://img.shields.io/badge/Supplemental_Material-lightgreen?style=for-the-badge" 
    alt="Supplemental Material" />
</div>



### `SM_fig1.py`

Generates and saves **SM_fig1.png**, comparing harmonic and Morse‐shifted interaction curves for three values of the Morse “stiffness” parameter (α = 0.5, 0.1, 0.01).


### `SM_fig2.py`

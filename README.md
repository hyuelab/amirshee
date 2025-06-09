<p align="center">
  <img 
    src="https://img.shields.io/badge/Tuning_Shear_Rheology_through_Active_Dopants-lightblue?style=for-the-badge" 
    alt="Tuning Shear Rheology through Active Dopants" />
  <br/>
  by
  <br/>
  <strong> Amir Shee, Ritwik Bandyopadhyay, and Haicen Yue </strong>
</p>







<div style="text-align: center;">
  <img
    src="https://img.shields.io/badge/Main_Article-lightgreen?style=for-the-badge"
    alt="Main Article"
</div>

### `fig1.png`

A 2D x-y view of our 3D simulation cell containing mixture of passive (C, D) and active (A, B) Brownian particles under simple shear velocity profile.  


### `fig2abcd.py`

This Python script reads shear‐flow data from `shear_data/` (CSV files named `phi_<φ>_alpha_<α>.csv`), fits the Herschel–Bulkley model, and produces a 2×2 panel figure (`fig2abcd.png`) showing stress and viscosity curves:

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





<div style="text-align: center;">
  <img 
    src="https://img.shields.io/badge/Supplemental_Material-lightgreen?style=for-the-badge" 
    alt="Supplemental Material" />
</div>



### `SM_fig1.py`

Generates and saves **SM_fig1.png**, comparing harmonic and Morse‐shifted interaction curves for three values of the Morse “stiffness” parameter (α = 0.5, 0.1, 0.01).


### `SM_fig2.py`

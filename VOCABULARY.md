# Pulse Sequence Vocabulary

Controlled vocabulary for `experiment_type` and `features` fields.

`experiment_type` values are enforced by the schema enum (v0.0.3). `features` is open — use existing terms where possible and propose new ones via PR if widely applicable.

## Experiment Types (enum)

### Dimensionality
- `1d`, `2d`, `3d` - Number of frequency dimensions in processed spectrum (not total dataset dimensions)

### Homonuclear
- `cosy`, `tocsy`, `noesy` - Standard 2D homonuclear experiments

### Heteronuclear
- `hsqc` - Heteronuclear single quantum coherence
- `hmqc` - Heteronuclear multiple quantum coherence
- `trosy` - Transverse relaxation optimized spectroscopy

### Core Experiments
- `relaxation` - R1, R2, NOE measurements
- `r1rho` - R1ρ relaxation dispersion
- `cest` - Chemical exchange saturation transfer
- `diffusion` - Diffusion/DOSY
- `calibration` - Pulse / power calibration experiments
- `solid_state` - Solid-state NMR experiments




## Features

### Relaxation
- `R1`, `R2`, `hetnoe`, `cpmg`, `hahn_echo`, `perfect_echo`, `inversion_recovery`, `relaxation_dispersion`, `temperature_compensation`, `broadband`

### Spinlock
- `on_resonance`, `off_resonance`

### Gradients
- `gradient_enhanced`, `sensitivity_enhanced`, `bipolar_gradients`

### Diffusion
- `ste`, `xste`, `led`

### Excitation
- `selective_excitation`, `sofast`, `alsofast`

### Calibration
- `nutation`, `condenz`

### Detection / processing
- `states_tppi`

### Water Suppression
- `presaturation`, `water_suppression`, `watergate`

### Detection
- `phase_sensitive`, `magnitude_mode`

### Other
- `noesy_hsqc`, `hsqc_noesy`, `tocsy_hsqc`, `hsqc_tocsy`, `hmqc_noesy_hmqc` - Composite experiment orderings

## Guidelines

- Use established literature names for `experiment_type`
- Add new `experiment_type` terms only when several sequences need them
- Use `features` for technical variations and implementation details
- Always use snake_case
- When uncertain, use `description` field instead of inventing new terms
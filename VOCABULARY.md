# Pulse Sequence Vocabulary

Controlled vocabulary for `experiment_type` and `features` fields.

## Experiment Types

### Dimensionality
- `1d`, `2d`, `3d`, `4d` - Number of frequency dimensions in processed spectrum (not total dataset dimensions)

### Homonuclear
- `cosy`, `tocsy`, `noesy` - Standard 2D homonuclear experiments

### Heteronuclear
- `hsqc` - Heteronuclear single quantum coherence
- `hmqc` - Heteronuclear multiple quantum coherence
- `trosy` - Transverse relaxation optimized spectroscopy

### Triple Resonance
- `hnco`, `hncaco`, `hnca`, `hncoca`, `hncacb`, `hncocacb` - Standard backbone experiments

### Core Experiments
- `relaxation` - R1, R2, NOE measurements
- `r1rho` - R1ρ relaxation dispersion
- `relaxation_dispersion` - (implicitly CPMG-based) relaxation dispersion
- `cest` - Chemical exchange saturation transfer
- `std` - Saturation transfer difference
- `waterlogsy` - Water-ligand observed via gradient spectroscopy
- `diffusion` - Diffusion/DOSY




## Features

### Relaxation
- `R1`, `R2`, `hetnoe`, `cpmg`, `hahn_echo`, `perfect_echo`, `inversion_recovery`

### Spinlock
- `on_resonance`, `off_resonance`

### Gradients
- `gradient_enhanced`, `sensitivity_enhanced`, `bipolar_gradients`

### Diffusion
- `ste`, `xste`, `led`

### Excitation
- `selective_excitation`, `sofast`, `alsofast`

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
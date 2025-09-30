# Schema Field Reference

Complete reference for all metadata fields in pulse sequence annotations.

## Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `schema_version` | string | Schema version | `"0.0.1"` |
| `sequence_version` | string | Sequence version (semantic) | `"1.2.0"` |
| `title` | string | Descriptive sequence name | `"SOFAST-HMQC"` |
| `authors` | array | List of contributors | `["Name <email>"]` |
| `created` | string | Creation date (YYYY-MM-DD) | `"2024-01-15"` |
| `last_modified` | string | Last modification date | `"2024-08-17"` |
| `repository` | string | Repository identifier | `"github.com/user/repo"` |
| `status` | string | Development status | `"stable"` |

## Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `experiment_type` | array | Experiment keywords | `["hsqc", "2d"]` |
| `description` | string | Detailed description | `"1H,15N SOFAST-HMQC..."` |
| `features` | array | Technical features | `["trosy", "sofast"]` |
| `nuclei_hint` | array | Suggested mapping of nuclei to channels | `["1H", "15N"]` |
| `citation` | array | Literature references | `["Author et al., Journal (Year)"]` |
| `doi` | array | DOI identifiers | `["10.1021/ja051306e"]` |

## Controlled Vocabularies

### Status Values
- `experimental`: Under development, use with caution
- `beta`: Testing phase, mostly stable  
- `stable`: Production ready, well tested
- `deprecated`: No longer recommended

### Nuclei Format
Use standard isotope notation: `1H`, `13C`, `15N`, `31P`, `19F`, etc.

### Common Experiment Types
- `1d`, `2d`, `3d`
- `cosy`, `tocsy`, `noesy`
- `hsqc`, `hmqc`, `trosy`
- `relaxation`
- `diffusion`
- `r1rho`, `cest`

### Common Experiment Features
- `watergate`
- `hahn echo`, `perfect echo` (relaxation)
- `ste`, `xste` (diffusion)
- `relaxation dispersion`
- `temperature compensation`
- `on-resonance` (r1rho)

## Details by Experiment Type / Feature

### Relaxation

Experiments with type `relaxation` should include an object `relaxation` with fields describing the following additional parameters:
- `type`: `R1`, `R2`
- `model`: `exponential-decay`, `inversion-recovery`, `saturation-recovery`
- `channel`: corresponding to observed nucleus
- `duration`: relaxation time

For example:

```
;@ experiment_type: [relaxation, 1d]
;@ relaxation: {type: R1, model: inversion-recovery, channel: f1, duration: <$VDLIST>}
```


### `cest`, `r1rho`

Experiments with type `cest` or `r1rho` should include an object `spinlock` with fields describing the spinlock parameters:
- `channel`: corresponding to observed nucleus
- `power`
- `duration`
- `offset`
- `alignment` (optional): `hard pulse`

For example:

```
;@ experiment_type: [r1rho, 1d]
;@ spinlock: {channel: f1, power: <$VALIST>, duration: <$VPLIST>, offset: 0, alignment: hard pulse}
```


### `diffusion`

Experiments with type `diffusion` should include an object `diffusion` with fields describing the following parameters:

- `type`: bipolar
- `coherence`: specifying the order of the encoding coherence `[channel, coherence_order]`
- `big-delta`: diffusion delay
- `little-delta`: total encoding pulse length
- `tau`: delay between bipolar gradients
- `Gmax`: maximum gradient strength
- `g`: reference to diff ramp file, or specify a calculated ramp (`[linear, cnst1, cnst2]`)
- `shape`: encoding gradient pulse name

For example:

```
;@ experiment_type: [diffusion, 1d]
;@ diffusion:
;@ - type: bipolar
;@ - coherence: [f1, 1]
;@ - big-delta: d20
;@ - little-delta: p31
;@ - tau: d17
;@ - Gmax: gpz6
;@ - g: [linear, cnst1, cnst2]
;@ - shape: gpnam6
```
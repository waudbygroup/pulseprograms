# Schema Field Reference

Complete reference for all metadata fields in pulse sequence annotations. Current schema: **v0.0.3** ([`schemas/current`](https://github.com/waudbylab/pulseprograms/blob/main/schemas/current)).

## Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `schema_version` | string | Schema version | `"0.0.3"` |
| `sequence_version` | string | Sequence version (semantic, `X.Y.Z`) | `"1.2.0"` |
| `title` | string | Descriptive sequence name | `"SOFAST-HMQC"` |
| `authors` | array | List of contributors | `["Name <email>"]` |
| `created` | string | Creation date (YYYY-MM-DD) | `"2024-01-15"` |
| `last_modified` | string | Last modification date | `"2026-04-30"` |
| `repository` | string | Repository identifier | `"github.com/user/repo"` |
| `status` | string | Development status | `"stable"` |
| `experiment_type` | array | Experiment keywords (controlled enum) | `[hmqc, 2d]` |

## Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `description` | string | Detailed description (multi-line YAML literal allowed) | `"1H,15N SOFAST-HMQC..."` |
| `features` | array | Technical features (open vocabulary — see VOCABULARY.md) | `[sofast, states_tppi]` |
| `typical_nuclei` | array | Typical nuclei, ordered by channel f1, f2, ... | `[1H, 13C, 15N]` |
| `citation` | array | Literature references | `["Author et al., Journal (Year)"]` |
| `doi` | array | DOI identifiers | `["10.1021/ja051306e"]` |
| `dimensions` | array | Indirect-dimension identifiers (dotted-path) | `[relaxation.duration, f1]` |
| `acquisition_order` | array | Loop order, innermost to outermost | `[f1, relaxation.duration]` |
| `reference_pulse` | array | Reference pulses for power calculations | `[{channel: f1, duration: p1, power: pl1}]` |

## Controlled Vocabularies

### Status Values
- `experimental`: Under development, use with caution
- `beta`: Testing phase, mostly stable
- `stable`: Production ready, well tested
- `deprecated`: No longer recommended

### Nuclei Format
Use standard isotope notation: `1H`, `13C`, `15N`, `31P`, `19F`, etc. Use `nothing` as a placeholder for unused channels.

### Experiment Types (enum)
`1d`, `2d`, `3d`, `cosy`, `tocsy`, `noesy`, `hsqc`, `hmqc`, `trosy`, `relaxation`, `r1rho`, `cest`, `diffusion`, `calibration`, `solid_state`

### Common Features
- Relaxation: `R1`, `R2`, `cpmg`, `hahn_echo`, `perfect_echo`, `inversion_recovery`, `relaxation_dispersion`, `temperature_compensation`, `broadband`
- Spinlock: `on_resonance`, `off_resonance`
- Diffusion: `ste`, `xste`, `led`
- Excitation: `selective_excitation`, `sofast`, `alsofast`
- Calibration: `nutation`, `condenz`
- Water suppression: `watergate`, `presaturation`, `water_suppression`
- Detection: `states_tppi`, `phase_sensitive`, `magnitude_mode`

## Parameter values

Several block fields (`power`, `duration`, `offset`, `gradient_strength`, ...) accept any of:

- a Bruker parameter name string (`p1`, `d20`, `cnst25`, `pl25`, `taulist`, `vplist`, `F19sat`)
- a numeric literal
- a **linear sweep**: `{type: linear, start: <param|number>, end|step: <param|number>, scale: <param|number>}` — `type` defaults to `linear`. `scale` is a multiplicative factor applied to the swept values; the dimension size is set elsewhere (TD).
- a **counter × scale** expression: `{counter: <param>, scale: <param|number>}` (e.g. CPMG `{counter: ncyc, scale: d20}`).

## Experiment-specific blocks

Each block extends a common shape (`channel`, `power`, `duration`, `offset`, `type`, `model`) with additional fields where needed.

### `relaxation`

Fields: `type` (`R1`, `R2`), `model` (`exponential-decay`, `inversion_recovery`, `saturation_recovery`), `channel`, `duration`.

```yaml
;@ experiment_type: [relaxation, 1d]
;@ relaxation: {type: R1, model: inversion_recovery, channel: f1, duration: t1delay}
```

CPMG (counter × spacing):

```yaml
;@ experiment_type: [relaxation, 1d]
;@ features: [R2, cpmg, broadband]
;@ relaxation: {type: R2, model: exponential-decay, channel: f1, duration: {counter: ncyc, scale: d20}}
```

### `r1rho`, `cest`

Fields: `channel`, `power`, `duration`, `offset`. Power, duration and offset are typically VA/VP/FQ lists referenced by name.

```yaml
;@ experiment_type: [r1rho, 1d]
;@ r1rho: {channel: f1, power: powerlist, duration: taulist, offset: 0}
```

```yaml
;@ experiment_type: [cest, 1d]
;@ cest: {channel: f1, power: pl25, duration: d18, offset: F19sat}
```

### `calibration`

Fields: `type` (e.g. `nutation`, `condenz`), `channel`, `power`, `duration`, `offset`, `model`.

```yaml
;@ experiment_type: [calibration, 1d]
;@ calibration:
;@   type: nutation
;@   channel: f1
;@   power: pl8
;@   duration: {type: linear, start: p9, step: p9}
;@   model: sine_modulated
```

### `diffusion`

Fields: `type` (`bipolar`), `coherence` (`[channel, coherence_order]`), `big_delta`, `little_delta`, `tau`, `gradient_strength`, `gradient_shape`.

```yaml
;@ experiment_type: [diffusion, 1d]
;@ diffusion:
;@   type: bipolar
;@   coherence: [f1, 1]
;@   big_delta: d20
;@   little_delta: p31
;@   tau: d17
;@   gradient_strength: {type: linear, start: cnst1, end: cnst2, scale: gpz6}
;@   gradient_shape: gpnam6
```

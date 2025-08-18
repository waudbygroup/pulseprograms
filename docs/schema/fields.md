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
| `nuclei_hint` | array | Nuclei involved | `["1H", "15N"]` |
| `citation` | array | Literature references | `["Author et al., Journal (Year)"]` |
| `doi` | array | DOI identifiers | `["10.1021/ja051306e"]` |

## Controlled Vocabularies

### Status Values
- `experimental`: Under development, use with caution
- `beta`: Testing phase, mostly stable  
- `stable`: Production ready, well tested
- `deprecated`: No longer recommended

### Common Experiment Types
`1d`, `2d`, `3d`, `cosy`, `tocsy`, `noesy`, `hsqc`, `hmqc`, `trosy`, `relaxation`, `diffusion`, `solid_state`

### Nuclei Format
Use standard isotope notation: `1H`, `13C`, `15N`, `31P`, `19F`, etc.

## Validation Rules

- Required fields must be present
- Dates must be in YYYY-MM-DD format
- Versions must follow semantic versioning (x.y.z)
- Authors can be "Name" or "Name <email>" format
- DOIs must start with "10."

For the complete schema definition, see the [current schema](current.md).
# Pulse Sequences

This directory contains NMR pulse sequence files with embedded YAML metadata annotations.

## Directory Structure

Sequences are stored as individual files in a flat structure:

```
sequences/
├── sofast_hmqc
├── t1_inversion_recovery
├── hsqc_watergate
└── cosy_standard
```

## Naming Conventions

- **Files**: Use descriptive names with underscores (`sofast_hmqc`, `t1_inversion_recovery`)
- **Format**: Lowercase letters, numbers, and underscores only
- **No extensions**: Pulse sequence files do not use file extensions

## Metadata Requirements

All sequence files must include embedded YAML metadata using the `;@` comment prefix. See the [schema documentation](../schemas/current) for complete field definitions.

### Minimal Example

```bruker
;@ schema_version: "0.0.1"
;@ sequence_version: "1.0.0"
;@ title: Basic T1 Measurement
;@ authors: [Your Name <email@institution.edu>]
;@ created: 2024-01-15
;@ last_modified: 2024-01-15
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: experimental

; Optional fields:
;@ experiment_type: [relaxation, 1d]

; Pulse program code follows...
"p1=4u"
"d1=1s"
```

## Contributing Sequences

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines on submitting new sequences.

## Validation

All sequences are validated through the PR review process. The PR Validation Action automatically checks annotations against the current schema and provides feedback via PR comments. Contributors can view validation status in their pull requests.

## Browse Sequences

- **Web interface**: Visit the [documentation site](https://waudbygroup.github.io/pulseprograms/sequences/)
- **Command line**: Use `ls sequences/` to list all sequences
- **Metadata search**: Use `grep -r "experiment_type.*hsqc" sequences/` to find specific types
# NMR Pulse Sequence Repository

A community-driven repository for sharing and documenting Nuclear Magnetic Resonance (NMR) pulse sequences with automated annotation, versioning, and documentation systems.

## Overview

This repository provides a platform for the NMR community to share pulse sequences with rich metadata, enabling better discoverability, reproducibility, and collaboration. All sequences are TopSpin-compatible and include embedded YAML annotations for enhanced documentation and automated processing.

## Goals

- **Future-proof but simple**: Start with pragmatic solutions that can evolve toward formal standards
- **Git-native**: Leverage Git for version control, merging, and change tracking
- **Community-friendly**: Multiple contribution pathways with varying barriers to entry
- **TopSpin compatible**: Sequences work seamlessly in existing Bruker workflows
- **Single source of truth**: All metadata embedded directly in pulse program files

## Quick Start

### Using Sequences

1. Browse the [sequences/](sequences/) directory or visit our [documentation site](https://waudbygroup.github.io/pulseprograms)
2. Download the pulse program file you need
3. Copy to your TopSpin experiment directory
4. The embedded annotations (`;@` comments) are ignored by TopSpin but provide rich metadata

### Example Sequence Structure

```bruker
;@ schema_version: "0.0.1"
;@ sequence_version: "1.0.0"
;@ title: SOFAST-HMQC
;@ experiment_type: [hmqc, 2d]
;@ features: [sofast, sensitivity_enhancement, selective_excitation]
;@ typical_nuclei: [1H, 13C, 15N]
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@   - P. Schanda
;@ created: 2024-01-15
;@ last_modified: 2025-08-15
;@ repository: github.com/waudbygroup/pulseprograms
;@ description: 1H,15N SOFAST-HMQC for rapid or sensitive measurements
;@ citation:
;@   - Schanda & Brutscher, J. Am. Chem. Soc. (2005) 127, 8014
;@ doi:
;@   - 10.1021/ja051306e
;@ status: stable

; Your standard Bruker pulse program follows here...
"p1=4u"
"d1=1s"
```

## Repository Structure

```
/
├── sequences/              # Pulse program files with embedded metadata
│   ├── 15n_sofast
│   └── 19f_r1rho_onres
├── schemas/               # YAML schema definitions
│   ├── v0.0.1.yaml       # Current schema version
│   └── current -> v0.0.1.yaml  # Symlink to current schema
├── docs/                  # Documentation source files
├── .github/workflows/     # GitHub Actions for validation & deployment
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md             # This file
```

## Annotation System

### Metadata Format

Sequences include embedded YAML metadata using the `;@` comment prefix. This approach ensures:
- **TopSpin compatibility**: Comments are ignored by the pulse program compiler
- **Single source of truth**: No separate metadata files to maintain
- **Version control**: Metadata travels with the sequence in Git

### Core Metadata Fields

**Required (with automatic defaults):**
- `schema_version`: Annotation schema version (auto-detected)
- `sequence_version`: Individual sequence version (defaults to "0.1.0")
- `title`: Short, descriptive sequence name (defaults to filename)
- `authors`: List of contributors with names and emails (defaults to GitHub user)
- `created`, `last_modified`: ISO dates (auto-populated from Git)
- `repository`: Repository URL for provenance (auto-detected from Git remote)
- `status`: Development status (defaults to "experimental")

**Optional:**
- `features`: Array of feature keywords
- `nuclei_hint`: Nuclei involved in the experiment
- `description`: Detailed explanation
- `citation`: Literature references
- `doi`: Related publication DOIs
- `status`: Development status (experimental/beta/stable/deprecated)

### Controlled Vocabularies

**Status Values:** `experimental`, `beta`, `stable`, `deprecated`

**Nuclei:** Standard isotope notation (`1H`, `13C`, `15N`, `31P`, `19F`, etc.)

## Contributing

We welcome contributions at all levels! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines including:

- **Low barrier**: Submit sequences via GitHub issues or email
- **Medium barrier**: Use guided web forms for metadata entry
- **High barrier**: Direct YAML annotation for full feature access

## Documentation

Full documentation is available at [https://waudbygroup.github.io/pulseprograms](https://waudbygroup.github.io/pulseprograms) including:

- Searchable sequence database
- Individual sequence pages with metadata and changelogs
- Schema documentation and validation rules
- Contribution guidelines and tutorials

## Versioning

### Schema Versioning
- Follows semantic versioning (major.minor.patch)
- Current version: 0.0.1
- Backwards compatibility maintained across minor versions

### Sequence Versioning
- Individual sequences have independent versions
- Git history provides automatic changelog generation
- Manual version management by contributors with PR validation
- Git-based changelogs from commit history and PR context

## Quality Standards

- All submissions undergo PR validation with automated feedback
- Schema compliance required for all annotations
- Community review process for new contributions via pull requests
- Educational feedback provided through PR comment suggestions
- Emphasis on complete metadata while maintaining accessibility

## Community

This project thrives on community participation. Whether you're sharing a novel pulse sequence, improving existing annotations, or helping with documentation, your contributions make the NMR community stronger.

### Getting Help

- Open an issue for questions or problems
- Check existing discussions for common topics
- Consult the documentation for detailed guides

## License

[Specify your chosen license here]

## Citation

If you use sequences from this repository in your research, please cite both the original sequence authors and this repository. Individual sequence pages provide specific citation information.

---

**Note**: This is an early-stage project. Features and documentation will expand as the community grows and contributes.
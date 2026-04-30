# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an NMR (Nuclear Magnetic Resonance) pulse sequence repository system designed as a community-driven platform for sharing and documenting pulse sequences with automated annotation, versioning, and documentation. The system is specifically designed for Bruker TopSpin compatibility.

## Architecture

### Core Design Philosophy
- **Git-native**: Leverages Git for version control, merging, and change tracking
- **Single source of truth**: Inline annotations in pulse program files using `;@` comment syntax
- **TopSpin compatible**: Sequences work seamlessly in existing Bruker workflows
- **Community-friendly**: Multiple contribution pathways with varying barriers to entry

### Repository Structure (Planned)
```
/
├── sequences/              # Pulse program files with embedded YAML metadata
│   ├── 15n_sofast
│   └── 19f_r1rho_onres
├── schemas/               # Schema definitions
│   ├── v0.0.1.yaml
│   ├── v0.0.2.yaml
│   ├── v0.0.3.yaml
│   └── current -> v0.0.3.yaml
├── docs/                  # Generated MkDocs documentation
├── .github/workflows/     # GitHub Actions for validation and deployment
├── CONTRIBUTING.md        # Instructions on how to contribute
└── README.md
```

### Annotation System
- Uses `;@` prefix for YAML metadata blocks within Bruker pulse program files
- Schema follows semantic versioning (currently v0.0.3)
- Individual sequence versioning independent of repository versioning
- Controlled vocabularies for experiment types, nuclei, and status fields

### Key Metadata Fields (v0.0.3 Schema)
Required fields (with automatic defaults):
- `schema_version`: "0.0.3" (semantic versioning)
- `sequence_version`: Sequence version (semantic) - defaults to "0.1.0"
- `title`: Short human-readable title - defaults to pulse program filename
- `authors`: List with name and email - defaults to GitHub user making the commit
- `created`, `last_modified`: Dates - automatically populated from Git history/commit dates
- `repository`: Repository URL - automatically detected from Git remote
- `status`: Development status - defaults to "experimental"
- `experiment_type`: Array of experiment type keywords (controlled vocabulary)

Optional fields:
- `features`: Array of feature keywords
- `typical_nuclei`: Array of nuclei, ordered by spectrometer channel (f1, f2, ...)
- `description`: Detailed description
- `citation`: Literature references
- `doi`: Related publication DOIs
- `dimensions`: Indirect-dimension identifiers using dotted-path notation (e.g. `relaxation.duration`, `f1`)
- `acquisition_order`: Acquisition loop order from innermost to outermost
- `reference_pulse`: List of reference pulse calibrations `{channel, duration, power}`
- Experiment-specific blocks: `calibration`, `relaxation`, `r1rho`, `cest`, `diffusion`. Each extends a common shape (`channel`, `power`, `duration`, `offset`, `type`, `model`) where any of `power`/`duration`/`offset` may be a parameter name, a number, a `linear` sweep `{start, end|step, scale}`, or a `{counter, scale}` expression.

### Technology Stack (Planned)
- **Documentation**: MkDocs with Material theme
- **Deployment**: GitHub Pages
- **Automation**: GitHub Actions for validation, versioning, and documentation generation

### Current State
Repository is in initial setup phase with only design documentation. No build system, tests, or automation implemented yet.

## Development Workflow

### GitHub Actions (2 Required)

#### 1. PR Validation Action
- **Trigger**: Pull request opened/updated
- **Purpose**: Extract `;@` annotations, validate against JSON schema, provide auto-injection suggestions via PR comments
- **Workflow**: Parse YAML → validate required fields → check controlled vocabularies → comment with missing fields/suggestions
- **Permissions**: Read repository, write PR comments

#### 2. Documentation Generation Action
- **Trigger**: Push to main branch (post-merge)
- **Purpose**: Generate MkDocs site with sequence database, individual sequence pages, and Git-based changelogs
- **Workflow**: Parse all sequence annotations → extract Git history per file → generate markdown pages → deploy to GitHub Pages
- **Permissions**: Read repository, write to GitHub Pages

### Branch Protection & PR-Only Workflow
**Design Decision**: All changes must go through pull requests with required status checks.

**Rationale**:
- GitHub Actions cannot block direct commits - they run after commits are already accepted
- Cross-fork auto-injection is impossible due to limited GitHub Actions permissions on forks
- Quality control - PR workflow ensures all merged content has passed validation and received human review
- Educational value - Contributors learn annotation system through guided feedback process
- Repository integrity - Main branch remains consistently clean and properly annotated

**Implementation**:
- Main branch requires PR with passing "PR Validation" status check
- No direct commits allowed (including for repository maintainer)
- Contributors handle versioning manually (validation checks version increments for modifications)
- Auto-injection suggestions provided via PR comments rather than automatic commits

### Version Management Strategy
- **Schema**: Semantic versioning with backwards compatibility
- **Sequences**: Individual versioning handled manually by contributors
- **Git-based changelogs**: Accurate history extracted from Git commits and PR context
- **Version validation**: PR validation checks ensure version increments for file modifications

## File Formats

### Pulse Program Files
Bruker pulse program files with embedded YAML metadata using `;@` comment syntax. Example:

```
;@ schema_version: "0.0.3"
;@ sequence_version: "1.1.0"
;@ title: SOFAST-HMQC
;@ experiment_type: [hmqc, 2d]
;@ features: [sofast, states_tppi]
;@ typical_nuclei: [1H, 13C, 15N]
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@   - P. Schanda
;@ created: 2024-01-15
;@ last_modified: 2026-04-30
;@ repository: github.com/waudbylab/pulseprograms
;@ description: 1H,15N SOFAST-HMQC for rapid or sensitive measurements
;@ citation:
;@   - Schanda & Brutscher, J. Am. Chem. Soc. (2005) 127, 8014
;@ doi:
;@   - 10.1021/ja051306e
;@ status: stable
;@ dimensions: [f3, f1]
;@ acquisition_order: [f1, f3]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ - {channel: f2, duration: p3, power: pl2}
;@ - {channel: f3, duration: p21, power: pl3}
```

### Schema Files
YAML schema definitions stored in `schemas/` directory with semantic versioning. Current schema is v0.0.3 (`schemas/current` symlinks to it).

### Controlled Vocabularies
- **experiment_type** (enum in v0.0.3): `1d`, `2d`, `3d`, `cosy`, `tocsy`, `noesy`, `hsqc`, `hmqc`, `trosy`, `relaxation`, `r1rho`, `cest`, `diffusion`, `calibration`, `solid_state`
- **nuclei**: Standard isotope notation (`1H`, `13C`, `15N`, `31P`, `19F`, etc.) or `nothing` placeholder for unused channels
- **status**: `experimental`, `beta`, `stable`, `deprecated`
- **features**: Open vocabulary — see VOCABULARY.md

## Schema Evolution Strategy
- Keep required fields minimal and stable
- Allow organic community-driven extension with informal fields
- Monitor usage patterns to identify common annotations for formalization
- Maintain backwards compatibility across schema versions
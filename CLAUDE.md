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
│   └── current -> v0.0.1.yaml
├── docs/                  # Generated MkDocs documentation
├── .github/workflows/     # GitHub Actions for validation and deployment
├── CONTRIBUTING.md        # Instructions on how to contribute
└── README.md
```

### Annotation System
- Uses `;@` prefix for YAML metadata blocks within Bruker pulse program files
- Schema follows semantic versioning (currently v0.0.1)
- Individual sequence versioning independent of repository versioning
- Controlled vocabularies for experiment types, nuclei, and status fields

### Key Metadata Fields (v0.0.1 Schema)
Required fields (with automatic defaults):
- `schema_version`: "0.0.1" (semantic versioning)
- `sequence_version`: Sequence version (semantic) - defaults to "0.1.0"
- `title`: Short human-readable title - defaults to pulse program filename
- `authors`: List with name and email - defaults to GitHub user making the commit
- `created`, `last_modified`: Dates - automatically populated from Git history/commit dates
- `repository`: Repository URL - automatically detected from Git remote
- `status`: Development status - defaults to "experimental"

Optional fields:
- `features`: Array of feature keywords
- `nuclei_hint`: Array of nuclei involved
- `description`: Detailed description
- `citation`: Literature references
- `doi`: Related publication DOIs
- `status`: experimental/beta/stable/deprecated

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
;@ schema_version: "0.0.1"
;@ sequence_version: "1.0.0"
;@ title: SOFAST-HMQC
;@ experiment_type: [hmqc, 2d]
;@ features: [sofast, sensitivity_enhancement, selective_excitation]
;@ nuclei_hint: [1H, 13C, 15N]
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
```

### Schema Files
YAML schema definitions stored in `schemas/` directory with semantic versioning. Current schema is v0.0.1.

### Controlled Vocabularies
- **experiment_type**: `1d`, `2d`, `3d`, `cosy`, `tocsy`, `noesy`, `hsqc`, `hmqc`, `trosy`, `relaxation`, `diffusion`, `solid_state` (extensible list)
- **nuclei**: Standard isotope notation (`1H`, `13C`, `15N`, `31P`, `19F`, etc.)
- **status**: `experimental`, `beta`, `stable`, `deprecated`

## Schema Evolution Strategy
- Keep required fields minimal and stable
- Allow organic community-driven extension with informal fields
- Monitor usage patterns to identify common annotations for formalization
- Maintain backwards compatibility across schema versions
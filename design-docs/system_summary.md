# NMR Pulse Sequence Repository System Design Summary

## Overview
This document outlines the design for a community-driven NMR pulse sequence repository with automated annotation, versioning, and documentation systems. The goal is to create a system that encourages community contribution whilst maintaining high-quality metadata and documentation.

## Core Principles
- **Future-proof but simple**: Start with pragmatic solutions that can evolve toward formal standards
- **Git-native**: Leverage Git for version control, merging, and change tracking
- **Community-friendly**: Multiple contribution pathways with varying barriers to entry
- **TopSpin compatible**: Sequences work seamlessly in existing workflows
- **Single source of truth**: Inline annotations in pulse program files only

## Annotation System

### Comment Syntax
Use `;@` as a special comment prefix for YAML metadata blocks within Bruker pulse program files:

```
;@ schema_version: "1.2.0"
;@ sequence_version: "2.1.3"
;@ title: HSQC with WATERGATE water suppression
;@ experiment_type: 2D_heteronuclear
;@ nuclei: [1H, 13C]
;@ authors:
;@   - A. Researcher
;@   - B. Collaborator
;@ last_modified: "2024-08-15"
```

### Metadata Format
- **Format**: YAML within `;@` comment blocks
- **Schema versioning**: Semantic versioning for annotation schema evolution
- **Controlled vocabularies**: Extensible vocabularies for experiment_type, nuclei, status, etc.
- **Future compatibility**: Field names and values aligned with potential NMR standards

### Core Metadata Fields
```yaml
schema_version: "0.0.1"        # Required: annotation schema version (semantic)
sequence_version: "1.0.0"      # Required: sequence version (semantic)
title: SOFAST-HMQC             # Required: short human-readable title
experiment_type: [hmqc, 2d]    # Required: list of keywords
features: [sofast, sensitivity_enhancement, selective_excitation]. # Optional
nuclei_hint: [1H, 13C, 15N]    # Optional: array of nuclei
authors:                       # Required: contributor list
- Chris Waudby <c.waudby@ucl.ac.uk>
- P. Schanda
created: 2024-01-15          # Required: creation date
last_modified: 2025-08-15    # Required: last modification date
repository: github.com/waudbygroup/pulseprograms  # Required: repository
description: 1H,15N SOFAST-HMQC for rapid or sensitive measurements   # Optional: detailed description
citation:
- Schanda & Brutscher, J. Am. Chem. Soc. (2005) 127, 8014
doi:          # Optional: related publication(s)
- 10.1021/ja051306e
status: stable                 # Optional: experimental/beta/stable/deprecated

# Future organic extensions (not yet formalised):
observe_channel: f1
dimensions: [f3, f1]
acquisition_order: [2, 1]
decoupling: [nothing, f3]
hard_pulse:
- [f1, p1, pl1]
- [f3, p21, pl3]
```

### Schema Evolution Strategy
- **Core schema**: Keep required fields minimal and stable (title, version, experiment_type, nuclei, authors, dates)
- **Organic extension**: Allow community to add informal fields (notes, parameters, setup_hints) without validation
- **Pattern recognition**: Monitor usage to identify common informal annotations
- **Gradual formalisation**: Add popular informal fields to official schema when patterns emerge
- **Backwards compatibility**: Ensure older annotations remain valid as schema evolves
- **Community-driven**: Let scientific community usage patterns drive metadata evolution rather than top-down design

### Vocabularies (Initial)

**experiment_type**: `1d`, `2d`, `3d`, `cosy`, `tocsy`, `noesy`, `hsqc`, `hmqc`, `trosy`, `relaxation`, `diffusion`, `solid_state`
- This should not be regarded as a complete list but a starting point

**nuclei**: Standard isotope notation (`1H`, `13C`, `15N`, `31P`, `19F`, etc.)

**status**: `experimental`, `beta`, `stable`, `deprecated`

## Repository Structure
```
/
├── sequences/              # Pulse program files
│   ├── 15n_sofast
│   └── 19f_r1rho_onres
├── schemas/               # Schema definitions
│   ├── v0.0.1.yaml
│   └── current -> v0.0.1.yaml
├── docs/                  # Generated documentation
├── .github/workflows/     # GitHub Actions
├── CONTRIBUTING.md        # Instructions on how to contribute
└── README.md
```

## Versioning Strategy

### Schema Versioning
- **Semantic versioning** for annotation schema
- **Major**: Breaking changes requiring migration
- **Minor**: Backwards-compatible additions
- **Patch**: Documentation/clarification updates

### Sequence Versioning
- **Individual sequence versioning** (not repository-wide)
- **Git history as changelog**: Extract change history from Git commits
- **Manual version management**: Contributors handle versioning in their PRs
- **PR validation**: Ensures version increments for file modifications
- **Git-based changelogs**: Generated from commit history and PR context

## Documentation System

### Technology Stack
- **MkDocs with Material theme**: Modern, searchable documentation
- **GitHub Pages**: Automatic deployment
- **GitHub Actions**: Automated generation from sequence metadata

### Site Structure
```
Home                   # Introduction, licensing, citing
├── Getting Started    # Usage and contribution guides
├── Sequence Database  # Searchable/filterable sequence list
├── Individual Pages   # One page per sequence
├── Contributing       # Community involvement, contributing policies
├── Annotation Schema  # Versioned schema documentation
└── GitHub Actions     # Technical documentation
```

### Content Generation
- **Sequence pages**: Metadata display, code blocks, Git-based changelog
- **Search functionality**: Built-in Material theme search across metadata
- **Automatic updates**: Rebuild on every repository change

## Contribution Pathways

### Low Barrier (Email/Issues)
- Accept plain Bruker sequences via GitHub issues or email
- Auto-convert to annotated format with minimal metadata
- Gradual enhancement by community

### Medium Barrier (Web Forms)
- Simple web form for guided metadata entry
- Auto-generate YAML from form inputs
- Journal submission-like experience

### Full Annotation
- Direct YAML editing for advanced users
- Complete schema utilisation
- Enhanced attribution and features

## GitHub Actions Architecture

### Required Actions
1. **PR Validation Action**: Extract `;@` annotations, validate against JSON schema, provide auto-injection suggestions via PR comments
2. **Documentation Generation Action**: Generate MkDocs site with sequence database, individual sequence pages, and Git-based changelogs

### Workflow Triggers
- **Pull requests**: PR Validation Action for schema compliance and feedback
- **Push to main branch**: Documentation generation and deployment to GitHub Pages

### Branch Protection
- All changes must go through pull requests with required status checks
- No direct commits to main branch allowed (including for maintainers)
- Contributors handle versioning manually with PR validation checks

## Repository Management

### Pull Request Policy
- **Initial management**: Repository owner (lecturer) reviews and merges all contributions
- **Quality standards**: All submissions must pass automated validation
- **Community growth**: As repository gains adoption, establish trusted contributor roles
- **Governance evolution**: Transition to community-driven review process for established contributors
- **Conflict resolution**: Maintainer has final authority on design decisions and standards

### Community Guidelines
- **Respectful collaboration**: Academic courtesy and constructive feedback
- **Attribution requirements**: Proper credit for sequence developers and contributors
- **Quality expectations**: Encourage complete annotations while maintaining low barriers
- **Educational focus**: Prioritise sequences that help others learn and reproduce experiments

## Community Engagement Strategy
- **Lead with practical value**: Focus on useful sequences, not annotation system
- **Optional adoption**: Traditional and annotated formats available
- **Target pain points**: Poor documentation, lack of searchability
- **Leverage networks**: Conference presentations, respected endorsements

### Quality Incentives
- **Featured sequences**: Highlight well-annotated contributions
- **Usage statistics**: Show download/citation metrics
- **DOI assignment**: Academic attribution for significant sequences
- **Collaborative enhancement**: Community-driven metadata improvement

## Future Extensions

### Dataset Integration
- **Bidirectional linking**: Sequences ↔ example datasets
- **User-contributed examples**: Upload datasets linked to sequences
- **Extended metadata**: Dataset references in sequence annotations

### Advanced Features
- **Parameter calculators**: Embedded Julia code for delay calculations
- **Simulation integration**: Links to theoretical predictions
- **Performance metrics**: Community-reported success rates
- **Cross-platform support**: Varian, Agilent format generation
- **Pulse program validation**: GitHub Actions for syntax checking and linting Bruker pulse programs
- **Code quality checks**: Automated detection of common pulse programming errors or inefficiencies
- **Semantic annotations**: Advanced parameter mapping and dimensional structure (building on community usage patterns)
- **Automated analysis integration**: Enable analysis software to automatically understand experimental structure from annotations

## Technical Considerations

### TopSpin Compatibility
- `;@` comments ignored by pulse program compiler
- No modification to existing workflows required
- Enhanced functionality available for engaged users

### Julia Integration
- **YAML.jl**: Parse and generate annotations programmatically
- **Future tooling**: Analysis scripts, parameter optimisation
- **Community scripts**: Share Julia code alongside sequences

### Standards Alignment
- **Field naming**: Compatible with emerging NMR standards
- **Vocabulary mapping**: Enable future alignment with formal ontologies
- **Migration pathways**: Smooth transition to formal standards when available
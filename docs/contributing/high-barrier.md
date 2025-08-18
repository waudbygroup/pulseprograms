# High Barrier Contribution

Complete control over metadata annotation with full schema compliance.

## Method: Full YAML Annotation

For users who want maximum control and searchability for their sequences.

### Prerequisites

- Strong understanding of YAML syntax
- Familiarity with NMR terminology
- Knowledge of Git workflows
- Understanding of semantic versioning

### Complete Metadata Template

```bruker
;@ schema_version: "0.0.1"
;@ sequence_version: "1.2.0"
;@ title: SOFAST-HMQC with TROSY
;@ experiment_type: [hmqc, 2d, trosy]
;@ features: [sofast, sensitivity_enhancement, selective_excitation, trosy]
;@ nuclei_hint: [1H, 15N]
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@   - P. Schanda
;@ created: 2024-01-15
;@ last_modified: 2024-08-17
;@ repository: github.com/waudbygroup/pulseprograms
;@ description: >
;@   1H,15N SOFAST-HMQC with TROSY selection for rapid or sensitive
;@   measurements of large proteins. Includes selective excitation
;@   and sensitivity enhancement.
;@ citation:
;@   - Schanda & Brutscher, J. Am. Chem. Soc. (2005) 127, 8014
;@   - Pervushin et al., Proc. Natl. Acad. Sci. (1997) 94, 12366
;@ doi:
;@   - 10.1021/ja051306e
;@   - 10.1073/pnas.94.23.12366
;@ status: stable

; Pulse sequence code follows...
```

### Field Reference

#### Required Fields
- `schema_version`: Always "0.0.1" for current schema
- `sequence_version`: Semantic version (major.minor.patch)
- `title`: Descriptive sequence name
- `authors`: Array of contributors (name or name <email>)
- `created`: Initial creation date (YYYY-MM-DD)
- `last_modified`: Last modification date (YYYY-MM-DD)
- `repository`: Repository identifier
- `status`: One of `experimental`, `beta`, `stable`, `deprecated`

#### Key Optional Fields
- `experiment_type`: Keywords for searchability
- `description`: Detailed explanation
- `features`: Technical features and enhancements
- `nuclei_hint`: Nuclei involved in experiment
- `citation`: Literature references
- `doi`: DOI identifiers for citations

### Controlled Vocabularies

#### Experiment Types
Common values: `1d`, `2d`, `3d`, `cosy`, `tocsy`, `noesy`, `hsqc`, `hmqc`, `trosy`, `relaxation`, `diffusion`, `solid_state`

#### Status Values
- `experimental`: Under development, use with caution
- `beta`: Testing phase, mostly stable
- `stable`: Production ready, well tested
- `deprecated`: No longer recommended

#### Nuclei Format
Use standard isotope notation: `1H`, `13C`, `15N`, `31P`, `19F`, etc.

### Validation Process

1. **Schema Compliance**: All fields validated against JSON schema
2. **Syntax Check**: YAML formatting verification
3. **Content Review**: Scientific accuracy and completeness
4. **Version Tracking**: Semantic version consistency

### Benefits

- 🎯 Maximum searchability and discoverability
- 📊 Rich metadata for advanced filtering
- 🔍 Detailed documentation for users
- 🏆 Full credit and recognition
- ⚡ Immediate integration after validation

### Advanced Features

#### Version Management
- Use semantic versioning for sequence updates
- Increment patch version for minor fixes
- Increment minor version for new features
- Increment major version for breaking changes

#### Multi-line Descriptions
```yaml
;@ description: >
;@   This is a multi-line description that can span
;@   several lines while maintaining proper YAML syntax.
;@   Use the > character for folded multi-line strings.
```

#### Complex Author Lists
```yaml
;@ authors:
;@   - John Doe <john@university.edu>
;@   - Jane Smith
;@   - Collaborator Name <collaborator@institution.org>
```

Perfect for users who want complete control and maximum impact!
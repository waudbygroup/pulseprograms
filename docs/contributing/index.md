# Contributing

We welcome contributions from the entire NMR community! This repository is designed to accommodate contributors with varying levels of technical expertise.

## Quick Links

- **GitHub Repository**: [waudbygroup/pulseprograms](https://github.com/waudbygroup/pulseprograms)
- **Issues**: [Submit sequences or report problems](https://github.com/waudbygroup/pulseprograms/issues)
- **Pull Requests**: [Direct contributions](https://github.com/waudbygroup/pulseprograms/pulls)

## Contribution Methods

### 🚀 Low Barrier: GitHub Issues
- Open a new issue with your pulse sequence
- Provide basic information (name, type, author)
- Maintainers will add metadata and integrate

### 🎯 Medium Barrier: Pull Requests
- Fork the repository
- Add your sequence with basic metadata
- Submit a pull request for review

### 🔬 High Barrier: Full Annotation
- Complete YAML metadata annotations
- Follow schema requirements exactly
- Maximum searchability and features

## Metadata Requirements

All sequences must include embedded YAML metadata using `;@` comment prefix:

```bruker
;@ schema_version: "0.0.1"
;@ sequence_version: "1.0.0"
;@ title: Your Sequence Name
;@ authors: [Your Name <email@institution.edu>]
;@ created: 2024-01-15
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: experimental

; Your pulse program code follows...
```

## Quality Standards

- Sequences must work correctly in TopSpin
- Required metadata fields must be included
- YAML syntax must be valid
- Follow naming conventions (snake_case)

For complete guidelines, see the [CONTRIBUTING.md](https://github.com/waudbygroup/pulseprograms/blob/main/CONTRIBUTING.md) file in the repository.
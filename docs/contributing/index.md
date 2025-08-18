# Contributing

We welcome contributions from the entire NMR community! This repository is designed to accommodate contributors with varying levels of technical expertise.

## Contribution Methods

### Easy: Use GitHub Issues

Quick link: [Submit a new sequence or report a problem](https://github.com/waudbygroup/pulseprograms/issues)

- Open a new issue and paste in or attach your pulse sequence
- Provide basic information (name, type, author)
- Maintainers will add essential metadata and integrate

### Advanced: Submit a Pull Request
- Fork the [repository](https://github.com/waudbygroup/pulseprograms)
- Add your sequence including at least essential metadata
- Submit a [pull request](https://github.com/waudbygroup/pulseprograms/pulls) for review

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

For complete guidelines, see the [CONTRIBUTING.md](https://github.com/waudbygroup/pulseprograms/blob/main/CONTRIBUTING.md) file in the repository.
# Contributing

Two ways to contribute a pulse sequence:

1. **Open an [issue](../../issues/new)** with the file attached and a brief description. We'll add metadata and merge it.
2. **Open a pull request** with the file in `sequences/` and the YAML metadata block at the top.

## Annotation format

Embed YAML metadata at the top of your pulse program using the `;@` comment prefix:

```bruker
;@ schema_version: "0.0.3"
;@ sequence_version: "1.0.0"
;@ title: Your Sequence Name
;@ experiment_type: [hmqc, 2d]
;@ authors:
;@   - Your Name <your.email@institution.edu>
;@ created: 2026-04-30
;@ last_modified: 2026-04-30
;@ repository: github.com/waudbylab/pulseprograms
;@ status: experimental

; pulse program code follows...
```

`schema_version`, `sequence_version`, `title`, `authors`, `created`, `last_modified`, `repository`, `status`, and `experiment_type` are required. See [schemas/current](schemas/current) for the full field list and [VOCABULARY.md](VOCABULARY.md) for `experiment_type`/`features` values.

## Conventions

- Filenames use `snake_case` and live directly in `sequences/`.
- Bump `sequence_version` (semver) when you modify a sequence — patch for fixes, minor for new features, major for breaking changes.
- All changes go through PRs — automated validation checks schema compliance and posts suggestions on the PR.

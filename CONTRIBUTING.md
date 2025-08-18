# Contributing to the NMR Pulse Sequence Repository

We welcome contributions from the entire NMR community! This repository is designed to accommodate contributors with varying levels of technical expertise and time availability.

## Contribution Pathways

### 🚀 Low Barrier: Submit via Issues or Email

**Best for:** Quick sequence sharing, minimal time investment

**Process:**
1. **GitHub Issues**: Open a [new issue](../../issues/new) with the "Sequence Submission" template
2. **Email**: Send sequences to [repository maintainer email]
3. **What to include:**
   - Your pulse program file
   - Basic information: sequence name, experiment type, author name
   - Optional: brief description, literature reference

**What happens next:**
- Maintainers will add basic metadata annotations
- Sequence gets added to the repository with minimal annotation
- Community can enhance metadata over time
- You'll be credited as the original contributor

**Example submission:**
```
Subject: New sequence: SOFAST-HMQC

Hi! I'd like to share my SOFAST-HMQC sequence.

Attached: sofast_hmqc
Author: Chris Waudby
Experiment type: 2D heteronuclear correlation
Reference: Schanda & Brutscher, JACS 2005

Thanks!
```

### 🎯 Medium Barrier: Guided Web Form

**Best for:** Structured metadata entry, journal-style submission

**Process:**
1. Visit our [sequence submission form](https://waudbygroup.github.io/pulseprograms/submit) *(Coming soon)*
2. Upload your pulse program file
3. Fill out guided metadata form with:
   - Required fields (title, experiment type, authors, dates)
   - Optional fields (features, nuclei, description, citations)
4. Preview generated YAML annotation
5. Submit for review

**What happens next:**
- Automatic validation of metadata
- Generated pull request for community review
- Integration into repository upon approval
- Enhanced search and discovery features

### 🔬 High Barrier: Full YAML Annotation

**Best for:** Power users, complete metadata control, advanced features

**Process:**
1. Fork this repository
2. Create a new directory in `sequences/` for your submission
3. Add your pulse program file with complete YAML annotations
4. Follow the [annotation guide](#annotation-guide) below
5. Submit a pull request

**What you get:**
- Full control over metadata structure
- Access to all schema features
- Enhanced attribution and provenance
- Priority in search results and documentation

## Annotation Guide

### Basic Structure

Embed YAML metadata in your pulse program using `;@` comment prefix:

```bruker
;@ schema_version: "0.0.1"
;@ sequence_version: "1.0.0"
;@ title: Your Sequence Name
;@ experiment_type: [type1, type2]
;@ authors:
;@   - Your Name <your.email@institution.edu>
;@ created: 2024-01-15
;@ last_modified: 2025-08-15
;@ repository: github.com/waudbygroup/pulseprograms

; Your pulse program code follows...
"p1=4u"
"d1=1s"
```

### Required Fields (with automatic defaults)

| Field | Type | Description | Example | Default |
|-------|------|-------------|---------|---------|
| `schema_version` | string | Current schema version | `"0.0.1"` | Auto-detected |
| `sequence_version` | string | Sequence version (semantic) | `"1.2.3"` | `"0.1.0"` |
| `title` | string | Short, descriptive name | `"SOFAST-HMQC"` | Filename |
| `authors` | array | Contributors with contact info | `["Name <email>"]` | GitHub user |
| `created` | string | Creation date (YYYY-MM-DD) | `"2024-01-15"` | Git commit date |
| `last_modified` | string | Last modification date | `"2025-08-15"` | Git commit date |
| `repository` | string | Repository identifier | `"github.com/user/repo"` | Git remote URL |
| `status` | string | Development status | `"stable"` | `"experimental"` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `features` | array | Feature keywords |
| `nuclei_hint` | array | Nuclei involved (e.g., `["1H", "13C"]`) |
| `description` | string | Detailed explanation (max 500 chars) |
| `citation` | array | Literature references |
| `doi` | array | Publication DOIs |
| `status` | string | `experimental/beta/stable/deprecated` |
| `institution` | string | Primary institution |
| `keywords` | array | Additional search terms |

### Controlled Vocabularies

**Experiment Types:**
`1d`, `2d`, `3d`, `4d`, `cosy`, `tocsy`, `noesy`, `roesy`, `hsqc`, `hmqc`, `hmbc`, `trosy`, `dept`, `inept`, `inadequate`, `relaxation`, `diffusion`, `exchange`, `solid_state`, `mas`, `cpmas`, `dosy`, `cpmg`, `watergate`

**Status Values:**
`experimental`, `beta`, `stable`, `deprecated`

**Nuclei Format:**
Standard isotope notation: `1H`, `13C`, `15N`, `31P`, `19F`, etc.

### Versioning Guidelines

**Sequence Versions:**
- **Patch (x.y.Z)**: Bug fixes, minor parameter adjustments
- **Minor (x.Y.z)**: New features, significant parameter changes
- **Major (X.y.z)**: Breaking changes, fundamental modifications

**When to increment:**
- Contributors handle versioning manually in their PRs
- PR validation checks ensure version increments for file modifications
- Version history is automatically tracked through Git commits and PR context

## Quality Standards

### Before Submitting

- [ ] Sequence works correctly in TopSpin
- [ ] All required metadata fields included
- [ ] YAML syntax is valid (use online validator if unsure)
- [ ] Citations and DOIs are accurate
- [ ] File follows naming conventions (`snake_case`)

### Naming Conventions

**Files:** Use descriptive, lowercase names with underscores
- ✅ `sofast_hmqc`, `t1_inversion_recovery`
- ❌ `mySeq`, `test`, `sequence1`

**File placement:** Store directly in sequences directory
- ✅ `sequences/sofast_hmqc`
- ❌ `sequences/subdirectory/sofast_hmqc`

### Review Process

1. **PR Validation Action**: Automatic extraction and validation of `;@` annotations, schema compliance checking, controlled vocabulary validation
2. **Auto-injection suggestions**: PR comments provide specific guidance for missing or invalid fields
3. **Community review**: Scientific accuracy, metadata completeness, and educational value
4. **Maintainer approval**: Final quality check and integration
5. **Post-merge documentation**: Automatic generation of sequence pages and Git-based changelogs

**Note**: All changes must go through pull requests. Direct commits to main branch are not allowed, even for maintainers.

## Community Guidelines

### Code of Conduct

- **Respectful collaboration**: Maintain academic courtesy and professionalism
- **Constructive feedback**: Focus on improving sequences and documentation
- **Attribution requirements**: Always credit original sequence developers
- **Educational focus**: Prioritize sequences that help others learn and reproduce experiments

### Best Practices

- **Complete annotations**: Provide as much useful metadata as possible
- **Clear descriptions**: Help others understand when and how to use your sequence
- **Cite sources**: Reference original publications and inspirations
- **Test thoroughly**: Ensure sequences work as described
- **Update regularly**: Keep contact information and status current

### Getting Help

- **Documentation**: Check the [schema guide](schemas/v0.0.1.yaml) for detailed field descriptions
- **Examples**: Browse existing sequences for annotation patterns
- **Issues**: Open a GitHub issue for technical questions
- **Discussions**: Use GitHub Discussions for general questions and community interaction

## Recognition and Attribution

### How We Credit Contributors

- **Author attribution**: Listed in sequence metadata and documentation
- **Contributor pages**: Individual profiles with contribution history
- **Citation generation**: Automatic citation formats for academic use
- **Featured sequences**: Highlighting exceptional contributions

### Academic Integration

- **DOI assignment**: For significant sequence contributions
- **Publication linking**: Connect sequences to related papers
- **Usage metrics**: Track downloads and citations
- **Conference presentations**: Opportunities to present the repository

## Development Workflow

### For Repository Maintainers

1. **Review submissions**: Validate technical accuracy and completeness
2. **Enhance metadata**: Add missing annotations from literature
3. **Community moderation**: Ensure respectful, constructive interactions
4. **Schema evolution**: Monitor usage patterns for future enhancements
5. **Documentation updates**: Keep guides current with community needs

### Future Enhancements

We're always looking for contributors to help with:

- **Web form development**: Building user-friendly submission interfaces
- **Documentation improvements**: Making guides clearer and more comprehensive
- **Schema extensions**: Adding fields based on community usage patterns
- **Validation tools**: Creating better checking and testing systems
- **Integration projects**: Connecting with analysis software and databases

---

## Quick Start Checklist

### First-time Contributors

- [ ] Read this contributing guide
- [ ] Choose your contribution pathway (low/medium/high barrier)
- [ ] Check existing sequences to avoid duplicates
- [ ] Follow naming and annotation conventions
- [ ] Test your sequence in TopSpin
- [ ] Submit via your chosen pathway

### Regular Contributors

- [ ] Keep your author information updated
- [ ] Monitor your submitted sequences for community feedback
- [ ] Help review new submissions
- [ ] Suggest improvements to documentation and processes
- [ ] Share the repository with colleagues

Thank you for contributing to the NMR community! 🧪✨
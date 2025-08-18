# Review Process

Understanding how contributions are reviewed and integrated.

## Automated Validation

All contributions go through automated validation before human review.

### PR Validation System

When you submit a pull request, our automated system:

1. **Syntax Check**: Validates YAML formatting in sequence metadata
2. **Schema Validation**: Ensures all required fields are present and properly formatted
3. **Filename Check**: Verifies naming conventions
4. **Version Analysis**: Checks for proper version incrementation on updates

### Educational Feedback

The validation system provides helpful guidance:

```markdown
📋 Current Metadata:
- schema_version: 0.0.1
- title: my_sequence

❌ Required Actions:
- Schema validation failed: 'sequence_version' is a required property

📝 Add Missing Required Fields:
;@ sequence_version: "0.1.0"
;@ authors: [Your Name <email@institution.edu>]
;@ created: "2024-08-17"
;@ last_modified: "2024-08-17"
;@ repository: "github.com/waudbygroup/pulseprograms"
;@ status: experimental

💡 Recommended Optional Fields:
- experiment_type: Keywords describing the experiment type
- description: Brief description of what this sequence does
```

## Human Review Process

### Maintainer Review Checklist

1. **Scientific Accuracy**
   - Sequence functionality in TopSpin
   - Correct experiment classification
   - Appropriate metadata fields

2. **Quality Standards**
   - Clear, descriptive titles
   - Adequate documentation
   - Proper author attribution

3. **Repository Standards**
   - Consistent naming conventions
   - Appropriate file organization
   - Version management compliance

### Review Timeline

- **Automated checks**: Immediate (< 1 minute)
- **Initial maintainer review**: 24-48 hours
- **Detailed review**: 2-5 business days
- **Integration**: Upon approval

### Common Review Comments

#### Metadata Improvements
- "Consider adding more descriptive experiment_type keywords"
- "Please add a brief description field for user clarity"
- "Citation formatting could be improved"

#### Technical Issues
- "Sequence parameters need verification"
- "Filename should follow snake_case convention"
- "Version number needs to be incremented for changes"

#### Documentation Requests
- "Could you expand the description with usage notes?"
- "Missing nuclei_hint field would improve searchability"
- "Consider adding literature references"

## Approval Criteria

### Required for Approval
✅ Valid YAML syntax
✅ All required metadata fields present
✅ Functional pulse sequence
✅ Appropriate file naming
✅ Clear authorship

### Encouraged for Higher Impact
🌟 Rich optional metadata
🌟 Literature citations
🌟 Detailed descriptions
🌟 Feature keywords
🌟 Example parameters

## Post-Review Process

### Upon Approval
1. **Merge**: Pull request merged to main branch
2. **Documentation**: Automatic documentation generation
3. **Database**: Sequence added to searchable database
4. **Recognition**: Author credit in repository and docs

### Continuous Improvement
- Community feedback integration
- Periodic metadata enrichment
- Version updates and maintenance

## Getting Help During Review

### Resources
- Comment on your PR with questions
- Check existing sequences for examples
- Review schema documentation
- Join community discussions

### Common Questions
- "How do I format multi-line descriptions?"
- "What experiment_type keywords should I use?"
- "How should I handle collaborative authorship?"
- "When should I increment version numbers?"

The review process is designed to be educational and supportive - we're here to help you contribute successfully!
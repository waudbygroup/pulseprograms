# Medium Barrier Contribution

Direct contribution via GitHub Pull Requests with guided assistance.

## Method: Pull Requests with Basic Metadata

Ideal for users comfortable with Git but who want guidance on metadata formatting.

### Prerequisites

- GitHub account
- Basic Git knowledge (clone, commit, push)
- Understanding of YAML syntax (we'll help!)

### Step-by-Step Process

1. **Fork Repository**: Click "Fork" on the [main repository](https://github.com/waudbygroup/pulseprograms)

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/pulseprograms.git
   cd pulseprograms
   ```

3. **Add Your Sequence**: 
   - Place pulse program file in `sequences/` directory
   - Use descriptive filename (e.g., `15n_hsqc_trosy.cw`)

4. **Add Basic Metadata**: Include minimum required fields:
   ```bruker
   ;@ schema_version: "0.0.1"
   ;@ sequence_version: "1.0.0"
   ;@ title: Your Sequence Name
   ;@ authors: [Your Name <email@institution.edu>]
   ;@ created: 2024-01-15
   ;@ last_modified: 2024-01-15
   ;@ repository: github.com/waudbygroup/pulseprograms
   ;@ status: experimental
   
   ; Your pulse program code...
   ```

5. **Commit and Push**:
   ```bash
   git add sequences/your_sequence_name
   git commit -m "Add [sequence name] pulse sequence"
   git push origin main
   ```

6. **Create Pull Request**: Go to your fork on GitHub and click "Create Pull Request"

### Automated Assistance

Our PR validation system will automatically:

- ✅ Check metadata syntax
- 📝 Suggest missing optional fields
- 🔧 Provide copy-paste ready corrections
- 📊 Validate against schema requirements

### What the Review Process Includes

1. **Automated Checks**: Immediate feedback on metadata format
2. **Maintainer Review**: Verification of sequence functionality
3. **Suggestions**: Recommendations for additional metadata fields
4. **Integration**: Merge into main repository once approved

### Benefits

- 🚀 Faster than issue-based submission
- 🎯 Direct control over your contribution
- 📚 Learn metadata annotation system
- 🤖 Automated validation and suggestions

### Example Workflow

The PR validation system will comment on your pull request with specific suggestions:

```markdown
### 📝 Add Missing Required Fields:
;@ experiment_type: [hsqc, 2d]
;@ description: Brief description of what this sequence does

### 💡 Recommended Optional Fields:
- nuclei_hint: [1H, 15N] 
- features: [trosy, sensitivity_enhancement]
```

Perfect balance of control and guidance!
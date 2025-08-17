#!/usr/bin/env python3
"""
PR Validation Script - Provides educational feedback and auto-injection suggestions.
"""
import os
import re
import yaml
import json
import subprocess
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple
from jsonschema import validate, ValidationError

class PRValidator:
    def __init__(self):
        self.repo_info = self.get_repo_info()
        self.schema = self.load_schema()
        self.validation_results = []
        self.suggestions = []
        
    def get_repo_info(self) -> Dict[str, str]:
        """Extract repository information from Git and GitHub."""
        info = {
            'url': 'github.com/waudbygroup/pulseprograms',
            'name': 'pulseprograms',
            'author_name': 'Your Name',
            'author_email': 'email@institution.edu'
        }
        
        try:
            # Get repository URL from git remote
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                remote_url = result.stdout.strip()
                # Convert SSH/HTTPS URL to github.com format
                if 'github.com' in remote_url:
                    repo_path = remote_url.split('github.com')[1].strip('/:').replace('.git', '')
                    info['url'] = f"github.com/{repo_path}"
                    info['name'] = repo_path.split('/')[-1]
            
            # Try to get contributor info from environment variables (GitHub Actions context)
            pr_author = os.environ.get('PR_AUTHOR')
            if pr_author:
                info['author_name'] = pr_author
                
                # Try to get email from GitHub API
                github_token = os.environ.get('GITHUB_TOKEN')
                if github_token:
                    try:
                        import requests
                        headers = {
                            'Authorization': f'token {github_token}',
                            'Accept': 'application/vnd.github.v3+json'
                        }
                        response = requests.get(f'https://api.github.com/users/{pr_author}', headers=headers)
                        if response.status_code == 200:
                            user_data = response.json()
                            if user_data.get('email'):
                                info['author_email'] = user_data['email']
                            if user_data.get('name'):
                                info['author_name'] = user_data['name']
                            # Don't set a fake email if we can't get a real one
                    except:
                        pass  # Keep defaults
            
            # Fallback: try git config (won't work in CI but good for local testing)
            if info['author_name'] == 'Your Name':
                name_result = subprocess.run(['git', 'config', 'user.name'], 
                                           capture_output=True, text=True)
                if name_result.returncode == 0 and name_result.stdout.strip():
                    info['author_name'] = name_result.stdout.strip()
            
            if info['author_email'] == 'email@institution.edu':
                email_result = subprocess.run(['git', 'config', 'user.email'], 
                                            capture_output=True, text=True)
                if email_result.returncode == 0 and email_result.stdout.strip():
                    info['author_email'] = email_result.stdout.strip()
            
        except:
            pass
        
        return info
    
    def load_schema(self) -> Dict[str, Any]:
        """Load the current schema."""
        schema_file = Path("schemas/current")
        if not schema_file.exists():
            schema_file = Path("schemas/v0.0.1.yaml")
        
        with open(schema_file, 'r') as f:
            return yaml.safe_load(f)
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed sequence files in this PR."""
        try:
            # Get files changed in PR (compared to base branch)
            result = subprocess.run(['git', 'diff', '--name-only', 'origin/main...HEAD'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                changed_files = []
                for file in result.stdout.strip().split('\n'):
                    if file.startswith('sequences/') and not file.endswith('README.md'):
                        changed_files.append(file)
                return changed_files
        except:
            pass
        
        # Fallback: check all sequence files
        sequences_dir = Path("sequences")
        if sequences_dir.exists():
            return [str(f) for f in sequences_dir.iterdir() 
                   if f.is_file() and f.name != 'README.md']
        return []
    
    def extract_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extract YAML metadata from a sequence file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML metadata
            yaml_pattern = r'^;@\s*(.+)$'
            yaml_lines = []
            
            for line in content.split('\n'):
                match = re.match(yaml_pattern, line)
                if match:
                    yaml_lines.append(match.group(1))
            
            if not yaml_lines:
                return None
            
            yaml_content = '\n'.join(yaml_lines)
            metadata = yaml.safe_load(yaml_content)
            
            if not isinstance(metadata, dict):
                return None
            
            # Convert date objects to strings for validation
            for key, value in metadata.items():
                if isinstance(value, date):
                    metadata[key] = value.isoformat()
            
            return metadata
            
        except Exception as e:
            return None
    
    def generate_auto_suggestions(self, file_path: str, metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate consolidated auto-injection suggestions."""
        file_name = Path(file_path).name
        suggestions = {
            'missing_required': [],
            'suggested_metadata': {},
            'improvements': [],
            'optional_recommendations': []
        }
        
        if metadata is None:
            # Complete metadata template for files with no annotations
            author_name = self.repo_info["author_name"]
            author_email = self.repo_info["author_email"]
            
            if author_email != 'email@institution.edu':
                # We have a real email
                authors_value = f'[{author_name} <{author_email}>]'
            else:
                # No real email, just use name
                authors_value = f'[{author_name}]'
            
            complete_template = {
                'schema_version': '"0.0.1"',
                'sequence_version': '"0.1.0"',
                'title': f'"{file_name}"',
                'authors': authors_value,
                'created': f'"{date.today().isoformat()}"',
                'last_modified': f'"{date.today().isoformat()}"',
                'repository': f'"{self.repo_info["url"]}"',
                'status': 'experimental'
            }
            
            suggestions['complete_template'] = complete_template
            return suggestions
        
        # Check for missing required fields
        required_fields = self.schema.get('required', [])
        missing_required = []
        suggested_additions = {}
        
        for field in required_fields:
            if field not in metadata:
                missing_required.append(field)
                suggested_additions[field] = self.get_default_value(field, file_name)
        
        suggestions['missing_required'] = missing_required
        suggestions['suggested_metadata'] = suggested_additions
        
        # Field improvements
        if 'title' in metadata and metadata['title'] == file_name:
            suggestions['improvements'].append({
                'field': 'title',
                'current': metadata['title'],
                'suggestion': 'Consider a more descriptive title',
                'example': '"Descriptive Sequence Name"'
            })
        
        # Optional field recommendations (as examples, not literal suggestions)
        valuable_optional_fields = {
            'experiment_type': {
                'description': 'Array of keywords describing the experiment type',
                'examples': ['hsqc', '2d', 'cosy', 'tocsy', 'noesy', 'relaxation', '1d', 'cest']
            },
            'nuclei_hint': {
                'description': 'Array of nuclei involved in the experiment', 
                'examples': ['1H', '13C', '15N', '19F', '31P']
            },
            'description': {
                'description': 'Brief description of what this sequence does and when to use it',
                'examples': []
            },
            'features': {
                'description': 'Array of technical features used in the sequence',
                'examples': ['watergate', 'gradient', 'selective', 'sofast', 'trosy']
            }
        }
        
        missing_optional = {}
        for field, info in valuable_optional_fields.items():
            if field not in metadata:
                missing_optional[field] = info
        
        if missing_optional:
            suggestions['optional_recommendations'] = missing_optional
        
        return suggestions
    
    def get_default_value(self, field: str, file_name: str) -> str:
        """Get appropriate default value for a field."""
        # Handle authors field specially based on available info
        if field == 'authors':
            author_name = self.repo_info["author_name"]
            author_email = self.repo_info["author_email"]
            
            if author_email != 'email@institution.edu':
                # We have a real email
                return f'[{author_name} <{author_email}>]'
            else:
                # No real email, just use name
                return f'[{author_name}]'
        
        defaults = {
            'schema_version': '"0.0.1"',
            'sequence_version': '"0.1.0"',
            'title': f'"{file_name}"',
            'created': f'"{date.today().isoformat()}"',
            'last_modified': f'"{date.today().isoformat()}"',
            'repository': f'"{self.repo_info["url"]}"',
            'status': 'experimental'
        }
        return defaults.get(field, '""')
    
    def validate_sequence(self, file_path: str) -> Dict[str, Any]:
        """Validate a single sequence file."""
        file_name = Path(file_path).name
        result = {
            'file': file_path,
            'valid': False,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Extract metadata
        metadata = self.extract_metadata(file_path)
        
        if metadata is None:
            result['errors'].append("No YAML metadata found")
            result['suggestions'] = self.generate_auto_suggestions(file_path, None)
            return result
        
        # Validate against schema
        try:
            validate(instance=metadata, schema=self.schema)
            result['valid'] = True
        except ValidationError as e:
            result['errors'].append(f"Schema validation failed: {e.message}")
        
        # Generate suggestions
        result['suggestions'] = self.generate_auto_suggestions(file_path, metadata)
        
        # Check for common issues and warnings
        if 'experiment_type' not in metadata:
            result['warnings'].append("Missing experiment_type - adds discoverability")
        
        if 'description' not in metadata:
            result['warnings'].append("Missing description - helps users understand the sequence")
        
        return result
    
    def validate_all_changed_files(self) -> List[Dict[str, Any]]:
        """Validate all changed sequence files."""
        changed_files = self.get_changed_files()
        results = []
        
        for file_path in changed_files:
            if os.path.exists(file_path):
                result = self.validate_sequence(file_path)
                results.append(result)
        
        return results
    
    def generate_pr_comment(self, results: List[Dict[str, Any]]) -> str:
        """Generate markdown comment for PR with consolidated suggestions."""
        if not results:
            return """
## 🎉 PR Validation Results

No sequence files were changed in this PR.
"""
        
        # Count statistics
        total_files = len(results)
        valid_files = sum(1 for r in results if r['valid'])
        files_with_errors = sum(1 for r in results if r['errors'])
        files_with_suggestions = sum(1 for r in results if r['suggestions'])
        
        comment = f"""
## 🔍 PR Validation Results

**Files processed:** {total_files} | **Valid:** {valid_files} | **With errors:** {files_with_errors} | **With suggestions:** {files_with_suggestions}

"""
        
        # Add status for each file
        for result in results:
            file_name = Path(result['file']).name
            suggestions = result.get('suggestions', {})
            
            if result['valid'] and not result['errors']:
                status_icon = "✅"
                status_text = "Valid"
            else:
                status_icon = "❌" 
                status_text = "Issues found"
            
            comment += f"### {status_icon} `{file_name}` - {status_text}\n\n"
            
            # Add errors
            if result['errors']:
                comment += "**❌ Errors:**\n"
                for error in result['errors']:
                    comment += f"- {error}\n"
                comment += "\n"
            
            # Add warnings
            if result['warnings']:
                comment += "**⚠️ Warnings:**\n"
                for warning in result['warnings']:
                    comment += f"- {warning}\n"
                comment += "\n"
            
            # Handle complete template for files with no metadata
            if 'complete_template' in suggestions:
                comment += "**📝 Add Complete Metadata (Copy & Paste Ready):**\n\n"
                comment += "```yaml\n"
                for field, value in suggestions['complete_template'].items():
                    comment += f";@ {field}: {value}\n"
                comment += "```\n\n"
            
            # Handle missing required fields
            elif suggestions.get('missing_required'):
                missing_fields = suggestions['missing_required']
                suggested_metadata = suggestions.get('suggested_metadata', {})
                
                comment += f"**📋 Missing Required Fields ({len(missing_fields)}):**\n"
                comment += f"Add these to your existing metadata:\n\n"
                comment += "```yaml\n"
                for field in missing_fields:
                    value = suggested_metadata.get(field, '""')
                    comment += f";@ {field}: {value}\n"
                comment += "```\n\n"
            
            # Handle field improvements
            if suggestions.get('improvements'):
                comment += "**✨ Suggested Improvements:**\n"
                for improvement in suggestions['improvements']:
                    comment += f"- **{improvement['field']}**: {improvement['suggestion']}\n"
                    comment += f"  ```yaml\n  ;@ {improvement['field']}: {improvement['example']}\n  ```\n"
                comment += "\n"
            
            # Handle optional recommendations
            if suggestions.get('optional_recommendations'):
                optional_fields = suggestions['optional_recommendations']
                comment += f"**💡 Optional Fields for Better Discoverability:**\n"
                comment += f"Consider adding these fields (choose appropriate values for your sequence):\n\n"
                
                for field, info in optional_fields.items():
                    comment += f"**`{field}`**: {info['description']}\n"
                    if info['examples']:
                        examples_str = ', '.join(f"`{ex}`" for ex in info['examples'])
                        comment += f"  - Example values: {examples_str}\n"
                    else:
                        comment += f"  - Example: `;@ {field}: \"Your sequence description here\"`\n"
                    comment += "\n"
            
            comment += "---\n\n"
        
        # Add footer with helpful information
        author_display = self.repo_info['author_name']
        if self.repo_info['author_email'] != 'email@institution.edu':
            author_display += f" <{self.repo_info['author_email']}>"
        
        comment += f"""
## 📚 Resources

- **Schema documentation:** See the [current schema](https://github.com/{self.repo_info['name']}/blob/main/schemas/v0.0.1.yaml)
- **Contributing guide:** Check [CONTRIBUTING.md](https://github.com/{self.repo_info['name']}/blob/main/CONTRIBUTING.md)
- **Examples:** Browse existing sequences for annotation patterns

💡 **Need help?** Open an issue or check our contributing guidelines for detailed instructions.

---
*This validation was performed automatically. The suggestions above are meant to be helpful - not all are required for your PR to be accepted.*

**Detected contributor:** {author_display}
"""
        
        return comment

def main():
    validator = PRValidator()
    results = validator.validate_all_changed_files()
    comment = validator.generate_pr_comment(results)
    
    # Save comment to file for GitHub Action to use
    with open('pr_comment.md', 'w') as f:
        f.write(comment)
    
    # Print summary
    total_files = len(results)
    valid_files = sum(1 for r in results if r['valid'])
    print(f"Validated {total_files} files. {valid_files} valid, {total_files - valid_files} with issues.")
    
    # Exit with error code if there are validation errors (optional - you might want to allow PRs with suggestions)
    # has_errors = any(r['errors'] for r in results)
    # if has_errors:
    #     exit(1)

if __name__ == "__main__":
    main()
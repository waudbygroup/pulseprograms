#!/usr/bin/env python3
"""
Generate MkDocs documentation from NMR pulse sequence metadata.
"""
import os
import re
import yaml
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class SequenceParser:
    def __init__(self, sequences_dir: str = "sequences"):
        self.sequences_dir = Path(sequences_dir)
        self.sequences = {}
        
    def parse_sequence_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a sequence file and extract YAML metadata."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML metadata using regex
            yaml_pattern = r'^;@\s*(.+)$'
            yaml_lines = []
            
            for line in content.split('\n'):
                match = re.match(yaml_pattern, line)
                if match:
                    yaml_lines.append(match.group(1))
            
            if not yaml_lines:
                return None
            
            # Parse YAML
            yaml_content = '\n'.join(yaml_lines)
            metadata = yaml.safe_load(yaml_content)
            
            if not isinstance(metadata, dict):
                return None
            
            # Convert date objects to strings for consistency
            from datetime import date
            for key, value in metadata.items():
                if isinstance(value, date):
                    metadata[key] = value.isoformat()
            
            # Add file information
            metadata['_file_path'] = str(file_path)
            metadata['_file_name'] = file_path.name
            
            return metadata
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def get_git_history(self, file_path: Path) -> List[Dict[str, str]]:
        """Get Git commit history for a file."""
        try:
            cmd = [
                'git', 'log', '--follow', '--pretty=format:%H|%ai|%an|%ae|%s',
                str(file_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=file_path.parent.parent)
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|', 4)
                    if len(parts) == 5:
                        commits.append({
                            'hash': parts[0][:8],
                            'date': parts[1][:10],
                            'author': parts[2],
                            'email': parts[3],
                            'message': parts[4]
                        })
            return commits
        except Exception as e:
            print(f"Error getting Git history for {file_path}: {e}")
            return []
    
    def parse_all_sequences(self) -> Dict[str, Dict[str, Any]]:
        """Parse all sequence files in the sequences directory."""
        sequences = {}
        
        if not self.sequences_dir.exists():
            print(f"Sequences directory {self.sequences_dir} does not exist")
            return sequences
        
        for file_path in self.sequences_dir.iterdir():
            if file_path.is_file() and file_path.name != 'README.md':
                metadata = self.parse_sequence_file(file_path)
                if metadata:
                    # Add Git history
                    metadata['_git_history'] = self.get_git_history(file_path)
                    sequences[file_path.name] = metadata
                else:
                    print(f"No valid metadata found in {file_path}")
        
        return sequences

class DocumentationGenerator:
    def __init__(self, sequences: Dict[str, Dict[str, Any]]):
        self.sequences = sequences
        self.output_dir = Path("docs-generated")
        
    def generate_sequence_page(self, seq_name: str, metadata: Dict[str, Any]) -> str:
        """Generate markdown page for a single sequence."""
        title = metadata.get('title', seq_name)
        
        md_content = [
            f"# {title}",
            "",
            "## Metadata",
            ""
        ]
        
        # Basic information table
        basic_fields = ['schema_version', 'sequence_version', 'status', 'created', 'last_modified']
        md_content.extend([
            "| Field | Value |",
            "|-------|-------|"
        ])
        
        for field in basic_fields:
            if field in metadata:
                value = metadata[field]
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)
                md_content.append(f"| {field.replace('_', ' ').title()} | {value} |")
        
        # Authors
        if 'authors' in metadata:
            md_content.extend(["", "## Authors", ""])
            authors = metadata['authors']
            if isinstance(authors, list):
                for author in authors:
                    md_content.append(f"- {author}")
            else:
                md_content.append(f"- {authors}")
        
        # Experiment details
        exp_fields = ['experiment_type', 'features', 'nuclei_hint']
        for field in exp_fields:
            if field in metadata:
                md_content.extend([f"", f"## {field.replace('_', ' ').title()}", ""])
                value = metadata[field]
                if isinstance(value, list):
                    for item in value:
                        md_content.append(f"- {item}")
                else:
                    md_content.append(f"{value}")
        
        # Description
        if 'description' in metadata:
            md_content.extend(["", "## Description", "", metadata['description']])
        
        # Citations
        if 'citation' in metadata:
            md_content.extend(["", "## Citations", ""])
            citations = metadata['citation']
            if isinstance(citations, list):
                for citation in citations:
                    md_content.append(f"- {citation}")
            else:
                md_content.append(f"- {citations}")
        
        # DOIs
        if 'doi' in metadata:
            md_content.extend(["", "## DOIs", ""])
            dois = metadata['doi']
            if isinstance(dois, list):
                for doi in dois:
                    md_content.append(f"- [{doi}](https://doi.org/{doi})")
            else:
                md_content.append(f"- [{dois}](https://doi.org/{dois})")
        
        # Git history / changelog
        if '_git_history' in metadata and metadata['_git_history']:
            md_content.extend(["", "## Changelog", ""])
            for commit in metadata['_git_history']:
                md_content.append(f"- **{commit['date']}** ({commit['hash']}): {commit['message']} - {commit['author']}")
        
        # Repository link
        if 'repository' in metadata:
            repo = metadata['repository']
            file_name = metadata['_file_name']
            md_content.extend([
                "", "## Source", "",
                f"View source: [{repo}/sequences/{file_name}](https://{repo}/blob/main/sequences/{file_name})"
            ])
        
        return '\n'.join(md_content)
    
    def generate_sequence_database(self) -> str:
        """Generate searchable sequence database page."""
        md_content = [
            "# Sequence Database",
            "",
            "Browse all available NMR pulse sequences with their metadata.",
            "",
            "## Search and Filter",
            "",
            "Use the search box above or browse by experiment type below.",
            "",
            "## All Sequences",
            "",
            "| Sequence | Title | Type | Features | Nuclei | Status | Version |",
            "|----------|-------|------|----------|--------|--------|---------|"
        ]
        
        # Sort sequences by name
        for seq_name in sorted(self.sequences.keys()):
            metadata = self.sequences[seq_name]
            
            title = metadata.get('title', seq_name)
            exp_type = ', '.join(metadata.get('experiment_type', [])) if isinstance(metadata.get('experiment_type'), list) else metadata.get('experiment_type', '')
            features = ', '.join(metadata.get('features', [])) if isinstance(metadata.get('features'), list) else metadata.get('features', '')
            nuclei = ', '.join(metadata.get('nuclei_hint', [])) if isinstance(metadata.get('nuclei_hint'), list) else metadata.get('nuclei_hint', '')
            status = metadata.get('status', '')
            version = metadata.get('sequence_version', '')
            
            # Create link to sequence page
            link = f"[{seq_name}](sequences/{seq_name}.md)"
            
            md_content.append(f"| {link} | {title} | {exp_type} | {features} | {nuclei} | {status} | {version} |")
        
        # Group by experiment type
        exp_types = set()
        for metadata in self.sequences.values():
            if 'experiment_type' in metadata:
                if isinstance(metadata['experiment_type'], list):
                    exp_types.update(metadata['experiment_type'])
                else:
                    exp_types.add(metadata['experiment_type'])
        
        if exp_types:
            md_content.extend(["", "## By Experiment Type", ""])
            
            for exp_type in sorted(exp_types):
                md_content.extend([f"### {exp_type.upper()}", ""])
                
                for seq_name in sorted(self.sequences.keys()):
                    metadata = self.sequences[seq_name]
                    seq_exp_types = metadata.get('experiment_type', [])
                    if not isinstance(seq_exp_types, list):
                        seq_exp_types = [seq_exp_types]
                    
                    if exp_type in seq_exp_types:
                        title = metadata.get('title', seq_name)
                        status = metadata.get('status', '')
                        md_content.append(f"- [{seq_name}](sequences/{seq_name}.md) - {title} ({status})")
        
        return '\n'.join(md_content)
    
    def generate_all_docs(self):
        """Generate all documentation files."""
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "sequences").mkdir(exist_ok=True)
        
        # Generate individual sequence pages
        for seq_name, metadata in self.sequences.items():
            page_content = self.generate_sequence_page(seq_name, metadata)
            output_file = self.output_dir / "sequences" / f"{seq_name}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_content)
            print(f"Generated {output_file}")
        
        # Generate sequence database
        db_content = self.generate_sequence_database()
        db_file = self.output_dir / "database.md"
        with open(db_file, 'w', encoding='utf-8') as f:
            f.write(db_content)
        print(f"Generated {db_file}")

def main():
    print("Parsing sequences...")
    parser = SequenceParser()
    sequences = parser.parse_all_sequences()
    
    print(f"Found {len(sequences)} sequences with metadata")
    
    if sequences:
        print("Generating documentation...")
        generator = DocumentationGenerator(sequences)
        generator.generate_all_docs()
        print("Documentation generation complete!")
    else:
        print("No sequences found with valid metadata")

if __name__ == "__main__":
    main()
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
            
            # Extract all lines starting with ';@' and strip the prefix
            yaml_lines = []
            for line in content.split('\n'):
                if line.strip().startswith(';@'):
                    # Remove ';@' prefix but preserve indentation after it
                    if len(line.strip()) == 2:  # Just ';@' with no content
                        yaml_lines.append('')  # Empty line
                    else:
                        yaml_line = line.strip()[2:]  # Remove ';@'
                        if yaml_line.startswith(' '):
                            yaml_line = yaml_line[1:]  # Remove one space after ';@'
                        yaml_lines.append(yaml_line)
            
            if not yaml_lines:
                return None
            
            # Join all YAML lines and parse as a single block
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
        self.output_dir = Path("docs-generated/docs")
        
    def generate_sequence_page(self, seq_name: str, metadata: Dict[str, Any]) -> str:
        """Generate markdown page for a single sequence."""
        title = metadata.get('title', seq_name)
        
        md_content = [f"# {title}", ""]
        
        # 1.5. Version, status, last modified (compact info box)
        info_items = []
        if 'sequence_version' in metadata:
            info_items.append(f"**Version:** {metadata['sequence_version']}")
        if 'status' in metadata:
            status_emoji = {"experimental": "🧪", "beta": "🔬", "stable": "✅", "deprecated": "⚠️"}
            emoji = status_emoji.get(metadata['status'], "")
            info_items.append(f"**Status:** {emoji} {metadata['status']}")
        if 'last_modified' in metadata:
            info_items.append(f"**Last Modified:** {metadata['last_modified']}")
        
        if info_items:
            md_content.extend(["> " + " • ".join(info_items), ""])
        
        # 2. Description
        if 'description' in metadata:
            md_content.extend(["## Description", "", metadata['description'], ""])
        
        # 3. Experiment Type
        if 'experiment_type' in metadata:
            md_content.extend(["## Experiment Type", ""])
            exp_types = metadata['experiment_type']
            if isinstance(exp_types, list):
                type_badges = " ".join([f"`{t}`" for t in exp_types])
                md_content.extend([type_badges, ""])
            else:
                md_content.extend([f"`{exp_types}`", ""])
        
        # 4. Features
        if 'features' in metadata:
            md_content.extend(["## Features", ""])
            features = metadata['features']
            if isinstance(features, list):
                for feature in features:
                    md_content.append(f"- {feature}")
            else:
                md_content.append(f"- {features}")
            md_content.append("")
        
        # 5. Nuclei Hint
        if 'nuclei_hint' in metadata:
            md_content.extend(["## Nuclei", ""])
            nuclei = metadata['nuclei_hint']
            if isinstance(nuclei, list):
                nuclei_badges = " ".join([f"`{n}`" for n in nuclei])
                md_content.extend([nuclei_badges, ""])
            else:
                md_content.extend([f"`{nuclei}`", ""])
        
        # 6. Authors
        if 'authors' in metadata:
            md_content.extend(["## Authors", ""])
            authors = metadata['authors']
            if isinstance(authors, list):
                for author in authors:
                    md_content.append(f"- {author}")
            else:
                md_content.append(f"- {authors}")
            md_content.append("")
        
        # 7. Citation
        if 'citation' in metadata:
            md_content.extend(["## Citations", ""])
            citations = metadata['citation']
            if isinstance(citations, list):
                for citation in citations:
                    md_content.append(f"- {citation}")
            else:
                md_content.append(f"- {citations}")
            md_content.append("")
        
        # 8. DOI
        if 'doi' in metadata:
            md_content.extend(["## DOI Links", ""])
            dois = metadata['doi']
            if isinstance(dois, list):
                for doi in dois:
                    md_content.append(f"- [{doi}](https://doi.org/{doi})")
            else:
                md_content.append(f"- [{dois}](https://doi.org/{dois})")
            md_content.append("")
        
        # 9. Other fields (any field not in the ordered list above)
        displayed_fields = {
            'title', 'sequence_version', 'status', 'last_modified', 'description', 
            'experiment_type', 'features', 'nuclei_hint', 'authors', 'citation', 
            'doi', 'schema_version', 'created', 'repository'
        }
        
        other_fields = {k: v for k, v in metadata.items() if k not in displayed_fields}
        if other_fields:
            md_content.extend(["## Additional Fields", ""])
            md_content.extend([
                "| Field | Value |",
                "|-------|-------|"
            ])
            
            for field, value in sorted(other_fields.items()):
                field_name = field.replace('_', ' ').title()
                
                if isinstance(value, list):
                    if not value:  # Empty list
                        formatted_value = "*empty*"
                    elif isinstance(value[0], dict):  # List of objects
                        formatted_items = []
                        for item in value:
                            item_parts = [f"{k}: {v}" for k, v in item.items()]
                            formatted_items.append("{" + ", ".join(item_parts) + "}")
                        formatted_value = "<br>".join(formatted_items)
                    else:  # Simple list
                        formatted_value = "<br>".join([str(item) for item in value])
                elif isinstance(value, dict):  # Single object
                    item_parts = [f"{k}: {v}" for k, v in value.items()]
                    formatted_value = "{" + ", ".join(item_parts) + "}"
                else:  # Simple value
                    formatted_value = str(value)
                
                md_content.append(f"| {field_name} | {formatted_value} |")
            
            md_content.append("")
        
        # 10. Schema version and metadata info (at the end)
        md_content.extend(["---", ""])
        if 'created' in metadata:
            md_content.append(f"*Created: {metadata['created']}*")
        if 'repository' in metadata:
            md_content.append(f"*Repository: {metadata['repository']}*") 
        if 'schema_version' in metadata:
            md_content.append(f"*Schema version: {metadata['schema_version']}*")
        
        # Source code
        sequence_file_path = Path("sequences") / seq_name
        if sequence_file_path.exists():
            try:
                with open(sequence_file_path, 'r', encoding='utf-8') as f:
                    source_content = f.read()
                md_content.extend(["## Source Code", ""])
                
                # Add GitHub link if repository info available
                if 'repository' in metadata:
                    repo = metadata['repository']
                    md_content.append(f"View on GitHub: [{repo}/sequences/{seq_name}](https://{repo}/blob/main/sequences/{seq_name})")
                    md_content.append("")
                
                md_content.extend([
                    "```bruker",
                    source_content.rstrip(),
                    "```",
                    ""
                ])
            except Exception as e:
                print(f"Warning: Could not read source file {sequence_file_path}: {e}")
        
        # Git history / changelog
        if '_git_history' in metadata and metadata['_git_history']:
            md_content.extend(["## Changelog", ""])
            for commit in metadata['_git_history']:
                md_content.append(f"- **{commit['date']}** ({commit['hash']}): {commit['message']} - {commit['author']}")
        
        
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
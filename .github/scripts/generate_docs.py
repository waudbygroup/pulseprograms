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

        # Compact info line: version, status, last_modified, jump-to-source link
        info_items = []
        if 'sequence_version' in metadata:
            info_items.append(f"**Version** {metadata['sequence_version']}")
        if 'status' in metadata:
            status_emoji = {"experimental": "🧪", "beta": "🔬", "stable": "✅", "deprecated": "⚠️"}
            emoji = status_emoji.get(metadata['status'], "")
            info_items.append(f"**Status** {emoji} {metadata['status']}")
        if 'last_modified' in metadata:
            info_items.append(f"**Modified** {metadata['last_modified']}")
        info_items.append("[**Jump to source ↓**](#source-code)")
        md_content.extend([" · ".join(info_items), ""])

        # Description (no heading — keep tight)
        if 'description' in metadata:
            md_content.extend([metadata['description'].rstrip(), ""])

        # Compact summary table: experiment type / features / nuclei / authors / citations / DOIs
        summary_rows = []

        def _list_or_str(val, sep=", "):
            if isinstance(val, list):
                return sep.join(str(v) for v in val)
            return str(val)

        if 'experiment_type' in metadata:
            summary_rows.append(("Type", _list_or_str(metadata['experiment_type'])))
        if 'typical_nuclei' in metadata:
            summary_rows.append(("Nuclei", _list_or_str(metadata['typical_nuclei'])))
        if 'features' in metadata and metadata['features']:
            summary_rows.append(("Features", _list_or_str(metadata['features'])))
        if 'authors' in metadata:
            summary_rows.append(("Authors", _list_or_str(metadata['authors'], sep="; ")))
        if 'citation' in metadata:
            summary_rows.append(("Citation", _list_or_str(metadata['citation'], sep="; ")))
        if 'doi' in metadata:
            dois = metadata['doi'] if isinstance(metadata['doi'], list) else [metadata['doi']]
            doi_links = "; ".join([f"[{d}](https://doi.org/{d})" for d in dois])
            summary_rows.append(("DOI", doi_links))

        if summary_rows:
            md_content.append("| | |")
            md_content.append("|---|---|")
            for k, v in summary_rows:
                md_content.append(f"| **{k}** | {v} |")
            md_content.append("")

        # Structural fields (dimensions/acquisition_order/reference_pulse + experiment-specific blocks)
        # Rendered compactly as a definition-list-like table; excludes git/file metadata.
        excluded = {
            'title', 'sequence_version', 'status', 'last_modified', 'description',
            'experiment_type', 'features', 'typical_nuclei', 'authors', 'citation',
            'doi', 'schema_version', 'created', 'repository',
            '_git_history', '_file_path', '_file_name',
        }
        structural = {k: v for k, v in metadata.items() if k not in excluded}

        if structural:
            md_content.extend(["## Structure", "", "| Field | Value |", "|---|---|"])
            for field, value in structural.items():
                field_name = field.replace('_', ' ')
                md_content.append(f"| {field_name} | {self._format_value(value)} |")
            md_content.append("")

        # Source code
        sequence_file_path = Path("sequences") / seq_name
        if sequence_file_path.exists():
            try:
                with open(sequence_file_path, 'r', encoding='utf-8') as f:
                    source_content = f.read()
                md_content.extend(["## Source Code", ""])
                if 'repository' in metadata:
                    repo = metadata['repository']
                    md_content.extend([
                        f"[View on GitHub](https://{repo}/blob/main/sequences/{seq_name})",
                        "",
                    ])
                md_content.extend(["```bruker", source_content.rstrip(), "```", ""])
            except Exception as e:
                print(f"Warning: Could not read source file {sequence_file_path}: {e}")

        # Changelog (from git history)
        if metadata.get('_git_history'):
            md_content.extend(["## Changelog", ""])
            for commit in metadata['_git_history']:
                md_content.append(
                    f"- **{commit['date']}** ({commit['hash']}) — {commit['message']} — {commit['author']}"
                )
            md_content.append("")

        # Footer: created / repo / schema version (one line, italic)
        footer = []
        if 'created' in metadata:
            footer.append(f"Created {metadata['created']}")
        if 'repository' in metadata:
            footer.append(metadata['repository'])
        if 'schema_version' in metadata:
            footer.append(f"schema {metadata['schema_version']}")
        if footer:
            md_content.extend(["---", "", "*" + " · ".join(footer) + "*", ""])

        return '\n'.join(md_content)

    @staticmethod
    def _format_value(value):
        """Format a metadata value for inline rendering inside a table cell."""
        if isinstance(value, list):
            if not value:
                return "*empty*"
            if isinstance(value[0], dict):
                items = []
                for item in value:
                    items.append("{" + ", ".join(f"{k}: {v}" for k, v in item.items()) + "}")
                return "<br>".join(items)
            return ", ".join(str(item) for item in value)
        if isinstance(value, dict):
            return "{" + ", ".join(f"{k}: {v}" for k, v in value.items()) + "}"
        return str(value)
    
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
            nuclei = ', '.join(metadata.get('typical_nuclei', [])) if isinstance(metadata.get('typical_nuclei'), list) else metadata.get('typical_nuclei', '')
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
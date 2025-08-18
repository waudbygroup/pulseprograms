#!/usr/bin/env python3
"""
Generate schema documentation from YAML schema files.
"""
import yaml
from pathlib import Path

def generate_schema_docs():
    """Generate documentation for the current schema."""
    schema_dir = Path("schemas")
    output_dir = Path("docs-generated/schema")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read current schema
    current_schema_path = schema_dir / "current"
    if current_schema_path.is_symlink():
        schema_file = current_schema_path.resolve()
    else:
        schema_file = schema_dir / "v0.0.1.yaml"
    
    if not schema_file.exists():
        print(f"Schema file {schema_file} not found")
        return
    
    with open(schema_file, 'r') as f:
        schema = yaml.safe_load(f)
    
    # Generate markdown documentation
    md_content = [
        f"# Schema Documentation",
        "",
        f"**Version:** {schema.get('version', 'Unknown')}",
        "",
        schema.get('description', ''),
        "",
        "## Required Fields",
        ""
    ]
    
    required_fields = schema.get('required', [])
    properties = schema.get('properties', {})
    
    if required_fields:
        md_content.extend([
            "| Field | Type | Description |",
            "|-------|------|-------------|"
        ])
        
        for field in required_fields:
            if field in properties:
                prop = properties[field]
                field_type = prop.get('type', 'unknown')
                description = prop.get('description', '')
                md_content.append(f"| `{field}` | {field_type} | {description} |")
    
    # Optional fields
    optional_fields = [f for f in properties.keys() if f not in required_fields]
    if optional_fields:
        md_content.extend([
            "", "## Optional Fields", "",
            "| Field | Type | Description |",
            "|-------|------|-------------|"
        ])
        
        for field in optional_fields:
            prop = properties[field]
            field_type = prop.get('type', 'unknown')
            description = prop.get('description', '')
            md_content.append(f"| `{field}` | {field_type} | {description} |")
    
    # Controlled vocabularies
    md_content.extend([
        "", "## Controlled Vocabularies", ""
    ])
    
    # Status enum
    if 'status' in properties and 'enum' in properties['status']:
        status_values = properties['status']['enum']
        md_content.extend([
            "### Status Values", "",
            "| Value | Description |",
            "|-------|-------------|"
        ])
        for status in status_values:
            md_content.append(f"| `{status}` | - |")
    
    # Examples
    if 'examples' in schema:
        md_content.extend([
            "", "## Example", "",
            "```yaml"
        ])
        
        example = schema['examples'][0] if schema['examples'] else {}
        for key, value in example.items():
            if isinstance(value, list):
                md_content.append(f"{key}:")
                for item in value:
                    md_content.append(f"  - {item}")
            else:
                md_content.append(f"{key}: {value}")
        
        md_content.append("```")
    
    # Write schema documentation
    output_file = output_dir / "current.md"
    with open(output_file, 'w') as f:
        f.write('\n'.join(md_content))
    
    print(f"Generated schema documentation: {output_file}")

if __name__ == "__main__":
    generate_schema_docs()
import json
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom

def directory_to_dict(path):
    """Convert directory structure to dictionary using JSON/XML Export"""
    path = Path(path)
    d = {'name': path.name, 'type': 'directory'}
    
    try:
        items = list(path.iterdir())
        d['children'] = []
        
        for item in sorted(items, key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.is_dir():
                d['children'].append(directory_to_dict(item))
            else:
                d['children'].append({
                    'name': item.name,
                    'type': 'file',
                    'size': item.stat().st_size,
                    'modified': item.stat().st_mtime
                })
    except (PermissionError, OSError):
        d['children'] = ['Permission Denied']
    
    return d

def save_tree_json(start_path, output_file):
    """Save directory tree as JSON"""
    tree_dict = directory_to_dict(start_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tree_dict, f, indent=2, default=str)
    
    print(f"JSON tree saved to: {output_file}")

def save_tree_xml(start_path, output_file):
    """Save directory tree as XML"""
    def dict_to_xml(element, data):
        for key, value in data.items():
            if key == 'children' and isinstance(value, list):
                for child in value:
                    child_elem = ET.SubElement(element, 
                        'directory' if child.get('type') == 'directory' else 'file')
                    dict_to_xml(child_elem, child)
            elif isinstance(value, dict):
                child_elem = ET.SubElement(element, key)
                dict_to_xml(child_elem, value)
            else:
                element.set(key, str(value))
    
    tree_dict = directory_to_dict(start_path)
    root = ET.Element('directory_tree')
    dict_to_xml(root, tree_dict)
    
    # Pretty print
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"XML tree saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    start_dir = "."
    
    # Save as JSON
    save_tree_json(start_dir, "directory_tree.json")
    
    # Save as XML
    save_tree_xml(start_dir, "directory_tree.xml")
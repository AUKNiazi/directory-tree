#!/usr/bin/env python3
"""
Complete Directory Tree Generator - FIXED RICH TREE SAVING
Save as: directory_tree_generator.py
"""

import os
import sys
import json
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# ============================================================================
# METHOD 1: Basic Directory Tree using os.walk()
# ============================================================================
def generate_directory_tree(start_path, output_file=None, max_depth=None, save_to_file=True):
    """
    Generate a directory tree starting from start_path
    
    Args:
        start_path (str): Starting directory path
        output_file (str, optional): File to save the tree
        max_depth (int, optional): Maximum depth to traverse
        save_to_file (bool): Whether to save to file (default: True)
    """
    start_path = Path(start_path).resolve()
    
    if not start_path.exists():
        raise FileNotFoundError(f"Directory not found: {start_path}")
    
    tree_lines = []
    
    def walk_directory(current_path, prefix="", depth=0):
        if max_depth is not None and depth > max_depth:
            return
        
        try:
            items = sorted([item for item in current_path.iterdir()])
            
            for i, item in enumerate(items):
                is_last = (i == len(items) - 1)
                connector = "└── " if is_last else "├── "
                tree_lines.append(f"{prefix}{connector}{item.name}")
                
                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    walk_directory(item, prefix + extension, depth + 1)
                    
        except PermissionError:
            tree_lines.append(f"{prefix}└── [Permission Denied]")
    
    # Add header
    tree_lines.insert(0, "=" * 60)
    tree_lines.insert(0, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tree_lines.insert(0, f"Directory Tree for: {start_path}")
    tree_lines.append("=" * 60)
    
    tree_str = "\n".join(tree_lines)
    
    # Auto-generate filename if not provided but save_to_file is True
    if save_to_file and output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = start_path.name if start_path.name else "root"
        output_file = f"tree_{dir_name}_{timestamp}.txt"
    
    if output_file:
        # Add .txt extension if not present and not JSON/XML
        if not output_file.endswith(('.txt', '.json', '.xml')):
            output_file = f"{output_file}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree_str)
        
        print(f"✓ Directory tree saved to: {output_file}")
        print(f"  Path analyzed: {start_path}")
        
        # Show file size
        file_size = os.path.getsize(output_file)
        print(f"  File size: {file_size} bytes")
    
    # Always print to console as well
    if not save_to_file or output_file:
        print("\n" + "=" * 60)
        print("CONSOLE OUTPUT:")
        print("=" * 60)
        print(tree_str)
    
    return tree_str, output_file if output_file else None


# ============================================================================
# METHOD 2: Simple ASCII Tree with File Counts and Sizes
# ============================================================================
def generate_ascii_tree(start_path, output_file=None, show_hidden=False, max_depth=None):
    """
    Simple ASCII tree with file counts and sizes (NO EMOJIS)
    """
    start_path = Path(start_path).resolve()
    
    if not start_path.exists():
        raise FileNotFoundError(f"Directory not found: {start_path}")
    
    tree_lines = []
    total_dirs = 0
    total_files = 0
    total_size = 0
    
    def build_tree(current_path, prefix="", is_last=True, depth=0):
        nonlocal total_dirs, total_files, total_size
        
        if max_depth is not None and depth > max_depth:
            return
        
        try:
            # Get items
            items = list(current_path.iterdir())
            if not show_hidden:
                items = [item for item in items if not item.name.startswith('.')]
            
            # Sort: directories first, then files, both alphabetically
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for i, item in enumerate(items):
                is_last_item = (i == len(items) - 1)
                
                # Determine connector
                connector = ""
                if i == 0:
                    connector = "└── " if is_last else "├── "
                else:
                    connector = "    " if is_last else "│   "
                
                # Build the line
                line = f"{prefix}{connector}"
                
                if item.is_dir():
                    total_dirs += 1
                    line += "[D] "
                    
                    # Count contents of this directory
                    try:
                        dir_items = list(item.iterdir())
                        if not show_hidden:
                            dir_items = [di for di in dir_items if not di.name.startswith('.')]
                        
                        dir_files = sum(1 for di in dir_items if di.is_file())
                        dir_subdirs = sum(1 for di in dir_items if di.is_dir())
                        
                        line += f"{item.name}/ ({dir_files}f, {dir_subdirs}d)"
                    except:
                        line += f"{item.name}/ (?)"
                    
                    tree_lines.append(line)
                    
                    # Recurse into subdirectory
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    build_tree(item, next_prefix, is_last_item, depth + 1)
                    
                else:
                    total_files += 1
                    line += "[F] "
                    
                    # Get file size
                    try:
                        size = item.stat().st_size
                        total_size += size
                        
                        # Format size
                        if size == 0:
                            size_str = "empty"
                        elif size < 1024:
                            size_str = f"{size} B"
                        elif size < 1024 * 1024:
                            size_str = f"{size/1024:.1f} KB"
                        elif size < 1024 * 1024 * 1024:
                            size_str = f"{size/(1024*1024):.1f} MB"
                        else:
                            size_str = f"{size/(1024*1024*1024):.1f} GB"
                        
                        line += f"{item.name} ({size_str})"
                    except:
                        line += f"{item.name} (access denied)"
                    
                    tree_lines.append(line)
                    
        except PermissionError:
            tree_lines.append(f"{prefix}└── [Permission Denied]")
    
    # Add header
    tree_lines.insert(0, "=" * 60)
    tree_lines.insert(0, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tree_lines.insert(0, f"ASCII Tree for: {start_path}")
    
    # Build the tree
    build_tree(start_path)
    
    # Format total size
    if total_size == 0:
        total_size_str = "0 B"
    elif total_size < 1024:
        total_size_str = f"{total_size} B"
    elif total_size < 1024 * 1024:
        total_size_str = f"{total_size/1024:.1f} KB"
    elif total_size < 1024 * 1024 * 1024:
        total_size_str = f"{total_size/(1024*1024):.1f} MB"
    else:
        total_size_str = f"{total_size/(1024*1024*1024):.1f} GB"
    
    # Add summary
    tree_lines.append("")
    tree_lines.append("=" * 60)
    tree_lines.append("SUMMARY")
    tree_lines.append("=" * 60)
    tree_lines.append(f"Total directories: {total_dirs}")
    tree_lines.append(f"Total files: {total_files}")
    tree_lines.append(f"Total size: {total_size_str}")
    if max_depth is not None:
        tree_lines.append(f"Max depth: {max_depth}")
    tree_lines.append(f"Include hidden: {'Yes' if show_hidden else 'No'}")
    tree_lines.append("=" * 60)
    
    tree_str = "\n".join(tree_lines)
    
    # Auto-generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = start_path.name if start_path.name else "root"
        output_file = f"ascii_tree_{dir_name}_{timestamp}.txt"
    elif not output_file.endswith(('.txt', '.json', '.xml')):
        output_file = f"{output_file}.txt"
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(tree_str)
    
    print(f"✓ ASCII tree saved to: {output_file}")
    print(f"  Directories: {total_dirs}, Files: {total_files}, Size: {total_size_str}")
    
    # Always print to console
    print("\n" + "=" * 60)
    print("CONSOLE OUTPUT:")
    print("=" * 60)
    print(tree_str)
    
    return tree_str, output_file


# ============================================================================
# METHOD 3: Rich Tree Output - FIXED SAVING
# ============================================================================
def create_rich_directory_tree(start_path, output_file=None, max_depth=None):
    """
    Create a visually rich directory tree using rich library
    FIXED: Now properly saves to file
    """
    start_path = Path(start_path).resolve()
    
    # Auto-generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = start_path.name if start_path.name else "root"
        output_file = f"rich_tree_{dir_name}_{timestamp}.txt"
    elif not output_file.endswith(('.txt', '.json', '.xml')):
        output_file = f"{output_file}.txt"
    
    # Check if rich is available
    try:
        from rich import print as rprint
        from rich.tree import Tree
        from rich.console import Console
        from rich.text import Text
        from rich.style import Style
        rich_available = True
    except ImportError:
        rich_available = False
        print("⚠️  Rich library not installed. Install with: pip install rich")
        print("Falling back to enhanced ASCII tree...")
    
    if not rich_available:
        # Fallback to enhanced ASCII tree
        return generate_enhanced_tree(start_path, output_file, max_depth)
    
    # Create console with recording
    console = Console(record=True, width=120)
    tree = Tree(f"[bold bright_blue]{start_path.name}[/bold bright_blue]", 
                guide_style="bright_black")
    
    def build_tree(current_path, parent_node, current_depth=0):
        if max_depth is not None and current_depth >= max_depth:
            # Add indicator that depth was limited
            parent_node.add("[dim italic]... (depth limited)[/dim italic]")
            return
        
        try:
            items = sorted(current_path.iterdir(), 
                         key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in items:
                if item.is_dir():
                    # Create directory node
                    dir_label = f"[bold cyan]{item.name}[/bold cyan]"
                    
                    # Count items in directory
                    try:
                        dir_items = list(item.iterdir())
                        dir_files = sum(1 for di in dir_items if di.is_file())
                        dir_dirs = sum(1 for di in dir_items if di.is_dir())
                        count_label = f" [dim]({dir_files}f, {dir_dirs}d)[/dim]"
                        dir_label += count_label
                    except:
                        dir_label += " [red][?][/red]"
                    
                    dir_node = parent_node.add(dir_label)
                    build_tree(item, dir_node, current_depth + 1)
                    
                else:
                    # Create file node
                    try:
                        size = item.stat().st_size
                        if size == 0:
                            size_str = "[dim](empty)[/dim]"
                        elif size < 1024:
                            size_str = f"[dim]({size} B)[/dim]"
                        elif size < 1024 * 1024:
                            size_str = f"[dim]({size/1024:.1f} KB)[/dim]"
                        elif size < 1024 * 1024 * 1024:
                            size_str = f"[dim]({size/(1024*1024):.1f} MB)[/dim]"
                        else:
                            size_str = f"[dim]({size/(1024*1024*1024):.1f} GB)[/dim]"
                    except:
                        size_str = "[red](access denied)[/red]"
                    
                    file_label = f"[green]{item.name}[/green] {size_str}"
                    parent_node.add(file_label)
                    
        except PermissionError:
            parent_node.add("[red][Permission Denied][/red]")
    
    # Build the tree
    build_tree(start_path, tree)
    
    # Print to console (this captures it for saving)
    console.print(tree)
    
    # Add header information
    header = Text()
    header.append("\n" + "="*60 + "\n", style="bright_black")
    header.append("RICH DIRECTORY TREE\n", style="bold bright_white")
    header.append("="*60 + "\n", style="bright_black")
    header.append(f"Directory: {start_path}\n", style="bright_blue")
    header.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", style="dim")
    if max_depth is not None:
        header.append(f"Max Depth: {max_depth}\n", style="dim")
    header.append("="*60 + "\n\n", style="bright_black")
    
    # Get the tree as text
    tree_text = console.export_text()
    
    # Combine header and tree
    full_output = header.plain + tree_text
    
    # FIXED: Save to file using standard file writing
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("=" * 60 + "\n")
        f.write("RICH DIRECTORY TREE\n")
        f.write("=" * 60 + "\n")
        f.write(f"Directory: {start_path}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if max_depth is not None:
            f.write(f"Max Depth: {max_depth}\n")
        f.write("=" * 60 + "\n\n")
        
        # Write tree (strip ANSI codes for clean text file)
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_tree = ansi_escape.sub('', tree_text)
        f.write(clean_tree)
        
        # Add footer
        f.write("\n" + "=" * 60 + "\n")
        f.write("Note: Colors are only visible in terminal with rich support\n")
        f.write("=" * 60 + "\n")
    
    # Verify file was saved
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"\n✓ Rich tree saved to: {output_file}")
        print(f"  File size: {file_size} bytes")
        
        if file_size == 0:
            print("  ⚠️  WARNING: File is empty! Using fallback method...")
            # Try fallback
            return generate_enhanced_tree(start_path, output_file, max_depth)
    else:
        print(f"❌ ERROR: File was not created: {output_file}")
        # Try fallback
        return generate_enhanced_tree(start_path, output_file, max_depth)
    
    return output_file

def generate_enhanced_tree(start_path, output_file, max_depth=None):
    """
    Enhanced ASCII tree as fallback when rich has issues
    """
    start_path = Path(start_path).resolve()
    
    tree_lines = []
    total_dirs = 0
    total_files = 0
    total_size = 0
    
    def build_tree(current_path, prefix="", is_last=True, depth=0):
        nonlocal total_dirs, total_files, total_size
        
        if max_depth is not None and depth > max_depth:
            tree_lines.append(f"{prefix}└── ... (depth limited)")
            return
        
        try:
            items = sorted(current_path.iterdir(), 
                         key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for i, item in enumerate(items):
                is_last_item = (i == len(items) - 1)
                
                connector = ""
                if i == 0:
                    connector = "└── " if is_last else "├── "
                else:
                    connector = "    " if is_last else "│   "
                
                line = f"{prefix}{connector}"
                
                if item.is_dir():
                    total_dirs += 1
                    line += "📁 "
                    
                    try:
                        dir_items = list(item.iterdir())
                        dir_files = sum(1 for di in dir_items if di.is_file())
                        dir_dirs = sum(1 for di in dir_items if di.is_dir())
                        line += f"{item.name}/ ({dir_files}f, {dir_dirs}d)"
                    except:
                        line += f"{item.name}/ (?)"
                    
                    tree_lines.append(line)
                    
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    build_tree(item, next_prefix, is_last_item, depth + 1)
                    
                else:
                    total_files += 1
                    line += "📄 "
                    
                    try:
                        size = item.stat().st_size
                        total_size += size
                        
                        if size == 0:
                            size_str = "(empty)"
                        elif size < 1024:
                            size_str = f"({size} B)"
                        elif size < 1024 * 1024:
                            size_str = f"({size/1024:.1f} KB)"
                        elif size < 1024 * 1024 * 1024:
                            size_str = f"({size/(1024*1024):.1f} MB)"
                        else:
                            size_str = f"({size/(1024*1024*1024):.1f} GB)"
                        
                        line += f"{item.name} {size_str}"
                    except:
                        line += f"{item.name} (access denied)"
                    
                    tree_lines.append(line)
                    
        except PermissionError:
            tree_lines.append(f"{prefix}└── 🔒 [Permission Denied]")
    
    # Header
    tree_lines.insert(0, "=" * 60)
    tree_lines.insert(0, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tree_lines.insert(0, f"ENHANCED TREE for: {start_path}")
    
    # Build tree
    build_tree(start_path)
    
    # Format total size
    if total_size == 0:
        total_size_str = "0 B"
    elif total_size < 1024:
        total_size_str = f"{total_size} B"
    elif total_size < 1024 * 1024:
        total_size_str = f"{total_size/1024:.1f} KB"
    elif total_size < 1024 * 1024 * 1024:
        total_size_str = f"{total_size/(1024*1024):.1f} MB"
    else:
        total_size_str = f"{total_size/(1024*1024*1024):.1f} GB"
    
    # Summary
    tree_lines.append("")
    tree_lines.append("=" * 60)
    tree_lines.append("SUMMARY")
    tree_lines.append("=" * 60)
    tree_lines.append(f"Total directories: {total_dirs}")
    tree_lines.append(f"Total files: {total_files}")
    tree_lines.append(f"Total size: {total_size_str}")
    if max_depth is not None:
        tree_lines.append(f"Max depth: {max_depth}")
    tree_lines.append("=" * 60)
    
    tree_str = "\n".join(tree_lines)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(tree_str)
    
    print(f"✓ Enhanced tree saved to: {output_file}")
    print(f"  (Used fallback method - rich library had issues)")
    print(f"  Directories: {total_dirs}, Files: {total_files}, Size: {total_size_str}")
    
    # Print to console
    print("\n" + "=" * 60)
    print("CONSOLE OUTPUT:")
    print("=" * 60)
    print(tree_str)
    
    return output_file


# ============================================================================
# METHOD 4: Detailed Tree with File Counts and Sizes (with emojis)
# ============================================================================
def generate_detailed_tree(start_path, output_file=None, show_hidden=False, max_depth=None):
    """
    Detailed tree with file counts, sizes and emojis
    """
    start_path = Path(start_path).resolve()
    
    tree_lines = []
    dir_count = 0
    file_count = 0
    total_size = 0
    
    def process_directory(current_path, prefix="", is_last=True, current_depth=0):
        nonlocal dir_count, file_count, total_size
        
        if max_depth is not None and current_depth > max_depth:
            return
        
        try:
            items = list(current_path.iterdir())
            if not show_hidden:
                items = [item for item in items if not item.name.startswith('.')]
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for i, item in enumerate(items):
                is_last_item = (i == len(items) - 1)
                
                if i == 0:
                    connector = "└── " if is_last else "├── "
                else:
                    connector = "    " if is_last else "│   "
                
                if item.is_dir():
                    dir_count += 1
                    marker = "📁 "
                    
                    try:
                        sub_items = list(item.iterdir())
                        if not show_hidden:
                            sub_items = [si for si in sub_items if not si.name.startswith('.')]
                        file_count_in_dir = sum(1 for si in sub_items if si.is_file())
                        dir_count_in_dir = sum(1 for si in sub_items if si.is_dir())
                        count_info = f" ({file_count_in_dir} files, {dir_count_in_dir} dirs)"
                    except:
                        count_info = " [?]"
                    
                    tree_lines.append(f"{prefix}{connector}{marker}{item.name}{count_info}")
                    
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    process_directory(item, next_prefix, is_last_item, current_depth + 1)
                else:
                    file_count += 1
                    marker = "📄 "
                    
                    try:
                        size = item.stat().st_size
                        total_size += size
                        if size > 1024*1024*1024:
                            size_str = f" ({size/(1024*1024*1024):.2f} GB)"
                        elif size > 1024*1024:
                            size_str = f" ({size/(1024*1024):.2f} MB)"
                        elif size > 1024:
                            size_str = f" ({size/1024:.2f} KB)"
                        else:
                            size_str = f" ({size} bytes)"
                    except:
                        size_str = ""
                    
                    tree_lines.append(f"{prefix}{connector}{marker}{item.name}{size_str}")
                    
        except PermissionError:
            tree_lines.append(f"{prefix}└── 🔒 [Permission Denied]")
    
    tree_lines.append(f"📂 {start_path}")
    tree_lines.append("=" * 60)
    process_directory(start_path, "", True, 0)
    
    # Format total size
    if total_size > 1024*1024*1024:
        total_size_str = f"{total_size/(1024*1024*1024):.2f} GB"
    elif total_size > 1024*1024:
        total_size_str = f"{total_size/(1024*1024):.2f} MB"
    elif total_size > 1024:
        total_size_str = f"{total_size/1024:.2f} KB"
    else:
        total_size_str = f"{total_size} bytes"
    
    # Add summary
    tree_lines.append("\n" + "=" * 60)
    tree_lines.append(f"📊 SUMMARY")
    tree_lines.append("=" * 60)
    tree_lines.append(f"• Directories: {dir_count}")
    tree_lines.append(f"• Files: {file_count}")
    tree_lines.append(f"• Total Size: {total_size_str}")
    tree_lines.append(f"• Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tree_lines.append(f"• Path: {start_path}")
    if max_depth is not None:
        tree_lines.append(f"• Max Depth: {max_depth}")
    
    tree_str = "\n".join(tree_lines)
    
    # Auto-generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = start_path.name if start_path.name else "root"
        output_file = f"detailed_{dir_name}_{timestamp}.txt"
    elif not output_file.endswith(('.txt', '.json', '.xml')):
        output_file = f"{output_file}.txt"
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(tree_str)
    
    print(f"✓ Detailed tree saved to: {output_file}")
    print(f"  Directories: {dir_count}, Files: {file_count}, Size: {total_size_str}")
    
    # Always print to console as well
    print("\n" + "=" * 60)
    print("CONSOLE OUTPUT:")
    print("=" * 60)
    print(tree_str)
    
    return tree_str, output_file


# ============================================================================
# METHOD 5: JSON/XML Export
# ============================================================================
def directory_to_dict(path, max_depth=None, current_depth=0):
    """Convert directory structure to dictionary"""
    path = Path(path)
    d = {
        'name': path.name,
        'path': str(path),
        'type': 'directory',
        'size': 0,
        'modified': path.stat().st_mtime if path.exists() else 0
    }
    
    if max_depth is not None and current_depth >= max_depth:
        d['children'] = []
        return d
    
    try:
        items = list(path.iterdir())
        d['children'] = []
        
        for item in sorted(items, key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.is_dir():
                child_dict = directory_to_dict(item, max_depth, current_depth + 1)
                d['children'].append(child_dict)
                d['size'] += child_dict['size']
            else:
                try:
                    stat = item.stat()
                    child_dict = {
                        'name': item.name,
                        'path': str(item),
                        'type': 'file',
                        'size': stat.st_size,
                        'modified': stat.st_mtime
                    }
                    d['children'].append(child_dict)
                    d['size'] += stat.st_size
                except:
                    d['children'].append({
                        'name': item.name,
                        'type': 'file',
                        'error': 'Permission denied'
                    })
    except (PermissionError, OSError):
        d['children'] = [{'error': 'Permission denied'}]
    
    return d

def save_tree_json(start_path, output_file=None, max_depth=None):
    """Save directory tree as JSON"""
    start_path = Path(start_path).resolve()
    
    # Auto-generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = start_path.name if start_path.name else "root"
        output_file = f"tree_{dir_name}_{timestamp}.json"
    elif not output_file.endswith('.json'):
        output_file = f"{output_file}.json"
    
    tree_dict = directory_to_dict(start_path, max_depth)
    
    # Add metadata
    tree_dict['metadata'] = {
        'generated': datetime.now().isoformat(),
        'source_path': str(start_path),
        'max_depth': max_depth
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tree_dict, f, indent=2, default=str)
    
    print(f"✓ JSON tree saved to: {output_file}")
    print(f"  Path analyzed: {start_path}")
    
    # Show file info
    file_size = os.path.getsize(output_file)
    print(f"  File size: {file_size} bytes")
    
    return output_file

def save_tree_xml(start_path, output_file=None, max_depth=None):
    """Save directory tree as XML"""
    start_path = Path(start_path).resolve()
    
    # Auto-generate filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = start_path.name if start_path.name else "root"
        output_file = f"tree_{dir_name}_{timestamp}.xml"
    elif not output_file.endswith('.xml'):
        output_file = f"{output_file}.xml"
    
    def dict_to_xml(element, data):
        for key, value in data.items():
            if key == 'children' and isinstance(value, list):
                for child in value:
                    child_type = child.get('type', 'item')
                    child_elem = ET.SubElement(element, child_type)
                    dict_to_xml(child_elem, child)
            elif isinstance(value, dict):
                child_elem = ET.SubElement(element, key)
                dict_to_xml(child_elem, value)
            elif key not in ['type', 'children']:
                element.set(key, str(value))
    
    tree_dict = directory_to_dict(start_path, max_depth)
    root = ET.Element('directory_tree')
    root.set('generated', datetime.now().isoformat())
    root.set('path', str(start_path))
    root.set('max_depth', str(max_depth) if max_depth else 'unlimited')
    dict_to_xml(root, tree_dict)
    
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"✓ XML tree saved to: {output_file}")
    print(f"  Path analyzed: {start_path}")
    
    # Show file info
    file_size = os.path.getsize(output_file)
    print(f"  File size: {file_size} bytes")
    
    return output_file


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================
def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Generate directory tree structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Auto-generate filename for current dir
  %(prog)s /home/user                # Auto-generate filename for specified dir
  %(prog)s . -o my_tree              # Save as my_tree.txt
  %(prog)s . -f ascii                # ASCII tree with file counts
  %(prog)s . -f rich                 # Rich colored tree
  %(prog)s . -f json                 # Auto-generate JSON filename
  %(prog)s . -f detailed -d 3        # Detailed tree with depth limit 3
  %(prog)s . -a                      # Include hidden files
  %(prog)s --auto-all                # Generate ALL formats automatically
        """
    )
    
    parser.add_argument('path', nargs='?', default='.', 
                       help='Starting directory (default: current directory)')
    
    parser.add_argument('-o', '--output', 
                       help='Output file name (auto-adds extension if needed)')
    
    parser.add_argument('-d', '--depth', type=int,
                       help='Maximum depth to traverse')
    
    parser.add_argument('-a', '--all', action='store_true',
                       help='Include hidden files and directories')
    
    parser.add_argument('-f', '--format', 
                       choices=['basic', 'ascii', 'rich', 'detailed', 'json', 'xml', 'all'],
                       default='basic',
                       help='Output format (default: basic, "all" for all formats)')
    
    parser.add_argument('--auto-all', action='store_true',
                       help='Generate ALL output formats automatically')
    
    parser.add_argument('--test-rich', action='store_true',
                       help='Test rich library functionality')
    
    return parser.parse_args()

def test_rich_functionality():
    """Test if rich library works properly"""
    print("\n" + "="*60)
    print("TESTING RICH LIBRARY FUNCTIONALITY")
    print("="*60)
    
    try:
        from rich.console import Console
        console = Console(record=True)
        console.print("[bold green]✓ Rich library is installed[/bold green]")
        console.print("[blue]Testing console recording...[/blue]")
        
        # Test saving
        test_text = "Test rich output\nSecond line\nThird line"
        console.print(test_text)
        
        # Try to save
        import tempfile
        test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        test_filename = test_file.name
        test_file.close()
        
        # Try different saving methods
        print(f"\nTesting save methods...")
        
        # Method 1: console.save_text()
        try:
            console.save_text(test_filename)
            size1 = os.path.getsize(test_filename)
            print(f"  Method 1 (save_text): {size1} bytes")
        except Exception as e1:
            print(f"  Method 1 failed: {e1}")
        
        # Method 2: Manual export
        try:
            exported = console.export_text()
            with open(test_filename, 'w') as f:
                f.write(exported)
            size2 = os.path.getsize(test_filename)
            print(f"  Method 2 (export_text): {size2} bytes")
        except Exception as e2:
            print(f"  Method 2 failed: {e2}")
        
        # Cleanup
        os.unlink(test_filename)
        
        print(f"\n[bold]Rich test completed[/bold]")
        
    except ImportError as e:
        print(f"❌ Rich library not available: {e}")
        print("\nInstall it with: pip install rich")
    except Exception as e:
        print(f"❌ Rich test failed: {e}")

def generate_auto_filename(start_path, format_type):
    """Generate automatic filename based on directory and format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    start_path = Path(start_path).resolve()
    dir_name = start_path.name if start_path.name else "root"
    
    # Clean directory name for filename
    dir_name_clean = "".join(c for c in dir_name if c.isalnum() or c in ('-', '_')).rstrip()
    
    format_extensions = {
        'basic': '.txt',
        'ascii': '.txt',
        'rich': '.txt',
        'detailed': '.txt',
        'json': '.json',
        'xml': '.xml'
    }
    
    format_prefixes = {
        'basic': 'tree',
        'ascii': 'ascii_tree',
        'rich': 'rich_tree',
        'detailed': 'detailed_tree',
        'json': 'tree_data',
        'xml': 'tree_data'
    }
    
    prefix = format_prefixes.get(format_type, 'tree')
    ext = format_extensions.get(format_type, '.txt')
    
    return f"{prefix}_{dir_name_clean}_{timestamp}{ext}"

def generate_all_formats(start_path, depth=None, include_hidden=False):
    """Generate ALL output formats for the given directory"""
    start_path = Path(start_path).resolve()
    print(f"\n{'='*60}")
    print(f"GENERATING ALL FORMATS FOR: {start_path}")
    print(f"{'='*60}\n")
    
    formats = ['basic', 'ascii', 'detailed', 'json', 'xml']
    results = []
    
    for fmt in formats:
        print(f"📁 Generating {fmt.upper()} format...")
        
        try:
            if fmt == 'basic':
                _, filename = generate_directory_tree(start_path, None, depth)
            elif fmt == 'ascii':
                _, filename = generate_ascii_tree(start_path, None, include_hidden, depth)
            elif fmt == 'detailed':
                _, filename = generate_detailed_tree(start_path, None, include_hidden, depth)
            elif fmt == 'json':
                filename = save_tree_json(start_path, None, depth)
            elif fmt == 'xml':
                filename = save_tree_xml(start_path, None, depth)
            
            results.append((fmt, filename))
            print(f"   ✓ Saved as: {filename}\n")
            
        except Exception as e:
            print(f"   ✗ Error: {e}\n")
            results.append((fmt, f"ERROR: {e}"))
    
    # Try rich separately since it might have issues
    print(f"📁 Generating RICH format (may have issues)...")
    try:
        rich_file = create_rich_directory_tree(start_path, None, depth)
        results.append(('rich', rich_file))
        print(f"   ✓ Saved as: {rich_file}\n")
    except Exception as e:
        print(f"   ✗ Rich format failed: {e}\n")
        results.append(('rich', f"ERROR: {e}"))
    
    print(f"{'='*60}")
    print("SUMMARY OF GENERATED FILES:")
    print(f"{'='*60}")
    for fmt, filename in results:
        if filename and isinstance(filename, str) and not filename.startswith("ERROR"):
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                status = f"{file_size} bytes"
                if file_size == 0:
                    status = "⚠️  EMPTY FILE"
                print(f"  {fmt:10} - {filename} ({status})")
            else:
                print(f"  {fmt:10} - {filename} (FILE NOT CREATED)")
        else:
            print(f"  {fmt:10} - {filename}")
    
    return results

def main():
    """Main command line function"""
    args = parse_arguments()
    
    # Handle special test flag
    if args.test_rich:
        test_rich_functionality()
        return
    
    # Handle --auto-all flag
    if args.auto_all:
        generate_all_formats(args.path, args.depth, args.all)
        return
    
    # Handle 'all' format
    if args.format == 'all':
        generate_all_formats(args.path, args.depth, args.all)
        return
    
    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        # Auto-generate filename based on directory and format
        output_file = generate_auto_filename(args.path, args.format)
    
    print(f"\n{'='*60}")
    print(f"📁 DIRECTORY TREE GENERATOR")
    print(f"{'='*60}")
    print(f"📂 Analyzing: {args.path}")
    print(f"📄 Output: {output_file}")
    print(f"🎯 Format: {args.format}")
    if args.depth:
        print(f"📏 Max Depth: {args.depth}")
    if args.all:
        print(f"👁️  Including hidden files")
    print(f"{'='*60}\n")
    
    try:
        if args.format == 'basic':
            generate_directory_tree(args.path, output_file, args.depth)
            
        elif args.format == 'ascii':
            generate_ascii_tree(args.path, output_file, args.all, args.depth)
            
        elif args.format == 'rich':
            create_rich_directory_tree(args.path, output_file, args.depth)
            
        elif args.format == 'detailed':
            generate_detailed_tree(args.path, output_file, args.all, args.depth)
            
        elif args.format == 'json':
            save_tree_json(args.path, output_file, args.depth)
            
        elif args.format == 'xml':
            save_tree_xml(args.path, output_file, args.depth)
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except PermissionError:
        print(f"❌ Error: Permission denied for {args.path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    # Verify file was created
    print(f"\n{'='*60}")
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        if file_size > 0:
            print(f"✅ SUCCESS! File saved as: {output_file}")
            print(f"📁 Location: {os.path.abspath(output_file)}")
            print(f"📊 Size: {file_size} bytes")
        else:
            print(f"⚠️  WARNING: File created but empty: {output_file}")
            print(f"   The tree was displayed in terminal but not saved properly.")
            print(f"   Try using a different format like 'ascii' or 'basic'.")
    else:
        print(f"❌ ERROR: File was not created: {output_file}")
        print(f"   Try using a different format or check permissions.")
    
    print(f"{'='*60}")


# ============================================================================
# INTERACTIVE MODE
# ============================================================================
def interactive_mode():
    """Interactive mode for easy use"""
    print("\n" + "="*60)
    print("🌳 INTERACTIVE DIRECTORY TREE GENERATOR")
    print("="*60)
    
    # Get directory to analyze
    default_dir = "."
    dir_prompt = f"Enter directory to analyze (press Enter for current '{default_dir}'): "
    target_dir = input(dir_prompt).strip()
    if not target_dir:
        target_dir = default_dir
    
    # Check if directory exists
    if not os.path.exists(target_dir):
        print(f"\n❌ ERROR: Directory '{target_dir}' does not exist!")
        print("Please try again with a valid directory path.")
        return
    
    # Get format
    print("\nAvailable formats:")
    print("  1. Basic tree (simple ASCII)")
    print("  2. ASCII tree with file counts & sizes")
    print("  3. Rich tree (colored, may have save issues)")
    print("  4. Detailed tree (with emojis and sizes)")
    print("  5. JSON export (for data processing)")
    print("  6. XML export")
    print("  7. ALL formats (generates all of the above)")
    
    format_map = {
        '1': 'basic',
        '2': 'ascii',
        '3': 'rich',
        '4': 'detailed',
        '5': 'json',
        '6': 'xml',
        '7': 'all'
    }
    
    format_choice = input("\nChoose format (1-7, default 1): ").strip()
    if not format_choice:
        format_choice = '1'
    
    if format_choice not in format_map:
        print(f"Invalid choice. Using 'basic' format.")
        format_choice = '1'
    
    selected_format = format_map[format_choice]
    
    # Get depth limit
    depth_input = input("Maximum depth (press Enter for unlimited): ").strip()
    depth_limit = int(depth_input) if depth_input.isdigit() else None
    
    # Include hidden files?
    include_hidden = False
    if selected_format in ['basic', 'ascii', 'detailed', 'all']:
        hidden_input = input("Include hidden files? (y/N): ").strip().lower()
        include_hidden = hidden_input in ['y', 'yes']
    
    print(f"\n{'='*60}")
    print(f"📊 SETTINGS:")
    print(f"   Directory: {target_dir}")
    print(f"   Format: {selected_format}")
    print(f"   Max Depth: {'Unlimited' if depth_limit is None else depth_limit}")
    print(f"   Hidden Files: {'Yes' if include_hidden else 'No'}")
    print(f"{'='*60}\n")
    
    # Generate the tree
    try:
        if selected_format == 'all':
            generate_all_formats(target_dir, depth_limit, include_hidden)
        elif selected_format == 'basic':
            generate_directory_tree(target_dir, None, depth_limit)
        elif selected_format == 'ascii':
            generate_ascii_tree(target_dir, None, include_hidden, depth_limit)
        elif selected_format == 'rich':
            # Warn about potential issues
            print("⚠️  Note: Rich format may have file saving issues in some environments.")
            print("   If file is empty, try using 'ascii' or 'detailed' format instead.\n")
            create_rich_directory_tree(target_dir, None, depth_limit)
        elif selected_format == 'detailed':
            generate_detailed_tree(target_dir, None, include_hidden, depth_limit)
        elif selected_format == 'json':
            save_tree_json(target_dir, None, depth_limit)
        elif selected_format == 'xml':
            save_tree_xml(target_dir, None, depth_limit)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Interactive session completed!")
    print(f"{'='*60}")


# ============================================================================
# QUICK USAGE FUNCTIONS
# ============================================================================
def quick_tree(path="."):
    """Quick tree generation - auto-generates filename"""
    print(f"\n🌳 Generating quick tree for: {path}")
    tree_str, filename = generate_directory_tree(path)
    print(f"✓ Saved to: {filename}")
    return tree_str, filename

def quick_ascii_tree(path=".", include_hidden=False, depth=3):
    """Quick ASCII tree with counts"""
    print(f"\n📊 Generating ASCII tree for: {path}")
    tree_str, filename = generate_ascii_tree(path, None, include_hidden, depth)
    print(f"✓ Saved to: {filename}")
    return tree_str, filename

def reliable_tree(path=".", depth=None):
    """Most reliable tree generation (ASCII format)"""
    print(f"\n🔧 Generating reliable ASCII tree for: {path}")
    tree_str, filename = generate_ascii_tree(path, None, False, depth)
    print(f"✓ Reliably saved to: {filename}")
    return tree_str, filename


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    # Check for special commands
    if len(sys.argv) == 2 and sys.argv[1] == "--examples":
        print("\n" + "="*60)
        print("📚 EXAMPLE USAGE")
        print("="*60)
        print("\nFor reliable file saving, use ASCII or basic formats:")
        print("  python directory_tree_generator.py . -f ascii")
        print("  python directory_tree_generator.py . -f basic")
        print("\nIf rich format creates empty files, try:")
        print("  python directory_tree_generator.py . -f detailed")
        print("  python directory_tree_generator.py . --test-rich")
        print("="*60)
        sys.exit(0)
    
    # Check if arguments were passed (command line mode)
    if len(sys.argv) > 1:
        main()
    else:
        # Interactive mode
        interactive_mode()
    
    # Show helpful message
    print("\n💡 TIPS:")
    print("  • Use 'ascii' or 'basic' format for reliable file saving")
    print("  • Run with '--test-rich' to check rich library issues")
    print("  • Run with '--help' for all options")
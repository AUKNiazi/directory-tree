import os
from pathlib import Path

def generate_detailed_tree(start_path, output_file=None, show_hidden=False):
    """
    Generate detailed directory tree with Simple ASCII Tree with file counts and sizes
    """
    start_path = Path(start_path).resolve()
    
    tree_lines = []
    dir_count = 0
    file_count = 0
    
    def process_directory(current_path, prefix="", is_last=True):
        nonlocal dir_count, file_count
        
        try:
            # Get items, filter hidden if needed
            items = list(current_path.iterdir())
            if not show_hidden:
                items = [item for item in items if not item.name.startswith('.')]
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for i, item in enumerate(items):
                is_last_item = (i == len(items) - 1)
                
                # Determine connector
                if i == 0:
                    connector = "└── " if is_last else "├── "
                else:
                    connector = "    " if is_last else "│   "
                
                # Item representation
                if item.is_dir():
                    dir_count += 1
                    marker = "📁 "
                    # Count files in directory
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
                    
                    # Prepare next prefix
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    process_directory(item, next_prefix, is_last_item)
                else:
                    file_count += 1
                    marker = "📄 "
                    # Get file size
                    try:
                        size = item.stat().st_size
                        if size > 1024*1024:
                            size_str = f" ({size/(1024*1024):.1f} MB)"
                        elif size > 1024:
                            size_str = f" ({size/1024:.1f} KB)"
                        else:
                            size_str = f" ({size} bytes)"
                    except:
                        size_str = ""
                    
                    tree_lines.append(f"{prefix}{connector}{marker}{item.name}{size_str}")
                    
        except PermissionError:
            tree_lines.append(f"{prefix}└── 🔒 [Permission Denied]")
    
    # Start the tree
    tree_lines.append(f"📂 {start_path}")
    process_directory(start_path, "", True)
    
    # Add summary
    tree_lines.append("\n" + "="*50)
    tree_lines.append(f"Summary: {dir_count} directories, {file_count} files")
    
    tree_str = "\n".join(tree_lines)
    
    # Output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree_str)
        print(f"Directory tree saved to: {output_file}")
    else:
        print(tree_str)
    
    return tree_str

# Example usage
if __name__ == "__main__":
    generate_detailed_tree(".", "detailed_tree.txt")
    
    # Include hidden files
    generate_detailed_tree(".", "detailed_tree_all.txt", show_hidden=True)
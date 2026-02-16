import os
from pathlib import Path

def generate_directory_tree(start_path, output_file=None, max_depth=None):
    """
    Generate a directory tree starting from start_path
    
    Args:
        start_path (str): Starting directory path
        output_file (str, optional): File to save the tree. If None, prints to console
        max_depth (int, optional): Maximum depth to traverse. None for unlimited
    """
    start_path = Path(start_path).resolve()
    
    if not start_path.exists():
        raise FileNotFoundError(f"Directory not found: {start_path}")
    
    tree_lines = []
    
    def walk_directory(current_path, prefix="", depth=0):
        if max_depth is not None and depth > max_depth:
            return
        
        try:
            # Get all items in current directory
            items = sorted([item for item in current_path.iterdir()])
            
            for i, item in enumerate(items):
                # Determine if this is the last item
                is_last = (i == len(items) - 1)
                
                # Set the connector symbol
                connector = "└── " if is_last else "├── "
                
                # Add the current item
                tree_lines.append(f"{prefix}{connector}{item.name}")
                
                # If it's a directory, recurse
                if item.is_dir():
                    # Determine the next prefix
                    extension = "    " if is_last else "│   "
                    walk_directory(item, prefix + extension, depth + 1)
                    
        except PermissionError:
            tree_lines.append(f"{prefix}└── [Permission Denied]")
    
    # Add the root directory
    tree_lines.append(f"{start_path.name}/" if start_path.is_dir() else start_path.name)
    
    # Generate the tree
    walk_directory(start_path)
    
    # Create final tree string
    tree_str = "\n".join(tree_lines)
    
    # Output to file or console
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree_str)
        print(f"Directory tree saved to: {output_file}")
    else:
        print(tree_str)
    
    return tree_str

# Example usage
if __name__ == "__main__":
    # Generate tree for current directory
    generate_directory_tree(".", "directory_tree.txt")
    
    # With max depth
    generate_directory_tree(".", "directory_tree_shallow.txt", max_depth=2)
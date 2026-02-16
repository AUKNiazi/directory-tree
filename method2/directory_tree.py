# First install: pip install rich

from rich import print
from rich.tree import Tree
from rich.console import Console
from pathlib import Path

def create_rich_directory_tree(start_path, output_file=None, max_depth=None):
    """
    Create a visually rich directory tree using rich library
    
    Args:
        start_path (str): Starting directory path
        output_file (str, optional): File to save the tree
        max_depth (int, optional): Maximum depth to traverse
    """
    start_path = Path(start_path).resolve()
    
    console = Console(record=True)
    tree = Tree(f"[bold blue]{start_path.name}[/bold blue]")
    
    def build_tree(current_path, parent_node, current_depth=0):
        if max_depth is not None and current_depth >= max_depth:
            return
        
        try:
            items = sorted(current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in items:
                if item.is_dir():
                    # Directory node
                    dir_node = parent_node.add(f"[bold cyan]{item.name}[/bold cyan]")
                    build_tree(item, dir_node, current_depth + 1)
                else:
                    # File node
                    size = item.stat().st_size
                    size_str = f" ({size:,} bytes)" if size > 0 else " (empty)"
                    parent_node.add(f"[green]{item.name}[/green][dim]{size_str}[/dim]")
                    
        except PermissionError:
            parent_node.add("[red][Permission Denied][/red]")
    
    build_tree(start_path, tree)
    
    # Print to console
    console.print(tree)
    
    # Save to file if specified
    if output_file:
        console.save_text(output_file)
        print(f"Tree saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    create_rich_directory_tree(".", "rich_tree.txt", max_depth=3)
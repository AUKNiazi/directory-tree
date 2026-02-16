# Directory Tree Generator

A comprehensive Python tool for generating directory trees with multiple output formats and flexible configuration options.

## Features

- **Multiple Methods**: 5 different implementation approaches included
- **Multiple Output Formats**: Plain text, detailed, JSON, XML, and rich colorful output
- **Command Line Interface**: Easy-to-use CLI with comprehensive help
- **Interactive Mode**: Run without arguments for an interactive experience
- **Depth Control**: Limit tree depth to any level
- **Hidden Files**: Option to include hidden files and directories
- **File Statistics**: Calculate and display file sizes
- **Error Handling**: Graceful handling of permission errors and missing directories
- **Timestamps**: Automatic timestamp in outputs
- **Python Integration**: Import and use functions directly in your scripts

## Requirements

- Python 3.x
- Dependencies (see `requirements.txt`):
  - `rich==14.2.0` - For beautiful terminal output
  - `Pygments==2.19.2` - For syntax highlighting
  - `markdown-it-py==4.0.0` - Markdown parsing
  - `mdurl==0.1.2` - URL handling for markdown

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. The main script is `directory_tree_generator.py` - no additional installation needed.

## Usage

### Command Line

#### Basic Usage

```bash
# Display help
python directory_tree_generator.py --help

# Generate basic tree of current directory
python directory_tree_generator.py .

# Generate tree of specific directory
python directory_tree_generator.py /path/to/directory
```

#### With Options

```bash
# Limit depth
python directory_tree_generator.py /home/user/projects -d 3

# Generate detailed tree with all files
python directory_tree_generator.py . -f detailed -a

# Detailed output to file with hidden files included
python directory_tree_generator.py . -f detailed -a -o mytree.txt

# Export as JSON
python directory_tree_generator.py . -f json -o data.json

# Export as XML
python directory_tree_generator.py . -f xml -o data.xml

# Rich colorful output to file
python directory_tree_generator.py . -f rich -o colorful_tree.txt
```

### Interactive Mode

Run without arguments for an interactive experience:

```bash
python directory_tree_generator.py
```

You'll be prompted for:
- Directory to analyze
- Output format
- Output filename

### Python Integration

Import and use the functions in your Python scripts:

```python
# Import specific functions
from directory_tree_generator import generate_directory_tree, save_tree_json

# Generate a basic tree
generate_directory_tree(".", "my_tree.txt", max_depth=3)

# Save as JSON
save_tree_json("/home/user", "home_directory.json")

# Import everything
from directory_tree_generator import *

# Use utility functions
quick_tree(".", "simple_tree.txt")
analyze_project("/path/to/project")
```

## Output Formats

- **basic**: Simple text-based directory tree
- **detailed**: Includes file sizes and additional information
- **rich**: Colorful terminal-friendly output with Unicode characters
- **json**: Structured JSON format for programmatic use
- **xml**: XML format for data interchange

## Options

- `-d, --depth`: Maximum depth to traverse (default: unlimited)
- `-f, --format`: Output format (basic, detailed, rich, json, xml)
- `-o, --output`: Output file path (if not specified, prints to console)
- `-a, --all`: Include hidden files and directories

## Project Structure

```
directory_tree/
├── directory_tree_generator.py  # Main script with all 5 methods
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── usage_single_file.txt        # Usage documentation
├── test_commands.txt            # Example test commands
└── method1-5/                   # Individual method implementations
    ├── directory_tree.py
    └── ...
```

## Examples

### Generate a tree of current directory
```bash
python directory_tree_generator.py . -o current_tree.txt
```

### Analyze a project directory with limited depth
```bash
python directory_tree_generator.py /path/to/project -d 3 -f detailed -o project_structure.txt
```

### Export directory structure as JSON
```bash
python directory_tree_generator.py . -f json -o directory_structure.json
```

### Include all files including hidden ones
```bash
python directory_tree_generator.py . -a -o complete_tree.txt
```

## Error Handling

The tool includes built-in error handling for:
- Missing or inaccessible directories
- Permission denied errors
- Invalid file paths
- Circular symbolic links

## License

This project is provided as-is for educational and professional use. Give credit to Asmat Ullah Khan (GitHub: AUKNiazi)

## Support

For usage examples and more information, refer to `usage single file.txt` in the project directory.

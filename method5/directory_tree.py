#!/usr/bin/env python3
"""
Command-line directory tree generator
Usage: python directory_tree.py [path] [options]
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Generate directory tree')
    parser.add_argument('path', nargs='?', default='.', 
                       help='Starting directory (default: current directory)')
    parser.add_argument('-o', '--output', 
                       help='Output file name')
    parser.add_argument('-d', '--depth', type=int,
                       help='Maximum depth to traverse')
    parser.add_argument('-a', '--all', action='store_true',
                       help='Include hidden files and directories')
    parser.add_argument('-f', '--format', choices=['text', 'json', 'xml'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('-s', '--summary', action='store_true',
                       help='Show summary statistics')
    
    args = parser.parse_args()
    
    try:
        # Choose method based on format
        if args.format == 'json':
            from method4.method4 import save_tree_json
            output_file = args.output or 'directory_tree.json'
            save_tree_json(args.path, output_file)
            
        elif args.format == 'xml':
            from method4.method4 import save_tree_xml
            output_file = args.output or 'directory_tree.xml'
            save_tree_xml(args.path, output_file)
            
        else:  # text format
            from method3 import generate_detailed_tree
            output_file = args.output or 'directory_tree.txt'
            generate_detailed_tree(args.path, output_file, args.all)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python

import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Process some arguments.')

    # Define arguments
    parser.add_argument('-i', '--input', help='Input file', required=False)
    parser.add_argument('-o', '--output', help='Output file', required=False)
    parser.add_argument('-d', '--directory', help='Directory path', required=False)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('-D', '--debug', help='Debug mode', action='store_true')

    # Parse arguments
    args = parser.parse_args()

    # Example of how to use the arguments
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Directory: {args.directory}")
    print(f"Verbose: {'Yes' if args.verbose else 'No'}")
    print(f"Debug: {'Yes' if args.debug else 'No'}")

    # Add your processing logic here

if __name__ == "__main__":
    main()

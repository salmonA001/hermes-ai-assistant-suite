#!/usr/bin/env python3
"""
Script to display the AI poem stored in poem.txt
"""

def main():
    try:
        with open('poem.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print(content)
    except FileNotFoundError:
        print("Error: poem.txt not found in the current directory.")
        print("Please make sure poem.txt exists in the same folder as this script.")
    except Exception as e:
        print(f"Error reading poem.txt: {e}")

if __name__ == "__main__":
    main()
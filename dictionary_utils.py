import argparse
import json
import os
import sys

VOWELS = {"А", "Э", "Ջ", "О", "U", "Я", "И", "J", "Е", "У", "Σ", "Ю"}

def load_dictionary(path):
    if not os.path.exists(path):
        print(f"Error: File not found at '{path}'")
        sys.exit(1)
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON document.")
        sys.exit(1)

def swap_characters(path, find_char, replace_char):
    data = load_dictionary(path)
    target_categories = ["level0", "level1", "level2+"]
    changes_made = 0
    words_modified = 0
    
    for category in target_categories:
        if category in data:
            for item in data[category]:
                if "conlang" in item:
                    original_word = item["conlang"]
                    if find_char in original_word:
                        new_word = original_word.replace(find_char, replace_char)
                        item["conlang"] = new_word
                        
                        changes_made += original_word.count(find_char)
                        words_modified += 1
                        
    if words_modified > 0:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Success! Replaced {changes_made} occurrence(s) across {words_modified} word(s).")
    else:
        print(f"No occurrences of '{find_char}' found in conlang keys. No changes made.")

def validate_spelling(path):
    data = load_dictionary(path)
    target_categories = ["level0", "level1", "level2+"]
    violations_found = 0
    
    print(f"Scanning '{path}' for double vowels...")
    print("-" * 40)
    
    for category in target_categories:
        if category in data:
            for item in data[category]:
                conlang_word = item.get("conlang", "")
                
                # Check for any two consecutive vowels
                for i in range(len(conlang_word) - 1):
                    if conlang_word[i] in VOWELS and conlang_word[i+1] in VOWELS:
                        english_def = item.get("english", "No definition")
                        print(f"[{category}] {conlang_word} ({english_def})")
                        violations_found += 1
                        break # Move to the next word so we don't print the same word twice
                        
    print("-" * 40)
    if violations_found == 0:
        print("Great job! No double vowels found in the dictionary.")
    else:
        print(f"Found {violations_found} word(s) with double vowels.")

def main():
    parser = argparse.ArgumentParser(description="Dictionary utilities for Wordforge.")
    subparsers = parser.add_subparsers(dest="command", help="The utility to run")
    subparsers.required = True

    # 1. Swap Command
    parser_swap = subparsers.add_parser("swap", help="Replace characters in the 'conlang' keys")
    parser_swap.add_argument("path", help="Path to the dictionary.json file")
    parser_swap.add_argument("-f", "--find", required=True, help="Character(s) to find")
    parser_swap.add_argument("-r", "--replace", required=True, help="Character(s) to replace with")

    # 2. Validate Command
    parser_val = subparsers.add_parser("validate", help="Check dictionary for spelling violations (e.g. double vowels)")
    parser_val.add_argument("-d", "--dict", default="dictionary.json", help="Path to dictionary.json (default: dictionary.json)")

    args = parser.parse_args()

    if args.command == "swap":
        swap_characters(args.path, args.find, args.replace)
    elif args.command == "validate":
        validate_spelling(args.dict)

if __name__ == "__main__":
    main()
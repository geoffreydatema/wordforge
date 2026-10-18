import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Replace characters in the 'conlang' keys of Wordforge dictionary.json.")
    parser.add_argument("path", help="Path to the dictionary.json file")
    parser.add_argument("-f", "--find", required=True, help="Character(s) to find")
    parser.add_argument("-r", "--replace", required=True, help="Character(s) to replace with")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: File not found at '{args.path}'")
        sys.exit(1)
        
    try:
        with open(args.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON document.")
        sys.exit(1)
        
    target_categories = ["level0", "level1", "level2+"]
    changes_made = 0
    words_modified = 0
    
    for category in target_categories:
        if category in data:
            for item in data[category]:
                if "conlang" in item:
                    original_word = item["conlang"]
                    if args.find in original_word:
                        new_word = original_word.replace(args.find, args.replace)
                        item["conlang"] = new_word
                        
                        changes_made += original_word.count(args.find)
                        words_modified += 1
                        
    if words_modified > 0:
        with open(args.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Success! Replaced {changes_made} occurrence(s) across {words_modified} word(s).")
    else:
        print(f"No occurrences of '{args.find}' found in conlang keys. No changes made.")

if __name__ == "__main__":
    main()

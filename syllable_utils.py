import argparse
import json
import os
import sys
from pathlib import Path

CONSONANTS = [
        "Б",
        "В",
        "Г",
        "Δ",
        "Z",
        "К",
        "Λ",
        "М",
        "Н",
        "П",
        "Р",
        "С",
        "Т",
        "V",
        "Х",
        "Q",
        "Ь",
        "Ե",
        "Ж",
        "Ч",
        "Ш",
        "Θ",
        "D",
        "Ф",
        "F",
        "Ξ",
        "Ց",
        "Ц",
        "პ",
        "Щ",
        "დ",
        "ს",
        "Ը",
        "Է",
        "რ",
        "ձ"
    ]

VOWELS = [
        "А",
        "Э",
        "Ջ",
        "О",
        "U",
        "Я",
        "И",
        "J",
        "Е",
        "У",
        "Σ",
        "Ю"
    ]

DEFINITIONS = {
        "А": "a",
        "Э": "e",
        "Ջ": "i",
        "О": "o",
        "U": "u",
        "Я": "ay",
        "И": "ee",
        "J": "iy",
        "Е": "ow",
        "У": "oo",
        "Σ": "oe",
        "Ю": "ue",
        "Б": "b",
        "В": "v",
        "Г": "g",
        "Δ": "d",
        "Z": "z",
        "К": "k",
        "Λ": "l",
        "М": "m",
        "Н": "n",
        "П": "p",
        "Р": "r",
        "С": "s",
        "Т": "t",
        "V": "f",
        "Х": "kh",
        "Q": "w",
        "Ь": "y",
        "F": "rr",
        "Ց": "h",
        "Ե": "j",
        "Ж": "zh",
        "Ч": "ch",
        "Ш": "sh",
        "Θ": "th",
        "D": "dh",
        "Ф": "ng",
        "Ξ": "shch",
        "Ц": "ts",
        "პ": "st",
        "Щ": "sk",
        "დ": "sv",
        "ს": "ks",
        "Ը": "kr",
        "Է": "kv",
        "რ": "gr",
        "ձ": "dv"
    }

def get_file(path):
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
        
    if path.split(".")[-1] == "json":
        with open(path, "r", encoding="utf-8") as file:
            raw = file.read()
        dictionary = json.loads(raw)
        return dictionary
    
    elif path.split(".")[-1] == "txt":
        items = []
        with open(path, "r", encoding="utf-8") as file:
            items = [line.strip() for line in file if line.strip()]
            return items

def get_syllables(word):
    syllables = []
    remainder = word

    while len(remainder) > 0:
        if remainder[0] in CONSONANTS:
            syllable = ""
            remainder_position = 0
            while len(remainder) > 0:
                if len(remainder) > 1:
                    if remainder[remainder_position + 1] in CONSONANTS:
                        word_end = remainder[remainder_position + 1:]
                        consonant_cluster = True
                        for c in word_end:
                            if c in VOWELS:
                                consonant_cluster = False
                        if consonant_cluster:
                            syllable += remainder
                            remainder = ""
                            break # C+VC+
                    
                    if remainder[remainder_position] in VOWELS:
                        syllable += remainder[remainder_position]
                        remainder = remainder[1:]
                        break # C+V
                    
                syllable += remainder[remainder_position]
                remainder = remainder[1:]

            syllables.append(syllable)

        elif remainder[0] in VOWELS:
            syllable = remainder[0]
            remainder = remainder[1:]
            syllables.append(syllable)
            
        else:
            syllables.append(remainder[0])
            remainder = remainder[1:]
            
    return syllables

def count_syllables(dictionary):
    syllable_sets = []
    syllable_frequencies = {}

    for level in dictionary:
        for definition in dictionary.get(level):
            current_word = definition.get("conlang")
            syllable = get_syllables(current_word)
            syllable_sets.append(syllable)
            
            for s in syllable:
                if s in syllable_frequencies.keys():
                    syllable_frequencies[s] += 1
                else:
                    syllable_frequencies[s] = 1

    return (syllable_sets, syllable_frequencies)

def get_syllable_list(dictionary_path):
    dictionary = get_file(dictionary_path)
    count_result = count_syllables(dictionary)
    syllables = count_result[0]
    unsorted_frequencies = count_result[1]
    sorted_frequencies = dict(sorted(unsorted_frequencies.items(), key=lambda item: item[1], reverse=True))

    c = 0
    for f in sorted_frequencies.items():
        print(f"{f[0]}\t{f[1]}")
        c += 1
        if c == 128:
            print("----------------------------")

def rename_images_to_names(dir_path: str | Path, names: list[str]) -> bool:
    target_dir = Path(dir_path)

    png_files: list[Path] = [p for p in target_dir.iterdir() if p.suffix.lower() == ".png"]

    if len(png_files) != len(names):
        print(
            f"Error: Count mismatch! Found {len(png_files)} PNG files, "
            f"but provided {len(names)} names. Aborting."
        )
        return False

    temp_files: list[Path] = []
    for idx, file_path in enumerate(png_files):
        temp_path = file_path.with_name(f"_temp_{idx}{file_path.suffix}")
        file_path.rename(temp_path)
        temp_files.append(temp_path)

    for temp_path, new_name in zip(temp_files, names):
        final_path = temp_path.with_name(f"{new_name}{temp_path.suffix}")
        temp_path.rename(final_path)
        print(f"Renamed -> '{final_path.name}'")

    print("All files successfully reset and renamed!")
    return True

def romanize(text_path):
    shigeyed_syllables = get_file(text_path)
    romanized_syllables = []
    for syllable in shigeyed_syllables:
        romanized = ""
        for character in syllable:
            romanized += DEFINITIONS.get(character, character)
        romanized_syllables.append(romanized)
        
    print(romanized_syllables)

def generate_spec(input_file, output_file):
    syllables = get_file(input_file)
    if not isinstance(syllables, list):
        print("Error: Input file must contain a list of syllables on separate lines.")
        sys.exit(1)

    shigeyed_to_code = {}
    code_to_shigeyed = {}
    shigeyed_categories = {}

    for syllable in syllables:
        romanized = ""
        for char in syllable:
            romanized += DEFINITIONS.get(char, char)
            
        shigeyed_to_code[syllable] = romanized
        code_to_shigeyed[romanized] = syllable
        
        first_char = syllable[0]
        if first_char not in shigeyed_categories:
            shigeyed_categories[first_char] = []
        shigeyed_categories[first_char].append(syllable)

    # Sort categories by length (longest first) then alphabetically for greedy matching
    for key in shigeyed_categories:
        shigeyed_categories[key].sort(key=lambda x: (-len(x), x))

    output_data = {
        "characters": syllables,  # <--- Added the raw syllables list here!
        "shigeyed_to_code": shigeyed_to_code,
        "code_to_shigeyed": code_to_shigeyed,
        "shigeyed_categories": shigeyed_categories
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    print(f"Success! Generated '{output_file}' with {len(syllables)} parsed syllables.")

def main():
    parser = argparse.ArgumentParser(description="Conlang syllable utilities.")
    subparsers = parser.add_subparsers(dest="command", help="The utility to run")
    subparsers.required = True

    # 1. List Command
    parser_list = subparsers.add_parser("list", help="Extract and count syllables from a dictionary JSON")
    parser_list.add_argument("-d", "--dict", default="dictionary.json", help="Path to the dictionary JSON file (default: dictionary.json)")

    # 2. Romanize Command
    parser_romanize = subparsers.add_parser("romanize", help="Romanize syllables from a text file")
    parser_romanize.add_argument("-f", "--file", default="shigeyed_syllables.txt", help="Path to the syllables text file (default: shigeyed_syllables.txt)")

    # 3. Spec Command
    parser_spec = subparsers.add_parser("spec", help="Generate Shigeyed spec JSON from syllables text list")
    parser_spec.add_argument("-i", "--input", default="shigeyed_syllables.txt", help="Path to input syllables text file (default: shigeyed_syllables.txt)")
    parser_spec.add_argument("-o", "--output", default="temp_shigeyed_spec.json", help="Path to output spec JSON (default: temp_shigeyed_spec.json)")

    args = parser.parse_args()

    if args.command == "list":
        get_syllable_list(args.dict)
    elif args.command == "romanize":
        romanize(args.file)
    elif args.command == "spec":
        generate_spec(args.input, args.output)

if __name__ == "__main__":
    main()

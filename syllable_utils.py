import json
from pathlib import Path

# aэջohλиეεyδюбвгдzкямнпpcтvxqьμՑжчшθdфըբζцპსպէთრც

CONSONANTS = [
    "б", "в", "г", "д", "z", "к", "я", "м", "н", "п", "p", "c", "т", "v", "x", 
    "q", "ь", "μ", "ж", "ч", "ш", "θ", "d", "ф", "ը", "բ", "ζ", "Ց", "ц", "პ", 
    "ს", "պ", "է", "თ", "რ", "ც"
]

VOWELS = [
    "a", "э", "ջ", "o", "h", "λ", "и", "ე", "ε", "y", "δ", "ю"
]

DEFINITIONS = {
    "a": 'a',
    "э": 'e',
    "ջ": 'i',
    "o": 'o',
    "h": 'u',
    "λ": 'ay',
    "и": 'ee',
    "ე": 'eye',
    "ε": 'oh',
    "y": 'oo',
    "δ": 'oe',
    "ю": 'ue',
    "б": 'b',
    "в": 'v',
    "г": 'g',
    "д": 'd',
    "z": 'z',
    "к": 'k',
    "я": 'l',
    "м": 'm',
    "н": 'n',
    "п": 'p',
    "p": 'r',
    "c": 's',
    "т": 't',
    "v": 'f',
    "x": 'kh',
    "q": 'w',
    "ь": 'y',
    "μ": 'j',
    "ж": 'zh',
    "ч": 'ch',
    "ш": 'sh' ,
    "θ": 'th',
    "d": 'dh',
    "ф": 'ng',
    "ը": 'kr',
    "բ": 'rr',
    "ζ": 'sz',
    "Ց": 'h',
    "ц": 'ts',
    "პ": 'st',
    "ს": 'ks',
    "պ": 'sk',
    "է": 'kv',
    "თ": 'sv',
    "რ": 'zv',
    "ც": 'dv'
}

def get_file(path):
    if path.split(".")[-1] == "json":
        with open(path, "r", encoding="utf-8") as file:
            raw = file.read()
        dictionary = json.loads(raw)
        return dictionary
    
    elif path.split(".")[-1] == "txt":
        items = []
        with open(path, "r", encoding="utf-8") as file:
            items = [line.strip() for line in file]
            return items

def get_syllables(word):
    syllables = []
    remainder = word

    while len(remainder) > 0:

        if len(remainder) > 0:
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

        if len(remainder) > 0:
            if remainder[0] in VOWELS:
                syllable = remainder[0]
                remainder = remainder[1:]

                syllables.append(syllable)
    
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

def get_syllable_list():
    dictionary = get_file("dictionary.json")
    count_result = count_syllables(dictionary)
    syllables = count_result[0]
    unsorted_frequencies = count_result[1]
    sorted_frequencies = dict(sorted(unsorted_frequencies.items(), key=lambda item: item[1], reverse=True))

    # for s in syllables:
    #     print(s)

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

def romanize():
    shigeyed_syllables = get_file("shigeyed_syllables.txt")
    romanized_syllables = []
    for syllable in shigeyed_syllables:
        romanized = ""
        for character in syllable:
            romanized += DEFINITIONS[character]
        romanized_syllables.append(romanized)
    print(romanized_syllables)
    # rename_images_to_names("C:/Working/TezhnorAlphabet/syllabary", romanized_syllables)

if __name__ == "__main__":
    # get_syllable_list()
    romanize()

    #@! add shigeyed typing to wordforge

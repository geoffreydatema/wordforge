import json

# aэջohλиეεyδюбвгдzкямнпpcтvxqьμжчшθdфըբζՑцპსպէთრც

CONSONANTS = [
    "б", "в", "г", "д", "z", "к", "я", "м", "н", "п", "p", "c", "т", "v", "x", 
    "q", "ь", "μ", "ж", "ч", "ш", "θ", "d", "ф", "ը", "բ", "ζ", "Ց", "ц", "პ", 
    "ს", "պ", "է", "თ", "რ", "ც"
]

VOWELS = [
    "a", "э", "ջ", "o", "h", "λ", "и", "ე", "ε", "y", "δ", "ю"
]

def get_file(path):
    with open(path, "r", encoding="utf-8") as file:
        raw = file.read()
    dictionary = json.loads(raw)
    return dictionary

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
                syllable = ""
                remainder_position = 0
                while len(remainder) > 0:
                    if remainder[remainder_position] in VOWELS:
                        if len(remainder) > 1:
                            if remainder[remainder_position + 1] in VOWELS:
                                syllable += remainder[remainder_position]
                                remainder = remainder[1:]
                                break # V
                        else:
                            syllable += remainder[remainder_position]
                            remainder = remainder[1:]
                            break # V at end of word

                        syllable += remainder[remainder_position]
                        remainder = remainder[1:]

                    elif remainder[remainder_position] in CONSONANTS:
                        if len(remainder) > 1:
                            if remainder[remainder_position + 1] in VOWELS:
                                syllable += remainder[remainder_position]
                                remainder = remainder[1:]
                                break # VC+
                            
                        else:
                            syllable += remainder[remainder_position]
                            remainder = remainder[1:]
                            break # VC+ at end of word

                        syllable += remainder[remainder_position]
                        remainder = remainder[1:]


                syllables.append(syllable)
    
    return syllables

def count_syllables(dictionary):
    syllable_frequencies = {}
    for level in dictionary:
        for definition in dictionary.get(level):
            current_word = definition.get("conlang")
            syllables = get_syllables(current_word)
            for s in syllables:
                if s in syllable_frequencies.keys():
                    syllable_frequencies[s] += 1
                else:
                    syllable_frequencies[s] = 1

    return syllable_frequencies

def get_syllable_list():
    dictionary = get_file("dictionary.json")
    unsorted_frequencies = count_syllables(dictionary)
    sorted_frequencies = dict(sorted(unsorted_frequencies.items(), key=lambda item: item[1]))

    for f in sorted_frequencies.items():
        print(f"{f[0]}\t{f[1]}")

if __name__ == "__main__":
    get_syllable_list()

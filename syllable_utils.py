import json

# aэջohλиეεyδюбвгдzкямнпpcтvxqьμжчшθdфըբζՑцპსպէთრც

CONSONANTS = [
    "б", "в", "г", "д", "z", "к", "я", "м", "н", "п", "p", "c", "т", "v", "x", 
    "q", "ь", "μ", "ж", "ч", "ш", "θ", "d", "ф", "ը", "բ", "ζ", "Ց", "ц", "პ", 
    "ს", "պ", "է", "თ", "რ"
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
    syllable = ""
    position = 0
    while position < len(word):
        character = word[position]

        # C+V
        if character in CONSONANTS:
            print("found c")
            # pass in word, return (word remainder, syllable)

        # V
        if character in VOWELS:
            print("found v")
            # pass in word, return (word remainder, syllable)

            # for this branch, it could be V or VC+

        position += 1

def count_syllables(dictionary):
    for level in dictionary:
        for definition in dictionary.get(level):
            current_word = definition.get("conlang")
            syllables = get_syllables(current_word)

            break
        break

def get_syllable_list():
    syllable_list = []

    dictionary = get_file("dictionary.json")
    count_syllables(dictionary)

    return syllable_list

if __name__ == "__main__":
    syllables = get_syllable_list()
    print(syllables)

import sys
import json
import os
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTabWidget, QLineEdit, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QMessageBox, QGridLayout, QFrame, QLabel, QTextEdit,
                               QSlider, QTextBrowser, QMenu) # --- ADDED QMenu ---
from PySide6.QtGui import QFont, QColor, QTextCursor
from PySide6.QtCore import Qt, QObject, QEvent, Signal

# ========================================================
#       MASTER CHARACTER DEFINITIONS
#
#       aэջohλиეբюռըδεyбвгдzкηмнпpcтvxզьμжчшяdфՑцპსպէთრც
# ========================================================

class DEFINITIONS:
    a = 'a'     # short a
    э = 'e'     # short e
    ջ = 'i'     # short i
    o = 'o'     # short o
    h = 'u'     # short u
    λ = 'ay'    # long a
    и = 'ee'    # long e
    ე = 'eye'   # long i
    բ = 'oi'    # oi as in boy
    ю = 'ui'    # anglicised ы
    ռ = 'ow'    # ow as in ouch
    ը = 'ew'    # ew as in knew
    δ = 'oe'    # oe as in book
    ε = 'oh'    # long o
    y = 'oo'    # oo as in poop
    б = 'b'
    в = 'v'
    г = 'g'
    д = 'd'
    z = 'z'
    к = 'k'
    η = 'l' 
    м = 'm'
    н = 'n'
    п = 'p'
    p = 'r'
    c = 's'
    т = 't'
    v = 'f'
    x = 'h'
    զ = 'w'
    ь = 'y'
    μ = 'j'
    ж = 'zh'    # as in measure
    ч = 'ch'
    ш = 'sh'
    я = 'th'    # unvoiced th
    d = 'TH'    # voiced th
    ф = 'ng'    # velar nasal
    Ց = 'tr'
    ц = 'ts'
    პ = 'st'
    ს = 'ks'
    պ = 'sk'
    է = 'kv'
    თ = 'sv'
    რ = 'zv'
    ც = 'dv'
    カ = 'ka'
    キ = 'kee'
    ク = 'koo'
    ケ = 'ke'
    コ = 'ko'
    サ = 'sa'
    ス = 'soo'
    セ = 'se'
    ソ = 'so'
    タ = 'ta'
    チ = 'tee'
    ツ = 'too'
    テ = 'te'
    ト = 'to'
    ナ = 'na'
    ニ = 'nee'
    ヌ = 'noo'
    ネ = 'ne'
    ノ = 'no'
    ハ = 'ha'
    ヒ = 'hee'
    フ = 'hoo'
    ヘ = 'he'
    ホ = 'ho'
    マ = 'ma'
    ミ = 'mee'
    ム = 'moo'
    メ = 'me'
    モ = 'mo'
    ヤ = 'ya'
    ユ = 'yoo'
    ヨ = 'yo'
    ラ = 'ra'
    リ = 'ree'
    ル = 'roo'
    レ = 're'
    ロ = 'ro'
    ワ = 'wa'
    ヲ = 'wo'
    ガ = 'ga'
    ギ = 'gee'
    グ = 'goo'
    ゲ = 'ge'
    ゴ = 'go'
    ザ = 'za'
    ジ = 'zee'
    ズ = 'zoo'
    ゼ = 'ze'
    ゾ = 'zo'
    ダ = 'da'
    ヂ = 'dee'
    ヅ = 'doo'
    デ = 'de'
    ド = 'do'
    バ = 'ba'
    ビ = 'bee'
    ブ = 'boo'
    ベ = 'be'
    ボ = 'bo'
    パ = 'pa'
    ピ = 'pee'
    プ = 'poo'
    ペ = 'pe'
    ポ = 'po'

class LORE:
    a = 'a'
    e = 'э'
    i = 'ջ'
    o = 'o'
    u = 'h'
    A = 'λ'
    E = 'и'
    I = 'ე'
    O = 'բ'
    U = 'ю'
    AU = 'ռ'
    EU = 'ը'
    OE = 'δ'
    OU = 'ε'
    OO = 'y'
    B = 'б'
    V = 'в'
    G = 'г'
    D = 'д'
    Z = 'z'
    K = 'ᴋ'
    L = 'η' 
    M = 'м'
    N = 'н'
    P = 'п'
    R = 'p'
    C = 'c'
    T = 'т'
    F = 'v'
    X = 'x'
    W = 'զ'
    Y = 'ь'
    J = 'μ'
    ZH = 'ж'
    CH = 'ч'
    SH = 'ш'
    TH = 'я'
    DH = 'd'
    NG = 'ф'
    TR = 'Ց'
    TS = 'ц'
    ST = 'პ'
    KS = 'ს'
    SK = 'պ'
    KV = 'է'
    SV = 'თ'
    ZV = 'რ'
    DV = 'ც'

class PRONUNCIATION:
    a = 'a'     # short a
    e = 'e'     # short e
    i = 'i'     # short i
    o = 'o'     # short o
    u = 'u'     # short u
    A = 'ay'    # long a
    E = 'ee'    # long e
    I = 'eye'   # long i
    O = 'oi'    # oi as in boy
    U = 'ui'    # anglicised ы
    AU = 'ow'   # ow as in ouch
    EU = 'ew'   # ew as in knew
    OE = 'oe'   # oe as in book
    OU = 'oh'   # long o
    OO = 'oo'   # oo as in poop
    B = 'b'
    V = 'v'
    G = 'g'
    D = 'd'
    Z = 'z'
    K = 'k'
    L = 'l' 
    M = 'm'
    N = 'n'
    P = 'p'
    R = 'r'
    C = 's'
    T = 't'
    F = 'f'
    X = 'h'
    W = 'w'
    Y = 'y'
    J = 'j'
    ZH = 'zh'   # as in measure
    CH = 'ch'
    SH = 'sh'
    TH = 'th'   # unvoiched th as in think
    DH = 'TH'   # voiced th as in this
    NG = 'ng'   # anglophone ng sound used in the ing word ending
    TR = 'tr'
    TS = 'ts'
    ST = 'st'
    KS = 'ks'
    SK = 'sk'
    KV = 'kv'
    SV = 'sv'
    ZV = 'zv'
    DV = 'dv'

# ==========================================
#           LORE CONFIGURATION
# ==========================================

VOWELS = [
    LORE.a, LORE.e, LORE.i, LORE.o, LORE.u, 
    LORE.A, LORE.E, LORE.I, LORE.O, LORE.U, 
    LORE.AU, LORE.EU, LORE.OU, LORE.OO, LORE.OE
]

CONSONANTS = [
    LORE.W, LORE.P, LORE.T, LORE.B, LORE.R, LORE.C, LORE.D, LORE.F, LORE.G, 
    LORE.X, LORE.J, LORE.K, LORE.L, LORE.Z, LORE.V, LORE.Y, LORE.N, LORE.M, 
    LORE.ZH, LORE.CH, LORE.SH, LORE.TH, LORE.DH, LORE.NG, LORE.TR,
    LORE.TS, LORE.ST, LORE.KS, LORE.SK, LORE.KV, LORE.SV, LORE.ZV, LORE.DV
]

ALPHABET_DEFS = [
    (LORE.a, "a", "short a"),
    (LORE.e, "e", "short e"),
    (LORE.i, "i", "short i"),
    (LORE.o, "o", "short o"),
    (LORE.u, "u", "short u"),
    (LORE.A, "ay", "long a"),
    (LORE.E, "ee", "long e"),
    (LORE.I, "eye", "long i"),
    (LORE.O, "oi", "oi as in boy"),
    (LORE.U, "ui", "anglicised ы"),
    (LORE.AU, "ow", "ow as in ouch"),
    (LORE.EU, "ew", "ew as in knew"),
    (LORE.OE, "oe", "oe as in book"),
    (LORE.OU, "oh", "long o"),
    (LORE.OO, "oo", "oo as in poop"),
    (LORE.B, "b", ""),
    (LORE.V, "v", ""),
    (LORE.G, "g", ""),
    (LORE.D, "d", ""),
    (LORE.Z, "z", ""),
    (LORE.K, "k", ""),
    (LORE.L, "l", ""),
    (LORE.M, "m", ""),
    (LORE.N, "n", ""),
    (LORE.P, "p", ""),
    (LORE.R, "r", ""),
    (LORE.C, "s", ""),
    (LORE.T, "t", ""),
    (LORE.F, "f", ""),
    (LORE.X, "h", ""),
    (LORE.W, "w", ""),
    (LORE.Y, "y", ""),
    (LORE.J, "j", ""),
    (LORE.ZH, "zh", "as in measure"),
    (LORE.CH, "ch", ""),
    (LORE.SH, "sh", ""),
    (LORE.TH, "th", "unvoiced th as in think"),
    (LORE.DH, "TH", "voiced th as in this"),
    (LORE.NG, "ng", "anglophone ng sound used in the ing word ending"),
    (LORE.TS, "ts", ""),
    (LORE.TR, "tr", ""),
    (LORE.ST, "st", ""),
    (LORE.KS, "ks", ""),
    (LORE.SK, "sk", ""),
    (LORE.KV, "kv", ""),
    (LORE.SV, "sv", ""),
    (LORE.ZV, "zv", ""),
    (LORE.DV, "dv", ""),
]

LORE_TO_PRON = {}
for attr in dir(LORE):
    if not attr.startswith('__') and not callable(getattr(LORE, attr)):
        lore_val = getattr(LORE, attr)
        if hasattr(PRONUNCIATION, attr):
            pron_val = getattr(PRONUNCIATION, attr)
            LORE_TO_PRON[lore_val] = pron_val

GLOBAL_KATAKANA_HEADER_SIZE = "24px"
GLOBAL_KATAKANA_TABLE_SIZE = "10pt"

TABLE_SIZE_CORRECTIONS = {}
HEADER_SIZE_CORRECTIONS = {}

KEYBOARD_LAYOUT = [
    [('w', LORE.W), ('e', LORE.e), ('r', LORE.R), ('t', LORE.T), ('y', LORE.Y), ('u', LORE.u), ('i', LORE.i), ('o', LORE.o), ('p', LORE.P)],
    [('a', LORE.a), ('s', LORE.C), ('d', LORE.D), ('f', LORE.F), ('g', LORE.G), ('h', LORE.X), ('j', LORE.J), ('k', LORE.K), ('l', LORE.L)],
    [('z', LORE.Z), ('v', LORE.V), ('b', LORE.B), ('n', LORE.N), ('m', LORE.M)]
]

LONG_VOWEL_MAP = {
    "a": LORE.A, "e": LORE.E, "i": LORE.I, "o": LORE.O, "u": LORE.U
}

COMBO_MAP = {
    "au": LORE.AU, "eu": LORE.EU, "ou": LORE.OU, "oo": LORE.OO, "oe": LORE.OE,
    "zh": LORE.ZH, "sh": LORE.SH, "kh": LORE.CH, 
    "th": LORE.TH, "dh": LORE.DH, "ng": LORE.NG, "tr": LORE.TR, 
    "ts": LORE.TS, "st": LORE.ST, "ks": LORE.KS, "sk": LORE.SK,
    "kv": LORE.KV, "sv": LORE.SV, "zv": LORE.ZV, "dv": LORE.DV
}

DISABLED_KEYS = ['q', 'x', 'c']

# ==========================================
#          KATAKANA CONFIGURATION
# ==========================================
KATAKANA_MAP = {
    LORE.K + LORE.a: 'カ', LORE.K + LORE.E: 'キ', LORE.K + LORE.OO: 'ク', LORE.K + LORE.e: 'ケ', LORE.K + LORE.o: 'コ',
    LORE.C + LORE.a: 'サ', LORE.C + LORE.OO: 'ス', LORE.C + LORE.e: 'セ', LORE.C + LORE.o: 'ソ', 
    LORE.T + LORE.a: 'タ', LORE.T + LORE.E: 'チ', LORE.T + LORE.OO: 'ツ', LORE.T + LORE.e: 'テ', LORE.T + LORE.o: 'ト',
    LORE.N + LORE.a: 'ナ', LORE.N + LORE.E: 'ニ', LORE.N + LORE.OO: 'ヌ', LORE.N + LORE.e: 'ネ', LORE.N + LORE.o: 'ノ',
    LORE.X + LORE.a: 'ハ', LORE.X + LORE.E: 'ヒ', LORE.X + LORE.OO: 'フ', LORE.X + LORE.e: 'ヘ', LORE.X + LORE.o: 'ホ',
    LORE.M + LORE.a: 'マ', LORE.M + LORE.E: 'ミ', LORE.M + LORE.OO: 'ム', LORE.M + LORE.e: 'メ', LORE.M + LORE.o: 'モ',
    LORE.Y + LORE.a: 'ヤ', LORE.Y + LORE.OO: 'ユ', LORE.Y + LORE.o: 'ヨ',
    LORE.R + LORE.a: 'ラ', LORE.R + LORE.E: 'リ', LORE.R + LORE.OO: 'ル', LORE.R + LORE.e: 'レ', LORE.R + LORE.o: 'ロ',
    LORE.W + LORE.a: 'ワ', LORE.W + LORE.o: 'ヲ',
    LORE.G + LORE.a: 'ガ', LORE.G + LORE.E: 'ギ', LORE.G + LORE.OO: 'グ', LORE.G + LORE.e: 'ゲ', LORE.G + LORE.o: 'ゴ',
    LORE.Z + LORE.a: 'ザ', LORE.Z + LORE.E: 'ジ', LORE.Z + LORE.OO: 'ズ', LORE.Z + LORE.e: 'ゼ', LORE.Z + LORE.o: 'ゾ',
    LORE.D + LORE.a: 'ダ', LORE.D + LORE.E: 'ヂ', LORE.D + LORE.OO: 'ヅ', LORE.D + LORE.e: 'デ', LORE.D + LORE.o: 'ド',
    LORE.B + LORE.a: 'バ', LORE.B + LORE.E: 'ビ', LORE.B + LORE.OO: 'ブ', LORE.B + LORE.e: 'ベ', LORE.B + LORE.o: 'ボ',
    LORE.P + LORE.a: 'パ', LORE.P + LORE.E: 'ピ', LORE.P + LORE.OO: 'プ', LORE.P + LORE.e: 'ペ', LORE.P + LORE.o: 'ポ'
}

KATAKANA_OO_MAP = {
    'コ': 'ク', 'ソ': 'ス', 'ト': 'ツ', 'ノ': 'ヌ', 'ホ': 'フ',
    'モ': 'ム', 'ヨ': 'ユ', 'ロ': 'ル', 'ゴ': 'グ', 'ゾ': 'ズ',
    'ド': 'ヅ', 'ボ': 'ブ', 'ポ': 'プ'
}

# ==========================================
#               APP LOGIC
# ==========================================

def apply_visual_fixes(text, mode='table'):
    if not text: return ""
    
    if mode == 'header':
        corrections = HEADER_SIZE_CORRECTIONS
        base_size = "32px"
        kata_size = GLOBAL_KATAKANA_HEADER_SIZE
    else:
        corrections = TABLE_SIZE_CORRECTIONS
        base_size = "14pt"
        kata_size = GLOBAL_KATAKANA_TABLE_SIZE
    
    html = ""
    for char in text:
        if char in corrections:
            scale = corrections[char]
            html += f"<span style='font-size:{scale};'>{char}</span>"
        elif '\u30A0' <= char <= '\u30FF':  
            html += f"<span style='font-size:{kata_size};'>{char}</span>"
        else:
            html += char
            
    return f"<span style='font-size:{base_size};'>{html}</span>"

class RichLineEdit(QTextEdit):
    returnPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptRichText(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTabChangesFocus(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setFixedHeight(50) 
        
        self.setStyleSheet("""
            QTextEdit {
                font-size: 14pt; 
                font-weight: bold;
                padding-top: 12px; 
                padding-left: 5px;
                padding-right: 5px;
                border: 1px solid #555; 
                border-radius: 2px;
                background-color: #2b2b2b; 
                color: white;
            }
        """)

    def insertFromMimeData(self, source):
        if source.hasText():
            pasted_text = source.text()
            styled_html = apply_visual_fixes(pasted_text, mode='table')
            self.textCursor().insertHtml(styled_html)
        else:
            super().insertFromMimeData(source)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.returnPressed.emit()
            return 
        super().keyPressEvent(event)

    def setText(self, text):
        styled = apply_visual_fixes(text, mode='table')
        self.setHtml(styled)
        self.moveCursor(QTextCursor.End)
        
    def text(self):
        return self.toPlainText()
        
    def insert(self, text):
        styled = apply_visual_fixes(text, mode='table')
        self.textCursor().insertHtml(styled)
        
    def backspace(self):
        self.textCursor().deletePreviousChar()

    def get_prev_char(self):
        cursor = self.textCursor()
        if cursor.atBlockStart(): return None
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
        return cursor.selectedText()

    def get_last_n_chars(self, n):
        cursor = self.textCursor()
        if cursor.positionInBlock() < n: return None
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, n)
        return cursor.selectedText()

class WordGenerator:
    GEN_SHORT = [LORE.a, LORE.e, LORE.i, LORE.o, LORE.u]
    GEN_LONG = [LORE.A, LORE.E, LORE.I, LORE.O, LORE.U, 
                LORE.AU, LORE.EU, LORE.OU, LORE.OO, LORE.OE]
    
    ALL_VOWELS = GEN_SHORT + GEN_LONG

    @staticmethod
    def generate_word(num_syllables=3):
        word = ""
        structure_log = [] 
        pronunciation_log = []
        
        for i in range(num_syllables):
            structure = random.choices(
                ["CV", "VC", "CVC"], 
                weights=[50, 25, 25],
                k=1
            )[0]
            
            prev_char = word[-1] if word else None
            if prev_char in WordGenerator.ALL_VOWELS and structure in ["V", "VC", "VCC"]:
                structure = random.choice(["CV", "CVC", "CCV"])
            
            structure_log.append(structure)
            syllable = ""
            
            if structure == "V":
                v = random.choice(WordGenerator.ALL_VOWELS)
                if prev_char:
                    while v == prev_char: v = random.choice(WordGenerator.ALL_VOWELS)
                syllable = v
            elif structure == "CV":
                c = random.choice(CONSONANTS)
                while c == prev_char: c = random.choice(CONSONANTS)
                v = random.choice(WordGenerator.ALL_VOWELS)
                syllable = c + v
            elif structure == "CVC":
                c1 = random.choice(CONSONANTS)
                while c1 == prev_char: c1 = random.choice(CONSONANTS)
                v = random.choice(WordGenerator.ALL_VOWELS)
                c2 = random.choice(CONSONANTS)
                while c2 == v: c2 = random.choice(CONSONANTS)
                syllable = c1 + v + c2
            elif structure == "VC":
                valid = WordGenerator.ALL_VOWELS.copy()
                if prev_char in valid: valid.remove(prev_char)
                if prev_char in WordGenerator.GEN_SHORT: valid = [x for x in valid if x not in WordGenerator.GEN_SHORT]
                v = random.choice(valid) if valid else random.choice(WordGenerator.GEN_LONG)
                c = random.choice(CONSONANTS)
                while c == v: c = random.choice(CONSONANTS)
                syllable = v + c
            elif structure == "CVV":
                c = random.choice(CONSONANTS)
                while c == prev_char: c = random.choice(CONSONANTS)
                pair = random.choice(['LL', 'SL', 'LS'])
                v1 = random.choice(WordGenerator.GEN_LONG) if pair[0] == 'L' else random.choice(WordGenerator.GEN_SHORT)
                v2 = random.choice(WordGenerator.GEN_LONG) if pair[1] == 'L' else random.choice(WordGenerator.GEN_SHORT)
                while v2 == v1: v2 = random.choice(WordGenerator.GEN_LONG) if pair[1] == 'L' else random.choice(WordGenerator.GEN_SHORT)
                syllable = c + v1 + v2
            elif structure == "CCV":
                c1 = random.choice(CONSONANTS)
                while c1 == prev_char: c1 = random.choice(CONSONANTS)
                c2 = random.choice(CONSONANTS)
                while c2 == c1: c2 = random.choice(CONSONANTS)
                v = random.choice(WordGenerator.ALL_VOWELS)
                syllable = c1 + c2 + v
            elif structure == "VCC":
                valid = WordGenerator.ALL_VOWELS.copy()
                if prev_char in valid: valid.remove(prev_char)
                if prev_char in WordGenerator.GEN_SHORT: valid = [x for x in valid if x not in WordGenerator.GEN_SHORT]
                v = random.choice(valid) if valid else random.choice(WordGenerator.GEN_LONG)
                c1 = random.choice(CONSONANTS)
                while c1 == v: c1 = random.choice(CONSONANTS)
                c2 = random.choice(CONSONANTS)
                while c2 == c1: c2 = random.choice(CONSONANTS)
                syllable = v + c1 + c2

            word += syllable

            pron_syl = ""
            for char in syllable:
                pron_syl += LORE_TO_PRON.get(char, "?")
            pronunciation_log.append(pron_syl)

        return word, "-".join(structure_log), "-".join(pronunciation_log)

class PhysicalKeyFilter(QObject):
    def __init__(self, parent_window):
        super().__init__()
        self.window = parent_window
        self.key_map = {}
        for row in KEYBOARD_LAYOUT:
            for key_id, lore_char in row:
                self.key_map[key_id] = lore_char

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key_text = event.text().lower()
            if key_text in DISABLED_KEYS: return True 
            if event.key() == Qt.Key_Backspace:
                self.window.backspace()
                return True 
            if event.key() == Qt.Key_Space:
                self.window.input_conlang.insertPlainText(" ")
                return True
            
            if event.modifiers() & Qt.ShiftModifier:
                self.window.shift_active = True
                self.window.shift_btn.setChecked(True)

            if event.modifiers() & (Qt.ControlModifier): return False
            
            if key_text in self.key_map:
                lore_char = self.key_map[key_text]
                self.window.handle_keypress(key_text, lore_char)
                return True 
        return super().eventFilter(obj, event)

class VocabVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Forge")
        self.resize(1200, 750)
        font = QFont("Arial", 12)
        self.setFont(font)
        self.filename = "dictionary.json"
        self.categories = ["dictionary", "word endings", "phrases", "other"]
        self.tables = {} 
        self.data = self.load_data()
        
        self.common_words = self.load_common_words()

        self.shift_active = False
        
        self.key_to_lore = {}
        for row in KEYBOARD_LAYOUT:
            for k, char in row:
                self.key_to_lore[k] = char
        
        self.setup_ui()
        self.key_filter = PhysicalKeyFilter(self)
        self.input_conlang.installEventFilter(self.key_filter)

    def load_data(self):
        default_data = {cat: [] for cat in self.categories}
        if not os.path.exists(self.filename): return default_data
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return json.loads(content) if content else default_data
        except: return default_data
        
    def load_common_words(self):
        filename = "1000.txt"
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            return []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # LEFT PANEL
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(550) 
        
        # --- LEFT PANEL TABS ---
        self.left_tabs = QTabWidget()
        
        # TAB 1: Forge / Keyboard
        forge_tab = QWidget()
        forge_layout = QVBoxLayout(forge_tab)
        
        gen_group = QFrame()
        gen_group.setStyleSheet("background-color: #2b2b2b; border-radius: 8px; padding: 10px;")
        gen_layout = QVBoxLayout(gen_group)
        self.gen_result_display = QLabel("...")
        self.gen_result_display.setAlignment(Qt.AlignCenter)
        self.gen_result_display.setFixedHeight(80) 
        self.gen_result_display.setStyleSheet("color: white; margin-top: 10px;") 
        self.gen_result_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        gen_layout.addWidget(self.gen_result_display)
        
        self.gen_pron_display = QLabel("")
        self.gen_pron_display.setAlignment(Qt.AlignCenter)
        self.gen_pron_display.setStyleSheet("color: #4fc3f7; font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        self.gen_pron_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        gen_layout.addWidget(self.gen_pron_display)

        self.gen_structure_display = QLabel("")
        self.gen_structure_display.setAlignment(Qt.AlignCenter)
        self.gen_structure_display.setFixedHeight(30)
        self.gen_structure_display.setStyleSheet("color: #888; font-size: 14px; font-style: italic; margin-bottom: 10px;")
        gen_layout.addWidget(self.gen_structure_display)
        
        slider_container = QHBoxLayout()
        self.syllable_label = QLabel("Syllables: 3")
        self.syllable_label.setStyleSheet("color: #bbb; font-weight: bold;")
        
        self.syllable_slider = QSlider(Qt.Horizontal)
        self.syllable_slider.setMinimum(1)
        self.syllable_slider.setMaximum(8)
        self.syllable_slider.setValue(3)
        self.syllable_slider.setTickPosition(QSlider.TicksBelow)
        self.syllable_slider.setTickInterval(1)
        self.syllable_slider.setStyleSheet("""
            QSlider::groove:horizontal { border: 1px solid #555; height: 8px; background: #333; margin: 2px 0; border-radius: 4px; }
            QSlider::handle:horizontal { background: #0277bd; border: 1px solid #0277bd; width: 18px; height: 18px; margin: -7px 0; border-radius: 9px; }
        """)
        self.syllable_slider.valueChanged.connect(self.update_slider_label)
        
        slider_container.addWidget(self.syllable_label)
        slider_container.addWidget(self.syllable_slider)
        gen_layout.addLayout(slider_container)

        btn_generate = QPushButton("Generate Random Word")
        btn_generate.clicked.connect(self.run_generator)
        btn_generate.setStyleSheet("QPushButton { background-color: #0277bd; color: white; padding: 8px; border-radius: 4px; font-weight: bold; } QPushButton:hover { background-color: #039be5; } QPushButton:pressed { background-color: #01579b; }")
        gen_layout.addWidget(btn_generate)
        forge_layout.addWidget(gen_group)
        forge_layout.addSpacing(10)

        # MANUAL ENTRY
        form_layout = QGridLayout()
        self.input_conlang = RichLineEdit()
        self.input_conlang.returnPressed.connect(self.add_entry)

        self.input_conlang.setPlaceholderText("New Word")
        self.input_english = QLineEdit()
        self.input_english.setPlaceholderText("English Definition")
        self.input_english.setFixedHeight(50)
        self.input_english.setStyleSheet("font-size: 14pt; padding: 5px;")
        self.input_english.returnPressed.connect(self.add_entry)

        self.input_notes = QLineEdit()
        self.input_notes.setPlaceholderText("Notes")
        self.input_notes.setFixedHeight(50)
        self.input_notes.setStyleSheet("font-size: 14pt; padding: 5px;")
        self.input_notes.returnPressed.connect(self.add_entry)
        
        form_layout.addWidget(QLabel("Word:"), 0, 0)
        form_layout.addWidget(self.input_conlang, 0, 1)
        form_layout.addWidget(QLabel("Def:"), 1, 0)
        form_layout.addWidget(self.input_english, 1, 1)
        form_layout.addWidget(QLabel("Notes:"), 2, 0)
        form_layout.addWidget(self.input_notes, 2, 1)
        forge_layout.addLayout(form_layout)
        
        self.add_button = QPushButton("Save to Dictionary")
        self.add_button.setMinimumHeight(45)
        self.add_button.setStyleSheet("QPushButton { background-color: #2e7d32; color: white; font-weight: bold; border-radius: 4px; font-size: 16px; } QPushButton:hover { background-color: #388e3c; } QPushButton:pressed { background-color: #1b5e20; }")
        self.add_button.clicked.connect(self.add_entry)
        forge_layout.addWidget(self.add_button)
        
        forge_layout.addSpacing(15)
        
        kbd_header_layout = QHBoxLayout()
        kbd_header_layout.addWidget(QLabel("Touch Keyboard:"))
        kbd_header_layout.addStretch()
        
        self.katakana_mode_btn = QPushButton("Katakana Mode: OFF")
        self.katakana_mode_btn.setCheckable(True)
        self.katakana_mode_btn.setStyleSheet("""
            QPushButton { background-color: #333; color: white; font-weight: bold; border: 1px solid #555; border-radius: 4px; padding: 4px 10px; }
            QPushButton:hover { background-color: #444; border-color: #777; }
            QPushButton:checked { background-color: #9c27b0; color: white; border-color: #7b1fa2; }
        """)
        self.katakana_mode_btn.toggled.connect(self.toggle_katakana_mode)
        self.katakana_mode_btn.setChecked(False)
        kbd_header_layout.addWidget(self.katakana_mode_btn)
        
        forge_layout.addLayout(kbd_header_layout)
        
        keyboard = self.create_keyboard()
        forge_layout.addWidget(keyboard)
        forge_layout.addStretch()
        
        self.left_tabs.addTab(forge_tab, "Word Forge")
        
        # TAB 2: Alphabet Definitions
        def_tab = QWidget()
        def_layout = QVBoxLayout(def_tab)
        
        self.def_browser = QTextBrowser()
        self.def_browser.setOpenExternalLinks(False)
        self.def_browser.setStyleSheet("background-color: #2b2b2b; color: white; font-size: 12pt; border: 1px solid #444;")
        
        html = "<h2>Angloslav Alphabet</h2><table width='100%' cellpadding='6' style='border-collapse: collapse; margin-bottom: 20px;'>"
        html += "<tr style='background-color: #444;'><th style='border-bottom: 1px solid white;'>Char</th><th style='border-bottom: 1px solid white;'>Sound</th><th style='border-bottom: 1px solid white;'>Notes</th></tr>"
        for char, sound, notes in ALPHABET_DEFS:
            styled_char = apply_visual_fixes(char, mode='table')
            html += f"<tr><td style='border-bottom: 1px solid #444; text-align: center; font-size: 16pt;'>{styled_char}</td><td style='border-bottom: 1px solid #444;'>{sound}</td><td style='border-bottom: 1px solid #444; font-size: 11pt; color: #bbb;'>{notes}</td></tr>"
        
        html += "</table><h2>Katakana Syllabary</h2><table width='100%' cellpadding='6' style='border-collapse: collapse;'>"
        html += "<tr style='background-color: #444;'><th style='border-bottom: 1px solid white;'>Cluster</th><th style='border-bottom: 1px solid white;'>Katakana</th><th style='border-bottom: 1px solid white;'>Pronunciation</th></tr>"
        for cluster, kata in KATAKANA_MAP.items():
            styled_cluster = apply_visual_fixes(cluster, mode='table')
            styled_kata = f"<span style='font-size:{GLOBAL_KATAKANA_TABLE_SIZE};'>{kata}</span>"
            c1, c2 = cluster[0], cluster[1]
            pron = LORE_TO_PRON.get(c1, "?") + LORE_TO_PRON.get(c2, "?")
            html += f"<tr><td style='border-bottom: 1px solid #444; text-align: center; font-size: 16pt;'>{styled_cluster}</td><td style='border-bottom: 1px solid #444; text-align: center; font-size: 16pt; color: #9c27b0;'>{styled_kata}</td><td style='border-bottom: 1px solid #444; text-align: center;'>{pron}</td></tr>"
        html += "</table>"
        
        self.def_browser.setHtml(html)
        def_layout.addWidget(self.def_browser)
        
        self.left_tabs.addTab(def_tab, "Definitions")
        left_layout.addWidget(self.left_tabs)
        
        # RIGHT PANEL
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.tabs = QTabWidget()
        for category in self.categories:
            tab = QWidget()
            t_layout = QVBoxLayout(tab)
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Lore Word", "Definition", "Notes", ""])
            
            # --- ENABLE CONTEXT MENU FOR COPYING ---
            table.setContextMenuPolicy(Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(lambda pos, t=table, c=category: self.show_table_context_menu(pos, t, c))
            
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.Stretch)
            header.setSectionResizeMode(3, QHeaderView.Fixed)
            table.setColumnWidth(3, 40)
            
            self.tables[category] = table
            t_layout.addWidget(table)
            self.tabs.addTab(tab, category.title())
        right_layout.addWidget(self.tabs)
        self.stats_label = QLabel("Total Words: 0")
        right_layout.addWidget(self.stats_label)
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        for category in self.categories:
            self.refresh_table(category)

    def show_table_context_menu(self, pos, table, category):
        row = table.rowAt(pos.y())
        col = table.columnAt(pos.x())
        
        # Ignore out of bounds clicks or clicks on the delete button column
        if row < 0 or col < 0 or col == 3:
            return

        # Fetch plain text directly from the saved data (bypassing HTML)
        item_data = self.data[category][row]
        text_to_copy = ""
        
        if col == 0:
            text_to_copy = item_data.get('conlang', '')
        elif col == 1:
            text_to_copy = item_data.get('english', '')
        elif col == 2:
            text_to_copy = item_data.get('notes', '')

        if not text_to_copy:
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #333; color: white; border: 1px solid #555; }
            QMenu::item:selected { background-color: #0277bd; }
        """)
        copy_action = menu.addAction("Copy")
        
        action = menu.exec(table.viewport().mapToGlobal(pos))
        
        if action == copy_action:
            QApplication.clipboard().setText(text_to_copy)

    def create_keyboard(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(4)
        KEY_STYLE = "QPushButton {{ background-color: #444; color: {color}; border: 1px solid #555; border-radius: 5px; }} QPushButton:hover {{ background-color: #555; border-color: #777; }} QPushButton:pressed {{ background-color: #222; border-color: #333; }}"
        for row_data in KEYBOARD_LAYOUT:
            row = QHBoxLayout()
            row.setSpacing(4)
            row.addStretch() 
            for key_id, label in row_data:
                btn = QPushButton(label)
                btn.setFixedSize(45, 45)
                btn.setFont(QFont("Arial", 14))
                btn.clicked.connect(lambda ch=False, k=key_id, l=label: self.handle_keypress(k, l))
                text_color = "#ffab91" if label in VOWELS else "#81d4fa"
                btn.setStyleSheet(KEY_STYLE.format(color=text_color))
                row.addWidget(btn)
            row.addStretch()
            layout.addLayout(row)
        
        ctrl_row = QHBoxLayout()
        ctrl_row.addStretch()
        
        self.shift_btn = QPushButton("SHIFT")
        self.shift_btn.setCheckable(True)
        self.shift_btn.setFixedSize(80, 45)
        self.shift_btn.setStyleSheet("""
            QPushButton { background-color: #333; color: white; font-weight: bold; border: 1px solid #555; border-radius: 5px; }
            QPushButton:hover { background-color: #444; border-color: #777; }
            QPushButton:checked { background-color: #ff9800; color: black; border-color: #e65100; }
        """)
        self.shift_btn.toggled.connect(self.toggle_shift)
        ctrl_row.addWidget(self.shift_btn)

        CTRL_STYLE = "QPushButton { background-color: #333; color: white; border: 1px solid #555; border-radius: 5px; } QPushButton:hover { background-color: #444; border-color: #777; } QPushButton:pressed { background-color: #222; border-color: #111; }"
        space_btn = QPushButton("Space")
        space_btn.setFixedSize(150, 45)
        space_btn.setStyleSheet(CTRL_STYLE)
        space_btn.clicked.connect(lambda: self.input_conlang.insertPlainText(" "))
        ctrl_row.addWidget(space_btn)
        
        back_btn = QPushButton("⌫")
        back_btn.setFixedSize(60, 45)
        back_btn.setStyleSheet(CTRL_STYLE)
        back_btn.clicked.connect(self.backspace)
        ctrl_row.addWidget(back_btn)
        
        ctrl_row.addStretch()
        layout.addLayout(ctrl_row)
        return container

    def update_slider_label(self, value):
        self.syllable_label.setText(f"Syllables: {value}")

    def toggle_shift(self, checked):
        self.shift_active = checked

    def toggle_katakana_mode(self, checked):
        if checked:
            self.katakana_mode_btn.setText("Katakana Mode: ON")
        else:
            self.katakana_mode_btn.setText("Katakana Mode: OFF")

    def handle_keypress(self, key_id, default_char):
        if self.shift_active:
            if key_id in LONG_VOWEL_MAP:
                result = LONG_VOWEL_MAP[key_id]
                self.input_conlang.insert(result)
            else:
                self.input_conlang.insert(default_char)
            self.shift_btn.setChecked(False)
            self.input_conlang.setFocus()
            self._check_katakana()
            return

        prev_char = self.input_conlang.get_prev_char()
        
        if prev_char:
            for combo_key, combo_val in COMBO_MAP.items():
                if combo_key.endswith(key_id) and len(combo_key) == 2:
                    prefix_key = combo_key[0] 
                    
                    if prefix_key in self.key_to_lore:
                        expected_lore_prefix = self.key_to_lore[prefix_key]
                        
                        if prev_char == expected_lore_prefix:
                            self.input_conlang.backspace()
                            self.input_conlang.insert(combo_val)
                            self.input_conlang.setFocus()
                            self._check_katakana()
                            return

        self.input_conlang.insert(default_char)
        self.input_conlang.setFocus()
        self._check_katakana()

    def _check_katakana(self):
        if not self.katakana_mode_btn.isChecked(): return

        prev_2 = self.input_conlang.get_last_n_chars(2)
        if not prev_2: return

        if prev_2[0] in KATAKANA_OO_MAP and prev_2[1] == LORE.o:
            self.input_conlang.backspace()
            self.input_conlang.backspace()
            self.input_conlang.insert(KATAKANA_OO_MAP[prev_2[0]])
            return

        if prev_2 in KATAKANA_MAP:
            self.input_conlang.backspace()
            self.input_conlang.backspace()
            self.input_conlang.insert(KATAKANA_MAP[prev_2])

    def backspace(self):
        self.input_conlang.backspace()
        self.input_conlang.setFocus()

    def run_generator(self):
        syl_count = self.syllable_slider.value()
        word, structure, pron = WordGenerator.generate_word(num_syllables=syl_count)
        
        if self.katakana_mode_btn.isChecked():
            for cluster, katakana in KATAKANA_MAP.items():
                word = word.replace(cluster, katakana)

        styled_word = apply_visual_fixes(word, mode='header')
        self.gen_result_display.setText(styled_word)
        self.gen_structure_display.setText(structure)
        self.gen_pron_display.setText(pron)
        self.input_conlang.setText(word)
        
        if self.common_words:
            random_def = random.choice(self.common_words)
            self.input_english.setText(random_def)

    def add_entry(self):
        conlang = self.input_conlang.text().strip()
        english = self.input_english.text().strip()
        notes = self.input_notes.text().strip()
        if not conlang or not english:
            QMessageBox.warning(self, "Missing Info", "Need word and definition.")
            return
        cat = self.categories[self.tabs.currentIndex()]
        self.data[cat].append({ "conlang": conlang, "english": english, "notes": notes })
        self.save_data()
        self.refresh_table(cat)
        self.input_conlang.clear()
        self.input_english.clear()
        self.input_notes.clear()
        self.input_conlang.setFocus() 
        self.gen_result_display.setText("...")
        self.gen_structure_display.setText("")
        self.gen_pron_display.setText("")

    def delete_entry(self, category, index):
        if index < 0 or index >= len(self.data[category]):
            return
        del self.data[category][index]
        self.save_data()
        self.refresh_table(category)

    def refresh_table(self, category):
        table = self.tables[category]
        items = self.data[category]
        table.setRowCount(0)
        self.stats_label.setText(f"Total Words: {sum(len(v) for v in self.data.values())}")
        
        for r, item in enumerate(items):
            table.insertRow(r)
            lore_word_raw = item.get('conlang', '')
            lore_word_styled = apply_visual_fixes(lore_word_raw, mode='table')
            label = QLabel(lore_word_styled)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setMinimumWidth(150)
            table.setCellWidget(r, 0, label)
            
            english_item = QTableWidgetItem(item.get('english', ''))
            english_item.setFont(QFont("Arial", 12))
            table.setItem(r, 1, english_item)
            
            notes_item = QTableWidgetItem(item.get('notes', ''))
            notes_item.setFont(QFont("Arial", 12))
            table.setItem(r, 2, notes_item)

            del_btn = QPushButton("x")
            del_btn.setFixedSize(24, 24)
            del_btn.setStyleSheet("""
                QPushButton {
                    background-color: #d32f2f; 
                    color: white; 
                    font-weight: bold; 
                    border: none; 
                    border-radius: 12px;
                    padding-bottom: 2px;
                }
                QPushButton:hover { background-color: #b71c1c; }
            """)
            del_btn.clicked.connect(lambda checked=False, c=category, i=r: self.delete_entry(c, i))
            
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0,0,0,0)
            layout.setAlignment(Qt.AlignCenter)
            layout.addWidget(del_btn)
            table.setCellWidget(r, 3, container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VocabVault()
    window.show()
    sys.exit(app.exec())

"""
backlog
    - syllable length
    - pronunciation
    - definition generator
"""
import sys
import json
import os
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTabWidget, QLineEdit, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QMessageBox, QGridLayout, QFrame, QLabel, QTextEdit,
                               QSlider) # Added QSlider
from PySide6.QtGui import QFont, QColor, QTextCursor
from PySide6.QtCore import Qt, QObject, QEvent, Signal

# ==========================================
#        MASTER CHARACTER DEFINITIONS
# ==========================================

class LORE:
    # --- VOWELS ---
    # Short
    A_SHORT = 'a'
    E_SHORT = 'э'
    I_SHORT = 'ɪ'
    O_SHORT = 'o'
    U_SHORT = 'ɦ'

    # Long (Shifted)
    A_LONG = 'ʌ'
    E_LONG = 'и'
    I_LONG = 'ꭅ'
    O_LONG = 'ꟻ'
    U_LONG = 'Ʉ'

    # Compounds (Auto-Ligatures)
    AU = 'ѫ'
    EW = 'ը'
    OE = 'ɶ'
    OW = 'ᴇ'
    OO = 'У'

    # --- CONSONANTS ---
    # Standard Mappings
    Q = 'Ƿ'
    P = 'ʀ'
    T = 'ᴛ'
    B = 'ь'
    P_CYR = 'п'
    C = 'c'
    D_CYR = 'д'
    V = 'v'
    G_CYR = 'г'
    X = 'x'
    D = 'џ'
    K_SMALL = 'ᴋ'
    L_CYR = 'Ԓ' 
    Z = 'z'
    B_SMALL = 'ʙ'
    B_CYR = 'Б'
    N_SMALL = 'ʜ'
    M_SMALL = 'ᴍ'

    # Compounds (Auto-Ligatures)
    ZH = 'ж'
    CH = 'ч'
    SH = 'ш'
    TH = 'ᴘ'
    DH = 'ƌ'
    NG = 'ҕ'
    GLOTTAL = '⧅'

    # Non-Essential Compounds (Shortcuts)
    TS = 'ҵ'
    ST = 'ʒ'
    KS = 'Ұ'
    SK = 'ϣ'
    KV = 'Է'
    SV = '₪'
    ZV = 'ᴝ'
    DV = 'ƶ'

# ==========================================
#           LORE CONFIGURATION
# ==========================================

VOWELS = [
    LORE.A_SHORT, LORE.E_SHORT, LORE.I_SHORT, LORE.O_SHORT, LORE.U_SHORT, 
    LORE.A_LONG, LORE.E_LONG, LORE.I_LONG, LORE.O_LONG, LORE.U_LONG, 
    LORE.AU, LORE.EW, LORE.OW, LORE.OO, LORE.OE
]

CONSONANTS = [
    LORE.Q, LORE.P, LORE.T, LORE.B, LORE.P_CYR, LORE.C, LORE.D_CYR, LORE.V, LORE.G_CYR, 
    LORE.X, LORE.D, LORE.K_SMALL, LORE.L_CYR, LORE.Z, LORE.B_SMALL, LORE.B_CYR, LORE.N_SMALL, LORE.M_SMALL, 
    LORE.ZH, LORE.CH, LORE.SH, LORE.TH, LORE.DH, LORE.NG, LORE.GLOTTAL,
    LORE.TS, LORE.ST, LORE.KS, LORE.SK, LORE.KV, LORE.SV, LORE.ZV, LORE.DV
]

# --- VISUAL TWEAKS ---
TABLE_SIZE_CORRECTIONS = {
    LORE.U_SHORT:   "14pt", 
    LORE.O_LONG:    "10.5pt", 
    LORE.U_LONG:    "10.5pt", 
    LORE.OO:        "10.5pt", 
    LORE.B_CYR:     "10.5pt", 
    LORE.L_CYR:     "10.5pt",
    LORE.Q:         "10pt",
    LORE.GLOTTAL:   "13pt",
    LORE.TH:        "14pt",
    LORE.DH:        "14pt",
    LORE.NG:        "14pt",
    LORE.SK:        "14pt",
    LORE.ZV:        "16pt",
    LORE.KS:        "10.5pt"
}

HEADER_SIZE_CORRECTIONS = {
    LORE.U_SHORT:   "20pt", 
    LORE.O_LONG:    "17pt",
    LORE.U_LONG:    "17pt",
    LORE.OO:        "17.5pt", 
    LORE.B_CYR:     "17pt", 
    LORE.L_CYR:     "17pt",
    LORE.Q:         "17pt",
    LORE.GLOTTAL:   "20pt",
    LORE.TH:        "23pt",
    LORE.DH:        "20pt",
    LORE.NG:        "24pt",
    LORE.SK:        "24pt",
    LORE.ZV:        "26pt",
    LORE.KS:        "17pt"
}

# Keyboard Layout
KEYBOARD_LAYOUT = [
    [('`', LORE.GLOTTAL), ('w', LORE.Q), ('e', LORE.E_SHORT), ('r', LORE.P), ('t', LORE.T), ('y', LORE.B), ('u', LORE.U_SHORT), ('i', LORE.I_SHORT), ('o', LORE.O_SHORT), ('p', LORE.P_CYR)],
    [('a', LORE.A_SHORT), ('s', LORE.C), ('d', LORE.D_CYR), ('f', LORE.V), ('g', LORE.G_CYR), ('h', LORE.X), ('j', LORE.D), ('k', LORE.K_SMALL), ('l', LORE.L_CYR)],
    [('z', LORE.Z), ('v', LORE.B_SMALL), ('b', LORE.B_CYR), ('n', LORE.N_SMALL), ('m', LORE.M_SMALL)]
]

# --- INPUT MAPPING ---

LONG_VOWEL_MAP = {
    "a": LORE.A_LONG, 
    "e": LORE.E_LONG, 
    "i": LORE.I_LONG, 
    "o": LORE.O_LONG, 
    "u": LORE.U_LONG
}

COMBO_MAP = {
    # Vowels
    "au": LORE.AU, "eu": LORE.EW, "ou": LORE.OW, "oo": LORE.OO, "oe": LORE.OE,
    # Consonants (Essential)
    "zh": LORE.ZH, "sh": LORE.SH, "kh": LORE.CH, 
    "th": LORE.TH, "dh": LORE.DH, "ng": LORE.NG,
    # Consonants (Non-Essential Shortcuts)
    "ts": LORE.TS, "st": LORE.ST, "ks": LORE.KS, "sk": LORE.SK,
    "kv": LORE.KV, "sv": LORE.SV, "zv": LORE.ZV, "dv": LORE.DV
}

DISABLED_KEYS = ['q', 'x', 'c']

# ==========================================
#               APP LOGIC
# ==========================================

def apply_visual_fixes(text, mode='table'):
    if not text: return ""
    
    if mode == 'header':
        corrections = HEADER_SIZE_CORRECTIONS
        base_size = "32px"
    else:
        corrections = TABLE_SIZE_CORRECTIONS
        base_size = "14pt"
    
    html = ""
    for char in text:
        if char in corrections:
            scale = corrections[char]
            html += f"<span style='font-size:{scale};'>{char}</span>"
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
        if cursor.atBlockStart():
            return None
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
        return cursor.selectedText()

class WordGenerator:
    GEN_SHORT = [LORE.A_SHORT, LORE.E_SHORT, LORE.I_SHORT, LORE.O_SHORT, LORE.U_SHORT]
    GEN_LONG = [LORE.A_LONG, LORE.E_LONG, LORE.I_LONG, LORE.O_LONG, LORE.U_LONG, 
                LORE.AU, LORE.EW, LORE.OW, LORE.OO, LORE.OE]
    
    ALL_VOWELS = GEN_SHORT + GEN_LONG

    @staticmethod
    def generate_word(num_syllables=3):
        word = ""
        structure_log = [] 
        
        for i in range(num_syllables):
            structure = random.choices(
                ["CV", "CVC", "VC", "CVV", "V", "CCV", "VCC"], 
                weights=[25, 25, 20, 10, 5, 10, 5],
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
        return word, "-".join(structure_log)

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
                self.window.input_conlang.insert(" ")
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
        self.filename = "future_lang.json"
        self.categories = ["dictionary", "phrases"]
        self.tables = {} 
        self.data = self.load_data()
        
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
        left_panel.setFixedWidth(500)
        
        gen_group = QFrame()
        gen_group.setStyleSheet("background-color: #2b2b2b; border-radius: 8px; padding: 10px;")
        gen_layout = QVBoxLayout(gen_group)
        self.gen_result_display = QLabel("...")
        self.gen_result_display.setAlignment(Qt.AlignCenter)
        self.gen_result_display.setFixedHeight(80) 
        self.gen_result_display.setStyleSheet("color: white; margin-top: 10px;") 
        self.gen_result_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        gen_layout.addWidget(self.gen_result_display)

        self.gen_structure_display = QLabel("")
        self.gen_structure_display.setAlignment(Qt.AlignCenter)
        self.gen_structure_display.setFixedHeight(30)
        self.gen_structure_display.setStyleSheet("color: #888; font-size: 14px; font-style: italic; margin-bottom: 10px;")
        gen_layout.addWidget(self.gen_structure_display)
        
        # --- SLIDER CONTROL START ---
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
        # --- SLIDER CONTROL END ---

        btn_generate = QPushButton("Generate Random Word")
        btn_generate.clicked.connect(self.run_generator)
        btn_generate.setStyleSheet("QPushButton { background-color: #0277bd; color: white; padding: 8px; border-radius: 4px; font-weight: bold; } QPushButton:hover { background-color: #039be5; } QPushButton:pressed { background-color: #01579b; }")
        gen_layout.addWidget(btn_generate)
        left_layout.addWidget(gen_group)
        left_layout.addSpacing(10)

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
        self.input_notes.setPlaceholderText("Etymology / Root Notes")
        self.input_notes.setFixedHeight(50)
        self.input_notes.setStyleSheet("font-size: 14pt; padding: 5px;")
        self.input_notes.returnPressed.connect(self.add_entry)
        
        form_layout.addWidget(QLabel("Word:"), 0, 0)
        form_layout.addWidget(self.input_conlang, 0, 1)
        form_layout.addWidget(QLabel("Def:"), 1, 0)
        form_layout.addWidget(self.input_english, 1, 1)
        form_layout.addWidget(QLabel("Root:"), 2, 0)
        form_layout.addWidget(self.input_notes, 2, 1)
        left_layout.addLayout(form_layout)
        
        self.add_button = QPushButton("Save to Dictionary")
        self.add_button.setMinimumHeight(45)
        self.add_button.setStyleSheet("QPushButton { background-color: #2e7d32; color: white; font-weight: bold; border-radius: 4px; font-size: 16px; } QPushButton:hover { background-color: #388e3c; } QPushButton:pressed { background-color: #1b5e20; }")
        self.add_button.clicked.connect(self.add_entry)
        left_layout.addWidget(self.add_button)
        
        left_layout.addSpacing(15)
        left_layout.addWidget(QLabel("Touch Keyboard:"))
        keyboard = self.create_keyboard()
        left_layout.addWidget(keyboard)
        left_layout.addStretch()
        
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
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
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
        space_btn.clicked.connect(lambda: self.input_conlang.insert(" "))
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

    def handle_keypress(self, key_id, default_char):
        if self.shift_active:
            if key_id in LONG_VOWEL_MAP:
                result = LONG_VOWEL_MAP[key_id]
                self.input_conlang.insert(result)
            else:
                self.input_conlang.insert(default_char)
            self.shift_btn.setChecked(False)
            self.input_conlang.setFocus()
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
                            return

        self.input_conlang.insert(default_char)
        self.input_conlang.setFocus()

    def backspace(self):
        self.input_conlang.backspace()
        self.input_conlang.setFocus()

    def run_generator(self):
        # NEW: GET VALUE FROM SLIDER
        syl_count = self.syllable_slider.value()
        word, structure = WordGenerator.generate_word(num_syllables=syl_count)
        
        styled_word = apply_visual_fixes(word, mode='header')
        self.gen_result_display.setText(styled_word)
        self.gen_structure_display.setText(structure)
        self.input_conlang.setText(word)

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
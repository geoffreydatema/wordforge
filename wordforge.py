import sys
import json
import os
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTabWidget, QLineEdit, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QMessageBox, QGridLayout, QFrame, QLabel, QTextEdit)
from PySide6.QtGui import QFont, QColor, QTextCursor
from PySide6.QtCore import Qt, QObject, QEvent

# --- LORE CONFIGURATION ---
VOWELS = ['a', 'э', 'ʟ', 'o', 'h', 'ʌ', 'и', 'ꭅ', 'ꟻ', 'ю', 'e', 'ᴇ', 'У', 'я', 's']
CONSONANTS = ['q', 'p', 'ᴛ', 'b', 'п', 'c', 'д', 'v', 'г', 'x', 'd', 'ᴋ', 'ԉ', 'z', 'ʙ', 'Б', 'ʜ', 'ᴍ', 'ж', 'ц', 'ч', 'ш', 'ꚇ', 'Ұ', 'њ', 'Ꙗ', 'ԕ']

# --- VISUAL TWEAKS ---
# 1. TABLE/INPUT CORRECTIONS (Base font ~14pt)
TABLE_SIZE_CORRECTIONS = {
    "ꟻ": "10pt", "У": "10pt", "Б": "10pt", "Ұ": "10pt", "ꚇ": "16pt", "Ꙗ": "12pt"
}

# 2. HEADER CORRECTIONS (Base font ~32px/24pt)
HEADER_SIZE_CORRECTIONS = {
    "ꟻ": "17pt", "У": "17pt", "Б": "17pt", "Ұ": "17pt", "ꚇ": "24pt", "Ꙗ": "17pt"
}

# Keyboard Layout
KEYBOARD_LAYOUT = [
    [('w', 'q'), ('e', 'э'), ('r', 'p'), ('t', 'ᴛ'), ('y', 'b'), ('u', 'h'), ('i', 'ʟ'), ('o', 'o'), ('p', 'п')],
    [('a', 'a'), ('s', 'c'), ('d', 'д'), ('f', 'v'), ('g', 'г'), ('h', 'x'), ('j', 'd'), ('k', 'ᴋ'), ('l', 'ԉ')],
    [('z', 'z'), ('v', 'ʙ'), ('b', 'Б'), ('n', 'ʜ'), ('m', 'ᴍ')]
]

# Clusters & Combos
COMBO_MAP = {
    "a": "ʌ", "e": "и", "i": "ꭅ", "o": "ꟻ", "u": "ю",
    "ya": "я", "ye": "e", "yo": "ᴇ", "oo": "У", "oe": "s",
    "ts": "ц", "zh": "ж", "sh": "ш", "kh": "ч", "sk": "ꚇ", "st": "ԕ",
    "th": "Ұ", "dh": "њ", "ng": "Ꙗ"
}

DISABLED_KEYS = ['q', 'x', 'c']

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
    """
    A Custom Widget that looks like a QLineEdit but supports Rich Text (HTML).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptRichText(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTabChangesFocus(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setFixedHeight(40) # Fixed height to match single line input
        
        # Style to match the other inputs
        self.setStyleSheet("""
            QTextEdit {
                font-size: 14pt; 
                font-weight: bold;
                padding: 5px; 
                border: 1px solid #555; 
                border-radius: 2px;
                background-color: #2b2b2b; 
                color: white;
            }
        """)

    def keyPressEvent(self, event):
        # Prevent newlines when hitting Enter
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            return 
        super().keyPressEvent(event)

    def setText(self, text):
        # Automatically apply visual fixes when setting text programmatically
        styled = apply_visual_fixes(text, mode='table')
        self.setHtml(styled)
        self.moveCursor(QTextCursor.End)
        
    def text(self):
        return self.toPlainText()
        
    def insert(self, text):
        # FIX: Apply visual fixes to individual characters/strings inserted
        # This handles both Virtual Keyboard clicks and Physical key presses
        styled = apply_visual_fixes(text, mode='table')
        self.textCursor().insertHtml(styled)
        
    def backspace(self):
        # Compatibility method for Virtual Keyboard
        self.textCursor().deletePreviousChar()

class WordGenerator:
    SHORT_VOWELS = ['a', 'э', 'ʟ', 'o', 'h', 's']
    LONG_VOWELS = ['ʌ', 'и', 'ꭅ', 'ꟻ', 'ю', 'e', 'ᴇ', 'У', 'я']
    ALL_VOWELS = SHORT_VOWELS + LONG_VOWELS

    @staticmethod
    def generate_word(min_syllables=1, max_syllables=3):
        word = ""
        structure_log = [] 
        syllables = random.randint(min_syllables, max_syllables)
        
        for i in range(syllables):
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
                if prev_char in WordGenerator.SHORT_VOWELS: valid = [x for x in valid if x not in WordGenerator.SHORT_VOWELS]
                v = random.choice(valid) if valid else random.choice(WordGenerator.LONG_VOWELS)
                c = random.choice(CONSONANTS)
                while c == v: c = random.choice(CONSONANTS)
                syllable = v + c
            elif structure == "CVV":
                c = random.choice(CONSONANTS)
                while c == prev_char: c = random.choice(CONSONANTS)
                pair = random.choice(['LL', 'SL', 'LS'])
                v1 = random.choice(WordGenerator.LONG_VOWELS) if pair[0] == 'L' else random.choice(WordGenerator.SHORT_VOWELS)
                v2 = random.choice(WordGenerator.LONG_VOWELS) if pair[1] == 'L' else random.choice(WordGenerator.SHORT_VOWELS)
                while v2 == v1: v2 = random.choice(WordGenerator.LONG_VOWELS) if pair[1] == 'L' else random.choice(WordGenerator.SHORT_VOWELS)
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
                if prev_char in WordGenerator.SHORT_VOWELS: valid = [x for x in valid if x not in WordGenerator.SHORT_VOWELS]
                v = random.choice(valid) if valid else random.choice(WordGenerator.LONG_VOWELS)
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
            if event.modifiers() & (Qt.ControlModifier | Qt.AltModifier): return False
            if key_text in self.key_map:
                lore_char = self.key_map[key_text]
                is_shifted = bool(event.modifiers() & Qt.ShiftModifier)
                if is_shifted:
                    self.window.shift_active = True
                    self.window.shift_btn.setChecked(True)
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
        self.shift_buffer = ""
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
        
        btn_generate = QPushButton("Generate Random Word")
        btn_generate.clicked.connect(self.run_generator)
        btn_generate.setStyleSheet("QPushButton { background-color: #0277bd; color: white; padding: 8px; border-radius: 4px; font-weight: bold; } QPushButton:hover { background-color: #039be5; } QPushButton:pressed { background-color: #01579b; }")
        gen_layout.addWidget(btn_generate)
        left_layout.addWidget(gen_group)
        left_layout.addSpacing(10)

        # MANUAL ENTRY
        form_layout = QGridLayout()
        
        self.input_conlang = RichLineEdit()
        self.input_conlang.setPlaceholderText("New Word")
        
        self.input_english = QLineEdit()
        self.input_english.setPlaceholderText("English Definition")
        self.input_english.setStyleSheet("font-size: 14pt; padding: 5px;")
        
        self.input_notes = QLineEdit()
        self.input_notes.setPlaceholderText("Etymology / Root Notes")
        self.input_notes.setStyleSheet("font-size: 14pt; padding: 5px;")
        
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
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Lore Word", "Definition", "Notes"])
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
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
        self.shift_btn.setStyleSheet("QPushButton { background-color: #333; color: white; font-weight: bold; border: 1px solid #555; border-radius: 5px; } QPushButton:hover { background-color: #444; border-color: #777; } QPushButton:checked { background-color: #ff9800; color: black; border-color: #e65100; }")
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

    def toggle_shift(self, checked):
        self.shift_active = checked
        if not checked and self.shift_buffer:
            if self.shift_buffer in COMBO_MAP:
                result = COMBO_MAP[self.shift_buffer]
                self.replace_last_chars(len(self.shift_buffer), result)
            self.shift_buffer = ""

    def replace_last_chars(self, n, new_text):
        for _ in range(n):
            self.input_conlang.backspace()
        self.input_conlang.insert(new_text)

    def handle_keypress(self, key_id, default_char):
        if not self.shift_active:
            self.input_conlang.insert(default_char)
            self.input_conlang.setFocus()
            self.shift_buffer = ""
            return
        self.input_conlang.insert(default_char)
        self.input_conlang.setFocus()
        self.shift_buffer += key_id
        is_prefix = False
        for code in COMBO_MAP.keys():
            if code.startswith(self.shift_buffer) and len(code) > len(self.shift_buffer):
                is_prefix = True
                break
        if is_prefix: return
        if self.shift_buffer in COMBO_MAP:
            result = COMBO_MAP[self.shift_buffer]
            self.replace_last_chars(len(self.shift_buffer), result)
            self.shift_buffer = ""
        else:
            prev_buffer = self.shift_buffer[:-1]
            if prev_buffer in COMBO_MAP:
                self.input_conlang.backspace() 
                result = COMBO_MAP[prev_buffer]
                self.replace_last_chars(len(prev_buffer), result)
                self.input_conlang.insert(default_char) 
                self.shift_buffer = ""
            else:
                self.shift_buffer = ""
        self.shift_btn.setChecked(False)

    def backspace(self):
        self.input_conlang.backspace()
        self.input_conlang.setFocus()
        if self.shift_buffer: self.shift_buffer = self.shift_buffer[:-1]

    def run_generator(self):
        word, structure = WordGenerator.generate_word()
        # Apply Header-specific visual fixes
        styled_word = apply_visual_fixes(word, mode='header')
        self.gen_result_display.setText(styled_word)
        self.gen_structure_display.setText(structure)
        # Apply Table-specific visual fixes to the Input box automatically via RichLineEdit
        self.input_conlang.setText(word)

    def add_entry(self):
        # Must grab plain text for storage, but rich text is purely for display
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
        self.gen_result_display.setText("...")
        self.gen_structure_display.setText("")

    def refresh_table(self, category):
        table = self.tables[category]
        items = self.data[category]
        table.setRowCount(0)
        self.stats_label.setText(f"Total Words: {sum(len(v) for v in self.data.values())}")
        
        for r, item in enumerate(items):
            table.insertRow(r)
            
            # Lore Word (Styled with Visual Fixes)
            lore_word_raw = item.get('conlang', '')
            lore_word_styled = apply_visual_fixes(lore_word_raw, mode='table')
            label = QLabel(lore_word_styled)
            label.setAlignment(Qt.AlignCenter)
            table.setCellWidget(r, 0, label)
            
            # English Definition (Standard)
            english_item = QTableWidgetItem(item.get('english', ''))
            english_item.setFont(QFont("Arial", 12))
            table.setItem(r, 1, english_item)
            
            # Notes (Standard)
            notes_item = QTableWidgetItem(item.get('notes', ''))
            notes_item.setFont(QFont("Arial", 12))
            table.setItem(r, 2, notes_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VocabVault()
    window.show()
    sys.exit(app.exec())
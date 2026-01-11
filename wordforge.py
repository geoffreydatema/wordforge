import sys
import json
import os
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTabWidget, QLineEdit, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QMessageBox, QGridLayout, QFrame, QLabel)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

# --- LORE CONFIGURATION ---
VOWELS = ['a', 'э', 'ʟ', 'o', 'h', 'ᴀ', 'и', 'ꭅ', 'ꟻ', 'ю', 'e', 'ᴇ', 'У', 'я', 's']
CONSONANTS = ['q', 'p', 'ᴛ', 'b', 'п', 'c', '⊿', 'v', 'г', 'x', 'd', 'ᴋ', 'ԉ', 'z', 'ʙ', 'Б', 'ʜ', 'ᴍ', 'ж', 'ц', 'ч', 'ш', 'ꚇ', 'Ұ', 'њ', 'Ꙗ', 'ԕ']

# Keyboard Layout: (Key ID, Display Label)
KEYBOARD_LAYOUT = [
    [('q', 'q'), ('w', 'э'), ('e', 'p'), ('r', 'ᴛ'), ('t', 'b'), ('y', 'h'), ('u', 'ʟ'), ('i', 'o'), ('o', 'п')],
    [('a', 'a'), ('s', 'c'), ('d', '⊿'), ('f', 'v'), ('g', 'г'), ('h', 'x'), ('j', 'd'), ('k', 'ᴋ'), ('l', 'ԉ')],
    [('z', 'z'), ('x', 'ʙ'), ('c', 'Б'), ('v', 'ʜ'), ('b', 'ᴍ')]
]

# MAP: Key Sequence -> Target Character
COMBO_MAP = {
    # SINGLE CHARACTERS (Long Vowels)
    "a": "ᴀ", 
    "w": "и", 
    "u": "ꭅ", 
    "i": "ꟻ", 
    "y": "ю",

    # CLUSTERS
    "ta": "я",  # ya
    "tw": "e",  # ye
    "ti": "ᴇ",  # yo
    "ii": "У",  # oo
    "iw": "s",  # oe
    "rs": "ц",  # ts
    "zh": "ж",  # zh
    "sh": "ш",  # sh
    "kh": "ч",  # ch
    "sk": "ꚇ",  # sk
    "rh": "Ұ",  # th (unvoiced)
    "jh": "њ",  # dh (voiced)
    "vg": "Ꙗ",  # ng
    "sr": "ԕ"   # st
}

class WordGenerator:
    @staticmethod
    def generate_word(min_syllables=1, max_syllables=3):
        word = ""
        syllables = random.randint(min_syllables, max_syllables)
        for i in range(syllables):
            structure = random.choice(["CV", "CVC", "VC", "CVV"])
            syllable = ""
            if structure == "CV":
                syllable = random.choice(CONSONANTS) + random.choice(VOWELS)
            elif structure == "CVC":
                syllable = random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(CONSONANTS)
            elif structure == "VC":
                syllable = random.choice(VOWELS) + random.choice(CONSONANTS)
            elif structure == "CVV":
                syllable = random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(VOWELS)
            word += syllable
        return word

class VocabVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Future Language Forge")
        self.resize(1200, 750)
        
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        
        self.filename = "future_lang.json"
        self.categories = ["dictionary", "phrases"]
        self.tables = {} 
        self.data = self.load_data()
        
        self.shift_active = False
        self.shift_buffer = ""
        
        self.setup_ui()

    def load_data(self):
        default_data = {cat: [] for cat in self.categories}
        if not os.path.exists(self.filename):
            return default_data
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return json.loads(content) if content else default_data
        except:
            return default_data

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # === LEFT PANEL ===
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(500)
        
        # Generator
        gen_group = QFrame()
        gen_group.setStyleSheet("background-color: #2b2b2b; border-radius: 8px; padding: 10px;")
        gen_layout = QVBoxLayout(gen_group)
        self.gen_result_display = QLabel("...")
        self.gen_result_display.setAlignment(Qt.AlignCenter)
        self.gen_result_display.setStyleSheet("font-size: 32px; color: white; margin: 10px;")
        self.gen_result_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        gen_layout.addWidget(self.gen_result_display)
        
        # GENERATE BUTTON (Blue Theme)
        btn_generate = QPushButton("Generate Random Word")
        btn_generate.clicked.connect(self.run_generator)
        btn_generate.setStyleSheet("""
            QPushButton { 
                background-color: #0277bd; 
                color: white; 
                padding: 8px; 
                border-radius: 4px; 
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #039be5; 
            }
            QPushButton:pressed { 
                background-color: #01579b; 
            }
        """)
        gen_layout.addWidget(btn_generate)
        left_layout.addWidget(gen_group)
        left_layout.addSpacing(10)

        # Manual Entry
        form_layout = QGridLayout()
        self.input_conlang = QLineEdit()
        self.input_conlang.setPlaceholderText("Lore Word")
        self.input_conlang.setStyleSheet("font-size: 24px; padding: 5px; font-weight: bold;")
        self.input_english = QLineEdit()
        self.input_english.setPlaceholderText("English Definition")
        self.input_notes = QLineEdit()
        self.input_notes.setPlaceholderText("Etymology / Root Notes")
        
        form_layout.addWidget(QLabel("Word:"), 0, 0)
        form_layout.addWidget(self.input_conlang, 0, 1)
        form_layout.addWidget(QLabel("Def:"), 1, 0)
        form_layout.addWidget(self.input_english, 1, 1)
        form_layout.addWidget(QLabel("Root:"), 2, 0)
        form_layout.addWidget(self.input_notes, 2, 1)
        left_layout.addLayout(form_layout)
        
        # SAVE BUTTON (Green Theme)
        self.add_button = QPushButton("Save to Dictionary")
        self.add_button.setMinimumHeight(45)
        self.add_button.setStyleSheet("""
            QPushButton { 
                background-color: #2e7d32; 
                color: white; 
                font-weight: bold; 
                border-radius: 4px; 
                font-size: 16px;
            }
            QPushButton:hover { 
                background-color: #388e3c; 
            }
            QPushButton:pressed { 
                background-color: #1b5e20; 
            }
        """)
        self.add_button.clicked.connect(self.add_entry)
        left_layout.addWidget(self.add_button)
        
        # Virtual Keyboard
        left_layout.addSpacing(15)
        left_layout.addWidget(QLabel("Touch Keyboard:"))
        keyboard = self.create_keyboard()
        left_layout.addWidget(keyboard)
        left_layout.addStretch()
        
        # === RIGHT PANEL ===
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
        
        # CSS Template for Keys
        KEY_STYLE = """
            QPushButton {{
                background-color: #444; 
                color: {color}; 
                border: 1px solid #555; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #555;
                border-color: #777;
            }}
            QPushButton:pressed {{
                background-color: #222;
                border-color: #333;
            }}
        """

        for row_data in KEYBOARD_LAYOUT:
            row = QHBoxLayout()
            row.setSpacing(4)
            row.addStretch() 
            for key_id, label in row_data:
                btn = QPushButton(label)
                btn.setFixedSize(45, 45)
                btn.setFont(QFont("Arial", 14))
                btn.clicked.connect(lambda ch=False, k=key_id, l=label: self.handle_keypress(k, l))
                
                # Apply Style with Color Injection
                text_color = "#ffab91" if label in VOWELS else "#81d4fa"
                btn.setStyleSheet(KEY_STYLE.format(color=text_color))
                
                row.addWidget(btn)
            row.addStretch()
            layout.addLayout(row)
            
        ctrl_row = QHBoxLayout()
        ctrl_row.addStretch()
        
        # SHIFT BUTTON STYLE
        self.shift_btn = QPushButton("SHIFT")
        self.shift_btn.setCheckable(True)
        self.shift_btn.setFixedSize(80, 45)
        self.shift_btn.setStyleSheet("""
            QPushButton { 
                background-color: #333; color: white; font-weight: bold; border: 1px solid #555; border-radius: 5px; 
            }
            QPushButton:hover { background-color: #444; border-color: #777; }
            QPushButton:checked { background-color: #ff9800; color: black; border-color: #e65100; }
        """)
        self.shift_btn.toggled.connect(self.toggle_shift)
        ctrl_row.addWidget(self.shift_btn)
        
        # CONTROL BUTTONS STYLE (Space/Back)
        CTRL_STYLE = """
            QPushButton { 
                background-color: #333; color: white; border: 1px solid #555; border-radius: 5px; 
            }
            QPushButton:hover { background-color: #444; border-color: #777; }
            QPushButton:pressed { background-color: #222; border-color: #111; }
        """
        
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
        
        if is_prefix:
            return
        
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
        if self.shift_buffer:
            self.shift_buffer = self.shift_buffer[:-1]

    def run_generator(self):
        word = WordGenerator.generate_word()
        self.gen_result_display.setText(word)
        self.input_conlang.setText(word)

    def add_entry(self):
        conlang = self.input_conlang.text().strip()
        english = self.input_english.text().strip()
        notes = self.input_notes.text().strip()
        
        if not conlang or not english:
            QMessageBox.warning(self, "Missing Info", "Need word and definition.")
            return

        cat = self.categories[self.tabs.currentIndex()]
        self.data[cat].append({
            "conlang": conlang, 
            "english": english, 
            "notes": notes
        })
        self.save_data()
        self.refresh_table(cat)
        self.input_conlang.clear()
        self.input_english.clear()
        self.input_notes.clear()
        self.gen_result_display.setText("...")

    def refresh_table(self, category):
        table = self.tables[category]
        items = self.data[category]
        table.setRowCount(0)
        self.stats_label.setText(f"Total Words: {sum(len(v) for v in self.data.values())}")
        for r, item in enumerate(items):
            table.insertRow(r)
            table.setItem(r, 0, QTableWidgetItem(item.get('conlang', '')))
            table.setItem(r, 1, QTableWidgetItem(item.get('english', '')))
            table.setItem(r, 2, QTableWidgetItem(item.get('notes', '')))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VocabVault()
    window.show()
    sys.exit(app.exec())
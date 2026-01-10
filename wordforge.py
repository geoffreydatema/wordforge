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
# 1. Define Categories for Procedural Generation
VOWELS = [
    'a', 'э', 'ʟ', 'o', 'h',   # Short
    'ᴀ', 'и', 'ꭅ', 'ꟻ', 'ю',   # Long
    'e', 'ᴇ', 'У', 'я', 's'    # Diphthongs/Special
]

CONSONANTS = [
    'Б', 'ʙ', 'г', '⊿', 'z', 'ᴋ', 'ԉ', 'ᴍ', 'ʜ', 'п', 
    'p', 'c', 'ᴛ', 'v', 'x', 'q', 'b', 'd', 'ж', 'ц', 
    'ч', 'ш', 'ꚇ', 'Ұ', 'њ', 'Ꙗ', 'ԕ'
]

# 2. Virtual Keyboard Mapping (Physical Key -> Lore Character)
KEY_MAP = {
    # Row 1 (Numbers row)
    '1': 'ᴀ', '2': 'и', '3': 'ꭅ', '4': 'ꟻ', '5': 'ю', '6': 'e', '7': 'ᴇ', '8': 'У', '9': 'я', '0': 's',
    # Row 2 (QWERTY)
    'q': 'q', 'w': 'q', 'e': 'э', 'r': 'p', 't': 'ᴛ', 'y': 'b', 'u': 'h', 'i': 'ʟ', 'o': 'o', 'p': 'п',
    # Row 3 (ASDF)
    'a': 'a', 's': 'c', 'd': '⊿', 'f': 'v', 'g': 'г', 'h': 'x', 'j': 'd', 'k': 'ᴋ', 'l': 'ԉ',
    # Row 4 (ZXCV)
    'z': 'z', 'x': 'ж', 'c': 'ц', 'v': 'ʙ', 'b': 'Б', 'n': 'ʜ', 'm': 'ᴍ'
}

class WordGenerator:
    """Handles the logic for creating new words based on lore rules."""
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

        # === LEFT PANEL: INPUT & GENERATOR ===
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(450)
        
        # 1. Title
        title = QLabel("Word Forge")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        left_layout.addWidget(title)

        # 2. Generator Controls
        gen_group = QFrame()
        gen_group.setStyleSheet("background-color: #2b2b2b; border-radius: 8px; padding: 10px;")
        gen_layout = QVBoxLayout(gen_group)
        
        gen_label = QLabel("Procedural Generator")
        gen_label.setStyleSheet("color: #4fc3f7; font-weight: bold;")
        gen_layout.addWidget(gen_label)
        
        self.gen_result_display = QLabel("...")
        self.gen_result_display.setAlignment(Qt.AlignCenter)
        self.gen_result_display.setStyleSheet("font-size: 32px; color: white; margin: 10px;")
        self.gen_result_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        gen_layout.addWidget(self.gen_result_display)
        
        btn_generate = QPushButton("Generate Random Word")
        btn_generate.clicked.connect(self.run_generator)
        btn_generate.setStyleSheet("background-color: #0277bd; color: white; padding: 8px;")
        gen_layout.addWidget(btn_generate)
        
        left_layout.addWidget(gen_group)
        left_layout.addSpacing(20)

        # 3. Manual Entry Fields
        form_layout = QGridLayout()
        
        self.input_conlang = QLineEdit()
        self.input_conlang.setPlaceholderText("Lore Word")
        self.input_conlang.setStyleSheet("font-size: 18px; padding: 5px;")
        
        self.input_english = QLineEdit()
        self.input_english.setPlaceholderText("English Definition")
        
        self.input_notes = QLineEdit()
        self.input_notes.setPlaceholderText("Etymology / Root Notes (Optional)")
        
        form_layout.addWidget(QLabel("Word:"), 0, 0)
        form_layout.addWidget(self.input_conlang, 0, 1)
        form_layout.addWidget(QLabel("Def:"), 1, 0)
        form_layout.addWidget(self.input_english, 1, 1)
        form_layout.addWidget(QLabel("Root:"), 2, 0)
        form_layout.addWidget(self.input_notes, 2, 1)
        
        left_layout.addLayout(form_layout)
        
        # 4. Add Button
        self.add_button = QPushButton("Save to Dictionary")
        self.add_button.setMinimumHeight(45)
        self.add_button.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold;")
        self.add_button.clicked.connect(self.add_entry)
        left_layout.addWidget(self.add_button)
        
        # 5. Virtual Keyboard
        left_layout.addSpacing(20)
        left_layout.addWidget(QLabel("Alphabet Input:"))
        keyboard = self.create_keyboard()
        left_layout.addWidget(keyboard)
        
        left_layout.addStretch()
        
        # === RIGHT PANEL: DICTIONARY ===
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tabs
        self.tabs = QTabWidget()
        for category in self.categories:
            tab = QWidget()
            t_layout = QVBoxLayout(tab)
            table = QTableWidget()
            table.setColumnCount(3) # Removed Score column
            table.setHorizontalHeaderLabels(["Lore Word", "Definition", "Notes"])
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            
            self.tables[category] = table
            t_layout.addWidget(table)
            self.tabs.addTab(tab, category.title())
            
        right_layout.addWidget(self.tabs)
        
        # Status Bar (Total Words)
        status_layout = QHBoxLayout()
        self.stats_label = QLabel("Total Words: 0")
        self.stats_label.setStyleSheet("color: #888; font-weight: bold;")
        status_layout.addWidget(self.stats_label)
        status_layout.addStretch()
        right_layout.addLayout(status_layout)
        
        # Assemble Main Layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        # Load initial data
        for category in self.categories:
            self.refresh_table(category)

    def create_keyboard(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(2)
        
        # Helper to make a row
        def make_row(chars):
            row = QHBoxLayout()
            row.setSpacing(2)
            for char in chars:
                btn = QPushButton(char)
                btn.setFixedSize(32, 32)
                btn.clicked.connect(lambda ch=False, c=char: self.insert_char(c))
                # Style Consonants differently from Vowels
                if char in VOWELS:
                    btn.setStyleSheet("color: #ffab91; font-weight: bold;") # Reddish
                elif char in CONSONANTS:
                    btn.setStyleSheet("color: #81d4fa; font-weight: bold;") # Blueish
                row.addWidget(btn)
            row.addStretch()
            return row

        # Row 1: Short Vowels
        layout.addLayout(make_row(['a', 'э', 'ʟ', 'o', 'h']))
        # Row 2: Long Vowels
        layout.addLayout(make_row(['ᴀ', 'и', 'ꭅ', 'ꟻ', 'ю']))
        # Row 3: Special/Diphthongs
        layout.addLayout(make_row(['e', 'ᴇ', 'У', 'я', 's']))
        # Row 4: Common Consonants (Labials/Dentals)
        layout.addLayout(make_row(['Б', 'ʙ', 'г', '⊿', 'z', 'ᴋ', 'ԉ', 'ᴍ', 'ʜ']))
        # Row 5: Fricatives/Liquids
        layout.addLayout(make_row(['п', 'p', 'c', 'ᴛ', 'v', 'x', 'q', 'b', 'd']))
        # Row 6: Complex/Clusters
        layout.addLayout(make_row(['ж', 'ц', 'ч', 'ш', 'ꚇ', 'Ұ', 'њ', 'Ꙗ', 'ԕ']))
        
        # Space / Backspace row
        ctrl_row = QHBoxLayout()
        btn_space = QPushButton("Space")
        btn_space.clicked.connect(lambda: self.insert_char(" "))
        btn_back = QPushButton("⌫")
        btn_back.clicked.connect(self.backspace)
        ctrl_row.addWidget(btn_space)
        ctrl_row.addWidget(btn_back)
        layout.addLayout(ctrl_row)
        
        return container

    def insert_char(self, char):
        self.input_conlang.insert(char)
        self.input_conlang.setFocus()

    def backspace(self):
        self.input_conlang.backspace()
        self.input_conlang.setFocus()

    def run_generator(self):
        # Generate word and put it in the display label
        word = WordGenerator.generate_word()
        self.gen_result_display.setText(word)
        # Also auto-fill the input box for convenience
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
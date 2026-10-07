import sys
import json
import os
import random
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTabWidget, QLineEdit, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QMessageBox, QGridLayout, QFrame, QLabel, QTextEdit,
                               QSlider, QTextBrowser, QMenu, QComboBox, QDialog, QScrollArea, QFileDialog)
from PySide6.QtGui import QFont, QTextCursor, QPainter, QPixmap, QColor, QTextBlockFormat, QFontDatabase
from PySide6.QtCore import Qt, QObject, QEvent, Signal

# ========================================================
#       MASTER CHARACTER SET
#
#       aэջohяиეεyδюбвгдzкλмнпpcтvxqьμжчшθdфբζՑцპსպըէთრც
#       
# ========================================================

def load_spec():
    try:
        with open('tezhnor_spec.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load tezhnor_spec.json: {e}")
        sys.exit(1)

SPEC = load_spec()

def load_shigeyed_spec():
    try:
        with open('shigeyed_spec.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load shigeyed_spec.json: {e}")
        return {"shigeyed_to_code": {}, "code_to_shigeyed": {}}

SHIGEYED_SPEC = load_shigeyed_spec()
SHIGEYED_TO_CODE = SHIGEYED_SPEC.get("shigeyed_to_code", {})
CODE_TO_SHIGEYED = SHIGEYED_SPEC.get("code_to_shigeyed", {})
SHIGEYED_VOWELS = set(SHIGEYED_SPEC.get("vowels", []))
SHIGEYED_CONSONANTS = set(SHIGEYED_SPEC.get("consonants", []))
TEZHNOR_VOWEL_MAP = SHIGEYED_SPEC.get("tezhnor_vowel_map", {})
TEZHNOR_CONSONANT_MAP = SHIGEYED_SPEC.get("tezhnor_consonant_map", {})
SYLLABLES_BY_CONSONANT = SHIGEYED_SPEC.get("shigeyed_categories", {})

TEZHNOR_TO_CODE = SPEC["tezhnor_to_code"]
CODE_TO_TEZHNOR = SPEC["code_to_tezhnor"]
TEZHNOR_TO_PRONUNCIATION = SPEC["tezhnor_to_pronunciation"]
VOWELS = SPEC["vowels"]
CONSONANTS = SPEC["consonants"]

ASCII_TO_SYMBOL = SPEC.get("ascii_to_symbol", {})

SORTED_ASCII_KEYS = sorted(ASCII_TO_SYMBOL.keys(), key=len, reverse=True)

escaped_keys = [re.escape(k) for k in SORTED_ASCII_KEYS]
SYMBOL_REGEX_PATTERN = f"(<---->|\\s+|{'|'.join(escaped_keys)})" if escaped_keys else "(<---->|\\s+)"

TYPER_CHAR_TO_SYMBOL_NAME = ASCII_TO_SYMBOL.copy()

CHAR_TO_FILENAME = TEZHNOR_TO_CODE.copy()

RAW_PIXMAP_CACHE = {}
SCALED_PIXMAP_CACHE = {}

LOADED_UNICODE_FONTS = ["Arial - Regular", "Arial - Bold"] # Default fallbacks

def preload_font_pixmaps():
    """Loads all raw bitmap images into memory once at startup, avoiding disk I/O later."""
    for font_key, profile in FONT_PROFILES.items():
        font_dir = profile["dir"]
        
        mapping = SHIGEYED_TO_CODE if "shigeyed" in font_dir.lower() else CHAR_TO_FILENAME
        for char, filename in mapping.items():
            image_path = os.path.join(font_dir, f"{filename}.png")
            if os.path.exists(image_path):
                RAW_PIXMAP_CACHE[(char, font_dir)] = QPixmap(image_path)
                
        for char, symbol_name in TYPER_CHAR_TO_SYMBOL_NAME.items():
            image_path = os.path.join(font_dir, f"{symbol_name}.png")
            if os.path.exists(image_path):
                RAW_PIXMAP_CACHE[(char, font_dir)] = QPixmap(image_path)

def load_unicode_fonts():
    """Loads custom TTF fonts and extracts exact Family + Style combinations."""
    LOADED_UNICODE_FONTS.clear()
    LOADED_UNICODE_FONTS.extend(["Arial - Regular", "Arial - Bold"])
    
    ttf_files = [
        "NotoSansTezhnor_Bold.ttf",
        "NotoSansTezhnor_Light.ttf",
        "NotoSansTezhnor_Regular.ttf",
        "NotoSerifTezhnor_Bold.ttf",
        "NotoSerifTezhnor_Light.ttf",
        "NotoSerifTezhnor_Regular.ttf"
    ]
    families = set()
    for ttf in ttf_files:
        path = ttf if os.path.exists(ttf) else os.path.join("fonts", ttf)
        if os.path.exists(path):
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id != -1:
                for family in QFontDatabase.applicationFontFamilies(font_id):
                    families.add(family)
                    
    for family in sorted(list(families)):
        for style in QFontDatabase.styles(family):
            LOADED_UNICODE_FONTS.append(f"{family} - {style}")

def get_shared_pixmap(char, font_dir, scale):
    """Returns the scaled pixmap, utilizing the in-memory caches."""
    cache_key = (char, font_dir, scale)
    if cache_key in SCALED_PIXMAP_CACHE:
        return SCALED_PIXMAP_CACHE[cache_key]
    
    raw_key = (char, font_dir)
    orig_pixmap = RAW_PIXMAP_CACHE.get(raw_key)
    
    if orig_pixmap:
        target_width = int(orig_pixmap.width() * scale)
        target_height = int(orig_pixmap.height() * scale)
        
        scaled_pixmap = orig_pixmap.scaled(
            target_width, 
            target_height, 
            Qt.IgnoreAspectRatio, 
            Qt.SmoothTransformation
        )
        
        SCALED_PIXMAP_CACHE[cache_key] = scaled_pixmap
        return scaled_pixmap
        
    return None

LORE_TO_PRON = TEZHNOR_TO_CODE.copy()

FONT_PROFILES = {
    "Rounded Regular": {
        "dir": "fonts/tezhnor_rounded_regular",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.18,
        "line_height": 210,
        "space_width": 60,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 12
    },
    "Rounded Bold": {
        "dir": "fonts/tezhnor_rounded_bold", 
        "text_base_pt": 28,
        "bitmap_base_scale": 0.18,
        "line_height": 210,
        "space_width": 60,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 12
    },
    "Block Regular": {
        "dir": "fonts/tezhnor_block_regular",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.18,
        "line_height": 210,
        "space_width": 60,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 12
    },
    "Block Mono": {
        "dir": "fonts/tezhnor_block_mono",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.18,
        "line_height": 210,
        "space_width": 103,    
        "advance_normal": 103, 
        "advance_square": 103, 
        "advance_wide": 103,   
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 12
    },
    "Block Extended": {
        "dir": "fonts/tezhnor_block_mono_extended",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.18,
        "line_height": 210,
        "space_width": 128,    
        "advance_normal": 128, 
        "advance_square": 128, 
        "advance_wide": 128,   
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 12
    },
    "Block Monoheight": {
        "dir": "fonts/tezhnor_block_monoheight",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.18,
        "line_height": 210,
        "space_width": 60,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 12
    },
    "Shigeyed Bold": {
        "dir": "fonts/shigeyed_bold",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.14,
        "symbol_scale": 2.0,
        "symbol_offset_y": 77,
        "advance_symbol": 103,
        "line_height": 400,
        "space_width": 80,
        "advance_normal": 0,
        "advance_square": 0,
        "advance_wide": 250,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 20
    }
}

CURRENT_FONT_KEY = "Rounded Bold"
FONT_METRICS = FONT_PROFILES[CURRENT_FONT_KEY]

CHAR_WIDTHS = {
    CODE_TO_TEZHNOR["o"]: "advance_square",
    CODE_TO_TEZHNOR["ue"]: "advance_square",
    CODE_TO_TEZHNOR["d"]: "advance_square",
    CODE_TO_TEZHNOR["m"]: "advance_square",
    CODE_TO_TEZHNOR["zh"]: "advance_wide",
    CODE_TO_TEZHNOR["sh"]: "advance_wide",
    CODE_TO_TEZHNOR["th"]: "advance_square",
    CODE_TO_TEZHNOR["sk"]: "advance_wide",
    CODE_TO_TEZHNOR["ts"]: "advance_square",
    CODE_TO_TEZHNOR["kv"]: "advance_square",
    CODE_TO_TEZHNOR["sv"]: "advance_wide",
    CODE_TO_TEZHNOR["zv"]: "advance_wide",
}

KEYBOARD_LAYOUT = [
    [('w', CODE_TO_TEZHNOR['w']), ('e', CODE_TO_TEZHNOR['e']), ('r', CODE_TO_TEZHNOR['r']), ('t', CODE_TO_TEZHNOR['t']), ('y', CODE_TO_TEZHNOR['y']), ('u', CODE_TO_TEZHNOR['u']), ('i', CODE_TO_TEZHNOR['i']), ('o', CODE_TO_TEZHNOR['o']), ('p', CODE_TO_TEZHNOR['p'])],
    [('a', CODE_TO_TEZHNOR['a']), ('s', CODE_TO_TEZHNOR['s']), ('d', CODE_TO_TEZHNOR['d']), ('f', CODE_TO_TEZHNOR['f']), ('g', CODE_TO_TEZHNOR['g']), ('h', CODE_TO_TEZHNOR['h']), ('j', CODE_TO_TEZHNOR['j']), ('k', CODE_TO_TEZHNOR['k']), ('l', CODE_TO_TEZHNOR['l'])],
    [('z', CODE_TO_TEZHNOR['z']), ('x', CODE_TO_TEZHNOR['kh']), ('c', CODE_TO_TEZHNOR['shch']), ('v', CODE_TO_TEZHNOR['v']), ('b', CODE_TO_TEZHNOR['b']), ('n', CODE_TO_TEZHNOR['n']), ('m', CODE_TO_TEZHNOR['m'])]
]

COMBO_MAP = {
    "ay": CODE_TO_TEZHNOR['ay'], "ee": CODE_TO_TEZHNOR['ee'], "iy": CODE_TO_TEZHNOR['iy'], 
    "ow": CODE_TO_TEZHNOR['ow'], "oo": CODE_TO_TEZHNOR['oo'], "oe": CODE_TO_TEZHNOR['oe'], 
    "ue": CODE_TO_TEZHNOR['ue'],
    "zh": CODE_TO_TEZHNOR['zh'], "sh": CODE_TO_TEZHNOR['sh'], "ch": CODE_TO_TEZHNOR['ch'], 
    "th": CODE_TO_TEZHNOR['th'], "dh": CODE_TO_TEZHNOR['dh'], "ng": CODE_TO_TEZHNOR['ng'], 
    "kr": CODE_TO_TEZHNOR['kr'], "rr": CODE_TO_TEZHNOR['rr'],
    "ts": CODE_TO_TEZHNOR['ts'], "st": CODE_TO_TEZHNOR['st'],
    "ks": CODE_TO_TEZHNOR['ks'], "sk": CODE_TO_TEZHNOR['sk'],
    "kv": CODE_TO_TEZHNOR['kv'], "sv": CODE_TO_TEZHNOR['sv'], "zv": CODE_TO_TEZHNOR['zv'], 
    "dv": CODE_TO_TEZHNOR['dv']
}

DISABLED_KEYS = ['q']

class BitmapRenderer(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_to_render = ""
        
        self.font_dir = FONT_PROFILES[CURRENT_FONT_KEY]["dir"]
        self.base_scale = FONT_PROFILES[CURRENT_FONT_KEY]["bitmap_base_scale"]
        
        self.scale = self.base_scale
        self.lh_factor = 1.0
        self.char_spacing = 0

    def get_current_metrics(self):
        for profile in FONT_PROFILES.values():
            if profile["dir"] == self.font_dir:
                return profile
        return FONT_PROFILES[CURRENT_FONT_KEY]

    def update_settings(self, scale_factor, lh_factor, char_spacing):
        metrics = self.get_current_metrics()
        self.base_scale = metrics.get("bitmap_base_scale", 1.0)
        self.scale = scale_factor * self.base_scale
        self.lh_factor = lh_factor
        self.char_spacing = char_spacing
        self.update()

    def set_text(self, new_text):
        self.text_to_render = new_text
        self.update() 

    def get_pixmap(self, char, custom_scale=None):
        active_scale = custom_scale if custom_scale is not None else self.scale
        return get_shared_pixmap(char, self.font_dir, active_scale)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#2b2b2b"))
        self._draw_layout(painter)

    def export_to_pixmap(self):
        # 1. Do a dry-run to find the exact boundary size of the text
        width, height = self._draw_layout(painter=None)
        
        # 2. Create a blank image of that exact size and fill it with solid black
        export_pix = QPixmap(width, height)
        export_pix.fill(QColor("black"))
        
        # 3. Draw the exact same text layout directly onto the image
        painter = QPainter(export_pix)
        self._draw_layout(painter)
        painter.end()
        
        return export_pix

    def _draw_layout(self, painter=None):
        """Unified math engine: draws to screen if painter is provided, otherwise calculates bounding box."""
        metrics = self.get_current_metrics()
        
        dynamic_lh = (metrics["line_height"] * self.lh_factor) * self.scale
        scaled_space_width = metrics["space_width"] * self.scale
        
        PADDING_SCREEN = metrics.get("padding", 10)
        OFFSET_X = metrics.get("bitmap_offset_x", 0)
        OFFSET_Y = metrics.get("bitmap_offset_y", 0)
        
        BASE_SPACING_SCALED = metrics.get("bitmap_base_char_spacing", 0) * self.scale
        effective_char_spacing = self.char_spacing + BASE_SPACING_SCALED
        
        max_x = self.width() - (PADDING_SCREEN + OFFSET_X)
        
        cursor_x = PADDING_SCREEN + OFFSET_X
        cursor_y = PADDING_SCREEN + OFFSET_Y
        
        is_shigeyed = "shigeyed" in self.font_dir.lower()
        
        iterable = []
        raw_tokens = [t for t in re.split(SYMBOL_REGEX_PATTERN, self.text_to_render) if t]
        
        for token in raw_tokens:
            if token in TYPER_CHAR_TO_SYMBOL_NAME or token == "<---->":
                iterable.append(token)
            elif token.isspace():
                iterable.extend(list(token))
            else:
                if is_shigeyed:
                    syls = token.split('·')
                    for s in syls:
                        if s: iterable.append(s)
                else:
                    iterable.extend(list(token))
                    
        actual_max_x = cursor_x
        actual_max_y = cursor_y + dynamic_lh
        
        for item in iterable:
            if item == '\n':
                cursor_x = PADDING_SCREEN + OFFSET_X 
                cursor_y += dynamic_lh
                actual_max_y = max(actual_max_y, cursor_y + dynamic_lh)
                continue
                
            if item == ' ':
                cursor_x += scaled_space_width + effective_char_spacing
                if cursor_x > max_x:
                    cursor_x = PADDING_SCREEN + OFFSET_X 
                    cursor_y += dynamic_lh
                    actual_max_y = max(actual_max_y, cursor_y + dynamic_lh)
                actual_max_x = max(actual_max_x, cursor_x)
                continue
                
            is_symbol = item in TYPER_CHAR_TO_SYMBOL_NAME
            
            if is_symbol:
                width_key = "advance_symbol"
                symbol_multiplier = metrics.get("symbol_scale", 1.0)
                current_item_scale = self.scale * symbol_multiplier
            elif len(item) > 1:
                width_key = "advance_wide"
                current_item_scale = self.scale
            else:
                width_key = CHAR_WIDTHS.get(item, "advance_normal")
                current_item_scale = self.scale
                
            raw_advance = metrics.get(width_key, 103)
            advance = (raw_advance * current_item_scale) + effective_char_spacing
            
            if cursor_x + advance > max_x:
                cursor_x = PADDING_SCREEN + OFFSET_X 
                cursor_y += dynamic_lh
                actual_max_y = max(actual_max_y, cursor_y + dynamic_lh)
                
            pixmap = self.get_pixmap(item, current_item_scale)
            if pixmap:
                active_y = cursor_y
                
                if is_shigeyed and is_symbol:
                    standard_shig_height = 256 * self.scale
                    active_y += (standard_shig_height - pixmap.height())
                    
                if is_symbol:
                    raw_y_offset = metrics.get("symbol_offset_y", 0)
                    active_y += (raw_y_offset * self.scale)
                    
                if painter:
                    painter.drawPixmap(int(cursor_x), int(active_y), pixmap)
                    
                actual_max_y = max(actual_max_y, active_y + pixmap.height())
                
            cursor_x += advance
            actual_max_x = max(actual_max_x, cursor_x)
            
        return int(actual_max_x + PADDING_SCREEN), int(actual_max_y + PADDING_SCREEN)

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
            self.textCursor().insertText(source.text())
        else:
            super().insertFromMimeData(source)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.returnPressed.emit()
            return 
        super().keyPressEvent(event)

    def setText(self, text):
        self.setPlainText(text)
        self.moveCursor(QTextCursor.End)
        
    def text(self):
        return self.toPlainText()
        
    def insert(self, text):
        self.textCursor().insertText(text)
        
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

class TyperTextEdit(RichLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(16777215) 
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        self.line_height_factor = 1.0
        self.char_spacing = 0
        self.font_family = "Arial"
        
        self.textChanged.connect(self.apply_block_formatting)
        self.update_font_settings(0.5, 1.0, 0, "Arial - Regular")

    def update_font_settings(self, scale_factor, lh_factor, char_spacing, font_selection="Arial - Regular"):
        self.line_height_factor = lh_factor
        self.char_spacing = char_spacing
        self.font_selection = font_selection

        self.base_pt = FONT_METRICS.get("text_base_pt", 28) 
        current_pt = max(8, int(self.base_pt * scale_factor))
        pad = FONT_METRICS.get("padding", 10) 
        
        if " - " in font_selection:
            family, style_str = font_selection.split(" - ", 1)
        else:
            family, style_str = font_selection, "Regular"
            
        # Get the exact font object directly from Qt's database
        new_font = QFontDatabase.font(family, style_str, current_pt)
        
        # Store the font so we can use it in apply_block_formatting
        self.active_custom_font = new_font 
        
        # Apply it cleanly to the widget and document
        self.setFont(new_font)
        self.document().setDefaultFont(new_font)
        
        # Only use CSS for the box styling now
        self.setStyleSheet(f"""
            QTextEdit {{
                padding: {pad}px;  
                border: 1px solid #555; 
                border-radius: 2px;
                background-color: #2b2b2b; 
                color: white;
            }}
        """)
        
        self.apply_block_formatting()

    def apply_block_formatting(self):
        self.blockSignals(True)
        
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        
        # 1. Apply Line Height
        block_fmt = cursor.blockFormat()
        block_fmt.setLineHeight(float(self.line_height_factor * 100), QTextBlockFormat.ProportionalHeight.value)
        cursor.setBlockFormat(block_fmt)
        
        # 2. Apply Character Spacing & Font
        char_fmt = cursor.charFormat()
        
        # --- FIX: Explicitly apply the font to the characters so old fonts don't get stuck! ---
        if hasattr(self, 'active_custom_font'):
            char_fmt.setFont(self.active_custom_font)
        
        if self.char_spacing == 0:
            char_fmt.setFontLetterSpacingType(QFont.PercentageSpacing)
            char_fmt.setFontLetterSpacing(100.0)
        else:
            char_fmt.setFontLetterSpacingType(QFont.AbsoluteSpacing)
            char_fmt.setFontLetterSpacing(float(self.char_spacing))
            
        cursor.mergeCharFormat(char_fmt)
        
        self.blockSignals(False)

    def keyPressEvent(self, event):
        QTextEdit.keyPressEvent(self, event)
        
    def insert(self, text):
        self.textCursor().insertText(text)
        
    def setText(self, text):
        self.setPlainText(text)
        self.moveCursor(QTextCursor.End)

class WordGenerator:
    @staticmethod
    def generate_word(num_syllables=3):
        word = ""
        structure_log = [] 
        pronunciation_log = []
        
        def get_c(exclude=None):
            opts = [c for c in CONSONANTS if c != exclude] if exclude else CONSONANTS
            return random.choice(opts) if opts else random.choice(CONSONANTS)

        def get_v(exclude=None):
            opts = [v for v in VOWELS if v != exclude] if exclude else VOWELS
            return random.choice(opts) if opts else random.choice(VOWELS)
        
        for i in range(num_syllables):
            structure = random.choices(
                ["V", "CV", "VC", "CVC", "CVV", "CCV", "VCC"], 
                weights=[10, 30, 10, 25, 5, 15, 5], 
                k=1
            )[0]
            
            prev_char = word[-1] if word else None
            
            if prev_char in VOWELS and structure in ["V", "VC", "VCC", "CVV"]:
                structure = random.choice(["CV", "CVC", "CCV"])
            
            structure_log.append(structure)
            syllable = ""
            
            if structure == "V":
                syllable = get_v(exclude=prev_char)
                
            elif structure == "CV":
                syllable = get_c(exclude=prev_char) + get_v()
                
            elif structure == "CVC":
                c1 = get_c(exclude=prev_char)
                v = get_v()
                c2 = get_c(exclude=v)
                syllable = c1 + v + c2
                
            elif structure == "VC":
                v = get_v(exclude=prev_char)
                syllable = v + get_c(exclude=v)
                
            elif structure == "CVV":
                c = get_c(exclude=prev_char)
                v1 = get_v()
                v2 = get_v(exclude=v1) 
                syllable = c + v1 + v2
                
            elif structure == "CCV":
                c1 = get_c(exclude=prev_char)
                c2 = get_c(exclude=c1)
                syllable = c1 + c2 + get_v()
                
            elif structure == "VCC":
                v = get_v(exclude=prev_char)
                c1 = get_c(exclude=v)
                c2 = get_c(exclude=c1)
                syllable = v + c1 + c2

            word += syllable

            pron_syl = "".join([LORE_TO_PRON.get(char, "?") for char in syllable])
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
                
        for ascii_key in TYPER_CHAR_TO_SYMBOL_NAME.keys():
            if len(ascii_key) == 1:
                self.key_map[ascii_key.lower()] = ascii_key

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key_text = event.text().lower()
            
            if event.modifiers() & Qt.ControlModifier: 
                return False

            if event.key() == Qt.Key_Backspace:
                obj.backspace() 
                return True 
                
            if event.key() == Qt.Key_Space:
                obj.insertPlainText(" ") 
                return True

            if key_text in DISABLED_KEYS: 
                return True 
            
            if key_text in self.key_map:
                lore_char = self.key_map[key_text]
                self.window.handle_keypress(key_text, lore_char, target=obj)
                return True 
                
        return super().eventFilter(obj, event)

class Wordforge(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Forge")
        self.resize(1200, 750)
        font = QFont("Arial", 12)
        self.setFont(font)
        self.filename = "dictionary.json"
        self.categories = ["level0", "level1", "level2+"]
        self.tables = {} 
        self.data = self.load_data()

        preload_font_pixmaps()
        load_unicode_fonts()
        
        self.key_to_lore = {}
        for row in KEYBOARD_LAYOUT:
            for k, char in row:
                self.key_to_lore[k] = char
        
        self.setup_ui()
        self.key_filter = PhysicalKeyFilter(self)
        self.input_conlang.installEventFilter(self.key_filter)
        self.typer_input.installEventFilter(self.key_filter)

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
        
        main_layout = QVBoxLayout(central_widget)
        
        self.top_tabs = QTabWidget()
        tab_font = QFont("Arial", 14, QFont.Normal)
        self.top_tabs.setFont(tab_font)
        main_layout.addWidget(self.top_tabs)

        # ==========================================
        # 1. WORDFORGE TAB
        # ==========================================
        wordforge_top_tab = QWidget()
        wf_top_layout = QHBoxLayout(wordforge_top_tab)

        # --- LEFT PANEL: Tools ---
        left_panel = QWidget()
        left_panel.setFixedWidth(550) 
        forge_layout = QVBoxLayout(left_panel)
        
        gen_group = QFrame()
        gen_group.setStyleSheet("background-color: #2b2b2b; border-radius: 8px; padding: 10px;")
        gen_layout = QVBoxLayout(gen_group)
        self.gen_result_display = QLabel("...")
        self.gen_result_display.setAlignment(Qt.AlignCenter)
        self.gen_result_display.setFixedHeight(80) 
        self.gen_result_display.setStyleSheet("color: white; margin-top: 10px; font-size: 32px;") 
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
        forge_layout.addLayout(kbd_header_layout)
        
        keyboard = self.create_keyboard()
        forge_layout.addWidget(keyboard)
        forge_layout.addStretch()
        
        wf_top_layout.addWidget(left_panel)

        # --- RIGHT PANEL: Dictionary ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.tabs = QTabWidget() 
        for category in self.categories:
            tab = QWidget()
            t_layout = QVBoxLayout(tab)
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Lore Word", "Definition", "Notes", ""])
            
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
        
        wf_top_layout.addWidget(right_panel)
        self.top_tabs.addTab(wordforge_top_tab, "Wordforge")

        # ==========================================
        # 3. SPECS TAB
        # ==========================================
        specs_tab = QWidget()
        specs_layout = QVBoxLayout(specs_tab)
        
        self.specs_subtabs = QTabWidget()
        
        # --- TEZHNOR SUBTAB ---
        def_tab = QWidget()
        def_layout = QVBoxLayout(def_tab)
        
        self.def_table = QTableWidget()
        self.def_table.setColumnCount(4)
        self.def_table.setHorizontalHeaderLabels(["Character", "Unicode", "Romanization", "Notes"])
        
        def_header = self.def_table.horizontalHeader()
        def_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        def_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        def_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        def_header.setSectionResizeMode(3, QHeaderView.Stretch)
        
        self.def_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.def_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.def_table.verticalHeader().setVisible(False)
        self.def_table.verticalHeader().setDefaultSectionSize(45) 
        self.def_table.setStyleSheet("background-color: #2b2b2b; color: white; gridline-color: #444;")
        
        self.def_table.setRowCount(len(TEZHNOR_TO_CODE))
        row_idx = 0
        
        definition_font = "Rounded Bold" 
        current_font_dir = FONT_PROFILES[definition_font]["dir"]
        base_scale = FONT_PROFILES[definition_font]["bitmap_base_scale"]
        table_icon_scale = base_scale * 0.65 
        
        for char, code in TEZHNOR_TO_CODE.items():
            lbl = QLabel()
            pixmap = get_shared_pixmap(char, current_font_dir, table_icon_scale)
            if pixmap: lbl.setPixmap(pixmap)
            lbl.setAlignment(Qt.AlignCenter)
            
            char_item = QTableWidgetItem(char)
            char_item.setTextAlignment(Qt.AlignCenter)
            char_item.setFont(QFont("Arial", 16))
            
            code_item = QTableWidgetItem(code)
            code_item.setTextAlignment(Qt.AlignCenter)
            code_item.setFont(QFont("Arial", 12))
            
            notes_text = TEZHNOR_TO_PRONUNCIATION.get(char, "")
            notes_item = QTableWidgetItem(notes_text)
            notes_item.setFont(QFont("Arial", 11))
            notes_item.setForeground(QColor("#bbb"))
            
            self.def_table.setCellWidget(row_idx, 0, lbl)
            self.def_table.setItem(row_idx, 1, char_item)
            self.def_table.setItem(row_idx, 2, code_item)
            self.def_table.setItem(row_idx, 3, notes_item)
            row_idx += 1
            
        self.def_table.setSortingEnabled(True)
        def_layout.addWidget(self.def_table)
        self.specs_subtabs.addTab(def_tab, "Tezhnor")

        # --- SHIGEYED SUBTAB ---
        shig_tab = QWidget()
        shig_layout = QVBoxLayout(shig_tab)
        
        self.shig_table = QTableWidget()
        self.shig_table.setColumnCount(3)
        self.shig_table.setHorizontalHeaderLabels(["Character", "Tezhnor", "Romanization"])
        
        shig_header = self.shig_table.horizontalHeader()
        shig_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        shig_header.setSectionResizeMode(1, QHeaderView.Stretch)
        shig_header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.shig_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.shig_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.shig_table.verticalHeader().setVisible(False)
        self.shig_table.verticalHeader().setDefaultSectionSize(45)
        self.shig_table.setStyleSheet("background-color: #2b2b2b; color: white; gridline-color: #444;")
        
        self.shig_table.setRowCount(len(SHIGEYED_TO_CODE))
        s_row_idx = 0
        
        shig_font_dir = FONT_PROFILES["Shigeyed Bold"]["dir"]
        shig_scale = FONT_PROFILES["Shigeyed Bold"]["bitmap_base_scale"] * 0.65
        
        for char, code in SHIGEYED_TO_CODE.items():
            lbl = QLabel()
            pixmap = get_shared_pixmap(char, shig_font_dir, shig_scale)
            if pixmap: lbl.setPixmap(pixmap)
            lbl.setAlignment(Qt.AlignCenter)
            
            char_item = QTableWidgetItem(char)
            char_item.setTextAlignment(Qt.AlignCenter)
            char_item.setFont(QFont("Arial", 16))
            
            code_item = QTableWidgetItem(code)
            code_item.setTextAlignment(Qt.AlignCenter)
            code_item.setFont(QFont("Arial", 12))
            
            self.shig_table.setCellWidget(s_row_idx, 0, lbl)
            self.shig_table.setItem(s_row_idx, 1, char_item)
            self.shig_table.setItem(s_row_idx, 2, code_item)
            s_row_idx += 1
            
        self.shig_table.setSortingEnabled(True)
        shig_layout.addWidget(self.shig_table)
        self.specs_subtabs.addTab(shig_tab, "Shigeyed")

        specs_layout.addWidget(self.specs_subtabs)
        self.top_tabs.addTab(specs_tab, "Specs")
        
        # ==========================================
        # 2. TRANSLATE TAB
        # ==========================================
        translator_tab = QWidget()
        translator_layout = QHBoxLayout(translator_tab) 

        # --- LEFT SIDE: Editors ---
        left_editors_widget = QWidget()
        left_editors_layout = QVBoxLayout(left_editors_widget)
        left_editors_layout.setContentsMargins(0, 0, 10, 0) 

        label_style = "color: #ccc; font-weight: bold; font-size: 11pt; margin-top: 5px;"

        lbl_eng = QLabel("English Source")
        lbl_eng.setStyleSheet(label_style)
        left_editors_layout.addWidget(lbl_eng)
        
        self.english_input = QTextEdit()
        self.english_input.setStyleSheet("""
            QTextEdit {
                font-size: 14pt; padding: 10px; background-color: #2b2b2b; 
                color: #81d4fa; border: 1px solid #555; border-radius: 2px;
            }
        """)
        self.english_input.textChanged.connect(self.translate_english_to_tezhnor)
        left_editors_layout.addWidget(self.english_input, stretch=1)

        # --- UPDATED: Tezhnor Typer Header with Font Dropdown ---
        tezhnor_header_layout = QHBoxLayout()
        
        lbl_tezhnor = QLabel("Tezhnor Typer")
        lbl_tezhnor.setStyleSheet(label_style)
        tezhnor_header_layout.addWidget(lbl_tezhnor)
        
        tezhnor_header_layout.addStretch()
        
        # 1. We MUST create the combo box first and attach it to 'self'
        self.unicode_font_dropdown = QComboBox()
        
        # 2. Now we can safely add the items to it!
        self.unicode_font_dropdown.addItems(LOADED_UNICODE_FONTS)
        
        self.unicode_font_dropdown.setStyleSheet("""
            QComboBox { background-color: #333; color: white; border: 1px solid #555; border-radius: 2px; padding: 2px; font-size: 10pt; }
            QComboBox::drop-down { border: none; }
        """)
        self.unicode_font_dropdown.currentTextChanged.connect(self.change_unicode_font)
        tezhnor_header_layout.addWidget(self.unicode_font_dropdown)
        
        left_editors_layout.addLayout(tezhnor_header_layout)
        
        # Typer text edit
        self.typer_input = TyperTextEdit()
        self.typer_input.textChanged.connect(self.translate_tezhnor_to_shigeyed)
        left_editors_layout.addWidget(self.typer_input, stretch=1)

        lbl_shigeyed = QLabel("Shigeyed Typer")
        lbl_shigeyed.setStyleSheet(label_style)
        left_editors_layout.addWidget(lbl_shigeyed)
        
        self.shigeyed_input = QTextEdit()
        self.shigeyed_input.setStyleSheet("""
            QTextEdit {
                font-size: 14pt; padding: 10px; background-color: #2b2b2b; 
                color: #ffab91; border: 1px solid #555; border-radius: 2px;
            }
        """)
        self.shigeyed_input.textChanged.connect(lambda: self.shigeyed_display.set_text(self.shigeyed_input.toPlainText()))
        left_editors_layout.addWidget(self.shigeyed_input, stretch=1)

        translator_layout.addWidget(left_editors_widget, stretch=1)

        # --- RIGHT SIDE: Displays ---
        right_displays_widget = QWidget()
        right_displays_layout = QVBoxLayout(right_displays_widget)
        right_displays_layout.setContentsMargins(10, 0, 0, 0)

        lbl_active_word = QLabel("Active Word Details")
        lbl_active_word.setStyleSheet(label_style)
        right_displays_layout.addWidget(lbl_active_word)

        self.active_word_display = QTextEdit()
        self.active_word_display.setReadOnly(True)
        self.active_word_display.setFixedHeight(80) 
        self.active_word_display.setStyleSheet("""
            QTextEdit {
                font-size: 12pt; padding: 5px; background-color: #2b2b2b; 
                color: #e0e0e0; border: 1px solid #555; border-radius: 2px;
            }
        """)
        right_displays_layout.addWidget(self.active_word_display)
        right_displays_layout.addSpacing(10)

        typer_controls_container = QVBoxLayout()
        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()

        slider_style = """
            QSlider::groove:horizontal { border: 1px solid #555; height: 8px; background: #333; margin: 2px 0; border-radius: 4px; }
            QSlider::handle:horizontal { background: #0277bd; border: 1px solid #0277bd; width: 18px; height: 18px; margin: -7px 0; border-radius: 9px; }
        """
        slider_label_style = "color: #bbb; font-weight: bold; font-size: 10pt;"

        self.font_dropdown = QComboBox()
        tezhnor_fonts = [k for k in FONT_PROFILES.keys() if "shigeyed" not in k.lower()]
        self.font_dropdown.addItems(tezhnor_fonts)
        self.font_dropdown.setCurrentText("Rounded Bold")
        self.font_dropdown.currentTextChanged.connect(self.change_font_profile)
        
        row1_layout.addWidget(QLabel("Tezhnor Font:"))
        row1_layout.addWidget(self.font_dropdown)
        row1_layout.addStretch() 
        
        size_layout = QVBoxLayout()
        self.typer_scale_label = QLabel("Size: 50%")
        self.typer_scale_label.setStyleSheet(slider_label_style)
        self.typer_scale_slider = QSlider(Qt.Horizontal)
        self.typer_scale_slider.setRange(10, 150)
        self.typer_scale_slider.setValue(50)
        self.typer_scale_slider.setStyleSheet(slider_style)
        self.typer_scale_slider.valueChanged.connect(self.update_typer_settings)
        size_layout.addWidget(self.typer_scale_label)
        size_layout.addWidget(self.typer_scale_slider)

        lh_layout = QVBoxLayout()
        self.typer_lh_label = QLabel("Line Height: 100%")
        self.typer_lh_label.setStyleSheet(slider_label_style)
        self.typer_lh_slider = QSlider(Qt.Horizontal)
        self.typer_lh_slider.setRange(50, 200)
        self.typer_lh_slider.setValue(100)
        self.typer_lh_slider.setStyleSheet(slider_style)
        self.typer_lh_slider.valueChanged.connect(self.update_typer_settings)
        lh_layout.addWidget(self.typer_lh_label)
        lh_layout.addWidget(self.typer_lh_slider)

        cs_layout = QVBoxLayout()
        self.typer_cs_label = QLabel("Char Spacing: 0")
        self.typer_cs_label.setStyleSheet(slider_label_style)
        self.typer_cs_slider = QSlider(Qt.Horizontal)
        self.typer_cs_slider.setRange(-20, 50)
        self.typer_cs_slider.setValue(1)
        self.typer_cs_slider.setStyleSheet(slider_style)
        self.typer_cs_slider.valueChanged.connect(self.update_typer_settings)
        cs_layout.addWidget(self.typer_cs_label)
        cs_layout.addWidget(self.typer_cs_slider)

        row2_layout.addLayout(size_layout)
        row2_layout.addLayout(lh_layout)
        row2_layout.addLayout(cs_layout)
        
        typer_controls_container.addLayout(row1_layout)
        typer_controls_container.addLayout(row2_layout)
        right_displays_layout.addLayout(typer_controls_container)
        
        lbl_disp_tezhnor = QLabel("Tezhnor Display")
        lbl_disp_tezhnor.setStyleSheet(label_style)
        right_displays_layout.addWidget(lbl_disp_tezhnor)
        
        self.typer_bottom = BitmapRenderer()
        self.typer_bottom.setMinimumHeight(200) 
        self.typer_input.textChanged.connect(
            lambda: self.typer_bottom.set_text(self.typer_input.toPlainText())
        )
        right_displays_layout.addWidget(self.typer_bottom, stretch=1)
        
        lbl_disp_shigeyed = QLabel("Shigeyed Display")
        lbl_disp_shigeyed.setStyleSheet(label_style)
        right_displays_layout.addWidget(lbl_disp_shigeyed)
        
        self.shigeyed_display = BitmapRenderer()
        self.shigeyed_display.setMinimumHeight(200)
        
        shig_prof = FONT_PROFILES["Shigeyed Bold"]
        self.shigeyed_display.font_dir = shig_prof["dir"]
        self.shigeyed_display.base_scale = shig_prof["bitmap_base_scale"]
        self.shigeyed_display.scale = shig_prof["bitmap_base_scale"] * 0.5 
        
        right_displays_layout.addWidget(self.shigeyed_display, stretch=1)

        translator_layout.addWidget(right_displays_widget, stretch=1)
        
        self.top_tabs.addTab(translator_tab, "Translate")

        # ==========================================
        # 4. RENDER TAB
        # ==========================================
        render_tab = QWidget()
        render_layout = QVBoxLayout(render_tab)
        
        # --- TOP: Controls ---
        render_controls_layout = QHBoxLayout()
        
        # Bitmap Font Selector
        self.render_font_dropdown = QComboBox()
        tezhnor_fonts = [k for k in FONT_PROFILES.keys() if "shigeyed" not in k.lower()]
        self.render_font_dropdown.addItems(tezhnor_fonts)
        self.render_font_dropdown.setCurrentText(CURRENT_FONT_KEY)
        self.render_font_dropdown.currentTextChanged.connect(self.change_font_profile)
        
        render_controls_layout.addWidget(QLabel("Tezhnor Font:"))
        render_controls_layout.addWidget(self.render_font_dropdown)
        render_controls_layout.addSpacing(20)
        
        # Sliders
        self.render_scale_label = QLabel("Size: 150%")
        self.render_scale_label.setStyleSheet(slider_label_style)
        self.render_scale_slider = QSlider(Qt.Horizontal)
        self.render_scale_slider.setRange(50, 500)
        self.render_scale_slider.setValue(150)
        self.render_scale_slider.setStyleSheet(slider_style)
        self.render_scale_slider.valueChanged.connect(self.update_render_settings)
        
        self.render_lh_label = QLabel("Line Height: 100%")
        self.render_lh_label.setStyleSheet(slider_label_style)
        self.render_lh_slider = QSlider(Qt.Horizontal)
        self.render_lh_slider.setRange(50, 200)
        self.render_lh_slider.setValue(100)
        self.render_lh_slider.setStyleSheet(slider_style)
        self.render_lh_slider.valueChanged.connect(self.update_render_settings)
        
        self.render_cs_label = QLabel("Char Spacing: 0")
        self.render_cs_label.setStyleSheet(slider_label_style)
        self.render_cs_slider = QSlider(Qt.Horizontal)
        self.render_cs_slider.setRange(-20, 50)
        self.render_cs_slider.setValue(1)
        self.render_cs_slider.setStyleSheet(slider_style)
        self.render_cs_slider.valueChanged.connect(self.update_render_settings)
        
        render_controls_layout.addWidget(self.render_scale_label)
        render_controls_layout.addWidget(self.render_scale_slider)
        render_controls_layout.addSpacing(15)
        render_controls_layout.addWidget(self.render_lh_label)
        render_controls_layout.addWidget(self.render_lh_slider)
        render_controls_layout.addSpacing(15)
        render_controls_layout.addWidget(self.render_cs_label)
        render_controls_layout.addWidget(self.render_cs_slider)
        
        render_controls_layout.addStretch()
        self.btn_export_png = QPushButton("Render to Disk")
        self.btn_export_png.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold; padding: 6px 15px; border-radius: 4px;")
        self.btn_export_png.clicked.connect(self.export_render_to_png)
        render_controls_layout.addWidget(self.btn_export_png)
        
        render_layout.addLayout(render_controls_layout)
        
        # --- BOTTOM: Subtabs ---
        self.render_subtabs = QTabWidget()
        
        # Tezhnor Subtab
        render_tezhnor_tab = QWidget()
        render_tezhnor_layout = QVBoxLayout(render_tezhnor_tab)
        
        self.render_tezhnor_scroll = QScrollArea()
        self.render_tezhnor_scroll.setWidgetResizable(True)
        self.render_tezhnor_display = BitmapRenderer()
        self.render_tezhnor_display.setMinimumSize(4000, 4000) # Massive canvas for scrolling
        self.render_tezhnor_scroll.setWidget(self.render_tezhnor_display)
        
        render_tezhnor_layout.addWidget(self.render_tezhnor_scroll)
        self.render_subtabs.addTab(render_tezhnor_tab, "Tezhnor")
        
        # Shigeyed Subtab
        render_shigeyed_tab = QWidget()
        render_shigeyed_layout = QVBoxLayout(render_shigeyed_tab)
        
        self.render_shigeyed_scroll = QScrollArea()
        self.render_shigeyed_scroll.setWidgetResizable(True)
        self.render_shigeyed_display = BitmapRenderer()
        self.render_shigeyed_display.setMinimumSize(4000, 4000)
        
        # Lock it to the Shigeyed profile
        self.render_shigeyed_display.font_dir = shig_prof["dir"]
        self.render_shigeyed_display.base_scale = shig_prof["bitmap_base_scale"]
        
        self.render_shigeyed_scroll.setWidget(self.render_shigeyed_display)
        
        render_shigeyed_layout.addWidget(self.render_shigeyed_scroll)
        self.render_subtabs.addTab(render_shigeyed_tab, "Shigeyed")
        
        render_layout.addWidget(self.render_subtabs)
        self.top_tabs.addTab(render_tab, "Render")

        # ==========================================
        # POST-SETUP OPERATIONS
        # ==========================================
        for category in self.categories:
            self.refresh_table(category)
        
        self.update_typer_settings()

    def show_table_context_menu(self, pos, table, category):
        row = table.rowAt(pos.y())
        col = table.columnAt(pos.x())
        
        if row < 0 or col < 0 or col == 3:
            return

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

    def handle_keypress(self, key_id, default_char, target=None):
        if target is None:
            target = self.input_conlang

        prev_char = target.get_prev_char()
        
        if prev_char:
            for combo_key, combo_val in COMBO_MAP.items():
                if combo_key.endswith(key_id) and len(combo_key) == 2:
                    prefix_key = combo_key[0] 
                    
                    if prefix_key in self.key_to_lore:
                        expected_lore_prefix = self.key_to_lore[prefix_key]
                        
                        if prev_char == expected_lore_prefix:
                            target.backspace()
                            target.insert(combo_val)
                            target.setFocus()
                            return

        target.insert(default_char)
        target.setFocus()

    def backspace(self):
        self.input_conlang.backspace()
        self.input_conlang.setFocus()

    def run_generator(self):
        syl_count = self.syllable_slider.value()
        word, structure, pron = WordGenerator.generate_word(num_syllables=syl_count)
        
        self.gen_result_display.setText(word)
        self.gen_structure_display.setText(structure)
        self.gen_pron_display.setText(pron)
        self.input_conlang.setText(word)

    def add_entry(self):
        conlang = self.input_conlang.text().strip()
        english = self.input_english.text().strip()
        notes = self.input_notes.text().strip()
        
        if not conlang or not english:
            QMessageBox.warning(self, "Missing Info", "Need word and definition.")
            return

        conflicts = []
        new_c_words = set(w.strip() for w in conlang.lower().split() if w.strip())
        new_e_clean = english.lower().replace('/', ' ')
        new_e_words = set(w.strip() for w in new_e_clean.split() if w.strip())

        for category in self.categories:
            for item in self.data[category]:
                existing_conlang = item.get("conlang", "").strip().lower()
                existing_english = item.get("english", "").strip().lower()

                ex_c_words = set(w.strip() for w in existing_conlang.split() if w.strip())
                ex_e_clean = existing_english.replace('/', ' ')
                ex_e_words = set(w.strip() for w in ex_e_clean.split() if w.strip())

                conlang_conflict = bool(new_c_words.intersection(ex_c_words))
                english_conflict = bool(new_e_words.intersection(ex_e_words))

                if conlang_conflict or english_conflict:
                    c_word = item.get("conlang", "")
                    e_word = item.get("english", "")
                    conflicts.append(f"• <b>{c_word}</b> <i>({e_word})</i>")

        if conflicts:
            dialog = QDialog(self)
            dialog.setWindowTitle("Possible Conflicts Found")
            dialog.setMinimumSize(400, 300)
            layout = QVBoxLayout(dialog)

            warning_label = QLabel("The following exact whole words already exist in your dictionary:")
            warning_label.setStyleSheet("color: #ffab91; font-weight: bold; font-size: 12pt;")
            layout.addWidget(warning_label)

            browser = QTextBrowser()
            browser.setHtml("<br>".join(conflicts))
            browser.setStyleSheet("background-color: #2b2b2b; color: white; font-size: 14pt; border: 1px solid #555; padding: 5px;")
            layout.addWidget(browser)

            btn_layout = QHBoxLayout()
            btn_cancel = QPushButton("Cancel")
            btn_cancel.setStyleSheet("background-color: #555; color: white; font-weight: bold; padding: 8px; border-radius: 4px;")
            btn_cancel.clicked.connect(dialog.reject)
            
            btn_continue = QPushButton("Continue (Add Anyway)")
            btn_continue.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 8px; border-radius: 4px;")
            btn_continue.clicked.connect(dialog.accept)

            btn_layout.addWidget(btn_cancel)
            btn_layout.addWidget(btn_continue)
            layout.addLayout(btn_layout)

            if dialog.exec() != QDialog.Accepted:
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
            label = QLabel(lore_word_raw)
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
                QPushButton { background-color: #d32f2f; color: white; font-weight: bold; border: none; border-radius: 12px; padding-bottom: 2px; }
                QPushButton:hover { background-color: #b71c1c; }
            """)
            del_btn.clicked.connect(lambda checked=False, c=category, i=r: self.delete_entry(c, i))
            
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0,0,0,0)
            layout.setAlignment(Qt.AlignCenter)
            layout.addWidget(del_btn)
            table.setCellWidget(r, 3, container)

    def change_unicode_font(self, font_name):
        self.update_typer_settings(new_font=font_name)

    def update_typer_settings(self, *args, new_font=None):
        size_val = self.typer_scale_slider.value()
        lh_val = self.typer_lh_slider.value()
        cs_val = self.typer_cs_slider.value()

        self.typer_scale_label.setText(f"Size: {size_val}%")
        self.typer_lh_label.setText(f"Line Height: {lh_val}%")
        self.typer_cs_label.setText(f"Char Spacing: {cs_val}")

        scale_factor = size_val / 100.0
        lh_factor = lh_val / 100.0

        if new_font is not None:
            ff_name = new_font
        else:
            ff_name = self.unicode_font_dropdown.currentText()
            
        self.typer_input.update_font_settings(scale_factor, lh_factor, cs_val, ff_name)
        self.typer_bottom.update_settings(scale_factor, lh_factor, cs_val)
        
        if hasattr(self, 'shigeyed_display'):
            self.shigeyed_display.update_settings(scale_factor, lh_factor, cs_val)

    def update_render_settings(self):
        if not hasattr(self, 'render_scale_slider'):
            return
            
        size_val = self.render_scale_slider.value()
        lh_val = self.render_lh_slider.value()
        cs_val = self.render_cs_slider.value()

        self.render_scale_label.setText(f"Size: {size_val}%")
        self.render_lh_label.setText(f"Line Height: {lh_val}%")
        self.render_cs_label.setText(f"Char Spacing: {cs_val}")

        scale_factor = size_val / 100.0
        lh_factor = lh_val / 100.0

        if hasattr(self, 'render_tezhnor_display'):
            self.render_tezhnor_display.update_settings(scale_factor, lh_factor, cs_val)
            
        if hasattr(self, 'render_shigeyed_display'):
            self.render_shigeyed_display.update_settings(scale_factor, lh_factor, cs_val)

    def export_render_to_png(self):
        # Determine whether Tezhnor or Shigeyed tab is currently active
        is_shigeyed = self.render_subtabs.currentIndex() == 1
        target_display = self.render_shigeyed_display if is_shigeyed else self.render_tezhnor_display
        default_name = "shigeyed_render.png" if is_shigeyed else "tezhnor_render.png"
            
        if not target_display.text_to_render.strip():
            QMessageBox.warning(self, "Empty Render", "There is no text to render!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "Render to Disk", default_name, "PNG Images (*.png)")
        
        if file_path:
            # Trigger the off-screen generation
            pixmap = target_display.export_to_pixmap()
            pixmap.save(file_path, "PNG")
    
    def change_font_profile(self, font_name):
        global CURRENT_FONT_KEY
        CURRENT_FONT_KEY = font_name
        profile = FONT_PROFILES[font_name]
        
        # Synchronize both dropdown selectors without infinite loop signals
        if hasattr(self, 'font_dropdown'):
            self.font_dropdown.blockSignals(True)
            self.font_dropdown.setCurrentText(font_name)
            self.font_dropdown.blockSignals(False)
            
        if hasattr(self, 'render_font_dropdown'):
            self.render_font_dropdown.blockSignals(True)
            self.render_font_dropdown.setCurrentText(font_name)
            self.render_font_dropdown.blockSignals(False)

        # Update Translator Tab Display
        self.typer_bottom.font_dir = profile["dir"]
        self.update_typer_settings()
        self.typer_bottom.set_text(self.typer_input.toPlainText())
        
        # Update Render Tab Display
        if hasattr(self, 'render_tezhnor_display'):
            self.render_tezhnor_display.font_dir = profile["dir"]
            self.update_render_settings()
            self.render_tezhnor_display.set_text(self.typer_input.toPlainText())

    def translate_english_to_tezhnor(self):
        eng_to_lore = {}
        for category in self.categories:
            for item in self.data[category]:
                eng_definitions = item.get("english", "").strip().lower()
                conlang_word = item.get("conlang", "").strip()
                
                if eng_definitions and conlang_word:
                    for sub_word in eng_definitions.split('/'):
                        clean_eng_word = sub_word.strip()
                        if clean_eng_word:
                            if clean_eng_word not in eng_to_lore:
                                eng_to_lore[clean_eng_word] = []
                            if conlang_word not in eng_to_lore[clean_eng_word]:
                                eng_to_lore[clean_eng_word].append(conlang_word)

        IGNORED_WORDS = {"a", "an", "the"}

        english_text = self.english_input.toPlainText()
        current_tezhnor_text = self.typer_input.toPlainText()
        
        eng_tokens = [t for t in re.split(SYMBOL_REGEX_PATTERN, english_text) if t]
        tezhnor_tokens = [t for t in re.split(SYMBOL_REGEX_PATTERN, current_tezhnor_text) if t]
        
        tezhnor_words = [t for t in tezhnor_tokens if not t.isspace() and t != "<---->" and t not in TYPER_CHAR_TO_SYMBOL_NAME]
        
        translated_tokens = []
        word_index = 0
        
        for token in eng_tokens:
            if token == "<---->":
                translated_tokens.append("<---->")
                continue
                
            if token.isspace():
                translated_tokens.append(token)
                continue
                
            if token in TYPER_CHAR_TO_SYMBOL_NAME:
                translated_tokens.append(token)
                continue
                
            word = token.lower()
            
            if word in IGNORED_WORDS:
                continue 
                
            if word in eng_to_lore:
                options = eng_to_lore[word]
                
                if word_index < len(tezhnor_words):
                    existing_choice = tezhnor_words[word_index]
                    if existing_choice in options:
                        chosen_word = existing_choice
                    else:
                        chosen_word = "/".join(options)
                else:
                    chosen_word = "/".join(options)
                    
                translated_tokens.append(chosen_word)
            else:
                translated_tokens.append("<---->")
                
            word_index += 1

        translated_text = "".join(translated_tokens)
        translated_text = re.sub(r'[ \t]+', ' ', translated_text).strip()

        self.typer_input.blockSignals(True) 
        self.typer_input.setText(translated_text)
        self.typer_input.apply_block_formatting()
        self.typer_input.blockSignals(False)
        
        display_text = self.typer_input.toPlainText().replace("<---->", "[]")
        self.typer_bottom.set_text(display_text)

        if hasattr(self, 'translate_tezhnor_to_shigeyed'):
            self.translate_tezhnor_to_shigeyed()
            
        if hasattr(self, 'update_active_word_panel'):
            self.update_active_word_panel()

        if hasattr(self, 'render_tezhnor_display'):
            self.render_tezhnor_display.set_text(display_text)

    def translate_tezhnor_to_shigeyed(self):
        self.shigeyed_input.blockSignals(True)
        tezhnor_text = self.typer_input.toPlainText()
        
        tokens = [t for t in re.split(SYMBOL_REGEX_PATTERN, tezhnor_text) if t]
        
        translated_tokens = []
        
        for token in tokens:
            if token == "<---->":
                translated_tokens.append(token)
                continue
                
            if token.isspace() or token in TYPER_CHAR_TO_SYMBOL_NAME:
                translated_tokens.append(token)
                continue
                
            norm_word = ""
            for char in token:
                if char in TEZHNOR_VOWEL_MAP:
                    norm_word += TEZHNOR_VOWEL_MAP[char]
                elif char in TEZHNOR_CONSONANT_MAP:
                    norm_word += TEZHNOR_CONSONANT_MAP[char]
                else:
                    norm_word += char
                    
            shigeyed_output = []
            cursor = 0
            
            while cursor < len(norm_word):
                char = norm_word[cursor]
                
                if char in SHIGEYED_VOWELS:
                    soft_syl = "ь" + char
                    if soft_syl in SYLLABLES_BY_CONSONANT.get("ь", []):
                        shigeyed_output.append(soft_syl)
                    else:
                        shigeyed_output.append(char) 
                    cursor += 1
                    continue
                    
                if char in SYLLABLES_BY_CONSONANT:
                    available_syls = SYLLABLES_BY_CONSONANT[char]
                    matched = False
                    
                    for length in [4, 3, 2]:
                        if cursor + length <= len(norm_word):
                            candidate = norm_word[cursor:cursor+length]
                            if candidate in available_syls:
                                ends_in_consonant = candidate[-1] not in SHIGEYED_VOWELS
                                
                                if ends_in_consonant and cursor + length < len(norm_word):
                                    next_char = norm_word[cursor + length]
                                    if next_char in SHIGEYED_VOWELS:
                                        continue 
                                
                                shigeyed_output.append(candidate)
                                cursor += length
                                matched = True
                                break
                    
                    if not matched:
                        fallback_syl = available_syls[0] if available_syls else char
                        shigeyed_output.append(fallback_syl)
                        cursor += 1
                else:
                    shigeyed_output.append(char)
                    cursor += 1
                    
            translated_tokens.append("·".join(shigeyed_output))

        self.shigeyed_input.setPlainText("".join(translated_tokens))
        self.shigeyed_input.blockSignals(False)
        
        display_text = self.shigeyed_input.toPlainText().replace("<---->", "[]")
        self.shigeyed_display.set_text(display_text)
        
        if hasattr(self, 'update_active_word_panel'):
            self.update_active_word_panel()

        if hasattr(self, 'render_shigeyed_display'):
            self.render_shigeyed_display.set_text(display_text)

    def find_dictionary_entry(self, tezhnor_word):
        if isinstance(self.data, dict):
            for category_list in self.data.values():
                for entry in category_list:
                    if entry.get("conlang") == tezhnor_word:
                        return entry
                        
        elif isinstance(self.data, list):
            for entry in self.data:
                if entry.get("conlang") == tezhnor_word:
                    return entry
                    
        return None

    def update_active_word_panel(self):
        active_tezhnor_words = []
        
        def get_word_near_cursor(text_edit):
            pos = text_edit.textCursor().position()
            text = text_edit.toPlainText()
            
            tokens = re.split(SYMBOL_REGEX_PATTERN, text)
            
            current_idx = 0
            last_valid_word = None
            
            for token in tokens:
                start_idx = current_idx
                end_idx = current_idx + len(token)
                
                is_word = bool(token.strip()) and token not in TYPER_CHAR_TO_SYMBOL_NAME and token != "<---->"
                
                if is_word:
                    last_valid_word = token
                    
                if start_idx <= pos <= end_idx:
                    if is_word:
                        return token
                    else:
                        return last_valid_word
                        
                current_idx = end_idx
                
            return last_valid_word

        if hasattr(self, 'english_input') and self.english_input.hasFocus():
            eng_word = get_word_near_cursor(self.english_input)
            if eng_word:
                eng_word = eng_word.lower()
                for category in self.categories:
                    for item in self.data[category]:
                        eng_defs = item.get("english", "").strip().lower()
                        conlang_word = item.get("conlang", "").strip()
                        if eng_defs and conlang_word:
                            for sub_word in eng_defs.split('/'):
                                if sub_word.strip() == eng_word and conlang_word not in active_tezhnor_words:
                                    active_tezhnor_words.append(conlang_word)
        else:
            tezhnor_word = get_word_near_cursor(self.typer_input)
            if tezhnor_word:
                active_tezhnor_words = [w for w in tezhnor_word.split('/') if w]

        if not active_tezhnor_words:
            self.active_word_display.setHtml("<i>No active word...</i>")
            return
            
        html_output = ""
        for opt in active_tezhnor_words:
            entry = self.find_dictionary_entry(opt)
            if entry:
                def_text = entry.get("english", entry.get("definition", "Unknown Definition"))
                notes_text = entry.get("notes", "")
                notes_html = f" <span style='color:#888;'>({notes_text})</span>" if notes_text else ""
                html_output += f"<b style='color:#81d4fa;'>{opt}</b>: {def_text}{notes_html}<br>"
            else:
                html_output += f"<b style='color:#81d4fa;'>{opt}</b>: <i>Not found in dictionary</i><br>"
                
        self.active_word_display.setHtml(html_output)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Wordforge()
    window.show()
    sys.exit(app.exec())
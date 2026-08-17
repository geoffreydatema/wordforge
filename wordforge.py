import sys
import json
import os
import random
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTabWidget, QLineEdit, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QMessageBox, QGridLayout, QFrame, QLabel, QTextEdit,
                               QSlider, QTextBrowser, QMenu, QComboBox, QDialog)
from PySide6.QtGui import QFont, QTextCursor, QPainter, QPixmap, QColor, QTextBlockFormat
from PySide6.QtCore import Qt, QObject, QEvent, Signal

# ========================================================
#       MASTER CHARACTER SET
#
#       aэջohλиეεyδюбвгдzкямнпpcтvxqьμжчшθdфըբζՑцპსպէთრც
#       
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
    ε = 'oh'    # long o
    y = 'oo'    # oo as in poop
    δ = 'oe'    # oe as in put
    ю = 'ue'    # ы
    б = 'b'
    в = 'v'
    г = 'g'
    д = 'd'
    z = 'z'
    к = 'k'
    я = 'l' 
    м = 'm'
    н = 'n'
    п = 'p'
    p = 'r'
    c = 's'
    т = 't'
    v = 'f'
    x = 'h'
    q = 'w'
    ь = 'y'
    μ = 'j'
    ж = 'zh'
    ч = 'ch'
    ш = 'sh'
    θ = 'th'
    d = 'dh'
    ф = 'ng'
    ը = 'nd'
    բ = 'pl'
    ζ = 'ps'
    Ց = 'tr'
    ц = 'ts'
    პ = 'st'
    ს = 'ks'
    պ = 'sk'
    է = 'kv'
    თ = 'sv'
    რ = 'zv'
    ც = 'dv'

class LORE:
    A = 'a'
    E = 'э'
    I = 'ջ'
    O = 'o'
    U = 'h'
    AY = 'λ'
    EE = 'и'
    IY = 'ე'
    OW = 'ε'
    OO = 'y'
    OE = 'δ'
    UE = 'ю'
    B = 'б'
    V = 'в'
    G = 'г'
    D = 'д'
    Z = 'z'
    K = 'к'
    L = 'я' 
    M = 'м'
    N = 'н'
    P = 'п'
    R = 'p'
    C = 'c'
    T = 'т'
    F = 'v'
    X = 'x'
    W = 'q'
    Y = 'ь'
    J = 'μ'
    ZH = 'ж'
    CH = 'ч'
    SH = 'ш'
    TH = 'θ'
    DH = 'd'
    NG = 'ф'
    ND = 'ը'
    PL = 'բ'
    PS = 'ζ'
    TR = 'Ց'
    TS = 'ц'
    ST = 'პ'
    KS = 'ს'
    SK = 'պ'
    KV = 'է'
    SV = 'თ'
    ZV = 'რ'
    DV = 'ც'
    PERIOD = '╷'
    QUOTE = '╵'
    OPEN = '└'
    CLOSE = '┘'

# Automatically map the conlang character (the variable name) to the filename (the value)
CHAR_TO_FILENAME = {}
for attr in dir(DEFINITIONS):
    if not attr.startswith('__') and not callable(getattr(DEFINITIONS, attr)):
        filename_prefix = getattr(DEFINITIONS, attr)
        CHAR_TO_FILENAME[attr] = filename_prefix

CHAR_TO_FILENAME[LORE.PERIOD] = "period"
CHAR_TO_FILENAME[LORE.QUOTE] = "quote"
CHAR_TO_FILENAME[LORE.OPEN] = "open"
CHAR_TO_FILENAME[LORE.CLOSE] = "close"

# Place this at the top of your file
FONT_PROFILES = {
    "Rounded Regular": {
        "dir": "fonts/tezhnor_rounded_regular",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.17,
        "line_height": 210,
        "space_width": 60,
        "advance_punctuation": 50,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 20
    },
    "Rounded Bold": {
        "dir": "fonts/tezhnor_rounded_bold", 
        "text_base_pt": 28,
        "bitmap_base_scale": 0.17,
        "line_height": 210,
        "space_width": 60,
        "advance_punctuation": 50,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 20
    },
    "Block Regular": {
        "dir": "fonts/tezhnor_block_regular",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.17,
        "line_height": 210,
        "space_width": 60,
        "advance_punctuation": 50,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 20
    },
    "Block Mono": {
        "dir": "fonts/tezhnor_block_mono",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.17,
        "line_height": 210,
        "space_width": 103,    # Adjusted to match the mono width for even word gaps
        "advance_punctuation": 50,
        "advance_normal": 103, 
        "advance_square": 103, # Flattened to smallest width
        "advance_wide": 103,   # Flattened to smallest width
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 20
    },
    "Block Extended": {
        "dir": "fonts/tezhnor_block_mono_extended",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.17,
        "line_height": 210,
        "space_width": 128,    # Adjusted to match the extended width
        "advance_punctuation": 50,
        "advance_normal": 128, # Flattened to middle width
        "advance_square": 128, # Flattened to middle width
        "advance_wide": 128,   # Flattened to middle width
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 20
    },
    "Block Monoheight": {
        "dir": "fonts/tezhnor_block_monoheight",
        "text_base_pt": 28,
        "bitmap_base_scale": 0.17,
        "line_height": 210,
        "space_width": 60,
        "advance_punctuation": 50,
        "advance_normal": 103,
        "advance_square": 128,
        "advance_wide": 155,
        "padding": 15,
        "bitmap_offset_x": 5,
        "bitmap_offset_y": 10,
        "bitmap_base_char_spacing": 20
    }
}

CURRENT_FONT_KEY = list(FONT_PROFILES.keys())[0]
FONT_METRICS = FONT_PROFILES[CURRENT_FONT_KEY]

CHAR_WIDTHS = {
    # Wide & Square Characters
    LORE.O: "advance_square",
    LORE.UE: "advance_square",
    LORE.D: "advance_square",
    LORE.M: "advance_square",
    LORE.W: "advance_square",
    LORE.ZH: "advance_wide",
    LORE.SH: "advance_wide",
    LORE.TH: "advance_square",
    LORE.SK: "advance_wide",
    LORE.TS: "advance_square",
    LORE.KV: "advance_square",
    LORE.SV: "advance_wide",
    LORE.ZV: "advance_wide",
    LORE.PERIOD: "advance_punctuation",
    LORE.QUOTE: "advance_punctuation",
    LORE.OPEN: "advance_punctuation",
    LORE.CLOSE: "advance_punctuation"
}

class PRONUNCIATION:
    A = 'a'     # short a
    E = 'e'     # short e
    I = 'i'     # short i
    O = 'o'     # short o
    U = 'u'     # short u
    AY = 'ay'   # long a
    EE = 'ee'   # long e
    IY = 'iy'   # long i
    OW = 'ow'   # long o
    OO = 'oo'   # oo as in poop
    OE = 'oe'   # oe as in put
    UE = 'ue'   # ы
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
    NG = 'ng'   # anglophone ng sound used in the ing word 
    ND = 'nd'
    PL = 'pl'
    PS = 'ps'
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
    LORE.A, LORE.E, LORE.I, LORE.O, LORE.U, 
    LORE.AY, LORE.EE, LORE.IY, LORE.OW, LORE.OO, 
    LORE.OE, LORE.UE
]

CONSONANTS = [
    LORE.W, LORE.P, LORE.T, LORE.B, LORE.R, LORE.C, LORE.D, LORE.F, LORE.G, LORE.X,
    LORE.J, LORE.K, LORE.L, LORE.Z, LORE.V, LORE.Y, LORE.N, LORE.M, LORE.ZH, LORE.CH,
    LORE.SH, LORE.TH, LORE.DH, LORE.NG, LORE.ND, LORE.PL, LORE.PS, LORE.TR, LORE.TS,
    LORE.ST, LORE.KS, LORE.SK, LORE.KV, LORE.SV, LORE.ZV, LORE.DV
]

ALPHABET_DEFS = [
    (LORE.A, "a", "short a"),
    (LORE.E, "e", "short e"),
    (LORE.I, "i", "short i"),
    (LORE.O, "o", "short o"),
    (LORE.U, "u", "short u"),
    (LORE.AY, "ay", "long a"),
    (LORE.EE, "ee", "long e"),
    (LORE.IY, "eye", "long i"),
    (LORE.OW, "ow", "long o"),
    (LORE.OO, "oo", "oo as in poop"),
    (LORE.OE, "oe", "oe as in put"),
    (LORE.UE, "ue", "ы"),
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
    (LORE.ND, "nd", ""),
    (LORE.PL, "pl", ""),
    (LORE.PS, "ps", ""),
    (LORE.TR, "tr", ""),
    (LORE.TS, "ts", ""),
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

TABLE_SIZE_CORRECTIONS = {}
HEADER_SIZE_CORRECTIONS = {}

KEYBOARD_LAYOUT = [
    [('w', LORE.W), ('e', LORE.E), ('r', LORE.R), ('t', LORE.T), ('y', LORE.Y), ('u', LORE.U), ('i', LORE.I), ('o', LORE.O), ('p', LORE.P)],
    [('a', LORE.A), ('s', LORE.C), ('d', LORE.D), ('f', LORE.F), ('g', LORE.G), ('h', LORE.X), ('j', LORE.J), ('k', LORE.K), ('l', LORE.L)],
    [('└', LORE.OPEN), ('┘', LORE.CLOSE), ('z', LORE.Z), ('v', LORE.V), ('b', LORE.B), ('n', LORE.N), ('m', LORE.M), ('╵', LORE.QUOTE), ('╷', LORE.PERIOD)]
]

LONG_VOWEL_MAP = {
    "a": LORE.A, "e": LORE.E, "i": LORE.I, "o": LORE.O
}

COMBO_MAP = {
    "ay": LORE.AY, "ee": LORE.EE, "iy": LORE.IY, "ow": LORE.OW, "oo": LORE.OO,
    "oe": LORE.OE, "ue": LORE.UE,
    "zh": LORE.ZH, "sh": LORE.SH, "ch": LORE.CH, 
    "th": LORE.TH, "dh": LORE.DH, "ng": LORE.NG, "nd": LORE.ND,
    "pl": LORE.PL, "ps": LORE.PS,
    "tr": LORE.TR, "ts": LORE.TS, "st": LORE.ST,
    "ks": LORE.KS, "sk": LORE.SK,
    "kv": LORE.KV, "sv": LORE.SV, "zv": LORE.ZV, "dv": LORE.DV
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

class BitmapRenderer(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_to_render = ""
        self._pixmap_cache = {}
        self.font_dir = FONT_METRICS["dir"]
        
        self.base_scale = 1.0
        self.scale = 1.0 
        self.lh_factor = 1.0
        self.char_spacing = 0

    def update_settings(self, scale_factor, lh_factor, char_spacing):
        self.base_scale = FONT_METRICS.get("bitmap_base_scale", 1.0)
        self.scale = scale_factor * self.base_scale
        self.lh_factor = lh_factor
        self.char_spacing = char_spacing
        self.update()

    def set_scale(self, scale_factor):
        # 3. Multiply the slider's scale factor by the font's base scale
        self.scale = scale_factor * self.base_scale
        self.update()

    def set_text(self, new_text):
        self.text_to_render = new_text
        self.update() 

    def get_pixmap(self, char):
        # Cache based on BOTH the character and the current scale
        cache_key = (char, self.scale)
        if cache_key in self._pixmap_cache:
            return self._pixmap_cache[cache_key]
            
        file_prefix = CHAR_TO_FILENAME.get(char, char) if 'CHAR_TO_FILENAME' in globals() else char
        image_path = os.path.join(self.font_dir, f"{file_prefix}.png")
        
        if os.path.exists(image_path):
            orig_pixmap = QPixmap(image_path)
            
            # Perform a high-quality downscale ONCE, not every frame
            target_width = int(orig_pixmap.width() * self.scale)
            target_height = int(orig_pixmap.height() * self.scale)
            
            scaled_pixmap = orig_pixmap.scaled(
                target_width, 
                target_height, 
                Qt.IgnoreAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self._pixmap_cache[cache_key] = scaled_pixmap
            return scaled_pixmap
            
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#2b2b2b"))
        
        # We removed the painter scaling and render hints!
        
        # Convert raw metrics to actual screen pixels
        dynamic_lh = (FONT_METRICS["line_height"] * self.lh_factor) * self.scale
        scaled_space_width = FONT_METRICS["space_width"] * self.scale
        
        PADDING_SCREEN = FONT_METRICS.get("padding", 10)
        OFFSET_X = FONT_METRICS.get("bitmap_offset_x", 0)
        OFFSET_Y = FONT_METRICS.get("bitmap_offset_y", 0)
        
        # Base spacing was in raw pixels, so it needs scaling. 
        # self.char_spacing comes from the UI slider, so it doesn't need scaling.
        BASE_SPACING_SCALED = FONT_METRICS.get("bitmap_base_char_spacing", 0) * self.scale
        effective_char_spacing = self.char_spacing + BASE_SPACING_SCALED
        
        max_x = self.width() - (PADDING_SCREEN + OFFSET_X)
        
        # Start the cursors
        cursor_x = PADDING_SCREEN + OFFSET_X
        cursor_y = PADDING_SCREEN + OFFSET_Y
        
        for char in self.text_to_render:
            if char == '\n':
                cursor_x = PADDING_SCREEN + OFFSET_X 
                cursor_y += dynamic_lh
                continue
                
            if char == ' ':
                cursor_x += scaled_space_width + effective_char_spacing
                if cursor_x > max_x:
                    cursor_x = PADDING_SCREEN + OFFSET_X 
                    cursor_y += dynamic_lh
                continue
                
            # Scale the character advance to screen pixels
            width_key = CHAR_WIDTHS.get(char, "advance_normal")
            raw_advance = FONT_METRICS[width_key]
            advance = (raw_advance * self.scale) + effective_char_spacing
            
            if cursor_x + advance > max_x:
                cursor_x = PADDING_SCREEN + OFFSET_X 
                cursor_y += dynamic_lh
                
            pixmap = self.get_pixmap(char)
            if pixmap:
                # Draw exactly at the screen coordinates
                painter.drawPixmap(int(cursor_x), int(cursor_y), pixmap)
                
            cursor_x += advance

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

class TyperTextEdit(RichLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(16777215) 
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        self.line_height_factor = 1.0
        self.char_spacing = 0
        
        self.textChanged.connect(self.apply_block_formatting)
        self.update_font_settings(0.5, 1.0, 0)

    def update_font_settings(self, scale_factor, lh_factor, char_spacing):
        self.line_height_factor = lh_factor
        self.char_spacing = char_spacing

        # Pull the base size from our unified metrics
        self.base_pt = FONT_METRICS.get("text_base_pt", 28) 

        current_pt = max(8, int(self.base_pt * scale_factor))
        pad = FONT_METRICS.get("padding", 10) 
        
        # Let CSS handle only the container, padding, and base point size
        self.setStyleSheet(f"""
            QTextEdit {{
                font-size: {current_pt}pt; 
                font-weight: normal; 
                padding: {pad}px;  
                border: 1px solid #555; 
                border-radius: 2px;
                background-color: #2b2b2b; 
                color: white;
            }}
        """)
        
        # We removed the buggy self.setFont() logic from here!
        self.apply_block_formatting()

    def apply_block_formatting(self):
        self.blockSignals(True)
        
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        
        # 1. Apply Line Height
        block_fmt = cursor.blockFormat()
        block_fmt.setLineHeight(float(self.line_height_factor * 100), QTextBlockFormat.ProportionalHeight.value)
        cursor.setBlockFormat(block_fmt)
        
        # 2. Apply Character Spacing
        char_fmt = cursor.charFormat()
        if self.char_spacing == 0:
            # If the slider is at 0, restore the font's beautiful native kerning
            char_fmt.setFontLetterSpacingType(QFont.PercentageSpacing)
            char_fmt.setFontLetterSpacing(100.0)
        else:
            # If the user moves the slider, apply their exact pixel offset
            char_fmt.setFontLetterSpacingType(QFont.AbsoluteSpacing)
            char_fmt.setFontLetterSpacing(float(self.char_spacing))
            
        cursor.mergeCharFormat(char_fmt) # merge avoids destroying other styles
        
        self.blockSignals(False)

    def keyPressEvent(self, event):
        QTextEdit.keyPressEvent(self, event)
        
    def insert(self, text):
        self.textCursor().insertText(text)
        
    def setText(self, text):
        self.setPlainText(text)
        self.moveCursor(QTextCursor.End)

class WordGenerator:
    ALL_VOWELS = [LORE.A, LORE.E, LORE.I, LORE.O, LORE.U, LORE.AY, LORE.EE, LORE.IY, LORE.OW, LORE.OO, LORE.OE, LORE.UE]

    @staticmethod
    def generate_word(num_syllables=3):
        word = ""
        structure_log = [] 
        pronunciation_log = []
        
        # Helper functions now purely prevent immediate repetition
        def get_c(exclude=None):
            opts = [c for c in CONSONANTS if c != exclude] if exclude else CONSONANTS
            return random.choice(opts) if opts else random.choice(CONSONANTS)

        def get_v(exclude=None):
            opts = [v for v in WordGenerator.ALL_VOWELS if v != exclude] if exclude else WordGenerator.ALL_VOWELS
            return random.choice(opts) if opts else random.choice(WordGenerator.ALL_VOWELS)
        
        for i in range(num_syllables):
            structure = random.choices(
                ["V", "CV", "VC", "CVC", "CVV", "CCV", "VCC"], 
                weights=[10, 30, 10, 25, 5, 15, 5], 
                k=1
            )[0]
            
            prev_char = word[-1] if word else None
            
            # Prevent awkward double-vowel boundaries across syllables
            if prev_char in WordGenerator.ALL_VOWELS and structure in ["V", "VC", "VCC", "CVV"]:
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
                v2 = get_v(exclude=v1) # Just ensure it doesn't pick the exact same vowel twice
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
        
        # 1. Load your standard visual layout
        for row in KEYBOARD_LAYOUT:
            for key_id, lore_char in row:
                self.key_map[key_id] = lore_char
                
        # 2. Define the hidden punctuation binds
        punctuation_binds = {
            '.': LORE.PERIOD,
            "'": LORE.QUOTE,
            '"': LORE.QUOTE,
            '(': LORE.OPEN,
            '[': LORE.OPEN,
            '{': LORE.OPEN,
            '<': LORE.OPEN,
            ')': LORE.CLOSE,
            ']': LORE.CLOSE,
            '}': LORE.CLOSE,
            '>': LORE.CLOSE
        }
        
        # 3. Merge them into the active key map
        self.key_map.update(punctuation_binds)
        
        self.pending_c = False

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key_text = event.text().lower()
            
            if event.modifiers() & Qt.ControlModifier: 
                self.pending_c = False
                return False

            if event.key() == Qt.Key_Backspace:
                self.pending_c = False
                obj.backspace() 
                return True 
                
            if event.key() == Qt.Key_Space:
                self.pending_c = False
                obj.insertPlainText(" ") 
                return True

            if key_text == 'c':
                self.pending_c = True
                return True  # Consume the keypress, but don't type anything yet

            if self.pending_c:
                self.pending_c = False  # Reset the tracker immediately
                if key_text == 'h':
                    lore_char = self.key_map.get('ch', 'ч') 
                    self.window.handle_keypress('ch', lore_char, target=obj)
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
        
        self.common_words = self.load_common_words()

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
        
        # Wordforge
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
        
        forge_layout.addLayout(kbd_header_layout)
        
        keyboard = self.create_keyboard()
        forge_layout.addWidget(keyboard)
        forge_layout.addStretch()
        
        self.left_tabs.addTab(forge_tab, "Word Forge")
        
        # Typer tab
        typer_tab = QWidget()
        typer_layout = QVBoxLayout(typer_tab)

        # 1. Top Section: English Input
        self.english_input = QTextEdit()
        self.english_input.setPlaceholderText("Type English here to translate to Tezhnor...")
        self.english_input.setStyleSheet("""
            QTextEdit {
                font-size: 14pt; 
                padding: 10px; 
                background-color: #2b2b2b; 
                color: #81d4fa; 
                border: 1px solid #555; 
                border-radius: 2px;
            }
        """)
        self.english_input.textChanged.connect(self.translate_english_to_tezhnor)
        typer_layout.addWidget(self.english_input, stretch=1)

        # 2. Middle Section: Typer Input
        self.typer_input = TyperTextEdit()
        self.typer_input.setPlaceholderText("Tezhnor output...")
        typer_layout.addWidget(self.typer_input, stretch=1)

        # 3. Controls Section (Moved above the bitmap renderer)
        typer_controls_container = QVBoxLayout()
        
        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()

        slider_style = """
            QSlider::groove:horizontal { border: 1px solid #555; height: 8px; background: #333; margin: 2px 0; border-radius: 4px; }
            QSlider::handle:horizontal { background: #0277bd; border: 1px solid #0277bd; width: 18px; height: 18px; margin: -7px 0; border-radius: 9px; }
        """
        label_style = "color: #bbb; font-weight: bold; font-size: 10pt;"

        # --- ROW 1: Font Selector ---
        self.font_dropdown = QComboBox()
        self.font_dropdown.addItems(FONT_PROFILES.keys())
        self.font_dropdown.currentTextChanged.connect(self.change_font_profile)
        
        row1_layout.addWidget(QLabel("Select Font:"))
        row1_layout.addWidget(self.font_dropdown)
        row1_layout.addStretch() # Pushes the dropdown to the left so it doesn't stretch weirdly
        
        # --- ROW 2: Sliders ---
        # 1. Size Slider
        size_layout = QVBoxLayout()
        self.typer_scale_label = QLabel("Size: 50%")
        self.typer_scale_label.setStyleSheet(label_style)
        self.typer_scale_slider = QSlider(Qt.Horizontal)
        self.typer_scale_slider.setRange(10, 150)
        self.typer_scale_slider.setValue(50)
        self.typer_scale_slider.setStyleSheet(slider_style)
        self.typer_scale_slider.valueChanged.connect(self.update_typer_settings)
        size_layout.addWidget(self.typer_scale_label)
        size_layout.addWidget(self.typer_scale_slider)

        # 2. Line Height Slider
        lh_layout = QVBoxLayout()
        self.typer_lh_label = QLabel("Line Height: 100%")
        self.typer_lh_label.setStyleSheet(label_style)
        self.typer_lh_slider = QSlider(Qt.Horizontal)
        self.typer_lh_slider.setRange(50, 200)
        self.typer_lh_slider.setValue(100)
        self.typer_lh_slider.setStyleSheet(slider_style)
        self.typer_lh_slider.valueChanged.connect(self.update_typer_settings)
        lh_layout.addWidget(self.typer_lh_label)
        lh_layout.addWidget(self.typer_lh_slider)

        # 3. Char Spacing Slider
        cs_layout = QVBoxLayout()
        self.typer_cs_label = QLabel("Char Spacing: 0")
        self.typer_cs_label.setStyleSheet(label_style)
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
        
        # Add both rows to the main container
        typer_controls_container.addLayout(row1_layout)
        typer_controls_container.addLayout(row2_layout)
        
        typer_layout.addLayout(typer_controls_container)
        
        # 4. Bottom Section: The Custom Font Renderer
        self.typer_bottom = BitmapRenderer()
        self.typer_bottom.setMinimumHeight(200) 
        
        self.typer_input.textChanged.connect(
            lambda: self.typer_bottom.set_text(self.typer_input.toPlainText())
        )
        
        typer_layout.addWidget(self.typer_bottom, stretch=1)
        
        self.left_tabs.addTab(typer_tab, "Typer")

        # Definitions tab
        def_tab = QWidget()
        def_layout = QVBoxLayout(def_tab)
        
        self.def_browser = QTextBrowser()
        self.def_browser.setOpenExternalLinks(False)
        self.def_browser.setStyleSheet("background-color: #2b2b2b; color: white; font-size: 12pt; border: 1px solid #444;")
        
        html = "<h2>тэжнop alphabet</h2><table width='100%' cellpadding='6' style='border-collapse: collapse; margin-bottom: 20px;'>"
        html += "<tr style='background-color: #444;'><th style='border-bottom: 1px solid white;'>Char</th><th style='border-bottom: 1px solid white;'>Sound</th><th style='border-bottom: 1px solid white;'>Notes</th></tr>"
        for char, sound, notes in ALPHABET_DEFS:
            styled_char = apply_visual_fixes(char, mode='table')
            html += f"<tr><td style='border-bottom: 1px solid #444; text-align: center; font-size: 16pt;'>{styled_char}</td><td style='border-bottom: 1px solid #444;'>{sound}</td><td style='border-bottom: 1px solid #444; font-size: 11pt; color: #bbb;'>{notes}</td></tr>"
        
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
        
        self.update_typer_settings()

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
        # If no target is passed (e.g., clicking the on-screen touch keyboard), default to Word Forge input
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

        # --- 1. VALIDATION CHECK (WHOLE WORDS ONLY) ---
        conflicts = []
        
        # Break new inputs into sets of whole words
        new_c_words = set(w.strip() for w in conlang.lower().split() if w.strip())
        
        # For English, replace slashes with spaces first, then split into words
        new_e_clean = english.lower().replace('/', ' ')
        new_e_words = set(w.strip() for w in new_e_clean.split() if w.strip())

        for category in self.categories:
            for item in self.data[category]:
                existing_conlang = item.get("conlang", "").strip().lower()
                existing_english = item.get("english", "").strip().lower()

                # Break existing entries into sets of whole words
                ex_c_words = set(w.strip() for w in existing_conlang.split() if w.strip())
                ex_e_clean = existing_english.replace('/', ' ')
                ex_e_words = set(w.strip() for w in ex_e_clean.split() if w.strip())

                # Check for overlap (intersection) between the sets
                conlang_conflict = bool(new_c_words.intersection(ex_c_words))
                english_conflict = bool(new_e_words.intersection(ex_e_words))

                if conlang_conflict or english_conflict:
                    # Format it nicely for the popup
                    c_word = item.get("conlang", "")
                    e_word = item.get("english", "")
                    conflicts.append(f"• <b>{c_word}</b> <i>({e_word})</i>")

        # --- 2. SHOW POPUP IF CONFLICTS EXIST ---
        if conflicts:
            dialog = QDialog(self)
            dialog.setWindowTitle("Possible Conflicts Found")
            dialog.setMinimumSize(400, 300)
            layout = QVBoxLayout(dialog)

            warning_label = QLabel("The following exact whole words already exist in your dictionary:")
            warning_label.setStyleSheet("color: #ffab91; font-weight: bold; font-size: 12pt;")
            layout.addWidget(warning_label)

            # Display conflicts in a readable text box
            browser = QTextBrowser()
            browser.setHtml("<br>".join(conflicts))
            browser.setStyleSheet("background-color: #2b2b2b; color: white; font-size: 14pt; border: 1px solid #555; padding: 5px;")
            layout.addWidget(browser)

            # Buttons
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

            # If the user clicks Cancel or closes the window, abort the save.
            if dialog.exec() != QDialog.Accepted:
                return  

        # --- 3. ADD TO DICTIONARY ---
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

    def update_typer_settings(self, *args):
        # Grab values from all three sliders
        size_val = self.typer_scale_slider.value()
        lh_val = self.typer_lh_slider.value()
        cs_val = self.typer_cs_slider.value()

        # Update the UI Labels
        self.typer_scale_label.setText(f"Size: {size_val}%")
        self.typer_lh_label.setText(f"Line Height: {lh_val}%")
        self.typer_cs_label.setText(f"Char Spacing: {cs_val}")

        # Convert to math-friendly factors
        scale_factor = size_val / 100.0
        lh_factor = lh_val / 100.0

        # Push to both renderers simultaneously
        self.typer_input.update_font_settings(scale_factor, lh_factor, cs_val)
        self.typer_bottom.update_settings(scale_factor, lh_factor, cs_val)
    
    def change_font_profile(self, font_name):
        global FONT_METRICS
        FONT_METRICS = FONT_PROFILES[font_name]
        
        self.typer_bottom.font_dir = FONT_METRICS["dir"]
        self.typer_bottom._pixmap_cache.clear()
        
        self.update_typer_settings()

    def translate_english_to_tezhnor(self):
        eng_to_lore = {}
        for category in self.categories:
            for item in self.data[category]:
                eng_definitions = item.get("english", "").strip().lower()
                conlang_word = item.get("conlang", "")
                
                if eng_definitions:
                    for sub_word in eng_definitions.split('/'):
                        clean_eng_word = sub_word.strip()
                        if clean_eng_word:
                            eng_to_lore[clean_eng_word] = conlang_word

        punct_map = {
            '.': LORE.PERIOD,
            "'": LORE.QUOTE,
            '"': LORE.QUOTE,
            '(': LORE.OPEN,
            '[': LORE.OPEN,
            '{': LORE.OPEN,
            '<': LORE.OPEN,
            ')': LORE.CLOSE,
            ']': LORE.CLOSE,
            '}': LORE.CLOSE,
            '>': LORE.CLOSE
        }
        
        IGNORED_WORDS = {"a", "an", "the"}

        english_text = self.english_input.toPlainText()

        def replace_token(match):
            token = match.group(0)
            
            if token in punct_map:
                return punct_map[token]
                
            word = token.lower()
            
            if word in IGNORED_WORDS:
                return ""
                
            return eng_to_lore.get(word, "<--->")

        pattern = r"[a-zA-Z]+(?:'[a-zA-Z]+)?|[.\"'()\[\]{}<>]"
        translated_text = re.sub(pattern, replace_token, english_text)

        translated_text = re.sub(r'[ \t]+', ' ', translated_text).strip()

        self.typer_input.blockSignals(True) 
        self.typer_input.setText(translated_text)
        self.typer_input.blockSignals(False)
        self.typer_bottom.set_text(self.typer_input.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Wordforge()
    window.show()
    sys.exit(app.exec())

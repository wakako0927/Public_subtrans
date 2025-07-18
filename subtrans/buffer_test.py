#tempCodeRunnerFile.py

from ocr_processor import SubtitleBuffer

#バッファ連結＋重複回避
buffer = SubtitleBuffer()

import difflib

class SubtitleMemory:
    def __init__(self, threshold=0.85):
        self.last_text = None
        self.threshold = threshold

    def is_new(self, text: str) -> bool:
        cleaned = text.strip()
        if self.last_text is None:
            self.last_text = cleaned
            return True
        ratio = difflib.SequenceMatcher(None, cleaned, self.last_text).ratio()
        if ratio >= self.threshold:
            return False
        self.last_text = cleaned
        return True


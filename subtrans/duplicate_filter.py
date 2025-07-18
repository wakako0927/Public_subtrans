import difflib

# 字幕の重複を検出するクラス
class SubtitleMemory:
    def __init__(self, threshold=0.85):
        self.last_text = None   # 最後に処理した字幕テキストを保持
        self.threshold = threshold  # 類似度のしきい値（85%以上で重複とみなす）

    def is_new(self, text: str) -> bool:
        cleaned = text.strip()  # 前後の空白を削除
        if self.last_text is None:
            self.last_text = cleaned
            return True
        # 類似度を計算
        ratio = difflib.SequenceMatcher(None, cleaned, self.last_text).ratio()
        if ratio >= self.threshold:
            return False
        self.last_text = cleaned
        return True

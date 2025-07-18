import cv2
import numpy as np
import easyocr
import re
import unicodedata
import difflib

# 字幕の重複を除外してバッファするクラス
class SubtitleBuffer:
    def __init__(self, threshold=0.92):
        self.buffer = []
        self.last_text = ""
        self.threshold = threshold

    def normalize_text(self, text):
        # 全角→半角、カタカナ統一などの正規化
        text = unicodedata.normalize("NFKC", text)
        # 記号や句読点、各種クォートを削除
        text = re.sub(r"[、。．，・_ ';:…「」『』【】（）()『』“”\"\'\-\–\—’‘‛]", "", text)
        # 空白（全角・半角、改行含む）を半角スペースに統一
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def is_duplicate(self, current_text):
        norm_current = self.normalize_text(current_text)
        norm_last = self.normalize_text(self.last_text)
        similarity = difflib.SequenceMatcher(None, norm_current, norm_last).ratio()
        return similarity >= self.threshold

    def add(self, text, timestamp):
        if not text.strip():
            return None
        if self.is_duplicate(text):
            return None
        cleaned = self.normalize_text(text)
        self.buffer.append({"timestamp": timestamp, "text": cleaned})
        self.last_text = text
        return cleaned

def increase_saturation(hsv, scale=1.5):
    """
    HSV画像の彩度(S)をscale倍に上げる関数。
    255を超えないようクリップする。
    """
    hsv_copy = hsv.copy()
    s = hsv_copy[:, :, 1].astype(np.float32)
    s = np.clip(s * scale, 0, 255).astype(np.uint8)
    hsv_copy[:, :, 1] = s
    return hsv_copy

def preprocess_frame_color_background_white_text(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_saturated = increase_saturation(hsv, scale=1.5)  # 彩度アップを適用
    lower_white = np.array([0, 0, 210])
    upper_white = np.array([180, 40, 255])
    mask_white = cv2.inRange(hsv_saturated, lower_white, upper_white)
    res_white = cv2.bitwise_and(frame, frame, mask=mask_white)
    gray_image = cv2.cvtColor(res_white, cv2.COLOR_BGR2GRAY)
    return gray_image

# extract_ocr_subtitlesはそのまま
def extract_ocr_subtitles(video_path, interval=10):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("動画が読み込めませんでした。パスを確認してください。")
        return []

    reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)
    results = []
    buffer = SubtitleBuffer()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            h, w, _ = frame.shape
            roi = frame[int(h * 0.75):h, 0:w]
            processed = preprocess_frame_color_background_white_text(roi)
            ocr_results = reader.readtext(processed)

            for (_, text, conf) in ocr_results:
                if conf < 0.5:
                    continue  # 信頼度が低いものは除外
                timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                added = buffer.add(text, timestamp)
                if added:
                    results.append({"timestamp": timestamp, "text": added})

        frame_count += 1

    cap.release()
    return results

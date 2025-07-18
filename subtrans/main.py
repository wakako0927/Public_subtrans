#main.py

from config import VIDEO_PATH, FRAME_INTERVAL
from ocr_processor import extract_ocr_subtitles
from translator import translate_chinese_to_ja
from duplicate_filter import SubtitleMemory

def main():
    # 指定動画から字幕テキストをフレーム単位で抽出
    raw_subtitles = extract_ocr_subtitles(VIDEO_PATH, interval=FRAME_INTERVAL)
    # 重複を避けるためのフィルターインスタンスを作成
    memory = SubtitleMemory()

    print("\n---翻訳結果 ---")
    for item in raw_subtitles:
        zh_text = item["text"]
        ja_text = translate_chinese_to_ja(zh_text)
    
        print(f"原文: {zh_text}")
        print(f"翻訳: {ja_text}\n")

if __name__ == "__main__":
    main()

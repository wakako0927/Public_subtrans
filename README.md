<!DOCTYPE html>
<html lang="ja">

<body>

  <h1>中国語字幕翻訳システム</h1>
  <p>本プログラムは、中国語の映像に含まれる字幕を検出・翻訳し、<br>日本語訳を表示するPythonアプリケーションです。</p>

  <h2>主な機能</h2>
  <ul>
    <li><strong>映像処理:</strong> OpenCVで映像から字幕部分を抽出</li>
    <li><strong>OCR:</strong> EasyOCRで中国語字幕を文字認識</li>
    <li><strong>重複検出:</strong> 類似度判定により重複字幕を除去</li>
    <li><strong>翻訳:</strong> OpenAI GPT-4o APIで日本語に翻訳</li>
    <li><strong>バッファ処理:</strong> 字幕の類似性をもとにフィルタリングし連結</li>
  </ul>

  <h2>ディレクトリ構成</h2>
  <pre><code>.
├── main.py                 # エントリーポイント
├── config.py               # 設定（APIキー、パス）
├── ocr_processor.py        # OCRと字幕抽出
├── translator.py           # GPTベースの翻訳
├── duplicate_filter.py     # 類似の字幕を除外
</code></pre>

  <h2> 動作要件</h2>
  <ul>
    <li>Python 3.10+</li>
    <li>OpenCV</li>
    <li>EasyOCR</li>
    <li>openai (要APIキー)</li>
    <li>GPU(CUDA環境) - OCR処理高速化のため</li>
  </ul>

  <h2>セットアップ手順</h2>
  <h3>1.リポジトリをクローン</h3>
  <pre><code>
git clone https://github.com/wakako0927/Public_subtrans
cd Public_subtrans/subtrans
</code></pre>
  <h3>2. 必要なライブラリをインストール</h3>
  <pre><code>
pip install opencv-python
pip install numpy
pip install easyocr
pip install OpenAI
</code></pre>
<h3>3. プログラムの実行</h3>
  <pre><code>python3 main.py</code></pre>
  <h2>使い方</h2>
  <ol>
    <li><code>config.py</code> にある<code>VIDEO_PATH</code>を対象の動画に設定</li>
    <li>OpenAI APIキーと使用モデル（例: gpt-4o）を記入</li>
    <li><code>main.py</code> を実行</li>
    <li>動画内の字幕がリアルタイムで翻訳・出力されます</li>
  </ol>

  <h2>翻訳のしくみ</h2>
  <p>
    字幕はOCR処理された後、<code>SubtitleBuffer</code> によって正規化・重複排除され、<code>translate_chinese_to_ja</code> により、翻訳されます。<br>ChatGPT APIのシステムプロンプトに「<ドラマタイトル>の字幕である」と明示することで、より自然な日本語を生成されるようになりました。
  </p>

  <h2>参考技術</h2>
  <ul>
    <li>OpenCV（画像処理）</li>
    <li>EasyOCR（中国語OCR）</li>
    <li>difflib（字幕の類似度比較）</li>
    <li>OpenAI GPT-4o（翻訳処理）</li>
  </ul>
  
</body>
</html>

<!DOCTYPE html>
<html lang="ja">
<body>

<header>
  <h1>中国語字幕翻訳システム</h1>
  <p class="muted">本プログラムは、中国語の映像に含まれる字幕を検出・翻訳し、<br>日本語訳を表示するPythonアプリケーションです。</p>
</header>

<section>
  <h2>特徴</h2>
  <ul>
    <li><strong>字幕検出:</strong> 自作学習の YOLOv8 モデルで字幕領域を検出</li>
    <li><strong>文字認識:</strong> EasyOCR（中国語簡体）</li>
    <li><strong>翻訳:</strong> OpenAI API による自然な日本語翻訳</li>
    <li><strong>重複除外:</strong> NFKC正規化＋編集距離＋2-gram Jaccard のハイブリッド判定</li>
  </ul>
</section>

<section>
  <h2>ディレクトリ構成</h2>
  <pre><code>.
├─ config.py            # 設定（動画パス, モデル名, DRAMA_TITLE, フレーム間隔など）
├─ duplicate_filter.py  # 重複除外ロジック（編集距離＋Jaccard）
├─ ocr_processor.py     # OCR（YOLO + EasyOCR + 重複判定）
├─ translator.py        # 翻訳処理（OpenAI API）
├─ main.py              # エントリーポイント
└─ models/best.pt       # 自作YOLOモデル（同梱, 約6MB）
</code></pre>
</section>

<section>
  <h2>セットアップ</h2>

  <h3>1) 環境</h3>
  <ul>
    <li>Python 3.10–3.12</li>
    <li>Windows / Linux（GPUは環境依存）</li>
  </ul>

  <h3>2) 依存関係</h3>
  <pre><code>pip install opencv-python numpy easyocr ultralytics openai torch torchvision torchaudio</code></pre>
  <p class="note small">PyTorch は公式インストールガイド（CPU/GPU）に従ってください。</p>

  <h3>3) OpenAI API キー</h3>
  <pre><code># PowerShell（新しいシェルを開き直す）
setx OPENAI_API_KEY "sk-xxxx"</code></pre>

  <h3>4) 設定ファイル</h3>
  <pre><code>VIDEO_PATH     = "翻訳対象のビデオ"
OPENAI_MODEL   = "gpt-4oなど"
DRAMA_TITLE    = "ビデオのタイトル名"
FRAME_INTERVAL = 5
MODEL_PATH     = "models\\best.pt"</code></pre>
  <p class="small">APIキーは環境変数 <code>OPENAI_API_KEY</code> から読み込みます。</p>
</section>

<section>
  <h2>使い方</h2>
  <pre><code>python main.py</code></pre>

  <h3>出力例</h3>
  <pre><code>原文: 如今是尸骸遍地
翻訳: 今や死体が至る所に転がっている</code></pre>
</section>

<section>
  <h2>パラメータとチューニング</h2>
  <ul>
    <li><strong>FRAME_INTERVAL:</strong> 30fps動画で <code>5</code> → 約0.16秒ごと。取りこぼしがあれば 3–6 に調整。</li>
    <li><strong>白抽出閾値:</strong> <code>S=40</code> はやや厳しめなので拾いが弱ければ <code>S=60</code> まで緩めてください。</li>
    <li><strong>GPU設定:</strong> EasyOCR は <code>gpu=False</code> で安定確認後、環境整備できたら <code>True</code>へ。</li>
  </ul>
</section>

<section>
  <h2>モデル（YOLOv8）について</h2>
  <p><code>models/best.pt</code>（約6MB）は本リポジトリに直接同梱しています。<br>GitHub の容量制限（100MB）を下回るため、追加設定不要でそのまま利用可能です。</p>

  <h3>学習データ</h3>
  <ul>
    <li>中国ドラマのスクリーンショットから自作収集</li>
    <li>クラス: <code>subtitle</code> のみ</li>
    <li>データ分割: train 400 / val 70 （test セットは別管理）</li>
    <li>YOLOフォーマット（txt, bbox座標）でアノテーション</li>
  </ul>

  <h3>学習条件</h3>
  <ul>
    <li>モデル: YOLOv8n</li>
    <li>画像サイズ: 640x640</li>
    <li>バッチサイズ: 16</li>
    <li>エポック: 約100</li>
  </ul>

  <h3>適用範囲</h3>
  <ul>
  <li>本モデルは PC 画面上の動画プレーヤー（各種サイト含）から取得した字幕領域で学習しており、<br>PC環境では汎用的に動作することを確認しています。</li>
  <li>一方で、スマートフォン画面では十分に学習していないため、検出精度が低下する可能性があります。</li>
  <li>スマホ対応を行うには、追加データによる再学習が必要です。</li>
  </ul>


  <h3>配布ポリシー</h3>
  <p>ファイルサイズが小さいため GitHub に直接含めています</p>
</section>

<section>
  <h2>内部実装のポイント</h2>
  <ul>
    <li><strong>OCR直後に重複除外：</strong> NFKC正規化＋編集距離＋2-gram Jaccard で似字・微差分を吸収</li>
    <li><strong>責務分離：</strong> 検出/認識/重複判定と翻訳/出力をモジュールで分離</li>
  </ul>
</section>

<section>
  <h2>トラブルシューティング</h2>
  <ul>
    <li>検出ゼロが続く → conf/iou 調整、白抽出閾値を緩める、間隔短縮</li>
    <li>EasyOCR (GPU) エラー → <code>gpu=False</code> で確認、CUDA版は環境整合が必要</li>
    <li>OpenAI API エラー → APIキーとモデル名を確認（利用料に注意）</li>
  </ul>
</section>

<section>
  <h2>ライセンス</h2>
  <p>MIT</p>
</section>

</body>
</html>

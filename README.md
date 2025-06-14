# mosic_ai_codex

アップロードした写真に人の顔があればモザイクをかける Web アプリです。

## 使い方

1. 依存ライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
   `uv` を利用する場合は次のように仮想環境を作成してインストールできます。
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
2. アプリを起動します。
   ```bash
   python app.py
   ```
   ポート `5000` が使用中の場合は環境変数 `PORT` で別のポート番号を指定できます。
   例: `PORT=8000 python app.py`
3. ブラウザで `http://localhost:5000` (別ポートを指定した場合はその番号) を開き、画像をアップロードすると、顔部分にモザイクがかかった画像が表示されます。

## ファイル構成
- `app.py` : Flask アプリ本体
- `templates/index.html` : アップロードフォーム
- `requirements.txt` : 必要な Python パッケージ

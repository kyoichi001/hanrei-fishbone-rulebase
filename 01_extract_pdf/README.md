# PDFからテキスト抽出・構造化

PDFからテキストを抽出し、ヘッダーとそれ以下の文に構造化したものを出力します。

## 入出力
### 入力
- PDFファイル
### 出力
- jsonファイル
    - header, header_typeとそのヘッダーに属するテキストの配列
## 各ファイルの説明

### `pdf2txt.py`
pdfからテキストのセルを抽出。そのページに含まれる文と座標のリストを出力。
### `justify_sentence.py`
セルを上から並び替え、テキストを正しい順番で読ませる
### `detect_header.py`
テキストの先頭を見て、スペースが空いていて、ヘッダーのフォーマットに一致していれば、ヘッダー候補としてマークする
### `split_section.py`
ヘッダー候補を順番に見て、順番通りに正しいものを抽出する
### `detect_header_text.py`
ヘッダーが含まれる行のテキストを、ヘッダーを修飾するテキスト（header_text）として抽出（未使用）
### `split_centence.py`
本文を「。」、『「」』、「（）」で分割する。
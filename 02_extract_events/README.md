# 係り受け解析結果からイベントを抽出

CaboChaで係り受け解析を行い、その結果をもとにイベントを抽出する。

## `process_data.py`
係り受け解析結果と、PDFの抽出結果を結合し、プログラムで扱える形に変換します。

## `mark_data.py`
結合したデータにある、文節に属性を付加させます。

### 付加させる属性
| 属性名         | 説明           | type               |
| -------------- | -------------- | ------------------ |
| `is_rentaishi` | 連体詞かどうか | `bool`             |
| `person`       | 人物           | `{text:string}`    |
| `time`         | 時間           | `長いので別途記述` |

### 属性 : 連体詞
その文節が、体言を含む文節に係る文節かどうかをDFSで判定。

時間や人物が連体詞なら無視するようにするために使用。

### 属性 : 時間
その文節に時間表現が含まれるかどうかを正規表現で判定。正規表現のルールはjsonで記述。

現在単語単位でテキストを判定。

``` TypeScript
{
    "type": "point"|"begin"|"end"|"other",
    "text": string,
    "value": number?
}
```

`value` は `type` が `point` のときのみ。

#### `point`
一点を表す時間表現。
#### `begin`
「～から」「～以降」のように、区間の開始を意味する表現。それ単体では時間を表してはいない。
#### `end`
「～まで」「～以前」のように、区間の終了を意味する表現。それ単体では時間を表してはいない。
#### `other`
「～頃」のように、時間に付加される区間以外の表現。

### 属性 : 人物
その文節に人物表現が含まれるかどうかを正規表現で判定。正規表現のルールはjsonで記述。

現在単語単位でテキストを判定。 `被告` か `原告` が含まれる単語を人物として検出。

``` TypeScript
{
    "text":string
}
```

## `extract_events.py`
文節の属性をもとに、イベントを抽出します。

イベントの条件に会う時間、人物、行動をそれぞれ抽出し、一つのイベントとして紐づけます。

### 抽出 : 時間
連体詞でない時間について抽出。区間について適切に抽出。

### 抽出 : 人物
連体詞でない人物について抽出。

### 抽出 : 行動
イベントとして抽出できた人物を基準に、順番に文節を見る。次の時間表現、人物、文末が来るまでの文節を行動として抽出。

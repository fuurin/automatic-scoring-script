# 某講義の採点プログラム

### 【最重要事項】
いかなる理由があろうと決して2次配布はしないでください.  
ほしいときはここからダウンロードしてください.

### 【ファイル内容】
###### Participant.csv:
学籍番号("ID")を含む名簿です. アップロードされているものはサンプルです.
###### grading.py:
成績評価スクリプトです. python3.xで動くと思います.


### 【実行方法】
terminalで以下のように入力すると実行可能です.  
`$ python3 grading.py [DIRECTORY_NAME]`  
DIRECTORY_NAMEの後ろには`/`をつけてもつけなくても大丈夫です．  
  
採点結果をファイルに出力することも可能です．  
`$ python3 grading.py [DIRECTORY_NAME] > textfile.txt`  
以下のオプションで示すソースコードの出力，コンパイルエラーの出力なども可能ですが，色はANSIのカラーコードのままです．  
(カラーコードをエディタ上で色に変換する方法を募集中です．)  

### 【オプション】
`-s`: ソースコードの確認 (デフォルト: False)  
`-c`: コンパイル, 実行確認のみcsvに保存しない (デフォルト: False)  
`-w`: このオプションをつけることで，評価に応じたデフォルトのコメントの行を追加できます．(デフォルト: False)  
`-t`: A評価となるコメント量の閾値を指定します．1を超える値を指定した場合は，コメントの割合ではなくコメントの行数を指定します．(デフォルト: 0.3)  
`-i`: 実行ファイルへの標準入力  
`-o`: 期待される出力結果を正規表現で指定(実験的に実装)  

`-s`に関しては,  
`$ python3 grading.py [DIRECTORY_NAME] -s`  
のように実行することでオプションが反映できます.  
`-i`に関しては,  
`$ python3 grading.py [DIRECTORY_NAME] -i "hoge 2020 3 14"`  
のように入力することで実行ファイルへ標準入力をわたすことができます.  
scanfがあるプログラムで使えます.  
`-o`に関しては，  
`$ python3 grading.py [DIRECTORY_NAME] -o 'Hello!!\nMy name is .*\n'`
のように，シングルクォーテーションで囲まれた正規表現によって期待される出力を指定します．  
例の実行コマンドであれば
```
Hello!!
My name is Hoge.
```
といった出力に対して，`Match!!!`と出力します．  
正規表現に合わなければ，`Mismatch...`と出力します．  
なお，この機能にはreモジュールの`re.search`を使用しています．  

### 【ディレクトリ構造】
```
DIRECTORY_NAME - ID1 - ex9999.c
               - ID2 - ex9999.c
               ...
```

某大学のインターネットスクールからダウンロードしてきたディレクトリの構造のまま使えば問題ないと思います.


### 【実行結果(サンプル)】
```
ID1: GRADE = A, comment/line = 90/90
ID2: GRADE = B, comment/line = 1/90
ID3: GRADE = D, comment/line = 0/0
...
```

IDx: 学籍番号  
GRADE: 評価(AA, A, B, C, D)  
commnt: コメントが書かれている行数  
line: プログラムの全行数


### 【評価方法】
GRADEは成績でAA, A, B, C, Dの5段階評価で評価基準は以下のようになっています.  
AA: コンパイルでき正しく動作でき, コメントが十分にかけている. (白色表示/デフォルトカラー)  
A: コンパイルでき正しく動作できているが, コメントが極端に少ないもの (黄色表示)  
B: コンパイルはできるが, 実行結果が正しくないもの (青色表示)  
C: プログラムにエラーがありコンパイルできないもの. (赤色表示)  
D: 未提出 (緑色表示)


### 【実行環境(確認済み)】
- OS: lubuntu 17.04
- python 3.5.3
    - pandas 0.20.3
- gcc 6.3.0

他の環境で動くかどうかは未確認です. gcc があれば動作すると思います.  
色を表示するときにANSIエスケープコード(よくわからない)を使っているので  
もしかしたら他の環境だとエラーが出るかもしれません.


### 【その他】
改良できるところ/してほしいところがあったらやってください.


### 【更新】
- 2018/02/12 : 再採点時に特定の課題を抽出するスクリプトを追加しました. クソゴミだった-lオプションは無かった事になりました.
- 2017/11/7 : -lオプションを追加しました. READMEをmdファイルに変更しました.  
- 2017/11/7 : オプションを変更しました. scanfがある場合でも実行可能(確認済み)  
- 2017/10/31: オプション引数の導入, scanfがある場合でも実行可能(未確認)  
- 2017/10/30: 実行ファイルを動作させるように変更しました. (scanf文が含まれるものに関しては未確認)  
- 2017/10/27: 公開しました.

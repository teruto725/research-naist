# code 2seq の作業ログ

シェルスクリプトで実行できるようになっているっぽいので、シェルスクリプトの入力形式を特定する

data は単なる java ファイルの集合

それを preprocessing している。

preprocessing 後のデータ形式を調べる。

c2s ファイルが生成される。おそらく code2seq の略だろう

code2seq から分析しにかかる

どうやら pickle で展開できるようだ

```

if config.LOAD_PATH:
    self.load_model(sess=None)
else:
    with open('{}.dict.c2s'.format(config.TRAIN_PATH), 'rb') as file:
        subtoken_to_count = pickle.load(file)
        node_to_count = pickle.load(file)
        target_to_count = pickle.load(file)
        max_contexts = pickle.load(file)
        self.num_training_examples = pickle.load(file)
        print('Dictionaries loaded.')

```

ただ pickle で展開した感じ結構厳しいかも？
いくつか細かい処理がいる

現状考えられるパターンは以下の通り

1. code_review 元データ(raw_data_splitted)を code2seq の preprocessing から処理していき結果を出すパターン
1. code_review 元データ(raw_data_splitted)から直接、c2s ファイルを作成し、モデルに投げるパターン
1. code2seq で中間表現だけ抽出してそれを特徴量として code_review 手法に付け加える手法
1. code2code している論文を探してそのモデルをパクる

# パターン 1 のトライ

- code2seq の難しいところをスキップできるがノイズデータの削除をやる必要がある。 is_relevant.py を使えば不可能では無いかも
- raw_data_splitted に is_relevant.ipynb でノイズデータを削除できた
- 次に code2seq の preprocessing にかける作業

問題として普通に preprocessing にかけると名前がマスキングされてしまうと思われる...
そんなことはなさそう
おそらく models.py を書き換えることで code2code のモデルにアップグレードできる可能性はある（一旦これに着手する）

一旦そこはおいておいて preprocessed ファイルを理解する必要がある

開け方がわからんので model.py から頑張って探す

render.py が怪しい（179 行目）

一回回したほうがいいかもねー

どうやら元の方は tensor1.12 らしい。めちゃくちゃ古い

もう少しライブラリ厳選をしたほうが良さそう

pytorch: https://github.com/JetBrains-Research/code2seq

一回脳死でこの pytorch 回したほうがいいかも

pytorch pip install した

一旦普通に回しておく

small-java で回してみる

エラーである。github でも同じエラーが issue にある。

tensor2.x で動く方を試してみる。:https://github.com/Kolkir/code2seq

依存ライブラリとして cppminer を試す必要があるみたい。環境構築方法が書かれてないんですが...: https://github.com/Kolkir/cppminer

cppminer は C++から code2seq 五感のデータセットを作成してくれるらしい。

submodule のインポートで解決した

次に usageError が出た。

ここで実は test.c2s の中身が見れることに気づく
get|timestamp override,Nm0|MarkerExpr|Mth|Prim1,long override,Nm0|MarkerExpr|Mth|Nm2,METHOD_NAME long,Prim1|Mth|Nm2,METHOD_NAME long,Prim1|Mth|Bk|Ret|Nm0,timestamp METHOD_NAME,Nm2|Mth|Bk|Ret|Nm0,timestamp

どうやらただの文字列だった。

この情報からコードリーディングを再開

reader.py の process_dataset が各データに対して処理しているっぽい

ラベル行方不明問題

process_file

# パターン２のトライ

openMNT にうまく組み込む必要がある。
1 のほうが簡単そうなのでそっちを優先する

# パターン 3 のトライ

ぱっと探した感じは見つからず、ありそうな感じはするが...

将来の目標として、ビジネスサイドからエンジニアサイドまで横断的に関わることでプロダクト・サービスを大きくできるエンジニアになりたいと考えています。

## 1 月 14 日の目標

### 目標

- preprocessing のりかい
  - preprocessing.sh の理解
  - preprocessing.py の理解
- 特に AST 変換部分を理解したい。

### path の抽出

AST 解析しているところを探そう！

- JavaExtractor/extract.py がっぽい

- JavaExtractor ディレクトリ
  - extract.py が実行スクリプトで os コマンドを生成。
  - 外部 Java ライブラリ, JPredict ライブラリがそれっぽい
    - README も何も入ってないんだが

TRAIN_DATA_FILE=${DATASET_NAME}.train.raw.txt
raw.txt ってなんだ？

preprocess.sh から探りを入れていく

```
python3 JavaExtractor/extract.py --dir ./data/java-small/validation --max_path_length 8 --max_path_width 2 --num_threads 64 --jar JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar > java-small.val.raw.txt 2>> error_log.txt
```

JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar が本体だと特定できたのはでかい
終盤の > ってなんだ？

よくわからないが path を作ってるだけっぽい

['java', '-Xmx100g', '-XX:MaxNewSize=60g', '-cp', 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar', 'JavaExtractor.App', '--max_path_length', '8', '--max_path_width', '2', '--dir', './data/java-small/validation/libgdx', '--num_threads', '64']

ディレクトリが一つだけだとエラーが出るようだ..

preprocess.py の起動コマンド

```
python3 preprocess.py --train_data java-small.train.raw.txt --test_data java-small.test.raw.txt --val_data java-small.val.raw.txt   --max_contexts 200 --max_data_contexts 1000 --subtoken_vocab_size 186277 --target_vocab_size 26347 --subtoken_histogram data/java-small/java-small.histo.ori.c2s --node_histogram data/java-small/java-small.histo.node.c2s --target_histogram data/java-small/java-small.histo.tgt.c2s --output_name data/java-small/java-small
```

## 1 月 21 日の目標

- preprocessing の理解。
- ast 変換を自分のディレクトリでやりたい

AST の解析を頑張る 1 ファイルで検証を行ってみる。

以下の java ファイルを解析する

```
private CloningBTreeRowBuilder(AbstractAllocator allocator)
{
    super(true);
    this.allocator = allocator;
}
```

結果はこのような AST が出力される。

```
cloning|b|tree|row|builder
row,Cls0|Cls|Mth|Nm1,METHOD_NAME row,
Cls0|Cls|Mth|Bk|Ret|ObjEx|Cls0,cloning|b|tree|row|builder row,
Cls0|Cls|Mth|Bk|Ret|ObjEx|This1,this METHOD_NAME,Nm1|Mth|Bk|Ret|ObjEx|Cls0,cloning|b|tree|row|builder METHOD_NAME,Nm1|Mth|Bk|Ret|ObjEx|This1,this cloning|b|tree|row|builder,Cls0|ObjEx|This1,this
```

メソッド名が一番始めに来る row?はよくわからんコンストラクタのことか。。。 クラス名、クラス名

ケース 2

```
@Override
public void addCell(Cell cell)
{
    super.addCell(cell.copy(allocator));
}

```

結果はこのような AST が出力される。

```
add|cell
override,Nm0|MarkerExpr|Mth|Void1,void
override,Nm0|MarkerExpr|Mth|Nm2,METHOD_NAME
void,Void1|Mth|Nm2,METHOD_NAME
void,Void1|Mth|Prm|VDID0,cell
void,Void1|Mth|Prm|Cls1,cell
METHOD_NAME,Nm2|Mth|Prm|VDID0,cell
METHOD_NAME,Nm2|Mth|Prm|Cls1,cell METHOD_NAME,Nm2|Mth|Bk|Ex|Cal0|SupEx0,super METHOD_NAME,Nm2|Mth|Bk|Ex|Cal0|Cal2|Nm0,cell METHOD_NAME,Nm2|Mth|Bk|Ex|Cal0|Cal2|Nm2,allocator METHOD_NAME,Nm2|Mth|Bk|Ex|Cal0|Cal2|Nm3,copy METHOD_NAME,Nm2|Mth|Bk|Ex|Cal0|Nm3,add|cell cell,VDID0|Prm|Cls1,cell cell,VDID0|Prm|Mth|Bk|Ex|Cal0|SupEx0,super cell,VDID0|Prm|Mth|Bk|Ex|Cal0|Cal2|Nm0,cell cell,VDID0|Prm|Mth|Bk|Ex|Cal0|Cal2|Nm2,allocator cell,VDID0|Prm|Mth|Bk|Ex|Cal0|Cal2|Nm3,copy cell,VDID0|Prm|Mth|Bk|Ex|Cal0|Nm3,add|cell cell,Cls1|Prm|Mth|Bk|Ex|Cal0|SupEx0,super cell,Cls1|Prm|Mth|Bk|Ex|Cal0|Cal2|Nm0,cell cell,Cls1|Prm|Mth|Bk|Ex|Cal0|Cal2|Nm2,allocator cell,Cls1|Prm|Mth|Bk|Ex|Cal0|Cal2|Nm3,copy cell,Cls1|Prm|Mth|Bk|Ex|Cal0|Nm3,add|cell super,SupEx0|Cal|Cal2|Nm0,cell super,SupEx0|Cal|Cal2|Nm2,allocator super,SupEx0|Cal|Cal2|Nm3,copy cell,Nm0|Cal2|Nm2,allocator cell,Nm0|Cal2|Cal|Nm3,add|cell
allocator,Nm2|Cal2|Nm3,copy
allocator,Nm2|Cal2|Cal|Nm3,add|cell
copy,Nm3|Cal2|Cal|Nm3,add|cell
```

AST 木の構造はざっくり理解した。

- スペース区切りになっている。
- 更にそれがこんまくぎりになっている。
- コンマ区切りの左側が先頭トークン、真ん中が ASTPAHT、最後が末尾トークンとなっている。必ず３つに分けられる。
- つまり 1 つのメソッドがかなり細切れになっている状態であると理解すれば OK
- あとこの時点ではマスキングがされていないことも同時に明らかとなった。

(中国語文献より)[https://www.codenong.com/cs105867383/]
code2seq レプリケーション
データ

データはスペースで区切られた行ごとに保存されます。 このうち最初の test|reset は縦線|subtoken で区切られたメソッド名で、残りの項目は AST PATH になっている。
AST PATH は、カンマで区切られた 3 つの部分から構成されています。
1 番目と 3 番目の項目は、AST PATH の先頭のトークンと末尾のトークンを縦線|subtoken で区切ったものである。
2 番目の項目は、AST PATH のノードで、これも縦線|で区切られている。

Preprocessing 自体は特に意識せずやって良さそうなので codereview を加工して DB の方に持ってくる

tran

# 1 月 28 日まで

思いつきプラン
前処理済みデータをコードに戻してざっくり書けれないか

とりあえずコードリーディング引き続きテストラベルを設定している箇所を見つけることを目的とする

まず ModelRunner(config)に注目
これの self.model がモデルでそれに train をしているここが鍵なはず

Common は static メソッドの集合体

model に遷移
build encoder
と build decoder がっぽい

この関数は引数 params に含まれる embedding 形式のテンソルの中かから、ids に該当するものを抽出するという動作を並列に実行する。

\_beam_embedding はテンソルの中から ids に該当するものを持ってくる

reader.py で各種ファイルを読み込んでいる

- process_dataset ここで関数を抜き出しているっぽい
- TARGET_STRING_KEY がそれっぽい

# print しないとまじでわからないので小規模データで回しましょ

方針

- 先行研究のデータを使って回す。なので 1_create_raw_data.ipynb と同じノリで too_small_dataset を作る

```
  df = df.head() # 10ファイルずつのみ
```

こいつを追加してもう一回１から実行する。

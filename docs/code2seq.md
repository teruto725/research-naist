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
2. code2seq で中間表現だけ抽出してそれを特徴量として code_review 手法に付け加える手法
3. code2code している論文を探してそのモデルをパクる

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

# パターン２のトライ

openMNT にうまく組み込む必要がある。
1 のほうが簡単そうなのでそっちを優先する

# パターン 3 のトライ

ぱっと探した感じは見つからず、ありそうな感じはするが...

将来の目標として、ビジネスサイドからエンジニアサイドまで横断的に関わることでプロダクト・サービスを大きくできるエンジニアになりたいと考えています。

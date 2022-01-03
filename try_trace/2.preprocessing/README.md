<!-- @format -->

# 2.preprocessing

## 概要

スクレイピングしてきた diff データを加工して ms(レビュー前のメソッド)と mr(レビュー後のメソッド)のファイルを生成する。

## 作りたいデータ

- comments.pkl

  - とりあえず情報をいっぱい付けていく
  - カラム
    - id: comment_id
    - line:
    - comment_message: コメントメッセージ
    - filepath_before: レビュー前のファイルの path
    - filepath_after: レビュー後のファイルの path
    - repository_name: リポジトリ名
    - is_gerrit: gerrit で収集したデータかどうか
    - method_name_commented: レビュー前のコメントが付いているメソッド名
    - is_included_after: method_name_before と同名のメソッドがレビュー後に追加されているか
    - is_revised_method_commented: レビュー後にレビュー前のコメントされたメソッドが修正されたか

- files/
  - コードファイルは容量が重いのでここにまとめる。
  - lizard で解析するためには単体ファイルである必要もある
    - <comment_id>\_before: レビュー前のコード
    - レビュー後のコード

ついでにいくつか不要なものは削除する。

## preprocessing 手順

1. いらないカラムを drop する（処理高速化）
1. revision 内でコメントが単一のもののみを抽出する。(これはスキップした)
1. java ファイルに対する diff のみを抽出する。
1. diff の content が無いものは削除
1. diff と comment をマージ
1. java ファイルの生成
1. lizard でメソッドリスト before の生成
1. line から method_name_commented カラムの生成
1. lizard でメソッドリスト after の生成
1. method_name_commented がメソッドリスト after に含まれているかを is_included_after に反映
1. methodlist_before != method_list_after かどうかを is_revised_method_comment に反映
1. それぞれファイルに書き込み

<!-- @format -->

# 3. Masking

src2abs ライブラリを使ってマスキングを行う。
メソッド並びにコメントに対して実施する。

## 成果物

- comments.pkl
  - とりあえず情報をいっぱい付けていく
  - カラム
    - id: comment_id
    - line:
    - message: コメントメッセージ
    - filepath_before: レビュー前のファイルの path
    - filepath_after: レビュー後のファイルの path
    - repository_name: リポジトリ名
    - is_gerrit: gerrit で収集したデータかどうか
    - method_name_commented: レビュー前のコメントが付いているメソッド名
    - is_included_after: method_name_before と同名のメソッドがレビュー後に追加されているか
    - is_revised_method_commented: レビュー後にレビュー前のコメントされたメソッドが修正されたか
    - masked_content_before: マスクされたメソッドの文字列（前）
    - masked_content_after: マスクされたメソッドの文字列（後）
    - masked_message: マスクされたメソッドの文字列

## 作業の流れ

1. src2abs を実行して masked_content_before.java と masked_content_after.java, masked_content_before.map を生成する。全部./masked_files に保管する.
1. 再度すべてを呼び出して masked_content_before と masked_content_after を埋める。
1. map ファイルに対してパーサーを定義する
1. パーサーを使って masked_message を生成する。

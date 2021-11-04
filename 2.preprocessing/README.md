<!-- @format -->

# 2.preprocessing

## 概要

スクレイピングしてきた diff データを以下のデータに加工する。

- comment.pkl
  - レビュー情報と、前後コードの filepath を持つ
  - カラム
    - id: comment_id
    - line:
    - comment_message: コメントメッセージ
    - filepath_before: レビュー前のファイルの path
    - filepath_after: レビュー後のファイルの path
    - repository_name: リポジトリ名
    - is_gerrit: gerrit で収集したデータかどうか
- files/
  - コードファイルは容量が重いのでここにまとめる。
  - lizard で解析するためには単体ファイルである必要もある
    - <comment_id>\_before: レビュー前のコード
    - レビュー後のコード

ついでにいくつか不要なものは削除する。

<!-- @format -->

# 1.Crawling

第一フェーズとしてクローリングを行う。
クローリングしてきたファイルは crawled_files に保存していく

## 成果物

- comments.csv
  - comments の基本情報を取得する。
- diff.csv
  - diff の content（ファイルの差分文字列情報）を取得する

## クローリングの流れ

- GET changes
  - changes の一覧を取得 (最終成果物には含まれない)
- GET changes/:id/comments
  - changes.id から comments の一覧を取得
  - in_reply_to があるものは除外する。（これで返信をすべて除外できる）
- GET changes/:id/comments/:id
  - changes.id と comments.id から comments.path を取得
- GET changes/:id/revisions/:id/files/:id/diff
  - changes.id と comments.commit(revisions.id)と comments.path(files.id)から diff を取得。diff が存在しないものは 404 が帰ってくるので 200 以外は除外する。
- 最終的に changes.id が主キーのテーブル、comments.id が主キーのテーブル、revisions.id と files.id が主キーのテーブルが出来上がる。

# 各データのカラム

- diff

```
 0   change_type          28750 non-null  object
 1   content              28750 non-null  object
 2   meta_a.name          28229 non-null  object
 3   meta_a.content_type  28229 non-null  object
 4   meta_a.lines         28229 non-null  float64
 5   meta_a.web_links     26691 non-null  object
 6   meta_b.name          28741 non-null  object
 7   meta_b.content_type  28741 non-null  object
 8   meta_b.lines         28741 non-null  float64
 9   meta_b.web_links     27203 non-null  object
 10  changes_id           28750 non-null  object
 11  revisions_id         28750 non-null  object
 12  path                 28750 non-null  object
 13  patch_set_a          28750 non-null  int64
 14  patch_set_b          28750 non-null  int64
 15  comments_id          28750 non-null  object
 16  diff_header          21195 non-null  object
```

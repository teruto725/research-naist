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
  - changes.id と comments.commit_id(revisions.id)と comments.path(files.id)から diff を取得。diff が存在しないものは 404 が帰ってくるので 200 以外は除外する。
- 最終的に changes.id が主キーのテーブル、comments.id が主キーのテーブル、revisions.id と files.id が主キーのテーブルが出来上がる。

# 各データのカラム

- comments api のバグで重複データ有り

```
 0   index                  30802 non-null  int64
 1   change_message_id      30802 non-null  object
 2   unresolved             30802 non-null  bool
 3   patch_set              30802 non-null  int64
 4   id                     30802 non-null  object
 5   updated                30802 non-null  object
 6   message                30802 non-null  object
 7   commit_id              30802 non-null  object コミットID=revisionID
 8   author._account_id     30802 non-null  int64
 9   author.name            30802 non-null  object
 10  author.email           30794 non-null  object
 11  author.avatars         30802 non-null  object
 12  author.status          3705 non-null   object
 13  in_reply_to            16016 non-null  object
 14  change_id              30802 non-null  object
 15  path                   30802 non-null  object
 16  line                   30802 non-null  float64
 17  range.start_line       18884 non-null  float64
 18  range.start_character  18884 non-null  float64
 19  range.end_line         18884 non-null  float64
 20  range.end_character    18884 non-null  float64
 21  side                   432 non-null    object
 22  author.username        190 non-null    object
 23  author.display_name    828 non-null    object
 24  author.inactive        213 non-null    object
 25  tag                    771 non-null    object
```

- diff それに伴って重複が発生している

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

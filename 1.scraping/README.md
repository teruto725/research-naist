<!-- @format -->

# 1.Crawling

第一フェーズとしてクローリングを行う。
生成するファイルは以下の３つ

## クローリングの流れ

- GET changes
  - changes の一覧を取得
- GET changes/:id/comments
  - changes.id から comments の一覧を取得
  - in_reply_to があるものは除外する。（これで返信をすべて除外できる）
- GET changes/:id/comments/:id
  - changes.id と comments.id から comments.path を取得
- GET changes/:id/revisions/:id/files/:id/diff
  - changes.id と comments.commit(revisions.id)と comments.path(files.id)から diff を取得。diff が存在しないものは 404 が帰ってくるので 200 以外は除外する。
- 最終的に changes.id が主キーのテーブル、comments.id が主キーのテーブル、revisions.id と files.id が主キーのテーブルが出来上がる。

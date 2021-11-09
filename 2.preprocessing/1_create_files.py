# contentからbeforeとafterのjavaファイルを切り出してくる作業

import pandas as pd

def separate_before_after(comment_id,contents):
  before = list()
  after = list()
  for content in contents:
    if "a" in content:
      after.extend(content["a"])
    elif "b" in content:
      before.extend(content["b"])
    elif "ab" in content:
      after.extend(content["ab"])
      before.extend(content["ab"])
  with open("./files/"+comment_id+"_before.java","w", encoding="utf-8") as f:
    f.write("\n".join(before))
  with open("./files/"+comment_id+"_after.java","w", encoding="utf-8") as f:
    f.write("\n".join(after))


def main():
  diff_df = pd.read_pickle("../1.scraping/scraped_files/chromium/diff.pkl")
  diff_df["has_diff"] = diff_df["content"].apply(lambda x: len(x) != 1)
  diff_df["is_java"]  = diff_df["meta_a.name"].str.contains(".java")
  df_temp = diff_df[diff_df["is_java"] & diff_df["has_diff"] ]
  [*map(lambda x: separate_before_after(x[0],x[1]), df_temp.loc[:,["comments_id","content"]].values )]

if __name__ == "__main__":
  main()

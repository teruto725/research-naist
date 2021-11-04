import pandas as pd
import pickle
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


def create_review_df():
  diff_df = pd.read_pickle("1.scraping/scraped_files/chromium/diff.pkl")
  comments_df = pd.read_pickle("1.scraping/scraped_files/chromium/comments.pkl")
  diff_df["has_diff"] = diff_df["content"].apply(lambda x: len(x) != 1) #diffを持っているか
  diff_df["is_java"]  = diff_df["meta_a.name"].str.contains(".java") # javaかどうか
  df_temp = diff_df[diff_df["is_java"] & diff_df["has_diff"] ] 
  comments_df = comments_df[diff_df[""]]
  # merge
  comments_df = comments_df.rename(columns={'id': 'comments_id'})
  merge_df = pd.merge(comments_df, df_temp)
  # データの整形
  merge_df= merge_df.loc[:,["comments_id","line","message","range.start_line","range.end_line"]]
  merge_df["filepath_before"] = merge_df["comments_id"].apply(lambda x: x+"_before.java")
  merge_df["filepath_after"] = merge_df["comments_id"].apply(lambda x: x+"_after.java")
  merge_df["is_gerrit"] = True
  merge_df["repository_name"] = "chromium"
  merge_df.to_pickle("2/preprocessing/review_df.pkl")

if __name__ == "__main__":
  create_review_df()



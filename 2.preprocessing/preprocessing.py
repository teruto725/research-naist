import lizard
import pandas as pd
import os
import shutil

comments_read_df = pd.read_pickle("../1.crawling/scraped_files/chromium/comments.pkl")
diff_read_df = pd.read_pickle("../1.crawling/scraped_files/chromium/diff.pkl")


# いらないカラムをdropする
comments_df = comments_read_df.loc[:,["id","line","message","range.start_line","range.end_line"]] 
diff_df = diff_read_df.loc[:,["comments_id","content","changes_id","revisions_id","path"]]

# 重複削除
comments_df = comments_df[comments_df.duplicated()]
diff_df = diff_df[diff_df["comments_id"].duplicated()]


# javaファイルに関するdiffのみを抽出する
diff_df = diff_df
diff_df = diff_df[diff_df["path"].str.contains(".java")]
diff_df.info()

# diffのcontentが無いものは削除
diff_df = diff_df[diff_df["content"].apply(lambda x: len(x) != 1)]

# diffとcommentをマージ
comments_df = comments_df.rename(columns={'id': 'comments_id'})
comments_df = pd.merge(comments_df, diff_df)

# javaファイルの作成
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
  with open("./java_files/"+comment_id+"_before.java","w", encoding="utf-8") as f:
    f.write("\n".join(before))
  with open("./java_files/"+comment_id+"_after.java","w", encoding="utf-8") as f:
    f.write("\n".join(after))

shutil.rmtree("./java_files/")
os.mkdir("./java_files/")
[*map(lambda x: separate_before_after(x[0],x[1]), comments_df.loc[:,["comments_id","content"]].values )]
comments_df["filepath_before"] = comments_df["comments_id"].apply(lambda x: x+"_before.java")
comments_df["filepath_after"] = comments_df["comments_id"].apply(lambda x: x+"_after.java")

#  lineからmethod_name_commentedカラムの生成
def read_file_as_list(file_path):
  f = open(file_path, 'r')
  lines = f.readlines()
  f.close()
  return lines

# ファイルをlistで保存
def save_list_as_file(file_path,li):
  with open(file_path,"w", encoding="utf-8") as f:
    f.write("".join(li))

def get_methods_name_commented(filepath,line):
  
  liz = lizard.analyze_file("./java_files/"+filepath)
  for i,liz_func in enumerate(liz.function_list):
    start_line = liz_func.__dict__["start_line"]
    end_line = liz_func.__dict__["end_line"]
    if start_line <= int(line) and line <= end_line:
      return liz_func.__dict__["name"]
  #print("None")
  return "None"

comments_df["method_name_commented"] = comments_df.loc[:,["filepath_before","line"]].apply(lambda x:get_methods_name_commented(x[0],x[1]), axis=1)
comments_df = comments_df[comments_df["method_name_commented"] != "None"]


#  lineからmethod_name_commentedカラムの生成
def is_included_after(filepath,method_name):
  liz = lizard.analyze_file("./java_files/"+filepath)
  for i,liz_func in enumerate(liz.function_list):
    if liz_func.__dict__["name"] == method_name:
      return True
  return False

comments_df["is_included_after"] = comments_df.loc[:,["filepath_after","method_name_commented"]].apply(lambda x:is_included_after(x[0],x[1]), axis=1)
comments_df = comments_df[comments_df["is_included_after"]]


# methodslist_before != method_list_afterかどうかをis_revised_method_commentに反映
# ファイルをlistで保存
def save_list_as_file(file_path,li):
  with open(file_path,"w", encoding="utf-8") as f:
    f.write("".join(li))


def is_included_after(filepath_before,filepath_after,method_name):
  liz_before = lizard.analyze_file("./java_files/"+filepath_before)
  file_before_li = read_file_as_list("./java_files/"+filepath_before)
  liz_after = lizard.analyze_file("./java_files/"+filepath_after)
  file_after_li = read_file_as_list("./java_files/"+filepath_after)
  before_s = ""
  after_s = ""
  for i,liz_func in enumerate(liz_before.function_list):
    if liz_func.__dict__["name"] == method_name:
      start_line = liz_func.__dict__["start_line"]
      end_line = liz_func.__dict__["end_line"]
      methods = file_before_li[start_line-1:end_line]
      before_s = "".join(methods)
      save_list_as_file("./methods/"+filepath_before,methods)
      break
  for i,liz_func in enumerate(liz_after.function_list):
    if liz_func.__dict__["name"] == method_name:
      start_line = liz_func.__dict__["start_line"]
      end_line = liz_func.__dict__["end_line"]
      methods = file_after_li[start_line-1:end_line]
      after_s = "".join(methods)
      save_list_as_file("./methods/"+filepath_after,methods)
      break
  if before_s ==after_s:
    return False
  return True
shutil.rmtree("./methods/")
os.mkdir("./methods/")
comments_df["is_revised_method_comment"] = comments_df.loc[:,["filepath_before","filepath_after","method_name_commented"]].apply(lambda x:is_included_after(x[0],x[1],x[2]), axis=1)
comments_df = comments_df[comments_df["is_revised_method_comment"]]


# ファイル保存
comments_df.to_pickle("./comments.pkl",index=False)
comments_df.to_csv("./comments.csv",index=False)
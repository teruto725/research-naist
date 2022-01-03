import pandas as pd
import subprocess
import os
import shutil

# commentsの読み込み
comments_df = pd.read_pickle("../2.preprocessing/comments.pkl")

# src2mbsによるマスキング
shutil.rmtree("./masked_files/")
os.mkdir("./masked_files/")
def masking(comments_id):
  input_file_path_A = "../2.preprocessing/java_files/"+comments_id+"_before.java"
  output_file_path_A = "./masked_files/"+comments_id+"_before.java"
  input_file_path_B = "../2.preprocessing/java_files/"+comments_id+"_after.java"
  output_file_path_B = "./masked_files/"+comments_id+"_after.java"
  cp = subprocess.run(["java", "-jar","src2abs-0.1-jar-with-dependencies.jar", "pair","method",input_file_path_A, input_file_path_B,output_file_path_A,output_file_path_B,"./idioms.csv"])

_ = comments_df["comments_id"].apply(lambda x: masking(x))

# マスキング結果をカラムに格納
def load_masked_file(filepath):
  with open("./masked_files/"+filepath,"r", encoding="utf-8") as f:
    return f.read()
  
comments_df["masked_content_before"]= comments_df["filepath_before"].apply(lambda x: load_masked_file(x))
comments_df["masked_content_after"] = comments_df["filepath_after"].apply(lambda x: load_masked_file(x))


#　mapファイルから辞書を作ってコメントのマスキング
def map_perser(filepath):
  lines = list()
  with open("./masked_files/"+filepath+".map","r", encoding="utf-8") as f:
    lines = list(map(lambda x: x.rstrip("\n"),f.readlines()))
  di = dict()
  for i in range(0,len(lines)-1,2):
    if lines[i] =="":
      continue
    keys = lines[i].split(",")
    values = lines[i+1].split(",")
    di_temp = dict(zip(keys, values))
    di.update(di_temp)
  if '' in di:
    di.pop('')
  return di

def masking_message(message, filepath):
  di = map_perser(filepath)
  for k,v in di.items():
    message = message.replace(k,v)
  return message

comments_df["masked_message"] = comments_df.loc[:,["message","filepath_before"]].apply(lambda x: masking_message(x[0],x[1]),axis=1)

# ファイル保存
comments_df.to_csv("./comments.csv")
comments_df.to_pickle("./comments.pkl")
import pandas as pd
import lizard

def read_file_as_list(file_path):
  f = open(file_path, 'r')
  lines = f.readlines()
  f.close()
  return lines

# ファイルをlistで保存
def save_list_as_file(file_path,li):
  with open(file_path,"w", encoding="utf-8") as f:
    f.write("".join(li))

def get_methods(filepath):
  file_li = read_file_as_list("./files/"+filepath)
  
  liz = lizard.analyze_file("./files/"+filepath)
  for i,liz_func in enumerate(liz.function_list):
    start_line = liz_func.__dict__["start_line"]
    end_line = liz_func.__dict__["end_line"]
    methods = file_li[start_line-1:end_line]
    save_list_as_file("./methods/"+filepath.rsplit("_",1)[0]+"_"+str(i)+"_"+filepath.rsplit("_",1)[1],methods)
  return len(liz.function_list)



def masking_methods():
  df = pd.read_pickle("./review_df.pkl")
  df["methods_before_count"] = df["filepath_before"].apply(lambda x:get_methods(x))
  df["methods_after_count"]  =  df["filepath_after"].apply(lambda x:get_methods(x))
  df.to_pickle("./3_review_df.pkl")
  df.to_csv("./3_review_df.csv")


if __name__ == "__main__":
  masking_methods()
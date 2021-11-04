import requests
import pprint
import json
import numpy as np
import pandas as pd

"""
commentsからdiffを収集する

"""


def get_to_uri(endpoint, uri = "https://chromium-review.googlesource.com/" ):
  response = requests.get(uri+endpoint)
  return response


comments_df = pd.read_pickle("./scraping/scraped_files/comments.pkl")


df = None
rows = comments_df.loc[:,["change_id","commit_id","path","patch_set","id"]].values
for i,row in enumerate(rows):
  response = get_to_uri("changes/"+row[0]+"/revisions/"+str(row[3])+"/files/"+row[2].replace("/", "%2f")+"/diff?base="+str(row[3]+1))
  if response.status_code != 200:
    continue

  content = response.content.decode("utf-8").split("\n")[1]
  di = json.loads(content.split("\n")[0])
  df_temp = pd.json_normalize(di)
  df_temp["changes_id"] = row[0]
  df_temp["revisions_id"] = row[1]
  df_temp["path"] = row[2]
  df_temp["patch_set_a"] = row[3]+1
  df_temp["patch_set_b"] = row[3]
  df_temp["comments_id"] = row[4]
  if df is None:
    df = df_temp
    continue
  df = pd.concat([df,df_temp])
  if i % 100 == 0:
    print(i)
df = df.reset_index(drop=True)
df.to_pickle("./scraping/scraped_files/diff.pkl")
df.to_csv("./scraping/scraped_files/diff.csv")
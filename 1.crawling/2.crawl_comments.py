import requests
import pprint
import json
import numpy as np
import pandas as pd

"""
changes_idsからcommentsを収集する

"""


def get_to_uri(endpoint, uri = "https://chromium-review.googlesource.com/" ):
  response = requests.get(uri+endpoint)
  return response


change_ids = pd.read_pickle("./scraping/scraped_files/changes.pkl").id.values
df = None
for i,change_id in enumerate(change_ids):
  response = get_to_uri("changes/"+change_id+"/comments")
  if response.status_code != 200:
    continue

  content = response.content.decode("utf-8").split("\n")[1]
  di = json.loads(content.split("\n")[0])
  for key in di.keys(): #pathでfor回す
    df_temp = pd.json_normalize(di[key])
    df_temp["change_id"]  = change_id
    df_temp["path"] = key
    if df is None:
      df = df_temp
      continue
    df = pd.concat([df,df_temp])
    if i % 500 == 0:
      print(i)
df = df[pd.isnull(df["line"]) == False]
df = df.reset_index(drop=True)
df.to_pickle("./scraping/scraped_files/comments.pkl")
df.to_csv("./scraping/scraped_files/comments.csv")

# changes_pickleの解凍
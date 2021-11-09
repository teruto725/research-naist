import requests
import pprint
import json
import numpy as np
import pandas as pd



def get_to_uri(endpoint, uri = "https://review.opendev.org/" ):
  response = requests.get(uri+endpoint)
  return response

def to_pd_from_response(response):
  content = response.content.decode("utf-8").split("\n")[1]
  di = json.loads(content.split("\n")[0])
  df = pd.json_normalize(di)
  return df

df = None
i = 0
while True:
  response = get_to_uri("changes/?start="+str(i))
  if response.status_code != 200:
    break
  df_temp = to_pd_from_response(response)
  if df is None:
    df = df_temp
    continue
  if df_temp.empty:
    break
  df = pd.concat([df,df_temp])
  df.append(df)
  i += 500
  print(i)
df = df.reset_index(drop=True)
df.to_pickle("./scraping/scraped_files/opendev/changes.pkl")
df.to_csv("./scraping/scraped_files/opendev/changes.csv")

"""
changes_idsからcommentsを収集する

"""

del df

change_ids = pd.read_pickle("./scraping/scraped_files/opendev/changes.pkl").id.values
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
df.to_pickle("./scraping/scraped_files/opendev/comments.pkl")
df.to_csv("./scraping/scraped_files/opendev/comments.csv")


del change_ids
del df


"""
commentsからdiffを収集する

"""

comments_df = pd.read_pickle("./scraping/scraped_files/opendev/comments.pkl")

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
df.to_pickle("./scraping/scraped_files/opendev/diff.pkl")
df.to_csv("./scraping/scraped_files/opendev/diff.csv")
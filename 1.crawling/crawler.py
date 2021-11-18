import requests
import json
import numpy as np
import pandas as pd
import sys
import sqlite3 as sql

REPO_URL = ""
REPO_NAME = ""
DBNAME = "crawl_db.sqlite3"

def get_to_uri(endpoint, uri = REPO_URL +"/" ):
  response = requests.get(uri+endpoint)
  return response

def to_pd_from_response(response):
  content = response.content.decode("utf-8").split("\n")[1]
  di = json.loads(content.split("\n")[0])
  df = pd.json_normalize(di)
  return df


"""
changesを取得する
"""
def crawling_changes():
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
  change_ids = df.id.values
  return change_ids


"""
changes_idsからcommentsを収集する

"""

def crawling_comments(change_ids):
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
      df_temp["repo_name"] = REPO_NAME 
      if df is None:
        df = df_temp
        continue
      df = pd.concat([df,df_temp])
      if i % 500 == 0:
        print(i)
  df = df[pd.isnull(df["line"]) == False]
  df = df.reset_index(drop=True)
  df = df.loc[:,["change_message_id","unresolved","patch_set","id","message","commit_id","in_reply_to","change_id","path","line","range.start_line","range.end_line","repo_name"]]
  with sql.connect("crawl_db.sqlite3") as conn:
    df.to_sql("COMMENT", con=conn, if_exists='append')
  return df


"""
commentsからdiffを収集する

"""
def crawling_diffs(comments_df):

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
    df_temp["repo_name"] = REPO_NAME
    if df is None:
      df = df_temp
      continue
    df = pd.concat([df,df_temp])
    if i % 100 == 0:
      print(i)
  df = df.reset_index(drop=True)

  df = df.loc[:,["change_type","content","changes_id","revisions_id","path","patch_set_a","patch_set_b","comments_id"]]
  df["content"] = df["content"].astype("str")
  with sql.connect("crawl_db.sqlite3") as conn:
    df.to_sql("DIFF", con=conn, if_exists='append')

  del df

if __name__ == "__main__":
  REPO_URL = sys.argv[1]
  REPO_NAME = sys.argv[2]
  print("crawling_changes")
  change_ids = crawling_changes()
  print("crawling_commnets")
  comments_df = crawling_comments(change_ids)
  print("crawling_diffs")
  crawling_diffs(comments_df)
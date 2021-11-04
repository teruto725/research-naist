import requests
import pprint
import json
import numpy as np
import pandas as pd

def get_to_uri(endpoint, uri = "https://chromium-review.googlesource.com/" ):
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
  df = pd.concat([df,df_temp])
  df.append(df)
  i += 500
  print(i)
df = df.reset_index(drop=True)
df.to_pickle("./scraping/scraped_files/changes.pkl")
df.to_csv("./scraping/scraped_files/changes.csv")
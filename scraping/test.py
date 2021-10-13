import requests
import pprint
import json
import numpy as np
import pandas as pd
uri = "https://codereview.qt-project.org/projects/"

def json_parser(content):
  content = content.decode("utf-8").split("\n")[1]
  
  
  di = json.loads(content.split("\n")[0])
  data = pd.DataFrame(di)
  


response = requests.get(uri)
json_parser(response.content)

# dataframeに変換するメソッド
def convertResponseToDF(response):
  content = response.content.decode("utf-8").split("\n")[1]
  di = json.loads(content.split("\n")[0])
  df = pd.DataFrame(di)
  return di,df
# uriを叩くためのメソッド
def get_to_uri(endpoint, uri = "https://chromium-review.googlesource.com/" ):
  response = requests.get(uri+endpoint)
  print(response.status_code)
  return response